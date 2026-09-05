"""Optional local OCR backends. Recognition boxes are ink, not text-frame bounds."""

from __future__ import annotations

import csv
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Protocol

from .scene import InputError


class OcrBackend(Protocol):
    def recognize(self, image: Path) -> list[dict]: ...


class VisionOcr:
    def __init__(self, languages: str | None = None):
        self.languages = "zh-Hans,en-US" if languages is None else languages

    def recognize(self, image: Path) -> list[dict]:
        script = Path(__file__).with_name("vision_ocr.swift")
        result = subprocess.run(
            ["swift", str(script), str(image.resolve()), self.languages],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if result.returncode:
            raise InputError(f"Local Vision OCR failed: {result.stderr[-1000:]}")
        return json.loads(result.stdout)


class TesseractOcr:
    def __init__(self, languages: str | None = None):
        self.languages = "eng" if languages is None else languages

    def recognize(self, image: Path) -> list[dict]:
        result = subprocess.run(
            [
                "tesseract",
                str(image.resolve()),
                "stdout",
                "-l",
                self.languages,
                "--psm",
                "11",
                "tsv",
            ],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if result.returncode:
            raise InputError(f"Tesseract OCR failed: {result.stderr[-1000:]}")
        groups: dict[tuple, list] = {}
        for row in csv.DictReader(
            io.StringIO(result.stdout), delimiter="\t", quoting=csv.QUOTE_NONE
        ):
            if row.get("level") != "5" or not row.get("text", "").strip():
                continue
            key = tuple(row[k] for k in ["page_num", "block_num", "par_num", "line_num"])
            groups.setdefault(key, []).append(row)
        lines = []
        for words in groups.values():
            left = min(int(w["left"]) for w in words)
            top = min(int(w["top"]) for w in words)
            right = max(int(w["left"]) + int(w["width"]) for w in words)
            bottom = max(int(w["top"]) + int(w["height"]) for w in words)
            lines.append(
                {
                    "text": " ".join(w["text"] for w in words),
                    "confidence": sum(max(0, float(w["conf"])) for w in words) / len(words) / 100,
                    "box": [left, top, right - left, bottom - top],
                }
            )
        return lines


BACKENDS = {"vision": VisionOcr, "tesseract": TesseractOcr}


def choose_backend(name: str, languages: str | None = None) -> tuple[str, OcrBackend | None]:
    if name == "auto":
        if sys.platform == "darwin" and shutil.which("swift"):
            name = "vision"
        elif shutil.which("tesseract"):
            name = "tesseract"
        else:
            name = "none"
    if name == "none":
        return name, None
    if name not in BACKENDS:
        raise InputError(f"Unknown OCR backend: {name}")
    return name, BACKENDS[name](languages)
