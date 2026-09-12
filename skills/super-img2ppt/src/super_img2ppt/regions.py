"""Compare explicit source-coordinate ink regions without image registration."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

from .prepare import _normalize_image, fresh_directory, json_write
from .scene import InputError


def _mask(image, color, tolerance):
    target = Image.new("RGB", image.size, color)
    channels = ImageChops.difference(image.convert("RGB"), target).split()
    masks = [
        channel.point([255 if n <= tolerance else 0 for n in range(256)]) for channel in channels
    ]
    return ImageChops.darker(ImageChops.darker(masks[0], masks[1]), masks[2])


def _touches(mask):
    box = mask.getbbox()
    if box is None:
        return []
    return [
        side
        for side, edge, boundary in zip(
            ["left", "top", "right", "bottom"], box, [0, 0, mask.width, mask.height], strict=True
        )
        if edge == boundary
    ]


def compare_region(source, actual, roi, color, *, tolerance=64):
    """Report isolated-mask diagnostics; no threshold confers source-fidelity PASS."""
    if source.size != actual.size:
        raise InputError(
            "Source and actual canvas sizes must match; do not register or resize them"
        )
    if source.width * source.height > 40_000_000:
        raise InputError("Comparison image exceeds 40 million pixels")
    if not isinstance(roi, (list, tuple)) or len(roi) != 4 or any(type(n) is not int for n in roi):
        raise InputError("ROI must contain four integers: x y width height")
    x, y, w, h = roi
    if x < 0 or y < 0 or w < 1 or h < 1 or x + w > source.width or y + h > source.height:
        raise InputError("ROI must be nonempty and inside the source canvas")
    if w * h > 4_000_000:
        raise InputError("Comparison ROI exceeds four million pixels")
    if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise InputError("Mask color must be #RRGGBB")
    if type(tolerance) is not int or not 0 <= tolerance <= 255:
        raise InputError("Mask tolerance must be an integer between 0 and 255")
    box = (x, y, x + w, y + h)
    a, b = [_mask(im.crop(box), color, tolerance) for im in (source, actual)]
    intersection = ImageChops.darker(a, b).histogram()[255]
    union = ImageChops.lighter(a, b).histogram()[255]
    touches = [_touches(m) for m in (a, b)]
    bounds = []
    for mask in (a, b):
        local = mask.getbbox()
        bounds.append([local[0] + x, local[1] + y, local[2] + x, local[3] + y] if local else None)
    issues = []
    if bounds[0] is None:
        issues.append("empty_source_mask")
    if bounds[1] is None:
        issues.append("empty_actual_mask")
    if any(touches):
        issues.append("ink_touches_roi_boundary")
    valid = not issues
    return {
        "status": "review",
        "roi": list(roi),
        "canvas_size": list(source.size),
        "mask_color": color,
        "mask_tolerance": tolerance,
        "mask_rule": "Every RGB channel differs from the selected color by at most tolerance",
        "source_pixels": a.histogram()[255],
        "actual_pixels": b.histogram()[255],
        "source_ink_box": bounds[0],
        "actual_ink_box": bounds[1],
        "source_touches_roi": touches[0],
        "actual_touches_roi": touches[1],
        "edge_metrics_valid": valid,
        "edge_delta_px": [q - p for p, q in zip(*bounds, strict=True)] if valid else None,
        "mask_iou": intersection / union if union and bounds[0] is not None else None,
        "issues": issues,
        "limits": [
            "ROI and color must isolate the intended ink; nearby same-color geometry can contaminate the mask.",
            "Boundary contact invalidates complete-ink edges; any IoU still describes only the cropped mask.",
            "Equal extrema do not prove equal glyphs; no aggregate or automatic source-fidelity pass.",
            "Caller must supply the actual PPTX render; this command cannot attest its origin.",
        ],
    }


def compare_region_files(source: Path, actual: Path, out: Path, **options):
    fresh_directory(out)
    report = {"status": "fail"}
    try:
        for path, name in ((source, "source"), (actual, "actual")):
            if not path.is_file() or path.stat().st_size > 64_000_000:
                raise InputError("Comparison inputs must be local image files below 64 MB each")
            _normalize_image(path, out / f"{name}.png")
            report[f"{name}_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        with Image.open(out / "source.png") as a, Image.open(out / "actual.png") as b:
            report["source_size"] = list(a.size)
            report["actual_size"] = list(b.size)
            report.update(compare_region(a, b, **options))
            x, y, w, h = report["roi"]
            crops = [im.crop((x, y, x + w, y + h)).convert("RGB") for im in (a, b)]
            column = max(w, 180)
            comparison = Image.new("RGB", (column * 2 + 36, h + 54), "#F1F5F9")
            draw = ImageDraw.Draw(comparison)
            for index, (crop, name) in enumerate(zip(crops, ("source", "actual"), strict=True)):
                crop.save(out / f"{name}_crop.png")
                _mask(crop, report["mask_color"], report["mask_tolerance"]).save(
                    out / f"{name}_mask.png"
                )
                draw.text(
                    (12 + index * (column + 12), 12),
                    name.upper(),
                    fill="#0F172A",
                    font=ImageFont.load_default(size=16),
                )
                comparison.paste(crop, (12 + index * (column + 12), 42))
            comparison.save(out / "comparison.png")
        report["normalization"] = (
            "EXIF orientation and alpha-on-white only; no resizing or registration"
        )
    except (InputError, OSError, ValueError, Image.DecompressionBombError) as exc:
        report.update(status="fail", error=str(exc))
    finally:
        json_write(out / "region.json", report)
    return report
