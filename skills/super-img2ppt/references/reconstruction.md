# Reconstruct from evidence

## Typography

An OCR rectangle surrounds visible ink. It is not a paragraph box, a baseline, or the font's
em square. Setting `font_size = box.height` and making a text frame the exact OCR size can
clip ascenders/descenders or over-shrink Chinese text. Extend the text frame within available
whitespace to include the font ascent/descent; estimate size from multiple letters at a known
font, then measure and render. Do not expand the box across adjacent content.

For example, an observed 30 px-high glyph might come from a 34 px font with a 46 px line box.
These numbers are illustrative, not a universal multiplier. Lowercase English ink and Chinese
square glyphs require different measurements. Group OCR lines by alignment, spacing and style;
do not turn every character into a separate textbox. Keep original line breaks when the source
clearly fixes them. Measure bold and italic faces separately.

For partial emphasis, use `runs` and keep their font-size ratio when shrinking. For a small
superscript, a separate positioned native text element is currently more faithful than an
unsupported style field. Connected Arabic shaping, vertical text, variable-font axes and complex
effects need a source-specific review; ordinary glyph coverage does not prove correct shaping.

Office and local image renderers can space mixed Chinese/Latin/digit sequences differently even
when the font name and glyph size match. Compare the positions of script transitions and the
right edge, not only whether the text fits. If the target renderer adds inter-script gaps that
cannot be expressed reliably by the current scene, split the line into a few semantic phrases
and number labels positioned from the source. Keep each phrase editable; do not split every
glyph or claim a text-content check proves exact spacing.

## Geometry and assets

Use a background color for flat backgrounds and native shapes for panels, rules and simple
symbols. Slanted convex nodes use polygon vertices; continuous colorbars can use a native linear
gradient sampled from the source. Adjacent tiny fill strips can reveal seams in actual document
renderers, even when their scene coordinates touch. Give an element a stable ID and explicit integer `z`. A textbox inside a panel names
the panel in `container`. Touching edges do not count as overlap; positive-area collisions do.
Bounding checks for ellipses/triangles use their actual convex footprint, while rounded rectangles
and chevrons use conservative bounding rectangles. A conservative warning can be reviewed with
a narrow named exemption; it must not trigger arbitrary repositioning.

Crop photos/icons only where the crop contains the intended object. Retain native transparency
when available. If background texture or an adjacent label is fused to an icon, preserve the
whole independent region and disclose its noneditable internal content, or use an authorized
image editing tool to separate it. Do not invent a lookalike brand mark. Never overlay new text
on the original screenshot containing that same text. A full-page screenshot belongs only in
`source`, outside the output's visible elements.

Represent a simple table using cell rectangles and text when values are readable. Bar charts
can use native bars/labels if their geometry is identifiable. Do not infer missing numeric data
from a curve. The current output uses editable shapes, not a native Excel-linked chart/table.
Connectors are native lines, but endpoints are fixed source coordinates; moving a node does not
automatically reroute them.

## Repairs

When text overflows, compare OCR text, actual font, font size, padding and intended line breaks
in that order. Correct a too-tight OCR-derived box before reducing font size. If the original
font is unavailable, use a documented substitute and remeasure all same-style text.

When shapes overlap, inspect the source: add a real container relationship, correct an erroneous
box/z-order, or document a specific intentional pair. Do not “repair” a diagram by moving nodes
or deleting decoration without source evidence. After changing geometry, repeat both preflight
and actual PPTX rendering because either can invalidate the earlier check.
