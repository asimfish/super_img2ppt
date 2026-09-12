# Hyena Hierarchy complete Figure 1 — realistic forward reconstruction

**Delivered a complete editable reconstruction. Automated checks pass; frozen pixel fidelity fails (2/12 joint ROIs).** This is a reviewable example with disclosed failures, not a high-fidelity success claim.

Final artifacts are in `build_06/`: `editable.pptx`, `svg/page_001.svg`, `scene.resolved.json`, `assets/`, `fonts.json`, `validation.json`, `render/editable.pdf`, `actual-source-width.png`. Source: `figure1.png`; official source PDF: `source.pdf`. Original attribution and archived license evidence: `ATTRIBUTION.md`.

Coverage: complete Figure 1 on physical PDF page 2, including the full Hyena recurrence, broadcast path, all math symbols and Dense labels, all discrete h-filter plots, and the complete Window / FFN / PositionalEncoding inset. The caption is excluded deliberately from the figure crop. Seven text-free heatmaps remain local movable images: three Toeplitz matrices, three Dense matrices, and positional-encoding heatmap. Everything readable remains native text. Counts: **30 text + 206 shapes + 172 lines = 408 native objects**, plus 7 images (415 total).

Raster crops occupy 53826 / 519156 = 10.37% of the source area. This is pixel area of the seven independently movable asset boxes, not a claim of semantic editability for their interiors. Stems, dots, D diagonal cells, borders, labels, arrows, and broadcast wiring are editable.

Fonts: actual exported PDF uses ArialMT, TimesNewRomanPSMT, TimesNewRomanPS-ItalicMT. Source mathematical typeface was not recovered; Times New Roman is a disclosed approximation. Font files are not embedded or copied. Exact resolved font paths, hashes, rights and discovery evidence are in fonts.json.

Validation: final runtime status `pass`; preflight and native objects and rendered text checks pass; visual review still required. Actual PowerPoint file was rendered by LibreOffice to PDF and PDFium to PNG. No native PowerPoint or WPS verification. Source and actual evaluation rasters both 1518 × 342. Joint threshold frozen before authoring: every ROI edge error <=4px AND unregistered ink IoU >=.70. The mask is any channel <160; no registration or candidate-specific mask changes.

| ROI | Split | Max edge px | IoU | Joint pass |
|---|---|---:|---:|---|
| dense_input | dev | 1 | 0.5445 | False |
| window | dev | 0 | 0.6841 | False |
| ffn | dev | 0 | 0.7264 | True |
| pe | dev | 1 | 0.5501 | False |
| dense_middle | dev | 1 | 0.4855 | False |
| S1 | dev | 2 | 0.3419 | False |
| h1 | dev | 2 | 0.4186 | False |
| input_arrow | dev | 0 | 0.8134 | True |
| dense_last | heldout | 0 | 0.5930 | False |
| SN | heldout | 4 | 0.2677 | False |
| DN | heldout | 6 | 0.2458 | False |
| output_arrow | heldout | 0 | 0.1347 | False |

Dev: 2/8 pass. Heldout: 0/4 pass. Eleven of twelve satisfy the edge criterion, but this does not establish glyph fidelity; most fail IoU. Heldout DN has 6px edge drift. Heldout output arrow has equal bbox but only .1347 IoU, demonstrating that matching edge extents is insufficient. No edits after heldout reveal; all frozen hashes checked unchanged.

Failure interpretation: source-vs-substitute mathematical glyph shapes and label stroke positioning remain noticeably different at pixel level. Dense labels and PositionalEncoding are readable but do not achieve the frozen IoU. Source-width line raster placement also leaves heldout connector mismatch. This should be presented in README as a complex complete conversion with explicit limitations.

Repair record: initial preflight plus two targeted typography/arrow repair passes; fonts stopped thereafter. Parent reviewed first actual render and corrected FFN center sampling and overbroad overlap automation before final freeze. FFN received one local repair; semantic overlap/container declarations received a local rewrite and a follow-up terminal-cell bounds correction. All initial failed validation reports and logs are retained in build_02/03/05. No runtime modifications, installations or uploads. See COMMANDS.md and scripts for reproducibility.

Licensing: publisher FAQ links to its standard publication agreement, paragraph 2 CC BY 4.0, paragraph 3 attribution plus publication hyperlink. Archived documents provide publisher policy evidence; an individually signed publication agreement was not obtained. Attribution supplies all authors, title, conference/pages, original link, license link and adaptation description.
