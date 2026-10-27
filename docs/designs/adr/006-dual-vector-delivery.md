# ADR-006: Dual editable and publication-vector delivery

## Status

Accepted

## Context

Conference figures are commonly consumed in two different ways: authors need an
editable PPTX for later revisions, while paper tooling needs a scalable vector
figure. The runtime already emitted SVG beside the PPTX, but that relationship was
implicit and did not say which parts were still raster assets. A PPTX-rendered PDF
is also not a reliable substitute for the canonical vector export.

## Candidates

### Option A: Keep the existing SVG as an undocumented side effect

- Pros: no code or artifact changes.
- Cons: callers cannot discover the output contract; raster regions are indistinguishable
  from vector regions; no publication-oriented PDF is available.

### Option B: Make SVG canonical and emit a manifest plus SVG-derived PDF pages

- Pros: preserves the existing `svg/` path, gives paper tooling a stable manifest,
  keeps text and geometry as vector elements, and offers a PDF path without adding
  a third-party dependency.
- Cons: local LibreOffice is required for PDF pages; photos and intentionally retained
  artwork remain raster and must be disclosed.

## Decision

Choose Option B. Every build writes `vector/manifest.json` alongside the existing
`svg/` directory and `editable.pptx`. Rendered builds also write `vector/pdf/` by
converting each canonical SVG page with isolated local LibreOffice Draw. The manifest
records page dimensions, element counts, whether a page is pure vector or mixed, and
the IDs and provenance of embedded raster assets. `--no-render` remains an explicitly
unverified draft and writes the SVG manifest without running the PDF conversion.

The SVG is the canonical vector source; the PDF is a publication convenience derived
from that SVG. The PPTX and vector exports are generated from the same measured scene,
but neither is claimed to recover unavailable source data or to make raster artwork
vector automatically.

## Impact

- `build` now exposes PPTX and vector outputs in its artifact report.
- Existing `svg/` links remain valid; no duplicate SVG tree is introduced.
- The new manifest makes mixed vector/raster boundaries machine-readable.
- No dependency or network behavior is added. `--no-render` remains usable without
  LibreOffice and records `pdf_status: not_run`; a rendered build still requires the
  existing LibreOffice PPTX validation path, and therefore cannot claim a rendered PDF
  when that dependency is unavailable.
