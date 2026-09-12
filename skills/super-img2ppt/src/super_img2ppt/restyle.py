"""Explicit, auditable style changes; never infer AI origin or rewrite content."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path

from .prepare import fresh_directory, json_write
from .scene import InputError, safe_asset, validate_scene

# Geometry, content, ordering, topology, raster paths and QA exemptions are immutable.
FIELDS = {
    "text": {"font_family", "cjk_font_family", "font_size", "color", "bold", "align"},
    "shape": {"fill", "stroke", "stroke_width", "radius", "gradient"},
    "line": {"stroke", "stroke_width"},
    "image": set(),
}


def apply_plan(scene: dict, plan: dict) -> tuple[dict, list[dict]]:
    """Apply explicit per-element style fields to a copy, returning an audit trail."""
    validate_scene(scene)
    if not isinstance(plan, dict) or set(plan) != {"version", "changes"}:
        raise InputError("Style plan requires only version and changes")
    if type(plan["version"]) is not int or plan["version"] != 1:
        raise InputError("Unsupported style plan version")
    changes = plan["changes"]
    if not isinstance(changes, list) or not 1 <= len(changes) <= 5000:
        raise InputError("Style plan requires 1–5000 explicit changes")
    result = copy.deepcopy(scene)
    index = {(s["id"], e["id"]): e for s in result["slides"] for e in s["elements"]}
    audit, seen = [], set()
    for change in changes:
        if not isinstance(change, dict) or set(change) != {"slide", "element", "set", "reason"}:
            raise InputError("Each change requires slide, element, set and reason")
        if not all(
            isinstance(change[k], str) and change[k].strip() for k in ("slide", "element", "reason")
        ):
            raise InputError("Change identifiers and reason must be nonempty strings")
        key = change["slide"], change["element"]
        if key not in index or key in seen:
            raise InputError("Unknown or repeated style target")
        seen.add(key)
        element = index[key]
        fields = change["set"]
        if not isinstance(fields, dict) or not fields or not set(fields) <= FIELDS[element["kind"]]:
            raise InputError("Only supported visual style fields may change")
        if element["kind"] == "text" and "runs" in element:
            raise InputError("Rich text/formula styles are protected; restyle plain labels only")
        edits = []
        for field, value in fields.items():
            present = field in element
            before = copy.deepcopy(element.get(field))
            if value is None:
                if field != "gradient":
                    raise InputError("Only gradient can be removed with null")
                element.pop(field, None)
            else:
                element[field] = copy.deepcopy(value)
            if before != value or (not present and value is not None):
                edits.append(
                    {"field": field, "before_present": present, "before": before, "after": value}
                )
        if edits:
            audit.append(
                {"slide": key[0], "element": key[1], "reason": change["reason"], "edits": edits}
            )
    if not audit:
        raise InputError("Style plan has no effective changes")
    for slide in result["slides"]:
        slide["reviewed"] = False
    return validate_scene(result), audit


def stage_variants(scene: dict, root: Path, plan: dict, out: Path) -> dict:
    """Create portable baseline/refined scenes without modifying the input assets."""
    refined, audit = apply_plan(scene, plan)
    baseline = copy.deepcopy(scene)
    # Resolve and validate every asset before creating output.
    assets = {}
    for slide in scene["slides"]:
        paths = ([slide["source"]] if "source" in slide else []) + [
            e["path"] for e in slide["elements"] if e["kind"] == "image"
        ]
        for path in paths:
            source = safe_asset(root, path)
            data = source.read_bytes()
            assets[path] = (f"assets/{hashlib.sha256(data).hexdigest()}{source.suffix}", data)
    fresh_directory(out)
    (out / "assets").mkdir()
    for relative, data in assets.values():
        (out / relative).write_bytes(data)
    for variant, value in (("baseline", baseline), ("refined", refined)):
        for slide in value["slides"]:
            if "source" in slide:
                slide["source"] = assets[slide["source"]][0]
            for element in slide["elements"]:
                if element["kind"] == "image":
                    element["path"] = assets[element["path"]][0]
        json_write(out / f"{variant}.json", value)
    report = {
        "status": "unverified",
        "visual_review": "required",
        "changes": audit,
        "limitations": [
            "Style changes are intentional, not source-fidelity improvements.",
            "Raster artwork is unchanged. No AI-origin detection is performed.",
        ],
    }
    json_write(out / "plan.json", plan)
    json_write(out / "restyle.json", report)
    return report
