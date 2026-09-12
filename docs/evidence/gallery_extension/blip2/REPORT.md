# BLIP-2 Figure 2 — complete editable reconstruction, fidelity limitations retained

Original: Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi. *BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models*. ICML 2023, PMLR 202:19730–19742. https://proceedings.mlr.press/v202/li23q.html . Figure 2 on PDF page 3. Publisher publication agreement grants CC BY 4.0: https://proceedings.mlr.press/pmlr-license-agreement.html ; license https://creativecommons.org/licenses/by/4.0/ . Copyright retained by authors. Archived publisher/license pages and SHA-256 hashes in provenance.json.

Adaptation: manually reconstructed editable text, geometry and connectors from complete figure raster; cat photo and snowflake preserved as local raster assets. Caption excluded from figure crop. Attribution included in PPTX notes. Source font identity is not claimed.

## Paths for publication integration

- Source: `/tmp/blip2-gallery-ovi4ki/source.png` (1464 × 303).
- Complete original page: `/tmp/blip2-gallery-ovi4ki/page3-full.png` (PDFium scale 3).
- Final build: `/tmp/blip2-gallery-ovi4ki/build_final/`.
- PPTX: `build_final/editable.pptx`.
- SVG: `build_final/svg/page_001.svg`.
- Resolved scene: `build_final/scene.resolved.json`; dependencies: `build_final/assets/`.
- Font manifest: `build_final/fonts.json`; fonts not embedded or distributed.
- Validation: `build_final/validation.json`.
- Actual LibreOffice PDF: `build_final/render/editable.pdf`.
- Actual PPTX render at source width: `build_final/render/source-width.png` (1464 × 303).
- Runtime preview: `build_final/render/page_001.png` (1600 × 332).
- Frozen hashes: `FINAL_FREEZE.json` (written before heldout evaluation; all hashes checked afterward).
- Commands and helper failure evidence: `commands.md`, scripts, check_* directories, build_*.log, dev/heldout metric JSON.

## Completeness and editability

48 native text objects, 71 native shapes, 18 native lines, 2 raster objects. Both architecture and all three attention-mask diagrams retained, including Q/T labels, all 48 gray/white matrix cells, query tokens and ellipsis, all objectives, bidirectional/causal/dashed links, x N, the printed source typo “mutlimodal causal”, and italic input prompt. Per-cell mask patterns visually checked against source. Source mask diagrams are not generic replacement grids.

Two raster crops use source coordinates `[x,y,width,height]`: cat `[4,104,121,120]`, snowflake `[157,110,22,21]`. Neither includes editable text. The cat crop preserves the source's fused white patch grid. Snowflake includes its blue background. Combined box area 14982 / 443592 = 3.38% of figure. Source raster itself is stored for comparison but is not a visible whole-slide image.

Source creation recipe: `pypdfium2.PdfDocument(paper.pdf)[2].render(scale=3).to_pil()`, then PIL crop `(164,204,1628,507)`. No original PDF text/vector coordinates or author drawing code were used as reconstruction answers.

## Actual validation

Preflight PASS; native-object/content checks PASS; rendered-text REVIEW due to legend “T:” visible width drift (measured 15px versus actual 12.786px). All expected native text was found in actual LibreOffice PDF. Arial regular, bold and italic resolve from locally installed fonts with no reported substitutions. This is LibreOffice evidence only; no native PowerPoint or WPS verification.

Parent visual review of first actual PPTX found complete panels, mask patterns, objective boxes and data paths. Final source-width PNG was also inspected after source typo correction. Text baselines, glyph details and matrix edge sampling still differ. The file is a reviewable complete conversion, not a claim of source-pixel accuracy.

## Frozen measurement result

Contract fixed before scene authoring: 8 development + 4 heldout ROIs; target jointly edge <= 4 source pixels and unregistered ink IoU >= .70. Edge means maximum difference of ink bounding-box coordinates, not contour Hausdorff distance. Black mask uses max(R,G,B)<150; feed-forward white mask uses min>220 and channel range<30. Render uses actual PPTX-export PDF at source width, no registration.

Development: 3/8 joint passes. Heldout: 0/4 recorded passes, comprising 3 valid failures and 1 invalid ROI mask. **The frozen held_cross_attention region uses black ink despite containing white text on blue; both masks are empty. Its sentinel edge 999 and IoU 0 are not meaningful fidelity estimates. It is retained as an evaluation-design failure and must not be advertised as four valid heldout measurements.** There are 11 evaluable ROIs in total, of which 3 pass; this diagnostic does not establish general performance.

| ROI | Split | Edge px | IoU | Joint |
|---|---|---:|---:|---|
| qformer | dev | 0 | 0.756 | pass |
| input_image | dev | 1 | 0.760 | pass |
| feed_forward | dev | 1 | 0.277 | fail |
| image_matching | dev | 0 | 0.784 | pass |
| learned_queries | dev | 1 | 0.543 | fail |
| mask_grid1 | dev | 0 | 0.459 | fail |
| encoder_arrow | dev | 0 | 0.679 | fail |
| legend | dev | 0 | 0.617 | fail |
| held_cross_attention | heldout | invalid: empty masks | 0.000 | fail |
| held_input_text | heldout | 0 | 0.297 | fail |
| held_grid3 | heldout | 2 | 0.298 | fail |
| held_mask_title | heldout | 2 | 0.144 | fail |

No holdout-driven scene changes. Final scene/PPTX/SVG/PDF/assets/fonts and source-width render hashes were frozen before heldout computation and rechecked afterward. The measurement script regenerates the identical source-width raster; its final hash is unchanged.

## Repair and failure history

Initial helper errors (missing fitz/numpy, duplicate Python keyword) were corrected without installation. First runtime checks preserved in check_01 (prepared empty draft after helper failure), check_02 (polygon radius schema rejection), and check_03 (missing nested-container declarations). Schema radius removal is one encoder-region preflight repair. Then one structural containment repair, one targeted dev ink-origin repair, and one visual source-spelling correction. No region underwent more than three meaningful repairs. Build_01 and build_02 plus dev metrics remain available; failed metrics were never deleted or thresholds lowered.

Initial dev result was 0/8. Targeted text origin repairs yielded the final 3/8. We stopped rather than tuning indefinitely. No runtime defect was identified; helper assumptions and measurement-mask design are the conversion author's limitations. Rebuild resolved scene in a new directory with the listed font directories and existing runtime; frozen artifacts should not be overwritten.
