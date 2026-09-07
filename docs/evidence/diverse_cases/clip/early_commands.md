Before the structured runtime logger was added, these commands were executed with the frozen runtime:

```sh
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python -c 'import tempfile; print(tempfile.mkdtemp(prefix="super-img2ppt-diverse-clip-",dir="/tmp"))'
PATH=/opt/homebrew/bin:$PATH PYTHONPATH=/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/src /Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt prepare /Users/liyufeng/Code/super_img2ppt/output/diverse_cases_20260906/raw/clip_CLIP.png --out /tmp/super-img2ppt-diverse-clip-f11ta96b/job
PATH=/opt/homebrew/bin:$PATH PYTHONPATH=/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/src /Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt doctor
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-diverse-clip-f11ta96b/reconstruct_01.py
PATH=/opt/homebrew/bin:$PATH PYTHONPATH=/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/src /Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt check /tmp/super-img2ppt-diverse-clip-f11ta96b/job/scene_01.json --out /tmp/super-img2ppt-diverse-clip-f11ta96b/job/check_01
```

`prepare` exited 0 with `needs_reconstruction`, one page and macOS Vision OCR. `doctor` exited 0; its reported package/tool versions are retained in `provenance_original.json`. Reconstruction exited 0 with 311 scene objects and 30 fixed ROIs. `check_01` exited 2 with six explicit front-text/back-card overlap errors; its complete original validation remains in `job/check_01/validation.json`.

Two exploratory measurement commands failed before producing measurements: one imported unavailable NumPy (`ModuleNotFoundError: No module named 'numpy'`); the other had a Python conditional-expression syntax error. No dependency was installed. The measurement was rewritten using Pillow and the standard library. Neither error was a frozen-runtime failure.

The first `measurements_build_02.json` XML counter called every `p:txBody` a text box, including empty text bodies attached to shapes. Its `text_boxes: 280` field must not be interpreted as 280 editable text contents. The final measurement script explicitly counts nonempty `a:t` content, yielding 131 text objects, and retains the earlier JSON without replacement.

All subsequent runtime commands, timestamps, exit codes, environment overrides and stdout/stderr log paths are in `commands.jsonl`. Runtime operations used the `python -m super_img2ppt` module with an explicit frozen `PYTHONPATH`.
