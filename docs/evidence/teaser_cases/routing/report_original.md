# Routed-branches independent forward test — original report

Final artifact: `build_04/editable.pptx`; editable SVG `build_04/svg/page_001.svg`; complete editable source `build_04/scene.resolved.json`. This input is a super_teaser-generated synthetic explanatory schematic, not an original paper figure.

Protocol: inspected only the supplied image, frozen SKILL.md and references, own generated job/reports; implementation bytes were read only to hash. No implementation, other cases, tests, upstream prompt or external image service was inspected. No dependencies/fonts installed, no repository edits, no uploads, no further agents. All outputs are under this isolated /tmp directory. Python module runs used command-local PATH=/opt/homebrew/bin:$PATH and PYTHONPATH=frozen-skill/src. Runtime 0.3.0; full dependency versions in command_01.json; Python 3.12.12; LibreOffice 26.2.4.2 (environment.json).

Before scene authoring, 25 source-pixel text/line ROIs and thresholds were frozen in roi_contract.json. Thresholds remained unchanged: ink RGB max <170 or chroma >45 with min channel <170; bbox max edge delta <=4px; centroid max coordinate delta <=4px; ink-count relative delta <=25%. Render was aspect-matched to source dimensions using Lanczos, then the same masks/ROIs were applied. These are regional diagnostics, not character-shape identity. The ROI count is not a whole-slide fidelity percentage. Bbox bottom edges are visible ink bottoms, not inferred typographic baselines.

Build_01 exit 2 retained the initial overlap failure: inactive_word/trunk and mergelabel/merge. Neither pair was exempted. Repair 1 narrowed inactive_word within its source area and separated Weighted/merge/(additive) into native semantic lines. Build_02 passed runtime checks but only 4/25 fixed ROIs passed; Arial bold was too wide/thick (title edge drift 16px). Repair 2 used Arial regular for larger labels, retained small bold legend/key labels, set 5px rounded corners and corrected shaft thickness from 2.5 to 3px. Build_03 passed runtime checks and 21/25 fixed ROIs. Repair 3 adjusted title 24->23px, footer 21->21.2px with measured position correction, split output formula into its source lines, and moved top connector center to y244.5 with source-sized arrowhead. No region received more than 3 repairs. All four scene versions, failures and reports remain.

Final independent measurements: 25/25 fixed ROIs pass. Runtime preflight/native_objects/rendered_text all pass; runtime visual_review remains required. I opened the actual LibreOffice full-page preview and source-normalized dense gate/process and merge/formula crops, not a surrogate scene rendering. I also inspected source full page and dense source crop. No missing labels, clipping or unintended content overlap observed in these inspected areas. No native PowerPoint/WPS verification.

Topology checked individually: token x branches at common trunk to E1 and E3, while middle horizontal reaches gated E2; E1/E3 gate outputs point right to their processor, then right to 0.6/0.4; upper route turns down into +; lower route turns up into +; + points right to formula. E2 processor has no incoming/outgoing execution connector. All three gate status symbols, legend arrow/active/inactive/weight/merge symbols, lane dividers, E labels, processing lines, all numeric formula tokens and schematic disclaimer are present. Lower branch connector heights intentionally follow the slight source y591/y593 difference. Source-verified exemptions are named: route junctions, divider crossings, check/cross strokes and connectors crossing gate border. Actual label collisions were repaired, never exempted.

Native editability: 37 text objects, 22 shapes, 28 lines = 87 native objects; zero raster image elements. Source image copied into assets is comparison provenance only and is not visible slide artwork. Checkmarks/crosses are native line strokes; icons use flat native circles. Editable connector endpoints are fixed; node movements do not automatically reroute them.

Remaining differences: source font identity cannot be uniquely inferred; Arial regular/bold substitute source visual typography, with larger labels visibly lighter in some places. No runtime font substitution; actual Arial.ttf and Arial Bold.ttf hashes in fonts.json; fonts are not embedded. Source's subtle paper/background texture, icon shading and faint box shadows are omitted; circles retain flat fills, so those effects are not faithfully reconstructed. Source check/cross symbols have thicker/softer stroke styling than the native approximation. Regional text edges differ by up to 4px and some label centroids differ by up to 3.66px; passing broad ink ROIs does not prove glyph-level alignment, exact weight or complete visual fidelity. No remaining nonnative region, but effects were simplified rather than rasterized. Final result is a reviewable editable reconstruction, not pixel-identical reproduction.

Runtime defects: none established in this constrained test. The first failure correctly detected authored layout collisions. Automated pass plus poor fixed-ROI fidelity in build_02 illustrates the documented validation boundary, not proof of a runtime bug. All command exits, durations and raw outputs are retained in command_*.json.

## Commands

- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt doctor`: exit 0, 0.306s.
- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt prepare /Users/liyufeng/Code/super_img2ppt/output/teaser_cases_20260910/raw/examples/images/fixtures/fixture-routed-branches.png --out /tmp/teaser-routing-Dg29E2/job`: exit 0, 3.383s.
- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build --help`: exit 0, 0.279s.
- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build /tmp/teaser-routing-Dg29E2/job/scene.json --out /tmp/teaser-routing-Dg29E2/build_01 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype`: exit 2, 0.778s.
- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build /tmp/teaser-routing-Dg29E2/job/scene.json --out /tmp/teaser-routing-Dg29E2/build_02 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype`: exit 0, 4.647s.
- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build /tmp/teaser-routing-Dg29E2/job/scene.json --out /tmp/teaser-routing-Dg29E2/build_03 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype`: exit 0, 4.601s.
- `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build /tmp/teaser-routing-Dg29E2/job/scene.json --out /tmp/teaser-routing-Dg29E2/build_04 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype`: exit 0, 5.316s.

## Fixed ROI final results

| ROI | Max edge delta px | Max centroid delta px | Ink-count delta | Result |
|---|---:|---:|---:|---|
| title | 2 | 0.264 | 11.148% | pass |
| gate_title | 2 | 1.066 | 4.290% | pass |
| gate_instruction | 4 | 1.364 | 3.799% | pass |
| active1_label | 3 | 3.657 | 1.901% | pass |
| active3_label | 4 | 2.948 | 3.841% | pass |
| inactive_label | 0 | 1.185 | 7.002% | pass |
| input_text | 4 | 0.567 | 9.043% | pass |
| E1_gate | 3 | 0.378 | 5.532% | pass |
| E2_gate | 2 | 0.712 | 1.375% | pass |
| E3_gate | 2 | 0.109 | 6.207% | pass |
| E1_processor | 4 | 1.912 | 0.345% | pass |
| E2_processor | 1 | 0.234 | 14.082% | pass |
| E3_processor | 4 | 1.445 | 0.872% | pass |
| weight_title | 2 | 0.847 | 11.622% | pass |
| weight06 | 1 | 0.934 | 10.210% | pass |
| weight04 | 1 | 0.584 | 14.286% | pass |
| merge_label | 2 | 1.807 | 13.999% | pass |
| output | 1 | 1.129 | 17.219% | pass |
| footer | 0 | 0.818 | 6.610% | pass |
| top_connector | 1 | 1.147 | 1.917% | pass |
| bottom_connector | 1 | 0.823 | 1.299% | pass |
| upper_merge_vertical | 0 | 1.570 | 2.177% | pass |
| lower_merge_vertical | 1 | 1.690 | 1.923% | pass |
| separator_top | 1 | 1.467 | 6.475% | pass |
| legend_text | 2 | 0.944 | 8.993% | pass |

All artifact SHA-256 hashes are in artifact_hashes.json (manifest excludes itself). Frozen package hashes are in frozen_skill_hashes.json.
