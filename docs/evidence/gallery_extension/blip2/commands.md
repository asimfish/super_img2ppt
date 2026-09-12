# Commands and audit

Runtime: /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt
Python: /Users/liyufeng/Code/super_img2ppt/.venv/bin/python
All runtime invocations use command-local PATH=/opt/homebrew/bin:$PATH. No installations or repository mutations.

1. curl -L https://proceedings.mlr.press/v202/li23q/li23q.pdf -o paper.pdf
2. Raster-only extraction via pypdfium2 PdfDocument(paper.pdf)[2].render(scale=3).to_pil(), PIL crop (164,204,1628,507). No PDF text or vector coordinates.
3. super-img2ppt prepare source.png --out job
4. python freeze.py (ROI contract, before authoring)
5. python author.py (initial script TypeError fixed; then unsupported polygon radius removed).
6. check job/scene.json --out check_01/check_02/check_03 (each distinct directory). check_01 accidentally evaluated prepared empty draft following helper exception; check_02 records polygon radius rejection; check_03 records actual containment omissions.
7. python repair1.py; build job/scene.json --out build_01
8. python measure.py build_01 dev
9. python repair2.py; build job/scene.json --out build_02
10. python measure.py build_02 dev
11. Visual typo correction: printed source says mutlimodal causal. Scene changed to preserve it, then build --out build_final.

All check/build commands add --font-dir /System/Library/Fonts/Supplemental --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype. Logs are sibling .log files.

Helper failures: first PDF helper import fitz failed ModuleNotFoundError; used existing pypdfium2. First metric helper import numpy failed ModuleNotFoundError; rewrote using Pillow lists. No installation. First author helper raised TypeError: dict() got multiple values for keyword argument color; fixed helper keyword merging before scene existed. A report probe used absent root findings key (actual validation uses automated_checks); no artifact changes. No runtime defect identified.
