# Cosmos 3 Figure 5 — independent forward conversion

Current reviewable baseline: `build_04/editable.pptx`. Complete Figure 5, PDF page 11, arXiv 2606.02800v4 (23 June 2026). Source article and licensing evidence are archived locally. The arXiv paper page links CC BY 4.0; the project's OpenMDW model/code license was not substituted for the paper license. Attribution and modification notice are included in PPTX notes and provenance.json.

## Evidence boundary

Only PDF raster pixels, visual inspection and local Vision OCR informed reconstruction. PDF text/vector coordinates and author drawing code were not read. pypdfium2 rendered page index 10 at scale 3 to 1786×2526; crop [220,250,1620,875] produced the complete 1400×625 figure, excluding its prose caption. This includes five encoders, both token subsequences, independent LayerNorm/MLP paths, shared attention with both complete formulas, recurrence annotation, reasoner/generator outputs, complete 12×12 attention matrix, query/key axes and the seven-category token legend.

No photographs are present. Two independently movable raster crops remain in this baseline: the curved repetition brace (18×279, no text) and the diagonal attention-mask header labels (310×34, contains text). The former exceeds the schema's native path support; the latter uses approximately −45° text rotation, while the tested scene schema initially admitted only quarter-turns. The rest is native: 156 text objects, 198 shapes, and 28 lines (384 total visible objects including the 2 images). This baseline does **not** satisfy fully native readable diagonal labels; a runtime enhancement is being independently evaluated by the parent task.

## Actual verification

Build 04: aggregate **review**, preflight **review**, native object checks **pass**, actual LibreOffice/PDF rendered-text checks **review**. There are no blocking errors. The warnings are the declared raster text strip and `tokensheading` ink width drift (83.5 measured versus 80.715 rendered source pixels). This is LibreOffice evidence, not native PowerPoint/WPS verification. The font is Times New Roman from installed local files; no font files were embedded or redistributed. Source font identity is an approximation inferred from pixels, not proven by the family name.

`actualsourcewidth.png` is rendered directly from the actual exported PDF at scale 1400 / PDF page width. PDFium returned exactly 1400×625; no resize, registration, alignment compensation or crop was applied. `comparison.png` is source above actual, at matching resolution. `measurements.json` records fixed text regions, half-open ink bounds and threshold-mask overlap; figures are not a fidelity score. Full image and source-width formula/detail crops were opened and inspected.

The general geometry, panels, layer ordering and labels survive. Initial shared-attention title width and mask-title horizontal origin were visibly off and were corrected. Mathematical main symbols, normal scripts and lowered subscripts remain independently editable; these are text parts, not an Office equation object. Visible formula spacing and glyph shapes still differ from source even where whole-formula edges agree within 2 pixels. In particular, the source's tightly set Attn/Q/script transitions are less compact in the reconstruction. Token script baselines and dash appearance also remain approximate. Do not infer exact fidelity from native object counts or passing text checks.

## Attempts and findings

- `build_01` (failed preflight): six noisy-token tilde frames were too short / outside their declared containers; one formula semicolon/script collision; matrix divider crossing lacked its specific declared intentional pair. These were genuine authoring failures, not runtime bugs. The failed scene is preserved as `scene_attempt01.json`.
- `build_02` (review): local repairs fixed those blockers. Actual rendering exposed poor formula punctuation placement. The checker also reported broad width drift for tiny formula parts whose large transparent frames included neighbors; this is consistent with its documented conservative attribution fallback, not yet a proven bug.
- `build_03` (review): formula parts were remeasured from source pixels; all formula drift warnings disappeared. Residual source glyph/spacing differences remain. The complete before snapshot is retained.
- `build_04` (review): isolated heading calibration, LayerNorm size calibration and omitted noisy-row tilde repair. No repeated font minimum reductions or weakened validation checks were used.

An ancillary measurement script initially imported unavailable NumPy; that attempt failed immediately, and the script was rewritten using installed Pillow. No dependencies were installed. This was an evaluation-script issue, not the conversion runtime.

## Reproduction

Existing environment: `/Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt` 0.3.4; command-local `PATH=/opt/homebrew/bin:$PATH`; existing font directories `/System/Library/Fonts/Supplemental` and `/Applications/LibreOffice.app/Contents/Resources/fonts/truetype`. Use the sibling resolved scene/assets and build into a new directory. `reconstruct.py`, sequential `repair02.py`/`repair03.py`/`repair04.py`, and `measure.py` preserve source-based authoring and measurement. They are job-local scripts with the original temp path; edit that root if relocating the archive. Failed attempts and their logs remain present.

Final baseline measurements after isolated title repair: shared attention title edge deltas [−2,0,−1,0] source pixels with threshold-mask IoU 0.550; attention-mask title [1,1,0,0], IoU 0.434. The left and right formula masks remain substantially different despite close outer edges; their low IoUs are retained in measurements.json rather than hidden by image registration.

Date provenance: arXiv records v4 on 23 June 2026 at 17:33:32 UTC; the PDF cover itself prints 2026-6-24, verified from raster and archived in cover_date.png. Both are recorded without silently treating them as identical.
