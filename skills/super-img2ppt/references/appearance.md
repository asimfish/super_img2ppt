# Color and ink-density acceptance

Geometry PASS does not mean colors match. Never substitute a shared palette for sampled
source colors in faithful conversion. Preserve distinct colors for text, outlines, fills,
arrows and legends even when they belong to one module. Inspect at equal source scale:
wrong hue and thinner/smaller text can both make a figure look pale.

## Capture the intended appearance before reconstruction

Open the actual source. Select isolated representative regions for each important visual role:
flat panel fill, main arrow, secondary border, heading, body label and legend/category color.
Record source pixels; do not infer exact colors from a screenshot displayed at reduced size.
Use native font weight and stroke width, not darker RGB alone, to recover source ink density.
Record which regions remain unchecked. A few sampled regions cannot certify the entire page.

For faithful conversion, sample the source directly. If the user explicitly requests a palette
change, retain the faithful baseline and record the target RGB and reason. Do not silently
switch to target mode to make a failing source match pass. New target colors still need actual
PPTX verification; `restyle` does not automatically perform this gate. Rebuild each resulting
portable scene using its appropriate appearance plan.

## Run an actual-render gate

```bash
super-img2ppt build JOB/scene.json --appearance-plan JOB/appearance-plan.json --out JOB/build_01
```

```json
{
  "version": 1,
  "regions": [
    {"id": "panel_fill", "slide": "page_001", "roi": [80, 80, 20, 20], "kind": "solid", "mode": "faithful"},
    {"id": "main_arrow", "slide": "page_001", "roi": [100, 200, 120, 20], "kind": "ink", "mode": "faithful", "background": "#FFFFFF", "max_channel_delta": 12, "density_ratio": [0.8, 1.25]},
    {"id": "requested_accent", "slide": "page_001", "roi": [300, 80, 20, 20], "kind": "solid", "mode": "target", "target_color": "#1B717D", "reason": "User requested a solid teal center instead of white"}
  ]
}
```

Coordinates are source pixels, `[x, y, width, height]`. Each slide needs its exact-sized local
`source`. `actual_roi` optionally locates the equivalent region after an intentional layout
change; compare matching content and geometry, not unrelated crops. Ink regions must have
identical source/actual dimensions so a smaller ROI cannot hide thinner strokes. Region IDs must be unique.
ROIs are at least 2×2 and at most 1 MP; at most 128 regions per plan. Unknown fields, duplicate
JSON keys, unbounded/nonfinite tolerances, missing slides and invalid ROIs fail.

- `solid`: place entirely inside a flat fill, away from text and antialiased borders. Mixed
  colors/gradients are rejected; use multiple isolated stop regions for gradients.
- `ink`: isolate one label, stroke or same-color geometry with the correct `background`.
  The foreground is selected by background contrast, **not** by the expected hue, so a wrong
  color cannot disappear from the comparison. The highest-contrast quartile estimates core
  color; mixed hues fail. At least four foreground pixels are required. `min_contrast`
  defaults to 16 (1–128); pale or subpixel-only strokes may lack reliable core samples.
- Default color tolerance is a maximum **sRGB channel difference of 12**, not perceptual ΔE
  or a universal aesthetic threshold. Explicit `max_channel_delta` may range from 0 to 64.
- `ink` also compares integrated background contrast divided by core contrast, normalized by
  ROI area, to estimate ink coverage. Default actual/source ratio is 0.8–1.25. A thin line or
  smaller/lighter type can fail even when RGB matches. It is not an exact font-weight or
  line-width measurement; same-hue clutter can compensate lost ink. Isolate the intended
  object and follow up with geometry and actual-size visual inspection. Ink comparisons use
  a common background; a redesign that changes the background also needs a separate region
  plan appropriate to the new reference, rather than treating background fill as text ink.
  If intentional geometry changes justify other limits, state them in the review record.

The runtime renders the actual Office-exported PDF directly at source scale, removes known
letterboxing, and never registers or resizes an existing preview to manufacture a match.
Source EXIF orientation and alpha-on-white are normalized; tagged ICC references must first
be deliberately normalized to sRGB. Non-sRGB PDF behavior is not calibrated by this check.

## Interpret and deliver

`appearance/` contains the exact plan, reference/PDF hashes, source and actual ROI crops, and
`appearance.json` with separate color and density findings. Region failures block the build.
Uncovered source slides yield `review`. Without a plan, source-backed builds now yield `review`
and `appearance: not_run`; `--no-render` remains `unverified`. Existing scenes still build,
but old geometry-only evidence must not be described as color-verified.

Inspect every failed crop. Fix wrong source sampling, scene colors, stroke width or typography
at their actual cause; do not increase tolerance repeatedly or sample a different region just
to pass. Retain ambiguous regions as unresolved. `pass` covers selected regions and thresholds
only; `visual_review` stays required. Confirm intended layout, semantic color mappings, arrows,
formula styles and target editor appearance separately.

For a hosted gallery, check the deployed source selection, embedded preview, downloadable
PPTX/SVG/PDF and cache freshness together. An updated SVG alone does not prove that the page
shows the latest actual-PPTX preview. Identify intentional redesigns separately from faithful
reconstructions and keep their reference/target record with the deliverables.
