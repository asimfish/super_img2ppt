# Appearance gate verification — 2026-09-13

## Recovered task and deployed correction

The prior session read 100 visible messages, IDs 13627434–13658080, plus two tool details.
This continuation read 15 newer visible messages through ID 13660367 and two further tool
records. No internal/platform history or credentials are stored here. Read-only SSE reported
idle before implementation began. The last message said figures 3/5 had been re-rendered and
published with the author's newly requested richer palette. No competing edits were made to
that agent's project or deployment.

The original defect used shared #1F6F78/#B8862B scene constants instead of source-specific colors.
Geometry validation did not test this; lighter strokes and smaller type also changed perceived
weight. Later author requests explicitly changed the target from source matching to enhanced
palette, so current differences from the original S5 image are intentional.

Read back the deployed SVG and embedded actual-render JPEG previews. Downloaded the deployed
PPTX files and independently rendered them locally with LibreOffice. Three isolated flat
regions in those new renders match the recorded target RGB exactly: figure 3 warm hypothesis
fill, figure 5 teal hub, and figure 5 cool-gray card. See [live-local-pptx-checks.json](live-local-pptx-checks.json)
and [live-readback.json](live-readback.json). This is selected-region validation, not full-page
font, layout, or aesthetic acceptance. The hosted page remains authored/deployed by the
original agent. No source/PPTX files or third-party artwork are redistributed here.

One first JPEG sampling region crossed heading glyphs and correctly failed as mixed. Visual
inspection moved the region left into the empty panel fill; thresholds were unchanged. The
three corrected JPEG measurements differ from target by at most one channel unit. Local PPTX
renders eliminate that JPEG difference in the selected solid regions.

## Runtime evidence

- Full local suite: **169 passed in 137.55 seconds**, including 22 new appearance tests.
- Actual PPTX example with correct color/weight passes. Same scene with shared-palette fill
  and half-width line fails for `color_drift` and `ink_density_drift` respectively, despite
  passing native/geometry checks. [regression.json](regression.json)
- Example inputs are independently authored: [scene](../../../examples/appearance/scene.json),
  [plan](../../../examples/appearance/plan.json), [source](../../../examples/appearance/source.png).
- Existing source-backed builds remain compatible but no longer report overall pass without
  an appearance plan. No-render drafts retain not_run and unverified. Failed sampling blocks.
- Independent forward testing found that unequal source/actual ROI sizes could conceal thinner
  ink. Equal dimensions are now enforced and covered by a regression test. Mixed-hue regions
  reject; same-hue clutter remains a documented isolation limitation.
- Package smoke test unpacks the distributable, uses existing dependencies, and builds the
  example through the actual-PPTX appearance gate. [package.json](package.json)
- Ruff, package references/frontmatter, registry drift and deterministic governance checks pass.
  No runtime dependency or external-service behavior was added.

## Remaining boundaries

No claim of zero future errors. Agent-selected ROIs, default RGB thresholds, uniform-background
ink estimation, target approval provenance and semantic color mappings still need judgment.
Same-hue clutter can compensate missing stroke mass; gradients and tiny antialiased strokes
need isolated evidence. Missing coverage is reported rather than treated as color acceptance.
The original agent's frozen environment was not remotely upgraded: future use must load the
updated skill/runtime from this repository. Version 0.3.10 does not retroactively validate
previously produced files. Native PowerPoint/WPS compatibility is separate.
