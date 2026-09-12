# 2026 具身与世界模型：完整图实测与 v0.3.6 改进

截至 2026-09-12，新增 DreamZero、Cosmos Policy、Cosmos 3 三张完整图，画廊共十五例。选择近期公开的世界动作模型、视频控制与多模态世界模型架构，未对项目作热度排名。只有 Cosmos Policy 在本轮明确核实 ICLR 2026 发表；另外两例按 arXiv 论文展示。

| 固定论文与完整图 | 来源版本日期 | 原图像素 | 原生对象 / 局部图片 | 最终自动检查 |
| --- | --- | --- | --- | --- |
| [DreamZero Fig.4](https://arxiv.org/abs/2602.15922v1)，PDF 第 6 页 | 2026-02-17 | 1888×632 | 129 / 15 | 原始 review；resolved scene 复建 pass |
| [Cosmos Policy Fig.2](https://arxiv.org/abs/2601.16163v1)，PDF 第 4 页 | 2026-01-22 | 1195×476 | 56 / 26 | pass |
| [Cosmos 3 Fig.5](https://arxiv.org/abs/2606.02800v4)，PDF 第 11 页 | 2026-06-23 | 1400×625 | 414 / 1 | review，无阻断错误 |

Cosmos 3 首发 06-01，使用 v4；PDF 封面印 06-24，与 arXiv 提交日期分别记录。Cosmos Policy 的 [ICLR 2026 页面](https://proceedings.iclr.cc/paper_files/paper/2026/hash/748becc400a57c0e31cfe6a2e7951467-Abstract-Conference.html) 已核实，画廊冻结的是 arXiv v1 图源。三个论文的 CC BY 4.0 链接及许可页面逐篇存档，未把模型或代码许可当成论文图许可。详见[来源审计](evidence/world_models/source_audit.json)与各例 ATTRIBUTION。

## 实际交付与剩余差异

- [DreamZero 完整对照](previews/gallery/dreamzero.png) · [PPTX、SVG、原图、报告](../examples/gallery/dreamzero)：训练/推理和反馈回路全部保留；文字与主要结构可编辑，视频、噪声、机器人、动作示意图、金色弯曲汇合线和虚线自回归回路保留为图片。复杂连接资产含窄边缘和箭头尖端像素。Arial 提示语偏重、反馈标签偏短。原始竖省略号字体替代提示保留；复建使用已解析字体。
- [Cosmos Policy 完整对照](previews/gallery/cosmos_policy.png) · [PPTX、SVG、原图、报告](../examples/gallery/cosmos_policy)：三行条件/目标子序列、潜变量注入与状态/动作/价值括号完整。照片堆叠和潜变量块为图片，其余说明与公式为原生对象。图中不含规划搜索过程。小字、斜体与撇号仍不同。
- [Cosmos 3 完整对照](previews/gallery/cosmos3.png) · [PPTX、SVG、原图、报告](../examples/gallery/cosmos3)：完整双塔、五个编码器、共享注意力公式、144 格矩阵及图例。仅无文字曲线括号为图片；所有可读标签为原生文字。共有 415 个可见对象，其中 414 个原生对象。共享注意力公式和斜排标签的字体/间距仍有近似。

## 案例反馈如何进入系统

### 斜排公式从图片变为可编辑文字

旧 schema 只允许直角旋转，Cosmos 3 首轮把整个斜排表头保留为图片。v0.3.6 支持原生任意角度文字；`compose-math` 先测量各部件，再将部件中心和基线围绕同一个 `origin` 旋转，保持上下标关系。

[相同坐标的原图与最终细节](previews/gallery/cosmos3_detail.png) · [旧实际图](evidence/world_models/cosmos3/before_actualsourcewidth.png) · [旧 PPTX](evidence/world_models/cosmos3/before_editable.pptx) · [精确场景差异](evidence/world_models/cosmos3/before_after_scenediff.json)。删除一个文字图片条，增加 32 个 −45° 原生文字部件；已有对象改动为零。提升的是可编辑性，旧图片条的字形本来更接近原图，不能用它证明新原生字体更保真。

首轮公式组合因 Times New Roman 缺少 U+22EF 被严格拒绝。最终用三个普通点按显式间距组合源图可见点列；不声称恢复了源文件 Unicode。第二轮实际渲染后只做一次针对点距和脚标位置的修正，保留失败与前后结果。最终 32 条 `diagonal_glyph_bounds_require_visual_review` 提示保留，另有原有 Tokens 字宽提示；没有降低字号阈值或屏蔽阻断错误。

PDFium 返回的是轴对齐字形框，不能完全证明字形被斜框包容。运行时使用旋转框内的字形中心筛选文字，避免把外接矩形内的邻近字误认作本标签；斜边精确包容性仍要求人工复核。测试专门构造“本标签缺字、旁边恰有同字”的失败案例。详见[斜排格式](../skills/super-img2ppt/references/diagonal_text.md)、[能力引入前失败](evidence/world_models/diagonal_red.log)、[改进后验证](evidence/world_models/diagonal_neighbor.log)。

### 外框一致不足以证明公式一致

新增 [`compare-roi`](../skills/super-img2ppt/references/regions.md) 在固定同坐标 ROI 内保存原图/实际裁片、颜色掩码、外缘差、交并比与文件哈希。尺寸不一致直接失败，不缩放或配准。空掩码及触边截断会标记无效边缘指标；工具始终输出诊断 `review`，没有整图保真 PASS 阈值。

独立执行者对冻结的 Cosmos Policy 实际 PPTX 图使用另写的 Python 像素集合算法核对结果。黑色目标、容差 149，相当于三个通道均小于 150；未调阈值。三个区域均无触边。完整[独立结论](evidence/world_models/cosmos_policy/roi_forward_test/CONCLUSION.md)与[独立数值核验](evidence/world_models/cosmos_policy/roi_forward_test/independent_audit.json)保留。

| 区域 `[x,y,w,h]` | 外缘差 `[L,T,R,B]` px | 墨迹 IoU |
| --- | --- | --- |
| 标题 `[160,0,295,33]` | `[0,0,-1,1]` | 0.347165 |
| 小标签 `[198,42,104,19]` | `[-1,0,0,0]` | 0.386819 |
| `V(s′)` `[1095,439,65,31]` | `[1,0,-1,0]` | 0.228155 |

数值是指定墨迹掩码的重合程度，不是 OCR 正确率，也不能跨不同区域平均成“转换准确率”。外缘接近、字形不同的情况因此被明确暴露。另用 1600×638 的错误实际图验证退出码 2；之后补充失败报告的两侧尺寸字段，并通过回归测试。Cosmos 3 的宽表头诊断含下方边框、EOS 局部碰到邻边，只作描述性记录，未冒充孤立字形得分。

## 复建与验证范围

三个发布的 resolved scene 均从新的输出目录复建，再按源图宽度直接栅格化实际 PPTX 的 PDF。与归档实际 PNG 比较均为 **0 changed pixels**，见[复建命令与哈希](evidence/world_models/replay.json)。这是同环境复现，不是源图保真率。DreamZero 的 PDFium 输出多一行全白像素，经断言后裁去末行；另两例不裁切、不缩放、不配准。

本轮完整测试 **119 passed**：[原始日志](evidence/world_models/full_tests.log)。新增覆盖局部掩码、裁剪/空白边界、尺寸错误、原生斜排实际 PDF、邻字误归属和共同中心旋转后脚标顺序。原来的十二例文件和对照保持不变。终验与包级检查记录见 [delivery.json](evidence/world_models/delivery.json)。

图源只有栅格像素与本地 OCR，未用 PDF 文本/矢量坐标或作者绘图源码。开发期允许观察并修图，因此不是盲测。自动检查通过、可编辑性、复建一致与源图字形保真分别报告。没有新增依赖或字体安装，没有嵌入/分发字体，未验证原生 PowerPoint/WPS。

[十五例完整包](../examples/gallery/paper_gallery.zip) · [逐文件 SHA256](../examples/gallery/SHA256SUMS) · [README 实图](../README.md#2026-具身与世界模型)
