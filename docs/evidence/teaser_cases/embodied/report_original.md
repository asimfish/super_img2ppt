# Embodied pi0.5 independent forward reconstruction report — original frozen runtime

Input is a super_teaser-generated explanatory schematic, NOT an original paper figure. Source was visually opened before ROI selection and scene authoring. Read only frozen SKILL.md, its three references and supplied image/OCR; implementation files were hashed, not inspected. No dependency/font installation, external upload, source-repository edit or delegation.

## Result

Final deliverable: `build_06/editable.pptx`, `build_06/svg/page_001.svg`, `build_06/scene.resolved.json`, sibling assets, fonts.json and validation.json. True LibreOffice PPTX→PDF→PNG render exists. Automated aggregate **review**, preflight and native objects pass. Independent fidelity result **FAIL**: only 4/26 fixed ROI tests pass; all 22 text ROIs fail at least one locked threshold. This is a usable editable draft, not a faithful reconstruction acceptance. Source font is unknown. No PowerPoint/WPS verification.

95 scene elements: 45 native text objects, 16 native shapes, 20 native line/arrow objects, 14 independently movable raster crops. Text content was checked visually against source; corrected OCR's `9t`→q_t, full-width brackets, `ioint`→joint, and subscript math. Source title pi0.5 and numbered stages 1/2/3 retained. Labels Task→VLA subtask prediction→Pick up the plate→context, camera input branch to both prediction and action expert, noise up-arrow, action chunk down-arrow, and sequence arrows were individually checked. No new inferred scientific data.

Raster boundaries: main robot illustration; three camera crops; three action-stage illustrations; three braces; joint-chain glyph diagram; camera separator/diamond; complex noise/trajectory strokes with three baked symbolic ellipses. The final trajectory crop correctly declares contains_text=true; initial build_01–05 metadata erroneously said false, corrected in build_06 without appearance changes. Photos, braces and trajectory details remain nonnative. No full-page background source image and no native text overlay on baked text.

## Frozen evidence and iteration history

`roi_contract.json` has 26 source-pixel xywh regions and SHA256 fixed before authoring. Thresholds unchanged: max bbox edge error≤4px, max ink centroid axis error≤4px, ink IoU≥0.45. Evaluator uses min(R,G,B)<160 ink threshold and resizes real render to original 1586×992 before measuring. Same evaluator for build_03/04/05/06. Pixel antialiasing and font difference affect IoU; it is not a perceptual/scientific score. Some glyph edges hit fixed ROI limits and thus width errors can be lower bounds. Keep every failure.

build_01: exit2, three text overflows and named connector/brace joins. build_02: exit2, prediction still needs 253.5px while frame is250px. build_03: exit0/review after extending its frame to258px. build_04: exit2 after evidence-led narrow-font/baseline correction, caused by runtime attributing adjacent Action's A to Flow matching. build_05: exit0/review with only the Flow matching empty frame shortened120→96px; visible text and glyph positions unchanged. build_06: exit0/review, only truthful raster-text metadata correction.

Repairs per affected region bounded: prediction had 3 repairs (font/size, width, source-ink font/position), then stopped; flow_title had 3 repairs (font family, source-ink font/position, blank-frame trim), then stopped. Other text regions at most2. Real text overlap at initial subtask lines repaired by valid font size and frame height; never exempted. Only source-visible connector joins/crossings have named exemptions.

The initial diagnostic message over-attributed width failure to Arial→DejaVu substitution. Correction: manifests contain multiple fonts. Final resolved runs show only Unicode subscript ₜ in images/state and ⋯ in action chunk fall back to DejaVu Sans. Other text uses explicit Liberation Sans or Liberation Sans Narrow; regular/bold/italic/bold-italic are resolved distinctly. Font substitution summary alone cannot locate affected text. Five remaining runtime width warnings concern task_sub, obs_o, q, a_start and a_end. Their positional proximity to subscript objects may contribute to glyph attribution; not independently proved for these five and not waived.

## Confirmed runtime regression trigger

Original `build_04/scene.original.json`, `.resolved.json`, PDF, validation and source assets retained untouched. Rebuild its original scene from original job-relative assets or use self-contained resolved scene. No candidate implementation read.

`flow_title` text is “Flow matching”, frame [1051,430.75,120,25]. Runtime emitted rendered_glyph_overflow glyphs='A' and measured-vs-rendered width90.5→123.589. Actual PDF extracted glyph evidence in `pdf_flow_evidence.json`: its own glyphs span x1051.845–1142.106; the neighboring “Action” A spans x1166.242–1175.432, y443.731–453.269. These are different native text objects and visibly disjoint. Thus A is wrongly assigned to the empty edge of Flow matching's frame. The blank-frame-only build_05 contrast removes the false overflow and false flow_title width warning while preserving visible ink. This is a rendered-check glyph ownership defect, not a true collision or a font availability failure.

## Visual limitations

Opened true full-slide renders and dense source/output crops for hierarchy, flow/action expert, left observation panel and execution sequence. Source labels are often narrow with taller glyphs; fitting Liberation Sans Narrow improves some widths but worsens several baselines and does not reproduce the original font. Main title, task title, expert title, Camera views, flow matching, context, step captions and footer retain visible font/position drift. Multiline Images/robot state and inference-mode label line spacing differs. Context math uses upright native o/q with subscript Unicode rather than the source's exact italic typography. Mathematical a/q/o weights differ. Text all remains readable; full fidelity not accepted.

Red routed arrow uses angular native segments in place of unsupported source round corners; source hierarchy topology and direction retained. Simple green boxes have flat fill replacing subtle source texture. Original photo crops are not retouched but LibreOffice image resampling softens trajectory lines, joint nodes and brace edges. No source line data was invented.

## Environment

Python3.12.12, super-img2ppt0.3.0, python-pptx1.0.2, Pillow12.3.0, fonttools4.64.0, pypdfium2 5.13.0, jsonschema4.26.0. LibreOffice26.2.4.2 (see exact version file). Installed /opt/homebrew/bin fontconfig and soffice selected with command-local PATH; font-dir is existing LibreOffice truetype directory. No packages installed. Auxiliary ROI script first failed with ModuleNotFoundError:numpy (exit1); rewritten with Pillow/pure Python, no new dependency. This auxiliary failure is not a skill-runtime defect.

## Command results

Full commands, env overrides, elapsed seconds and inner process exit codes are in commands.jsonl. The wrapper itself exits0 even if inner command fails: always use recorded inner exit_code, not shell wrapper status.

- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'prepare', '/Users/liyufeng/Code/super_img2ppt/output/teaser_cases_20260910/raw/examples/images/embodied/pi05-hierarchy-v3.png', '--out', '/tmp/embodied-forward-TNEbMc/job'] — exit 0, 2.595 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'doctor'] — exit 0, 0.209 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '/tmp/embodied-forward-TNEbMc/job/scene.json', '--out', '/tmp/embodied-forward-TNEbMc/build_01', '--font-dir', '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype'] — exit 2, 0.966 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '/tmp/embodied-forward-TNEbMc/job/scene.json', '--out', '/tmp/embodied-forward-TNEbMc/build_02', '--font-dir', '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype'] — exit 2, 0.88 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '--help'] — exit 0, 0.271 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '/tmp/embodied-forward-TNEbMc/job/scene.json', '--out', '/tmp/embodied-forward-TNEbMc/build_03', '--font-dir', '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype'] — exit 0, 7.611 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '/tmp/embodied-forward-TNEbMc/job/scene.json', '--out', '/tmp/embodied-forward-TNEbMc/build_04', '--font-dir', '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype'] — exit 2, 5.367 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '/tmp/embodied-forward-TNEbMc/job/scene.json', '--out', '/tmp/embodied-forward-TNEbMc/build_05', '--font-dir', '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype'] — exit 0, 6.591 s
- ['/Users/liyufeng/Code/super_img2ppt/.venv/bin/python', '-m', 'super_img2ppt', 'build', '/tmp/embodied-forward-TNEbMc/job/scene.json', '--out', '/tmp/embodied-forward-TNEbMc/build_06', '--font-dir', '/Applications/LibreOffice.app/Contents/Resources/fonts/truetype'] — exit 0, 6.721 s
- ['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--version'] — exit 0, 0.455 s

## Fixed ROI results (final)

|ROI|bbox max px|centroid max px|IoU|Result|
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

All product hashes are in artifact_hashes.json (manifest excludes itself to avoid recursion). Frozen package hashes in frozen_skill_hashes.json. Reproducible author/repair/measure scripts retained. Original report must not be overwritten by any candidate retest.
