# Upstream provenance

- URL: https://github.com/ningzimu/image-to-editable-ppt-skill
- Full reviewed commit: `fb869763127fd31ba7288d905671ffc4ea542f60`
- Reviewed date: 2026-09-05
- License: MIT, copyright (c) 2026 ningzimu. Read the upstream `LICENSE` before implementation.
- Relationship: independent synthesis informed by source review. No upstream runtime, prompt,
  asset or instruction file is copied into this package. This is not an upstream-compatible fork.
- Inspected paths: `skills/image-to-editable-ppt/SKILL.md`, `references/manifest-schema.md`,
  `cli/pyproject.toml`, `cli/editppt/runtime/build_pptx_from_manifest.py`,
  `cli/editppt/runtime/validate_pptx.py`, plus repository README.

Observed mechanisms, not an empirical score of upstream quality: the reviewed writer estimates
ASCII width with a fixed 0.55-em factor, uses a separate preview-font chooser with system-specific
fallbacks, and emits explicit OOXML fonts. Its visible validation includes provenance/text/package
checks. Our focused change is actual font-file metrics, a shared geometry contract, conservative
collision checks, and rendering the emitted PPTX for verification. These observations do not
prove that every upstream conversion fails, or that this version is universally more accurate.

Adjacent ownership search: no image-to-editable reconstruction owner was found in the inspected
Forge capability registry or Super Skill Team index on this date. Existing `ppt-master`,
`codex-ppt`, paper presentation and slide-polish skills create/design presentations or edit
existing documents. This user-requested repository owns reconstruction from existing pixels.

Primary technical references reviewed:

- https://python-pptx.readthedocs.io/en/stable/api/text.html — text frame margins, wrapping and fitting.
- https://pillow.readthedocs.io/en/stable/reference/ImageFont.html — actual font metrics and glyph bounds.
- https://pypdfium2-team.github.io/pypdfium2/python_api.html — PDF rendering and bounded text extraction.
- https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.font — font information and embedding relationship.

Upstream updates require new source/license review; no automatic synchronization is provided.

v0.3.4 PDF text validation reference (reviewed 2026-09-12): PDFium's public
`FPDFText_IsHyphen` API and its `IsHyphen` / `GetTextWithHyphen` embedder tests explain
U+0002/U+FFFE line-end markers. Independently implemented a narrowly confirmed conversion;
no PDFium implementation or fixture content copied.
https://pdfium.googlesource.com/pdfium/+/45a5ea16c998110d9aa2ce2dbf8d47ad1d2ae364/fpdfsdk/fpdf_text_embeddertest.cpp

v0.3.5 formula composition is independently implemented from the existing font/layout APIs.
Real 3D Diffuser Actor raster-only reconstruction exposed blanket bold-italic argument styling
and a Unicode superscript that selected an unrelated fallback face. No paper vector/text
coordinates, author drawing code, TeX engine or third-party math implementation was imported.
The new helper compiles explicit observed baselines and styles to existing native text objects.

v0.3.6 region diagnostics and diagonal text support are independent extensions of this runtime.
Source-only Cosmos 3 reconstruction exposed a 45-degree attention-header strip that v0.3.5
could only retain as raster text. Native rotation reuses existing python-pptx/SVG transforms;
formula parts share one explicit rotation anchor. PDF verification keeps the page-axis glyph
bounds limitation visible instead of treating a rotated AABB as proof of exact containment.
Repeated public-paper measurements (OpenVLA, Cosmos Policy) motivated explicit empty/clipped
mask diagnostics. No figure-author code or upstream math/vision implementation was imported.

The v0.3.7 native edit-group schema/export and recursive object verification are independently
implemented here, motivated by real editing granularity tests. They are not copied from the
upstream skill. Explicit semantic grouping is independent of layout containers and retains
existing leaf geometry and paint order.
