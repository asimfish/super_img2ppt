Commands used (all filesystem writes under this new /tmp job; no installs or repository edits)

- curl -L https://proceedings.mlr.press/v202/poli23a/poli23a.pdf -o source.pdf
- curl -L https://proceedings.mlr.press/v202/poli23a.html -o publisher.html
- curl -L https://proceedings.mlr.press/v202/ -o volume.html
- curl -L https://proceedings.mlr.press/faq.html -o faq.html
- curl -L https://proceedings.mlr.press/pmlr-license-agreement.pdf -o license-agreement.pdf
- curl -L https://creativecommons.org/licenses/by/4.0/ -o cc-by-4.0.html
- Existing repo .venv/bin/python with pypdfium2 rasterized source.pdf page index 1 at scale=4. Pillow crop (426,260,1944,602) saved figure1.png. No source PDF text/vector coordinates used. The license PDF text was separately extracted to verify paragraph 2 and 3.
- PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt prepare /tmp/hyena-forward-20260912/figure1.png --out /tmp/hyena-forward-20260912/job --ocr none
- Opened source image before authoring; author.py wrote roi-contract.json before any scene elements. Frozen contract: 8 dev, 4 heldout, unregistered binary ink IoU >= .70 AND all ink bbox edges <=4 source px.
- author.py: native geometry and text from raster inspection, seven text-free crops. First attempt imported unavailable numpy; rewritten to Pillow and standard Python without installing anything. Initial optional fitz import was also unavailable; switched to existing PDFium. These are authoring dependency probes, not runtime bugs.
- Build command repeated with fresh --out build_02 through build_06:
  PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/hyena-forward-20260912/job/scene.json --out /tmp/hyena-forward-20260912/build_06 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype --font-dir /System/Library/Fonts/Supplemental
- Initial preflight build_02 failed text widths, containers, superscript frame bounds. repair1.py fixed these => build_03 actual PPTX rendered; y italic left overhang remained.
- measure.py build_03: dev only. First actual image sent to parent for review.
- repair2.py fixed open arrowheads, italic y frame padding, and source font origins, producing build_04. Automated pass, dev 2/8. No further font tuning.
- Parent review requested correcting FFN sampling pitch and replacing automatic bounding-box overlap exemptions with explicit semantic pairs. parent-repair.py did both, output build_05. Native matrix cell containers detected last 4x4 cell outside frame by 1–2px. Clipped d1cell26/dncell26 width and height to their corresponding matrix frame (no changes to runtime), producing build_06.
- FFN source dot centers were separately saved in ffn-dot-centers.json and visually checked in ffn-source.png. 25 native stems now use actual source center pitch approximately 4.335px instead of arbitrary 4px sampling; endpoint detection reads visible red stem pixels. This reconstructs drawing geometry, not experimental values.
- measure.py build_06 without --final: dev only. Render actual exported PDF through PDFium with scale=1518/page.width. Source and actual size are both 1518x342. No translation, registration, resizing after rendering or mask threshold changes.
- FINAL-FREEZE.json archived SHA256 of source, contract, authored and resolved scenes, assets, PPTX, PDF, SVG, fonts, validation, and actual PNG before heldout reveal.
- measure.py build_06 --final: first heldout evaluation after hash freeze. No scene/artifact edits followed. All frozen hashes reverified unchanged.
