**MobileViT Figure 1 独立位图重建案例（2026-09-06）**

实际 PPTX 构建、原生对象检查及 LibreOffice 渲染检查均通过；核心框线对齐良好。此案例达到“文字可编辑、结构可调整、实际可渲染”，没有达到全部内部图元可编辑或严格逐像素保真。最终文件是 `job/build_04/editable.pptx`。

输入来自任务提供的 MobileViT / ICLR 2022 Figure 1 图面裁剪，1600 × 944 像素。仅查看和测量该位图，未读取论文 PDF 矢量、文本坐标或其他人的重建场景。源文件 SHA-256：`1f7bcd373898059c710fbbe68157642f27c2c5b0faf629b6558bc4aba3eec919`。所有案例文件在本临时目录生成，没有安装依赖、修改仓库代码、提交或推送。

本次评测期间父代理更新了运行时，因此结果属于 **candidate working tree**，不能当作两个冻结发布版之间的完整 A/B 基准。初次 `doctor` 报告包版本 0.1.1；后续候选代码加入原生 dash、部分旋转、自定义箭头和 alpha 感知碰撞检查。每阶段的源码哈希保存在 `job/runtime_provenance_01.json`、`02.json`、`04.json`。

**交付边界与原生对象证据**

最终场景共有 697 个对象：91 个原生文字框、29 个原生形状、569 条原生线、8 张独立图片。解包 PPTX 核对得到 569 个 `cxnSp`、120 个 `sp`（91 文字 + 29 形状）和 8 个 `pic`。PPTX 中没有整幅源图作为可见背景，也没有把图中文字放进资产后再叠加可编辑文字。

8 张图片是两张动物照片和六个彩色张量。上方照片中的原始网格仍属于照片像素；六个张量按原始轮廓做 alpha 裁剪，以排除附近的维度文字。它们可分别移动、缩放，但内部网格和色块不可逐个编辑。全部资产已通过 `job/assets_contact_sheet.png` 目视检查，均不含文字。实际不透明图片面积合计 75,059 源像素，占页面面积约 4.97%；这不是“可编辑率”或视觉质量分数。

所有可读标签都重建为原生文字。流程框、背景、分区虚线、立方体轮廓、箭头和花括号为原生对象。受 schema 限制，立方体白色斜面采用原生白色短线拼成，曲线和花括号采用原生线段近似。当前不是可重布线的智能图：移动节点不会自动重连，细小线段也没有合并成逻辑模块组。

**原始失败与受控修复**

| 阶段 | 真实结果 | 保留的证据 |
| --- | --- | --- |
| 初稿预检 | fail：28 个 `unintended_overlap`，另有 8 个 `image_stretched` warning；无文字溢出 | `job/scene.authored_01.json`、`job/check_01/validation.json` |
| 首次实际构建 | pass；通过逐对源图连接关系说明及 6 个透明角落的像素证据暂时解除误报 | `job/scene.repaired_01.json`、`job/build_01/` |
| 候选运行时复测 | pass；去掉 6 个图片/文字 pair 豁免，并恢复原始同尺寸 stretch；原生 dash 将对象数从 1207 降到 697 | `job/scene.candidate_02.json`、`job/build_02/` |
| 一次局部字体修复 | pass；主标题与底部数字尺寸改善，数学式仍存在宽度残差 | `job/typography_repair_03.json`、`job/build_03/` |
| 下采样标签首次空隙修复 | pass；5 个标签恢复为源图的“↓ 2”可见间隔 | `job/downsampling_gap_repair_04.json`、`job/build_04/` |

初稿的 28 个碰撞包括 6 个 PNG 透明角落误报、4 个源图可见的跨分区线交点、18 个同一个绿色放大箭头的原生线段接头。6 个 alpha 误报独立按 4 倍字体 mask 与资产 alpha 测量，非透明交面积均为 **0.0 px²**，数据在 `job/alpha_overlap_measurement.json`。最终场景没有这 6 个 pair 的豁免；候选 alpha QA 正常放行。真正不透明的图片区域没有因此获得全局豁免。

8 个 stretch warning 发生在图片尺寸与画面尺寸完全一致的情况下，初稿并未改变比例。候选修复后恢复同尺寸 stretch 进行复测，最终未产生该 warning。原始误报报告保留，没有用后续通过报告覆盖。

没有对同一区域做超过三次的未解决修复。斜置标签没有靠缩小字号迁就格式；已知任意角度不支持后直接记录限制。数学式只做了一次字体/样式修复，仍有残差后停止该区域继续调参。

**实际渲染与量化证据**

使用本机 LibreOffice 26.2.4.2（`0229ac93fcf0d7cbc6376066c6f35021cef002dc`）渲染实际生成的 PPTX，经过其真实 PDF 再栅格化成 1600 × 944 图像。没有使用另一套绘图代码伪造“PPTX 预览”。已检查整页、密集 MobileViT 模块、底部网络、主标题和斜置标签裁剪。未在原生 PowerPoint 或 WPS 中验证。

最终 `validation.json` 中 preflight、native_objects、rendered_text 均为 pass；后两项无 findings。`visual_review: required` 是运行时保留的独立字段，自动 pass 不等于源图保真验收。此报告记录代理已完成的视觉检查及剩余问题。

在相同源像素坐标的 25 个水平文字 ROI 内测量实际可见墨迹边缘，并另测 8 个框线锚点。黑字阈值为各 RGB 通道最大值 <155，红蓝字按颜色通道隔离。下面是测量结果，不是抽样成功率或自动视觉相似度评分。

| 指标/区域 | 首次真实渲染 | 最终真实渲染 |
| --- | ---: | ---: |
| 25 个文字 ROI、共 100 个边缘差的绝对中位数 | 1 px | 1 px |
| 上述文字边缘绝对最大值 | 28 px | 9 px |
| 主标题右边缘（渲染减源图） | -28 px | 0 px |
| 主标题下边缘 | 0 px | +2 px |
| 六组底部数字尺寸右边缘 | -6～-8 px | -2～-5 px |
| `h = w = 2` 右边缘 | -8 px | -9 px |
| 8 个形状/线段中心的绝对中位数 | 0 px | 0 px |
| 8 个形状/线段中心的绝对最大值 | 0.5 px | 0.5 px |

标题从源图的 x=565 到 x=1091，最终左右边缘相同；因为近似字体的宽高比不同，底边比源图低 2 px。`Transformers as Convolutions` 右边缘仍短 6 px，`representations` 短 4 px。五个下采样标签还存在约 1～3 px 的字形边缘偏差。数学式宽度残差没有被主标题改善掩盖。

线段测量使用黑色笔画中心，包含位图像素格中心的 +0.5 px，避免把整数像素行误当成几何中心。文字只报告墨迹上/下/左/右边缘；没有从位图虚构唯一的字体基线。原生虚线保留了分区结构，但密集边框上每个短划的相位与源图仍略有差异。

4 个代表性斜置标签单列测量，未混入上述水平文字统计。`3P` 的源图墨迹框为 `[451,22,476,55]`，最终为 `[451,24,480,44]`，下边缘差 -11 px；这反映了源图斜角与输出水平文本的形状差异。`2C` 下边缘差 -6 px。测量时排除了张量/立方体轮廓及其抗锯齿边界，避免把图片边缘误算成标签文字。完整明细在 `job/build_04/anchor_measurements.json`。

**必须保留的限制**

- `3P`、`d`、`C`、`2C` 等共 10 个斜置标签转为水平可编辑文字。候选 runtime 的 90° 旋转不能表达这些任意斜角，因此没有试图用错误旋转掩盖。
- 六个彩色三维张量以及照片中的网格仍是位图内部内容，不能声称全图所有形状都可编辑。
- 最近似可用字体选择 Times New Roman 的 Regular、Bold、Italic 三个实际本地字形文件。运行时没有字体替换，也没有嵌入字体；这不能证明其就是原图字体。数学式和部分粗体标题的间距/比例仍有可见偏差。
- 曲线、花括号、箭头形状和分区虚线相位是原生图元近似；可编辑性与精确自由曲线并不相同。
- 自动检查只覆盖实际运行的门禁。原生 PowerPoint/WPS 与跨电脑字体可用性未验证。

**绝对路径与重建入口**

- PPTX：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/editable.pptx`
- 可编辑 SVG：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/svg/page_001.svg`
- 已解析场景：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/scene.resolved.json`
- 其配套资产：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/assets/`
- 字体清单：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/fonts.json`
- 最终验证：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/validation.json`
- 真实整页预览：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/render/page_001.png`
- 源图/实际渲染/差分：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/render/page_001_comparison.png`
- 密集模块对照：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/dense_source_render.png`
- 底部网络对照：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/bottom_source_render.png`
- 定量墨迹与框线测量：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/build_04/anchor_measurements.json`
- 原始失败：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/job/check_01/validation.json`
- 机器可读审计：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/CASE_RESULT.json`
- 绝对路径清单：`/tmp/super-img2ppt-conference-mobilevit-tsXEcl/artifacts.json`

重建时使用 `build_04/scene.resolved.json` 及其相邻 `assets/`，输出到新的目录，并使用包含本轮候选功能的运行时与列出的字体。`author_scene.py`、`repair_01.py`、`candidate_retest.py`、`final_typography.py` 和 `measure_render.py` 保留了独立作者和测量过程；最终“↓ 2”修复的完整场景与逐项记录另存于 `job/scene.final_04.json` 与 `job/downsampling_gap_repair_04.json`。
