# Super Img2PPT capability card

Owner: super_img2ppt contributors. Version: 0.3.4. Risk: scoped_change.
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
