# Commands and reproduction record

Working directory: `/Users/liyufeng/Code/super_img2ppt`; task directory `/tmp/vision_mamba_forward_20260912`. No installs, repo edits, or publishing performed.

Downloads:
```sh
curl -L --fail https://raw.githubusercontent.com/mlresearch/v235/main/assets/zhu24f/zhu24f.pdf -o /tmp/vision_mamba_forward_20260912/source/zhu24f.pdf
curl -L --fail https://proceedings.mlr.press/v235/zhu24f.html -o /tmp/vision_mamba_forward_20260912/source/official.html
curl -L --fail https://proceedings.mlr.press/pmlr-license-agreement.html -o /tmp/vision_mamba_forward_20260912/source/license.html
```

PDF raster: existing `.venv/bin/python`, `pypdfium2.PdfDocument`, page index 4 `.render(scale=2).to_pil()`. Source crop: PIL crop `(110,130,1090,388)`. Artwork crops on full-page raster: `(133,304,237,377)`, `(278,331,375,351)`, `(396,331,474,351)`. PDF text and vector extraction were not used to author.

Authoring sequence: `.venv/bin/python author.py`; build_01; `relations.py`; build_02; remove class_token container and add named token_5 overlap (source-verified patch-area sharing); build_03; `repair_01.py`; build_04; `repair_02.py`; build_05; `repair_03.py`; build_06. The inline class-token adjustment is preserved in final `scene.json`.

Every build used a NEW output directory and this command pattern:
```sh
PATH=/opt/homebrew/bin:$PATH .venv/bin/super-img2ppt build /tmp/vision_mamba_forward_20260912/scene.json --out /tmp/vision_mamba_forward_20260912/build_06 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype --font-dir /System/Library/Fonts/Supplemental
```
Use a fresh output name when reproducing. Each build has a scene original snapshot after preflight success. Initial failed build_01/_02 preserve validation findings.

Dev only measurements ran for build_03 through build_06:
```sh
.venv/bin/python /tmp/vision_mamba_forward_20260912/measure.py build_06 dev
```
After candidate_freeze.json was saved, heldout was first revealed using:
```sh
.venv/bin/python /tmp/vision_mamba_forward_20260912/measure.py build_06 all
```

Initial dependency probes failed for `fitz` and `numpy`; immediately used installed PDFium and PIL equivalents. No installation was attempted. Font parser timestamp warnings occurred but builds 04–06 passed all automated checks. These are not fidelity passes.
