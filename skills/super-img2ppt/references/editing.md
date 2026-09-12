# Editing granularity and semantic groups

Use the unit the person is likely to edit. An ordinary label should be one text box; mixed
font weights/colors on a common line can use runs. For a same-style multiline module title,
prefer one text object with explicit line breaks and `line_height` when it preserves the
source baselines; separate line objects should have a demonstrated layout need. Separate formula parts only when differing
baselines, angles or styles require it, then group them as one formula. Group a module's body,
label and internal diagram; keep cross-module connections separately selectable. Group the
segments of one curve together, not all curves in a chart. A token's body and label belong
together; repeated tokens may form a nested row. A photo remains an independent image asset.

Groups are native PowerPoint groups, not flattened images. The group ID is its name in the
Selection Pane. Choose meaningful IDs such as `vision_encoder` or `action_noise_formula`,
not generated numbers. Children retain their own names, text runs and editable geometry.
In PowerPoint, select the group to move it; enter the group or ungroup it for individual edits.
Actual click/keyboard behavior can differ across editors and is not asserted by our Linux or
macOS LibreOffice rendering checks.

```json
"groups": [
  {"id": "encoder", "members": ["encoder_body", "encoder_label", "output_formula"],
   "description": "Move the encoder and its internal output equation together"},
  {"id": "output_formula", "members": ["variable", "superscript", "subscript"]}
]
```

This is a slide field. Members reference element IDs or other group IDs. Each belongs to at
most one parent. Group IDs must be distinct from all element IDs, and nesting is limited to
eight levels. Helpers `compose-math` and `trace-curve` emit a ready-to-merge `groups.json` for
multi-part output. Ensure generated IDs are unique across the slide. Single-part outputs
need no extra group.

## Keep stacking intact

A group moves as one unit in the paint stack. All its descendant leaves must form a continuous
range in the scene's stable ascending z order. Noncontiguous grouping fails explicitly: the
exporter never moves intervening objects in front of or behind a module to make grouping work.
The order in `members` does not override z. Author modules with contiguous layers when possible.
If a existing scene needs z changes, make them explicitly, compare flat and grouped actual PPTX
renders, and retain any visual difference for review. Choose smaller meaningful groups if the
original occlusion cannot support a larger one.

`container` is still only a layout/containment relationship; it does not group objects.
Groups do not bypass any geometry, overlap, native-text or actual-font check. Group-only changes
should preserve leaf geometry, styles, text and actual pixels. Native verification recursively
checks children, membership and flattened paint order, so an outer group cannot hide missing text.

## Verify a real editing operation

On a duplicate PPTX, move a representative module or formula as a group and confirm all intended
children move while neighbors stay fixed. Change one label through its retained text run and
confirm siblings remain editable and unchanged. For a long curve, verify one curve is selectable
without selecting other series. Use `editability.json` to inspect root groups, child IDs, remaining
ungrouped elements and counts. Counts describe organization, not an automatic usability score.

Moving a module does not automatically reroute external arrows. Grouped line segments are not
a data-driven chart or a fitted spline. Formula groups are styled text parts, not Office equation
objects. Editing a label to substantially longer text can require resizing its frame; a previous
source-fidelity check does not validate arbitrary future edits. Font files are not embedded.
