# Vision Mamba Figure 2 — public forward reconstruction test

Final candidate: `build_06`. Automated preflight/native-object/rendered-text checks pass. Strict source-fidelity target fails: 5/12 ROIs satisfy **edge ≤4 px AND IoU ≥0.70**. Dev: 5/8; heldout: 0/4. The candidate is useful editable reconstruction evidence, not a fidelity pass.

## Source and coverage

Official ICML 2024 / PMLR paper, page 5, complete Figure 2 artwork (caption excluded). Rasterized entire page at scale 2; pixel crop [110,130,1090,388] gives 980×258. Both panels, the legend, 0–9 plus class token, projection polygons, bidirectional convolution/SSM branches, gates, state loops, residual connection, labels, and captions within the figure are included. No source PDF text/vector coordinates or author drawing code were used as reconstruction answers.

See ATTRIBUTION.md, source/license.html, source/official.html and source_hashes.json for publisher CC BY 4.0 grant, attribution, and exact provenance. Three image-only original artwork crops remain raster: input image and two patch strips. No raster label overlays.

## Native content and rendering

Objects: {'shape': 45, 'text': 42, 'line': 71, 'image': 3}. All readable labels are editable text; geometry/connectors use native shapes/lines. Native text symbols include italic x/y/z/h and small state subscripts. Times New Roman regular/bold/italic resolved without substitution; font files are not redistributed.

Actual PPTX rendered by LibreOffice, rasterized by PDFium at source width 980; no registration, rescaling alignment, or pixel-mask shifts were applied. PowerPoint/WPS were not separately tested. Source-width actual: build_06/render/actual_source_width.png; larger actual preview: build_06/render/page_001.png.

## Frozen measurement contract

roi_contract.json was saved/hash-recorded before authoring: 12 ROIs, eight dev and four heldout. Dark-pixel mask is all RGB channels <140, bounding ink edge maximum and unregistered set IoU; ROI boxes and thresholds unchanged. Some ROIs intentionally contain bordering geometry, making their mask a combined label/geometry measurement rather than pure glyph IoU. All heldout metrics remained unopened until candidate_freeze.json was written after parent visual review. No scene edits after freeze.

| ROI | Split | Max edge px | IoU | Joint |
|---|---|---:|---:|---|
| mlp | dev | 0 | 0.7877 | pass |
| encoder_label | dev | 1 | 0.7302 | pass |
| flatten | heldout | 2 | 0.3035 | FAIL |
| norm | dev | 1 | 0.7863 | pass |
| forward_conv | dev | 0 | 0.5038 | FAIL |
| backward_conv | heldout | 2 | 0.2558 | FAIL |
| activation | dev | 4 | 0.4161 | FAIL |
| forward_ssm | dev | 3 | 0.7115 | pass |
| backward_ssm | heldout | 5 | 0.5473 | FAIL |
| panel_title | dev | 1 | 0.7368 | pass |
| token_numbers | heldout | 2 | 0.1239 | FAIL |
| output_arrow | dev | 3 | 0.5200 | FAIL |

## Attempts and remaining errors

All attempts remain on disk. build_01: missing specific intentional layer/container declarations, preflight fail. build_02: class token exceeded declared parent shape, preflight fail. build_03: first actual PPTX; italic y left glyph overhang fails rendered check, and visually reversed output projection was found. build_04 repair 1: fixed y padding/projection and adjusted label size/origin, automated pass, dev 1/8. build_05 repair 2: adjusted source-centered module bounds/font widths, automated pass, dev 2/8. build_06 repair 3: final label origins/activation restoration, automated pass, dev 5/8. Three meaningful typography repairs maximum; no further tuning after heldout reveal.

Remaining quantitative failures: Forward Conv1d and Activation glyph overlap; output-arrow stroke/head geometry; heldout Flatten label width/glyph spacing, Backward Conv1d/SSM shape and glyph differences, and token digit/arrow alignment. All token values 0–9 and class star remain semantically present, but low heldout token IoU (0.124) shows their pixel alignment is weak. Backward SSM also exceeds edge target (5px). Rounded shape outlines, small serif glyphs and connector heads remain visibly different at magnification. No claim of exact source-font identity.

Parent visually reviewed source and first actual two-panel output before freeze, accepted semantic coverage with projection correction and disclosed font/arrow differences. Final self visual review inspected the actual PPTX image.

## Deliverables

- build_06/editable.pptx
- build_06/svg/page_001.svg
- build_06/scene.resolved.json and build_06/assets/
- build_06/fonts.json, build_06/validation.json
- build_06/render/editable.pdf and actual_source_width.png
- scene.json, assets/, author.py, relations.py, repair_01.py through repair_03.py, measure.py
- source/ original PDF, official webpage, license webpage, page raster
- source_hashes.json, candidate_freeze.json, roi_contract.json, commands.md
