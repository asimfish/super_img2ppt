# Architecture and decision record

Status: accepted, 2026-09-05. Runtime input is a versioned JSON scene in source pixels.

## Decision 1: independent reconstruction runtime

| Candidate | Benefit | Cost |
| --- | --- | --- |
| Adapt upstream runtime and worker state machine | Existing orchestration and asset processing | Coupled remote OCR/image services, heuristic font fitting, preview/output mismatch |
| New local runtime with agent-authored scene | Explicit coordinates, measurable fonts, controlled dependencies, portable skill | Agent still needs to interpret shapes and correct OCR; no universal automatic image parser |

Choose the new runtime. Upstream is researched, not vendored. The agent owns semantic
recognition; deterministic code owns validation, layout, export and rendering. Complex
photos remain individually movable raster assets. The repository is not a competing
paper-to-slides or slide-design skill.

## Decision 2: preserve positions and reject unresolved collisions

Compare automatic global reflow with explicit container/overlap relationships. Reflow can
change chart semantics or arrow destinations. Choose fixed source coordinates, measured
font fitting within an explicit minimum, shared scale for a typography group, and blocking
reports for unresolved overflow/collisions. The agent repairs the scene based on the source.
Intentional overlap requires named pairs and a reason, or a geometrically valid container.
Text-frame whitespace can intersect if its measured visible ink remains separate. This narrow
exception does not relax frame containment or the check against duplicated baked image text.

## Decision 3: validation from the actual artifact

Compare a Pillow mock preview with opening the emitted PPTX through LibreOffice and
rasterizing the resulting PDF. Choose the latter as the automated renderer, behind a
renderer Protocol. Pillow measures font metrics and makes comparison images; it does not
claim to emulate PowerPoint. Native PowerPoint and WPS are separate compatibility checks.
PDF and SVG previews do not prove editability: inspect PPTX text/shapes separately.
Compare PDF font identifiers and visible ink widths with the selected face, since text content
alone misses substituted fonts and mixed-script spacing. Width drift requests visual review;
do not insert per-character spacing guesses into the exporter.

## Module boundaries

`prepare` normalizes image/PDF/PPTX pages, preserves notes, and produces OCR hints.
OCR adapters implement one Protocol and are selected from a small explicit registry.
`scene` validates bounded local data and asset paths. `fonts` resolves real local font
faces and glyph coverage. `layout` computes explicit lines and fit decisions.
`qa` checks geometry and native objects. `export` writes native PPTX objects and SVG.
`render` invokes a local renderer with isolated temporary state and bounded subprocesses,
then checks the rendered PDF text, font identifiers and glyph bounds.
`cli` coordinates these modules and writes a fresh output directory.

The standalone skill includes the runtime package and schema; it does not depend on
sibling repositories, user credentials, an agent spawning feature, or external OCR APIs.
Parameters affecting fidelity live in the scene or typed configuration defaults.
