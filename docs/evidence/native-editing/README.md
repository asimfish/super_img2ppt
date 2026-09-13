# Native editing regression — 2026-09-14

A user-supplied Consistency Policy reconstruction used the 0.2.0 runtime and contained
61 visible pictures, including tensor arrays, U-Net columns and formulas. The local source
is an AI-generated explanatory figure, not a certified copy of the paper's original figure.
The source scientific limitations were retained, not silently corrected.

54 pictures were replaced: 162 independent cuboid groups (three editable native faces each),
42 Office equations and supporting native text, totaling 222 native items. Seven pictures
remain: four photos, a denoising arc, a paired brace and a pose-axis illustration.
`case-audit.json` records source/output hashes, XML counts, unique shape IDs, and three
selected face-color checks against the actual Office render (all RGB deltas zero).
This is selected-region evidence, not a full-page color/geometry or scientific acceptance.
The local enhanced artifact is build_05; the original build_02 remains unchanged.
No user source image or paper/PPTX binary is redistributed with this evidence.

Regression tests verify source-hash binding, unchanged input, object order, unique IDs,
actual OMML scripts/accents/fractions/radicals, preservation on PPTX reload/save, invalid
plans, name conflicts, recursive residual-image reporting, theme-effect suppression and
actual LibreOffice rendering. Independent forward review reproduced namespace/name and
nested-picture reporting gaps, now covered; unsupported line input was removed rather
than implying a general path editor.

Full suite: 208 passed in 106.83 s. Ruff, static skill validation, registry, governance and
extracted-package equation smoke passed. PowerPoint/WPS editing was not run; equation
font availability and final source/actual appearance still require review.
Package 0.3.13 SHA256: `cc070e6b07cdd0169e124154f122314ed7d14cb246296189721d43d0f02a7d36`.
