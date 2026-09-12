# Diagonal native labels

Text `rotation` accepts finite degrees from −360 to 360, clockwise in source-image coordinates.
`box` remains the unrotated horizontal frame; its center is the rotation pivot. Native PPTX
text and SVG text preserve the angle. Preflight containment/collision uses rotated geometry
and measured ink. Do not enter the rotated screen bounding rectangle as the unrotated frame.

For a formula or mixed superscript/subscript label, prefer `compose-math` with top-level
`rotation`. `origin` is the common source-coordinate baseline anchor and rotation pivot.
All part offsets are specified in the formula's unrotated coordinate system. The helper
rotates both part positions and their individual frames around that one anchor; rotating
frames without repositioning their centers would scatter the formula.

```json
{
  "id": "key_label", "origin": [1040, 144],
  "font_family": "Times New Roman", "font_size": 13, "rotation": -45,
  "parts": [
    {"text": "v", "offset": [0, 0], "italic": true},
    {"text": "1", "offset": [6, 3], "size_scale": 0.65},
    {"text": "AR", "offset": [6, -7], "size_scale": 0.65}
  ]
}
```

These are format examples, not inferred source coordinates. Inspect the source at high zoom
for angle, font roles and script positions. Replace the whole previous raster label strip,
not just part of its pixels. Native text must not be overlaid on baked copies of itself.

## Actual-render boundary

For non-quarter-turn text the actual PDF check selects glyph centers inside the rotated frame,
not merely inside its page-axis bounding rectangle. It checks expected text and font identity,
and compares the page-x ink span with the similarly rotated predicted span. The old vertical
width shortcut is not used for diagonal labels.

PDFium reports page-axis glyph rectangles, which cannot establish exact ink containment against
slanted frame edges. Therefore every diagonal text element retains the explicit warning
`diagonal_glyph_bounds_require_visual_review`. Existing text-mismatch, font-substitution and
page-axis overflow errors still block. This warning must not be suppressed to get PASS.
Inspect actual PPTX crops against source pixels (and use `compare-roi` where the ink is isolated).
PPTX/SVG editability and source fidelity are separate claims. PowerPoint/WPS are not attested
by a LibreOffice render.
