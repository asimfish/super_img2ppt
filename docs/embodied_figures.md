# 具身智能完整论文图实测

> 历史批次记录：下述计数和状态属于 v0.3.4。当前 Diffuser Actor 公式已修订，见[新增具身案例与公式修订](formula_gallery.md)。

2026-09-12，运行时 v0.3.4。本轮新增 RT-2、3D Diffuser Actor 和 ViNT，覆盖机器人
VLA、三维动作扩散和视觉导航。[完整对照与下载](../README.md#具身智能与机器人) ·
[本轮冻结九例文件包](https://github.com/asimfish/super_img2ppt/blob/56712f5b70ddea937206043e127fe08612c0a9d0/examples/gallery/paper_gallery.zip) · [第三方归属](../examples/gallery/NOTICE.md)。

三个独立任务只从官方 PDF 栅格图重建，没有读取原 PDF 的文字/向量坐标或作者绘图代码。
父任务检查了每张完整原图、首个实际 PPTX 渲染、最终源宽渲染和关键局部，并从交付场景复建。
这批是有人工反馈的真实案例测试，**没有盲测通过率，也不保证所有复杂图均能精确对齐**。

## 图面与编辑边界

| 完整论文图 | 原生对象 | 保留的图片 | 自动状态与限制 |
| --- | --- | --- | --- |
| RT-2，CoRL 2023 Fig.1 | 29 文本、47 形状、58 线 | 7 块，19.05% 面积；照片内运动箭头不拆分 | review：RT-2 / De-Tokenize 字宽漂移 |
| 3D Diffuser Actor，CoRL 2024 Fig.1 | 74 文本、90 形状、110 线 | 19 块，矩形并集 35.31%；点云内抓手轨迹等不拆分 | review：部分数学字符 Times New Roman → DejaVu Sans |
| ViNT，CoRL 2023 Fig.2 | 27 文本、63 形状、25 线 | 3 块，13.40% 面积；照片堆叠、边框和白色路径仍为栅格 | review：7 Tokens 字宽漂移 |

面积以各例报告的局部图片矩形面积为准，不等于图片内容全部可编辑。3D Diffuser Actor
同时保留完整模型架构、去噪序列和真实机器人任务三个面板；其 CoRL 会期是 **2024**，
PMLR 论文集出版年份为 **2025**，不能将它写成 CoRL 2025。

所有任务说明、图间标签和模块文字均为原生文本；照片中的微小产品印刷和场景纹理属于
照片内容。照片内部不可分离的轨迹或点云可视化没有被宣称为原生几何。
公式采用文字与上下标部件重建，不是 Office 原生公式对象。

## 实际发现和修正

- RT-2 的 Δ 大小和动作行距经过修正；法文、动作 token 和三栏内容保留。
  照片 caption 的纯灰底近似了原半透明背景，圆角阴影未重建，弯箭头与括号采用折线近似。
- ViNT 修正希腊符号、竖排标签字体及位置；Self-Attention 的固定区域墨迹边缘差从
  约 11 px 垂直偏移缩小到 `[0,-1,0,+1] px`。这是参与修正的诊断区域，不能称为盲测。
  字重和斜体仍偏粗，秒表小按钮及位置编码曲线也有近似。
- 3D Diffuser Actor 修正冻结编码器雪花图标、特征网格、公式上下标与预测标签间距。
  长去噪箭头使用实色近似渐变；数学字体、块体阴影与源图仍不同。

RT-2 另做了看过候选后的六处固定源掩码诊断，IoU 约 0.096–0.512，保真未全部达标。
Rotation 的实际墨迹接触 ROI 左边界，完整边缘诊断受限，未纳入任何通过率。
ViNT 的五处文字边缘检查也属于已观察区域，不证明字形一致或整图准确。
原始失败检查、字体扫描超时和修正前记录均保留，不通过放宽判定或删除内容消除失败。

报告：[RT-2](evidence/embodied_figures/rt2/REPORT.md) ·
[ViNT](evidence/embodied_figures/vint/REPORT.md) ·
[3D Diffuser Actor](evidence/embodied_figures/diffuser_actor/REPORT.md)。

## 可复建交付

每例下载目录包含 `editable.pptx`、`svg/`、`scene.resolved.json`、`assets/`、
`source.png`、`actual.png`、`actual.pdf`、字体和检查记录，另有来源与修改说明。
使用新输出目录复建，例如：

```bash
uv run super-img2ppt build examples/gallery/rt2/scene.resolved.json --out output/rt2_rebuild
uv run super-img2ppt build examples/gallery/vint/scene.resolved.json --out output/vint_rebuild
uv run super-img2ppt build examples/gallery/diffuser_actor/scene.resolved.json --out output/diffuser_rebuild
```

复建使用原有本地字体目录与 LibreOffice，未安装依赖或分发字体。
RT-2 按 Poppler 显式源宽/高生成展示；ViNT 的 PDFium 源宽渲染因页面尺寸舍入多出一行，
仅在确认末行全白后裁去，原始 1435×437 PNG 仍存证。没有配准、平移或缩放渲染图来掩盖偏移。

[来源、页码与裁切哈希](evidence/embodied_figures/source_audit.json) ·
[父任务复建记录](evidence/embodied_figures/replay.json)。

三例从发布场景复建后，与冻结实际预览的差异像素数均为 **0**。这证明展示可以复现，
不是源图保真指标。3D Diffuser Actor 的 resolved scene 已明确记录替代后的字体，复建
状态为 pass；最初字体替代 review 和实际交付文件仍保留，未通过改变图像刷掉告警。

[本地工具与打包检查](evidence/embodied_figures/verification.json) ·
[文件完整性、链接与画廊校验](evidence/embodied_figures/artifact_checks.json)。
九个 PPTX 均通过 ZIP 完整性检查；新增三例的字体、结构和实际文字检查随文件提供。
当前画廊 ZIP 可确定性重建，原有六例产物及十张预览与上一提交一致。

本轮扩展案例与证据，没有从个别手调结果推断出通用运行时修复，skill 和运行时版本保持
v0.3.4。原有六例场景/产物保留；此前六例冻结包仍在 v0.3.4 Release。
验证范围为 LibreOffice，原生 Microsoft PowerPoint / WPS 尚未单独检查。
