# LoRA 独立前向测试原始报告

输入是 super_teaser 生成示意图，不是论文原图。仅读冻结 skill 的 SKILL.md、三个 references、指定原图及本任务产物；未读实现、测试、其他案例或上游 prompt。未安装依赖/字体、未修改主仓库/冻结skill、未上传。

## 结果

选择 build_05，实际 LibreOffice PPTX→PDF→PNG，自动 pass，独立保真评估仍不通过：冻结18个ROI中 8/18 同时满足边界误差≤3源像素、暗像素IoU≥0.70。首次可渲染 build_04 为3/18，原指标保留不覆盖。ROI在 scene 编写前写入 rois_frozen.json，始终同坐标、同阈值。渲染图归一化回1536×1024，Lanczos采样后以所有RGB通道<110提取暗像素。边界差按左、上、右、下；底边是可见墨迹底边，不冒充字形学基线。抗锯齿对IoU敏感，不能将低IoU全部解释为抗锯齿。

76个可移动元素：15个原生文字、13个原生形状、45条原生线、3个独立图片。W0通过主文+单独原生0下标表示，未栅格化正文。锁图标、Frozen图例色块、Trainable图例色块保留精确独立源图裁切，内部不可编辑。无全页背景图片。灰/青/红矩阵保留格数与位置，源纹理被纯色近似，连接圆角被直角近似。

实际打开 build_04/render/page_001.png、build_05/render/page_001.png 与 build_05/dense.png 逐字检查。内容为 x, h, Frozen W₀, d x k, Trainable A, r x k, Trainable B, d x r, alpha/r, Frozen, Trainable, h = W₀ x + (alpha/r) B A x。字符0均为数字且位于下标位置，不是字母o；无其他上下标。A为2×6格、B为7×2格、W为4×6格；输入输出各三点省略。仍有字体字重/字距差异，公式W₀间距偏大、后半段与源字距不一致；A/B标题、alpha与图例不是逐像素对齐。未见未声明真实文字交叠或裁切。

## 字体与运行环境

Python 3.12.12, super-img2ppt 0.3.0, python-pptx 1.0.2, Pillow 12.3.0, fonttools 4.64.0, pypdfium2 5.13.0, jsonschema 4.26.0。LibreOffice LibreOffice 26.2.4.2 0229ac93fcf0d7cbc6376066c6f35021cef002dc
字体实际为 Arial.ttf (400) 与 Arial Bold.ttf (700)，fonts.json substitutions=[]，不是 DejaVu 替换。源字体身份未知。字体没有嵌入；未做 PowerPoint/WPS 本机检查。

## 原始失败与修正上限

build_01 exit2: 圆点z与容器同层，container must be a shape behind its content。仅升圆点z。
build_02 exit2: plusH allow_overlap_with误含自身，invalid element reference plusH。仅移除自引用。
build_03 exit2: title measured width162+0.5>160且与下标真实交叠。仅按源像素缩34字号，未豁免交叠。
build_04 exit0/pass: 首次可渲染，18ROI仅3通过。build_05按此测量调整标题y、下标y、标签字号、公式宽度、若干箭头笔画与头宽，18ROI仅8通过。
标题至多2次局部修正；其他区域≤1次（结构错误各自1次）。未用反复降低阈值/最小字号取通过。
自写审计脚本首次import numpy失败（当前环境无numpy），改成Pillow+Python集合运算后成功；这是审计脚本依赖假设错误，不是skill运行时缺陷。未发现可复现运行时缺陷。前三次场景报错均正确拒绝，不能归咎运行时。

## 固定ROI终次测量

|ROI|边界差 l/t/r/b (px)|暗像素IoU|合格|
|---|---|---|---|
|title|[-2, 1, 0, 0]|0.7577|True|
|x|[-1, 0, 1, 0]|0.7828|True|
|h|[-1, 0, 1, 0]|0.7273|True|
|dimW|[-1, 1, 0, 1]|0.7897|True|
|labelA|[0, 0, -2, -1]|0.4550|False|
|labelB|[-2, 0, 0, -2]|0.4526|False|
|dimA|[0, 0, -2, 0]|0.4135|False|
|dimB|[-1, 0, -1, 0]|0.6430|False|
|alpha|[-1, 1, -1, -2]|0.5181|False|
|legendFrozen|[-1, -1, 1, -3]|0.3005|False|
|legendTrainable|[0, 0, 1, -2]|0.4918|False|
|formula|[-1, 0, -3, 2]|0.1816|False|
|gridWtop|[0, 0, 0, 0]|0.5998|False|
|gridAbottom|[0, 0, 0, -1]|0.4930|False|
|gridBleft|[0, 0, 0, -1]|0.7281|True|
|upperArrow|[1, 0, 0, 0]|0.9923|True|
|outputArrow|[0, 0, -1, -1]|0.8280|True|
|lowerArrow|[0, 1, -1, -1]|0.9520|True|

## 可复现命令与时长

所有CLI经run.py固定命令局部PATH与PYTHONPATH，详见command_*.json。

- `prepare /Users/liyufeng/Code/super_img2ppt/output/teaser_cases_20260910/raw/examples/images/lora-clean.png --out /tmp/lora-forward-LO8vEs/job` → exit 0, 8.759s
- `doctor` → exit 0, 0.254s
- `build /tmp/lora-forward-LO8vEs/job/scene.json --out /tmp/lora-forward-LO8vEs/build_01 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` → exit 2, 0.205s
- `build /tmp/lora-forward-LO8vEs/job/scene.json --out /tmp/lora-forward-LO8vEs/build_02 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` → exit 2, 0.314s
- `build /tmp/lora-forward-LO8vEs/job/scene.json --out /tmp/lora-forward-LO8vEs/build_03 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` → exit 2, 0.736s
- `build /tmp/lora-forward-LO8vEs/job/scene.json --out /tmp/lora-forward-LO8vEs/build_04 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` → exit 0, 7.886s
- `build /tmp/lora-forward-LO8vEs/job/scene.json --out /tmp/lora-forward-LO8vEs/build_05 --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype` → exit 0, 4.585s

最终交付：build_05/editable.pptx、svg/page_001.svg、scene.resolved.json、fonts.json、validation.json、render/page_001.png、dense.png、roi_metrics.json。重建可运行：

`/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/lora-forward-LO8vEs/run.py build /tmp/lora-forward-LO8vEs/build_05/scene.resolved.json --out /tmp/lora-forward-LO8vEs/rebuild_new --font-dir /Applications/LibreOffice.app/Contents/Resources/fonts/truetype`
