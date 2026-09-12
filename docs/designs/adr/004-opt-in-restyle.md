# ADR-004: Independent audited restyling

Status: Accepted

## Context
Users want an optional less decorative, more consistent academic figure conversion,
while retaining faithful conversion and editable atomic objects.

## Candidates
| Approach | Benefit | Cost |
| --- | --- | --- |
| Automatically restyle every build | Single command | Changes faithful behavior; may destroy semantic colors |
| Agent-authored explicit plan and independent restyle command | Auditable targets; preserves baseline | Requires visual judgment; raster artwork stays unchanged |

## Decision
Use the second approach. `apply_plan(scene, plan)` returns a new scene and field audit;
`stage_variants` copies local assets; CLI builds both variants with existing QA.
Canonical boundaries remain scene JSON and a versioned JSON style plan. No new dependency.
Text content, geometry, groups, ordering, image paths and QA exemptions cannot be patched.
Rich text is protected to preserve formula scripts and symbol styles. Reset refined review
state. Always require visual review; visual differences are intentional, not fidelity scores.
Existing build behavior and frozen gallery cases are untouched.

## Limits
The agent selects coherent targets and verifies meaning, including semantic colors.
This initial executable layer adjusts style, not automatic layout or raster regeneration.
Geometry redesign requires a separately authored scene and explicit disclosure.
