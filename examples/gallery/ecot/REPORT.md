# ECoT 完整主方法图正向测试

最终候选：`build_04/editable.pptx`，实际源宽预览 `build_04/actual_source_width.png`。构建自动状态 **pass**；已目视实际全图及公式、模块标签、长提示词细节。没有运行 Microsoft PowerPoint/WPS。

选用官方 PMLR 论文 **Figure 4**（第5页完整数据生成流水线），而非 Figure 1 teaser 或 Figure 2 转载 OpenVLA 小图。包含 Dataset 输入、Describe scene、Extract bounding boxes、Compute motion primitives、Compute gripper position、Generate plans + subtasks 全部六栏/面板，未删去复杂提示词。完整页 `page5_full.png`，源图 `source.png`（1587×593）。作者、出版物和 CC BY 4.0 证据见 ATTRIBUTION.md。

## 编辑性和限制

- 40 个 native text，26 个 native shape；11 个 image 实例，10 个不同源资产。四个 detector 框为 native rectangle。
- 所有可读正文/模块标签/数学表达式均为 native text。照片上的 “black robotic arm” 已切除原始像素并替换为 native rectangle + text，无烘焙重复文字。
- 保留 raster：三张叠放的 observation 照片、重复的 detector 照片、带分割轮廓的 gripper 照片；另有 rainbow、DINO、Python、owl、Gemini 五个小 logo 和一个 curved arrow。因此并非严格的“仅照片 raster”结果。弧形箭头不具原生编辑性；此 schema 不支持相应凹形弧箭头，未冒充原生。
- 所有 overlap 均为明确命名的源图可见关系：叠卡、照片叠放、前景公式覆盖后卡、检测框覆盖照片和交叉框、透明挖孔的标签面板。不使用 blanket overlap 豁免。

## 数学与字体

图中有两处 `[Δx, Δθ, ΔGrip]`；此图没有上下标，不能用于证明上下标定位能力。`Proprio 1:` 用 Arial Bold；方括号、逗号、Δ、Grip 用 Arial Regular；x 用 Arial Italic；θ 经放大对照采用 Times New Roman Italic 单独 run（22 source px），主体21.2 px。源像素不能唯一识别字体，这些是视觉选择，未读取PDF字体或文本。Times θ 相比全Arial版本更接近源图细笔画和椭圆形态。正文包含 regular、bold、italic、bold italic；词语色彩按源图分run保留。fonts.json 记录5个真实字体face，无替代告警；字体不嵌入。

固定ROI在首次实际候选 build_02 后冻结，没有图像配准。灰度<145墨迹阈值边界测量，详情见 build_04/ink_measurements.json；边界并不等于字形一致：

| ROI | actual−source 左/上/右/下（源像素） |
|---|---|
| 输入公式 | 0 / +1 / 0 / 0 |
| 输出公式 | +1 / +1 / +1 / 0 |
| Prismatic | 0 / 0 / −1 / 0 |
| arm label | 0 / 0 / −1 / +1 |
| dataset title | 0 / +1 / −1 / +2 |
| 长提示词固定行 | +1 / 0 / −4 / 0 |

源图/实际渲染放大图保存在 `build_04/detail_*.png`，上方源图，下方实际PPTX。保留字形笔画/kerning差异、个别正文数像素宽度和标题1–2像素垂直差。检测照片重用相同 observation 的清洁crop，其取景可能有约1–2像素差；照片边框和圆角近似。未给出虚构一致率。

## 实际渲染与复现

先由技能 build 将 native PPTX 经 LibreOffice 导出 `build_04/render/editable.pdf`，然后运行：

```sh
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/ecot-forward-20260912/render_actual.py /tmp/ecot-forward-20260912/build_04
```

脚本实际调用 `page.render(scale=1587/page.get_width()).to_pil()`。PDF页960.0094604492188×358.7243957519531 pt，scale 1.653108709217712，PDFium原始输出1587×594，保存 `actual_source_width_raw.png`。逐像素断言额外末行全白后仅裁末行，最终1587×593；证明见 rasterization.json。没有先缩放/配准源图来隐藏误差。

复现：`zsh /tmp/ecot-forward-20260912/reproduce.sh /tmp/ecot-rebuild-NEW`。需要现有 repo .venv、LibreOffice、指定系统字体；不安装依赖。`prepare_source.py` 仅 rasterize 官方PDF第5页，并按像素裁 `(432,285,2019,878)`；未读取PDF文本/矢量坐标。`reconstruct.py` + `repair1.py` + `repair2.py` + `repair3.py` 保留改动过程。build_01为失败preflight，build_02/03/04保留可比较实际候选；最终仅选择build_04。公式经历有界两轮实际细节修复。

可编辑交付：`build_04/editable.pptx`、`build_04/svg/page_001.svg`、`build_04/scene.resolved.json` 及其 `assets/`；审计：`build_04/fonts.json`、`build_04/validation.json`、`provenance.json`。本任务仅写入 /tmp，未改仓库、安装、上传或运行作者代码。
