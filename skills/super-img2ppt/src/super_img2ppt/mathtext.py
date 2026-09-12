"""Place explicitly styled formula parts on source-coordinate baselines."""

from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path

from .fonts import FontCatalog, ink_bounds, measure
from .geometry import box_points, rotate_points
from .prepare import fresh_directory, json_write
from .scene import InputError, _unique_pairs


def _number(value, low, high, name):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not low <= value <= high
    ):
        raise InputError(f"{name} must be finite and between {low} and {high}")
    return value


def _pair(value, name):
    if not isinstance(value, list) or len(value) != 2:
        raise InputError(f"{name} must contain two source-pixel coordinates")
    return [_number(v, -100000, 100000, name) for v in value]


def _keys(value, allowed, required, name):
    if not isinstance(value, dict) or set(value) - allowed or required - set(value):
        raise InputError(
            f"Invalid {name} fields; required {sorted(required)}, allowed {sorted(allowed)}"
        )


def compose_math(spec: dict, catalog: FontCatalog) -> dict:
    """Compile observed baseline offsets into ordinary editable scene text elements.

    This is not a TeX parser or automatic mathematical OCR. Each part's style and
    baseline offset is provided explicitly; scripts use ordinary letters at a
    smaller size. No overlap exemptions or source-derived guesses are inserted.
    """
    _keys(
        spec,
        {
            "id",
            "origin",
            "font_family",
            "font_size",
            "color",
            "parts",
            "z",
            "container",
            "rotation",
        },
        {"id", "origin", "font_family", "font_size", "parts"},
        "formula",
    )
    prefix = spec["id"]
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", prefix):
        raise InputError("Formula id must be a short scene identifier")
    origin = _pair(spec["origin"], "origin")
    rotation = _number(spec.get("rotation", 0), -360, 360, "rotation")
    size = _number(spec["font_size"], 1, 300, "font_size")
    family = spec["font_family"]
    if not isinstance(family, str) or not family.strip() or len(family) > 128:
        raise InputError("font_family must name an installed font")
    z = spec.get("z", 0)
    if isinstance(z, bool) or not isinstance(z, int) or not 0 <= z <= 100000:
        raise InputError("z must be an integer between 0 and 100000")
    if "container" in spec and (
        not isinstance(spec["container"], str)
        or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", spec["container"])
    ):
        raise InputError("container must be a scene identifier")
    parts = spec["parts"]
    if not isinstance(parts, list) or not 1 <= len(parts) <= 128:
        raise InputError("A formula requires 1–128 explicitly positioned parts")
    elements, metrics = [], []
    total = 0
    for index, part in enumerate(parts):
        _keys(
            part,
            {"text", "offset", "size_scale", "bold", "italic", "color"},
            {"text", "offset"},
            "formula part",
        )
        text = part["text"]
        if not isinstance(text, str) or not text.strip() or len(text) > 128:
            raise InputError("Each formula part requires 1–128 visible characters")
        total += len(text)
        if total > 2048:
            raise InputError("Formula exceeds 2048 characters")
        if any(unicodedata.category(c).startswith("C") or c in "\n\r\t" for c in text):
            raise InputError("Formula parts must be single-line visible text")
        if any(
            "SUPERSCRIPT" in unicodedata.name(c, "") or "SUBSCRIPT" in unicodedata.name(c, "")
            for c in text
        ):
            raise InputError(
                "Use ordinary characters with size_scale and baseline offsets for scripts"
            )
        offset = _pair(part["offset"], "offset")
        part_size = size * _number(part.get("size_scale", 1), 0.1, 3, "size_scale")
        _number(part_size, 1, 300, "effective font_size")
        bold, italic = part.get("bold", False), part.get("italic", False)
        if not isinstance(bold, bool) or not isinstance(italic, bool):
            raise InputError("bold and italic must be booleans")
        color = part.get("color", spec.get("color", "#000000"))
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise InputError("Formula color must be #RRGGBB")
        try:
            face = catalog.resolve(text, family, family, bold, italic)
        except InputError as exc:
            raise InputError(f"Formula part {prefix}_{index} ({text!r}): {exc}") from exc
        if (
            family.casefold() not in {n.casefold() for n in (*face.aliases, face.family)}
            or face.italic != italic
            or (bold and face.weight < 600)
            or (not bold and face.weight >= 600)
        ):
            raise InputError(
                f"Formula part {prefix}_{index} ({text!r}) requires the requested font, glyphs and weight/italic face; choose an available family explicitly"
            )
        width, ascent, descent = measure(face, text, part_size)
        ink = ink_bounds(face, text, part_size)
        if ink is None:
            raise InputError("Formula part has no measurable visible ink")
        x, baseline = origin[0] + offset[0], origin[1] + offset[1]
        left_reserve = max(0, -ink[0]) + 0.5
        top_reserve = max(0, -ink[1] - ascent) + 0.5
        height = max(ascent + descent, part_size * 1.15)
        element = {
            "id": f"{prefix}_{index}",
            "kind": "text",
            "z": z + index,
            "box": [
                x - left_reserve,
                baseline - ascent - top_reserve,
                width + left_reserve + 1,
                height + top_reserve + 1,
            ],
            "padding": [top_reserve, 0, 0, left_reserve],
            "text": text,
            "font_family": face.family,
            "cjk_font_family": face.family,
            "font_size": part_size,
            "bold": bold,
            "italic": italic,
            "color": color,
            "fit": "strict",
            "wrap": False,
        }
        if "container" in spec:
            element["container"] = spec["container"]
        ink_quad = box_points([x + ink[0], baseline + ink[1], ink[2] - ink[0], ink[3] - ink[1]])
        measured_baseline = [x, baseline]
        if rotation:
            pivot = {"box": [*origin, 0, 0], "rotation": rotation}
            bx, by, bw, bh = element["box"]
            cx, cy = rotate_points([(bx + bw / 2, by + bh / 2)], pivot)[0]
            element.update(box=[cx - bw / 2, cy - bh / 2, bw, bh], rotation=rotation)
            measured_baseline = list(rotate_points([measured_baseline], pivot)[0])
            ink_quad = rotate_points(ink_quad, pivot)
        elements.append(element)
        metrics.append(
            {
                "id": element["id"],
                "text": text,
                "baseline": measured_baseline,
                "ink_box": [
                    min(p[0] for p in ink_quad),
                    min(p[1] for p in ink_quad),
                    max(p[0] for p in ink_quad),
                    max(p[1] for p in ink_quad),
                ],
                "rotation": rotation,
                "font_family": face.family,
                "font_size": part_size,
                "bold": bold,
                "italic": italic,
            }
        )
    return {
        "status": "unverified",
        "elements": elements,
        "parts": metrics,
        "limitations": [
            "Observed offsets and styles are supplied by the author, not inferred.",
            "Native text parts, not Office equation objects; run full build and source comparison.",
        ],
    }


def compose_file(source: Path, out: Path, font_dirs: tuple[Path, ...] = ()) -> dict:
    fresh_directory(out)
    report = {"status": "fail"}
    try:
        if not source.is_file() or source.stat().st_size > 65536:
            raise InputError("Formula specification must be a regular JSON file of at most 64 KiB")
        with source.open("rb") as stream:
            raw = stream.read(65537)
        if len(raw) > 65536:
            raise InputError("Formula specification exceeds 64 KiB")
        spec = json.loads(raw, object_pairs_hook=_unique_pairs)
        catalog = FontCatalog(extra_dirs=font_dirs)
        result = compose_math(spec, catalog)
        json_write(out / "elements.json", result.pop("elements"))
        json_write(out / "fonts.json", catalog.manifest())
        report = result
        return report
    except (InputError, OSError, ValueError, RuntimeError) as exc:
        report["error"] = str(exc)
        raise
    finally:
        json_write(out / "math.json", report)
