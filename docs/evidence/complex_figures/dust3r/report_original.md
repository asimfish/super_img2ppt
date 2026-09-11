# DUSt3R CVPR 2024: independent complete-figure reconstruction

Final candidate: `build_07/editable.pptx`, two slides. Automated status **review**; strict Figure 2 pixel fidelity **FAIL**. Development regions 2/16, held-out regions 1/8. Do not describe this as a high-fidelity or all-aligned conversion.

## Source and coverage

Official CVPR 2024 paper, Wang et al., *DUSt3R: Geometric 3D Vision Made Easy*. The bounded download, SHA256 and URL are in `source_manifest.json`; crop coordinates, raster scale and PNG hashes are in `crop_manifest.json`. The official PDF was inspected visually, without reading PDF text, vector coordinates, author drawing code, or the conversion runtime implementation as reconstruction answers. Frozen skill bytes are hashed separately.

- Slide 1 is the complete Figure 2, “Architecture of the network”, page 4 (printed 20700). Both image inputs, patchification tokens, shared ViT encoders, both transformer decoders, bidirectional cross-attention, both heads, pointmap/confidence outputs, camera frame and the overlaid red/blue 3D point cloud are retained. Caption is outside the figure crop.
- Slide 2 is the complete Figure 3 qualitative reconstruction demonstration, page 5 (printed 20701): RGB/depth/confidence for two scenes and separate reconstructed/aligned 3D views. This is **not a second complex architecture**. The paper caption identifies the right scene as a global-alignment result. It is a mostly-raster qualitative figure, honestly retained as independently movable local regions.

All source and derived paper images remain local evaluation materials. No redistribution license was established. CVF availability alone is not a grant to redistribute the paper or figures.

## Editable boundary

Figure 2: **31 text objects, 24 native shapes, 60 native line segments, 4 raster assets** (119 objects). Readable pipeline and mathematical labels are native text. Multiplication signs in dimensional exponents use separately positioned native text; no baked formula crops. Native geometry includes paired encoder/decoder/head backgrounds, 14 token rectangles, camera faces, axes and connectors.

Four Figure 2 raster assets are two input cube illustrations and two nonoverlapping point-cloud crops. The upper point-cloud crop also retains a short terminal red curve segment fused with the artwork. The preceding curve is approximated with native short straight segments and its raster join is visibly imperfect. Token patch textures/triangular color pieces are simplified into flat native rectangles. Camera polygons and arrowhead profiles approximate the source.

Figure 3: **17 independent raster image objects**, no native text (there are no separate readable diagram labels in the cropped figure). Photographs, depth/confidence maps and 3D views are not editable internally. No full-slide screenshot is inserted as the reconstruction.

## Fixed evaluation and held-out protocol

`roi_contract.json` froze 24 regions before authoring: 16 development and every third region held out (8). Both labels and geometry are covered, including encoder/decoder, arrow and camera regions. The source is 1496 × 352 pixels. Actual exported PPTX was rendered through LibreOffice to PDF; that PDF was rasterized at **exact source width**, without translation/registration. A region passes only when maximum ink bounding-box edge difference is <=4 pixels **and** mask IoU >=0.70. Colored formula/camera regions use a chroma mask; other regions use min(R,G,B)<180. Broad geometry regions can include enclosed labels; the mask is not a pure-outline metric. Topology was visually inventoried separately, not inferred from pixel scores.

`candidate_freeze.json` hashes the final PPTX, scene, actual PDF and actual previews before any held-out measurement. All six hashes were rechecked unchanged after measurement. Held-out scores were measured once for build_07 and were not used for subsequent corrections. Full-page visual inspection was used throughout; this is a **numeric-feedback holdout within one figure**, not a blind unseen-image generalization experiment.

- First actual render build_03 development: **1/16**.
- Repaired build_05 development: **2/16**.
- Frozen final build_07 development: **2/16**.
- Frozen final build_07 held-out: **1/8**; only blue camera passes (IoU 0.950, edge 1px).
- Combined final: **3/24**. Separate developmental and held-out results remain the primary report.

Examples: patch-2 bounding edges improve 7→1px, head-2 7→2px, confidence-1 5→1px, yet their final IoUs remain 0.268/0.444/0.462, respectively. Corrected red camera reaches edge 2px, IoU 0.892. Low glyph IoU despite near-correct bounding edges is a real residual limitation, not evidence that alignment is solved. Frozen formula-2 edge error 12px and IoU 0.232 remains a failure.

## Attempts retained

1. build_01: rejected before validation because the chosen custom arrowhead exceeded a short last curve segment. Original author script retains that initial scene generation. No successful artifact claimed.
2. build_02: preflight fail. Point-cloud rectangle included empty/adjacent label area, causing real reconstruction overlap issues. Split the point-cloud into two text-free local crops and separated the native/raster curve boundary.
3. build_03: first actual PPTX render; **review**.
4. build_04: trial Noto Sans plus position/line-height repair. Preflight rejected genuine measured frame overflows and collisions. Retained failed scene/report; family reverted, not silently relaxed.
5. build_05: bounded Arial origin/line-height repair; **review**. This is the second repair round for repeatedly adjusted labels; no endless tuning.
6. build_06: transcribed dimensional multiplication symbols as separately positioned native exponent text; **review**. This was a content/style correction, not a holdout-driven fit.
7. build_07: moved only those separate image/confidence exponent origins to attach to the base symbol; **review**. Protocol deviation: if the failed global Noto Sans trial and its reversion are each counted as corrections, the image/confidence exponent regions exceed the requested three-correction budget when the later content correction and origin attachment are included. Those regions are not claimed as budget-compliant successes; held-out measurement still occurred only after the final freeze. Final freeze precedes held-out measurement.

There is no established causal runtime defect from this case. The rejected preflight layouts were authoring mistakes, not checker bugs. The exact build commands and observed outcomes are recorded in `commands.json`; this command inventory was written after execution and is not claimed to be a captured timestamped terminal transcript.

## Remaining limitations

Source font identity is unknown. Arial requests resolve partly to Liberation Sans and DejaVu Sans; `fonts.json` records faces and glyph fallbacks. Native text preserves semantic labels but is visibly different in glyph shape, baseline, spacing and mathematical typography. Superscript index/comma treatment is approximate. The native curve and arrow profiles, simplified token cells, shadow-free shapes and source/raster join differ from the paper. Photos/point-cloud pixels are retained locally, not interpreted as measured new scientific results. Figure 3 raster tiling preserves broad composition but does not make its contents editable.

LibreOffice actual rendering and native-object/text checks were executed. Native Microsoft PowerPoint and WPS were not tested. No dependency/font installation, source upload, repository edit or push was performed by this independent evaluator.

Deliverables: `build_07/editable.pptx`, `build_07/svg/`, `build_07/scene.resolved.json`, `build_07/assets/`, `build_07/fonts.json`, `build_07/validation.json`, and `build_07/render/`. Raw failures and original source files are retained in this job directory.
