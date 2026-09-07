"""The source-pixel scene contract shared by exporters and validators."""

from __future__ import annotations

import copy
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator

from .geometry import strictly_convex


class InputError(ValueError):
    """An input cannot be processed without changing its declared meaning."""


NUM = {"type": "number", "minimum": -100000, "maximum": 100000}
POS = {"type": "number", "exclusiveMinimum": 0, "maximum": 100000}
COLOR = {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"}
ID = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$"}
BOX = {"type": "array", "prefixItems": [NUM, NUM, POS, POS], "minItems": 4, "maxItems": 4}
POINT = {"type": "array", "items": NUM, "minItems": 2, "maxItems": 2}
STYLE = {
    "font_family": {"type": "string", "minLength": 1, "maxLength": 150},
    "cjk_font_family": {"type": "string", "minLength": 1, "maxLength": 150},
    "font_size": {"type": "number", "minimum": 1, "maximum": 1000},
    "bold": {"type": "boolean"},
    "italic": {"type": "boolean"},
    "color": COLOR,
}
RUN = {
    "type": "object",
    "required": ["text"],
    "properties": {"text": {"type": "string", "maxLength": 20000}, **STYLE},
    "additionalProperties": False,
}
COMMON = {
    "id": ID,
    "kind": {"enum": ["text", "shape", "image", "line"]},
    "z": {"type": "integer", "minimum": -10000, "maximum": 10000},
    "container": ID,
    "allow_overlap_with": {"type": "array", "items": ID, "maxItems": 100},
    "overlap_reason": {"type": "string", "minLength": 8, "maxLength": 600},
    "role": {"enum": ["content", "decoration", "background"]},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
}
ELEMENT = {
    "type": "object",
    "required": ["id", "kind", "z"],
    "properties": {
        **COMMON,
        "box": BOX,
        "text": {"type": "string", "maxLength": 20000},
        "runs": {"type": "array", "items": RUN, "minItems": 1, "maxItems": 500},
        **STYLE,
        "align": {"enum": ["left", "center", "right"]},
        "valign": {"enum": ["top", "middle", "bottom"]},
        "rotation": {"enum": [-90, 0, 90, 180, 270]},
        "wrap": {"type": "boolean"},
        "line_height": {"type": "number", "minimum": 1, "maximum": 3},
        "padding": {
            "type": "array",
            "items": {"type": "number", "minimum": 0, "maximum": 1000},
            "minItems": 4,
            "maxItems": 4,
        },
        "fit": {"enum": ["strict", "shrink"]},
        "min_font_size": {"type": "number", "minimum": 1, "maximum": 1000},
        "font_group": ID,
        "shape": {
            "enum": ["rect", "round_rect", "ellipse", "triangle", "diamond", "chevron", "polygon"]
        },
        "vertices": {
            "type": "array",
            "minItems": 3,
            "maxItems": 32,
            "items": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": {"type": "number", "minimum": 0, "maximum": 1},
            },
        },
        "fill": {"anyOf": [COLOR, {"type": "null"}]},
        "gradient": {
            "type": "object",
            "required": ["direction", "stops"],
            "properties": {
                "direction": {"enum": ["vertical", "horizontal"]},
                "stops": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 16,
                    "items": {
                        "type": "object",
                        "required": ["offset", "color"],
                        "properties": {
                            "offset": {"type": "number", "minimum": 0, "maximum": 1},
                            "color": COLOR,
                        },
                        "additionalProperties": False,
                    },
                },
            },
            "additionalProperties": False,
        },
        "stroke": {"anyOf": [COLOR, {"type": "null"}]},
        "stroke_width": {"type": "number", "minimum": 0, "maximum": 100},
        "radius": {"type": "number", "minimum": 0, "maximum": 10000},
        "points": {"type": "array", "items": POINT, "minItems": 2, "maxItems": 2},
        "arrow": {"type": "boolean"},
        "arrow_head": {
            "type": "object",
            "required": ["length", "width"],
            "properties": {
                key: {"type": "number", "exclusiveMinimum": 0, "maximum": 1000}
                for key in ["length", "width"]
            },
            "additionalProperties": False,
        },
        "dash": {
            "type": "array",
            "items": {"type": "number", "minimum": 0.1, "maximum": 1000},
            "minItems": 2,
            "maxItems": 2,
        },
        "path": {"type": "string", "minLength": 1, "maxLength": 1000},
        "image_fit": {"enum": ["contain", "cover", "stretch"]},
        "provenance": {"type": "string", "minLength": 8, "maxLength": 1000},
        "contains_text": {"type": "boolean"},
    },
    "additionalProperties": False,
    "allOf": [
        {
            "if": {"properties": {"kind": {"const": "text"}}},
            "then": {
                "required": ["box", "font_size"],
                "oneOf": [
                    {"required": ["text"], "not": {"required": ["runs"]}},
                    {"required": ["runs"], "not": {"required": ["text"]}},
                ],
            },
        },
        {
            "if": {"properties": {"kind": {"const": "shape"}}},
            "then": {"required": ["box", "shape"]},
        },
        {
            "if": {"properties": {"kind": {"const": "image"}}},
            "then": {"required": ["box", "path", "provenance", "contains_text"]},
        },
        {"if": {"properties": {"kind": {"const": "line"}}}, "then": {"required": ["points"]}},
    ],
}
SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["version", "slides"],
    "properties": {
        "version": {"const": 1},
        "title": {"type": "string", "maxLength": 500},
        "slide_width_inches": {"type": "number", "minimum": 1, "maximum": 40},
        "fonts": {
            "type": "object",
            "properties": {
                key: {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "minItems": 1,
                    "maxItems": 20,
                }
                for key in ["latin", "cjk"]
            },
            "additionalProperties": False,
        },
        "slides": {
            "type": "array",
            "minItems": 1,
            "maxItems": 200,
            "items": {
                "type": "object",
                "required": ["id", "width", "height", "elements"],
                "properties": {
                    "id": ID,
                    "width": {"type": "integer", "minimum": 16, "maximum": 16384},
                    "height": {"type": "integer", "minimum": 16, "maximum": 16384},
                    "background": COLOR,
                    "source": {"type": "string", "minLength": 1, "maxLength": 1000},
                    "notes": {"type": "string", "maxLength": 100000},
                    "reviewed": {"type": "boolean"},
                    "elements": {"type": "array", "items": ELEMENT, "maxItems": 1500},
                },
                "additionalProperties": False,
            },
        },
    },
    "additionalProperties": False,
}


def text_content(element: dict) -> str:
    return element["text"] if "text" in element else "".join(r["text"] for r in element["runs"])


def safe_asset(root: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute() or re.match(r"^[A-Za-z]:", value) or "\\" in value:
        raise InputError(f"Assets must use relative POSIX paths: {value}")
    path = (root / candidate).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise InputError(f"Asset is missing or outside the scene directory: {value}")
    return path


def _validate_finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise InputError("NaN and infinity are not valid coordinates")
    if isinstance(value, dict):
        for v in value.values():
            _validate_finite(v)
    elif isinstance(value, list):
        for v in value:
            _validate_finite(v)
    elif isinstance(value, str) and any(ord(c) < 32 and c not in "\n\t" for c in value):
        raise InputError("Unsupported control character in scene text")


def validate_scene(scene: dict) -> dict:
    _validate_finite(scene)
    errors = sorted(Draft202012Validator(SCHEMA).iter_errors(scene), key=lambda e: str(e.path))
    if errors:
        raise InputError(
            "; ".join(f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors[:5])
        )
    slide_ids = set()
    for slide in scene["slides"]:
        if slide["id"] in slide_ids:
            raise InputError(f"Duplicate slide id: {slide['id']}")
        slide_ids.add(slide["id"])
        if slide["width"] * slide["height"] > 40_000_000:
            raise InputError("A slide may contain at most 40 million pixels")
        elements = {e["id"]: e for e in slide["elements"]}
        if len(elements) != len(slide["elements"]):
            raise InputError(f"Duplicate element id in {slide['id']}")
        for element in elements.values():
            fields_by_kind = {
                "text": {
                    "box",
                    "text",
                    "runs",
                    *STYLE,
                    "align",
                    "valign",
                    "rotation",
                    "wrap",
                    "line_height",
                    "padding",
                    "fit",
                    "min_font_size",
                    "font_group",
                },
                "shape": {
                    "box",
                    "shape",
                    "fill",
                    "stroke",
                    "stroke_width",
                    "radius",
                    "dash",
                    "vertices",
                    "gradient",
                },
                "image": {"box", "path", "image_fit", "provenance", "contains_text"},
                "line": {"points", "stroke", "stroke_width", "arrow", "arrow_head", "dash"},
            }
            unexpected = set(element) - set(COMMON) - fields_by_kind[element["kind"]]
            if unexpected:
                raise InputError(
                    f"{element['id']}: fields not supported for {element['kind']}: {', '.join(sorted(unexpected))}"
                )
            if element["kind"] == "line" and "stroke" in element and element["stroke"] is None:
                raise InputError(f"{element['id']}: a line requires a visible stroke")
            if element.get("allow_overlap_with") and not element.get("overlap_reason"):
                raise InputError(
                    f"{element['id']}: overlap exemptions need an evidence-based reason"
                )
            for ref in element.get("allow_overlap_with", []) + (
                [element["container"]] if "container" in element else []
            ):
                if ref not in elements or ref == element["id"]:
                    raise InputError(f"{element['id']}: invalid element reference {ref}")
            if "container" in element:
                parent = elements[element["container"]]
                if parent["kind"] != "shape" or parent["z"] >= element["z"]:
                    raise InputError(
                        f"{element['id']}: container must be a shape behind its content"
                    )
            if element["kind"] == "text":
                if element.get("min_font_size", element["font_size"] * 0.85) > element["font_size"]:
                    raise InputError(f"{element['id']}: minimum font size exceeds requested size")
                top, right, bottom, left = element.get("padding", [0, 0, 0, 0])
                if top + bottom >= element["box"][3] or left + right >= element["box"][2]:
                    raise InputError(f"{element['id']}: padding consumes the text box")
            if element["kind"] == "line" and element["points"][0] == element["points"][1]:
                raise InputError(f"{element['id']}: zero-length line")
            if element.get("shape") == "polygon":
                if "vertices" not in element or not strictly_convex(element["vertices"]):
                    raise InputError(
                        f"{element['id']}: polygon requires 3–32 distinct strictly convex vertices in perimeter order"
                    )
                if "radius" in element:
                    raise InputError(f"{element['id']}: polygon does not support corner radius")
            elif "vertices" in element:
                raise InputError(f"{element['id']}: vertices require shape=polygon")
            if "gradient" in element:
                offsets = [stop["offset"] for stop in element["gradient"]["stops"]]
                if (
                    element.get("fill") is not None
                    or offsets[0] != 0
                    or offsets[-1] != 1
                    or any(
                        round(b * 100000) <= round(a * 100000)
                        for a, b in zip(offsets, offsets[1:], strict=False)
                    )
                ):
                    raise InputError(
                        f"{element['id']}: gradient needs distinct ascending Office stop positions from 0 to 1 and no solid fill"
                    )
            if "dash" in element and (
                element.get("stroke_width", 1) <= 0
                or (element["kind"] == "shape" and not element.get("stroke"))
            ):
                raise InputError(
                    f"{element['id']}: dashes require a visible, positive-width stroke"
                )
            if "dash" in element and any(
                length / element.get("stroke_width", 1) > 21474 for length in element["dash"]
            ):
                raise InputError(
                    f"{element['id']}: dash/stroke ratio exceeds the Office integer range"
                )
            if "arrow_head" in element:
                head = element["arrow_head"]
                length = math.dist(*element["points"])
                if not element.get("arrow") or "dash" in element:
                    raise InputError(
                        f"{element['id']}: custom heads require arrow=true and a solid shaft"
                    )
                if element.get("stroke_width", 1) <= 0:
                    raise InputError(
                        f"{element['id']}: a custom arrow requires a positive shaft width"
                    )
                if head["length"] >= length or head["width"] < element.get("stroke_width", 1):
                    raise InputError(
                        f"{element['id']}: arrow head must be shorter than the line and at least as wide as its stroke"
                    )
        for element in elements.values():
            seen = {element["id"]}
            current = element
            while "container" in current:
                current = elements[current["container"]]
                if current["id"] in seen:
                    raise InputError("Cyclic containers")
                seen.add(current["id"])
    return copy.deepcopy(scene)


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_scene(path: Path) -> dict:
    if path.stat().st_size > 20_000_000:
        raise InputError("Scene exceeds 20 MB")
    return validate_scene(
        json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_pairs)
    )


@dataclass(frozen=True)
class Transform:
    scale: float
    x: float
    y: float
    width_inches: float
    height_inches: float

    def point(self, x: float, y: float) -> tuple[float, float]:
        return self.x + x * self.scale, self.y + y * self.scale

    def box(self, box: list) -> tuple[float, float, float, float]:
        x, y = self.point(box[0], box[1])
        return x, y, box[2] * self.scale, box[3] * self.scale


def slide_transform(scene: dict, slide: dict) -> Transform:
    first = scene["slides"][0]
    width = scene.get("slide_width_inches", 13.333333)
    height = width * first["height"] / first["width"]
    if height > 56:
        raise InputError("Presentation height exceeds PowerPoint's 56-inch limit")
    scale = min(width / slide["width"], height / slide["height"])
    return Transform(
        scale,
        (width - slide["width"] * scale) / 2,
        (height - slide["height"] * scale) / 2,
        width,
        height,
    )
