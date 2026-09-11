# BEVFormer full Figure 2 — independent image-only evaluation

**Result: reviewable editable draft; fails high-fidelity visual acceptance.** All panels (a), (b), (c) of the published main architecture are reconstructed. Final candidate: `build_07/editable.pptx`; editable SVG, resolved scene, assets, fonts, actual PPTX PDF and preview are in the same directory.

## Source and frozen contract

BEVFormer: Learning Bird’s-Eye-View Representation from Multi-Camera Images via Spatiotemporal Transformers, ECCV 2022. Official ECVA PDF `https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136690001.pdf`. Page 5, Figure 2, all panels. Rasterized at scale4; complete figure crop `[530,450,1930,985]`, 1400×535. Exact hashes and2,019,301-byte download in `source_provenance.json`. No PDF text/vector objects, paper drawing code, upstream implementation or reconstruction answer read. Whole pages were visually viewed to select Figure2. Source PDF/image/derived deck is **local-only** because no redistribution grant was established.

`roi_contract.json` fixed36 source ROIs before scene authoring; 24 development and12 heldout numeric-feedback ROIs (every third item). All source regions were visible during authoring: this is **within-figure numeric-feedback holdout, not independent generalization**. Primary fixed criterion: maximum ink bounding-box edge error≤4px AND mask IoU≥0.70; mask is maxRGB<170 OR chroma>45 with minRGB<170. Actual exported PPTX PDF rasterized directly to1400px width, no image registration. `candidate_freeze.json` seals scene/PPTX/PDF/render hashes before any heldout measurement. No edits occurred after that freeze.

## Measured outcomes and metric blind spot

Initial rendered `build_02`: development3/24. First font trial `build_03`:2/24. Second-family-sizing candidate `build_05`:2/24. Final `build_07`: development2/24 and heldout2/12, combined4/36. These counts do not mean the rest are missing: font glyph IoU remains poor even where most bounding-box edges are within1–4px. All complete primary rows and failures are retained.

The heldout `temporal` ROI scored1.0 because the gold background meets the chromatic mask across the entire region. **This is a known invalid glyph-fidelity success, not perfect text.** The coarse fixed result is preserved rather than replacing its threshold after seeing the outcome. `supplemental_dark_text.json` was calculated only after final freeze to expose this blind spot; temporal dark-text IoU=0.1868. This diagnostic did not guide corrections and is not substituted for the original contract. Other light feature planes mainly test dark borders under this threshold, making thin-stroke antialias differences dominate their IoU. Thus do not compare these aggregate scores directly to another figure with different backgrounds.

## Actual artifacts and editability

{'shape': 145, 'text': 23, 'line': 49, 'image': 7} = 224 objects, of which 217 native and7 independent raster camera/car crops. All23 readable label elements are native; no fused label raster crops or full-source backdrop. Mathematical variables use native italic Times New Roman runs, Unicode subscripts may fall back to DejaVu Sans. Body font is installed Carlito (source looks Calibri-like but identity cannot be proved), and font files are not embedded. Actual `fonts.json` records Carlito-Regular, Times New Roman Italic, DejaVu Sans regular/oblique and substitutions. Another editing machine requires these fonts.

All6 module boxes, residual branches, task head, backbone stages, feature planes, BEV volumes/grid faces, query points, projected rays and red direction markers are native. Main camera input uses7 exact crops. The3D grids are approximated by native convex faces with fewer grid subdivisions than source; curved braces/routes/correspondences use a few straight segments, and the sampling pillar lacks the source’s full wireframe3D perspective. Task-head folded corner is rectangular. These are visible geometric simplifications, not unsupported content silently passed as exact. No subplot was omitted.

Whole-figure topology checked against source: multi-view input→backbone→multi-camera features feeds spatial attention; history BEV and BEV queries feed temporal attention; Add&Norm/feed-forward/spatial/temporal sequence and three residual branches remain; current BEV feeds detection/segmentation heads; ×6 and both zoom panels remain; spatial hit-view sampling and temporal history→current query directions are retained, including four red direction cues. Source anti-aliased curved geometry and exact sampling-point/grid positions remain approximate.

## Failures and bounded repairs

- build01 fail:27 missing named source-visible geometry intersections; no render. build02 declares only source-verified joins/point-on-plane intersections and renders review.
- build03 typography correction1:Arial→Carlito; math coordinates italic; green Hit Views and blue volume side-face colors restored. Development widths showed Carlito too small.
- build04 typography correction2:family sizing from development bounds; failed rotated Backbone frame height/placement. build05 corrected that frame without changing font.
- build06 typography correction3:final development origin corrections, family-consistent caption/module shifts, coordinate sizing, four source direction markers. Failed coordinate frame reserve: measured29.0px in29px frame needs29.5.
- build07 only expands coordinate frame height29→30. No tolerance or blanket text-overlap exemptions introduced. Final preflight/native-object/rendered-text checks allpass; overallreview due recorded font substitutions. All previous failed validation reports and scene inputs are retained.

Three meaningful typography corrections maximum; all changes in repair02–07 JSON. First source snapshot, initial failures and original scene are preserved. No causal runtime bug established; observed issues came from scene reconstruction or unsupported font/curve fidelity. Existing runtime implementation unchanged. No dependencies installed. Native PowerPoint/WPS not tested.

Commands: `commands.json`; environment: `environment.json`; frozen skill manifest: `frozen_skill_hashes.json`; final candidate seal: `candidate_freeze.json`; complete artifact digests: `artifact_hashes.json`.
