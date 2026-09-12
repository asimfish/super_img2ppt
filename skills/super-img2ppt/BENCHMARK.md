# Bounded reconstruction evidence

## v0.3.3 reusable curve tracing and public ICML figures

Three independent pixel-only reconstructions retain complete GaLore Figure 6 (753 native
objects, one 1.8058% image-only crossing crop), Vision Mamba Figure 2 (158 native, three
image-only crops), and Mamba-2 Figure 7 (475 native, no visible rasters). All have actual
PPTX renders and portable scenes; parent replays pass. Original Mamba-2 font substitution
remains review. Source-fidelity failures are retained: GaLore 4/10 recorded regions pass,
Vision Mamba 5/12, Mamba-2 2/9. Do not pool these different masks or call overall fidelity
a pass. Vision Mamba holdout is 0/4; the other two have disclosed inspected-holdout
contamination, and Mamba-2 exceeded the three-repair cap in one formula region.

Runtime changes have causal regressions: TTC italic face misclassification, directional
glyph-overflow reports, and round line caps with conservative endpoint collision checks.
GaLore exposed steep-stroke ambiguity, prompting axis-y tracing; same-color crossings
and long occlusions still fail rather than inventing trajectories. The 558 changed GaLore
segments differ only in cap metadata; actual rendering removes join seams. A frozen
extra green-curve diagnostic has IoU 0.949 and zero-pixel edge error, only for that ROI.

The owning repository docs/public_figures.md and docs/evidence/public_figures retain
original failures, frozen contracts, license evidence, package and regression results.
README previews are actual source-width PPTX renders. No source-private manuscript
artwork or font files are published. Native PowerPoint/WPS remain unverified.

## v0.3.2 complete published main figures

On 2026-09-11, independent image-only evaluations reconstructed the full Grounding DINO
ECCV2024 Figure 3, GLaMM CVPR2024 Figure 2 and UniAD CVPR2023 Figure 2. All major panels
were retained, including attention internals, token grids, grounded conversations and the
perception/prediction/planning branches. Repository image variants of the first two differed
from the publications, so evaluation used raster crops of the actual published PDFs.
No PDF text/vector coordinates or original drawing code provided the reconstruction answers.

Grounding DINO has 59 native text objects, 274 shapes, 392 lines and four local images.
Its fixed 35-region strict score improves 0 -> 3 -> 11; 21 isolated primary text labels reach
ink-edge error <=1 px after font-size/origin calibration, but glyph IoU and dense regions fail.
GLaMM has 32 text objects, 87 shapes, 22 lines and 14 local images. Only 3/39 fixed regions
pass, all connectors; a separately identified source-width PDF diagnostic gives 4/39. UniAD
has 28 texts, 27 shapes, 39 lines and eight images; 8/36 fixed regions pass, seven geometry.
Two important module labels stay fused to raster artwork. One red Planner ROI has an invalid
dark-only mask and is counted as failed, not silently excluded or recast as successful.

All three remain source-fidelity FAIL despite nonblocking automated review status. Per-case
thresholds and render resolutions differ and must not be pooled as conversion accuracy.
Font shape, weight, baseline/word spacing, soft shadows, perspective stacks and thin colored
lines remain unresolved. First builds and candidate repairs are preserved; parent feedback
after first actual renders is explicitly distinguished from the initial independent attempt.
The owning repository's docs/main_figures.md and docs/evidence/main_figures record raw results.

This release improves reconstruction instructions and source reproduction, not runtime layout
algorithms. No new runtime defect was causally established; implementation is unchanged from
v0.3.1 except the version constant. UniAD artwork is distributed under its explicit assets
license; the two paper-derived corpora remain local. No fonts or new dependencies installed.
Actual LibreOffice/PDFium was checked; native PowerPoint/WPS remain unverified.

## v0.3.1 super_teaser extension

On 2026-09-10, three independent image-only reconstructions used commit-pinned super_teaser
MIT-0 generated illustrations: LoRA, routed experts and embodied hierarchical inference.
They are conceptual illustrations, not original conference figures or experimental evidence.
Frozen v0.3.0 baseline reports and failures remain unchanged. A separate frozen candidate
replays the exact embodied failure; the parent replays all three final scenes and prior corpora.

LoRA has 89 native objects and three local rasters. Eight of 18 fixed regions meet both
edge <=3 px and IoU >=0.70; four supplemental rounded-corner regions improve bidirectional
P95 distance to <=2 px through native line approximations. Routed experts have 87 native
objects and no rasters; 25/25 regions meet edge/centroid <=4 px and ink-count delta <=25%.
Embodied inference has 81 native objects and 14 local rasters; only four line regions of
26 fixed regions meet edge/centroid <=4 px and IoU >=0.45. All 22 text regions retain failures.
These different masks and thresholds cannot be combined into population accuracy.

The PDF check previously attributed a neighboring Action's A to Flow matching's empty frame.
Unique complete PDF text-object ownership fixes this false overflow without changing render
pixels or source fidelity. Missing/ambiguous ownership retains conservative checks. Two actual
LibreOffice regressions cover horizontal/quarter-turn labels plus missing-text, true-overflow
and duplicate-owner negative controls. The local suite has 67 passes, no skips. No new runtime
dependencies, fonts or external capabilities were added. Native PowerPoint/WPS remain untested.
The owning repository's docs/teaser_cases.md and docs/evidence/teaser_cases retain measurements,
raw failures, original/candidate reports and hashes; examples/teaser_cases contains the artwork.

## v0.3.0 diverse figure extension

On 2026-09-07, three independent evaluators reconstructed CLIP (ICML 2021), Swin Transformer
(ICCV 2021) and a Matplotlib annotated heatmap from specified raw images. They started from a
frozen v0.2.0 skill/runtime; parent-authored fixes were then tested in separate frozen candidate
trees. Original reports, failures, fixed ROI definitions and file hashes remain unchanged.
DDPM's NeurIPS 2020 author-published table/rate-distortion figure was reconstructed by the parent
from its bitmap and is explicitly a development case, not an independent blind evaluation.
No source plotting code, chart data or PDF text/vector coordinates were used as answers.

- CLIP: four encoder trapezoids are native polygons. Final scene has 293 native objects,
  including 131 text objects, and two photographic regions. The original 20 px subscript
  candidate had nine false text/text collisions with zero measured glyph intersections.
  Comparing both glyph masks permits those original mathematical placements, while true
  duplicate glyphs remain blocked. Twenty-one fixed text ROIs improve from maximum edge
  delta 2 px to 1 px; nine grid/shape centers remain exact. Two runtime ink-width warnings
  remain `review`, even though those labels' actual/source widths agree at about 43 px.
- Swin: 497 native objects (92 text, 30 shapes, 375 lines/arrows) and 34 photo crops. Thirty
  fixed ROIs have median mean edge distance 0.573 px, maximum per-ROI mean 3.151 px. Several
  ROI masks also include borders/lines and are not used as isolated typography evidence.
  Formula multiplication signs, arrow silhouettes and photo-grid crop seams retain differences.
  Adjacent caret text was wrongly assigned to a neighboring z frame in an actual PDF check;
  the case uses native line hats as a scene workaround, not a claimed PDF ownership fix.
- Heatmap: one native 16-stop linear gradient replaces 358 solid bands. Source-size colorbar
  interior RGB MAE improves from 9.341/255 to 0.665/255; supplemental high-resolution dark
  residual runs fall from 203 to zero. The original 72 ROI plan improves from 70 to 72 within
  its fixed tolerances (text <=2 px, grids <=1 px). All 49 matrix values remain native text.
  Seven approximately 30-degree top labels remain one raster crop; final status is `review`.
  Mean native text-mask IoU is 0.5437, so edge agreement is not pixel-identical glyphs.
- DDPM: 254 native objects, including 69 text objects and 157 thin blue rectangles tracing
  the visible curve. Sixty-six fixed ROIs improve from maximum edge delta 29 px to 14 px;
  median absolute edge delta stays 1 px. Bold numerical widths, inequalities and loss notation
  still differ. This is not a data-linked chart or automatic mathematical typesetting.

Nine added regressions bring the local suite to 65 passing tests with no skips. Actual
LibreOffice tests cover both gradient directions and polygon geometry; negative controls
reject ambiguous polygons/gradients and actual glyph collisions. Runtime dependencies are
unchanged. The parent replays all three new redistributable scenes, local DDPM, the six old
general cases and two redistributable ICLR cases using the final code. The old dense table
still fails; the historical MobileViT local artwork is not counted as a new replay.

The owning repository's `docs/diverse_cases.md` and `docs/evidence/diverse_cases` contain
original/candidate reports, measurements, failures and hash manifests. Three attributed
redistributable cases are in `examples/diverse_cases`; DDPM artwork stays local because a
general redistribution license for the author-site image was not established. Selected font
families are Arial, Courier New, Times New Roman and DejaVu Sans; none are embedded. These
results do not imply universal alignment, exact source-font identification or population
accuracy. Validation uses LibreOffice/PDFium; native PowerPoint/WPS remain unverified.

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
