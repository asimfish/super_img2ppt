# Candidate 0.3 forward retest: native heatmap gradient

Created 2026-09-07T08:40:31.101578+00:00. Final candidate is `candidate_build_02`. Original `report_original.md`, `build_01`, scene, fixed ROI plan, and original measurements remain unchanged; every hash in `original_evidence_seal.json` was verified after this retest.

**Outcome: native linear-gradient capability passed this source-specific retest.** One editable PPTX/SVG gradient replaces 358 adjacent colorbar bands and removes the observed dark seam pattern. Final actual PPTX rendering meets all 72 fixed edge-ROI tolerances, including all 49 matrix values. The overall result remains `review`: the seven top labels are still an isolated raster crop because approximately 30° native text rotation is unsupported. This is a partial-native deliverable, not a claim that all labels are editable or that every source pixel is reproduced.

## Source, runtime and isolation

- Sole source remains `/Users/liyufeng/Code/super_img2ppt/output/diverse_cases_20260906/raw/heatmap_source.png`, 640×480, SHA256 `7d07f73d16e3dafb7f74fbbac2b8aa2739e29e39e5e430bf918d811606baacd8`.
- Candidate root: `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v030-candidate-k50on3nk/super-img2ppt`. Read candidate `SKILL.md` and `references/scene.md`. No runtime source contents, tests, other cases, plotting data, or web content were read. Candidate files were hashed opaquely.
- Candidate file-manifest SHA256: `40905c041019e6eabaa7da381ac99cb4087e640a7815782ef9e36d8100617c0f`; every file hash still matches at the end. Per-file hashes and original sample coordinates are in `candidate_provenance.json`.
- Python 3.12.12, `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python`; `doctor` reports super-img2ppt **0.3.0**. python-pptx 1.0.2, Pillow 12.3.0, fonttools 4.64.0, pypdfium2 5.13.0, jsonschema 4.26.0. Same existing LibreOffice 26.2.4.2 as baseline. Command-local `PATH=/opt/homebrew/bin:$PATH` and `PYTHONPATH=CANDIDATE/src` are recorded in every logged invocation.
- No dependencies installed; no repository/skill source edits or commits. All intentional authoring/measurement changes are under this temporary root. Separate candidate directories avoid overwriting baseline results.
- Native font stays DejaVu Sans regular, no substitutions, runtime file hash `7da195a74c55bef988d0d48f9508bd5d849425c1770dba5d7bfc6ce9ed848954`. No font-size shrink or change was used. Font identity from the bitmap remains an inference, and fonts are not embedded.

## Candidates and bounded repair

Candidate 01 changed only the continuous colorbar representation (and explanatory notes): 358 adjacent solid bands became one `shape: rect` with `gradient.direction: vertical` and 16 source-sampled stops. Direction is top-to-bottom: dark green to pale yellow. Shape box `[543,98,17,358]`, outline, numeric data, text geometry, and raster top labels were otherwise unchanged. `candidate_build_01` is preserved.

Its first/last sampled colors used y98/y455. Inspection of the sole source revealed those rows include black-outline antialiasing. That authoring choice slightly darkened the bottom gradient endpoint. The remaining original label drift was also unchanged. Candidate 02 applied **one evidence-based local repair**:

- Gradient endpoint colors resampled from clean interior points `[550,99]` and `[550,454]`: `#004629` and `#FFFFE4`. The other 14 sampled stops and all source-derived numerical values remain fixed.
- The seven same-level row labels moved left 1 source px; their font family/size and relative layout remain fixed. Original left edges drifted +1 to +3 px.
- The native 90° colorbar title moved right 2.5 source px; original left/right edge drift was −2/−3 px.

`candidate_repair_01.json` records exact old/new values and supporting evidence. No further repair was needed; each repaired region used one of the permitted three local corrections. No overlap exemption was added to make the gradient pass.

## Automated and actual-render evidence

| Invocation | Exit | Wall seconds |
|---|---:|---:|
| `doctor` | 0 | 5.237 |
| `check candidate_job/scene.json --out candidate_check_01 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` | 0 | 13.469 |
| `build candidate_job/scene.json --out candidate_build_01 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` | 0 | 18.027 |
| `check candidate_job/scene.json --out candidate_check_02 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` | 0 | 5.770 |
| `build candidate_job/scene.json --out candidate_build_02 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` | 0 | 15.248 |

All candidate check/build directories are new and preserved. Neither candidate check/build returned a blocking failure; all returned `review` with exit 0. Final `candidate_build_02/validation.json` reports:

- Preflight: `review`, solely the explicit `raster_text` warning for top coordinate labels.
- Native objects: `pass`.
- Actual rendered text: `pass`; all 64 native text elements are accounted for in the actual LibreOffice PDF.
- Overall: `review`, with `visual_review: required`. That automated flag is not relabeled as a machine fidelity approval.

Opened the actual `candidate_build_01/render/page_001.png` and final `candidate_build_02/render/page_001.png` at 1600×1200. Opened the final source-versus-actual colorbar and dense-matrix crops. No missing matrix values, lost signs/unit suffixes, unintended overlaps, or reversed gradient direction were observed in these inspected regions. The candidate seam pattern is visibly removed. PowerPoint/WPS were not opened; this is actual LibreOffice evidence only.

Own generated PPTX XML contains a single native `a:gradFill`, 16 `a:gs` stops, and `a:lin ang="5400000"` (vertical). SVG contains one `linearGradient`. Both contain 64 native text elements. PPTX contains only one picture/media item: the acknowledged top-label crop. The colorbar is not rasterized. XML evidence is retained in `measurements_candidate_build_02/native_gradient_shape.xml`; full stop data are in the supplemental measurement JSON.

Final scene objects: 137 = 64 text + 51 shapes + 21 lines + 1 image. Shapes comprise 49 heatmap cells, one native colorbar gradient, and its backing/outline. Compared with the baseline, this removes 357 objects. The source matrix remains editable shapes and text rather than an Excel-linked chart.

## Fixed ROI and gradient results

The original 72-ROI plan and tolerance definitions were unchanged: SHA256 `beda47e44850c08a708b839d14fb99e19fcb71e409cbc22c60e8559b1b3e78cf`. The same ROI measurement script was used in all three runs, SHA256 `1433be05c53b1b78ce4673154d8fa6426fe252f8907f512a65d68f72cc9229ab`. Text edge tolerance is ≤2 source px; grid tolerance ≤1 source px. Source pixels are compared with the actual PPTX render downsampled to 640×480 by LANCZOS. Pixel-cell edges and grid centers retain the original definitions; bottom ink edge is a baseline proxy. These comparisons do not establish pixel-perfect text shapes.

The colorbar interior ROI and residual method were selected after baseline seam discovery and then held fixed through both candidate runs. They are labeled supplemental, separate from the precommitted 72 ROIs.

| Run | Fixed ROIs within tolerance | Native text within tolerance | Interior RGB MAE / 255 | Dark residual runs at 1600×1200 |
|---|---:|---:|---:|---:|
| Frozen 0.2 first build | 70/72 | 62/64 | 9.341 | 203 |
| Candidate 0.3 first build | 70/72 | 62/64 | 1.058 | 1 |
| Candidate 0.3 final build | 72/72 | 64/64 | 0.665 | 0 |

Final details:

- Matrix values: **49/49**, maximum edge deviation 2 px; all six measured internal grid gaps: **6/6**, maximum deviation 1 px. Matrix numeric ROIs are exactly unchanged from baseline.
- All native text: **64/64** within fixed tolerance; all selected regions: **72/72**. Mean native text-mask IoU is 0.5437, so edge acceptance is not claimed to imply pixel-identical glyphs.
- Previously failing `cucumber` edge deltas are now `[2, 0, 0, 1]` px; colorbar-title deltas `[0, 0, -1, -1]` px, in `[left,top,right,bottom]` order.
- Gradient interior RGB MAE: **0.665/255**, compared with baseline 9.341/255. Mean luminance darkening: 0.039/255. All **354/354** sampled source rows stay below 10/255 darkening; no high-resolution residual run exceeds 12/255. These residual thresholds are diagnostic methods fixed after the baseline seam discovery, not a universal visual quality gate.
- Sixteen source-sampled stops approximate the bitmap color map. Small residual RGB differences remain; no missing chart data were inferred or fabricated.

Full signed edges, bboxes, grid centers/widths, bottom-ink proxies, masks, IoU, and failures (none in final fixed ROIs) are in `measurements_candidate_build_02/measurements.json`. Full colorbar row profiles, residuals, and native-gradient XML facts are in `measurements_candidate_build_02/colorbar_supplemental.json`.

## Remaining boundary and delivery paths

Seven approximately 30° top labels (`Farmer Joe`, `Upland Bros.`, `Smith Gardening`, `Agrifun`, `Organiculture`, `BioGoods Ltd.`, `Cornylee Corp.`) remain the original independent raster crop `[100,10,497,91]`. It remains movable, and the text is transcribed in notes, but the label glyphs themselves are noneditable. Quarter-turn legend text is native. No full-page screenshot or editable duplicate-text overlay is used.

- Final PPTX: `candidate_build_02/editable.pptx`.
- Editable SVG: `candidate_build_02/svg/page_001.svg`.
- Resolved scene and its assets: `candidate_build_02/scene.resolved.json`, `candidate_build_02/assets/`.
- Fonts and validation: `candidate_build_02/fonts.json`, `candidate_build_02/validation.json`.
- Representative actual preview: `candidate_build_02/render/page_001.png`.
- Dense and colorbar comparisons: `measurements_candidate_build_02/dense_matrix_source_vs_actual_2x.png`, `measurements_candidate_build_02/colorbar_source_vs_actual_2x.png`.
- Original baseline report remains `report_original.md`, hash `c1c5581e496ebb875f0ad981c6ffd2089bef7262658f6c73418d1fadc5202a55`.
- Commands/timings/stdout/stderr: `candidate_commands.jsonl`; exact authoring and measurement scripts are retained. Supplemental access audit: `candidate_command_access_audit.md`.
- Provenance/end-state hash checks: `candidate_provenance.json`, `candidate_final_verification.json`, and final `candidate_evidence_seal.json`.

The native-gradient feature meets this bounded source-specific test. Complete native label editability remains unmet, and the deliverable must retain its `review` characterization.
