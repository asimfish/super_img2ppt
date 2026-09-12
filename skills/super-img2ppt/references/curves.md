# Reconstruct visible curve geometry

Inspect the source image first. A mathematical guess can match the overall trend while
moving every local extremum. Trace the visible stroke in source pixels, then render the
actual PPTX and compare it with the source. This helper creates native line fragments;
it does not recover experimental data, chart axes or an Excel-backed Office chart.

```bash
super-img2ppt trace-curve source.png --roi 100 80 300 160 \
  --color '#1F77B4' --stroke-width 1.5 --prefix loss_blue --out trace_01
```

The ROI is `[x, y, width, height]` in normalized source pixels. Inspect `source.png` when
EXIF orientation or transparency normalization affects coordinates. Choose the observed
stroke color; `--tolerance` is Euclidean RGB distance (default 80). Use a tight ROI containing
one distinguishable curve. Review the magenta `overlay.png`, `trace.json` and its recorded
short interpolations before merging `elements.json` into the matching slide. Give every
curve a unique prefix; arrange z-order and exact allowed joins against the full scene.
The fragment is not a complete scene, and a successful trace remains `review`.
A tight ROI can avoid a neighboring border yet omit a visible connector endpoint. Inspect
both endpoints against the full source, including frame contacts and arrow tips. Add a
separate native segment only for an observed omitted stroke, include it in the same curve
group, and recheck joins; never invent a hidden continuation to close a gap.

- A source-verified horizontal guide may be explicitly excluded with repeated
  `--exclude-band TOP BOTTOM` (absolute y, half-open). No automatic horizontal-line removal:
  a real plateau must survive. Each band is at most eight pixels; at most eight bands.
- `--max-gap` defaults to four columns, at most 16. Every interpolated column is reported.
  Do not raise it repeatedly to bridge hidden crossings. Split visible fragments or retain
  the smallest honest image-only crop and disclose its editing boundary.
- Default tracing assumes y is single-valued in x. For a steep fragment, `--axis y` traces
  x as a function of y; excluded bands then refer to original x coordinates. Returned
  points still use the original image coordinates. This does not resolve a multibranch curve.
- Same-color branches, filled regions, long gaps and insufficient observed coverage fail.
  A failed trace writes diagnostics without fabricated geometry. Use a new output directory.
- Three-point smoothing and Ramer–Douglas–Peucker simplification reduce pixel stair steps.
  `--simplify-px` defaults to 0.25; inspect extrema because smoothing can move them slightly.
  Source images are limited to 40 million pixels, ROI to four million pixels and the tracing
  axis to 6000 pixels. Simplification has a work limit and emits at most 2000 segments.
- Segments use `line_cap: "round"` so native PPTX ends overlap smoothly. The expanded caps
  also participate in bounds and overlap checks. This is not a single editable spline.

After merging, run `check` and `build` in fresh directories. Inspect both the whole figure
and source-width curve crops. Preserve original axes, legends, ticks and uncertainty bands;
never infer missing labels or hidden measurements from the traced line. Compare the actual
PPTX render, not just the helper overlay. Stop after three unresolved repairs to one region
and report the remaining limitation.

For outputs with multiple parts/segments, the helper also writes `groups.json` with one
semantic edit group (empty for a single object). Merge it into the slide's `groups` along
with `elements.json`, using unique IDs and keeping its leaves contiguous in paint order.
See [editing.md](editing.md); helper output remains unverified until full build and review.
