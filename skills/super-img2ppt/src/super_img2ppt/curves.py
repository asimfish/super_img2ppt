"""Trace one visually isolated chart stroke into native scene line fragments."""

from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw

from .prepare import _normalize_image, fresh_directory, json_write
from .scene import InputError


def _number(value, low, high, name):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not low <= value <= high
    ):
        raise InputError(f"{name} must be finite and between {low} and {high}")


def _simplify(points, tolerance):
    keep = {0, len(points) - 1}
    work = [(0, len(points) - 1)]
    comparisons = 0
    while work:
        first, last = work.pop()
        a, b = points[first], points[last]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy)
        farthest, distance = first, 0.0
        for i in range(first + 1, last):
            comparisons += 1
            if comparisons > 2_000_000:
                raise InputError("Curve simplification exceeds work limit; use a smaller ROI")
            p = points[i]
            error = abs(dy * (p[0] - a[0]) - dx * (p[1] - a[1])) / length
            if error > distance:
                farthest, distance = i, error
        if distance > tolerance:
            keep.add(farthest)
            work.extend([(first, farthest), (farthest, last)])
    return [points[i] for i in sorted(keep)]


def trace_curve(
    image: Image.Image,
    roi: list[int],
    color: str,
    *,
    tolerance: float = 80,
    exclude_bands: list[tuple[int, int]] | None = None,
    max_gap: int = 4,
    simplify_px: float = 0.25,
    stroke_width: float = 1.5,
    prefix: str = "curve",
    axis: str = "x",
) -> dict:
    """Trace a single-valued y(x) stroke, refusing unresolved branches or long gaps.

    Coordinates are normalized-image pixels. Excluded bands are explicit absolute
    y intervals [top, bottom), not inferred horizontal lines. Interpolation bridges
    only short gaps inside observed endpoints and is recorded for visual review.
    """
    if image.width * image.height > 40_000_000:
        raise InputError("Source image exceeds 40 million pixels")
    if not isinstance(roi, (list, tuple)):
        raise InputError("ROI must contain four integers: x y width height")
    if axis not in {"x", "y"}:
        raise InputError("Tracing axis must be x or y")
    if axis == "y":
        if len(roi) != 4 or any(type(v) is not int for v in roi):
            raise InputError("ROI must contain four integers: x y width height")
        result = trace_curve(
            image.transpose(Image.Transpose.TRANSPOSE),
            [roi[1], roi[0], roi[3], roi[2]],
            color,
            tolerance=tolerance,
            exclude_bands=exclude_bands,
            max_gap=max_gap,
            simplify_px=simplify_px,
            stroke_width=stroke_width,
            prefix=prefix,
        )
        result["roi"] = list(roi)
        result["axis"] = "y"
        result["interpolated_rows"] = result.pop("interpolated_columns")
        for key in ["centers", "vertices"]:
            result[key] = [[y, x] for x, y in result[key]]
        for element in result["elements"]:
            element["points"] = [[y, x] for x, y in element["points"]]
        return result
    if len(roi) != 4 or any(type(v) is not int for v in roi):
        raise InputError("ROI must contain four integers: x y width height")
    x0, y0, width, height = roi
    if (
        x0 < 0
        or y0 < 0
        or width < 2
        or height < 2
        or x0 + width > image.width
        or y0 + height > image.height
        or width > 6000
        or width * height > 4_000_000
        or image.width * image.height > 40_000_000
    ):
        raise InputError("ROI is outside image bounds or exceeds 6000 columns / 4 million pixels")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise InputError("Curve color must be #RRGGBB")
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]{0,39}", prefix):
        raise InputError("Curve prefix must be a short alphanumeric scene ID")
    _number(tolerance, 1, 180, "Color tolerance")
    _number(simplify_px, 0.1, 2, "Simplification tolerance")
    _number(stroke_width, 0.25, 12, "Stroke width")
    _number(max_gap, 0, 16, "Maximum gap")
    if type(max_gap) is not int:
        raise InputError("Maximum gap must be an integer")
    bands = [] if exclude_bands is None else exclude_bands
    if len(bands) > 8:
        raise InputError("At most eight explicit guide bands are supported")
    excluded = set()
    for band in bands:
        if (
            len(band) != 2
            or any(type(v) is not int for v in band)
            or not y0 <= band[0] < band[1] <= y0 + height
            or band[1] - band[0] > 8
        ):
            raise InputError("Guide bands must be in the ROI and at most eight rows high")
        excluded.update(range(*band))
    target = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
    crop = image.crop((x0, y0, x0 + width, y0 + height)).convert("RGB")
    pixels = crop.load()
    observed = {}
    touches = []
    for x in range(width):
        ys = [
            y + y0
            for y in range(height)
            if y + y0 not in excluded
            and sum((a - b) ** 2 for a, b in zip(pixels[x, y], target, strict=True)) <= tolerance**2
        ]
        if not ys:
            continue
        if ys[-1] - ys[0] > 24 or any(
            b - a > 1 and any(y not in excluded for y in range(a + 1, b))
            for a, b in zip(ys, ys[1:], strict=False)
        ):
            raise InputError(
                f"Curve is ambiguous at x={x + x0}: multiple strokes or a filled/steep region; isolate one stroke or trace a steep fragment with axis=y"
            )
        observed[x + x0] = sum(ys) / len(ys) + 0.5
        if ys[0] == y0 or ys[-1] == y0 + height - 1:
            touches.append(x + x0)
    if len(observed) < 3:
        raise InputError("No usable curve stroke found; inspect the color and ROI")
    keys = sorted(observed)
    values = dict(observed)
    missing = []
    for a, b in zip(keys, keys[1:], strict=False):
        gap = b - a - 1
        if gap > max_gap:
            raise InputError(
                f"Unobserved curve gap of {gap} columns at x={a + 1}; not interpolated"
            )
        for x in range(a + 1, b):
            values[x] = values[a] + (values[b] - values[a]) * (x - a) / (b - a)
            missing.append(x)
    coverage = len(observed) / width
    if coverage < 0.8:
        raise InputError(
            "Curve coverage below 80%; crop more tightly instead of inventing endpoints"
        )
    centers = [[x + 0.5, values[x]] for x in sorted(values)]
    smooth = []
    for i, (x, _y) in enumerate(centers):
        near = [
            (centers[j][1], 2 if j == i else 1)
            for j in range(max(0, i - 1), min(len(centers), i + 2))
        ]
        smooth.append([x, sum(v * w for v, w in near) / sum(w for _, w in near)])
    vertices = _simplify(smooth, simplify_px)
    if len(vertices) > 2001:
        raise InputError("Curve exceeds 2000 native segments; inspect mask noise or split the ROI")
    elements = []
    for i, (a, b) in enumerate(zip(vertices, vertices[1:], strict=False)):
        elements.append(
            {
                "id": f"{prefix}_{i}",
                "kind": "line",
                "z": 4,
                "points": [[round(v, 4) for v in p] for p in (a, b)],
                "stroke": color.upper(),
                "stroke_width": stroke_width,
                "line_cap": "round",
                "allow_overlap_with": [
                    f"{prefix}_{j}"
                    for j in range(max(0, i - 2), min(len(vertices) - 1, i + 3))
                    if j != i
                ],
                "overlap_reason": "Neighboring segments form the same inspected source curve; other objects are not exempted.",
            }
        )
    return {
        "status": "review",
        "axis": "x",
        "roi": list(roi),
        "color": color.upper(),
        "color_tolerance": tolerance,
        "excluded_bands": [list(band) for band in bands],
        "coverage": round(coverage, 6),
        "interpolated_columns": missing,
        "roi_boundary_contacts": touches,
        "centers": centers,
        "vertices": vertices,
        "elements": elements,
        "limits": "Pixel geometry only, not recovered experimental data. Native line segments, not an Office chart or spline. Review gaps, ROI edges and actual PPTX rendering. Same-color crossings and long occlusions require another representation.",
    }


def trace_file(source: Path, out: Path, **options) -> dict:
    fresh_directory(out)
    report = {"status": "fail", "visual_review": "required"}
    try:
        if not source.is_file() or source.stat().st_size > 64_000_000:
            raise InputError("Curve input must be a local image file below 64 MB")
        _normalize_image(source, out / "source.png")
        with Image.open(out / "source.png") as image:
            result = trace_curve(image, **options)
            report.update(result)
            report["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
            report["normalized_source_sha256"] = hashlib.sha256(
                (out / "source.png").read_bytes()
            ).hexdigest()
            x, y, w, h = result["roi"]
            overlay = image.crop((x, y, x + w, y + h)).convert("RGB")
            draw = ImageDraw.Draw(overlay)
            draw.line([(a - x, b - y) for a, b in result["vertices"]], fill="#FF00FF", width=1)
            overlay.save(out / "overlay.png")
        json_write(out / "elements.json", report.pop("elements"))
    except (InputError, OSError, ValueError, Image.DecompressionBombError) as exc:
        report["status"] = "fail"
        report["error"] = str(exc)
    finally:
        json_write(out / "trace.json", report)
    return report
