# ADR-005: Explicit appearance regions in actual PPTX validation

Status: Accepted

## Problem
A shared hand-authored palette and lighter strokes passed geometry-only reconstruction QA.
Users also legitimately request recoloring; pixel equality is therefore not always the goal.

## Alternatives
| Candidate | Benefit | Limitation |
| --- | --- | --- |
| Global image/color-histogram similarity | No annotation | White space dominates; object color swaps can preserve the histogram |
| Expected-color mask only | Easy ROI reuse | Wrong-colored ink can disappear from the mask; thin lines confound coverage |
| Explicit regions, independent background-based ink extraction | Detect hue and coverage independently; auditable target overrides | Agent must isolate regions; partial coverage is not full-page acceptance |

Choose the third. Keep an external versioned JSON plan passed to `build --appearance-plan`.
No scene-schema changes or dependency additions. Pure region measurement is separate from
plan validation and actual PDF rasterization. Faithful/target modes are per region, and target
mode requires an explicit RGB and reason. Unknown options and invalid samples fail closed.

Source-backed builds without the gate remain usable but report review/not_run, avoiding the
previous implication that geometry PASS also validated color. Checks never recolor images,
change QA exemptions or write source inputs. Files stay local; no image service or credential
access. Input references use existing root-confined paths and explicit image/ROI/render bounds.

Scope is selected flat/isolated single-color regions. Defaults are engineering thresholds,
not calibrated perceptual acceptance; preserve visual review and report uncovered slides.
