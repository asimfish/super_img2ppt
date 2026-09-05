# Scoped security and capability review

Reviewed 2026-09-06. Scope: the complete skill directory and its local runtime, repository setup,
fixtures and packaging scripts. Verdict: no known blocking source-to-sink finding after the
controls below; this is not a claim that native third-party document parsers are sandboxed.

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
