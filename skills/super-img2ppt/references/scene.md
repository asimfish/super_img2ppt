# Scene v1

All geometry and typography use source-image pixels, top-left origin. Each slide records its
actual source dimensions. The first page determines the deck aspect ratio; later pages fit
uniformly inside it with letterboxing. `slide_width_inches` defaults to 13.333333. Font point
size in PPTX equals `font_size * transform.scale * 72`.

```json
{
  "version": 1,
  "slides": [{
    "id": "page_001", "width": 1280, "height": 720,
    "source": "pages/page_001/source.png", "background": "#FFFFFF",
    "notes": "Original notes", "reviewed": true,
    "elements": [
      {"id": "card", "kind": "shape", "z": 1,
       "box": [60, 60, 600, 180], "shape": "round_rect", "radius": 12,
       "fill": "#EDF3FC"},
      {"id": "title", "kind": "text", "z": 2, "container": "card",
       "box": [84, 84, 552, 90], "text": "Editable 中文", "font_size": 36,
       "font_family": "Arial", "cjk_font_family": "Noto Sans CJK SC",
       "bold": true, "fit": "strict", "wrap": false}
    ]
  }]
}
```

`source` is optional for hand-authored scenes; image conversion should retain it for comparison.
`elements` is empty in a prepared draft and must be reconstructed before building.

| Object | Required fields beyond `id`, `kind`, `z` | Useful optional fields |
| --- | --- | --- |
| text | `box`, `font_size`, exactly one of `text` or `runs` | `font_family`, `cjk_font_family`, `bold`, `italic`, `color`, `align`, `valign`, `padding`, `wrap`, `line_height`, `fit`, `min_font_size`, `font_group`, `rotation` |
| shape | `box`, `shape` | `fill`, `stroke`, `stroke_width`, `radius`, `dash`, `vertices`, `gradient` |
| line | `points: [[x1,y1],[x2,y2]]` | `stroke`, `stroke_width`, `arrow`, `arrow_head`, `dash` |
| image | `box`, `path`, `provenance`, `contains_text` | `image_fit: contain/cover/stretch` |

Shapes: `rect`, `round_rect`, `ellipse`, `triangle`, `diamond`, `chevron`, `polygon`. Colors: `#RRGGBB`.
Missing/null fill or stroke means none for shapes; lines default to a 1 px dark stroke.
Alignment: `left/center/right`; vertical alignment: `top/middle/bottom`.
Padding order: `[top, right, bottom, left]`, default all zero. Line height defaults to 1.15 em
and never goes below real ascent plus descent. `wrap` defaults to false and preserves explicit
newlines. The exporter writes explicit measured lines with Office autofit disabled.

A run contains `text` and optional font fields from the containing textbox; run size and
emphasis are preserved. Escape newlines in JSON strings as `\n`. Unknown fields are rejected.
The v0.2 and v0.3 runtimes extend scene v1 with the optional fields below. Arbitrary-angle
rotation and editable chart data remain unsupported; do not silently add ignored keys.

In v0.3, a shape can use `gradient` instead of a solid `fill`. For example:
`"gradient": {"direction": "vertical", "stops": [{"offset": 0, "color": "#FFFFE5"},
{"offset": 0.5, "color": "#78C679"}, {"offset": 1, "color": "#004529"}]}`.
Use 2–16 ordered stops covering exactly 0–1. Stops must remain distinct after rounding to
Office's 1/100000 position units. `vertical` runs top to bottom; `horizontal` left to right.
Sample colors and stop positions from the source; do not invent chart values. PPTX and SVG
both retain one editable gradient shape. Radial gradients, opacity and arbitrary gradient directions remain
unsupported. A sampled gradient approximates its source color map and still needs comparison.

The v0.3 runtime also supports `shape: "polygon"` with `vertices`: 3–32 normalized `[u,v]`
pairs within `[0,1]`, relative to `box`. For example, `box: [100,30,200,180]` and
`vertices: [[0,0],[1,0.2],[1,0.8],[0,1]]` create a slanted encoder with actual corners
`[100,30]`, `[300,66]`, `[300,174]`, `[100,210]`. List perimeter vertices in either winding,
without repeating the first point. Only strictly convex polygons are supported; concave,
self-crossing, duplicate or collinear vertices are rejected. Polygons export as native editable
freeforms, with round stroke joins. They support fill, stroke, dash and text containers;
collision and containment use the actual slanted footprint. Curves and polygon corner radii
remain unsupported. Do not approximate an unsupported path with a misleading rectangle.

- `rotation`: text only, finite degrees between `-360` and `360`, clockwise in screen coordinates.
  The `box` is the **unrotated horizontal** text frame. Fit its text normally, then rotate about
  `[x+w/2, y+h/2]`. For a final vertical footprint `[x,y,w,h]`, use horizontal box
  `[x+w/2-h/2, y+h/2-w/2, h, w]` and `rotation: 90` or `-90`. This preserves native text,
  font runs and editability. For diagonal text and compound formulas, read
  [diagonal_text.md](diagonal_text.md); actual slanted-edge ink containment requires visual review.
- `dash: [on, off]`: positive source-pixel dash and gap lengths for lines or shape outlines.
  Requires a positive visible stroke. No automatic split into hundreds of line elements.
  Collision checks conservatively treat the complete stroke as occupied, including gaps.
- `arrow_head: {"length": 12, "width": 10}`: requires `arrow: true`, a positive solid shaft,
  a head shorter than the point-to-point distance, and width at least the shaft width.
  The final point is the tip. The arrow exports as one editable native freeform, with geometry
  shared by SVG and QA; it does not reconnect automatically when a node is moved.
  Combining custom heads with `dash` is rejected. Legacy arrows without `arrow_head` retain
  native Office connector heads; QA uses conservative SVG-sized head bounds.

All objects may have `container`, `confidence`, `role`, `allow_overlap_with`, `overlap_reason`.
`container` must refer to a shape at a lower z-order and contain the child's visible text ink
(including its rotation), or the full geometry of a non-text child.
`role: background` permits a text-free background behind content; it does not authorize copying
the source screenshot. All asset paths are local, relative to the scene directory, and confined
to it even after resolving symlinks. URLs and absolute paths are rejected.

`fonts.latin` and `fonts.cjk` may each set a prioritized list of fallback families. Missing glyphs
are a hard error. `--font-dir` adds user-selected font search directories without installing or
copying fonts. Inspect `fonts.json` to see resolved family, face index, hash and embedding rights;
the runtime does not embed fonts or infer permission to redistribute them.

## Plain line end caps

Optional `line_cap: "round" | "butt"` controls native PPTX and SVG line ends. Omission
preserves existing behavior. Explicit caps require a plain line without `arrow: true`.
Rounded caps extend half the stroke width beyond both endpoints; bounds and collisions
include that footprint. Adjacent traced segments need specific, source-verified overlap
declarations; a cap does not exempt unrelated objects.
