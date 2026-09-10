# Candidate independent forward replay — embodied pi0.5

The candidate was copied opaquely from `/Users/liyufeng/Code/super_img2ppt/skills/super-img2ppt` into `frozen_skill/`; 26 copied files hashed in candidate_hashes.json without inspecting implementation. No repository edits, package/font installs, external uploads, or agent delegation. Original report_original.md and all183 original artifacts hash-verified unchanged. Input is a super_teaser schematic, not a paper-original figure.

## Outcome

- `replay_04`: exact byte-identical original build_04 scene.resolved.json replay; exit0,6.199s, aggregate review; preflight/native objects pass.
- `replay_06_restored`: final build_06 scene with only flow_title frame width96→120; contains_text=true preserved for raster trajectories. Exit0,9.722s, aggregate review; preflight/native objects pass.
- Original false `rendered_glyph_overflow` for foreign A is absent in both. Original false flow_title rendered-ink drift is absent. Four previous nearby-subscript width warnings (obs_o,q,a_start,a_end) are also absent. No error or warning was manually exempted.
- Both retain task_sub rendered_ink_width_drift: measured54.75px versus actual51.952px. This remaining warning is not waived.
- **Source fidelity remains FAIL:4/26 locked ROIs pass in both, all22 text ROIs fail at least one threshold.** The runtime fix improves glyph ownership checks, not source alignment or font fidelity.

## Actual render and visual evidence

Opened both real LibreOffice PPTX-rendered full pages and dense Flow matching/Action comparisons. Flow matching and Action remain distinct, visible, and nonoverlapping; no own-text clipping observed. Original evidence at `/tmp/embodied-forward-TNEbMc/pdf_flow_evidence.json` assigns Flow matching ink x1051.845–1142.106 and Action A x1166.242–1175.432. The120px frame is retained in the candidate; no blank-frame workaround is required. Native text content, arrow hierarchy, imagery and geometry are otherwise unchanged. Candidate bitmap equality checks below distinguish unchanged artwork from QA-only effects.

Known unresolved fidelity: narrow-font/baseline drift in title/task/expert/camera/context/flow/step captions/footer, multiline spacing differences, upright rather than exact italic context math, mathematical weight differences, angular red connector corners and softened raster details.14 movable raster crops still include all robot scenes, braces, joints, separator and complex trajectory marks/ellipses.45 native text objects,16 shapes,20 lines/arrows retained. No full-page bitmap workaround and no native text overlays on baked labels.

## Reproduction

Commands are recorded exactly with environment overrides, inner exit code and duration in commands.jsonl. Same existing Python3.12.12 and LibreOffice26.2.4.2 environment, command-local PATH=/opt/homebrew/bin:$PATH, PYTHONPATH=`frozen_skill/src`, --font-dir=/Applications/LibreOffice.app/Contents/Resources/fonts/truetype. Candidate doctor still reports distribution version0.3.0; use candidate file hashes to identify this candidate. Runtime implementation was never read. Original scene04 SHA256 is b4721027490ff5ffcedf76cbfaa05527273a2be91bf6363e97a4e85aba72c42a.

## Integrity checks

- exact_original04_scene: True
- roi_contract_unchanged: True
- 06_only_width_restoration: True
- 06_contains_text_true: True
- original_183_artifacts_unchanged: True
- replay_04_render_pixels_identical_to_original: True
- replay_06_restored_render_pixels_identical_to_original: True

## Locked ROI measurements

Original26 ROI boxes, edge≤4px, centroid≤4px, IoU≥0.45 unchanged. Same min-channel<160 ink mask and source-size resizing evaluator as original. Both replays have identical ROI outcomes.

|ROI|bbox max px|centroid max px|IoU|Outcome|
|---|---:|---:|---:|---|
|title|15|8.456|0.146|FAIL|
|task|5|4.802|0.213|FAIL|
|observation|1|3.469|0.360|FAIL|
|images_header|5|0.984|0.329|FAIL|
|camera_label|7|3.900|0.139|FAIL|
|task_tokens_header|11|5.249|0.161|FAIL|
|token_put|3|2.800|0.253|FAIL|
|token_dishes|4|2.760|0.191|FAIL|
|prediction|5|3.534|0.275|FAIL|
|predicted_label|5|4.250|0.219|FAIL|
|predicted_text|1|0.858|0.325|FAIL|
|modes|9|4.557|0.225|FAIL|
|expert|5|5.511|0.204|FAIL|
|context|4|3.461|0.164|FAIL|
|flow_title|3|3.389|0.298|FAIL|
|robot_label|1|1.260|0.292|FAIL|
|noise|4|2.850|0.172|FAIL|
|step1|7|4.315|0.168|FAIL|
|step2|5|3.896|0.215|FAIL|
|step3|6|4.529|0.173|FAIL|
|execution|6|5.343|0.172|FAIL|
|footer|10|8.889|0.187|FAIL|
|token_top|1|2.485|0.931|pass|
|vla_left|3|1.384|0.945|pass|
|green_bottom|0|0.115|0.997|pass|
|down_arrow|2|2.503|0.939|pass|

Raw validation, PPTX, SVG, resolved/original scenes, fonts, actual PDFs, PNGs, density crops and ROI JSON are under each replay directory. All candidate artifacts are hashed in artifact_hashes.json (self excluded).
