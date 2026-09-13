# Native formula typography calibration — 2026-09-14

The same OMML expression, declared at 24 pt in boxes of widths 2–5 inches and equal
height, rendered at the same 46.057 pt vertical font size but increasingly stretched
horizontally in LibreOffice. Disabling text autofit did not remove the distortion.
Declared fonts also substituted; this change does not certify exact font identity.

The fix reads intrinsic math aspect ratios from a temporary ODP import and glyph sizes
from the actual draft PDF, preserves each equation center and adjusts its native frame,
then renders the final PPTX again. It does not replace Office equations with pictures.

User case build_07: 42 original equation token sequences retained, 286 non-math top-level
objects XML-identical to build_05. Main formulas use 24 source pixels, auxiliary labels 20.
Final maximum measured glyph size per equation is within 0.238 source pixels of target.
`case-audit.json` records measurements and the final artifact hash. User artwork is not
redistributed. Actual LibreOffice preview was inspected; other Office viewers not tested.

Regressions cover identical formula size/aspect despite differing crop boxes, invalid
measurements and ignoring non-target chart objects. Full suite: 213 passed in 163.78 s.
After independent review, added chart isolation/missing-metrics handling: five math-layout
unit cases passed and the actual-render invariance case was rerun separately.

Limits: one-pass estimation uses maximum glyph size inside the original frame. Overlapping
text or enlarged symbols can contaminate it; report stays review. Final visual/isolated
size checks remain necessary. Font fallback and other-viewer typography are not fixed by
geometry calibration. Source alignment/neighbor collisions are not certified by aspect ratio.

Package 0.3.14 SHA256: `291a32be8d03d43a25593af1e00f996f2145df79bef65d83fe5baee8f094dc37`.
