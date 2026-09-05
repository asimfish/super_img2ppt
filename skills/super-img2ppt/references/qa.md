# Evidence and acceptance

`validation.json` contains independent checks:

| Check | What it proves | What it cannot prove |
| --- | --- | --- |
| preflight | Source bounds, measured text fit, explicit containers, text ink collisions, named overlap exemptions | OCR accuracy or complete visual reconstruction |
| native_objects | Expected named PPTX objects, editable text content, page count, exact notes | Appearance in a particular office program |
| rendered_text | Text, glyph bounds, font identifiers and visible width in LibreOffice's actual PDF | Correct source transcription, unique font identity from pixels, PowerPoint/WPS behavior |
| comparison image | Source beside a rasterization of the actual PPTX and a difference heatmap | Automatic fidelity acceptance; antialiasing affects pixel differences |
| fonts manifest | Actual locally resolved font files and substitutions | Availability/licensing on a different computer |

The aggregate status is `fail`, `review`, `pass` or `unverified`; `visual_review` stays `required`
because that is an agent/user inspection, not a machine truth. Keep a short visual-review note
with inspected page IDs, concrete remaining differences and the renderer/application used.
Do not replace this with “looks good” or a made-up percentage.

Examples of blocking failures: text does not fit at its allowed minimum; a text box escapes a
container; two content elements collide; image text is duplicated by an editable overlay; the
rendered text is missing/clipped; paths escape the job; sources and dimensions disagree.

`text_overflow` reports both measured dimensions and required dimensions, including the 0.5 source
pixel safety reserve. A width equal to the nominal advance is therefore insufficient. Do not
shrink the font to work around an unexplained margin; inspect `required_width_px` first.

`text_frame_overlap_only` is informational: two transparent text frames intersect, but the
measured visible glyph regions do not. Real ink intersections remain blocking. This exception
does not apply to a picture with baked text or permit a frame to escape its declared container.

`renderer_font_substitution` is blocking even when the text content matches. Font identifiers
are read from the actual PDF and compared with the locally measured font's known names.
`rendered_ink_width_drift` requests review when actual visible width differs from the measured
glyph ink by more than both 3% and 2 source pixels. This diagnostic excludes empty punctuation
cell space; total character advance can conceal mixed Chinese/Latin spacing changes. It is not
a similarity score and does not repair geometry automatically. Compare the source and, when
needed, separate semantic phrases as described in [reconstruction.md](reconstruction.md).

Differences worth reporting: unavailable source font, editable diagrams reconstructed as shapes,
raster labels in a complex chart, uncertain OCR, and no native target-application check.
Rebuild from `scene.resolved.json` with its sibling assets to reproduce selected fonts and line
breaks on a machine containing the same fonts. Rebuild into a new output directory.
