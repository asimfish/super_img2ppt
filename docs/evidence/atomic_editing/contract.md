# Editing granularity acceptance

Add two complete licensed recent embodied/world-model figures and explicitly authored semantic
edit groups. Keep full labels as single text boxes/runs where feasible; split math only for required
style/baseline differences and keep its parts together. A module, repeated token, formula, curve or
illustration-with-caption is a useful selectable group; grouping the whole slide is not a substitute.

Current container has only layout/QA semantics; native export is flat. Add optional slide groups
independently of container. Leaves retain coordinates, IDs, styles, paint order and editability.
Nested native PPTX groups and SVG groups; safe membership validation, unique parent, no cycles,
bounded depth, existing IDs only. Reject groups whose leaves interleave ungrouped/other leaves
in paint order rather than silently changing occlusion. Scene authors may explicitly reorder only
after full-source/actual inspection; exporter never guesses semantic groups or suppresses QA.

Verify flat-versus-grouped actual rendering is unchanged, native hierarchy/leaf count/text survive,
a group moves all descendants while leaving neighbors fixed, and a child label can be edited
without modifying others. Compare published real-case before/after actual render and independently
perform meaningful edit operations. No claim of native PowerPoint/WPS UI testing or automatic
connector rerouting. Existing 15 published cases remain frozen; new cases demonstrate groups.
