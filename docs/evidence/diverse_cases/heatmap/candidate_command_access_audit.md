# Candidate access audit

- Candidate skill root: `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v030-candidate-k50on3nk/super-img2ppt`.
- Read only candidate `SKILL.md` and `references/scene.md`; original workflow/schema references were already read for the frozen baseline. Did not inspect candidate runtime-source contents or tests.
- Exact substantive argv, environment, stdout, stderr, exit codes, and durations are in `candidate_commands.jsonl`; the command-local `PYTHONPATH` points to candidate `src`.
- Wrote only temporary analysis/authoring scripts: `run_logged_candidate.py`, `author_candidate_01.py`, `measure_colorbar_candidate.py`, `author_candidate_02.py`, and `write_candidate_report.py`; these scripts preserve exact execution code. Candidate job/build/measurement outputs are separate from all original outputs.
- Reused the unmodified `measure_candidate.py` and original 72-ROI plan to compare original and candidate renders. The source and ROI-plan hashes are rechecked during report generation.
- A read-only Python one-liner printed original label-edge deltas and sole-source endpoint pixels at y97–101 and y452–456. This identified original black-border antialiasing in y98/y455; no plotting/source data were consulted.
- `view_image` opened actual candidate PPTX renders for candidate 01 and candidate 02, and candidate 02 colorbar/dense matrix comparisons. These renders come from LibreOffice opening the actual PPTX, then its PDF rasterization.
- `measure_colorbar_candidate.py` reads only own generated PPTX/SVG XML to verify the single native `gradFill`, 16 stops, 64 native text elements, and one top-label image. It does not alter the PPTX after export.
- Candidate skill file bytes are hashed opaquely for provenance; no source semantic inspection. Runtime code/manifests must match the initial frozen candidate hashes at the end. Python bytecode/cache files are excluded from semantic runtime hashes.
- Candidate report is separate from `report_original.md`; original evidence seal is verified after candidate work.
