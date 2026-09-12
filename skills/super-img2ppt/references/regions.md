# Source-coordinate ink diagnostics

Use `compare-roi` after rendering the actual PPTX to the source image width. Compare an
isolated label, formula, curve or grid segment, using the same x/y/w/h in both images.
It never registers or resizes the actual output, and never returns a source-fidelity PASS.

```bash
super-img2ppt compare-roi source.png actual_source_width.png \
  --roi 100 80 240 60 --color '#000000' --tolerance 150 --out job/roi_01
```

Choose color and tolerance from visible source ink. The mask selects pixels whose **every
RGB channel** differs from the chosen color by at most tolerance (0–255). For white labels
on dark backgrounds explicitly select `#FFFFFF`; a dark mask measures the background instead.
Same-color grid lines, circled indices or neighboring labels may contaminate a region; inspect
both saved masks and crops. Record ROI definitions before comparing candidate revisions.

`region.json` contains source/actual mask counts, absolute `[left,top,right,bottom]` ink boxes
(right/bottom exclusive), edge deltas in source pixels, and mask IoU. Equal edge bounds do not
prove equal glyphs. If either mask touches an ROI boundary, complete-ink edge metrics are
invalid and deltas are null; any remaining IoU is only a cropped-mask diagnostic. An empty
source mask produces null IoU, including when both masks are empty. Missing actual ink has
IoU 0 when the source is nonempty. These cases remain `review`, with explicit issues.

`comparison.png`, `source_crop.png`, `actual_crop.png` and two binary mask images make the
measurement inspectable. Input canvas sizes must match exactly; incorrect dimensions fail.
Only EXIF orientation and alpha-on-white normalization occurs. Both inputs must be local
single-frame images, each below 64 MB / 40 million pixels; ROI area is at most four million
pixels. A fresh output directory is required, with failure evidence in `region.json`.

The caller must supply a true PPTX render and preserve its build provenance. This tool cannot
attest an image's origin, identify fonts, recover the intended text, isolate touching objects,
or turn source-guided diagnostics into blind evaluation. Do not aggregate different masks
into an accuracy score. Keep failures and freeze the final candidate before independent checks.
