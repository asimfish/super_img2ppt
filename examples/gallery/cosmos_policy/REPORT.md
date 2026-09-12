# Cosmos Policy full Figure 2 conversion

Final artifact: `build_04/editable.pptx`. Automated status **pass**, visual status **reviewed with remaining font/glyph differences**. No claim of pixel-identical fidelity or native Microsoft PowerPoint/WPS verification. Actual PPTX rendered through LibreOffice, then its PDF rasterized at the source width.

## Source and rights

Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, Jinwei Gu. *Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control and Planning*, arXiv:2601.16163v1, submitted 22 January 2026 18:09:30 UTC. https://arxiv.org/abs/2601.16163v1 . Paper license: **CC BY 4.0**, explicitly linked as “Rights to this article” in archived `arxiv.html`, line 178. License: https://creativecommons.org/licenses/by/4.0/ . This is a modified, editable reconstruction with raster crops, not an author-endorsed original.

The official ICLR 2026 PDF was separately downloaded as `iclr-official.pdf` and its page 4 visually inspected. Its Figure 2 has the same panel/row structure. The frozen conversion source is the dated arXiv v1 PDF, not a silently swapped conference document. All PDF hashes, URLs and crop coordinates are in `provenance.json`. Figure 2 is the complete main method figure; the caption and prose beneath it are outside the figure crop. It depicts conditioning, action generation, future-state prediction and value prediction; it does not depict the separate planning search algorithm, so no invented planning structure was added.

## Coverage and editability

Both full conditioning/target panels, all three rows, 6 image stacks, 10 latent tiles, 10 partially-noised tiles, all readable labels, injection heading, branching arrows, VAE/noise transitions and the state/action/future/value bracket labels are present. Final inventory: **31 native text objects, 6 native shapes, 19 native lines/arrows, 26 image assets**. Parent panels contain their labels and images; red frames contain their texture crops. Specific source-supported bus/tick intersections are declared; no blanket exemptions were used.

The 6 camera stacks and 20 photo/latent/noise tiles remain independently movable raster images. Their internal photographic/texture geometry is not editable. All visible meaningful text is native; no readable figure label is intentionally baked into these crops. No source PDF text or vector coordinates, author drawing code or external OCR/image services were used.

Font identity cannot be determined uniquely from pixels. Reconstruction uses Arial regular/bold and Times New Roman regular/italic, with no runtime substitutions. Native styled runs preserve bold red “latent injection,” italic variables, upright parentheses and visible prime marks. Times New Roman prime/glyph spacing differs from source, particularly `V(s′)`; no exact formula-font claim. Fonts are listed with hashes in `build_04/fonts.json`, not embedded or distributed.

## Actual quality evidence

Source: 1195 × 476 pixels. Actual exported PDF rasterized with PDFium `scale=1195/page_width`: also **1195 × 476**, so no white-row rounding, cropping correction or registration was needed. `comparison_sourcewidth.png` stacks source above actual; `detail_comparison.png` places source left and actual right. Full and detailed images were opened and visually inspected after the final build.

Frozen regions and unchanged black-ink threshold (`max(R,G,B)<150`) are in `measure.py`; `build_02/measurements.json` retains the first successful candidate. Final edge deltas [left,top,right,bottom], in source pixels:

| Region | Delta | Ink IoU |
|---|---|---:|
| conditioning title | [0,0,-1,1] | .347 |
| small current-wrist label | [-1,0,0,0] | .387 |
| injection heading black portion | [1,-1,-4,0] | .318 |
| state `s` | [-1,0,0,-1] | .719 |
| value `V(s′)` | [1,0,-1,0] | .228 |
| rotated VAE label | [1,-1,0,-1] | .327 |
| noised-frame multiline block | [0,0,0,-1] | .728 |
| injection bus ROI | [0,0,0,-1] | .950 |

These are diagnostic measurements, not an invented universal acceptance threshold. Low glyph IoU despite close bounding boxes exposes remaining font shape/spacing and antialiasing differences. The bus ROI includes adjacent ink and is not claimed as a pure shaft metric. Injection title is still about 4 pixels shorter than source. Photo tiles also undergo actual document image resampling. The final faint panel stroke approximates the source's very fine antialiased gray border.

## Forward-test findings and bounded repair

1. `build_01`: legitimate preflight fail: 4-line text requires 77.5 px height including reserve, authored frame was 76 px. Failure preserved in validation; author.py reproduces original scene.
2. `build_02`: increased that frame to 79 px; actual render passed. Visual inspection nevertheless found title right edge −13 px, VAE rotated position +9 px, multiline bottom +3 px. This demonstrates why automated pass must remain separate from visual fidelity.
3. `build_03`: targeted font-size/position correction, explicit black text color, split four semantic lines on observed 18 px spacing, sampled panel fills. All checks passed; large displacement reduced to the metrics above. The skill's minimum real font line-height made source 18 px spacing unsuitable for a single paragraph at this font; semantic line boxes preserve the observed baseline spacing without weakening checks.
4. `build_04`: restored faint native panel outline observed during final comparison. All checks passed; measured text results unchanged. No region received three unresolved repair cycles.

No reproducible runtime correctness bug was demonstrated in this case. The strongest observed limitation is font/glyph fidelity surviving automated pass, especially mathematical primes. OCR also missed/misread several small labels and injection text, corrected solely against raster. The local diagnostic script initially assumed NumPy, absent from the existing environment; it was rewritten with Pillow/Python sets, with no installs. This is harness setup, not a package defect.

## Reproduction and deliverables

Run `zsh reproduce.sh` from any location (new `rebuild_01` directory required). Existing repo environment is used; no package installation, repository edits, push or subagent work occurred. `raster_source.py` reproduces the exact source raster/crop from the archived PDF. `author.py` preserves the first authoring recipe; `repair.py` preserves the main visual repair. The final editable source scene and assets are `job/scene.json` and `job/assets/`; build_04 additionally contains the path-resolved scene, SVG, fonts, validation, actual PDF, default runtime comparison, full source-width comparison and detail comparison. Failed/intermediate build directories remain intact.
