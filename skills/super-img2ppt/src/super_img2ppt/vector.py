"""First-class vector delivery metadata and SVG-to-PDF export."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from .render import make_renderer

MANIFEST_VERSION = 1


def _page_inventory(slide: dict) -> dict:
    elements = slide["elements"]
    raster = [
        {
            "id": element["id"],
            "path": element["path"],
            "provenance": element.get("provenance"),
            "image_fit": element.get("image_fit", "contain"),
        }
        for element in elements
        if element["kind"] == "image"
    ]
    counts = {
        kind: sum(element["kind"] == kind for element in elements)
        for kind in ("text", "shape", "line", "image")
    }
    return {
        "slide": slide["id"],
        "width": slide["width"],
        "height": slide["height"],
        "pure_vector": not raster,
        "content_type": "vector" if not raster else "mixed_vector_raster",
        "element_counts": counts,
        "vector_element_count": len(elements) - len(raster),
        "embedded_raster_assets": raster,
    }


def write_manifest(
    scene: dict,
    out: Path,
    *,
    svg_dir: Path,
    pdf_paths: dict[str, Path] | None = None,
    pdf_status: str = "not_requested",
) -> dict:
    """Write a stable inventory for publication-side vector consumers.

    The existing ``svg/`` directory stays the canonical SVG location for backwards
    compatibility. The manifest makes the dual output explicit and records which
    elements remain embedded raster assets.
    """

    pdf_paths = {} if pdf_paths is None else pdf_paths
    pages = []
    for slide in scene["slides"]:
        page = _page_inventory(slide)
        page["svg"] = os.path.relpath(svg_dir / f"{slide['id']}.svg", out)
        page["pdf"] = (
            os.path.relpath(pdf_paths[slide["id"]], out) if slide["id"] in pdf_paths else None
        )
        pages.append(page)
    manifest = {
        "schema_version": MANIFEST_VERSION,
        "title": scene.get("title", "Editable reconstruction"),
        "source_scene": "../scene.resolved.json",
        "pptx": "../editable.pptx",
        "svg_root": os.path.relpath(svg_dir, out),
        "pdf_root": "pdf" if pdf_paths else None,
        "pdf_status": pdf_status,
        "vector_source": "SVG",
        "pages": pages,
        "limits": [
            "Text, native shapes, freeforms, gradients and lines are represented as SVG vector elements.",
            "Photos or intentionally retained complex artwork remain embedded raster assets and are listed per page.",
            "SVG text depends on the selected font being available to the consuming application.",
        ],
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def export_pdf_pages(svg_dir: Path, out: Path, slide_ids: list[str]) -> dict[str, Path]:
    """Convert each SVG page to a PDF without rasterizing the SVG first."""

    executable = shutil.which("soffice")
    if not executable:
        raise RuntimeError("Vector PDF export requires local LibreOffice (soffice)")
    out.mkdir(parents=True, exist_ok=True)
    renderer = make_renderer("libreoffice")
    paths: dict[str, Path] = {}
    for slide_id in slide_ids:
        svg = svg_dir / f"{slide_id}.svg"
        pdf = renderer.render(svg, out)
        paths[slide_id] = pdf
    return paths
