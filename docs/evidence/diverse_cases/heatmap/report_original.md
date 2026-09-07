# Original frozen-runtime forward test: heatmap

Frozen first-candidate report, created 2026-09-07T08:31:05.577515+00:00. This report refers only to `scene_01.json` and `build_01`; it must not be rewritten to include later scene or runtime fixes.

**Outcome: partial native reconstruction, overall acceptance unmet.** The original frozen runtime produced reviewable PPTX and SVG, and its automated native-object and rendered-text checks passed. All 49 matrix values are native editable text. Seven top coordinate labels remain a raster crop because the documented schema cannot express their approximately 30° rotation. The continuous colorbar was represented by 358 native sampled bands, and the actual PPTX render exhibits false dark horizontal seams. Two native label ROIs exceed the precommitted 2 px text-edge tolerance.

## Isolation and source

- Sole input: `/Users/liyufeng/Code/super_img2ppt/output/diverse_cases_20260906/raw/heatmap_source.png`, 640×480. Input SHA256 `7d07f73d16e3dafb7f74fbbac2b8aa2739e29e39e5e430bf918d811606baacd8`.
- Source was supplied as a published heatmap. Publication identity was not independently looked up, as browsing and other source material were forbidden.
- Job root: `/tmp/super-img2ppt-diverse-heatmap-UhTqQQ`. Only this temporary directory was intentionally modified. No dependencies were installed, no repositories/skills were edited, no commits or messages to external parties were made, and no web, other case, plotting source data, runtime source contents, or tests were consulted. Runtime files were hashed as opaque bytes only, to meet the requested runtime-hash requirement.
- Read the frozen `SKILL.md`, `references/reconstruction.md`, `references/scene.md`, `references/scene.schema.json`, and `references/qa.md`; ran `prepare`, opened the sole original and prepared source, and checked Vision OCR against the bitmap.
- OCR combined row labels with first-column values, joined two wheat zeros, altered `Farmer Joe` capitalization, and omitted the colorbar zero and `harvest [t/year]`. The supplied pixels were used to correct these. All 49 numeric values were visually legible; no chart/source data were consulted.

## Runtime and environment

- Frozen root: `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt`.
- Frozen file-manifest SHA256: `741f18b496d4fd5fd7f12f52a43edb817e8806bef7df310d9b40defe0a35d4d4`. Per-file hashes are in `provenance.json`; no semantic runtime-source inspection occurred.
- Python: 3.12.12 at `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python`; module is frozen `src` through command-local `PYTHONPATH`.
- Runtime 0.2.0; python-pptx 1.0.2; Pillow 12.3.0; fonttools 4.64.0; pypdfium2 5.13.0; jsonschema 4.26.0.
- LibreOffice 26.2.4.2 `0229ac93fcf0d7cbc6376066c6f35021cef002dc`; `soffice`, `fc-list`, and `tesseract` resolve under `/opt/homebrew/bin`. Existing LibreOffice font directory was supplied with `--font-dir`.
- Requested and resolved native font: DejaVu Sans regular, runtime font SHA256 `7da195a74c55bef988d0d48f9508bd5d849425c1770dba5d7bfc6ce9ed848954`. `fonts.json` reports no substitutions. Font identity cannot be uniquely established from source pixels; matching typeface name is not used as a fidelity claim. Fonts are not embedded.

## Content and editability

- 494 slide objects: 64 native text elements, 408 native shapes, 21 native lines, and 1 independent raster image.
- Native text: 49 matrix values, seven row labels, seven legend numbers (0 through 6), and the 90° legend title.
- Native shapes: 49 filled matrix cells, 358 source-sampled horizontal colorbar bands, one colorbar backing/outline rectangle. The six measured internal white grid gaps arise between native cell rectangles.
- Native lines: seven top ticks, seven row ticks, seven legend ticks.
- Raster boundary: only `[100,10,497,91]`, containing the seven top coordinate labels; not the entire source. It is independently movable but its internal label text cannot be edited. Names are also transcribed in slide notes. No editable duplicate text overlays the raster.
- The heatmap is an arrangement of native text/shapes, not an Excel-linked chart/table. A native gradient primitive and arbitrary-angle native text are outside this frozen schema.

| Crop / farmer | Farmer Joe | Upland Bros. | Smith Gardening | Agrifun | Organiculture | BioGoods Ltd. | Cornylee Corp. |
|---|---|---|---|---|---|---|---|
| cucumber | 0.8 t | 2.4 t | 2.5 t | 3.9 t | 0.0 t | 4.0 t | 0.0 t |
| tomato | 2.4 t | 0.0 t | 4.0 t | 1.0 t | 2.7 t | 0.0 t | 0.0 t |
| lettuce | 1.1 t | 2.4 t | 0.8 t | 4.3 t | 1.9 t | 4.4 t | 0.0 t |
| asparagus | 0.6 t | 0.0 t | 0.3 t | 0.0 t | 3.1 t | 0.0 t | 0.0 t |
| potato | 0.7 t | 1.7 t | 0.6 t | 2.6 t | 2.2 t | 6.2 t | 0.0 t |
| wheat | 1.3 t | 1.2 t | 0.0 t | 0.0 t | 0.0 t | 3.2 t | 5.1 t |
| barley | 0.1 t | 2.0 t | 0.0 t | 1.4 t | 0.0 t | 1.9 t | 6.3 t |


Legend: `harvest [t/year]`, visible tick labels 0, 1, 2, 3, 4, 5, 6. The source colorbar extends slightly above 6, but no missing numerical tick was invented.

## Original check/build results and retained failures

| Invocation | Exit | Wall seconds |
|---|---:|---:|
| `--help` | 0 | 2.031 |
| `doctor` | 0 | 2.014 |
| `prepare /Users/liyufeng/Code/super_img2ppt/output/diverse_cases_20260906/raw/heatmap_source.png --out job` | 0 | 17.650 |
| `check --help` | 0 | 0.955 |
| `build --help` | 0 | 0.956 |
| `check job/scene.json --out check_01 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` | 0 | 15.017 |
| `build job/scene.json --out build_01 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` | 0 | 25.498 |

`check_01` and `build_01` are preserved unchanged. Neither returned a blocking failure: both returned `review` with exit 0. Therefore there is no discarded initial check/build error. `build_01/validation.json` reports preflight `review`, native objects `pass`, rendered text `pass`, overall `review`, and `visual_review: required`. The warning explicitly records the noneditable top-label crop. Three informational findings concern blank text-frame space near the rotated colorbar label.

The actual `build_01/render/page_001.png` was opened. It is a 1600×1200 raster from the exported PPTX through LibreOffice PDF, not an unrelated mock. Comparison images and a colorbar crop were inspected. This is LibreOffice evidence only; PowerPoint/WPS were not opened.

## Fixed ROI measurements

The 72 ROIs, transcription, and thresholds were committed before scene authoring/first check and build. Final pre-candidate ROI-plan SHA256: `beda47e44850c08a708b839d14fb99e19fcb71e409cbc22c60e8559b1b3e78cf`. A source-visible white `3.2 t` mask annotation was corrected before the first candidate; no ROI or threshold changed after first candidate generation.

Coordinates use source pixels. Actual PPTX raster was downsampled with LANCZOS to 640×480 before comparison; edges are thresholded pixel-cell bounds. Text mask uses maximum absolute RGB-channel distance ≥70 from the known source background. White grid mask requires all RGB channels ≥250. Bottom ink edge is a baseline proxy, not a typographic baseline. Horizontal/vertical grid stroke centers are computed from the two pixel-cell edges, respecting the half-pixel distinction.

| Group | ROIs | Within tolerance | Maximum relevant edge error |
|---|---:|---:|---:|
| All selected ROIs | 72 | 70 | 3 px |
| All native text | 64 | 62 | 3 px |
| Matrix numeric cells | 49 | 49 | 2 px |
| Internal grid gaps | 6 | 6 | 1 px |
| Raster top-label strip | 1 | 1 | 1 px |

Thresholds: native text ≤2 px per edge; grid ≤1 px per measured edge. **These are bounded edge comparisons, not a global fidelity percentage.** Mean text-mask IoU is 0.5096, showing that meeting bounding-edge tolerance does not imply pixel-identical glyph shapes.

Failed fixed ROIs (deltas are rendered minus source `[left, top, right, bottom]`):

- `row_label_1` (`cucumber`): `[3, 0, 1, 1]` px. Left edge exceeds tolerance by 1 px.
- `colorbar_label`: `[-2, 0, -3, -1]` px. Right edge exceeds tolerance by 1 px.

All 72 region bboxes, signed edge deltas, bottom-ink proxies, grid-center/width deltas, mask pixel counts, IoU, and per-region acceptance results are in `measurements_build_01/measurements.json`.

## Supplemental colorbar seam evidence

This ROI was selected **after** opening the first render, because the initial fixed ROI plan measured the colorbar boundary but did not quantify its interior. It is separately labeled supplemental and does not replace the fixed 72-ROI result.

- Interior ROI `[545,100,558,454]` in source coordinates.
- Source-size RGB MAE: 9.341 / 255; average luminance darkening: 10.909 / 255.
- 206 / 354 source scan rows are darkened by more than 10 / 255.
- At the actual 1600×1200 render, the center-column residual has 203 distinct dark runs above 12 / 255. These are diagnostic residual counts, not a precommitted acceptance criterion.
- Own generated PPTX XML was inspected: sampled band `colorbar_band_100` uses `a:ln/a:noFill`. Repeated false lines are consistent with the actual renderer exposing the black backing between antialiased adjacent fills, not explicitly authored black band outlines. This is an inference from the export and render, not runtime-source analysis.
- Full row profiles and numerical residuals: `measurements_build_01/colorbar_seam_supplemental.json`.
- Actual evidence: `measurements_build_01/colorbar_source_vs_actual_2x.png` (source left, actual PPTX right), `build_01/render/page_001.png`, and `measurements_build_01/source_vs_actual.png`.

## Candidate paths and limits

- PPTX: `build_01/editable.pptx`.
- SVG: `build_01/svg/page_001.svg`.
- Resolved scene/assets: `build_01/scene.resolved.json`, `build_01/assets/`.
- Font manifest and validation: `build_01/fonts.json`, `build_01/validation.json`.
- Original scene and ROI plan: `scene_01.json`, `roi_plan_frozen.json`.
- Commands/stdout/stderr/exit codes/timings: `commands.jsonl`; exact scripts are retained in the temporary root. Additional read/visual accesses are listed in `command_access_audit.md`.
- Runtime/source hashes: `provenance.json`; selected immutable first-candidate artifact hashes: `original_artifact_hashes.json`.

No repairs were applied before freezing this original report (zero of three allowed per-region repair attempts used). Parent requested preserving this original report before a prospective candidate-runtime test. Later results must be recorded under different filenames/directories. Original acceptance remains unmet because arbitrary-angle labels are raster, the native band approximation visibly seams, and two label edge measurements fail the fixed tolerance.
