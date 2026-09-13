# Perceptual color regression — 0.3.12

0.3.11 compared core RGB channels with a default maximum difference of 12; HSV was
only diagnostic. This allowed gray `#606060` → `#6C6C6C` and muted brown
`#807060` → `#747C6C` to pass. These are reproducible blind spots, not attribution
of every user complaint to this cause.

`regression-results.json` records the same samples after the fix. Both now fail
with ΔEOK about 0.0422 and 0.0354 respectively; a one-code gray change passes.
RGB and ΔEOK must both meet their limits. Default ΔEOK 0.02 is a product screening
threshold, not a universal visibility guarantee. Signed lightness/chroma are reported.
No output palette or global saturation is automatically altered.

`retained-dashboard-checks.json` rechecks three explicit target-color patches from
previously downloaded dashboard PPTX renders. All pass with zero ΔEOK. These were
intentional recolorings; this does not certify faithfulness to their original white fills
or the current deployed page. The original retained images and hashes are unchanged.

Conversion equations: [Oklab, Björn Ottosson](https://bottosson.github.io/posts/oklab/).
The author offers the linear-sRGB conversion matrices as public domain. The runtime
has no new dependency. Tests cover primary reference coordinates, symmetry, direction,
quantization, target mode, invalid thresholds and actual PPTX rendering.
Independent forward review additionally checked all 256 gray values, threshold equality,
and both gates independently; no blocking findings (35 non-render cases passed).

Coverage is unchanged: sparse automatic flat-patch checks and manually specified regions.
Thin curves, gradients and ambiguous samples still require dedicated checks and review.

Final validation: 199 tests passed in 144.01 s, including actual LibreOffice renders.
Ruff, package static validation, registry, governance and extracted-package smoke passed.
Package SHA256: `7c293af80942497edb939cc5dcd05d2e2f311f8b1a790088032c41087c807693`.
