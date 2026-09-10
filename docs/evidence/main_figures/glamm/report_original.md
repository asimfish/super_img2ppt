# Independent GLaMM CVPR2024 full main figure conversion

Final deliverable: `build_08/` (editable.pptx, SVG, resolved scene, 14 independent cropped assets, real LibreOffice/PDFium preview). This is a reviewable reconstruction, **NOT a source-fidelity pass**. Preflight review / native-object pass / rendered-text pass; 7 raster-text warnings refer to real-world balloon brand markings in photographs. All readable diagram labels, prompt captions, question/response text, and colored phrase text are native editable text. No diagram subpanel was discarded.

## Exact source and rights

Official CVPR2024 paper: https://openaccess.thecvf.com/content/CVPR2024/html/Rasheed_GLaMM_Pixel_Grounding_Large_Multimodal_Model_CVPR_2024_paper.html . **Figure 2, page 4** is the full architecture, with upper image/region/pixel streams and grounded conversation plus the lower referring-expression segmentation, image captioning, region captioning, and phrase-grounding panels.

`source_manifest.json` records official PDF URL and SHA256, scale 6 rasterization and crop `[326,426,3220,1480]` from page 4 (one-indexed), yielding **2894×1054 RGB** pixels. This is white paper, no transparency or black-background ambiguity. No PDF vector coordinates, text extraction, original SVG, or generating code was used as reconstruction answers. The figure was visually verified by opening the complete page raster.

The authors' GitHub `images/glamm/model_arch.png` at commit `1454b456cdd9ae9731915d2b79e9ff3553c3224a` was first inspected. It is **not identical** to the publication: it omits Image-region prompts and Output prompts labels. It was rejected as conversion input; the full published raster was used instead. GitHub root LICENSE is Apache 2.0, saved locally, but this is not evidence that the CVF paper artwork/photographs are licensed Apache. Author/publisher/photo rights remain intact. Keep paper-derived originals and reconstruction assets local for this research evaluation unless rights are separately established; no redistribution license is asserted.

## Frozen procedure and failures

Runtime frozen byte copy at `frozen/`, sealed by `frozen_hashes.json`. Only its SKILL.md and user-facing reconstruction/scene references were read, not implementation or tests. Existing repository venv and existing LibreOffice fonts were used; no dependencies/fonts installed, no API services, no repository edits.

`roi_contract.json` was written before authoring: **39 fixed ROIs** (31 text and 8 connector regions). Acceptance requires both maximum absolute ink-edge difference ≤4 source pixels and dark-ink IoU ≥0.70. RGB max<170 defines dark ink. The actual default PPTX preview (1600×583) is Lanczos-resized back to 2894×1054; no registration/alignment is fitted. These metrics are deliberately strict and retain OCR-box imperfections; excluded combined OCR regions were decided before authoring, not after failed results.

- Build01 failed: strict Courier frames overflowed, omitted panel containers, intentional pyramid occlusions, shadow layers, and connector joins were correctly flagged.
- Build02 failed: after declaring real containers, named source overlaps and correcting mono sizing, one actual T-junction still needed its named source relationship.
- Build03 actual render: review, **3/39 fixed ROIs pass**. Times New Roman/Courier were visibly too narrow/thin. No missing native text.
- Build04 failed: Georgia font candidate required 2.8 extra source pixels for Image-region prompts frame. Corrected within source whitespace.
- Build05 actual render: review, **3/39**. Georgia and Andale Mono, sampled VL/LP gradients, explicit LLM border, thicker native ROI dashes improved appearance but did not satisfy strict source geometry. `fc-match` did not reveal non-system registered LibreOffice fonts; inspection of the explicitly provided font directory found DejaVu Sans Mono.
- Build06 actual render: pass, **3/39**. Final mono font candidate DejaVu Sans Mono improves sans-monospace appearance and source weight. This automated pass is not accepted as visual fidelity.
- Build07 failed: metadata audit declared photographic balloon marks as baked text. The strict image-text rule rejected the blank corner of a two-line question frame and 1 px of empty response frame touching the photo. Kept the failure. Split the question at its existing source linebreak and trimmed empty response frame; no overlap waiver was added.
- Build08 actual render: review, **3/39**. Seven honest photo-text warnings, all native text matches, no font substitutions. This is final.

All eight build directories, failures, source scene snapshots, `command_01..08.json`, build logs and per-build metrics remain. Early prepare/download commands are documented by task transcript and manifests rather than fabricated retrospective process timings. `run_build.py` records subprocess exit codes; its own wrapper exit status is not the CLI exit status. Pillow diagnostic getdata deprecation warnings were emitted and do not invalidate saved metrics.

Typography bounded revisions: initial mono sizing correction, Andale candidate, DejaVu candidate (3); serif one candidate and whitespace-frame correction. Native region-stack stroke received one revision. Metadata-only edits are separated from appearance iterations. No tolerance/ROI threshold or source coordinate registration was weakened.

## Results and limitations

Final **155 objects: 32 text, 87 native shapes, 22 native lines, 14 raster image crops**. The 14 are 9 photographic regions and 5 robot illustrations. Seven photographic regions conservatively declare small real-world printed marks. Token fronts/tops/sides, four feature-pyramid levels with dashed ROI outlines, panel borders, VL/LP gradients and all architecture arrows remain native editable geometry. Connectors have fixed endpoints; moving nodes does not automatically reroute them.

**Fixed source-fidelity result: 3/39 pass, 36 fail.** All three passing regions are connectors. Exact counts and signed edge differences are in `metrics_08.json`; these do not mean 36 semantically wrong regions. They mean the candidate does not meet the declared pixel alignment/shape threshold. Source-sized supplemental actual-PDF raster gives **4/39**, saved separately in `supplemental_sourcewidth_metrics.json`; it does not replace the pre-frozen metric or establish fidelity. The default preview downsampling therefore explains only a small part of the failures.

Remaining visible failures: Georgia is a source-font approximation, with baseline, glyph shape and paragraph word-spacing mismatch; mono word spacing/weight remains imperfect even with DejaVu Sans Mono; some source labels use distributed spacing absent from the reconstruction; the stacked feature surfaces and outline occlusions are native approximations and noticeably differ in depth; shadows are hard flat offsets instead of soft source blur; some borders/arrow sizes differ by a few pixels. The bottom panels preserve all content and layout topology, but are not pixel-exact. No source data values or scientific claims were invented.

Fonts actually used: Georgia and DejaVu Sans Mono regular/bold, no recorded substitutions, no fonts embedded or redistributed. Source font identity cannot be established from pixels alone. Only actual LibreOffice/PDFium was checked; PowerPoint/WPS are unverified.

No demonstrated runtime defect requiring a code change was established. The major failure is authoring/font/source-fidelity capability, while the checker correctly rejects structural problems. Strict baked-text collision checking is conservative with blank multiline frame corners; source-preserving scene splitting resolved that case without suppressing checks.

Final visual inspection opened full preview, dense lower-panel actual crop, region-stack actual crop, and original figure/page. File hashes in `artifact_hashes.json` seal the raw evidence.
