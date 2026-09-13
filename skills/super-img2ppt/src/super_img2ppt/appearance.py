"""Bounded source/target appearance checks independent of the target-color mask."""

from __future__ import annotations

import colorsys
import hashlib
import json
import math
from collections import Counter
from contextlib import closing

import pypdfium2 as pdfium
from jsonschema import Draft202012Validator
from PIL import Image

from .color_management import to_srgb
from .prepare import json_write
from .scene import COLOR, ID, InputError, _unique_pairs, safe_asset, slide_transform

ROI = {
    "type": "array",
    "items": {"type": "integer", "minimum": 0, "maximum": 16384},
    "minItems": 4,
    "maxItems": 4,
}
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["version", "regions"],
    "properties": {
        "version": {"const": 1, "type": "integer"},
        "regions": {
            "type": "array",
            "minItems": 1,
            "maxItems": 128,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "slide", "roi", "kind", "mode"],
                "properties": {
                    "id": ID,
                    "slide": ID,
                    "roi": ROI,
                    "actual_roi": ROI,
                    "kind": {"enum": ["solid", "ink"]},
                    "mode": {"enum": ["faithful", "target"]},
                    "target_color": COLOR,
                    "reason": {"type": "string", "minLength": 1, "maxLength": 2000},
                    "background": COLOR,
                    "max_channel_delta": {"type": "integer", "minimum": 0, "maximum": 64},
                    "min_contrast": {"type": "integer", "minimum": 1, "maximum": 128},
                    "density_ratio": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {"type": "number", "minimum": 0.05, "maximum": 20},
                    },
                },
            },
        },
    },
}


def validate_plan(plan, scene):
    errors = list(Draft202012Validator(SCHEMA).iter_errors(plan))
    if errors:
        raise InputError(f"Invalid appearance plan: {errors[0].message}")
    slides = {s["id"]: s for s in scene["slides"]}
    seen = set()
    for region in plan["regions"]:
        if region["id"] in seen:
            raise InputError("Repeated appearance region id")
        seen.add(region["id"])
        slide = slides.get(region["slide"])
        if slide is None or "source" not in slide:
            raise InputError("Appearance regions require a known slide with source")
        for key in ("roi", "actual_roi"):
            if key in region:
                _box(region[key], (slide["width"], slide["height"]))
        if (
            region["kind"] == "ink"
            and region.get("actual_roi", region["roi"])[2:] != region["roi"][2:]
        ):
            raise InputError("Ink comparison requires equal source and actual ROI dimensions")
        if region["mode"] == "target":
            if "target_color" not in region or not region.get("reason", "").strip():
                raise InputError("Target color requires an explicit color and change reason")
        elif "target_color" in region or "reason" in region:
            raise InputError("Faithful checks cannot override the source color")
        lo, hi = region.get("density_ratio", [0.8, 1.25])
        if not math.isfinite(lo) or not math.isfinite(hi) or not lo <= 1 <= hi:
            raise InputError("Density ratio interval must be finite and include 1")
    return plan


def load_plan(path, scene):
    if path.stat().st_size > 1_000_000:
        raise InputError("Appearance plan exceeds 1 MB")
    return validate_plan(
        json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_pairs), scene
    )


def _box(roi, size):
    x, y, w, h = roi
    if w < 2 or h < 2 or x + w > size[0] or y + h > size[1] or w * h > 1_000_000:
        raise InputError("Appearance ROI must be inside the canvas, at least 2x2, at most 1 MP")
    return x, y, x + w, y + h


def _rgb(value):
    return tuple(int(value[i : i + 2], 16) for i in (1, 3, 5))


def _median(colors):
    total = sum(colors.values())
    result = []
    for channel in range(3):
        bins = Counter()
        for color, n in colors.items():
            bins[color[channel]] += n
        count = 0
        for value, n in sorted(bins.items()):
            count += n
            if count >= (total + 1) // 2:
                result.append(value)
                break
    return tuple(result)


def sample(image, roi, kind, background="#FFFFFF", min_contrast=16):
    """Estimate opaque core color without selecting pixels by the expected hue."""
    crop = image.crop(_box(roi, image.size)).convert("RGB")
    colors = Counter(dict((color, n) for n, color in crop.getcolors(crop.width * crop.height)))
    bg = _rgb(background)

    def contrast(c):
        return max(abs(a - b) for a, b in zip(c, bg, strict=True))

    if kind == "ink":
        foreground = Counter({c: n for c, n in colors.items() if contrast(c) >= min_contrast})
        if sum(foreground.values()) < 4:
            return {"status": "invalid", "issue": "insufficient_foreground"}
        # Highest-contrast quartile suppresses edge antialiasing without a target-color mask.
        core, count = Counter(), 0
        required = max(4, math.ceil(sum(foreground.values()) * 0.25))
        for c, n in sorted(foreground.items(), key=lambda item: contrast(item[0]), reverse=True):
            core[c] = n
            count += n
            if count >= required:
                break
    else:
        core = colors
    color = _median(core)
    total = sum(core.values())
    agreement = (
        sum(
            n
            for c, n in core.items()
            if max(abs(a - b) for a, b in zip(c, color, strict=True)) <= 12
        )
        / total
    )
    if agreement < 0.85:
        return {
            "status": "invalid",
            "issue": "mixed_or_gradient_region",
            "core_agreement": agreement,
        }
    if kind == "ink":
        # Mixed hues must not disappear when only the darkest quartile is sampled.
        core_contrast = contrast(color)
        direction = [(v - b) / core_contrast for v, b in zip(color, bg, strict=True)]
        consistent = sum(
            n
            for c, n in foreground.items()
            if max(abs((v - b) / contrast(c) - d) for v, b, d in zip(c, bg, direction, strict=True))
            <= 0.15
        )
        if consistent / sum(foreground.values()) < 0.85:
            return {"status": "invalid", "issue": "mixed_ink_hues"}
    mass = sum(n * contrast(c) / 255 for c, n in colors.items()) / (crop.width * crop.height)
    return {
        "status": "measured",
        "rgb": list(color),
        "hsv_saturation": colorsys.rgb_to_hsv(*(v / 255 for v in color))[1],
        "hsv_value": colorsys.rgb_to_hsv(*(v / 255 for v in color))[2],
        "hex": "#" + "".join(f"{c:02X}" for c in color),
        "ink_mass": mass,
        "core_agreement": agreement,
        "pixels": crop.width * crop.height,
    }


def compare_region(source, actual, region):
    if region["kind"] == "ink" and region.get("actual_roi", region["roi"])[2:] != region["roi"][2:]:
        raise InputError("Ink comparison requires equal source and actual ROI dimensions")
    a = sample(
        source,
        region["roi"],
        region["kind"],
        region.get("background", "#FFFFFF"),
        region.get("min_contrast", 16),
    )
    b = sample(
        actual,
        region.get("actual_roi", region["roi"]),
        region["kind"],
        region.get("background", "#FFFFFF"),
        region.get("min_contrast", 16),
    )
    result = {
        "id": region["id"],
        "slide": region["slide"],
        "mode": region["mode"],
        "status": "fail",
        "source": a,
        "actual": b,
        "issues": [],
    }
    if a["status"] == "invalid" or b["status"] == "invalid":
        result["issues"].append("invalid_sampling_region")
        return result
    target = list(_rgb(region["target_color"])) if region["mode"] == "target" else a["rgb"]
    delta = max(abs(x - y) for x, y in zip(target, b["rgb"], strict=True))
    result.update(
        expected_rgb=target,
        max_channel_delta=delta,
        channel_tolerance=region.get("max_channel_delta", 12),
    )
    if delta > result["channel_tolerance"]:
        result["issues"].append("color_drift")
    if region["kind"] == "ink":
        # Divide ink mass by core contrast to separate line/letter coverage from pigment darkness.
        bg = _rgb(region.get("background", "#FFFFFF"))

        def coverage(v):
            return v["ink_mass"] / (
                max(abs(x - y) for x, y in zip(v["rgb"], bg, strict=True)) / 255
            )

        if max(abs(x - y) for x, y in zip(b["rgb"], bg, strict=True)) == 0:
            result["issues"].append("missing_actual_ink")
        else:
            ratio = coverage(b) / coverage(a)
            result["ink_coverage_ratio"] = ratio
            result["density_limits"] = region.get("density_ratio", [0.8, 1.25])
            if not result["density_limits"][0] <= ratio <= result["density_limits"][1]:
                result["issues"].append("ink_density_drift")
    result["status"] = "fail" if result["issues"] else "pass"
    return result


def _source_image(path):
    if path.stat().st_size > 64_000_000:
        raise InputError("Appearance reference exceeds 64 MB")
    with Image.open(path) as original:
        if original.width * original.height > 40_000_000:
            raise InputError("Appearance reference exceeds 40 MP")
        return to_srgb(original)[0]


def verify_pdf(scene, root, pdf, plan, out):
    """Render actual Office PDF directly at source scale; no fitted/resized preview oracle."""
    out.mkdir()
    report = {
        "status": "fail",
        "regions": [],
        "visual_review": "required",
        "scope": "Explicit isolated regions only; not full-page color or aesthetic acceptance",
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    }
    try:
        validate_plan(plan, scene)
        json_write(out / "plan.json", plan)
        with pdfium.PdfDocument(pdf) as document:
            if len(document) != len(scene["slides"]):
                raise InputError("Appearance PDF page count differs from scene")
            for index, slide in enumerate(scene["slides"]):
                regions = [r for r in plan["regions"] if r["slide"] == slide["id"]]
                if not regions:
                    continue
                source_path = safe_asset(root, slide["source"])
                source = _source_image(source_path)
                if source.size != (slide["width"], slide["height"]):
                    raise InputError(
                        "Appearance reference size differs from source-coordinate scene"
                    )
                tx = slide_transform(scene, slide)
                with closing(document[index]) as page:
                    scale = 1 / (72 * tx.scale)
                    pw, ph = page.get_size()
                    if math.ceil(pw * scale) * math.ceil(ph * scale) > 40_000_000:
                        raise InputError("Appearance render exceeds 40 MP")
                    bitmap = page.render(scale=scale)
                    try:
                        rendered = bitmap.to_pil()
                        x, y = round(tx.x / tx.scale), round(tx.y / tx.scale)
                        actual = rendered.crop(
                            (x, y, x + slide["width"], y + slide["height"])
                        ).convert("RGB")
                    finally:
                        bitmap.close()
                for region in regions:
                    measured = compare_region(source, actual, region)
                    measured["source_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
                    report["regions"].append(measured)
                    source.crop(_box(region["roi"], source.size)).save(
                        out / f"{region['id']}_source.png"
                    )
                    actual.crop(_box(region.get("actual_roi", region["roi"]), actual.size)).save(
                        out / f"{region['id']}_actual.png"
                    )
        report["uncovered_slides"] = [
            s["id"]
            for s in scene["slides"]
            if "source" in s and not any(r["slide"] == s["id"] for r in plan["regions"])
        ]
        report["status"] = (
            "fail"
            if any(r["status"] == "fail" for r in report["regions"])
            else "review"
            if report["uncovered_slides"]
            else "pass"
        )
        return report
    except (InputError, OSError, ValueError, RuntimeError) as exc:
        report["error"] = str(exc)
        raise
    finally:
        json_write(out / "appearance.json", report)


def automatic_plan(scene, root):
    """Sample a bounded fixed grid of flat nonwhite source patches; never use output colors."""
    regions = []
    eligible = []
    for slide in scene["slides"]:
        if "source" not in slide:
            continue
        image = _source_image(safe_asset(root, slide["source"]))
        if image.size != (slide["width"], slide["height"]):
            raise InputError("Appearance reference size differs from source-coordinate scene")
        found = []
        for row in range(8):
            for col in range(16):
                x = max(0, min(image.width - 5, round((col + 0.5) * image.width / 16) - 2))
                y = max(0, min(image.height - 5, round((row + 0.5) * image.height / 8) - 2))
                box = [x, y, 5, 5]
                patch = image.crop((x, y, x + 5, y + 5))
                extrema = patch.getextrema()
                if max(hi - lo for lo, hi in extrema) > 6:
                    continue
                color = patch.getpixel((2, 2))
                if max(255 - v for v in color) < 24:
                    continue
                found.append(
                    {
                        "id": f"auto_{len(eligible)}_{row}_{col}",
                        "slide": slide["id"],
                        "roi": box,
                        "kind": "solid",
                        "mode": "faithful",
                    }
                )
        eligible.append(found)
    # Round robin gives multi-page documents coverage without exceeding the plan budget.
    for index in range(128):
        for found in eligible:
            if index < len(found) and len(regions) < 128:
                regions.append(found[index])
    return {"version": 1, "regions": regions} if regions else None
