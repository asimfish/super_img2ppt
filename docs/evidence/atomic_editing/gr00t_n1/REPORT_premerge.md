# GR00T N1 — complete Figure 3 and native editing test

Final: **`build_05_grouped/editable.pptx`**. Full architecture reconstructed from the paper raster, with 35 native semantic groups. Automated status is **review**, with no blocking errors and two retained tokenizer width-drift warnings. Actual PPTX rendering and real edits were tested through LibreOffice, not native Microsoft PowerPoint/WPS UI.

## Source and permission

NVIDIA; Johan Bjorck, Fernando Castañeda, Nikita Cherniadev et al. *GR00T N1: An Open Foundation Model for Generalist Humanoid Robots*, arXiv:2503.14734v2, revised 27 March 2025 02:52:43 UTC (first submitted 18 March 2025). Official author-deposited paper: https://arxiv.org/pdf/2503.14734v2 ; metadata: https://arxiv.org/abs/2503.14734v2 . The complete author list is preserved in `article.html` and `paper.pdf`.

**Paper license: CC BY 4.0**, explicitly linked with `title="Rights to this article"` in archived `article.html`, line 184. License text/deed archived as `license.html`; https://creativecommons.org/licenses/by/4.0/ . This is the paper's license, not the separately licensed model weights or code. Attribution, source URL, license link and adaptation notice are also in PPTX notes. The reconstruction modifies typography/geometry into editable objects; retained photographic pixels are source crops. No author endorsement is implied.

Figure **3, “GR00T N1 Model Architecture,” page 4**. Full page rasterized at PDFium scale 4, 2382×3368 pixels; exact figure crop `[246,334,2137,1320]`, giving 1891×986 pixels. Caption and body prose are outside the figure boundary. All hashes and version metadata are in `provenance.json`; raster-only reproduction in `raster_source.py`. No source-PDF text/vector coordinates or author drawing code was consulted. Tesseract OCR was manually corrected against the opened raster.

## Complete coverage and native boundary

Preserved: camera image and three-line quoted instruction; Vision Encoder and Text Tokenizer; both purple/blue token strips; frozen Eagle-2 VLM and branches to both Cross-Attention sublayers; state `q_t`; input noised-action sequence with subscript formulas; State/Action Encoders; state/action token strips on both sides of DiT; both Cross/Self-Attention pairs, dashed omitted-layer segment, `x N` and DiT Blocks labels; Action Decoder; output action sequence; humanoid/motor label; K-iteration feedback loop; both legends.

Final leaves: **59 shapes, 52 native text objects, 57 native lines/arrows and 2 raster images** (170 leaves, 168 native). Only the observation photograph including its thin source photo border and the detailed humanoid artwork remain raster; no readable diagram labels are baked into those crops. Snowflakes are native line collections, not screenshot icons. Tokens are native colored rectangles. Native formula parts preserve italic variables, upright operators/numerals and explicit lower script baselines.

Fonts chosen from installed files: Arial, Andale Mono for the sans-serif monospaced instruction, Times New Roman regular/italic for math, and explicitly selected DejaVu Sans for vertical ellipses. Original font identity is not established by pixels. Files/hashes appear in `fonts.json`, and no fonts are embedded or redistributed.

## Editing granularity: 35 real groups, 41 top-level objects

`applied_groups.json` contains every member ID and rationale. `recommended_groups.json` preserves the initial proposal. `editability.json` records the actual group tree. PPTX XML contains **35 `grpSp` elements**, and all 35 named groups also exist as SVG `<g>` IDs. Grouping never exempts collision/containment checks.

- `vision_module`, `tokenizer_module`, `state_encoder_module`, `action_encoder_module`, `decoder_module`: module body and readable label lines move together. Labels are whole words/semantic lines, not per-character fragments. Separate lines preserve the source's explicit 34 px baseline spacing; entering the group permits editing a line without changing its sibling. A person wanting to replace the full two-line phrase will edit the two retained text objects.
- `vlm_module` nests its body/labels and `vlm_frozen_icon`, whose 18 native strokes behave as one status symbol. The other snowflake is similarly nested under its legend.
- `dit_block_stack` nests four body+rotated-label sublayer groups, internal connector segments, repeat count and title. One Cross-Attention label remains one rotated editable text box. External VLM and input/output wires stay independently selectable.
- Eight token-strip groups let a person move one semantic sequence without manually selecting 2–9 cells. Cells remain individually editable if needed.
- Each of seven formula groups contains 2–5 styled text parts. Main variable and lower scripts move together; operators and italic variables retain their own styles. These are **not Office equation objects**. Changing script structure or length can require adjusting part offsets. Input/output sequence groups nest their frame, three formula groups and one ellipsis.
- The three-line language instruction, legends, motor output and feedback route are additional semantic groups. The camera photograph remains independently selectable.

Cross-module connectors retain fixed coordinates. Moving a module does not reroute them. The actual move test makes this limitation visible rather than hiding it.

## Actual-render and editing evidence

`build_03` was the visually repaired flat baseline. `group_scene.py` explicitly reordered z to make each semantic group contiguous, retaining source geometry and source-supported layer relationships. **build_03→build_04_flat: 0 changed pixels. build_04_flat→build_05_grouped: 0 changed pixels.** All comparisons used actual exported PDFs at the source width. `group_pixel_audit.json` and both difference rasters preserve the evidence.

Raw PDFium actual raster is 1891×987, due to height rounding. Its row 986 is verified to contain exactly 1891 pure-white pixels in every measured build. Raw `actual_sourcewidth.png` is retained; `actual_sourcecanvas.png` removes only that extra bottom row to match the 1891×986 source. No registration, resampling or translation is applied. `comparison_sourcewidth.png` places source above actual. Full final output and enlarged details were opened and inspected.

Two independent copied PPTX edits are archived in `edit_test/`:

1. Move `state_encoder_module` by **(+35,+20) source pixels**. Recursive native xfrm calculations show its 3 leaves move equally; **all 167 other leaves retain position and text**. Actual render changes 20,538 pixels only within `[480,393,713,540]`.
2. Change editable `state_encoder_label_0` text **State→Joint** using its retained run. All 170 leaf geometries remain fixed; all other text stays unchanged. Actual render changes 1,028 pixels only within `[545,427,612,450]`.

The two edited actual renders were opened and inspected. `edit_test/edit_audit.json` records before/after paths, effective absolute coordinates and deltas for **every leaf**, including all neighbors. These are direct file-edit and LibreOffice-render checks, not claims about mouse/keyboard selection in PowerPoint/WPS.

## Fidelity measurements and remaining limitations

Frozen diagnostic ROIs are in `measure.py`; the threshold remains `max(R,G,B)<150`. Edge differences below are final actual minus source, in source pixels. These measurements are diagnostics, not an aggregate accuracy score.

| Region | Edge Δ [L,T,R,B] | Mask IoU |
|---|---|---:|
| Vision/Encoder | [-1,-1,1,1] | .625 |
| instruction | [1,-1,0,-1] | .467 |
| q_t | [0,0,0,2] | .374 |
| input a_(t+H−1) | [1,0,0,-1] | .180 |
| Cross-Attention | [0,2,0,0] | .570 |
| embodiment legend text | [0,-1,1,-1] | .618 |
| K iterations | [2,0,1,1] | .356 |

Font/glyph differences remain, especially the mathematical subscript H/operators and ellipsis dots. Close bounding boxes do not imply matching glyphs: the final long formula still has low mask IoU. The native token/source-color and fine arrow/dash appearance are approximations inspected against the source. The observation crop includes its thin photographic border, which remains raster together with that image.

The two retained automated warnings are `tokenizer_label_0` measured width 56 px versus actual 52.366 px, and `tokenizer_label_1` 128 versus 123.975 px. They were inspected; no repeated shrinking or threshold relaxation was used to turn review into pass. No runtime correctness bug was demonstrated by this case.

## Attempts and reproducibility

- `author_01_failed.py`: authoring-harness duplicate keyword argument, preserved; corrected locally without runtime changes.
- `build_01`: legitimate preflight failure: ellipsis frame narrower than measured glyph, plus missing VLM-container relationship on its freeze icon. Original report retained.
- `build_02`: fixed frame width and real containment; rendered with two width-drift warnings. Source comparison exposed serif Courier instruction mismatch and math/rotation differences.
- `build_03`: one targeted visual repair: Andale Mono, explicit ellipsis family, adjusted math baselines/scripts, rotated text and legend sizes. No blocking errors. Final residuals retained.
- `build_04_flat` / `build_05_grouped`: z organization and native groups, independently verified pixel-identical. No extra source-fidelity changes.

Run `zsh reproduce.sh` to build the final grouped scene into a fresh `rebuild_01`. It uses the existing repo `.venv`, command-local Homebrew PATH and installed LibreOffice/Supplemental fonts. Source files are `job/scene.grouped.json` and `job/assets/`; final package has `scene.resolved.json`, `scene.original.json`, `svg/`, `assets/`, `fonts.json`, `validation.json`, `editability.json`, actual PDF and comparisons. `author.py`, both repair scripts, `group_scene.py`, `measure.py` and `edit_test.py` preserve the work. No installation, repository modification, push or subagent spawn occurred.
