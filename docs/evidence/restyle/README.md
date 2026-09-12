# Opt-in restyle verification — 2026-09-13

Runtime 0.3.8 adds an independent command; existing `build` implementation is unchanged.

- Two local cases rendered both baseline and refined PPTX using LibreOffice. All four exports
  pass native-object and rendered-text checks; refined preflight requests source review as
  designed. See [case summary](../../../examples/restyle/evidence.json).
- Decorative fixture is authored for this feature, not a paper figure or an AI-origin sample.
  Title typography, module fill, border weight and radius change. Source geometry, arrows,
  labels and three editable module groups remain intact. Actual previews were visually inspected.
- Routing fixture derives from the existing repository case; eleven explicit fill changes
  preserve teal/gold branch semantics, labels, weights and arrow coordinates. Actual refined
  preview was visually inspected. This is styling evidence, not proof of improved fidelity.
- Independent skill forward test used routing in a fresh temporary directory: two draft
  exports, 87 native objects, no raster or font substitutions. A protected-rich-text mutation
  exited 2 and created no output. New actual render was deliberately not claimed in that test.
- Forward testing exposed the resolved-scene/runs distinction; the usage reference now tells
  callers to use authored plain-label scenes for typography changes.
- Final full local suite: **147 passed in 83.41 seconds**. Fifteen new targeted tests cover
  copies, field audit, protected content/geometry/runs, invalid
  style values, duplicate targets/JSON keys, no-op plans, gradient removal, groups/line geometry,
  output reuse, confined assets, dual draft exports and failure propagation.
- Extracted distribution smoke test: [package.json](package.json). No installation or host
  registry changes. Ruff, package metadata/reference and governance checks pass.

No native PowerPoint/WPS UI validation or broad aesthetic success claim is made. Existing
complex-paper gallery inputs and outputs remain frozen. Raster artwork is unchanged by this mode.
