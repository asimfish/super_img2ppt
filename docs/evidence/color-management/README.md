# Color management regression (2026-09-13)

The previous input normalizer converted channel modes without applying embedded ICC profiles.
For DCI(P3) `(80,150,180)`, it retained those channels instead of the reference sRGB
`(35,139,174)`. This demonstrates a reproducible color error, not a diagnosis of every user report.

`profile-results.json` records nine local checks across Display P3, Adobe RGB and DCI(P3).
New output exactly matches the Pillow/LittleCMS relative-colorimetric reference transform.
Only profile names and hashes are retained; no system ICC files are distributed.
These checks verify use of the color transform, not independent display calibration.

Portable regression tests cover LAB ICC input, invalid/missing profiles, RGB stability,
alpha and palette transparency, and the shared PPTX/SVG raster encoder.
Real LibreOffice builds check that a source `#087887` reconstructed as `#1F6F78`
fails by default without an appearance plan, and matching color remains review pending
whole-figure inspection. Intentional redesign is explicitly separate.

Automatic selection is sparse flat-patch screening. Curves, text, gradients, screenshots
without ICC metadata, and other Office viewers still need appropriate reference regions
and visual review. HSV diagnostics are not perceptual ΔE. No global saturation boost is used.

Validation: full suite 181 passed in 121.21 s (including actual Office renders).
Subsequent transparency fixes: all 11 color-management tests passed, including three
additional tRNS/gray-alpha cases; actual system gray ICC + LA produced `(128,128,128,100)`
with alpha preserved and RGB matching the reference transform. Independent forward review
identified these cases and checked 29 non-render cases. Ruff, skill static validation,
capability registry, governance audit and extracted-package runtime smoke passed.
Package version: 0.3.11; SHA256:
`ce0b3cf56daa19a8437d3690d5e0d0632a13e3275a0c9a864d0e1183890ff687`.
