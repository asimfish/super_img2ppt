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
