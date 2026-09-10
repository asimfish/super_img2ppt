# 正式顶会完整主架构图压力测试

2026-09-11，本轮测试正式论文的完整主架构图，保留所有子面板、模块、查询标记与主要分支。
**三例均能导出可检查的 PPTX/SVG，但严格源图保真均未通过。** 当前版本仍不能可靠地把复杂论文主图
转换成字体、间距和细节都准确的可编辑文件；以下报告不把自动检查通过解释成高保真。

## 实际转换结果

| 论文主图 | 原生可编辑对象 | 局部图片 | 自动检查 | 预先固定的严格区域检查 |
| --- | --- | --- | --- | --- |
| Grounding DINO，ECCV 2024，Figure 3 | 59文字、274形状、392连线 | 4 | review | 0/35 → 3/35 → 11/35 |
| GLaMM，CVPR 2024，Figure 2 | 32文字、87形状、22连线 | 14 | review | 3/39 → 3/39 |
| UniAD，CVPR 2023，Figure 2 | 28文字、27形状、39连线 | 8 | review | 4/36 → 7/36 → 8/36 |

这些比例是不同预设区域和掩膜下的像素阈值结果，不能合并成转换准确率。失败不等于内容都错误，
但明确说明没有达到预定对齐标准。UniAD 的8个通过区域中7个为几何区域；GLaMM的3个通过区域都是连线。

### Grounding DINO

使用 [ECCV 2024 正式论文](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06319.pdf)
第5页 Figure 3：完整模型、Feature Enhancer 和 Decoder Layer 三大面板。作者仓库的架构图与正式版本
在提示文本和间距上有差异，因此原仓库版本的初稿单独保留，另行冻结正式图的35个测量区域。

729个对象中725个是原生对象，包含多尺度网格、立体token、双色渐变模块、注意力连线和旋转提示词。
四处照片组合保留为图片。修正了字体尺寸、局部文本位置，以及查询token应为黄色而非文本token浅绿色的问题。
最后按实际字形边缘调整原生文字原点后，21个独立主标签的边缘误差均在1px内，严格指标提高到11/35。
这不是全部文字的保真通过：字形IoU、密集网格、旋转/等宽提示词及局部几何仍有失败。

旋转提示框的一处重叠经实际PDF核查：前景字形与后方提示框的几何区域相交，但前景面板按源图覆盖后景。
因此使用具体命名的源图叠放关系，而不是降低通用检查。报告中的 `area_px2` 是对象轮廓交叠面积，
不等于字形面积；字号变化后该数值不变不能证明检查器有bug。

### GLaMM

使用 [CVPR 2024 正式论文](https://openaccess.thecvf.com/content/CVPR2024/html/Rasheed_GLaMM_Pixel_Grounding_Large_Multimodal_Model_CVPR_2024_paper.html)
第4页 Figure 2：图像/区域/像素分支、LLM、grounded conversation，以及下方四个任务面板。
GitHub配图缺少 `Image-region prompts` 和 `Output prompts` 两处标签，实际评测改用正式PDF完整栅格。

全部可读的图示标签、问题、回答和彩色短语均为原生文本；特征堆叠面、ROI虚线、token和连接线为原生几何。
14个图片区域保留照片与机器人插图。七个照片区域保守声明包含真实场景中的细小品牌文字，未称其可编辑。
初始 Times New Roman/Courier 与原图差别明显，改用本机 Georgia/DejaVu Sans Mono 后视觉更接近，
但固定指标仍为3/39。源宽度实际PDF栅格的补充检查为4/39，说明缩略预览不能解释大部分失败。

剩余问题包括字体身份与字形不匹配、分布式词间距、基线、多行排版、特征堆叠深度、软阴影及箭头尺度。
照片附近的空白文本框触发保守烘焙文字检查，最终按原图换行拆框、修剪空白边界，未放开文字覆盖图片限制。

### UniAD

使用 [CVPR 2023 正式论文](https://openaccess.thecvf.com/content/CVPR2023/papers/Hu_Planning-Oriented_Autonomous_Driving_CVPR_2023_paper.pdf)
第3页 Figure 2，作者仓库 `sources/pipeline.png` 经整页栅格目视核对，与正式图的模块、标签和主要分支一致。
Backbone、TrackFormer、MapFormer、MotionFormer、OccFormer、Planner及直达规划的旁路均保留。

修正了查询 `Q` 的粗斜体、模块字重、分支/K,V颜色、多行文字位置和部分间距。严格区域通过数从4提高到8。
TrackFormer/MapFormer的文字与复杂图案融合，整块保留为含文字图片，没有删掉图案或叠加重复的原生文字。
两处关键模块名称仍不可编辑，所以不能用大量原生对象掩盖这一限制。其余图片包含输入图标、BEV及运动/道路插图。

UniAD冻结的暗色掩膜不适合Planner红色文字，该区域明确记为无效/失败；部分区域包含边框，不能解释成纯字形精度。
除几何区域外，多数文字的IoU仍低于0.70，即使边缘误差已经小于3px。字体和细线抗锯齿仍明显不同。

## 测量和独立性

三位独立评估者使用冻结的v0.3.1 skill和原图重建，只读skill说明及场景文档，不读取运行时实现作为答案。
未使用PDF文字/向量坐标、原始SVG或作者绘图脚本作为重建坐标。每例在正式源图确定后先固定ROI，再编写场景。
首次实际渲染后父任务给出具体视觉反馈，相关修订已在原始报告中注明，不伪称全程盲测。
每个失败区域的实质修改有界；所有失败版本、命令、原始报告和指标均保留。
这些固定区域也用于指导同图修正，属于开发评测，没有留出的独立泛化测试集。

| 案例 | 输入尺寸 | 固定测量方法 |
| --- | --- | --- |
| Grounding DINO | 2140×1460 | 实际PPTX PDF按源宽度渲染；预定明/暗区域掩膜；边缘误差≤4px且IoU≥0.70 |
| GLaMM | 2894×1054 | 默认1600×583实际预览Lanczos回源尺寸；RGB最大通道<170；边缘≤4px且IoU≥0.70 |
| UniAD | 1880×484 | 实际PPTX PDF按1880宽度渲染，实际高度485；RGB最大通道<150；边缘≤3px且IoU≥0.70 |

所有比较不做位置配准；源宽度补充结果不替换已有阈值。各例的完整ROI定义、无效区域与数据解释见原始报告。

## 文件与复现

[UniAD可编辑PPTX](../examples/main_figures/uniad/editable.pptx) ·
[SVG](../examples/main_figures/uniad/svg/page_001.svg) ·
[原图/实际渲染对照](../examples/main_figures/uniad/render/page_001_comparison.png) ·
[素材及许可证说明](../examples/main_figures/NOTICE.md)

Grounding DINO和GLaMM使用正式论文PDF，未把作者代码仓库许可证扩大解释为论文图片许可；
原图与派生产物保留在本地 `output/main_figures_20260911/deliverables/{grounding_dino,glamm}/`。
工程报告、源文件哈希、裁剪配方及本地产物身份见 [证据目录](evidence/main_figures)。

```bash
uv run python scripts/fetch_conference_sources.py \
  --cases grounding_dino_main glamm_main uniad_main --out output/main-figure-sources
uv run python scripts/run_real_cases.py \
  --corpus examples/main_figures --out output/uniad-replay
```

父任务已验证下载/裁剪输入与独立评测输入逐字节一致，并重新导出三个最终场景，核对实际渲染像素。
最终检查及安装包信息见 [验收证据](evidence/main_figures/verification_v032.json)。
本轮更新的是重建指南、源图复现和评测场景；未发现足以支持新运行时算法修复的因果证据。
运行时布局/导出行为与v0.3.1相同，未靠降低检查门槛获得通过。

本机LibreOffice/PDFium可检查，不代表PowerPoint/WPS原生外观已认证。未安装新依赖或字体；字体未嵌入。
下一步需要解决的具体能力是源字体候选匹配、统一基线与词间距拟合、复杂融合模块的可编辑边界，
以及更准确的立体堆叠和软阴影表现。
