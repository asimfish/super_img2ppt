以下为本次实际使用的命令及输出目录。未安装依赖；未向外部服务提交图片。

```sh
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt doctor

PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt prepare /Users/liyufeng/Code/super_img2ppt/output/conference_cases_20260906/raw/spatial_mamba_figure_4.png --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/job

/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_scene.py

PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt check /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/check_01
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt check /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/check_02
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt check /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/check_03

PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.hybrid.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_hybrid_01

/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native.py
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.native_01.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native_01
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.native_02.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native_02
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/super-img2ppt-conference-spatial-jzSWZJ/job/scene.native_03.json --out /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native_03

/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-spatial-jzSWZJ/measure.py /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_hybrid_01
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-spatial-jzSWZJ/measure.py /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native_01
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-spatial-jzSWZJ/measure.py /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native_02
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/super-img2ppt-conference-spatial-jzSWZJ/measure.py /tmp/super-img2ppt-conference-spatial-jzSWZJ/build_native_03
```

每次 build/check 均写入新的目录。最终场景重建时应使用另一个新的输出目录；上面的已存在目录不能当作新运行目标。

`scene.native_02.json` 根据 `build_native_01_measurements/anchors.json` 修正，具体内容在 `repair_02.json`。`scene.native_03.json` 根据 `repair_03.json` 收紧 L 的透明框并添加显式箭头尺寸。`build_scene_01.py` 是消除 NumPy 依赖之后、修复几何误检之前的完整作者脚本。最初缺包的终端异常转录在 `authoring_failure_00.txt`；当时的 NumPy 脚本未另存，不能以当前脚本重放该异常。所有实际完成的场景生成均使用标准库和 Pillow。
