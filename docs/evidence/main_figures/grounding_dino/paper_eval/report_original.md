# Independent original report: Grounding DINO published main architecture

Final result is a reviewable editable reconstruction, **not fidelity acceptance**. Final build_10 passes structural/native-object checks and has runtime status `review`; the unchanged strict pixel contract passes **11/35 regions**, versus **0/35** for first actual render build_04. **32/35** final region ink edge errors are at most 4 source pixels. The 21 representative title/body-label regions targeted in final_alignment.json all have maximum ink-box edge error <=1 source pixel; many still fail glyph IoU. Do not equate edge alignment with exact typography.

## Source and independence

Grounding DINO, ECCV 2024, Figure 3, full three-panel model architecture (graphic only; caption excluded). Conference primary source: https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/6319_ECCV_2024_paper.php . Official paper PDF: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06319.pdf . The untouched downloaded PDF is ../paper.pdf; source_manifest.json records SHA256, page index4, render scale6 and raster crop [800,680,2940,2140]. The final source is 2140x1460. No source PDF text, vectors, embedded images, generator coordinates or original editable artwork was used to reconstruct it. PDFium was used to rasterize source pages only; output PDF text inspection was used for verification.

Originally selected official GitHub .asset/arch.png at commit856dde20aee659246248e20734ef9ba5214f5e44. Visual comparison against published paper revealed a changed upper-left matrix prompt and spacing. That variant and its first failed preflight are retained one directory above; it is **not counted as the final actual-paper test**. A new paper_eval ROI contract was frozen before adapting the new source. The unpublished variant's coordinates were derived manually from its pixels, then independently mapped/visually corrected against the published raster. Full paper source and exact local photo crops are third-party research material; upstream repository Apache-2.0 LICENSE does not establish an independent license for every PDF figure/photo. Retain paper citation and rights; do not relabel this as our original diagram or original measured experiment. No fonts distributed.

Skill was copied opaquely from the existing super-img2ppt skill; only SKILL.md and reconstruction/scene references were read. Original copied file hashes remain unchanged: False. No implementation edits/reads, new dependencies, font installs, external OCR, or user source upload. Existing local Vision OCR was used for the initial repository bitmap only; new published figure text was checked visually. User/source text is task data.

## Editability and inspected artifacts

729 final elements: 59 native text objects, 274 native shapes/freeforms, 392 native lines/arrows, 4 exact raster photo composites. All readable diagram labels, rotated prompts, colored panels, matrix cells, tensor meshes and feature/query slats remain native. The four photo composites preserve original animal photos and their borders, are independently movable, and have no editable internals. Source image is comparison-only, never a visible full-page reconstruction backdrop. Native gradients are used in fusion panels. Native query bars were corrected to gold/yellow, distinct from green text tokens.

Deliverable directory: build_10; editable.pptx, svg/page_001.svg, scene.resolved.json, fonts.json, validation.json and assets/. Actual native PPTX was rendered with LibreOffice; default PNG is [1600, 1092], source-width PDF raster is [2140, 1460] (PDFium raw size [2140, 1460], Lanczos normalized only for the final one-pixel height rounding). Opened source, actual full previews 04/06/08/10, plus rotated label output crop. Native PowerPoint/WPS not checked.

## Fixed measurements and bounded corrections

roi_contract.json: 35 source-pixel regions, dark=maxRGB<150 or light=minRGB>220, max ink-edge error<=4px **and** ink IoU>=0.70. Both must hold. No thresholds, region rectangles, or denominator changed. The matrix ROI covers a local left/upper portion, not all matrix cells; the deformable region also includes part of its rounded border, so do not present those values as isolated label accuracy. The default 1600px preview was not used for numerical comparisons. There is no held-out evaluation set: these are measured reconstruction/development regions, not generalization evidence.

| Build | Exit | Runtime status | Strict ROI pass /35 | Seconds |
| --- | --- | --- | --- | --- |
| 01 | 2 | fail | not rendered | 1.08 |
| 02 | 2 | fail | not rendered | 1.53 |
| 03 | 2 | fail | not rendered | 1.13 |
| 04 | 0 | review | 0 | 5.76 |
| 05 | 2 | fail | not rendered | 1.38 |
| 06 | 0 | review | 0 | 5.92 |
| 07 | 2 | fail | not rendered | 1.41 |
| 08 | 0 | review | 3 | 5.97 |
| 09 | 0 | review | 11 | 6.10 |
| 10 | 0 | review | 11 | 6.07 |

Initial variant/preflight scene errors included tight matrix text frames, undeclared projected grid/junction contacts, text placement and inset containment. Actual-paper01/02 retained matrix/photo placement corrections and proper original prompt occlusion. Paper03 still reported a rotated text/rear-pill overlap; build04 added one narrow source-verified pair to obtain real glyph evidence. Actual PDF min glyph x609.566 slightly intersects rear pill endingx611 while foreground pill x603..637 occludes that area. Constant reported overlap area was the frame intersection, **not proof of a runtime bug**. Parent independently inspected the same scene. No runtime defect established in this case.

Typography loop: first actual Liberation Sans render04; family-only Carlito candidate05 failed preflight,06 rendered but was too small; measured consistent body size x1.15 plus spacing/source-smaller Q/K/V corrections07/08 improved fixed ROI to3/35. Third and final visible text correction09 used bounded +/-4px source-ink translation search, then rebuilt actual PPTX and measured11/35. Predicted shifted mask scores were not substituted for actual render scores (e.g. leftFFN prediction0.725 actually0.630 remains fail). Ten is the count of complete scene builds, not ten font revisions per region. Rotated prompt region was stopped with explicit occlusion/appearance limitation. Final whole-figure topology check found a9.275px authored gap in continuous text-feature trunk; build10 corrected only that endpoint with a source-verified shared-junction pair. Metrics remained11/35.

## Unresolved fidelity and runtime warnings

Font identity cannot be proven from pixels. Final uses Carlito-Regular and LiberationMono-Regular, both actually resolved with no requested-family substitution and no embedding. Carlito is an inferred visual substitute; source may use a related humanist font. Rendered width warnings remain for input_text and vanilla_text: [{"code": "rendered_ink_width_drift", "severity": "warning", "slide": "page_001", "element": "input_text", "measured_ink_width_px": 123.75, "rendered_ink_width_px": 119.972, "message": "Visible text width differs from the measured font by over 3% and 2 px; inspect mixed-script spacing and compare the source"}, {"code": "rendered_ink_width_drift", "severity": "warning", "slide": "page_001", "element": "vanilla_text", "measured_ink_width_px": 143.25, "rendered_ink_width_px": 138.223, "message": "Visible text width differs from the measured font by over 3% and 2 px; inspect mixed-script spacing and compare the source"}].

Strict failures remain in title shapes/weights, some same-baseline text glyph outlines, Deformable Self-Attention region, narrow rotated prompt appearance, monospaced input category line, dense tensor mesh/strip pitch, and arrow pixel/stroke alignment. Full arrow/source topology was visually checked and preserved; exact thin-stroke pixels do not pass. The wire bridge is a native eight-chord approximation, not an exact editable Bezier. The shaded/pale rear prompt/matrix styling is approximated using explicit colors because the schema lacks general opacity. Raster photo crops are exact source regions, but rendering antialiasing differs.

These failures are preserved as evidence. This case demonstrates the skill can deliver a complex native architecture and improve measured alignment, **but does not establish that arbitrary conference main figures convert cleanly or automatically**.

## Evidence

command_01..10.json store exact build commands, overrides, output, exit code and wall times; each scene_NN.json/build_NN remains. Auxiliary failure record retains premature measure05 FileNotFoundError and harmless Pillow getdata deprecation warnings. source_manifest.json, roi_contract.json, metrics_04/06/08/09/10.json, rotated_glyphs_04/06/08/09/10.json, font candidate/size/spacing/final alignment records, topology_review.json, and environment.json provide raw audit detail. ../frozen_hashes.json seals opaque runtime files. Artifact hashes are generated after this original report is written; do not silently overwrite this report.
