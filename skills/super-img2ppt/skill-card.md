# Super Img2PPT capability card

Owner: super_img2ppt contributors. Version: 0.3.9. Risk: scoped_change.
Canonical owner: this repository's `skills/super-img2ppt`.

Reads: user-selected image/PDF/PPTX files; scene JSON and relative local assets; installed font
metadata and glyph tables; local tool availability. Does not read credential stores.

Writes: fresh user-selected job/output directories; normalized source PNGs, OCR JSON, scene
snapshots, copied assets, font metadata/hashes, SVG, PPTX, PDF, previews and validation reports.
The renderer creates and removes its own temporary profile. No registry/global configuration changes.

Executes: Python runtime, local `fc-list`, optional `swift`/Apple Vision or `tesseract`, and
headless `soffice`. Subprocess arguments are structured lists; no shell, eval, or arbitrary
scene-provided command execution. Package setup uses the caller's selected virtual environment.

Network: runtime has no network client and no implicit external OCR/image API. Dependency setup
may download declared packages from the configured package index. External service use by an
agent is outside the runtime and requires existing authorization to transmit source images.

Credentials: no environment credential names, secret files, OAuth tokens, or account scopes.

External effects: no sending, publishing, deployment, purchases, permissions, or remote writes.
No automatic host installation or agents. Local source data is retained in the output job.

Approval gates: honor existing user authorization. Conversion to a new local directory is within
the conversion request. Dependency installation follows user environment preferences. External
transmission, publishing, and host-wide installation require separate authority where absent.

Controls: bounded scene schema; duplicate-key/NaN rejection; confined local asset paths including
symlinks; bounded image/page/archive sizes; no archive extraction; reject macros, embedded OLE,
external PPTX relationships and XML DTDs; isolated renderer profile; subprocess deadlines; fresh
output directories; blocking geometric and rendered-text checks; explicit unverified draft status.
Actual PDF font identities and visible text widths are compared with the measured font; spacing
drift requests review. Transparent text-frame whitespace is distinct from colliding glyph regions.

Risks and limits: native image/PDF/font/Office parsers remain dependencies; bounds do not provide
an operating-system sandbox. OCR and source interpretation can be wrong. OCR ink boxes are not
font metrics. Fonts are not embedded. Native PowerPoint/WPS require their own compatibility
evidence. Complex artwork remains raster; the skill cannot promise pixel-identical output.

Output contract: PPTX text/geometry as native objects, separately movable raster assets, SVG with
text/vector elements, portable resolved scene plus assets, font manifest, actual-PPTX preview,
machine validation and a separate visual-review statement.

Curve helper: reads one bounded local image and explicit ROI/color; writes native line
fragments, source hashes, interpolation/exclusion diagnostics and an overlay. No model,
network or new executable dependency. Rejects ambiguous branches and long gaps; output
always requests review and does not claim recovered chart data. Explicit rounded caps
participate in collision/bounds checks.

PDF text diagnostics retain raw extraction and separately normalize only PDFium-confirmed
line-end hyphen sentinels. No expected-text-driven replacement or arbitrary control stripping.
The glyph still participates in font, ownership and overflow checks; missing API confirmation
retains conservative failure. No new dependency, permission or external effect.

Formula helper: reads a bounded local JSON specification and installed font metadata; writes
measured native text parts and baseline/style diagnostics to a fresh directory. No TeX engine,
code execution, network or automatic spacing inference. Rejects unavailable font families,
glyphs or styles, Unicode script shortcuts, duplicate fields and oversized inputs. Ordinary
letters plus explicit script offsets preserve editable typography; actual source comparison
is still required.

Region diagnostics read two bounded local images and explicit ROI/color, write normalized
images/crops/masks and source-coordinate ink metrics. No image registration, resizing or
universal PASS; clipped/empty masks have explicit invalid edge metrics. Caller provides and
attests the actual PPTX render. No new executable, dependency, network or credential behavior.

Diagonal native text extends the bounded rotation field and formula common-pivot placement.
Actual PDF glyph-center ownership uses the rotated frame; width comparison uses common page
axes. PDF glyph rectangles do not prove exact slanted-edge containment, so diagonal text
always retains a visual-review warning; missing text/font substitution still block.

## v0.3.7 editability boundary

Optional semantic groups become native nested PPTX/SVG groups; formula and curve helpers
emit matching group definitions. Group ids appear in the Selection Pane, and editability.json
lists child membership and remaining ungrouped objects. Grouping preserves children and stable
paint order; interleaving groups, repeated parents, cycles and depth above eight are rejected.
No automatic semantic grouping, chart-data recovery, Office equation objects, external-arrow
rerouting or native PowerPoint/WPS UI verification is claimed.

## Optional restyling

Reads an explicit bounded local style plan; writes portable baseline/refined scenes, copied
assets, dual exports and per-field audit. Default build is unchanged. No AI classification,
network or credential behavior. Rich text, content, geometry, image paths and groups cannot
be patched. Semantic color selection still requires visual judgment.

## Semantic redrawing workflow

Opt-in agent-authored candidate scene can replace inconsistent illustrative icons with native
geometry and revise typography/local spacing while preserving content and diagram meaning.
Uses the existing check/build runtime; no automatic redraw CLI, network or extra executable.
Faithful baseline is retained. Region mapping and content coverage require explicit agent
review; static checks do not prove semantic equivalence or aesthetic improvement.
