# Vector detail refinement · 0.3.16

Request: improve shapes, colors and icons through actual complex figure testing.
Observed gaps: a concave flat-color icon could not be one scene shape; native shape/line/
gradient alpha was unsupported. Before implementation, the exact regression path rejected
those properties (3 failing cases in red.txt). The old convex polygon contract stays intact.

Implemented one simple concave native contour with triangulated actual-interior QA;
separate fill/stroke/gradient-stop alpha; explicit no-stroke for zero width; invisible vector
collision handling; bounded trace-icon and source sample-color commands. Runtime, package and
workspace versions are checked together after discovering the stale __version__ constant.
No new dependencies, external calls, raw XML/path input or host installation.

## Real figure evidence

[Four portable cases and actual renders](../../../examples/detail_cases/README.md) contain
PPTX, SVG, scenes/assets, actual PDF/PNG, fonts and reports. Inputs are existing, already-seen
full paper figures/scenes. These are controlled repair/retest cases, not blind reconstruction.
Source coordinates come from raster inspection, not PDF text/vector extraction.

- GR00T N1 Figure 3: 18-line legend icon replaced by one 130-vertex freeform. Same ROI and
  RGB mask tolerance: IoU0.67133758 ->0.92696629; outer-edge deltas [0,0,0,1] ->[0,0,0,0].
  Programmatic move[-65,+40] source px and recolor#E97424 kept 143 other native leaf objects
  XML-identical. Edited actual render contains 583 orange core pixels at [1220,243,1262,289],
  within1px of the requested box. This is not a PowerPoint/WPS UI test.
- GR00T old purple#D398E8 versus source#CC94F1 was rejected at ΔEOK0.0220591, above0.02;
  each of14 repeated token interiors was sampled and corrected. Original failures retained.
- BLIP-2 Figure 2: encoder blue#1682C1 versus source#157AC3 was rejected and corrected from
  its explicit source ROI. Its small snowflake remains raster; fragmented masks are refused.
- Spatial-Mamba Figure4 and Cosmos Policy Figure2 were rebuilt and rendered in full to check
  existing native geometry, dash/rotation, panels, layered images and source color sampling.
- Final four builds: preflight/native checks pass; 129 appearance samples total, no failed
  region. Builds retain review due sparse coverage; GR00T/BLIP-2 retain text-width warnings.

The source-scale comparison crops only the PDF rasterizer's ceil-only canvas edge, never
resizes/registers the measurement images. Showcase thumbnails are for display only. Masks,
thresholds and regions differ by task, so no global accuracy or color guarantee is claimed.

## Checks

Exact before/after behavior: tests/test_vector_details.py, tests/test_icons.py (including a
licensed real GR00T raster fixture) and tests/test_color_sampling.py. Coverage includes native
actual rendering, filled recesses, empty corners, source colors, uniform alpha, gradient alpha,
line alpha, independent editability, fully transparent shapes and rejected topology/fields.

Full final pytest output is in full-tests-final.log. Ruff, schema/activation/package checks,
registry drift, deterministic governance and isolated extracted-package smoke tests passed.
The smoke test resolves imports from the extracted skill, traces the real icon and measures
source#CC94F1. The package itself is a local ignored artifact under dist/.

Package SHA256: `7d13683eedb5efeed943dd18491ecd71d54402daa6e33e5febd88552c2bb9286`.

Security/capability review: image->bounded ROI->selected pixel boundary->validated simple
contour->existing native exporter; color patch->local ICC normalization->target-agnostic sample.
Source files and existing gallery artifacts retained. ROI/memory/edge/vertex bounds, confined
scene assets, fresh outputs and subprocess deadlines remain enforced. Hole/island/corner/
varying-alpha failures cannot silently drop content. Parsers/viewer differences remain
existing dependency risks; scanners are not semantic proof. Paper fixture/license credits are
retained in tests/fixtures/icons/NOTICE.md and each case attribution file.
