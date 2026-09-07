# Scoped security and capability review

Reviewed 2026-09-07. Scope: the complete skill directory and its local runtime, repository setup,
fixtures and packaging scripts. Verdict: no known blocking source-to-sink finding after the
controls below; this is not a claim that native third-party document parsers are sandboxed.

The v0.1.1 delta adds no runtime dependencies or remote capabilities. Font subprocess failures
are normalized and written to fresh report directories. Refined glyph geometry uses a local
Pillow mask capped at 8 million pixels per entry with an eight-entry cache; larger text retains
conservative box geometry. Baked-text overlay, path and existing-output boundaries remain in
place and their negative tests pass. Public test assets have separate source/license notices;
the standalone skill package contains neither fonts nor the external real-case corpus.

The v0.2.0 delta adds no dependencies, credentials or runtime network capability. Rotation is
restricted to quarter turns so rectangular PDF glyph-bound checks remain meaningful. Custom
arrow dimensions and dash/stroke ratios are validated before OOXML serialization; extreme
ratios cannot overflow Office integer attributes. Alpha refinement only reads confined,
text-free local assets, with at most 8 million source pixels and two cached alpha masks;
larger assets retain conservative geometry. Text masks keep the existing 8 million pixel cap.
Tests preserve rejection of actual opaque collisions and baked-text overlays in all three
image fitting modes, including rotated labels. No asset instructions are executed.

The v0.3.0 delta adds no dependencies or runtime external effects. Convex polygon vertices are
bounded to 3–32 normalized points, with every edge checked against all other vertices before
clipping/export. Duplicate, collinear, concave and self-intersecting paths are rejected. Native
linear gradients accept 2–16 opaque color stops in two directions; positions must be distinct
after rounding to Office's 1/100000 units. XML APIs serialize these bounded values and colors.
Text/text refinement transforms the second glyph mask into the first's coordinate frame;
both masks and the transformed output remain under the existing 8 million pixel per-entry
limit. Missing complete masks retain conservative collision geometry. Actual duplicate text
still blocks in horizontal and quarter-turn tests; baked-text checks are unchanged.

The repository-only source fetcher has fixed public URLs and SHA-256 values, writes only to a
new output directory, bounds each download to 25 MB, and checks the hash before parsing a PDF.
It is outside the standalone skill package. MobileViT source/derived artwork stays in local
test output because its downloaded paper's non-exclusive arXiv license was not treated as a
redistribution grant. Its provenance, findings and fetch recipe are documented separately.
The new CLIP/Swin author-repository figures and Matplotlib documentation image have explicit
attribution and complete license notices; the DDPM author-site artwork stays local because a
general redistribution grant was not established. The Matplotlib URL returned two PNG byte
encodings with identical RGB data. The first hash rejection is retained; only the two inspected
byte hashes are allowed, with no arbitrary-content or decoded-pixel acceptance fallback.

## Sources and sinks

| Source | Sink | Enforcement/evidence |
| --- | --- | --- |
| Scene JSON and agent-authored text | OOXML/SVG/XML | Typed schema, duplicate-key/non-finite rejection, XML APIs escape text; injection-like text stays text |
| Scene asset names | Local file reads/copies | Relative POSIX paths confined after symlink resolution; traversal/absolute/URL tests rejected |
| User-selected images | Pillow decoder | Regular-file/type/dimension/pixel/frame limits; EXIF orientation normalized; no network fetcher |
| User-selected PPTX | ZIP/XML parser, Office renderer | Archive size/member/count limits, duplicate/path checks, no extraction, macros/OLE/external links/DTD rejection before renderer |
| User-selected PDF | PDFium renderer | File/page/raster limits; no PDF JavaScript execution interface used |
| Installed fonts | FontTools/Pillow | Selected installed font directories and face metadata; no downloaded font execution or font installation |
| OCR and renderer arguments | Local subprocesses | Fixed tool entry points, argument lists, no shell, deadlines, isolated LibreOffice profile |
| Output directory | Filesystem | New directory required; existing output/user marker preservation verified |
| Skill/image instructions | Agent decisions | Explicitly treat OCR, image text and notes as data; no automatic remote service/credential path |

## Declared versus observed

`skill-card.md` matches runtime reads/writes/commands. No API client, credential-reading code,
automatic agent spawning, global installation, remote publication or source-image upload is
implemented. Dependencies are installed only as an explicit setup step. Python dependencies
are version/hash locked for the reviewed environment; system tools and fonts are reported
separately. Font hashes identify installed data, not a redistribution license.

The local deterministic checks scan Python AST for dynamic/shell execution and source files for
hidden directional controls, check skill metadata/references/schema/registry, and audit bounded
negative inputs. The semantic review additionally traced the above boundaries. A clean scanner
does not establish security on its own. No private content was sent to a semantic scanning service.

## Residual limits

PDFium, Pillow, FontTools and LibreOffice parse complex native formats in the user's process
environment. Size limits and isolated profiles are not an OS sandbox; high-risk untrusted files
should use the caller's existing sandbox. The runtime does not detect a scene author falsely
declaring that a re-encoded image has no baked text. Full-source identical copies and declared
baked-text overlays are checked, and visual comparison remains required.

No known-vulnerability database scan was run in this session; dependency hashes are reproducibility
evidence, not vulnerability evidence. Native target-application verification is tracked separately.
