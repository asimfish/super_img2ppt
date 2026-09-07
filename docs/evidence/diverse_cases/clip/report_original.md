CLIP 原图重建：冻结 v0.2.0 独立前向试用原始报告

最终保留 scene_04 / build_04，状态为 review。preflight 与 native_objects 均 pass；实际 LibreOffice 渲染文字检查保留两条宽度审阅项，未发生缺字或渲染字体替换。已打开实际 PPTX 渲染整页、runtime 比较图，以及矩阵、提示词和预测部分的源像素比例对照图。此报告在接触 v0.3.0 候选接口实现前固定；候选复测将另存。

输入：`/Users/liyufeng/Code/super_img2ppt/output/diverse_cases_20260906/raw/clip_CLIP.png`，原始 SHA-256 `308a3ca4503f1c7a07803916c369d78c4ef501e5ab7fc727da9b5e1d2f9ec85b`。prepare 后归一化页为 2162 × 762；归一化 source.png SHA-256 `aac9fc38897a498a481722ac09affac792ad46b762155b25fdc053f963daaf61`。工作目录为 `/tmp/super-img2ppt-diverse-clip-f11ta96b`。仅读取指定 skill、references、指定输入与已安装字体，执行冻结运行时；未查看其他案例、仓库源码或测试，未安装依赖、未联网、未提交。运行时代码仅为记录所要求的哈希而读取字节，未检查实现内容。

prepare 使用本地 macOS Vision OCR。逐项对照原图纠正了全角标点、Encoder 误识别、I/T 下标与点积符号；原图矩阵顺序为 1、2、3、…、N，预测高亮为 I₁·T₃，输出为 A photo of a dog.。原始 OCR 与独立校正清单均保留。

原生对象边界：实际 PPTX XML 有 311 个对象，其中 131 个含非空原生文字、149 个无文字的原生形状（含 19 个自定义箭头）、25 条连接线，合计 305 个原生非图片对象；另有 6 个图片对象。6 个图片对象包括 2 个独立照片区域及 4 个仅含编码器梯形填充的图片；4 个梯形的 16 条轮廓线和内部文字均为原生对象。左侧照片叠放作为一个独立照片区域保留，隐藏照片内容无法从源图恢复。整页源图只作为比对引用，不是可见幻灯片背景。矩阵通过单元格矩形与文字重建，不是 Excel 关联表格。

冻结 scene 的形状枚举不支持自由多边形，无法将 4 个源图梯形精确写成一个原生填充形状。因此基线保留局部填充图片，并明确披露。另一个实际限制是数学下标：18 px 候选通过，但较原图细；增到 20 px 后源锚点处出现 9 对字符碰撞错误。没有添加字符重叠豁免、降低 fit 下限、删除文字或移动矩阵来隐藏错误。最终保留先前已测量通过的数学子场景，并记为视觉差异。

所有候选和失败输出保留如下：

| 候选 | check | build | 结论与处置 |
| --- | --- | --- | --- |
| scene_01 | fail | fail | 6 对前卡文字/后卡背景被报重叠；失败报告完整保留。 |
| scene_02 | pass | review | 对 6 个实际被前卡遮住的后卡/文字命名对补充源图层叠声明；首个实际 PPTX。文字最大边差 3 px。 |
| scene_03 | fail | fail | 普通文字按实测修正；下标 18→20 px 后 9 对基字符/下标报碰撞。未豁免。 |
| scene_04 | pass | review | 保留普通文字坐标修正，数学恢复整个已通过的 scene_02 子场景。最终原始基线。 |

没有同一区域连续三次未解决的修复尝试。首次卡片诊断已用 6 个源图有据的明确命名关系解决；数学放大尝试失败后停止该方向并保留先前可审阅稿。运行命令的退出码、时间、路径和完整输出日志均保留。两次辅助测量脚本失误（缺 NumPy、临时 Python 语法错误）及早期 XML 文字计数更正单列在 early_commands.md。

30 个固定 ROI 在第一次 build 前已写入 fixed_rois.json：21 个水平文字区域、9 个形状/网格线区域。用实际 PPTX 经 LibreOffice 输出的 PDF 按源宽度直接栅格化为 2162 × 762，不使用替代绘图器重画文字。文字比较黑墨/粉色墨迹 bbox；“基线代理”是可见墨迹下缘，不能声称从位图恢复了真实字体基线。线中心按像素单元中心 index + 0.5 计算。

最终 21 处文字的最大绝对边差 2 px，中位最大边差 0 px；可见墨迹下缘代理最大偏差 1 px。9 处形状/网格线的中心偏差均为 0 px。两个紫色表头上缘 ROI 的宽松颜色掩码同时捕获了上方箭头抗锯齿像素，原始 bbox 上缘差 -5 px 仍保留在 JSON；本报告的网格结论只采用连续线段的密度中心，未将这个 bbox 值抹去。

| 固定 ROI | 左/上/右/下边差 px | 墨迹下缘代理差 px / 线中心差 px |
| --- | --- | --- |
| title_1 | [0, 0, -1, 0] | 0 |
| title_2 | [0, 0, -1, 0] | 0 |
| title_3 | [0, 0, -1, 0] | 0 |
| pepper_line_1 | [0, 0, 0, 0] | 0 |
| pepper_line_2 | [0, 0, 1, 0] | 0 |
| train_text_label_1 | [0, 0, 0, 0] | 0 |
| train_text_label_2 | [0, 0, 1, 0] | 0 |
| train_image_label_1 | [0, 0, 0, 0] | 0 |
| train_image_label_2 | [0, 0, 1, 0] | 0 |
| class_word_plane | [0, 1, 0, 1] | 1 |
| class_word_car | [0, 0, 0, 0] | 0 |
| class_word_dog | [0, 0, 0, 0] | 0 |
| class_word_bird | [0, 0, 0, 0] | 0 |
| class_prompt_line_1 | [0, 0, 0, 0] | 0 |
| classifier_text_label_1 | [0, 0, 0, 0] | 0 |
| classifier_text_label_2 | [0, 0, 0, 0] | 0 |
| prediction_image_label_1 | [0, 0, 0, 0] | 0 |
| prediction_image_label_2 | [0, 0, 0, 0] | 0 |
| math_T1 | [0, 1, -1, -1] | -1 |
| math_I1T1 | [1, 1, -1, 0] | 0 |
| math_predict_I1T3 | [1, 1, -2, 0] | 0 |
| matrix_top_grid | [0, 0, 0, 0] | 0.0 |
| matrix_mid_grid | [0, 0, 0, 0] | 0.0 |
| matrix_bottom_grid | [0, 0, 0, 0] | 0.0 |
| matrix_left_grid | [0, 0, 0, 0] | 0.0 |
| matrix_col_1_grid | [0, 0, 0, 0] | 0.0 |
| class_plane_top | [0, 0, 0, 0] | 0.0 |
| text_feature_top | [0, -5, 0, 0] | 0.0 |
| predict_feature_top | [0, -5, 0, 0] | 0.0 |
| predict_row_bottom | [0, 0, 0, 0] | 0.0 |

实际保留的两条 rendered_ink_width_drift 分别是 train_text_label_1 和 classifier_text_label_1：本地字体测量宽 46 px，实际 PDF 墨宽 43.322 / 43.323 px；相应源图黑墨宽均为 43 px。源图与最终渲染 ROI 也均为 43 px。因此保留审阅状态，没有为消除提示更改字号。

实际解析字体为 Arial、Courier New、Times New Roman regular，fonts.json 无替换；字体文件未嵌入。源字体不能单凭位图唯一证明，以上为视觉最接近的已安装字体。渲染器为 LibreOffice 26.2.4.2 0229ac93fcf0d7cbc6376066c6f35021cef002dc。未验证原生 Microsoft PowerPoint 或 WPS。残留视觉差异包括较细的数学下标、部分省略点较轻、源图凹尾箭头与运行时实心三角箭头的轮廓差异；它们不应被解释为完全像素一致。

主要交付路径：

- PPTX：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/editable.pptx`
- 可编辑 SVG：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/svg/page_001.svg`
- 最终编写 scene：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/scene_04.json`
- resolved scene：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/scene.resolved.json`
- 资产：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/assets/`
- 字体：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/fonts.json`
- 验证：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/validation.json`
- 实际渲染：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/render/page_001.png`
- 实际 PDF：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/render/editable.pdf`
- 源像素实际渲染：`/tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_04/render/page_001_source_px.png`
- 固定 ROI：`/tmp/super-img2ppt-diverse-clip-f11ta96b/fixed_rois.json`
- 最终测量：`/tmp/super-img2ppt-diverse-clip-f11ta96b/measurements_build_04.json`
- 首个实际候选测量：`/tmp/super-img2ppt-diverse-clip-f11ta96b/measurements_build_02.json`
- 校正 OCR：`/tmp/super-img2ppt-diverse-clip-f11ta96b/ocr_corrected.json`
- 命令：`/tmp/super-img2ppt-diverse-clip-f11ta96b/commands.jsonl` 与 `/tmp/super-img2ppt-diverse-clip-f11ta96b/early_commands.md`
- 版本和运行时逐文件哈希：`/tmp/super-img2ppt-diverse-clip-f11ta96b/provenance_original.json`
- 全部原始产物绝对路径及 SHA-256：`/tmp/super-img2ppt-diverse-clip-f11ta96b/original_artifacts_manifest.json`

冻结 runtime Python 文件树 SHA-256：`1e864f4e1462987082bd57c21e6c7d4cb863c814ee7b13c9f92ed13d58128b63`。冻结 SKILL.md SHA-256：`171c2561bc66b1858698fd6784f287c5a8545c6adf0707e3433c1031aef0606e`。加载的模块路径是 `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/src/super_img2ppt/__init__.py`；Python 3.12.12，super-img2ppt 0.2.0。

复现最终构建：

```sh
PATH=/opt/homebrew/bin:$PATH PYTHONPATH=/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/src /Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build /tmp/super-img2ppt-diverse-clip-f11ta96b/job/scene_04.json --out /tmp/super-img2ppt-diverse-clip-f11ta96b/job/build_reproduction_NEW
```

重建输出必须使用新的目录名。现场未向系统安装、嵌入或分发字体。
