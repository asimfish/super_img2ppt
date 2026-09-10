# Independent image-only forward evaluation: UniAD CVPR2023 Figure2

Final automated status: **review**, actual PPTX rendered. Strict source fidelity: **FAIL**. Final fixed ROI result **8/36** (build02 4/36, build03 7/36). This is a complete architecture reconstruction with explicitly disclosed raster boundaries, not a fully editable or pixel-matched reproduction.

## Source and method

Official OpenDriveLab/UniAD `sources/pipeline.png`, pinned commit532fc330151758c5e345aef74d2a1bf1042e50ab, SHA256a00580c3f7eaaa2603d91e2dfaa86b23ed7a44eeb3fc3079fded860e620d3c89. Visually verified against official CVF PDF page3 Figure2; screenshot retained. Repository README explicitly applies Apache2 to assets/code unless otherwise specified; license retained. No author implementation, PDF text/vector coordinates, or runtime implementation used. Frozen skill instructions/references and black-box CLI only. Image opened before scene authoring. 36-region contract written before scene elements were populated; SHA retained. Existing environment only, no dependency/font installation.

## Editability and topology

Final102objects: **28text,27shapes,39lines,8images**. All major modules, stage brackets, BEV/track/map/motion/occupancy queries, agent-to-planner bypass, and connectors retained. Native Q is bold italic; native Latin text and K,V remain editable. Exact raster regions: camera pictogram stack, backbone stack, BEV tile, motion trajectories artwork, occupancy illustration, planner road illustration, and two fused modules TrackFormer/MapFormer. The last two contain their original labels and are declared contains_text=true; no native duplicate text overlays. An initial unbuilt scene would have replaced artwork behind labels with flat fill; it was rejected before rendering and retained for audit, not delivered. This limitation prevents full-label editability; no original panel was deleted.

Source images, scene geometry, texts and renderer differ in antialiasing and font weight. Source font identity is unknown. Actual TimesNewRoman regular/bold/italic/bolditalic files resolved without substitutions; this does not establish correct source font. Fonts not embedded. Native connector endpoints fixed rather than rerouted automatically.

## Attempts and bounded repairs

- build01: fail before render. Agent label frame needed58px rather than55px; legendB missing real circle container; MapFormer raster top-margin/source arrowtip collision required narrow named pair. These were scene-authoring errors, not established runtime bugs.
- build02: actual review. Fixed36ROI 4pass. Parent independently inspected actual preview and observed plain Q/style weight mismatch; feedback is explicitly part of subsequent revision, not blind original acceptance.
- build03: actual review. Q rich text, module boldness, source arrow/KV colors, body-size and ink-origin adjustments. Fixed36ROI7pass. Source-colored arrows can score worse under frozen dark-only mask; failures retained.
- build04: actual review. Final bounded font sizing, source multiline positions (agent/scene split into native lines), original gray BEV query links restored, native round-corner radius corrected, bracket gap corrected. Fixed36ROI8pass. No region received more than3 meaningful changes after first candidate. Stopped with failed fidelity, not repeated tolerance relaxation.

## Measurement limits and unresolved failures

Metrics use actual PPTX exported PDF rendered at1880px width (1880x485 output vs1880x484 source), same fixed coordinates, dark maxRGB<150, max ink-edge error3px and minimumIoU0.70. No registration or posthoc threshold increase. Planner source text is red so its mask is empty: that ROI is INVALID/failed, never counted success. Several ROIs include circle/box/bracket edges, so those are composite-region results, not claims of precise glyph alignment. The final8passes consist of7geometry regions and B query label. Most text remains belowIoU0.70 despite several edge errors<=3px. Two raster labels also fail this strict metric due rendering/ROI boundary differences. Motion/Occ/Planner font weight and line spacing remain visibly imperfect. Circle B alignment and small K,V text, some query positions and colored thin-line antialiasing remain imperfect. This experiment establishes no runtime defect with causal evidence.

Build04 is selected as best reviewable final because source semantics/style/topology are more faithful, not because all automatic/source checks passed. Actual LibreOffice rendering only; native PowerPoint/WPS unverified. Original metrics, failed preflight, intermediate scenes, command logs and all hashes retained. Pillow emitted a getdata deprecation warning in measurement; it did not affect exit status.

## Outputs

Final `build_04/editable.pptx`, `build_04/svg/`, `build_04/scene.resolved.json`, `build_04/fonts.json`, `build_04/validation.json`, `build_04/render/source_width.png`. Scene source and crops under job/. Four build command records contain argv, elapsed time, exit code and captured stdout/stderr. Setup/source acquisition and authoring commands are retained as executable local scripts and source/environment manifests; the interactive shell transcript is not fabricated as a complete timed command log.
