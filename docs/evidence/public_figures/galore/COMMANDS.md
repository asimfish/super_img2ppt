Environment: existing /Users/liyufeng/Code/super_img2ppt/.venv; no install, repo edits, push, external upload, or author drawing code.

Source download:
`curl -L https://raw.githubusercontent.com/mlresearch/v235/main/assets/zhao24s/zhao24s.pdf -o paper.pdf`

Raster preparation: `pypdfium2.PdfDocument(paper.pdf)[20].render(scale=3).to_pil()`, producing 1836×2376; exact complete Figure 6 crop `(310,370,1480,1230)` producing 1170×860. No PDF text or vector access.

`super-img2ppt prepare figure6.png --out chart`

Scripts (absolute work paths are intentional audit records):
1. `freeze.py`: source/ROI contract and publisher license archive.
2. `author_chart.py`: native text/axes/legend authoring from pixels/OCR. Font calibration history kept in calibration01–04 (01 structural fail; 02–04 actual PPTX renders).
3. `trace_all.py`: first forward helper trial, retains rejected steep/occluded curves.
4. `trace_visible.py`: original axis-y transpose experiment, retained separately.
5. `trace_axis.py`: final reusable axis='y' trace implementation; masks original RGB pixels with color tolerance 35; explicit regions avoid legends, splits at observed long gaps; no invented experimental data.
6. `merge_curves.py`: original-coordinate lines + exact unsupported crossing crop; geometrically clips all underlying native strokes out of crop, preserving no duplicate raster/native text or chart strokes.
7. `super-img2ppt build chart/scene-complete.json --out chart/buildNN --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype --font-dir /System/Library/Fonts/Supplemental`
8. `measure.py buildNN`: actual exported PPTX PDF rasterized source width; no image registration. Black neutral ink threshold mean<180, max channel difference<35. Source/raster bbox edge displacement and exact pixel-set IoU.

All runtime invocations used `env PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt ...`.
