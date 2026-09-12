# DexVLA Figure 2: complete forward reconstruction

Final deliverable: `build07/editable.pptx`, `build07/svg/page_001.svg`, `build07/scene.resolved.json`, sibling `assets/`, `fonts.json`, and `validation.json`. Original crop: `source.png`. Actual source-width PPTX render: `build07/actual_source_width.png`. Complete source/actual comparison: `build07/source_vs_actual.png`; small text comparison: `build07/detail_comparison.png`.

The complete official CoRL 2025 Figure 2 is reconstructed: Stage 1, Stage 2 & 3, and the full Diffusion Expert/action-head/robot-embodiment panel. This is not Figure 1's photo teaser or a partial architecture crop. The source was only raster pixels: PDF page 3 rendered at scale 4 and cropped [420,285,2025,785], yielding 1605×500. No source-PDF text, embedded vectors/coordinates, or author drawing code was used to author the scene. Prepare's local macOS Vision OCR ran, but visual transcription was primary; obvious OCR errors such as “FiM” were not adopted.

## Native/raster boundary

302 native objects: **39 text, 216 shapes, 47 lines**. Ten movable raster crops occupy **6.3933%** of the full figure rectangle (sum of nonoverlapping crop boxes). They comprise two three-view observation strips, four embodiment robot images, and four tiny complex robot kinematics/motion-artwork crops. Thus the remaining assets are **photos plus complex robot artwork**, not exclusively photographic pixels. All readable diagram labels, module names, repeated-block notation, noise patterns, user symbols, separator, hatching and inter-module arrows are native. The small transition arrows between robot states were split out of the original broad crops and rebuilt natively. No editable text is overlaid on baked text. `asset_crops_final.json` lists every raster crop.

The source-sized source PNG is also retained as a comparison/audit asset in the resolved output; it is not a visible slide image. Native connector endpoints are fixed coordinates, not automatically rerouting connectors.

## Typography and mathematical scope

Times New Roman regular/bold and Arial regular were selected from installed fonts; the actual LibreOffice PDF used those families without substitutions. The source font identity cannot be proven from pixels. Fonts are not embedded or redistributed.

The original top title line is smaller than its second line; final native sizes are 25 and 28.5 source pixels. Expert labels use separately positioned 17 px lines to retain their source line spacing. Sans-serif block/head text uses 11 px Arial. The vertical “Block x N” is regular Times New Roman, rotated −90°; the visible source uses a lowercase x-shaped character and upright N. It has no italic variable, superscript, or subscript. **This figure does not validate rich mathematical superscript/subscript reconstruction.** No new formulas were added to make the example appear more challenging.

## Actual checks and measured evidence

`build07/validation.json`: preflight PASS, native objects PASS, rendered text PASS; aggregate PASS, with the runtime's `visual_review: required` marker retained. Full-page and small-label actual render images were opened and inspected. No PowerPoint or WPS application verification was performed.

PPTX was converted to PDF by the runtime's local LibreOffice, then the actual PDF was rasterized with PDFium at scale **1.6718585244451338** (1605 divided by PDF width 960.0094604492188 pt). Command:

```sh
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/dexvla_forward_20260912/render_actual.py build07
```

Raw size was exactly **1605×500**; there was no crop or registration. `actual_source_width_raw.png` is preserved. The script has an explicit all-white-row assertion for a possible 501-row PDFium rounding result, but this branch did not execute here. `rasterization.json` records the actual command and dimensions.

Eight fixed source-coordinate text windows were registered in `roi_contract.json` before source-width candidate measurements. `build05/ink_metrics.json` and final `build07/ink_metrics.json` retain before/after black-ink bounds. In the final eight diagnostic windows, each left/top/right/bottom bound differs by at most one source pixel. This is a local, source-guided **edge diagnostic**, not a glyph fidelity score or held-out evaluation. The regions were used during repair. Thresholding can include dark geometry in a window and matching extrema do not prove matching glyph shapes or exact spacing.

## Repairs and remaining limits

- Build01/02 were schema failures (duplicate element IDs, duplicate polygon clipping vertices); build03 stopped on undeclared joins/container relationships. All are retained. No scene quality thresholds were changed.
- Build04 was the first actual-PPTX render, and passed. Its source1 interior hatch, Stage2 FiLM placement and dashed arrows required visual repairs.
- Build05 repaired these and title alignment; build06 repaired source-specific typography/vertical label position; build07 minimized the robot-artwork raster crops and made their arrows native. Every actual build passed all three automated checks.
- Hatching is native polygon strips. Source hatching crosses some foreground fills, and the reconstructed stripes do not reproduce every blend/occlusion within the orange reasoning boxes or blue bars. Some panel corner shapes, rear-stack slivers, tiny user icons, and noise-cell diagonal patterns are approximations.
- The source robot artwork and native reconstruction are both low-resolution at these tiny regions; the raster boundary is disclosed above. Observation/robot photographs are source crops, not regenerated images.
- Small sans-serif labels retain approximately one-pixel edge differences; antialiasing and font-shape differences remain visible when enlarged. Automated PASS is not perfect source fidelity.

## Reproduction

No dependencies were installed and no repository files were modified. Used the existing `/Users/liyufeng/Code/super_img2ppt/.venv`, command-local Homebrew PATH, and the existing LibreOffice/System supplemental font directories.

Run `sh reproduce.sh /absolute/path/to/new_output` to rebuild the final resolved scene, its actual PDF, and source-width raster. Output must be fresh. `TASK_RUNTIME` may select another existing matching environment. `rasterize_source.py` reproduces the original crop from the cached official `paper.pdf` without text/vector extraction. Authoring history is `author.py` → `repair.py` → `repair_typography.py` → `split_robot_assets.py`; those scripts produce `job/scene.json`. The final resolved scene is the preferred portable edit/rebuild artifact.
