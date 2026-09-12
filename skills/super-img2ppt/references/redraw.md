# Optional semantic redrawing

Use this mode when the user asks to remove an AI-generated look from an editable conversion,
especially mismatched clip art, soft pseudo-vector edges, distorted typography, implausible
small geometry, inconsistent perspective or diagrams that look assembled from unrelated assets.
Do not equate this request with minimalism. Preserve the user's desired visual richness and
technical information. Appearance alone does not establish how an image was made.

## Choose the scope from the actual image

Open each source and describe concrete regions and symptoms. A global palette or font swap
cannot correct baked-in drawing defects. The lightweight `restyle` command is suitable only
when the request is limited to existing style fields. It deliberately cannot replace images,
rebuild formula parts or move objects. For semantic redrawing, author a separate scene and use
the normal `check`/`build` commands. Do not claim a nonexistent automatic redraw command.

Keep a faithful baseline and a separate `redrawn/` job. Record source objects/regions, replacement
objects, preserved meaning and the reason for each change in `redraw-changes.json`. This is a
review record, not a schema-validated assertion of semantic equivalence.

## Preserve information; change the drawing construction

- Inventory every panel, label, formula, number, matrix dimension/value, legend category,
  arrow direction, curve and meaningful visual cue before editing. Compare against captions
  when supplied; record disagreements instead of silently replacing source content.
- Replace inconsistent decorative icons with a coherent native vector vocabulary. Preserve
  their referents: a bridge remains a bridge, an agent remains an agent. Do not replace a
  technical apparatus, photograph, logo or scientifically meaningful shape with a generic icon.
  Real photos/measurements stay original unless the user separately requests a transformation.
- Rebuild matrices and tables with shared cell geometry and stroke rules. Preserve all values,
  dimensions, highlighted cells and ellipses. Flatten perspective only when it is decorative;
  orientation may carry tensor/3D meaning. Do not invent missing values.
- Retypeset prose using actual font metrics, without stretching glyphs to fit old boxes.
  Formula reconstruction can change fonts, baselines and grouping while retaining the complete
  expression, indices, hats, operators and mathematical styles. Use `compose-math` for measured
  parts; never apply a plain-label font change indiscriminately to mathematical runs.
- Keep measured plots and traced curves. Do not smooth, replace or invent data to make a chart
  attractive. Distinguish a conceptual schematic from measured results, and retain that status.
- Rebalance local frames and spacing where new typography needs it. Preserve reading order,
  graph connectivity, annotations and information density. Update affected connectors
  explicitly; the runtime does not reroute them automatically.
- Group icons, formulas and modules at the unit the user will edit. Keep curve series and
  external connectors separate. Grouping does not waive collision checks. Preserve line caps,
  endpoints and intended joins while eliminating accidental near-tangencies.

## Verify two different contracts

Build the baseline and candidate in fresh directories with actual PPTX rendering. Existing
font, native-object, glyph and overlap checks apply to both. Inspect the original, baseline
and redrawn previews together at full scale and at changed regions. Verify content coverage
and mathematical meaning separately from appearance; a pixel similarity score is not an
acceptance criterion for intentionally redesigned regions.

Check icon consistency, legible text, formula baselines, matrix geometry, meaningful colors,
arrow endpoints, local spacing and the editability of representative groups. Keep a region
marked unresolved if the underlying evidence is unreadable. A successful export is not proof
that viewers will judge the image less AI-like. Deliver the baseline and candidate with the
change record and specific remaining visual limitations; preserve user source privacy.
