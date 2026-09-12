# ViNT Figure 2 full editable reconstruction

Final build: `job/build_05`. Actual source-width preview: `job/build_05/actual_source_width.png`. Source: `source.png` (1435×436). Actual exported PPTX → LibreOffice PDF → PDFium raster is 1435×437; the extra bottom row results from PDF page dimension rounding, with no alignment, scaling-to-fit, crop, or registration after rendering.

118 elements: **115 native** (27 text, 63 shapes, 25 lines), plus **3 text-free photographic montages** (83,841 px² = 13.4004% of source area). All readable labels are editable, including both EfficientNet-B0 labels, parameters, dimensions, Greek symbols, rotated Self-Attention, and the complete input/output labels. Every panel and branch of the published Figure 2 is represented. There is no full-image overlay. The photo-region borders, overlapping observation snapshots, and white trajectory inside the output photograph remain raster internally and are disclosed.

## Verification

- Source Figure 2 from PDF page 3 was visually compared with source Figure 1 and selected as the complete architecture rather than the photographic teaser.
- Source-only PDFium rasterization at scale 4, crop [510,275,1945,711]. No source PDF text/vector coordinates or author drawing code were used.
- OCR was locally generated and checked against the source; corrected B0 versus BO and all labels manually.
- Final preflight PASS; native object/content checks PASS; actual LibreOffice rendered-text REVIEW solely for `7 Tokens` measured/runtime visible-width drift (72.75 vs 69.832 px). No blocking failures, missing text, rendered font substitution, or object collision remained.
- Actual whole-page PNG inspected, plus dense Self-Attention crop, encoder labels, token stacks, and output photo/text spacing.
- Five same-coordinate text ROIs measured diagnostically after visual inspection, using RGB max<160 masks. This is not a blind evaluation and no heldout set was used; source regions were visually verified to isolate their labels. Build04 diagnostic is retained. After the final position repair, Self-Attention ink edges are [902,117,923,280] vs source [902,118,923,279], differences [0,-1,0,+1] source px. Other checked edges remain within 3 px. This does not certify glyph similarity or whole-figure fidelity.
- Original build01 preflight failures retained; build02 first real preview retained; build03 actual fc-list timeout error retained; build04 style candidate retained; build05 final. Font-discovery timeout was diagnosed with doctor and recovered on a fresh output build without installation or global configuration changes.

## Remaining visual limits

- Source typefaces cannot be established from pixels. Arial, Arial Italic, Times New Roman Italic (Greek symbols), and Helvetica Neue (vertical attention labels) substitute for the source. Annotation italics and Self-Attention remain visibly heavier than source. Font files are not embedded.
- Some font widths/baselines differ by 1–3 source pixels in the checked labels; unmeasured regions may differ more.
- Stopwatch hand/button geometry and positional-encoding inner curve are native approximations; the latter is a short polyline, not the author's original smooth path.
- Native token colors and rounded card outlines are sampled/approximated visually. Complex local photo internals retain raster treatment.
- LibreOffice verification only; no Microsoft PowerPoint/WPS application verification.

## Reproduction

`bash reproduce.sh /tmp/a_fresh_vint_build` rebuilds the resolved scene and produces an actual source-width raster with the existing repo environment. The exact final raster command is:

```sh
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/vint_full_20260912/raster_actual.py /tmp/vint_full_20260912/job/build_05
```

The script calls `PdfDocument(build/render/editable.pdf)[0].render(scale=1435/page.get_width()).to_pil().save(...)`. Final PDF page size is 960.0094604492188 × 291.6850280761719 points, scale 1.4947769361861478. Attribution/license and source/hash provenance are in ATTRIBUTION.md and provenance.json.

For equal-size gallery comparison, `job/build_05/actual_presentation.png` is 1435×436: only the verified all-white final row was removed by `presentation_crop.py`; original 1435×437 actual is retained. Exact command: `/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/vint_full_20260912/presentation_crop.py /tmp/vint_full_20260912/job/build_05`. No registration or rescaling.


交付路径说明：报告中的 build/job 与 /tmp 路径是独立测试的历史目录。当前目录的 scene.resolved.json 与 assets/ 可直接复建；完整失败和诊断证据位于 [GitHub 测试记录](https://github.com/asimfish/super_img2ppt/tree/main/docs/evidence/embodied_figures/vint)。
