# Bounded reconstruction evidence

## v0.2.0 conference figure extension

On 2026-09-06, three independent evaluators reconstructed raw bitmaps from ViT (ICLR 2021),
MobileViT (ICLR 2022, Figure 1), and Spatial-Mamba (ICLR 2025, Figure 4). The evaluator inputs
were the skill and image only. The shared runtime was then modified in response to initial
findings; original reports and controlled candidate retests are separate. This was not a blind
comparison of two frozen released versions, and no source PDF vectors/text coordinates were
used as reconstruction answers.

All three final actual LibreOffice builds pass blocking checks, with measured limitations:

- ViT: 147 objects, including 35 text boxes and five custom arrow freeforms. Two residual
  arrowheads recovered the source's measured raster spans. Representative text edges differ
  by 0–1 px; some edges by 2 px; 11 stroke-center anchors differ by at most 0.715 px.
- Spatial-Mamba: 544 objects, 39 text boxes including 15 native rotated labels, and one photo.
  The 15 rotated labels have mean absolute edge delta 0.383 px and maximum 1 px. Eighteen
  horizontal text anchors have mean 0.417 px and maximum 1 px. Shadows/rounded dashes remain
  approximations, and four multiplication symbols differ by up to 2 px.
- MobileViT: the scene changed from 1207 to 697 objects after native dashed borders, retaining
  91 editable text boxes and eight text-free pictures. Twenty-five horizontal text ROIs have
  median absolute edge delta 1 px and maximum 9 px; the title's right edge improved from
  -28 px to 0. Ten tilted labels remain horizontal and six tensor interiors remain raster.

The runtime improvements add quarter-turn text, source-sized native arrows, native dash
patterns, alpha-aware text/image collision refinement and corrected matching-aspect stretch
warnings. Thirteen focused regressions, including actual Office rendering and opaque/baked-text
negative controls, bring the local suite to 56 passing tests. The six previous cases replay
without changed statuses; the old dense table still fails. No new dependencies were added.

The owning repository's `docs/conference_cases.md` links original findings, failed candidates,
frozen text ROIs, source/artifact hashes and actual previews. Two redistributable cases are in
`examples/conference_cases`; MobileViT artwork remains local because redistribution permission
was not established for its downloaded paper. The fixed-source fetch recipe is repository-only.
Source fonts are approximations, not identified ground truth; Times New Roman and, for ViT's
small note, Liberation Mono are required for the captured rendering. Fonts are not embedded.
Pixel edge measurements are local diagnostics, not a global fidelity score or population
accuracy estimate. PowerPoint/WPS and another computer's font availability remain unverified.

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
