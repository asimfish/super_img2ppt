# DreamZero Figure 4 — independent forward test

Delivered reconstruction: `job/build_05/editable.pptx`, `job/build_05/svg/`, `job/build_05/scene.resolved.json`, sibling assets and fonts/validation manifests. `source.png`, `actual_source_width.png`, `source_comparison.png` and `detail_*.png` are the inspected evidence. Status: **review**, all three automated gates pass. This is usable editable architecture content with visible typography differences; not a claim of pixel-exact reproduction or PowerPoint/WPS verification.

## Source and coverage

Seonghyeon Ye et al., *World Action Models are Zero-shot Policies*, arXiv:2602.15922v1, submitted 17 February 2026, current official version verified 12 September 2026. Official paper PDF, page 6, complete Figure 4 above caption: Training: Joint Video-Action Flow Matching and Inference: Closed-Loop Real World Execution. PDFium rasterization at 4×, crop left/top/right/bottom [248,332,2136,964], yielding 1888×632. Hash and attribution in provenance.json. Archived arxiv.html links this paper to CC BY 4.0; license.html archives its share/adapt/attribution terms. This is paper-license evidence, not repository code-license evidence.

All panels, headings, language prompts, encoder/decoder labels, Causal DiT blocks, KV Cache, feedback branches, merge and execution labels are present. Native representation: 37 text objects, 72 shapes, 20 lines; 15 independently movable raster assets. No readable label is deliberately rasterized. No mathematical formula occurs inside this figure; noise-injection plus symbols are native circles and crossing lines, and ellipsis uses native text. Italic prompts and bold panel headers remain styled text.

Raster boundary: 3 video/photo regions, 1 real-world execution photo, 2 action-trajectory plots, 4 noise tiles, 3 robot icons, gold curved merge, dotted autoregressive loop. The two curved-connector crops include narrow adjacent silhouette/margin pixels and source arrow-tip pixels; they are not fully native connector paths. Their explicit named overlaps retain source relationships. The action trajectories are illustrative artwork with no numeric scales and are retained as artwork, not invented data. These 15 local assets are documented with exact boxes. Source screenshot is never a visible whole-slide object.

## Validation and actual quality

Actual editable PPTX was converted by LibreOffice to PDF. PDFium rendered that PDF at exactly source width 1888 using scale = 1888 / actual PDF page width, with no registration. measure.py records the PDF point dimensions, scale, raw and final sizes in measurements.json. The script removes a possible extra 633rd row only if it is entirely white; it never vertically resizes to hide error. The source was only inspected as pixels and local macOS Vision OCR; no original-PDF text/vector coordinate extraction or author drawing code was used.

Full actual image and enlarged encoder, prompt and Causal DiT details were inspected. Arial is a disclosed approximation to the unknown source face; its actual rendering is heavier, especially in the italic prompt. Vertical ellipsis falls back to DejaVu Sans, recorded in fonts.json. Fonts are not embedded or redistributed. The source/actual glyph differences remain visible even when bounding edges match.

Frozen dark-ink mask: all RGB channels < 145 within the same six source-coordinate ROIs, no image alignment. Final edge deltas [left,top,right,bottom] and ink IoU:

| ROI | Edge deltas, source px | IoU |
|---|---|---:|
| Training heading | [-2,0,-9,1] | 0.425 |
| VAE Encoder | [0,1,-1,1] | 0.490 |
| Causal DiT / Blocks | [-1,0,0,-1] | 0.475 |
| KV Cache | [-1,-1,0,0] | 0.375 |
| Italic prompt | [5,0,-2,0] | 0.202 |
| Feedback label | [0,1,-10,0] | 0.337 |

The Causal DiT region improved from +11 px left/+12 px right displacement to [-1,0,0,-1] after one explicit origin repair. Prompt baseline and bottom ink match, but glyph weight/shape and first-line left edge differ. Training and feedback headings are about 9–10 px shorter at their right edge. State-encoder front/rear stacking is preserved with simplified flat fills; source texture/shadows are not reproduced. Dashed outlines and tiny play-glyph geometry differ slightly. The screenshot curve art is resampled by the office renderer. These are visual limitations, not dismissed by automated pass.

## Attempts and feedback

build_01: authoring schema failure from dash:null (schema requires omitted optional array). build_02: preflight stopped narrow U+22EE frame and undeclared source joins/overlays. build_03: named source relationships and actual text frames corrected; all gates passed, visual inspection exposed left-aligned multiline labels and wrong foreground encoder slant. build_04: centered labels and corrected slant; source-width measurement exposed the Causal DiT origin error. build_05: targeted origin correction; final review status. All directories retained; each attempt is fresh. No same region received more than three repair attempts, and no check thresholds were relaxed.

No independently established runtime correctness bug. Concrete limitations for the system: (1) source-font fidelity remains an agent selection/measurement task, (2) schema has no editable curved open path for the gold merge and sampling arc, (3) opaque text-free crop margins require explicit collision/layer reasoning, and (4) passing rendered-text checks does not establish matching glyph appearance. Minimal reproduction for limitation (1): inspect detail_encoder.png and detail_prompt.png, then rebuild the final resolved scene and rerun measure.py. Limitation (2): inspect the two image elements joint_merge_curve and autoregressive_loop in the resolved scene against source.png; editable lines cannot encode their curved path in scene v1. No repository edits, installs, pushes or subagents were used.

Two environment probes failed because fitz and numpy were absent; PDFium and Pillow supplied the existing-environment alternatives. Those are environment availability findings, not product bugs. The full-PDF prepare probe is retained separately and was not used as a text/vector reconstruction answer.

## Reproduction

Run `repro.sh NEW_OUTPUT_DIRECTORY` on this host (existing repository venv, command-local Homebrew PATH, system/LibreOffice font directories). It builds the final original scene into a fresh output. `author.py`, `repair.py`, `visual_repair.py`, and `final_origin_repair.py` preserve scene authoring/repair logic. `measure.py` reproduces final actual source-width rasters and fixed ROI measurements. For portability, copy the final build folder with its resolved scene and assets and supply the listed fonts on the editing machine. Keep provenance.json and this attribution with redistribution.
