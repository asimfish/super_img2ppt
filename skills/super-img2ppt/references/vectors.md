# Editable vector details

Use this when a small icon, transparency, outline or sampled color is being lost during
reconstruction. Geometry uses source pixels; colors are interpreted in normalized sRGB.

## Measure source colors first

```bash
super-img2ppt sample-color source.png --roi 534 31 5 5 --out purple_sample
super-img2ppt sample-color source.png --roi 120 80 40 20 --kind ink --out stroke_sample
```

Use the normalized source from `prepare`. `color.json` records the source hash, ROI,
core color, agreement and color-management metadata; `sample.png` retains the patch.
Copy `measurement.hex` into the appropriate scene fill/stroke/text field only after
checking which object the patch belongs to. Sample shape interiors away from text,
strokes and antialiasing. Ink sampling suppresses edges without selecting an expected hue.
A mixed patch/gradient cannot supply one flat color and returns `fail`; choose actual gradient
stops or a better isolated region. Repeated blocks with the same semantic color should
reuse a verified palette entry. Sampling does not bypass the rendered appearance gate.

## One flat icon, one native shape

```bash
super-img2ppt trace-icon source.png --roi 1277 196 59 60 \
  --color '#4295FF' --tolerance 64 --simplify-px 0.75 \
  --prefix legend_frozen_icon --out icon_trace
```

Inspect the ROI first. `icon.json` contains one `shape: freeform` element in original
source coordinates. Merge it into the scene at the correct paint slot and update any
container/group references. `overlay.png` shows the traced boundary. The element is one
selectable native object in PPTX; its contour points and fill remain editable. Existing
module/legend groups can contain this leaf. No raster picture or hundreds of separate
rectangles are used to fake a vector silhouette.

The helper selects foreground by explicit RGB tolerance and rejects clipped boundaries,
empty masks, holes, disconnected islands and ambiguous corner contacts. It never drops
small components. One uniform alpha is retained; varying alpha is rejected. Background
inference, automatic icon recognition and multi-color/path recovery are not supported.
Maximum ROI: 65536 pixels; boundary: 16384 edges; output: 256 vertices. Simplification is
explicit and bounded to 0–1 source pixel; 0 keeps exact orthogonal boundary vertices.
Increase it only after inspecting the comparison, never silently to force acceptance.
The color threshold and flattening of source antialiasing require actual-render review.

A low-resolution BLIP-2 snowflake has disconnected thresholded components and remains
raster. A larger GR00T N1 snowflake can be represented by one 130-point native contour.
Both behaviors are recorded in the 2026-10-10 tests; they do not imply all icons are recoverable.

## Preserve separate alpha and outlines

For a shape, set `fill_opacity` and `stroke_opacity` independently in 0–1. A gradient stop
can set `opacity`, multiplied by the shape's `fill_opacity`. Lines use `stroke_opacity`,
including custom arrow heads. Omission retains full opacity. Zero stroke width means no
stroke. Transparent raster alpha remains independently supported.

Do not infer alpha uniquely from one flattened color: a pale opaque fill and a saturated
translucent fill can yield identical pixels on one background. When alpha is unsupported by
evidence, use the measured flattened fill and disclose it. Test overlapping colors on their
actual backgrounds. Open XML alpha is stored on the color, as documented by
[Microsoft](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.drawing.alpha?view=openxml-3.0.1).

Use `compare-roi` on the actual PPTX PDF rendered at source scale for icon/color diagnostics.
Whole-page screenshots may hide a bad small icon. Keep the source ROI, mask color/tolerance,
edge deltas and pre/post edit artifacts; compare neighboring objects after moving/recoloring.
PowerPoint and WPS still need viewer-specific checks.
