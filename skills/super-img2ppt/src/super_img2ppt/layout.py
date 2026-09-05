"""Explicit, measured line layout. Never move a source object to hide an error."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import regex
from PIL import Image, ImageDraw

from .fonts import FontCatalog, FontFace, ink_bounds, is_cjk, measure, pil_font

OPENING = set("([{（【《「『〈〔“‘")
CLOSING = set(")]}）】》」』〉〕，。！？；：、,.!?;:%”’")


@dataclass(frozen=True)
class Fragment:
    text: str
    face: FontFace
    size: float
    bold: bool
    italic: bool
    color: str


@dataclass
class Line:
    fragments: list[Fragment]
    width: float
    ascent: float
    descent: float
    height: float

    @property
    def text(self) -> str:
        return "".join(f.text for f in self.fragments)


@dataclass
class TextLayout:
    lines: list[Line]
    scale: float
    width: float
    height: float
    available_width: float
    available_height: float
    fits: bool
    effective_font_size: float

    def report(self) -> dict:
        return {
            "scale": round(self.scale, 6),
            "effective_font_size_px": round(self.effective_font_size, 4),
            "width_px": round(self.width, 3),
            "height_px": round(self.height, 3),
            "available_width_px": self.available_width,
            "available_height_px": self.available_height,
            "safety_reserve_px": 0.5,
            "required_width_px": round(self.width + 0.5, 3),
            "required_height_px": round(self.height + 0.5, 3),
            "fits": self.fits,
            "lines": [line.text for line in self.lines],
        }


def _same_style(a: Fragment, b: Fragment) -> bool:
    return (a.face, a.size, a.bold, a.italic, a.color) == (
        b.face,
        b.size,
        b.bold,
        b.italic,
        b.color,
    )


def merge_fragments(atoms: list[Fragment]) -> list[Fragment]:
    merged: list[Fragment] = []
    for atom in atoms:
        if merged and _same_style(merged[-1], atom):
            merged[-1] = replace(merged[-1], text=merged[-1].text + atom.text)
        else:
            merged.append(atom)
    return merged


def make_line(atoms: list[Fragment], line_height: float, empty_style: Fragment) -> Line:
    fragments = merge_fragments(atoms) if atoms else [replace(empty_style, text="")]
    metrics = [measure(f.face, f.text, f.size) for f in fragments]
    width = sum(m[0] for m in metrics)
    ascent, descent = max(m[1] for m in metrics), max(m[2] for m in metrics)
    height = max(ascent + descent, max(f.size for f in fragments) * line_height)
    return Line(fragments, width, ascent, descent, height)


def atoms_for(element: dict, catalog: FontCatalog, scale: float) -> list[Fragment]:
    atoms = []
    runs = element["runs"] if "runs" in element else [{"text": element["text"]}]
    for run in runs:
        style = {**element, **run}
        text = run["text"].replace("\r\n", "\n").replace("\t", "    ")
        for cluster in regex.findall(r"\X", text):
            face = catalog.resolve(
                cluster,
                style.get("font_family"),
                style.get("cjk_font_family"),
                style.get("bold", False),
                style.get("italic", False),
            )
            atoms.append(
                Fragment(
                    cluster,
                    face,
                    style["font_size"] * scale,
                    style.get("bold", False),
                    style.get("italic", False),
                    style.get("color", "#111827"),
                )
            )
    return atoms


def tokens_for(atoms: list[Fragment]) -> list[list[Fragment]]:
    tokens: list[list[Fragment]] = []
    for atom in atoms:
        if not tokens:
            tokens.append([atom])
            continue
        prev = tokens[-1][-1].text
        char = atom.text
        if char == "\n" or prev == "\n":
            tokens.append([atom])
        elif char in CLOSING or prev in OPENING:
            tokens[-1].append(atom)
        elif char.isspace() != prev.isspace() or is_cjk(char) or is_cjk(prev):
            tokens.append([atom])
        else:
            tokens[-1].append(atom)
    return tokens


def layout_at(element: dict, catalog: FontCatalog, scale: float) -> TextLayout:
    top, right, bottom, left = element.get("padding", [0, 0, 0, 0])
    available_w, available_h = element["box"][2] - left - right, element["box"][3] - top - bottom
    atoms = atoms_for(element, catalog, scale)
    if atoms:
        empty_style = atoms[0]
    else:
        face = catalog.resolve(
            " ",
            element.get("font_family"),
            element.get("cjk_font_family"),
            element.get("bold", False),
            element.get("italic", False),
        )
        empty_style = Fragment(
            "", face, element["font_size"] * scale, False, False, element.get("color", "#111827")
        )
    line_height = element.get("line_height", 1.15)
    lines: list[Line] = []
    current: list[Fragment] = []
    for token in tokens_for(atoms):
        if token[0].text == "\n":
            lines.append(make_line(current, line_height, empty_style))
            current = []
            continue
        candidate = current + token
        line = make_line(candidate, line_height, empty_style)
        if (
            element.get("wrap", False)
            and current
            and line.width > available_w - 0.5
            and not all(a.text.isspace() for a in token)
        ):
            lines.append(make_line(current, line_height, empty_style))
            current = token
        else:
            current = candidate
    lines.append(make_line(current, line_height, empty_style))
    width = max(line.width for line in lines)
    height = sum(line.height for line in lines)
    # A small physical reserve prevents a one-rounding-unit overflow in Office.
    fits = width <= available_w - 0.5 and height <= available_h - 0.5
    return TextLayout(
        lines, scale, width, height, available_w, available_h, fits, element["font_size"] * scale
    )


def fit_text(element: dict, catalog: FontCatalog) -> TextLayout:
    initial = layout_at(element, catalog, 1)
    if initial.fits or element.get("fit", "strict") == "strict":
        return initial
    lower = element.get("min_font_size", element["font_size"] * 0.85) / element["font_size"]
    smallest = layout_at(element, catalog, lower)
    if not smallest.fits:
        return smallest
    upper = 1.0
    for _ in range(16):
        middle = (lower + upper) / 2
        if layout_at(element, catalog, middle).fits:
            lower = middle
        else:
            upper = middle
    return layout_at(element, catalog, lower)


def layout_scene(scene: dict, catalog: FontCatalog) -> dict[tuple[str, str], TextLayout]:
    results = {}
    groups: dict[str, list[tuple[dict, dict]]] = {}
    for slide in scene["slides"]:
        for element in slide["elements"]:
            if element["kind"] != "text":
                continue
            results[slide["id"], element["id"]] = fit_text(element, catalog)
            if "font_group" in element:
                groups.setdefault(element["font_group"], []).append((slide, element))
    for members in groups.values():
        strict_members = [e for _, e in members if e.get("fit", "strict") == "strict"]
        factor = 1 if strict_members else min(results[s["id"], e["id"]].scale for s, e in members)
        min_factor = max(
            e.get("min_font_size", e["font_size"] * 0.85) / e["font_size"] for _, e in members
        )
        factor = max(factor, min_factor)
        for slide, element in members:
            results[slide["id"], element["id"]] = layout_at(element, catalog, factor)
    return results


def positioned_lines(element: dict, layout: TextLayout):
    top, right, bottom, left = element.get("padding", [0, 0, 0, 0])
    x, y, width, height = element["box"]
    spare = height - top - bottom - layout.height
    valign = element.get("valign", "top")
    y += top + ({"top": 0, "middle": spare / 2, "bottom": spare}[valign])
    for line in layout.lines:
        dx = {
            "left": 0,
            "center": (width - left - right - line.width) / 2,
            "right": width - left - right - line.width,
        }[element.get("align", "left")]
        yield x + left + dx, y, line
        y += line.height


def text_ink_mask(element: dict, layout: TextLayout):
    """Bounded 4x mask for refining collisions near sloping edges and glyph corners."""
    boxes = text_ink_boxes(element, layout)
    if not boxes:
        return None
    left = math.floor(min(b[0] for b in boxes)) - 1
    top = math.floor(min(b[1] for b in boxes)) - 1
    right = math.ceil(max(b[2] for b in boxes)) + 1
    bottom = math.ceil(max(b[3] for b in boxes)) + 1
    width, height = (right - left) * 4, (bottom - top) * 4
    if width * height > 8_000_000:
        return None  # Retain conservative box geometry for unusually large text.
    mask = Image.new("L", (width, height))
    draw = ImageDraw.Draw(mask)
    for x, y, line in positioned_lines(element, layout):
        for fragment in line.fragments:
            draw.text(
                ((x - left) * 4, (y + line.ascent - top) * 4),
                fragment.text,
                font=pil_font(fragment.face, fragment.size),
                fill=255,
                anchor="ls",
            )
            x += measure(fragment.face, fragment.text, fragment.size)[0]
    return mask, left, top


def text_ink_boxes(element: dict, layout: TextLayout) -> list[tuple[float, float, float, float]]:
    boxes = []
    for x, y, line in positioned_lines(element, layout):
        for fragment in line.fragments:
            bounds = ink_bounds(fragment.face, fragment.text, fragment.size)
            if bounds is None and fragment.text.strip():
                # Partial measurements must not hide an unmeasured large run.
                return []
            if bounds is not None:
                left, top, right, bottom = bounds
                boxes.append((x + left, y + line.ascent + top, x + right, y + line.ascent + bottom))
            x += pil_font(fragment.face, fragment.size).getlength(fragment.text) / 4
    return boxes
