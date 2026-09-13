# Evidence and acceptance

`validation.json` contains independent checks:

| Check | What it proves | What it cannot prove |
| --- | --- | --- |
| preflight | Source bounds, measured text fit, explicit containers, text ink collisions, named overlap exemptions | OCR accuracy or complete visual reconstruction |
| native_objects | Expected named PPTX objects, editable text content, page count, exact notes | Appearance in a particular office program |
| rendered_text | Text, glyph bounds, font identifiers and visible width in LibreOffice's actual PDF | Correct source transcription, unique font identity from pixels, PowerPoint/WPS behavior |
| appearance | Selected source/target color and normalized ink coverage against actual PPTX render | Full-page fidelity, semantic color correctness, aesthetic quality or target-editor equivalence |
| comparison image | Source beside a rasterization of the actual PPTX and a difference heatmap | Automatic fidelity acceptance; antialiasing affects pixel differences |
| fonts manifest | Actual locally resolved font files and substitutions | Availability/licensing on a different computer |

PDF ink and font checks attribute a complete native PDF text object only when its text and
all glyph centers identify one scene text element. This prevents neighboring labels from
contaminating the empty part of a text frame. Missing or ambiguous ownership retains the
conservative geometric checks. Actual owned glyph overflow, missing text and font substitutions
remain checked; this is not a guarantee of exact source typography.

The aggregate status is `fail`, `review`, `pass` or `unverified`; `visual_review` stays `required`
because that is an agent/user inspection, not a machine truth. Keep a short visual-review note
with inspected page IDs, concrete remaining differences and the renderer/application used.
Do not replace this with “looks good” or a made-up percentage.

Examples of blocking failures: text does not fit at its allowed minimum; visible text escapes a
container; two content elements collide; image text is duplicated by an editable overlay; the
rendered text is missing/clipped; paths escape the job; sources and dimensions disagree.

`text_overflow` reports both measured dimensions and required dimensions, including the 0.5 source
pixel safety reserve. A width equal to the nominal advance is therefore insufficient. Do not
shrink the font to work around an unexplained margin; inspect `required_width_px` first.

`text_frame_overlap_only` is informational: transparent frame space intersects text, a line or
another object while visible ink remains separate. `text_frame_outside_container_only` means
empty frame corners extend beyond the background shape while visible ink fits. Near glyph
corners and sloping boundaries the check refines coarse ink boxes with a bounded 4x glyph mask.
Actual ink crossings remain blocking. The mask is limited to 8 million pixels and eight cached
entries; larger regions retain conservative boxes. These exceptions never waive baked-text
duplication, page bounds or the containment of non-text objects.

For text-free artwork, transparent image pixels are excluded from text collision checks using
the asset alpha channel and the actual contain/cover/stretch transform. The refinement supports
quarter-turn text, caps each source alpha mask at 8 million pixels and caches two masks per
page. Larger assets and image/image overlaps retain conservative box checks. Images declared
to contain text still trigger the baked-text guard before any alpha refinement or exemption.
`image_stretched` is reported only if the requested aspect ratio changes by more than 0.1%.

Quarter-turn text is checked in its rotated position for overlap, containment, page bounds and
actual PDF glyph bounds; width drift is measured along its reading direction. Custom arrow
heads participate in overlap and page-bound checks as triangles, separately from their shafts,
so empty corners beside a head do not become filled bounding-box obstacles. Legacy Office
arrow heads use conservative SVG-sized bounds. Dash gaps are conservatively occupied for QA.

Convex polygons use their perimeter for overlap and containment, including their empty slanted
corners. Both vertex windings are normalized for clipping. Vertex count and coordinates are
bounded before geometry is evaluated; invalid or self-crossing polygons are rejected.

Text/text candidates also compare both bounded glyph masks in one coordinate frame, including
quarter-turn rotation. Separate main letters and subscripts may have overlapping ink rectangles
without overlapping pixels. Real glyph intersections still block. If either complete mask is
unavailable, the check retains conservative geometry rather than using a partial measurement.

Source grid crossings can be declared with named overlap pairs and a concrete source-based
reason. Do not blanket-exempt table text. Thin source lines must be measured at their stroke
centers; an integer bitmap row denotes a pixel cell, not its center. A line polygon already
includes its stroke width, so the page-boundary check counts that width once.

Font discovery timeouts/nonzero exits are domain failures (exit 2), recorded in a fresh
`validation.json` for both `check` and `build`. The selected executable is included in the error.
Inspect `doctor` and select a working installed font tool for that command before retrying.

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

## PDFium line-end hyphen markers

PDFium may return U+0002 in bounded extraction and U+FFFE in range extraction for a
visible line-end hyphen. The runtime restores a hyphen only when the engine reports
`FPDFText_IsHyphen == 1` and Unicode U+0002 at the indexed glyph, with a matching count
inside the text frame. Raw `rendered` text is retained beside `rendered_normalized`.
The same indexed glyph remains in ownership, font and overflow checks. Missing or
unconfirmed markers still fail; no general control-character stripping is performed.

See [appearance.md](appearance.md) for explicit color/ink-density plans and required handling of missing coverage. Source-backed builds without a plan report review, not color PASS.
