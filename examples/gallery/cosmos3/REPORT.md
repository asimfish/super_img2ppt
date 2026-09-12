# Cosmos 3 Figure 5 — final forward-test report

Final deliverable: `build_06/editable.pptx`, with sibling `svg/page_001.svg`, `scene.resolved.json`, `assets/`, `fonts.json`, and `validation.json`. This is the complete architecture Figure 5 on PDF page 11, including both towers, all token categories, both shared-attention formulas, full attention matrix and legend. All readable labels are now native editable text. Only the text-free curved recurrence brace remains a raster asset.

## Provenance and evidence boundary

NVIDIA et al., *Cosmos 3: Omnimodal World Models for Physical AI*, arXiv 2606.02800v4. arXiv records this version on 23 June 2026 at 17:33:32 UTC; the PDF cover prints 2026-6-24, independently verified and archived as `cover_date.png`. The PDF, arXiv metadata HTML and CC BY 4.0 paper-license page are archived. The paper's CC BY license is distinguished from the project's OpenMDW code/model license. Attribution and the modification notice are present in provenance.json and PPTX notes. The reconstructed figure is an adaptation, with no endorsement implied.

Only raster pixels, local Vision OCR and visual inspection informed the reconstruction. PDF text/vector coordinates and author drawing code were not read. pypdfium2 rendered PDF page index 10 at scale 3 to 1786×2526 pixels, then the exact crop [220,250,1620,875] produced `source.png` at 1400×625. The prose caption is outside the crop; every figure panel and legend is included. PDF/source SHA-256 values, URLs and asset crops are recorded in provenance.json.

## Native diagonal conversion, before and after

`build_04/` is the preserved before version. Its full actual render and comparison are `before_actualsourcewidth.png` and `before_comparison.png`. `scene_before_diagonal.json` preserves its scene. The old `diagonal_mask_labels` raster strip was removed in full. The new runtime's `compose-math` common-origin rotation produced 32 native −45° text parts across all 12 attention-mask header labels, including ordinary lower/upper scripts and noisy-token tildes.

The exact scene diff (`before_after_scenediff.json`) proves: one image removed; 32 native text objects added; no previously existing element changed; attribution notes updated. Visible objects changed from 384 to 415: 198 shapes, 28 lines, 188 text objects, one text-free image. The final build assets contain the brace and the source reference image; the source reference is not a visible slide object. No baked diagonal text is underneath the new labels.

The initial font-strict composition rejected U+22EF because the requested Times New Roman face lacks that glyph. That failure remains in `diagonal_01/` and its logs. The visible three-dot sequences were instead composed from three ordinary period glyphs at explicit 8-pixel source-coordinate intervals, then rotated together. This preserves their visible content and editability; it does not claim the source used those exact Unicode characters. Font files were neither installed, embedded nor redistributed.

## Actual verification and remaining limitations

Build 06 status is **review**: preflight **pass**, native objects **pass**, rendered text **review**, no blocking errors. Exactly 32 `diagonal_glyph_bounds_require_visual_review` warnings are expected, one per diagonal text part. PDFium's page-axis glyph rectangles do not establish exact containment against slanted frame edges; this boundary is retained explicitly. The remaining non-diagonal warning is `tokensheading` measured-versus-rendered ink width drift (83.5 versus 80.715 source pixels). No checks or font minima were relaxed.

`actualsourcewidth.png` and `comparison.png` now contain final build 06. The actual PDF was rendered directly at scale 1400 / PDF page width; PDFium returned 1400×625 without resizing, registration or positional compensation. The full actual image and enlarged header were opened and inspected. `build_05_inspection/` and `build_06_inspection/` preserve complete actual/source comparisons, dense label crops and same-coordinate measurements. Detail images are enlarged 5× only for display; measurements use original source pixels.

The shared-origin helper preserved the source relationships between the main letter and its scripts. No native diagonal-runtime blocker or new reproducible implementation bug was found in this figure. However, source typography is still an approximation: Times New Roman's italic v/a/s shapes differ from the source, EOS/BOG glyphs and diagonal tildes differ, and some script spacing/baselines remain visibly different. The previously documented shared-attention formula spacing differences also remain. Native editability, exact text, close outer edges and pixel-perfect glyph fidelity are separate claims. This is LibreOffice actual-PPTX evidence, not native PowerPoint/WPS verification.

Measurements use unchanged source-pixel ROIs and min-RGB <150 binary masks, with no threshold tuning. The broad header ROI includes its lower matrix border and the EOS ROI catches a neighboring edge, so those aggregate masks are descriptive and must not be presented as isolated glyph scores. Individual token crops show the remaining differences directly. Earlier body measurements are preserved in `before_measurements.json`; final diagonal measurements are in `build_06_inspection/measurements.json`.

## Bounded attempts

The earlier body work and failed attempts are documented in `REPORT_before_diagonal.md`, with build 01–04 artifacts intact. Build 01's tilde-frame, real formula collision and undeclared matrix-divider crossing were authoring faults that were repaired, not runtime defects. Three formula candidates were inspected; remaining source typography differences were retained rather than obscured by endless fitting.

For this diagonal extension: the first compose attempt stopped on the missing glyph; build 05 passed blockers and exposed tight dot spacing, roughly 3-pixel offsets on l/EOS/BOG and a low DM superscript. Build 06 applies one source-driven targeted repair, with all expectations and review warnings unchanged. Both actual candidates are retained. The old raster before image is not presented as the final answer.

## Reproduction

Run `rebuild.sh` to rebuild the final resolved scene into a new `rebuilt_fresh` directory using the existing repository environment and installed fonts. The command uses a local PATH including `/opt/homebrew/bin` and font directories `/System/Library/Fonts/Supplemental` and `/Applications/LibreOffice.app/Contents/Resources/fonts/truetype`. This script does not install anything.

Source authoring scripts, sequential body repairs, the diagonal common-origin specifications and per-formula measured outputs are preserved. `diagonal_reconstruct_attempt01.py`, `diagonal_reconstruct_attempt02.py`, `diagonal_reconstruct.py`, and `diagonal_01/`–`diagonal_03/` retain all extension attempts. `diagonal_measure.py build_NAME` creates a new inspection directory, so stale output cannot hide a failure. Job-local authoring scripts contain their original temp root; update that root if moving the archive, or rebuild directly from the resolved scene and sibling assets.

Resolved-scene reproduction was actually executed using rebuild.sh: `rebuilt_fresh/validation.json` again reports review, with preflight/native pass and rendered review, no blockers. The rebuilt artifact and log are retained.
