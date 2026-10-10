"""Trace one isolated, flat-color icon as a single editable closed contour."""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw

from .color_management import to_srgb
from .curves import _simplify
from .prepare import fresh_directory, json_write
from .scene import InputError, validate_scene


def trace_icon(image, roi, color, *, tolerance=64, simplify_px=0.25, prefix="icon"):
    if image.width * image.height > 40_000_000:
        raise InputError("Source image exceeds 40 million pixels")
    if not isinstance(roi, (list, tuple)) or len(roi) != 4 or any(type(n) is not int for n in roi):
        raise InputError("Icon ROI must contain four integers: x y width height")
    x0, y0, w, h = roi
    if (
        min(x0, y0) < 0
        or min(w, h) < 3
        or x0 + w > image.width
        or y0 + h > image.height
        or w * h > 65536
    ):
        raise InputError("Icon ROI must be inside the image and at most 65536 pixels")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise InputError("Icon color must be #RRGGBB")
    if type(tolerance) is not int or not 0 <= tolerance <= 200:
        raise InputError("Icon tolerance must be an integer between 0 and 200")
    if (
        isinstance(simplify_px, bool)
        or not isinstance(simplify_px, (int, float))
        or not math.isfinite(simplify_px)
        or not 0 <= simplify_px <= 1
    ):
        raise InputError("Icon simplification must be finite and between 0 and 1 pixel")
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", prefix):
        raise InputError("Icon prefix must be a short alphanumeric ID")
    normalized, management = to_srgb(image, preserve_alpha=True)
    crop = normalized.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")
    target = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    pixels = crop.load()
    selected = {
        (x, y)
        for y in range(h)
        for x in range(w)
        if pixels[x, y][3] > 0
        and max(abs(a - b) for a, b in zip(pixels[x, y][:3], target, strict=True)) <= tolerance
    }
    if not selected:
        raise InputError("Icon mask is empty; select its foreground color")
    alpha_values = {pixels[x, y][3] for x, y in selected}
    if len(alpha_values) > 1 and min(alpha_values) < 255:
        raise InputError(
            "Icon has varying foreground alpha; preserve it as raster or measured native parts"
        )
    if any(x in {0, w - 1} or y in {0, h - 1} for x, y in selected):
        raise InputError("Icon touches the ROI boundary; include a clear margin")
    edges = {}
    for x, y in selected:
        for neighbor, a, b in [
            ((x, y - 1), (x, y), (x + 1, y)),
            ((x + 1, y), (x + 1, y), (x + 1, y + 1)),
            ((x, y + 1), (x + 1, y + 1), (x, y + 1)),
            ((x - 1, y), (x, y + 1), (x, y)),
        ]:
            if neighbor not in selected:
                if a in edges:
                    raise InputError(
                        "Icon has ambiguous corner contacts; use measured native parts"
                    )
                edges[a] = b
    if len(edges) > 16384:
        raise InputError("Icon boundary exceeds 16384 edges; use a smaller ROI")
    start = min(edges)
    contour, current = [], start
    while True:
        contour.append(current)
        current = edges.pop(current)
        if current == start:
            break
    if edges:
        raise InputError(
            "Icon has holes or separate components; use semantic native parts or keep raster"
        )
    # Remove only exactly collinear staircase vertices before bounded simplification.
    contour = [
        p
        for i, p in enumerate(contour)
        if (p[0] - contour[i - 1][0]) * (contour[(i + 1) % len(contour)][1] - p[1])
        != (p[1] - contour[i - 1][1]) * (contour[(i + 1) % len(contour)][0] - p[0])
    ]
    if simplify_px:
        split = max(range(1, len(contour)), key=lambda i: math.dist(contour[0], contour[i]))
        contour = (
            _simplify(contour[: split + 1], simplify_px)[:-1]
            + _simplify(contour[split:] + [contour[0]], simplify_px)[:-1]
        )
    if not 3 <= len(contour) <= 256:
        raise InputError(
            "Icon needs more than 256 vertices; use measured native parts or keep raster"
        )
    left, top = min(x for x, y in contour), min(y for x, y in contour)
    width, height = max(x for x, y in contour) - left, max(y for x, y in contour) - top
    element = {
        "id": prefix,
        "kind": "shape",
        "shape": "freeform",
        "z": 0,
        "box": [left + x0, top + y0, width, height],
        "fill": color,
        "vertices": [[(x - left) / width, (y - top) / height] for x, y in contour],
    }
    if min(alpha_values) < 255:
        element["fill_opacity"] = min(alpha_values) / 255
    validate_scene(
        {
            "version": 1,
            "slides": [
                {
                    "id": "page_001",
                    "width": image.width,
                    "height": image.height,
                    "elements": [element],
                }
            ],
        }
    )
    return {
        "status": "review",
        "roi": list(roi),
        "color": color,
        "color_tolerance": tolerance,
        "simplify_px": simplify_px,
        "mask_pixels": len(selected),
        "vertex_count": len(contour),
        "color_management": management,
        "elements": [element],
        "limits": [
            "One isolated, hole-free flat-color silhouette only.",
            "Color thresholding and antialiasing need actual-render comparison.",
            "No semantic recognition, removal of tiny components or automatic background inference.",
        ],
    }


def trace_icon_file(path: Path, out: Path, **options):
    if path.stat().st_size > 200_000_000:
        raise InputError("Icon source exceeds 200 MB")
    with Image.open(path) as image:
        result = trace_icon(image, **options)
        normalized, _ = to_srgb(image, preserve_alpha=True)
    fresh_directory(out)
    result["source_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    json_write(out / "icon.json", result)
    x, y, w, h = result["roi"]
    overlay = normalized.crop((x, y, x + w, y + h)).convert("RGB")
    element = result["elements"][0]
    bx, by, bw, bh = element["box"]
    points = [(bx + u * bw - x, by + v * bh - y) for u, v in element["vertices"]]
    ImageDraw.Draw(overlay).line(points + points[:1], fill="#FF0066", width=1)
    overlay.save(out / "overlay.png")
    return result
