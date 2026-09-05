"""Resolve the real installed font face before measuring or writing its name."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from fontTools.ttLib import TTCollection, TTFont, TTLibError
from PIL import ImageFont

from .scene import InputError

DEFAULT_LATIN = ["Arial", "Aptos", "Liberation Sans", "DejaVu Sans", "Noto Sans"]
DEFAULT_CJK = [
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "Microsoft YaHei",
    "PingFang SC",
    "Heiti SC",
    "Arial Unicode MS",
]


def is_cjk(text: str) -> bool:
    return any(unicodedata.east_asian_width(c) in {"W", "F"} for c in text)


@dataclass(frozen=True)
class FontFace:
    path: str
    index: int
    family: str
    aliases: tuple[str, ...]
    weight: int
    italic: bool

    @property
    def key(self) -> tuple[str, int]:
        return self.path, self.index


def font_candidates(extra_dirs: tuple[Path, ...] = ()) -> list[tuple[str, int]]:
    candidates = set()
    if shutil.which("fc-list"):
        result = subprocess.run(
            ["fc-list", "--format=%{file}\t%{index}\n"],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        for line in result.stdout.splitlines():
            fields = line.rsplit("\t", 1)
            if len(fields) == 2 and fields[1].isdigit() and int(fields[1]) < 65536:
                candidates.add((fields[0], int(fields[1])))
    roots = list(extra_dirs)
    if not candidates:
        roots += [
            Path("/System/Library/Fonts"),
            Path("/Library/Fonts"),
            Path.home() / "Library/Fonts",
            Path("/usr/share/fonts"),
            Path("/usr/local/share/fonts"),
            Path.home() / ".local/share/fonts",
            Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
        ]
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() not in {".ttf", ".otf", ".ttc", ".otc"} or not path.is_file():
                continue
            count = 1
            if path.suffix.lower() in {".ttc", ".otc"}:
                try:
                    collection = TTCollection(path, lazy=True)
                    count = len(collection.fonts)
                    collection.close()
                except (TTLibError, OSError):
                    continue
            candidates.update((str(path.resolve()), index) for index in range(count))
    return sorted(candidates)


@lru_cache(maxsize=4)
def discover_fonts(extra_dirs: tuple[Path, ...] = ()) -> tuple[FontFace, ...]:
    faces = []
    for path, index in font_candidates(extra_dirs):
        if Path(path).suffix.lower() not in {".ttf", ".otf", ".ttc", ".otc"}:
            continue
        try:
            with TTFont(path, fontNumber=index, lazy=True) as font:
                names = font["name"]
                family = names.getDebugName(16) or names.getDebugName(1)
                if not family or family.startswith("."):
                    continue
                aliases = tuple(sorted({n.toUnicode() for n in names.names if n.nameID in {1, 16}}))
                weight = int(font["OS/2"].usWeightClass) if "OS/2" in font else 400
                italic = bool(font["OS/2"].fsSelection & 1) if "OS/2" in font else False
                faces.append(FontFace(path, index, family, aliases, weight, italic))
        except (OSError, TTLibError, KeyError, UnicodeError):
            continue
    if not faces:
        raise InputError("No usable TrueType/OpenType fonts found; provide --font-dir")
    return tuple(faces)


@lru_cache(maxsize=128)
def glyphs(face: FontFace) -> frozenset[int]:
    with TTFont(face.path, fontNumber=face.index, lazy=True) as font:
        return frozenset(font.getBestCmap() or {})


@lru_cache(maxsize=1024)
def pil_font(face: FontFace, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(face.path, size=size * 4, index=face.index)


def measure(face: FontFace, text: str, size: float) -> tuple[float, float, float]:
    font = pil_font(face, round(size, 4))
    ascent, descent = font.getmetrics()
    if not text:
        return 0, ascent / 4, descent / 4
    bbox = font.getbbox(text)
    width = max(font.getlength(text), bbox[2]) - min(0, bbox[0])
    return width / 4, ascent / 4, descent / 4


@lru_cache(maxsize=1024)
def ink_bounds(face: FontFace, text: str, size: float) -> tuple[float, float, float, float] | None:
    """Visible ink relative to the baseline, excluding blank punctuation/space advance."""
    width, ascent, descent = measure(face, text, size)
    if not text.strip() or width * (ascent + descent) * 16 > 8_000_000:
        return None
    mask, offset = pil_font(face, size).getmask2(text, anchor="ls")
    bounds = mask.getbbox()
    if bounds is None:
        return None
    return tuple((bounds[i] + offset[i % 2]) / 4 for i in range(4))


@lru_cache(maxsize=128)
def east_asian_name(face: FontFace) -> str:
    with TTFont(face.path, fontNumber=face.index, lazy=True) as font:
        names = font["name"]
        for language in [2052, 1028]:
            for name_id in [16, 1]:
                value = names.getName(name_id, 3, 1, language)
                if value is not None:
                    return value.toUnicode()
    return face.family


def normalize_font_name(value: str) -> str:
    return "".join(c for c in re.sub(r"^[A-Z]{6}\+", "", value) if c.isalnum()).casefold()


@lru_cache(maxsize=128)
def font_identifiers(face: FontFace) -> frozenset[str]:
    with TTFont(face.path, fontNumber=face.index, lazy=True) as font:
        return frozenset(
            normalize_font_name(n.toUnicode())
            for n in font["name"].names
            if n.nameID in {1, 4, 6, 16}
        )


class FontCatalog:
    def __init__(self, preferences: dict | None = None, extra_dirs: tuple[Path, ...] = ()):
        self.faces = discover_fonts(extra_dirs)
        preferences = {} if preferences is None else preferences
        self.preferences = {
            "latin": preferences.get("latin", DEFAULT_LATIN),
            "cjk": preferences.get("cjk", DEFAULT_CJK),
        }
        self.by_name: dict[str, list[FontFace]] = {}
        for face in self.faces:
            for alias in {*face.aliases, face.family}:
                self.by_name.setdefault(alias.casefold(), []).append(face)
        self.used: set[FontFace] = set()
        self.events: set[tuple[str, str, str]] = set()
        self.resolve = lru_cache(maxsize=8192)(self.resolve)

    def resolve(
        self, cluster: str, family: str | None, cjk_family: str | None, bold: bool, italic: bool
    ) -> FontFace:
        script = "cjk" if is_cjk(cluster) else "latin"
        requested = cjk_family if script == "cjk" and cjk_family else family
        candidates = ([requested] if requested else []) + self.preferences[script]
        required = {
            ord(c)
            for c in cluster
            if not c.isspace() and unicodedata.category(c) not in {"Cf", "Mn", "Me"}
        }
        # Combining marks are required too; variation selectors are not standalone glyphs.
        required |= {
            ord(c)
            for c in cluster
            if unicodedata.category(c) in {"Mn", "Me"} and not 0xFE00 <= ord(c) <= 0xFE0F
        }
        for name in dict.fromkeys(candidates):
            faces = sorted(
                self.by_name.get(name.casefold(), []),
                key=lambda f: (
                    f.italic != italic,
                    abs(f.weight - (700 if bold else 400)),
                    f.path,
                    f.index,
                ),
            )
            for face in faces:
                if required <= glyphs(face):
                    if requested and name.casefold() != requested.casefold():
                        self.events.add(("font_substitution", requested, face.family))
                    if face.italic != italic or (bold and face.weight < 600):
                        self.events.add(("synthetic_font_style", name, face.family))
                    self.used.add(face)
                    return face
        codepoints = " ".join(f"U+{c:04X}" for c in sorted(required))
        raise InputError(
            f"No configured font covers {cluster!r} ({codepoints}); install a suitable font or set fonts.{script}"
        )

    def manifest(self) -> dict:
        records = []
        for face in sorted(self.used, key=lambda f: (f.family, f.weight, f.path, f.index)):
            with TTFont(face.path, fontNumber=face.index, lazy=True) as font:
                fs_type = int(font["OS/2"].fsType) if "OS/2" in font else None
            records.append(
                {
                    "family": face.family,
                    "east_asian_typeface": east_asian_name(face),
                    "file": Path(face.path).name,
                    "face_index": face.index,
                    "weight": face.weight,
                    "italic": face.italic,
                    "sha256": hashlib.sha256(Path(face.path).read_bytes()).hexdigest(),
                    "embedding_fs_type": fs_type,
                }
            )
        return {
            "embedded": False,
            "fonts": records,
            "substitutions": [
                {"code": code, "requested": requested, "resolved": resolved}
                for code, requested, resolved in sorted(self.events)
            ],
            "portability": "Install the listed font families on the editing computer. Font files are not copied or embedded.",
        }
