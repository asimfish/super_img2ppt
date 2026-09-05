本次独立实测完成了 Spatial-Mamba Figure 4 的可编辑重建。最终选择 `build_native_03/editable.pptx`：LibreOffice 实际 PPTX 渲染、原生对象检查与渲染文字检查均为 **pass**。这是父任务在评测期间修改运行时后的 **candidate working tree** 结果，不能当作原始未修改版本已经具备这些能力的证据。

输入仅为给定的 1600 × 624 原始位图，SHA-256 为 `a9b3706ca9a29d791d225300922fb064bb2c6441d4f7a5684b3fd6aaa16f2541`。读取了 skill、其规范、prepare 的 OCR 和原始位图；没有读取源 PDF 的向量/文字坐标，没有读取别人的答案场景，没有修改仓库代码、提交、推送或安装依赖。场景依据原图人工观察、像素测量和精确裁剪建立，不能描述为无人参与的一键转换。

最终 PPTX 包含 39 个原生文字对象，其中 15 个为旋转文字；129 个原生形状（含阴影近似层）；351 条原生线；24 个带显式箭头的原生 freeform；1 张独立蜻蜓照片。PPTX 的 `ppt/media/` 只有 1 张图片。整张原图保存在重建材料中作为比较依据，未用作 PPTX 的可见背景。下标采用单独的可编辑数字文本框。连线坐标固定，移动模块后不会自动重排连线。

原始 skill 所描述的 scene v1 没有旋转文字、虚线或柔和阴影字段。初始版因此把 Stem、3 个 Down Sampling、Head，以及底部 10 个旋转模块标签保存为独立精确裁剪。`build_hybrid_01` 的真实渲染为 **review**，有 15 条 `raster_text`，这份混合版和相关场景已经保留。父任务添加旋转支持后，受控复测将这 15 个标签全部改为原生文字，未保留文字栅格覆盖层。圆角虚线仍沿用原始独立场景中由源位图测得的可编辑短线段；本图没有改用候选新增的 dash 字段。阴影以文字之外的浅灰原生圆角层近似，没有声称生成了相同的原生模糊效果。

抽测在原图和最终实际渲染的相同隔离区域内取可见黑色文字/彩色描边的边界，所有量均为源像素。文字阈值为各 RGB 通道均小于 90。每个区域保存了原图、渲染图边界，四条边的差值，以及中心差值。这里的边界一致性不是像素全等或感知相似度得分。

| 代表锚点 | 数量 | 平均绝对边缘偏差 | 最大绝对边缘偏差 | 平均绝对中心偏差 |
|---|---:|---:|---:|---:|
| 旋转标签 | 15 | 0.383 px | 1 px | 0.150 px |
| 横排文字 | 18 | 0.417 px | 1 px | 0.222 px |
| 形状边缘 | 6 | 0.208 px | 1 px | 0.208 px |
| 残差主连线 | 1 | 0.250 px | 1 px | 0.250 px |
| 4 个重复乘号 | 4 | 1.500 px | 2 px | 0.500 px |

旋转文字受控复测首版 `build_native_01` 已通过自动检查，但 15 标签平均边缘偏差为 1.433 px、最大 4 px，Down Sampling 有 3.5 px 横向中心漂移。依据这次真实渲染只作一轮位置/字号定点修正，得到上述最终数据。`build_native_02` 和最终 `build_native_03` 的这 15 个标签完全相同。第一阶段混合版的旋转裁剪平均边缘偏差为 0.550 px、最大 1 px，但字符不能编辑。

箭头另外单独检查。第一个 stage 的入箭头，源图可见头部高度为 12 px；标准 `arrow:true` 产生的实际头部高度仅 9 px。最终采用候选运行时的 `arrow_head:{length:12,width:13}` 后实际高度为 11 px，尖端/下沿仍有约 1 px 差异。全部 24 个箭头均为可编辑 freeform。没有以自动 pass 掩盖这项剩余差异。

初始失败与修复均保留，未覆盖：

- 作者测量脚本最初误用环境中没有的 NumPy，报 `ModuleNotFoundError: No module named 'numpy'`。未安装依赖，改用 Python 标准库和 Pillow。紧随其后的 `check_01` 检查到 prepare 产生的空白未审阅场景，报 `unreviewed_scene` 和 `empty_slide`；这是作者脚本失败，不是图像重建质量结果。
- 首个完整场景 `scene_hybrid_01.json` / `check_02` 有 29 条 overlap。金色虚线提取误捕捉了照片中的黄色像素；扩大阴影还碰到边框。这些属于独立场景作者错误。限定测量区域并缩减阴影边界后，`check_03` 剩 12 条源图可见的边框/连线接点和阴影交叠；逐对指定了有源图依据的对象关系，没有统一豁免文字碰撞。
- OCR 把旋转术语识别成 `ISS`、`NAd`、`IuI`、`AUOO`、`JSVS` 等，并遗漏若干 L 下标。保留原始 OCR；最终文字均对照原图检查，没有直接采用这些误识别内容。
- `build_hybrid_01` 为 review，15 处文字仍是栅格。这是原始旋转能力缺口的可复核产物。
- `build_native_01` 为 pass，但实际对齐偏差最大 4 px，按上述测量修正，未把自动 pass 等同于源图对齐。
- `build_native_02` 的 preflight/native_objects 为 pass，rendered_text 为 fail。它把单独下标 `stage_3_index` 的“3”归给透明框较宽的 `stage_3_layers`，报 `rendered_glyph_overflow`；画面中的 L 与 3 本来分离且正确。最终只把 L 文本框宽度从 21 px 收紧到 17 px，保留可见 L 和下标位置，消除了实际 PDF 匹配的误归属。失败报告与真实渲染保留。
- `build_native_03` 的三项自动检查均 pass。该版另把标准箭头改为显式尺寸，以上局部变化均有 `repair_02.json` / `repair_03.json` 记录。旋转区仅有初版与一次位置/字号修正，没有继续反复试错。

已打开最终完整真实渲染、由它裁切的底部密集模块图，以及生成的源图/实际渲染/差异对比图。已检查文字内容、旋转方向、SSM 两行排布、L 下标、容器间距、运算符、连接关系与箭头方向。仍有轻微字体形状/乘号、柔和阴影、虚线圆角弧段差异；照片也受到实际 PPTX 栅格重采样影响。仅验证了本机 LibreOffice，没有验证 PowerPoint 或 WPS。

选择的字体为本机 Times New Roman Regular 和 Italic。`fonts.json` 与实际 PDF 检查没有报告字体替换。像素不能唯一证明源字体身份，因此这里只把 Times New Roman 视为最接近的选择。字体未嵌入；其他编辑电脑需要相同字体。

主要交付路径：

- 最终 PPTX：`build_native_03/editable.pptx`
- 可编辑 SVG：`build_native_03/svg/page_001.svg`
- 可重建场景及资产：`build_native_03/scene.resolved.json`、`build_native_03/assets/`
- 字体和检查：`build_native_03/fonts.json`、`build_native_03/validation.json`
- 实际完整预览和比较：`build_native_03/render/page_001.png`、`build_native_03/render/page_001_comparison.png`
- 实际密集区域：`build_native_03_measurements/dense_actual.png`
- 44 个锚点明细：`build_native_03_measurements/anchors.json`、`build_native_03_measurements/anchors.csv`
- 箭头明细：`arrowhead_measurements.json`
- 原生对象/媒体审计：`final_native_object_audit.json`
- 原始混合交付：`build_hybrid_01/`
- 全部初始失败：`check_01/`、`check_02/`、`check_03/`、`build_native_02/`
- 独立作者脚本：`build_scene_01.py`、`build_scene.py`、`build_native.py`、`measure.py`
- 环境版本记录：`runtime_candidate_manifest.json`（候选基底 commit 为 `ca9c72c070fcbcf68b014d3333e055696eb6332b`，附运行时 Python 文件哈希；评测期间工作树已修改）
- 命令复核：`commands.md`

最初两份测量文件还包含 sigma 的内区矩形，该矩形可能碰到圆边，不适合作为独立文字锚点；最终 44 锚点统计已排除这两行，原始文件没有删除。
