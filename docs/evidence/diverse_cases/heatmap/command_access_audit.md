# Command and access audit

Substantive runtime/analysis commands have exact argv, environment overrides, working directory, stdout, stderr, exit codes, and durations in `commands.jsonl`. Scripts written for this run are retained verbatim in the temporary root. `candidate_commands.jsonl` will separately record any later candidate-runtime work.

The following read/setup/visual operations preceded original report sealing and were not invoked through the subprocess logging wrapper. Their exact timestamp is not asserted:

- `cat` of the original frozen `SKILL.md` and `references/reconstruction.md`, `scene.md`, `qa.md`, `scene.schema.json` under `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/`.
- `mktemp -d /tmp/super-img2ppt-diverse-heatmap-XXXXXX` produced this root.
- Shell heredocs wrote `run_logged.py`, `inspect_source.py`, `precommit_evidence.py`, `source_ink_metrics.py`, `author_scene_01.py`, `measure_candidate.py`, and `freeze_original_report.py` only in this temporary directory. Those files contain the exact executable code.
- `cat` read the temporary job's `prepare.json`, `pages/page_001/ocr.json`, `scene.json`, `check_01/validation.json`, and `check_01/fonts.json`.
- An inspection-only Python one-liner read `build_01/validation.json`, printed report content, and listed files beneath that generated output directory.
- An inspection-only Python one-liner opened the newly generated `build_01/editable.pptx` ZIP and read `ppt/slides/slide1.xml` with lxml. It printed shapes named `colorbar_band_100` and `cell_r1_c1` to inspect their own output fill/line XML. It did not inspect runtime or source plotting code.
- `view_image` opened the sole raw supplied image, `job/pages/page_001/source.png`, the actual `build_01/render/page_001.png`, and the generated `measurements_build_01/colorbar_source_vs_actual_2x.png` comparison crop. The comparison includes source-left/actual-right and is not an independently rendered mock.
- Read-only hashing traversed the frozen skill directory and hashed file bytes without interpreting or printing runtime-source content. Exact per-file hashes are in `provenance.json`. No other case or plotting source data were accessed.

`original_artifact_hashes.json` was generated inside `freeze_original_report.py` before the logging wrapper appended that command's completion record. Its `commands.jsonl` entry therefore identifies the command-log prefix at report generation, not the final sealed command log. `original_evidence_seal.json` records the authoritative final hashes of the original report and sealed command log. It does not alter the original report.
