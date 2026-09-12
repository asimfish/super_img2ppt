# Cosmos 3: semantic editability forward test

The grouped deliverable is `grouped_01/editable.pptx`, with `scene.resolved.json`, `assets/`, `fonts.json`, SVG and validation in the same directory. All 415 existing leaves remain: 188 text objects, 198 shapes, 28 lines and one text-free brace image. The archived source figure, license, attribution and crop provenance are inherited from the frozen Cosmos 3 gallery case; this task introduced no source reconstruction or font substitution.

## Editing granularity

The slide has **37 root-selectable objects**, down from 415: **21 root groups** plus **16 independent objects**. There are **81 groups total**, counting nested groups. This is not one whole-slide group.

| Semantic unit | Number of groups | Why it is useful |
|---|---:|---|
| Repeated-transformer brace and ×L annotation | 1 | Move recurrence annotation without separating its symbols. |
| Five encoder/tokenizer modules | 5 | Each body and complete label moves together. |
| Individual token bodies and native label/script parts | 29 | Edit or move one token without detaching its scripts. |
| Input/output token rows | 4 | Move a row as a unit, then enter it to edit one token. |
| Subsequence bracket and heading | 2 | Keep each bracket with the text it annotates. |
| LayerNorm and MLP modules | 6 | Each box and ordinary text label is an atomic module. |
| Shared attention module and its two nested formulas | 3 | Move the entire operator, or independently move one complete styled formula. |
| Attention-mask panel and nested grid | 2 | Move the panel; select its 144 cells and dividers as one grid when needed. |
| Query/key and row formula symbols | 9 | Keep main variables, tildes and scripts together. |
| Attention-mask legend entries | 2 | Each swatch stays with its label. |
| Multipart diagonal header formulas | 10 | Preserve common-angle token/script or three-dot relationships. EOS/BOG remain ordinary single text boxes inside the panel. |
| Token-category legend and nested entries | 8 | Move the complete legend or edit one of its seven categories. |

The 16 independent root objects are two tower backgrounds, ten vertical inter-module arrows, two dashed cross-panel expansion lines and two role labels. Cross-module arrows intentionally stay independently selectable. Moving a group does **not** reroute these arrows or preserve endpoint attachment automatically. Matrix-internal arrows move with the matrix panel.

## Paint order and actual fidelity

The original scene appended attention formulas and some query/header parts at the end of the paint stack. Native groups require contiguous descendants, so the task explicitly moved formula parts beside their attention module, moved the noisy vision-row tilde beside its other formula parts, and placed diagonal labels within the matrix panel before the lower legend. All z values were normalized; every changed z is recorded in `z_changes.json`. No leaf geometry, text, styles, assets or other properties changed.

Three real PPTX files were rendered through LibreOffice: the archived **original published PPTX**, a flat scene with the explicit z changes, and the grouped scene. Their PDFs were rasterized directly to **1400×625**, the source resolution. Published-versus-flat, published-versus-grouped and flat-versus-grouped each have **0 differing RGB pixels**. No registration, image alignment, threshold tolerance or resizing was used. This demonstrates unchanged appearance in this renderer for the grouping/z change; it does not establish that the older source reconstruction is pixel-perfect.

Evidence: `group_pixel_audit.json`, `published_actualsourcewidth.png`, `flat_reordered_actualsourcewidth.png`, `actualsourcewidth.png`, `published_vs_grouped.png`, and `source_vs_grouped.png`. The grouped full actual render was opened and inspected. Original source typography differences and existing diagonal-glyph visual-review boundaries remain unchanged. `grouped_01/validation.json` is review, with preflight/native checks passing and no new blocking errors.

## Real editing operation on a duplicate

`edited_operation.pptx` is an explicitly modified test copy, not the faithful grouped deliverable. The operations used the actual native PowerPoint group objects through python-pptx:

1. Move `reasoner_input_norm` left by 16 source pixels.
2. Move nested `full_attention_formula` down by 8 source pixels.
3. Change child `arlabel1` from **Layer Norm** to **RMS Norm** through its retained single text run, keeping its formatting.

The reopened PPTX's composed group transforms confirm that exactly **22 intended leaves** moved: two module children and twenty formula parts. Observed translations differ from requested values by less than 0.00005 source pixels due to integer EMU rounding. The only changed leaf XML is the edited label; **414 of 415 leaf XML nodes are byte-identical**. All other group transforms, all group membership, all unedited leaf dimensions and all neighboring positions remain unchanged. Both moved groups retain their complete children. No blocking assertion failed.

The edited PPTX was actually rendered, and its full image and module/formula detail crops were inspected. There are **4,691 changed pixels**, entirely within the two declared old/new edit-region unions; **0 changed pixels outside those regions**. The unchanged external arrow is visibly no longer centered on the translated module, illustrating the documented attachment limitation.

Evidence: `operation_verification.json`, `edited_render_verification.json`, `edited_actualsourcewidth.png`, `before_after_edit.png`, `module_old_new_union_operation_detail.png`, `formula_old_new_union_operation_detail.png`, and `edited_render/edited_operation.pdf`.

## Scope and limitations

No conversion-runtime defect was reproduced in this case. The first grouped build and edit operation passed; there were no failed repair iterations to hide. No font or dependency was installed, no repository file was edited, and nothing was externally published. The use of a script to manipulate native groups verifies group structure and actual output, not interactive click/keyboard ergonomics in PowerPoint/WPS. Deep nested token/formula groups require entering a group or using the Selection Pane. Larger replacement labels may need frame resizing; this test only exercises a similarly sized label.

The 144 matrix cells remain separate editable leaves inside their grid group, not an Excel-backed chart. Formula groups remain styled native text parts, not Office equations. The curved recurrence brace remains one movable text-free raster asset. Existing fonts are still required on the editing machine.

## Reproduction files

`group_scene.py` creates the grouping and explicit z audit from the archived published scene; `compare_renders.py` checks the actual PDF rasters; `edit_operation.py` performs and asserts the native editing actions; `verify_edited_render.py` checks their actual rendered impact. These evaluation scripts retain their original temporary root; change that root if relocating them. The final resolved scene and sibling assets rebuild independently into a new directory using the existing runtime. `rebuild.sh` supplies that command. Font files are not distributed.

The resolved-scene rebuild was executed successfully: `rebuilt_fresh/validation.json` again reports review with no blocking errors; its actual rendering and editability manifest are retained. The z audit contains 276 numeric z changes, including normalization; this is not 276 geometry changes.
