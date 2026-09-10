# Third-Party Notices

The skill code and instructions retain the upstream [MIT-0 license](LICENSE).
This does not relicense third-party assets or source papers. Per-asset provenance
and usage terms remain in `references/vector-library/icon_canonical_index.jsonl`
and the corresponding asset cards.

| Source | Shipped canonical records | Terms and notices |
| --- | ---: | --- |
| Tabler Icons 3.44.0 | 183 | [MIT notice](licenses/tabler-icons-MIT.txt) |
| Lucide static 1.16.0 | 3 | [ISC and Feather-derived MIT notices](licenses/lucide-ISC-MIT.txt) |
| Upstream generated SVG icons | 388 | Original generated-asset terms in each record |
| Legacy local-workspace icons | 14 | Original local-project terms; independent redistribution grant not verified |
| Paper-derived motif abstractions | 100 | Original visual-abstraction terms; not licenses to copy source figures |

The 14 legacy local-workspace icons are inherited unchanged from the pinned
upstream artifact. Their records explicitly limit redistribution claims. Do not
assume the root MIT-0 license grants broader rights to these assets. Clarifying
or replacing this legacy subset is an open provenance task. The new public
showcase does not embed these icons or any original paper figures.

## Modifications

The upstream imported-icon metadata records tight bounding-box cropping and
explicit-stroke PPT-safe variants. This release preserves that metadata and adds
the full notices retrieved from these versioned sources:

- [Tabler v3.44.0 license](https://github.com/tabler/tabler-icons/blob/v3.44.0/LICENSE)
- [lucide-static 1.16.0 license](https://unpkg.com/lucide-static@1.16.0/LICENSE)

## Public Render Examples

The images in `examples/images/` were generated for this repository from
independently written prompts grounded in public papers. They are AI-generated
conceptual explanations, not reproductions of the authors' original figures or
experimental outputs. Source links and section anchors are recorded in
`examples/manifest.json`. No unpublished user manuscript is distributed here.

New project-authored prompts and documentation use the root license. Generated
sample images are shared under MIT-0 to the extent the maintainers hold applicable
rights; this is not a warranty of exclusivity, copyrightability or publication
acceptance. Paper authors retain rights to their source publications. No paper
author, conference, OpenAI, Tabler or Lucide endorsement is implied.

## Recent Figure Study

The [2025-2026 study](https://github.com/asimfish/super_teaser/blob/main/docs/research/2025-2026-figure-study.md) records source
links, PDF identities and independently written structural observations. Source
PDFs and figure screenshots were inspected locally, not imported into this
repository or its runtime bundle. The new generic composition recipes do not
grant any rights to copy the source publications' figures, photographs, logos
or experimental outputs. The Findings entry and the separately verified WMPO
preprint/acceptance record are identified explicitly in the study ledger.

## Paper-Craft Method Study

High-level methods from `zsyggg/paper-craft-skills` informed independently written
instructions. Its README MIT statement lacks a full license/copyright notice at
the reviewed commit, so no text, code or images from that repository are shipped.
See `UPSTREAM.md` for the exact commit, reviewed scope and no-copy boundary.
