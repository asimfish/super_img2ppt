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
| text | `box`, `font_size`, exactly one of `text` or `runs` | `font_family`, `cjk_font_family`, `bold`, `italic`, `color`, `align`, `valign`, `padding`, `wrap`, `line_height`, `fit`, `min_font_size`, `font_group` |
| shape | `box`, `shape` | `fill`, `stroke`, `stroke_width`, `radius` |
| line | `points: [[x1,y1],[x2,y2]]` | `stroke`, `stroke_width`, `arrow` |
| image | `box`, `path`, `provenance`, `contains_text` | `image_fit: contain/cover/stretch` |

Shapes: `rect`, `round_rect`, `ellipse`, `triangle`, `diamond`, `chevron`. Colors: `#RRGGBB`.
Missing/null fill or stroke means none for shapes; lines default to a 1 px dark stroke.
Alignment: `left/center/right`; vertical alignment: `top/middle/bottom`.
Padding order: `[top, right, bottom, left]`, default all zero. Line height defaults to 1.15 em
and never goes below real ascent plus descent. `wrap` defaults to false and preserves explicit
newlines. The exporter writes explicit measured lines with Office autofit disabled.

A run contains `text` and optional font fields from the containing textbox; run size and
emphasis are preserved. Escape newlines in JSON strings as `\n`. Unknown fields are rejected.
Rotation, gradients and editable chart data are not part of v1; do not silently add ignored keys.

All objects may have `container`, `confidence`, `role`, `allow_overlap_with`, `overlap_reason`.
`container` must refer to a shape at a lower z-order and contain the entire child.
`role: background` permits a text-free background behind content; it does not authorize copying
the source screenshot. All asset paths are local, relative to the scene directory, and confined
to it even after resolving symlinks. URLs and absolute paths are rejected.

`fonts.latin` and `fonts.cjk` may each set a prioritized list of fallback families. Missing glyphs
are a hard error. `--font-dir` adds user-selected font search directories without installing or
copying fonts. Inspect `fonts.json` to see resolved family, face index, hash and embedding rights;
the runtime does not embed fonts or infer permission to redistribute them.
