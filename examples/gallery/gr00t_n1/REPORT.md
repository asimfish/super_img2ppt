# GR00T N1 — complete architecture with atomic editable labels

**Final: `build_09_merged_grouped/editable.pptx`**, using `job/scene.merged_final.json`. The complete Figure 3 now has **34 real native groups and 161 leaves: 59 shapes, 43 text boxes, 57 lines/arrows, 2 raster images**. It presents 41 top-level selectable objects. Six two-line module names, Motor Action and the complete three-line instruction are each **one native text box**, reducing text objects by 9 without changing a single actual-render pixel from the reviewed earlier version.

Automated status remains **review**, with no blocking errors and one retained Text Tokenizer width-drift warning. Actual PPTX rendering and direct file edits were tested with LibreOffice; native PowerPoint/WPS UI behavior is not asserted. The old `build_05_grouped`, `edit_test/`, `REPORT_premerge.md`, `provenance_premerge.json` and original group proposal remain intact.

## Source, license and completeness

NVIDIA; Johan Bjorck, Fernando Castañeda, Nikita Cherniadev et al. *GR00T N1: An Open Foundation Model for Generalist Humanoid Robots*, **arXiv:2503.14734v2**, revised **27 March 2025 02:52:43 UTC**. Official author-deposited paper: https://arxiv.org/pdf/2503.14734v2 ; metadata https://arxiv.org/abs/2503.14734v2 . The complete author list is preserved in `article.html` and `paper.pdf`.

**Paper license CC BY 4.0**, explicitly linked with `title="Rights to this article"` in archived `article.html`, line 184; https://creativecommons.org/licenses/by/4.0/ is archived as `license.html`. This is the paper license, not code/model licensing. The PPTX notes credit the authors, source and license and state this is a modified reconstruction; no endorsement is implied.

Full **Figure 3 “GR00T N1 Model Architecture,” page 4**. PDFium scale 4 yields 2382×3368 pixels; crop `[246,334,2137,1320]` yields **1891×986**. Only caption/prose outside the figure boundary is excluded. PDF and image hashes, URLs, version and crop are in `provenance.json`; `raster_source.py` reproduces the raster without using PDF text/vector APIs. Reconstruction used visible raster plus locally corrected Tesseract OCR, never source PDF text/vector coordinates or author drawing code.

All figure components remain: camera/instruction; vision and language tokenization; frozen Eagle-2 VLM and two attention branches; state and action encoders; full input/output action-sequence formulas; token strips; all four Cross/Self-Attention sublayers and omitted-layer dash; decoder; humanoid output; iteration feedback; legends. Only the camera photograph including its thin source photo border and the detailed humanoid artwork remain raster. No readable diagram labels are baked into these two crops.

## Editing units and exact group membership

`applied_groups.json` and final `editability.json` list every group, member ID and rationale. All **34 groups exist both as PPTX `grpSp` and named SVG `<g>` objects**. Grouping does not bypass QA.

- `vision_module`, `tokenizer_module`, `state_encoder_module`, `action_encoder_module`, `decoder_module`: body plus **one complete multiline label**, e.g. `state_encoder_label` contains `State\nEncoder`. Its font/align/manual newlines are explicit. A user can edit the full module name in one text box. `vlm_module` similarly contains one Eagle-2/VLM label plus a nested freeze-status symbol.
- `dit_block_stack`: full composite panel with nested Cross/Self-Attention module groups, internal links, repeat count and title. Each rotated attention name remains a single text box; external incoming/outgoing arrows remain independently selectable.
- Eight token-strip groups provide sequence-level movement, while individual rectangles remain editable on entry into a group.
- Seven formula groups keep each mathematical quantity's 2–5 styled text parts together. Lower script baselines, italic variables and upright operators remain editable. These are styled native parts, **not Office equation objects**; changing the script structure/length may require adjusting offsets. Input/output sequence groups include their frame, formulas and ellipsis.
- `instruction_text` is now one complete three-line text object. The Motor Action label is one two-line object within `motor_output`. Snowflake line collections, legends and feedback segments are semantic groups. The camera photo remains independent.

Native grouping enables coherent movement, not automatic connector rerouting. The move experiment visibly preserves external arrows at their original coordinates, so a layout edit can require reconnecting them.

## Bounded label merge: actual evidence, no fidelity relaxation

A first State Encoder candidate (`build_06_state_merged`) used one box, `line_height=34/29`, centered alignment and the original first-line origin. It preserved line spacing but shifted both rendered lines down by **0.312 pt ≈ 0.614592 source pixels** in LibreOffice, producing 1,841 changed pixels. This was measured from the **generated actual PDF**, not from source-PDF text. A single y-origin compensation of −0.615 px (`build_07_state_adjusted`) yielded **zero changed pixels** versus old build 05.

The same bounded procedure was applied to six module names, Motor Action and the three-line instruction. `build_08_all_merged` is the uncompensated candidate. `merge_all_baseline_audit.json` records each line's first-character actual-PDF box and the measured common shift. Explicit source line intervals are 33 or 34 px for module names, 34 px for Motor Action and 29 px for instruction. Common-origin corrections range from about **+0.392 to −1.395 px**; the maximum within-label line-shift discrepancy was only 0.002 px from PDF rounding. No font sizes, content, alignment or measurement thresholds were changed for merging.

After the one measured-origin correction (`build_09_merged_grouped`):

- **Old reviewed build 05 → final merged build 09: 0 changed pixels across the full actual raster.** `merge_all_pixel_audit.json`.
- **Final grouped build 09 → final flat build 10: 0 changed pixels.** `merge_final_flat_group_pixel_audit.json`.
- Earlier premerge z-organization and flat/group audits remain preserved separately in `group_pixel_audit.json`.

This empirically resolves the initial over-fragmented multiline labels. Explicit `line_height` does support single-box editing here; it required an observed renderer-origin correction rather than assuming the old first-line frame origin could be reused unchanged.

## Final real editing tests

Independent copied final PPTX files and actual LibreOffice renders are in **`edit_test_merged/`**. `edit_audit.json` records parent paths, effective absolute xfrm coordinates, text and deltas for every one of the 161 leaves.

1. Move `state_encoder_module` by **(+35,+20) source pixels**: its body and one complete label move together; **all other 159 leaves keep their coordinates and text**.
2. Edit the complete single native text box **`State\nEncoder` → `Joint\nEncoder`** through its retained paragraph run, preserving styling and the second line. No other text changes; **all 161 leaf geometries remain fixed**. The result still contains one label text box, not two independent label fragments.

Both edited actual renders were opened and inspected. Local before/after previews are `moved/edit_comparison.png` and `label_edited/edit_comparison.png`; exact pixel change bounds are in each `pixel_difference.json`. Old three-leaf module editing evidence remains under `edit_test/` and is clearly superseded for the final label organization.

## Actual raster recipe and residual quality

Raw actual PDFium output is **1891×987** because of height rounding. Every measured build's last row (index 986) was verified to be exactly 1,891 white RGB pixels. Preserve raw `actual_sourcewidth.png`; `actual_sourcecanvas.png` removes only that extra white bottom row to match source 1891×986. No resizing, translation or registration is applied. `comparison_sourcewidth.png` places source above actual; `detail_comparison.png` provides enlarged isolated regions. The final source comparison is unchanged pixel-for-pixel from the reviewed premerge baseline.

Installed fonts: Arial, Andale Mono, Times New Roman regular/italic, explicitly selected DejaVu Sans for vertical ellipsis. Original font identity is not established from pixels, and glyph differences remain; fonts/hashes are in `fonts.json`, with no font embedding/distribution.

Frozen source-v-actual diagnostics from `measure.py` remain unchanged after merging:

| Region | Edge Δ [L,T,R,B], source px | Mask IoU |
|---|---|---:|
| Vision/Encoder | [-1,-1,1,1] | .625 |
| instruction | [1,-1,0,-1] | .467 |
| q_t | [0,0,0,2] | .374 |
| input a_(t+H−1) | [1,0,0,-1] | .180 |
| Cross-Attention | [0,2,0,0] | .570 |
| embodiment legend | [0,-1,1,-1] | .618 |
| K iterations | [2,0,1,1] | .356 |

These diagnostics are not an aggregate accuracy score. Long-formula internal glyph/spacing differences remain despite close edges; no exact source-fidelity claim is made. The one final warning is `tokenizer_label`: measured width 128 px versus rendered 123.975 px. Old build 05 had two per-line warnings; merging naturally yields one max-width warning, not a check exemption or altered threshold.

## Files and reproducibility

Run `zsh reproduce.sh` to rebuild final `job/scene.merged_final.json` with existing fonts/runtime into a fresh output directory. Final deliverables are `build_09_merged_grouped/{editable.pptx,scene.resolved.json,scene.original.json,svg/,assets/,fonts.json,validation.json,editability.json,render/}` plus full/source/detail previews. Source recipe, original authoring and bounded repairs remain in `raster_source.py`, `author.py`, `repair_01.py`, `repair_02.py`; grouping and label improvements are reproducible from `group_scene.py`, `merge_labels.py`, `measure_merge_baselines.py`, `adjust_merged_labels.py`, `edit_test_merged.py` and `measure.py`.

Failed/intermediate attempts and earlier evidence are retained. Initial preflight fixes were a too-narrow ellipsis frame and its legitimate container relationship; the authoring script's duplicate-keyword failure is also retained as a harness error. No runtime correctness defect was demonstrated. No runtime/repository modification, installation, push or subagent spawn occurred.
