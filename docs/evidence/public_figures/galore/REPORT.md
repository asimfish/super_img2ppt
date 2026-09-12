# GaLore Figure 6 — complete four-panel forward test

Publisher source: https://proceedings.mlr.press/v235/zhao24s.html . Zhao et al., ICML 2024, PMLR 235:61121–61143. Complete Figure 6 on printed page 21, caption excluded; panels LLaMA-130M, LLaMA-350M, LLaMA-1B and LLaMA-7B.

License: CC BY 4.0 under the PMLR publication agreement. See SOURCE_LICENSE.md and archived publisher HTML. Source author names, original publication and hyperlink must accompany any README publication; reconstruction changes must be identified. Fonts are neither embedded nor redistributed.

## Reconstruction boundary

1170×860 source pixels. 74 native text objects, 4 native legend shapes, 675 native line fragments and one exact original raster crop in the current candidate. Every readable label is editable. Chart traces represent observed visual stroke geometry, not recovered numeric training data or Excel-linked charts. All four panels and all 11 visibly plotted series are retained.

A 158×115 pixel local crop (1.8058% of page area) preserves ambiguous blue/brown crossings in LLaMA-7B, including short grid fragments. It contains no text. Underlying native strokes are clipped outside its rectangle; no duplicate visible chart content is overlaid. Its interior is not editable. Other short fully occluded blue intervals remain disjoint visible native fragments; no trajectory behind the brown foreground curve was invented.

## Actual verification and limits

Actual PPTX exported through LibreOffice to PDF, then rasterized to source width 1170. PowerPoint/WPS not independently verified. Final candidate is chart/build04. Automated structural/text checks pass. Earlier build02/build03 revealed small white seams at native line joins. The reusable line_cap round implementation removed those seams in the actual build04 render without extending source paths. Small pixel-trace stair steps remain, so this is not claimed as exact curve geometry.

Source font identity cannot be inferred uniquely. Times New Roman resolves without substitution; chosen from visual appearance and measurement. Font/position calibration used frozen development regions and stopped after limited repairs. Candidate title130 IoU .829 and axis IoU .977 pass edge≤4 px AND IoU≥.70. X label IoU .488 and legend IoU .606 fail despite edges within 1 pixel. Recorded heldout title350 .769 passes; legend7b .495 and tick1b .559 fail. Exact values are in roi-metrics.json; do not advertise strict all-region fidelity success.

Evaluation limitation: development and first heldout ROI coordinates were frozen before authoring, but the calibration evaluator printed both groups during calibration. No local heldout-only repair was applied, but the heldout was not fully blind. Those original heldout regions are therefore treated as already-exposed recheck regions. Three additional diagnostic regions were selected only after final candidate hashes froze and were measured without further repair; this does not restore an overall blind-evaluation claim.

## Forward-test failures preserved

- Initial color tolerance80 included gray grid pixels and was rejected as ambiguous. Tolerance35 excludes that known distinct color; this is source-color isolation, not deletion of chart structure.
- Original x-only helper rejects one contiguous steep brown stroke (x120, y35–64, 30 pixels) due to 24-pixel span limit. Reusable axis='y' now handles steep source fragments with coordinates mapped by the runtime.
- Long hidden blue gaps: 130M x226 onward (11 columns) and 7B x980 onward (8 columns) were not interpolated. Visible runs were split.
- Two 7B blue crossing/occlusion fragments still reject as ambiguous, even with proper axis direction. These are preserved in the declared small original crop.
- Initial build had true frame out-of-bounds and missing named grid/legend occlusion relationships. Subsequent checks corrected geometry bounds and source-supported named crossings. No broad text/text blanket exemptions.

Files: chart/build04/editable.pptx, svg/page_001.svg, scene.resolved.json, assets/, fonts.json, validation.json, render/editable.pdf and actual-sourcewidth.png. COMMANDS.md plus author/trace/merge/measure scripts record reproduction steps. Failures and previous candidates remain separate fresh directories.

## Final frozen candidate and extra diagnostics

Candidate: chart/build04; PPTX SHA256 `dd68ed32d6c99207dc93d7221955e7dbc7d77567d269df79dffaa930d62bb693`; resolved scene SHA256 `f2961a9a9acf7c70234483c64c0d7dcbaceb8f18340854ac10f6be76741cdbc4`. Full hashes and freeze time are in candidate-freeze.json.

After freeze, additional diagnostics: green130 isolated curve IoU .949, edge 0 px (pass); title1b IoU .534, edge 2 px (fail); ylabel7b IoU .384, edge 2 px (fail). See additional-contract.json and additional-metrics.json. No post-freeze edits or retests were made. These failures distinguish correct content/editability from strict glyph-level fidelity.

Forward-test summary: complete, visually reviewable, mostly native editable figure; automated checks pass; strict regional fidelity target fails on several text regions. Suitable as an honestly labeled complex reconstruction example, not as evidence of universal near-pixel accuracy.
