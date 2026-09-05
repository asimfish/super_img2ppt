"""Render the emitted PPTX, then inspect text in the renderer's PDF."""

from __future__ import annotations

import ctypes
import shutil
import subprocess
import tempfile
from contextlib import closing
from pathlib import Path
from typing import Protocol

import pypdfium2 as pdfium

from .fonts import font_identifiers, normalize_font_name
from .layout import text_ink_boxes
from .qa import compact_text
from .scene import InputError, slide_transform, text_content


class Renderer(Protocol):
    def render(self, source: Path, out_dir: Path) -> Path: ...


class LibreOfficeRenderer:
    def __init__(self, executable: str | None = None, timeout: int = 120):
        self.executable = executable if executable is not None else shutil.which("soffice")
        if not self.executable:
            raise InputError(
                "LibreOffice is not available. Install it for real PPTX validation; use --no-render only for an explicitly unverified draft"
            )
        self.timeout = timeout

    def render(self, source: Path, out_dir: Path) -> Path:
        out_dir.mkdir(parents=True, exist_ok=True)
        result_path = out_dir / (source.stem + ".pdf")
        if result_path.exists():
            raise InputError("Renderer destination already exists")
        with tempfile.TemporaryDirectory(prefix="super-img2ppt-office-") as tmp:
            profile = Path(tmp) / "profile"
            # Separate profile prevents interference with an open user presentation.
            command = [
                self.executable,
                f"-env:UserInstallation={profile.as_uri()}",
                "--headless",
                "--nologo",
                "--nodefault",
                "--nolockcheck",
                "--norestore",
                "--convert-to",
                "pdf:impress_pdf_Export",
                "--outdir",
                str(out_dir.resolve()),
                str(source.resolve()),
            ]
            try:
                result = subprocess.run(
                    command, capture_output=True, text=True, timeout=self.timeout, check=False
                )
            except subprocess.TimeoutExpired as exc:
                raise InputError(f"Office rendering exceeded {self.timeout} seconds") from exc
            if result.returncode != 0 or not result_path.is_file():
                raise InputError(
                    f"Office rendering failed: {(result.stderr + result.stdout)[-1500:]}"
                )
        return result_path


RENDERERS = {"libreoffice": LibreOfficeRenderer}


def make_renderer(name: str = "libreoffice") -> Renderer:
    try:
        factory = RENDERERS[name]
    except KeyError as exc:
        raise InputError(f"Unknown renderer: {name}") from exc
    return factory()


def rasterize_pdf(source: Path, out_dir: Path, width: int = 1600) -> list[Path]:
    pages = []
    with pdfium.PdfDocument(source) as document:
        if len(document) > 200:
            raise InputError("PDF exceeds 200 pages")
        for index in range(len(document)):
            with closing(document[index]) as page:
                w, h = page.get_size()
                if w <= 0 or h <= 0:
                    raise InputError("PDF has an invalid page size")
                scale = min(width / w, 4000 / h)
                bitmap = page.render(scale=scale)
                try:
                    image = bitmap.to_pil()
                    path = out_dir / f"page_{index + 1:03d}.png"
                    image.save(path)
                    pages.append(path)
                finally:
                    bitmap.close()
    return pages


def verify_rendered_text(pdf: Path, scene: dict, layouts: dict | None = None) -> dict:
    findings = []
    boxes = []
    with pdfium.PdfDocument(pdf) as document:
        if len(document) != len(scene["slides"]):
            return {
                "status": "fail",
                "findings": [{"code": "rendered_slide_count_mismatch"}],
                "text_boxes": [],
            }
        for index, slide in enumerate(scene["slides"]):
            tx = slide_transform(scene, slide)
            with closing(document[index]) as page, closing(page.get_textpage()) as textpage:
                pw, ph = page.get_size()
                for element in slide["elements"]:
                    if element["kind"] != "text":
                        continue
                    ix, iy, iw, ih = tx.box(element["box"])
                    left = ix / tx.width_inches * pw
                    top = ph - iy / tx.height_inches * ph
                    right = left + iw / tx.width_inches * pw
                    bottom = top - ih / tx.height_inches * ph
                    extracted = textpage.get_text_bounded(
                        left=left, bottom=bottom, right=right, top=top
                    )
                    expected = compact_text(text_content(element))
                    actual = compact_text(extracted)
                    matched = expected in actual
                    boxes.append(
                        {
                            "slide": slide["id"],
                            "element": element["id"],
                            "expected": text_content(element),
                            "rendered": extracted,
                            "matches": matched,
                        }
                    )
                    if not matched:
                        findings.append(
                            {
                                "code": "rendered_text_mismatch",
                                "slide": slide["id"],
                                "element": element["id"],
                                "message": "Expected text is absent or outside its box in the actual renderer PDF",
                            }
                        )
                    # Bounded extraction selects character centers; check visible glyph extents too.
                    overflow = []
                    expected_fonts: dict[str, set[str]] = {}
                    if layouts is not None:
                        for line in layouts[slide["id"], element["id"]].lines:
                            for fragment in line.fragments:
                                for char in fragment.text:
                                    expected_fonts.setdefault(char, set()).update(
                                        font_identifiers(fragment.face)
                                    )
                    observed_fonts = set()
                    substituted_fonts = set()
                    rendered_ink = []
                    for char_index in range(textpage.count_chars()):
                        char = textpage.get_text_range(char_index, 1)
                        if not char.strip():
                            continue
                        x0, y0, x1, y1 = textpage.get_charbox(char_index)
                        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                        if left <= cx <= right and bottom <= cy <= top:
                            rendered_ink.append((x0, x1))
                            length = pdfium.raw.FPDFText_GetFontInfo(
                                textpage, char_index, None, 0, None
                            )
                            if length:
                                buffer = ctypes.create_string_buffer(length)
                                pdfium.raw.FPDFText_GetFontInfo(
                                    textpage, char_index, buffer, length, None
                                )
                                name = buffer.value.decode("utf-8", errors="replace")
                                observed_fonts.add(name)
                                if (
                                    char in expected_fonts
                                    and normalize_font_name(name) not in expected_fonts[char]
                                ):
                                    substituted_fonts.add(name)
                        if (
                            left <= cx <= right
                            and bottom <= cy <= top
                            and (
                                x0 < left - 0.75
                                or x1 > right + 0.75
                                or y0 < bottom - 0.75
                                or y1 > top + 0.75
                            )
                        ):
                            overflow.append(char)
                    if overflow:
                        findings.append(
                            {
                                "code": "rendered_glyph_overflow",
                                "slide": slide["id"],
                                "element": element["id"],
                                "glyphs": "".join(overflow),
                                "message": "Rendered glyph ink crosses the text box by more than 0.75 pt",
                            }
                        )
                    boxes[-1]["actual_fonts"] = sorted(observed_fonts)
                    if layouts is not None and rendered_ink:
                        predicted = text_ink_boxes(element, layouts[slide["id"], element["id"]])
                        if predicted:
                            expected_width = max(b[2] for b in predicted) - min(
                                b[0] for b in predicted
                            )
                            actual_width = (
                                max(b[1] for b in rendered_ink) - min(b[0] for b in rendered_ink)
                            ) / (tx.scale * 72)
                            boxes[-1]["measured_ink_width_px"] = round(expected_width, 3)
                            boxes[-1]["rendered_ink_width_px"] = round(actual_width, 3)
                            if abs(actual_width - expected_width) > max(2, expected_width * 0.03):
                                findings.append(
                                    {
                                        "code": "rendered_ink_width_drift",
                                        "severity": "warning",
                                        "slide": slide["id"],
                                        "element": element["id"],
                                        "measured_ink_width_px": round(expected_width, 3),
                                        "rendered_ink_width_px": round(actual_width, 3),
                                        "message": "Visible text width differs from the measured font by over 3% and 2 px; inspect mixed-script spacing and compare the source",
                                    }
                                )
                    if substituted_fonts:
                        findings.append(
                            {
                                "code": "renderer_font_substitution",
                                "slide": slide["id"],
                                "element": element["id"],
                                "actual_fonts": sorted(substituted_fonts),
                                "message": "The renderer used a different font from the measured face; choose a supported family and rebuild",
                            }
                        )
    return {
        "status": "fail"
        if any(f.get("severity", "error") == "error" for f in findings)
        else "review"
        if findings
        else "pass",
        "renderer": "LibreOffice/PDFium",
        "findings": findings,
        "text_boxes": boxes,
        "limitations": "This checks renderer output and glyph bounds; source recognition and target PowerPoint/WPS appearance still need visual review.",
    }
