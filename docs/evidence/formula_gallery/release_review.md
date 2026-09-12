# v0.3.5 scoped release review

Requirements frozen for this change: add three complete embodied-paper cases, improve the
reported Diffuser Actor formula styles without baking text, turn measured baselines/styles
into reusable support, publish actual comparisons and reviewable files, preserve prior cases.
Exact source glyph identity is not claimed; observed residual differences remain prominently
reported. Formula typography has improved, but complete source-format fidelity is unachieved.

Changed execution surfaces: a bounded local JSON-to-native-text composer and its CLI route.
It reuses existing font discovery/measurement and fresh-directory behavior. No dependency,
network destination, credential read, external process type, auto-install or host mutation is
added. Explicit styles prevent ordinary variables/punctuation inheriting blanket bold/italic.
The composer does not execute formulas, parse TeX, auto-recognize content or assert that local
font availability proves Office font selection. Source PDF downloads and GitHub publication
are part of this authorized development task, not new runtime behavior.

Semantic review: unknown keys, duplicate keys, nonfinite values, oversized files/parts,
control characters, unsupported script shorthand, unavailable glyphs/styles and reused
outputs fail explicitly. Font fallback cannot silently satisfy the requested single family.
All composed outputs remain unverified; full preflight, native-object, actual-font and
source-image review are still required. The strict family restriction has an explicit
boundary: independently compose a disclosed symbol family when necessary, never replace
U+223C with ASCII tilde or describe mixed glyphs as perfectly uniform. No critical/high
finding identified in the changed capability; static audit alone is not this conclusion.

Ownership/activation: this extends existing image-to-editable reconstruction, without a new
synonym skill or broadened trigger. The eight existing activation cases retain four positive
and four adjacent negative boundaries. Independent forward tasks reconstructed full real
figures. A separate source-only formula task exercised missing glyphs, renderer replacement
and collisions; it reported incomplete fidelity and stopped after three repairs. No expected
formula layout was supplied to that independent task.

Verification: repository lint/format, full 101-test suite (including 11 new formula tests),
static skill verification, governed-skill audit, registry check and quick validation passed.
Four frozen gallery scenes rebuild pixel-identically to their own actual previews. Twelve
PPTX ZIPs, source/actual dimensions, 214 gallery hashes and deterministic gallery archive
rebuild passed. Eight original cases and fourteen previews remain unchanged from 56712f5.
See verification.json, replay.json, artifact_checks.json and package_smoke.json for commands.
The first isolated package harness used a nonexistent --version option; the documented doctor
command replaced it. This was a harness correction, not a runtime repair.

Release gate PASS for the scoped native-part capability and reproducible gallery artifacts.
This verdict does not attest complete formula/source fidelity or Microsoft PowerPoint/WPS
compatibility. Native PowerPoint/WPS, other machines' fonts, and automatic mathematical OCR
are unverified/unsupported. Private user manuscript figures and font binaries are excluded.

A second isolated harness attempt retained the unrelated flow example's source_02.png
reference; asset containment correctly failed. The formula-only harness now omits that
unrelated source field. The failed validation is preserved in package_smoke_template_failure.json.
No renderer, asset boundary or font threshold was relaxed for either harness correction.

The isolated package smoke reuses an existing dependency environment without installing.
`doctor` reports its installed distribution metadata (0.3.4); a separate import-identity check
confirms that both the runtime and new math module execute from the extracted 0.3.5 package.
That path/version assertion and command are recorded in package_smoke.json. This smoke
verifies unpacked-package execution, not a fresh dependency installation.
