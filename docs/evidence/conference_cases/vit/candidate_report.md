# ViT candidate working-tree retest

This report is separate from the unchanged original evaluation at `/tmp/super-img2ppt-conference-vit-dVqHtY/report_original.md`. It evaluates the parent's candidate runtime changes, not a released or frozen package version. The evaluator changed only files under `/tmp/super-img2ppt-conference-vit-dVqHtY`; no repository code, dependency installation, commit or push was performed.

## Result

The final candidate is `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/editable.pptx`. Actual LibreOffice rendering passed preflight, native object/content checks and rendered-text checks, with no runtime or renderer font substitution. The whole actual preview and enlarged right-panel, note, token and arrow comparisons were opened and inspected. Automated status is `pass`; source fidelity is still a visually reviewed approximation with the explicit limitations below. Native Microsoft PowerPoint/WPS has not been tested.

The final slide contains 147 native objects: 35 editable text boxes, 47 auto-shapes, 50 native lines, five editable native freeforms for measured horizontal arrows, and ten raster photo assets. The photos are the same exact text-free source crops used in the original reconstruction. There is no visible full-image background or rasterized text. `artifact_audit.json` verifies the actual PPTX shape types and names, including all five freeform arrows.

## Controlled arrow comparison

The original scenes used standard `arrow: true`; the candidate uses `arrow_head: {length, width}` in source pixels. No image pixels or custom raster heads were introduced. Horizontal head geometry is editable in the actual PPTX.

The five source/actual-PPTX profiles below use the same isolated regions and thresholds as the original evaluation. Each pair is `[maximum dark vertical span, horizontal span of head-core columns with at least 3 dark pixels]`. These are observed raster spans with about 1 px edge quantization. They are not a claim that the unknown source vector dimensions are uniquely recoverable.

| Arrow | Source raster | Original actual PPTX | Final candidate actual PPTX | Candidate nominal length × width |
| --- | --- | --- | --- | --- |
| Class output | `[9, 11]` | `[4, 3]` | `[10, 9]` | `14.5 × 10 px` |
| Top residual | `[9, 12]` | `[5, 4]` | `[9, 12]` | `15 × 10 px` |
| Bottom residual | `[10, 11]` | `[4, 3]` | `[10, 11]` | `15 × 10 px` |
| Embedding annotation | `[9, 12]` | `[5, 3]` | `[9, 11]` | `14.5 × 10 px` |
| Photo-to-patches | `[9, 11]` | `[5, 4]` | `[9, 12]` | `14.5 × 10 px` |

The two residual heads now match the selected source raster spans exactly. The class-output head still differs by +1 px in maximum vertical span and -2 px in dark core length; the two gray annotation heads differ by 1 px in core length. The original standard heads were only about half the source width and 3–4 px long in their dark cores. The candidate fixes the material head-size mismatch without thickening shafts. All arrow directions and endpoints were visually checked. No further head-size tuning was attempted after the bounded original/candidate-1/candidate-2 sequence.

## Text and shape alignment

Typography corrections moved the measured text frames upward by 0.9 px, enlarged the shared title size from 21 to 21.4 source pixels, and expanded transparent frames to retain the measured 0.5 px reserve. Body size remains 19.75 source pixels. These are measured source-alignment repairs; nodes were not rearranged.

Representative final deltas `[left, top, right, bottom]`, actual render minus source:

| Text | Original | Final candidate |
| --- | --- | --- |
| Vision Transformer (ViT) | `[0, +1, -4, +1]` | `[0, 0, +1, +1]` |
| Right Transformer Encoder title | `[+1, +1, -3, 0]` | `[0, 0, 0, 0]` |
| Main Transformer Encoder | `[-1, +1, -1, +2]` | `[0, 0, 0, +1]` |
| Linear Projection… | `[+1, +1, -1, +1]` | `[+1, 0, -1, 0]` |
| Top Norm | `[0, +1, 0, +2]` | `[0, 0, 0, 0]` |
| Multi-Head | `[0, +1, 0, +2]` | `[0, 0, 0, +1]` |
| Embedded | `[+1, +1, -1, +1]` | `[+1, 0, -1, 0]` |

The eleven measured shape/stroke anchors remain within 0.715 px of the source. Representative final errors are main encoder top +0.005 px, left -0.096 px and bottom +0.224 px; projection left -0.454 px; right panel right -0.715 px; lower Norm top +0.521 px. These use darkness-weighted stroke centers at pixel centers, rather than mixing line centers with integer bitmap row indices.

The numbered-token zero region in the generic measurement JSON is narrow and may include capsule-edge ink. It is not used to claim isolated text or baseline precision. The representative table above uses clear isolated text regions. Text bottom edges are baseline proxies only for strings without descenders; the original source baseline itself is not directly available from a bitmap.

## Native dash result

The original separator required 17 independent solid line segments. The candidate uses one native custom-dash line for the regular middle pattern plus two short endpoint segments. The middle dash uses `[13.4, 13.4]` source pixels, with source-measured starting phase at y = 52.2. This reduces the separator from 17 to three objects.

`job/build_candidate_02/dash_measurements.json` records every visible dash interval. The original manual pattern drifted by as much as 3 px near the bottom. All 17 final start/end pairs are within 1 px of the source; 13 of the 17 full pairs match exactly at the measured threshold. The separator x stroke-center error is -0.083 px. No page-wide similarity score was used as an acceptance condition.

## Actual failed candidate and font resolution

`job/build_candidate_01/validation.json` has an actual rendered-text `fail`: the locally measured macOS `Courier` font was replaced by LibreOffice's `LiberationMono`. This was detected even though the editable text content was present. The failed candidate, its real preview and measurements remain available.

The final scene explicitly requests `Liberation Mono` for `[class]`, and the build supplies the already installed directory `/Applications/LibreOffice.app/Contents/Resources/fonts/truetype` using `--font-dir`. Nothing was installed or copied into a host registry. The final manifest resolves and the actual PDF uses the same Liberation Mono face. The font substitution list is empty because the intended candidate font is now explicit; this is still a disclosed approximation to the unidentified source font. The proportional text uses Times New Roman regular/bold. Fonts are not embedded or distributed with the deck.

The original Courier New note was too thin. The final note's isolated ink edges differ from the source by `[-1, +1, 0, +1]` at threshold 100. Three actual note render states were evaluated: Courier New, substituted Courier, and explicit Liberation Mono. The font region is not subject to further open-ended retries.

## Remaining limitations

- The residual paths and attention fan-out still use square segment joins; the source uses small rounded corners. The current schema still lacks rounded polyline/freeform authoring. The residual topology, arrow direction and endpoints are preserved. This is the main visible structural approximation in the right-panel close-up.
- A few title/body ink edges differ by 1 px, and some small token edges by up to 2 px. Source font identity and anti-aliasing cannot be recovered exactly from the raster.
- The class-output arrow dark core still differs by 2 px as quantified above. This was retained after the bounded repair sequence.
- The ten photo assets are individually movable but their internal pixels are raster. The input patch grid is one photo crop.
- Diagram nodes and connectors are independent native objects, not semantic groups with automatic connector rerouting.
- The final deck requires Times New Roman and Liberation Mono on another editing computer. Only LibreOffice rendering is verified.

## Final evidence paths

- PPTX: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/editable.pptx`
- Actual preview: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/render/page_001.png`
- Source/actual comparison: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/render/page_001_comparison.png`
- Right-panel detail: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/render/detail_right.png`
- Small-text detail: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/render/detail_notes.png`
- SVG: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/svg/page_001.svg`
- Resolved scene: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/scene.resolved.json`
- Fonts: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/fonts.json`
- Validation: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/validation.json`
- Anchor measurements: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/anchor_measurements.json`
- Dash measurements: `/tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02/dash_measurements.json`
- Actual PPTX object audit: `/tmp/super-img2ppt-conference-vit-dVqHtY/artifact_audit.json`
- Candidate scene snapshot: `/tmp/super-img2ppt-conference-vit-dVqHtY/scene_candidate_02.json`
- Final-build runtime hashes before and after: `/tmp/super-img2ppt-conference-vit-dVqHtY/candidate_runtime_hashes_final.json`, `/tmp/super-img2ppt-conference-vit-dVqHtY/candidate_runtime_hashes_after.json`

The eight recorded runtime/schema/skill files were unchanged between the before/after hashes for the final build. The parent had already modified the shared working tree before this candidate run; the original and candidate are therefore explicitly distinguished.

## Final commands

```sh
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/super-img2ppt-conference-vit-dVqHtY/job/scene.json --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype --out /tmp/super-img2ppt-conference-vit-dVqHtY/job/build_candidate_02
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-vit-dVqHtY/measure_anchors.py build_candidate_02
```

The resolved scene and sibling `assets/` are the reproducible final input. Rebuild into a fresh output directory and supply the same existing font directory or an equivalent local installation of the listed font files.
