# RoboDream Figure 2 — complete figure and editing-granularity forward test

**Final delivery:** `full_job/build_13_grouped/` contains actual editable PPTX, SVG, resolved/original scenes, assets, fonts, validation and editability manifests. Automated status is **pass**. Source visual fidelity remains reviewed with explicit differences below. The matching flat baseline is `full_job/build_14_flat/`.

## Provenance and complete coverage

Junjie Ye et al., *RoboDream: Compositional World Models for Scalable Robot Data Synthesis*, arXiv:2606.02577v1, submitted June 1, 2026; current version verified September 12, 2026. Official PDF page 3, complete Figure 2 architecture above its caption. Original paper license was verified through arXiv's paper-specific license link: CC BY 4.0. Archived `arxiv.html` and `license.html`; exact PDF/source SHA-256, URLs, attribution and modification notice are in `provenance.json` and PPTX notes. No code-repository license was substituted for paper rights.

PDFium rendered page 3 at scale 4. Exact final crop [264,192,2180,1100] gives 1916×908. An initially bad crop clipped Rendering and Object prior; `source_initial_bad_crop.png` and the initial prepared job are retained as failed intake evidence. The full figure was recropped before authoring. Final source includes all four visual inputs, robot trajectory input, both top conditioning branches, four 3×3 latent grids, two stacked multiview token columns, Concat & MLP, object MLP, DiT, decoder, instruction and generated demonstration. Caption outside the figure is retained on the PDF page but not redrawn as diagram content.

Only raster source pixels and local macOS Vision OCR were used. No original PDF text/vector-coordinate extraction, author drawing code, generated lookalike art or online OCR. Eighteen complete readable labels/prompts are native text boxes; multiline module names remain one textbox. No label was fragmented into characters. No formula occurs in this figure. Six decorative ellipsis dots are simple native shapes.

## Atomicity and actual editing test

There are 232 leaf objects: 18 text, 81 shapes, 128 native lines and 5 images. The 27 native semantic groups (including one nested curve group) reduce the top-level selection units to 48. `semantic_groups.final.json` lists every group, exact member IDs and reason; the current scene groups implement that proposal. Major modules keep background and full label together; every 3×3 tensor grid is one group; each encoded-token column is one group; each traced curve contains its own line segments and arrowhead, independently of every other curve. The trajectory input combines its frame, label and nested curve. Cross-module straight arrows remain separately selectable.

Five raster assets are limited to independent noise, rendered robot motion, scene prior, object prior and generated demonstration artwork. They have native readable labels. Curves, diagram containers and token grids are native. Gradient tokens approximate the source's diagonal blend with a supported horizontal blend; that visible limitation is not hidden with rasterization.

The original flat scene was explicitly reordered to make semantic groups contiguous in z. Actual PDFium source-width renders before/after that reorder had **0 changed pixels**, as recorded in `measurements_before_lineheight.json`. Final flat/grouped actual PPTX renders also have **0 changed pixels**. Grouping does not change source geometry, typography or layer appearance.

On a duplicate of the final actual PPTX (`edit_probe_final3/edited.pptx`), a Python-pptx edit moved the native nested `group_trajectory_curve` 12 source pixels right and changed the complete retained encoder text run from `Encoder` to `Encode`. All curve children retained their original local coordinates and XML; the group offset moved them together. Only `encoder_label` changed among leaf XML. LibreOffice exported the edited PPTX; its actual source-width rendering changed 3,722 pixels, all inside two predeclared curve/label regions. Pixels outside them were unchanged. Operations and intended group children are recorded in `edit_probe_final3/operations.json`; the rendered result was inspected.

This establishes useful structure and a real saved-document editing operation, not a claim about PowerPoint/WPS click/keyboard UX. Compared with a flat scene, the current grouped output is materially easier to select and move. The remaining 22 ungrouped root leaves include cross-module arrows, stacked-card backgrounds and decorative dots. External connectors do not reroute when modules move; traced curves remain grouped line fragments, not a spline with control handles or a data-linked chart. Arbitrarily longer labels may require resizing.

## Actual source fidelity

LibreOffice actual PPTX → PDF, then PDFium scale `1916 / actual PDF page width`. Exact point sizes, raw dimensions and row-cropping flags are recorded in `measurements.json`. A sole extra bottom row is removed only if every channel is white. No registration, aspect-ratio distortion or threshold relaxation. Full source/actual and enlarged projector, instruction, DiT, curve and concat regions were inspected.

Final fixed-ROI dark/white/gray ink results:

| Region | Edge delta [L,T,R,B] px | Ink IoU |
|---|---|---:|
| Trajectory projector | [0,0,1,0] | 0.437 |
| Instruction | [-2,0,-1,0] | 0.402 |
| DiT label | [-3,0,3,0] | 0.184 |
| Trajectory curve | [0,0,-2,0] | 0.878 |
| Concat & MLP | [1,-1,-1,0] | 0.292 |

Text baselines/line breaks are now close in these regions, but Arial has a different glyph design from the source's geometric sans serif. DiT text demonstrates particularly clearly that matching edges/baselines does not imply matching glyphs. Courier New approximates the instruction's typewriter face. Module corner radii and native arrowheads differ slightly; gradients are horizontal instead of diagonal; source artwork remains subject to office raster resampling. Color and geometry are manual pixel-based approximations. This is a usable editable reconstruction and successful grouping test, not a pixel-exact showcase.

## Failures, repairs and independent limitation evidence

Four initial trace-curve runs rejected arrowhead/neighbor-edge ambiguity. ROI tightening excluded filled arrowheads and neighboring input borders without increasing tolerance or bridging hidden crossings. Second traces succeeded; their magenta overlays were inspected. The source arrowheads and short endpoint joins were added natively. Every failed/successful trace directory remains available.

Initial build 01 stopped narrow Object prior/Rendering frames and undeclared source curve/background overlaps. Build 02 still missed Object prior's 0.5px rendering reserve. Build 03 corrected it and passed preflight/native checks, but blocked actual font identity. A transient author script error meant build 04 repeated that scene; this is retained and not counted as a successful repair. Build 05 explicitly requested Avenir Book but still measured Avenir.ttc Book and exported Avenir-Roman. Build 06 chose supported Arial and passed. Builds 07/08 establish visually identical reordering/grouping. Builds 09/10 apply source-based multiline spacing; builds 11/12 apply its measured origin correction. Same-region repair budgets were bounded and no check thresholds were lowered.

The **Avenir subfamily issue** is independently reproducible with one text object: `font_subfamily_repro.json` and `font_subfamily_repro_build/`. Explicit request Avenir Book resolves locally to Avenir TTC face 0, but final exported PDF uses Avenir-Roman, causing renderer_font_substitution. Measured family is Avenir, so the narrower face request may be lost at export. This is an evidenced font-selection boundary; diagnosis of the underlying runtime/LibreOffice cause is left to the parent integration task. Do not remove the blocking font check to accept it. Arial avoids the mismatch but sacrifices source glyph fidelity.

## Rebuild and evidence

`repro.sh NEW_OUTPUT` rebuilds the final grouped resolved scene with existing fonts and repository venv. No fonts are embedded or redistributed. `author.py`, repair scripts, group_scene.py, trace directories, every build, final flat baseline, original and edited actual PPTX/PDF, OCR, fixed measurements, source comparison and source hashes are retained. No repository edits, installs, pushes or delegated subagents were performed in this test.

Parent full-figure review caught a real missing 9px upper endpoint on Rendering: tightening the body-trace ROI had omitted the visible connection to the trajectory frame. A separate 8×9px source ROI was traced into two native segments (`render_start_0`, `render_start_1`), visually checked and added to the same curve group. Builds 13/14 preserve the final correction and flat/group parity. This demonstrates why successful isolated tracing must still be inspected in the full figure. No hidden path was invented.
