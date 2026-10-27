# Dual vector delivery evidence

This note records a local smoke run of the new 0.3.17 output contract on the
published GR00T N1 Figure 3 scene.

Command:

```bash
PATH=/opt/homebrew/bin:$PATH .venv/bin/python - <<'PY'
from pathlib import Path
from super_img2ppt.cli import build

build(
    Path("examples/gallery/gr00t_n1/scene.resolved.json"),
    Path("output/vector-dual-smoke/gr00t_n1"),
)
PY
```

Observed artifacts:

- `editable.pptx` and the canonical `svg/page_001.svg` were emitted from the
  same scene.
- `vector/manifest.json` reports **159 vector elements** (43 text, 59 shapes,
  57 lines) and **2 explicitly retained raster assets** (the observation photo
  and humanoid artwork).
- `vector/pdf/page_001.pdf` was produced by converting the SVG with isolated
  LibreOffice Draw. `pdffonts` reports embedded text fonts and `pdfimages`
  reports exactly the two image objects listed by the manifest.
- The smoke build keeps the existing figure's `review`/appearance limitations;
  this evidence validates the dual artifact path and raster boundary, not a
  new claim of pixel-perfect fidelity or PowerPoint/WPS compatibility.

The smoke output is intentionally ignored under `output/`; this document does
not publish a generated binary or overwrite the historical gallery artifacts.
