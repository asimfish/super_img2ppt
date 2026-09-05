# ViT bitmap reconstruction: independent original evaluation

Input: `/Users/liyufeng/Code/super_img2ppt/output/conference_cases_20260906/raw/vit_figure.png`, 930 × 485 px, SHA-256 `4614d5404f0feb77c6d1dfc6b9db00969acf08387f3ec886f9fd06bb81d51b26`. Only this bitmap was used; no original PDF, vector figure, existing reconstruction, or external image service was used. Job: `/tmp/super-img2ppt-conference-vit-dVqHtY/job`.

The delivered original draft is `job/build_01/editable.pptx`. It contains 35 editable text objects, 47 editable shapes and 69 native lines. Ten photograph-only crops remain raster (one input patch grid and nine output patch photographs); no text or entire source image is used as a visible raster background. Source crop assets are in `job/assets`. Some panel labels were deliberately split at the source's semantic line breaks. All scene coordinates and font sizes use source pixels.

The workflow followed the installed `super-img2ppt` skill, including opening prepared source.png, reviewing OCR, running check, actual LibreOffice rendering, inspecting whole-page and enlarged detail comparisons, and recording failures. No dependencies were installed and no repository code was modified by this evaluator. The parent task modified the shared runtime during evaluation. `build_01` is the original feature-use baseline (no candidate arrow_head, dash or rotation fields); subsequent builds must be labelled candidate working-tree evaluations. Runtime source was not snapshotted before the first build, so this is artifact-level evidence rather than a reproducible claim about a frozen commit.

## Original failures and repairs

1. OCR misread `Class` as `Cass`, `Projection` as `Proiection`, full-width punctuation in the title and `[class]`, and failed on most numeric position tokens. These were corrected by reading the provided bitmap. All labels 0 through 9 and the separate class `*` are editable.
2. `job/check_01/validation.json` failed two `Norm` labels: required width 47.25 px, available width 47.00 px. The authoring helper's whole-word PIL advance differs from the runtime's atom-based measure. Each frame was widened by 0.5 px without changing its font size or panel position; `check_02` passed.
3. `check_01` also warned `image_stretched` for all ten images even though every crop and destination had identical width/height. This is a false claim about actual aspect change. Replacing `stretch` with `contain` removed the warnings without changing the visible dimensions.
4. `job/build_01/validation.json` passed preflight, native object/content checks and actual rendered-text checks. Its `visual_review` remained `required`. Visual comparison still revealed narrower horizontal arrowheads, 1–2 px text vertical drift and overly thin `[class]` strokes. Thus automated pass was not treated as fidelity acceptance.
5. A targeted typography repair was prepared in `scene_03.json`; its build to `job/build_02` stopped during preflight because the enlarged title required 239.50 px while its frame was 239.188 px. This failed directory is retained and has no PPTX preview. No render success is claimed for it.

## Quantitative original result

`job/build_01/anchor_measurements.json` contains 23 isolated text regions at two darkness thresholds, 11 stroke anchors, five arrowhead profiles and the exact measurement method. The real PPTX preview is normalized from 1600 × 835 to 930 × 485 with LANCZOS, without registration or shifting. Text bbox right/bottom are exclusive edges. A lower ink edge is only an approximate baseline proxy for strings with no descenders, with about 1 px pixel quantization. Stroke centers use darkness-weighted pixel centers `(index + 0.5)`.

Representative text edge deltas, render minus source `[left, top, right, bottom]` in source pixels:

| Region | Delta |
| --- | --- |
| Vision Transformer (ViT) | `[0, +1, -4, +1]` |
| Main Transformer Encoder | `[-1, +1, -1, +2]` |
| Linear Projection of Flattened Patches | `[+1, +1, -1, +1]` |
| Top Norm | `[0, +1, 0, +2]` |
| Multi-Head | `[0, +1, 0, +2]` |
| Embedded | `[+1, +1, -1, +1]` |

The Courier New `[class]` label is too light: at threshold 100 its isolated ink delta is `[+8, +3, -8, -3]`, while threshold 140 recovers nearly the original geometry. This is a stroke-weight mismatch and demonstrates why a single binary threshold can give a misleading alignment number.

Representative shape stroke-center deltas are main encoder top `+0.005 px`, left `-0.096 px`, bottom `+0.224 px`; projection left `-0.454 px`; right panel left `-0.181 px`, right `-0.715 px`; lower Norm top `+0.521 px`; vertical separator x `-0.083 px`.

Arrow measurements report `[maximum dark vertical span, head-core x span]`, where core columns contain at least three dark pixels. They are measured raster features, not guessed vector dimensions:

| Arrow | Source | Original actual PPTX |
| --- | --- | --- |
| Class output | `[9, 11]` | `[4, 3]` |
| Top residual | `[9, 12]` | `[5, 4]` |
| Bottom residual | `[10, 11]` | `[4, 3]` |
| Embedding annotation | `[9, 12]` | `[5, 3]` |
| Input photo-to-patches | `[9, 11]` | `[5, 4]` |

## Expressiveness and remaining limits

- The original schema cannot size standard connector heads independently of stroke width. Vertical heads were reconstructed as native triangles with thin native line shafts, but the five horizontal standard heads were visibly too small. These should be controlled by explicit source-pixel head geometry.
- The two residual paths and three-way attention branch have source-rounded corners; the schema only permits independent straight segments. Topology and endpoints are preserved, while corner curvature is approximated by square joins. This remains visible in the right-hand detail comparison.
- Source dash geometry requires 17 independent native segments because native dash style was unavailable to the original scene. These are editable but unnecessarily verbose.
- The source font identity cannot be uniquely proved from a bitmap. Times New Roman regular/bold closely matches the proportional text. Courier New is too thin for the monospaced note. No runtime font substitution occurred in build_01. Fonts are not embedded.
- All connectors use fixed coordinates; editing node positions does not reroute them automatically. The figure is not grouped into semantic PowerPoint groups.
- Only LibreOffice was actually tested. No native Microsoft PowerPoint or WPS visual verification is claimed.

## Original evidence paths

- Actual editable PPTX: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/editable.pptx`
- Full actual preview: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/render/page_001.png`
- Comparison: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/render/page_001_comparison.png`
- Dense detail, source left / render right: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/render/detail_right.png`
- Editable SVG: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/svg/page_001.svg`
- Resolved scene: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/scene.resolved.json`
- Fonts: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/fonts.json`
- Validation: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/validation.json`
- Measurements: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01/anchor_measurements.json`
- Failed preflight: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/check_01/validation.json`
- Failed typography repair: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_02/validation.json`
- Authoring and measurement scripts: `/tmp/super-img2ppt-conference-vit-dVqHtY/reconstruct.py`, `/tmp/super-img2ppt-conference-vit-dVqHtY/measure_anchors.py`

## Commands

All commands used the existing environment, with command-local PATH for working fontconfig and LibreOffice:

```sh
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt doctor
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt prepare /Users/liyufeng/Code/super_img2ppt/output/conference_cases_20260906/raw/vit_figure.png --out /tmp/super-img2ppt-conference-vit-dVqHtY/job
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-vit-dVqHtY/reconstruct.py
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt check /tmp/super-img2ppt-conference-vit-dVqHtY/job/scene.json --out /tmp/super-img2ppt-conference-vit-dVqHtY/job/check_01
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt check /tmp/super-img2ppt-conference-vit-dVqHtY/job/scene.json --out /tmp/super-img2ppt-conference-vit-dVqHtY/job/check_02
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/super-img2ppt-conference-vit-dVqHtY/job/scene.json --out /tmp/super-img2ppt-conference-vit-dVqHtY/job/build_01
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-vit-dVqHtY/measure_anchors.py build_01
```

These are historical commands, not commands to rerun into existing directories. Scene snapshots `scene_01.json`, `scene_02.json`, `scene_03.json` preserve successive authoring states; `reconstruct.py` creates the first state, while the resolved baseline scene preserves the successful second state and copied assets.
