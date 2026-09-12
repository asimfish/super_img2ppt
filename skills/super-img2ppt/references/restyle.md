# Optional academic restyling

Activate when the user requests only visual style-field adjustments during conversion.
For inconsistent artwork, distorted typography or an AI-generated look, first read
[redraw.md](redraw.md); these usually require rebuilding elements, not a restyle plan. Do not infer AI origin from appearance. Default conversion
remains faithful. No detection or detector-evasion claims.

Inspect the source and reconstruct a faithful scene first. Inventory labels, numbers,
formula parts, chart curves, arrows, panel order, semantic colors and raster assets.
Choose a restrained palette, consistent ordinary-label typography and stroke weights.
Flatten decorative gradients only after checking they are not data colorbars, shading cues,
or category encodings. Keep semantic color relationships consistent across legends and marks.
Do not rewrite text, fabricate unreadable symbols, delete logos or erase meaningful artwork.

Create a version-1 plan with explicit object IDs and a reason for each change:

```json
{
  "version": 1,
  "changes": [
    {"slide": "page_001", "element": "title", "set": {"font_family": "Arial", "color": "#243247"}, "reason": "Use a consistent ordinary-label typeface and dark ink"},
    {"slide": "page_001", "element": "module", "set": {"gradient": null, "fill": "#EEF3F8", "stroke_width": 1.5}, "reason": "Replace a decorative gradient with a flat module background"}
  ]
}
```

```bash
super-img2ppt restyle JOB/scene.json --plan JOB/style-plan.json --out JOB/restyle_01
```

Allowed fields: plain text `font_family`, `cjk_font_family`, `font_size`, `color`, `bold`,
`align`; shapes `fill`, `stroke`, `stroke_width`, `radius`, `gradient`; lines `stroke`,
`stroke_width`. Only `gradient` accepts null to remove it. Repeated targets are rejected.
Prefer the original authored scene for typography changes: `build` converts even ordinary
labels into `runs` in `scene.resolved.json`. Keep ordinary labels as `text` in the authored
scene; do not flatten formula runs to bypass protection. A resolved scene still supports
shape and line restyling.

Rich text/runs (including formula parts) and images are protected; the command does not
change geometry, topology, content, image crops, grouping or overlap exemptions.
A style plan is authored by the agent; there is no universal automatic “de-AI” filter.
This layer does not fix baked-in raster artifacts. Disclose them or separately reconstruct
supported content as native shapes under the user's requested scope.

Output contains `baseline/` and `refined/`, each with editable PPTX, SVG, font inventory,
editability manifest and normal build validation. Portable `baseline.json`, `refined.json`
and shared assets allow rebuilding. `plan.json` and `restyle.json` record every effective
field change. Original inputs remain untouched. Use a fresh directory for every attempt.

Open both actual PPTX renders. Check small text, formula style consistency, meaningful color
encodings, curves, legends, container spacing and edit groups. A failed build remains a
failure. Successful automated exports still have restyle status `review`; `--no-render`
produces `unverified` drafts. Source similarity is diagnostic only: intentional style changes
must not be reported as improved source fidelity. Deliver both versions and explain remaining
raster regions, deliberate changes and actual checks. Do not claim a universal aesthetic win.
