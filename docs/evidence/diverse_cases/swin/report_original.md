# Swin Transformer 原始四面板独立前向重建报告

最终候选 `build_04` 已通过冻结 v0.2.0 的完整检查：preflight、native_objects、rendered_text 均为 **pass**。已打开实际 PPTX 渲染、原图/渲染/差异对照及 C、D 局部图。该结论是结构和实际渲染验证通过，不是像素完全一致。

工作目录：`/tmp/super-img2ppt-diverse-swin-j37k7e_x`。输入为指定的真实 Swin PNG（2386 × 1312），prepare 生成 RGB 白底归一化 source.png 后已打开核对。仅使用冻结 SKILL.md、其三个文字 references 和 scene.schema.json；没有访问其他案例、运行时代码内容、测试或外部网页，没有安装依赖或修改主仓库。运行时源码只为任务要求计算 SHA-256 清单，没有阅读实现。

## 产物与原生边界

- pptx: [editable.pptx](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/editable.pptx)
- svg: [page_001.svg](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/svg/page_001.svg)
- scene_resolved: [scene.resolved.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/scene.resolved.json)
- fonts: [fonts.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/fonts.json)
- validation: [validation.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/validation.json)
- preview: [page_001.png](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/render/page_001.png)
- comparison: [page_001_comparison.png](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_04/render/page_001_comparison.png)
- measurement: [measurements_04.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/measurements_04.json)
- roi_definitions: [roi_fixed.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/roi_fixed.json)
- object_inventory: [native_object_inventory_04.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/native_object_inventory_04.json)
- commands: [commands.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/commands.json)
- provenance: [provenance.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/provenance.json)
- first_preflight_failure: [validation.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/check_01/validation.json)
- first_render_failure: [validation.json](/tmp/super-img2ppt-diverse-swin-j37k7e_x/build_02/validation.json)

实际 PPTX：**497 个原生对象**（92 个文本、30 个形状、375 条线/原生箭头）和 **34 个独立照片裁片**，总计 531 个对象；531 个场景 ID 全部在 PPTX XML 匹配，缺失 0。XML 中为 147 个 `p:sp`、350 个 `p:cxnSp`、34 个 `p:pic`；自定义箭头在 `p:sp` 中。SVG 的文本和几何也保持原生元素。

照片区域为 A 面板 21 个透视片与 B 面板 13 个矩形窗口。只保留独立照片像素，裁片剔除网格条带；灰色分格和红色窗口/外框均另建为原生线。没有把整页截图当作重建输出，也没有在烘焙文字上重复覆盖文字。所有可读正文、旋转标签、上标与公式均为原生文本或原生线组成。

## OCR 与字体核对

Vision OCR 成功但有误读：蓝色箭头被认作“个”；`Stage 3` 被认作 Stages；四处分数公式和部分 ×2 遗漏；`Layer l` 的字母 l 与数字 1 混淆。已按原图逐项校正，保留公式 H/4 × W/4 ×48、H/4 × W/4 ×C、H/8 × W/8 ×2C、H/32 × W/32 ×8C，重复次数 ×2 / ×2 / ×6 / ×2。没有添加源图未出现的 H/16 公式。详情见 transcription_review.json。

采用本机 Times New Roman Regular、Italic 和 Bold Italic，fonts.json 中运行时替换数为 0；实际 PDF 字体身份检查通过。像素不能唯一识别源字体，因此此处是可用近似选择；字体未嵌入。普通文字多数约 37–38.4 源像素，C 模块文字按源图 18–19 px 墨迹高度重新测得 27.5 px 字号，旋转标签按实际源/渲染长度校正到同组 42.25 px。未反复降低最小字号，也未使用自动无限缩字。

## 固定 ROI 的实际边缘测量

在作者场景和首次 build 前固定了 **30 个 ROI**，定义文件 SHA-256 为 `9b797ef3325e69c0a497c55d33108b5f2186ed345bae24acda80ae216f0c3973`；从头至尾没有改动 ROI。实际渲染为 1600 × 880，用 LANCZOS 归一至 2386 × 1312 后，在同一源像素区域测二值边界的双向 chamfer 距离。线条几何以笔画中心定位，位图边界以像素格边沿记账。此处测的是可见边缘，不将字框底部伪称为基线。

首次真实候选 build_02 的 ROI 均距中位数 0.863 px；最终为 **0.573 px**，最大单 ROI 均距 **3.151 px**。这些数值不是相似度分数或“保真率”。全部 30 处原始测量（含不理想结果）如下。

| 固定 ROI | 均距 px | P95 px | 墨迹框边差 L/T/R/B px |
|---|---:|---:|---|
| a_classification | 0.577 | 1.414 | [0, 1, -2, 1] |
| a_segmentation | 0.345 | 1.0 | [1, 0, -1, 0] |
| a_detection | 0.322 | 1.0 | [1, 0, -1, 0] |
| a_caption | 0.831 | 2.0 | [0, 0, -3, -1] |
| a_top_red_edge | 0.109 | 1.0 | [0, 0, -1, 0] |
| a_bottom_red_edge | 0.37 | 1.0 | [1, 0, 0, 0] |
| b_layer1 | 1.862 | 11.828 | [11, 0, -11, -3] |
| b_layer_next | 3.151 | 14.243 | [6, 1, -9, -5] |
| b_caption | 0.537 | 1.414 | [0, 0, -3, -1] |
| b_red_top_left | 0.041 | 0.0 | [-1, 0, 0, 0] |
| b_red_vertical_left | 0.492 | 1.0 | [-1, 0, 0, 0] |
| b_red_center_top | 0.08 | 1.0 | [-2, 0, 0, 0] |
| b_red_arrow | 0.564 | 1.0 | [1, 0, -1, 0] |
| b_patch_label | 0.761 | 2.0 | [1, 1, -1, 2] |
| c_mlp1 | 0.568 | 1.0 | [0, 0, 0, 0] |
| c_ln1 | 0.442 | 1.0 | [0, 0, 0, 0] |
| c_wmsa1 | 0.439 | 1.0 | [1, 0, -2, 1] |
| c_input_arrow | 1.142 | 4.414 | [0, 0, 0, 0] |
| c_residual_horizontal | 0.542 | 1.414 | [0, 0, 0, 0] |
| d_stage1 | 0.944 | 3.0 | [-1, 0, -4, -1] |
| d_stage2 | 0.653 | 1.414 | [2, 0, -1, -1] |
| d_images | 0.849 | 2.0 | [2, 0, 3, 0] |
| d_partition_vertical | 1.033 | 2.828 | [-3, 2, -1, -1] |
| d_swin1 | 0.362 | 1.0 | [-1, 0, 0, 0] |
| d_transformer1 | 1.084 | 2.0 | [-3, 9, -8, -8] |
| d_block1 | 0.435 | 1.0 | [1, 0, -1, 0] |
| d_image_arrow | 2.03 | 12.0 | [0, 0, 0, 0] |
| d_block_top_border | 0.923 | 1.0 | [0, -1, 1, 0] |
| d_caption | 0.675 | 1.414 | [0, 0, -2, -2] |
| d_formula_first | 1.423 | 4.243 | [-1, 0, 5, 1] |

ROI 限制：两个 Layer 标题区域在下边沿包含源图深红框线，被固定的 `max RGB <150` 黑色阈值纳入；d_transformer1 含源模块右边框细片。c_mlp1 是部分文字加边框/连线区域，c_ln1 实际是 LN 框边及连线而非独立 LN 文字。它们如实保留，不当作纯文字对齐证据。其余已固定文字、网格、连线区域超过 15 处；完整黑/红掩码条件和边缘数据在 measurements_04.json。

## 失败、修复与可复现问题

- check_01（exit 2）保留：作者遗漏 C 框内残差线/数学文字及 D 内部箭头的 container；C 模块字号过大；混合斜体公式框宽不足；右侧上标侵入圆。修复由源图墨迹实测支持，具体命名关系保留，没有全局碰撞豁免。
- check_02 pass；build_02（exit 2）保留完整 PPTX/SVG/真实预览。preflight 与 native_objects pass，但 rendered_text 报 c_left_z_305、c_right_z_305 的 `rendered_glyph_overflow`，glyphs=`^`。该字符来自独立的 c_left_hat/c_right_hat 文本对象，相邻文本检查把它归到 z 框。可用 commands.json 中 reproduce_rendered_caret_failure_command 重建 build_02/scene.resolved.json 原样复现。
- 候选 03 按原图把两处小帽改为四条原生短线，补齐四个加法圆横线，红箭头改为开口线头；普通字与旋转字据实际边缘测量局部调整。check_03（exit 2）只剩五个旋转文本框高度 49.0 px 小于所需 49.087 px，属于 0.5 px 安全余量边界。
- 候选 04 将这些透明横向框高扩到 50 px，不改字号；check_04、build_04 全 pass。没有任何同一区域连续三次失败后继续无限重试的情况。

## 剩余差异与验证范围

- Only 34 exact-source photograph crops remain raster. All readable labels, formulas, red/gray grids, module boxes, rounded groups and connectors are native objects. No full-page image is visible in the output.
- Perspective photograph assets use alpha clipping around their visible quadrilateral and source grid strips. Thin antialias remnants and small pale gaps at grid bands are visible in close inspection; their underlying photographic pixels are not editable vectors.
- Superscripts, fractions and hats remain separately positioned editable text and native line components, not Office equation objects.
- The source architecture and residual arrows have concave rear head edges. The runtime custom arrow contract gives triangular heads; all remain editable, but head silhouettes are approximate. The fixed d_image_arrow ROI has a 2.03 px mean boundary distance and 12 px p95.
- Rounded-corner curvature and dash phase differ slightly from source. Some labels retain small width/letter-spacing drift. No assertion of exact source font identification is made.
- Two pre-fixed Layer-title ROIs also include dark-red border pixels because the specified black threshold admits that color. d_transformer1 includes a sliver of the source module border. c_mlp1 contains partial text plus box/connector and c_ln1 contains a module edge/connector rather than the LN label. These mixed ROIs remain unchanged and are reported verbatim, not used as isolated typography evidence.
- Actual rendered evidence is from LibreOffice 26.2.4.2 and pypdfium2, not native PowerPoint or WPS. Fonts are not embedded.

凹尾箭头和虚线相位差异作为本次可审阅重建的限制保留；它们没有变成栅格，仍然可编辑。照片内摄影细节是唯一非原生图形区域。

## 版本、命令、哈希

- 冻结运行时：super-img2ppt 0.2.0，Python 3.12.12；导入路径 `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v020-frozen-25jvlm15/super-img2ppt/src/super_img2ppt`。
- Runtime Python 文件树 SHA-256：`962eb15fef9ec133cbe98a2ff7df0158978f23999b382f4fa01b883e3aa444d1`。算法为各 .py 文件相对路径→SHA-256 的排序紧凑 JSON 再做 SHA-256；每个文件摘要在 provenance.json。
- 冻结 SKILL.md SHA-256：`171c2561bc66b1858698fd6784f287c5a8545c6adf0707e3433c1031aef0606e`。
- 原始输入 SHA-256：`4edbd1fbd66972804cf11d66c6224f24b54209a2ec4607ac36ab9a7c1e18dfa2`。
- 归一化 source.png SHA-256：`c9cbfb998565c44603ebb21f87c563a0edc76c76ad8aefade06cd55746d08ee4`。
- LibreOffice 26.2.4.2 `0229ac93fcf0d7cbc6376066c6f35021cef002dc`。依赖版本见 doctor.json，字体摘要见最终 fonts.json。
- 完整有序命令、退出码、对应候选和最终/失败复现命令在 commands.json。
