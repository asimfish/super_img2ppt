# Bounded reconstruction evidence

## v0.1.1 real-case extension

On 2026-09-06, six published images from three sources were reconstructed: a Chinese consensus
flowchart, Matplotlib's chart/table example, and four NASA cFS presentation pages. Three cases
were evaluated independently from only the skill and raw images; the other three NASA pages
were authored by the main task from images/OCR. Source drawing code and PDF object coordinates
were not used to author the scenes.

Five cases pass blocking preflight/native/rendered-text checks; four retain `review` for raster
logos. The dense table remains `fail` at one text/grid collision. Its separately marked diagnostic
PPTX is not a successful production build. Arrowhead size and source font widths still differ.
The owning repository contains `docs/real_cases.md`, source/scene/artifact hashes and actual
PPTX PDF/PNG evidence in `examples/real_cases/`. The runner exits 2 while any case remains blocked.

This evaluation led to font-discovery failure reports, text/grid and sloping-container ink
refinement, and a line-stroke boundary fix. Ten new regression cases bring the local suite to
43 passing tests. No new runtime dependencies were added. The mask refinement is bounded.
Native PowerPoint/WPS remains unverified. These six cases do not establish population accuracy.

## Historical v0.1.0 synthetic evaluation

Version 0.1.0, evaluated 2026-09-05 through 2026-09-06. This is one synthetic reconstruction
case and targeted regression evidence, not a population accuracy or performance benchmark.
No quantitative comparison against the reference repository was performed.

## Input and environment

The owning repository contains an original Pillow-drawn 960 × 720 flow diagram at
`examples/source_02.png`, SHA256
`33b807a407e68e10e4feb3b8a450661689fe4165318d06827e91fe0795b8fa85`.
An independent agent received this image and the skill instructions, with no access to the
fixture generator, expected scene, implementation, tests or previous output. It used local
Vision OCR, visually corrected recognition and authored editable geometry.

Environment: macOS 26.2; Python 3.12.12; python-pptx 1.0.2; Pillow 12.3.0; FontTools 4.64.0;
PDFium through pypdfium2 5.13.0; LibreOffice 26.2.4.2. Selected fonts were installed Arial
Regular/Bold and PingFang SC Regular. Fonts were not embedded or redistributed.

## Observation and repair

The independent candidate preserved text and the intended font, but its Chinese/ratio line
was 27 source pixels wider than the source. The earlier checks returned pass and missed this.
The candidate is retained as `examples/flow_before_spacing_fix.json` in the owning repository.
Current checks return review with `rendered_ink_width_drift`: measured visible width 483 px,
actual PDF visible width 510.051 px. Empty trailing punctuation-cell space is excluded.

The repaired scene, `examples/flow_reconstruction.json`, uses five semantic text fragments
at fixed source coordinates, without reducing the font size. Two frame widths include the
reported 0.5 px safety reserve. Only frame whitespace intersects; glyph regions remain separate.
This is an agent-authored scene repair, not automatic mixed-script correction by the runtime.

| Chinese/ratio line | Dark-pixel bounds `[left, top, right, bottom]` |
| --- | --- |
| Source | `[87, 527, 569, 555]` |
| Independent candidate before repair | `[87, 527, 596, 555]` |
| Repaired actual PPTX render | `[87, 527, 569, 555]` |

Method: convert the actual PPTX with LibreOffice, rasterize its PDF, resize to 960 × 720 with
Lanczos, inspect source crop `[75, 515, 850, 570]`, and select pixels with all RGB channels
below 110. Right/bottom coordinates are exclusive. Matching bounds do not imply matching
pixels or exact font identification. Native arrowhead size and antialiasing still differ.

The repaired artifact contains 11 editable text boxes, 4 native shapes and 2 native lines;
it contains no raster picture objects. Preflight, native-object and actual-render checks pass.
The independent failure case also confirmed that a symlink escaping the scene's asset root
was rejected before producing a PPTX, without changing the outside control image.

## Reproduction and limits

From the owning repository, build the two named scenes into separate new output directories
with `super-img2ppt build`. Full commands, validation JSON, source/scene/artifact hashes and
the independent evaluation account are in `docs/verification.md` and `docs/evidence/`.
These repository development fixtures are not required for using the standalone skill bundle.

This evidence is specific to these fonts, this renderer and this synthetic input. Source
transcription required an agent. PowerPoint automation did not complete, WPS was not checked,
and real user failure images were unavailable. No universal fidelity, throughput or cross-editor
compatibility claim is made.
