# 六例完整论文图：新增多模态、长卷积与关系数据库

2026-09-12，v0.3.4。新增 BLIP-2、Hyena Hierarchy 和 Griffin，连同上一轮三个案例，
组成 [README 六例画廊](../README.md#真实复杂图效果)。每例提供完整原图、实际 PPTX
渲染、PPTX/SVG、可复建场景、字体清单、许可与失败记录。

[下载六例文件包](../examples/gallery/paper_gallery.zip) · [校验和](../examples/gallery/SHA256SUMS) · [第三方归属](../examples/gallery/NOTICE.md)

## 本轮实际结果

| 完整图 | 原生文本 / 形状 / 线条 | 图片边界 | 交付自动状态 | 冻结源图保真 |
| --- | --- | --- | --- | --- |
| BLIP-2，ICML 2023 Fig.2 | 48 / 71 / 18 | 猫与雪花两块，3.38% 面积 | review，文字宽度漂移 | 开发 3/8；保留 3 项有效失败、1 项无效掩码 |
| Hyena，ICML 2023 Fig.1 | 30 / 206 / 172 | 7 块无文字热图，10.37% 面积 | pass | 开发 2/8，保留 0/4 |
| Griffin，ICML 2025 Fig.1 | 139 / 139 / 60 | 无可见栅格图片 | pass，连字符检查已修复 | 开发 5/8，保留 0/4 |

图表、表格和矩阵均保留完整面板。Hyena 的杆状图是可见像素对应的原生杆与点，
不恢复原始实验数值；热图内部仍为图片。Griffin 的三张原始表、采样子图及模型结构
均可编辑，透明高亮采用实色近似。BLIP-2 保留三种掩码逐格图案及原图印刷拼写。

所有自动状态与图像保真分开。字体、数学符号、表格细线仍有差异；这些不是高保真全部达标案例。

## 评测方法与真实限制

独立任务读取官方论文的完整栅格图，没有使用原 PDF 文字/向量坐标或作者绘图代码
作为重建答案。每例记录 12 个固定区域，8 个开发、4 个保留。阈值为最大墨迹边界
误差 ≤4 源像素，同时未配准二值掩码 IoU ≥0.70；不同案例掩码定义各自固定，不汇总
成转换准确率。保留区域均在最终场景与 PPTX 哈希冻结后首次揭示，之后未改场景。

- BLIP-2 的 Cross Attention 白字区域错误地使用黑色墨迹阈值，两图均未检出字形。
  该项保持原始定义并标为 **无效**；不能当作一个有效失败或成功样本。
  另外三个保留区域是有效失败。原始报告与 null 边界结果全部保留。
- Griffin 最初源图底部有六像素 caption 碎片，父任务在首个成功渲染与指标反馈前要求
  修剪；原 source/contract v0 与更正版本均保留，不悄改来源。表头区域包含背景和网格，
  高 IoU 不单独证明文字准确。最终各 ROI 边界误差虽都 ≤1 px，多项字形/细线 IoU 仍失败。
- Hyena 初稿用固定杆间距采样，FFN 峰谷有偏差；父任务首图复核后改为真实杆中心。
  初稿按所有非文字包围盒交集生成的宽泛 overlap 声明也被移除，改为有来源依据的
  框/热图、杆/点、箭头和广播接点关系。保留修复前文件，不把初稿当作合规最终稿。
- 每个区域按三次有意义修复预算处理，包括 preflight。父任务的源图与首个实际图
  反馈发生在冻结前；字体与连接器的未解决差异如实保留。具体修复记录以原始报告为准。

原始报告：[BLIP-2](evidence/gallery_extension/blip2/REPORT.md) · [Hyena](evidence/gallery_extension/hyena/REPORT.md) · [Griffin](evidence/gallery_extension/griffin/REPORT.md)

## 真实案例带来的运行时修复

Griffin 原始 `validation.json` 报告 `User-` 和 `Cross-` 缺失，但 PPTX 中是正确的
连字符，实际 PDF 也显示笔画。PDFium 为行末连字符提供特殊表示：bounded text 返回
U+0002，range text 返回 U+FFFE；`FPDFText_IsHyphen` 明确标记该索引。
这与 [PDFium 官方接口](https://pdfium.googlesource.com/pdfium/+/refs/heads/chromium/6361/public/fpdf_text.h)
及[官方回归用例](https://pdfium.googlesource.com/pdfium/+/45a5ea16c998110d9aa2ce2dbf8d47ad1d2ae364/fpdfsdk/fpdf_text_embeddertest.cpp)一致。

v0.3.4 只在索引字符为 U+0002、引擎明确确认它为连字符、且文本框内标记数量一致时
恢复诊断文本。原始 `rendered` 与 `rendered_normalized` 并存；该字形仍参与归属、字体
和越界检查。不删除任意控制字符，不根据预期文字猜字符，API 缺失或不确认时保持失败。

两项实际 PPTX 渲染回归先失败、修复后通过；缺字、不应消失的连字符和未经确认的
控制字符仍失败。**同一份 Griffin PDF，两个 mismatch → 无错误，PDF 字节未变**。
[同文件复现证据](evidence/gallery_extension/hyphen_reproduction.json) · [原始红灯](evidence/gallery_extension/hyphens_red.txt)。

## 父任务复建、打包与检查

从发布的 resolved scene + assets 对六例重新执行完整 build。五例 pass，BLIP-2
保留文字宽度漂移 review。六例按各自原方法重栅格化，与冻结实际 PNG 的差异像素数均为 0。
原始 Griffin 自动 fail 报告保存在 `evidence/gallery_extension/griffin/frozen/`；
公开交付文件由修复后的 v0.3.4 重建，未修改图形、文本内容或保留区域结果。

Griffin 的原始 Poppler 命令显式指定 1460×724。初次复跑使用自动高度，导致 3060 个
像素不同；按原命令指定高度后归零。两次记录均保留，没有通过图像配准调整结果。
另五例复跑直接逐像素一致。[完整复跑记录](evidence/gallery_extension/replay.json)。

```bash
uv run super-img2ppt build examples/gallery/griffin/scene.resolved.json --out output/griffin
uv run super-img2ppt build examples/gallery/blip2/scene.resolved.json --out output/blip2
uv run super-img2ppt build examples/gallery/hyena/scene.resolved.json --out output/hyena
uv run python scripts/build_gallery_previews.py
uv run python scripts/build_gallery_bundle.py
```

生成器从 `examples/gallery/index.json` 读取明确列出的案例，生成完整对照与标明倍率的
局部细节；文件包包含各例场景、资产、真实 PDF/PNG 与许可。v0.3.3 原三例 ZIP 保留。
字体见各例 `fonts.json`；字体文件不嵌入也不分发。本机使用已有依赖，没有安装新字体。

[最终验证](evidence/gallery_extension/verification.json) · [独立技能包烟测](evidence/gallery_extension/package_smoke_v034.json) · [文件与链接核验](evidence/gallery_extension/artifact_checks.json)

本轮为 **CONDITIONAL** 交付：重建、可编辑文件与代码回归完成，复杂图像素保真仍存在
已记录失败，原生 PowerPoint/WPS 未单独验证。原始报告中的临时路径是历史工作目录；
可下载产物位于 `examples/gallery/{griffin,blip2,hyena}/`，脚本审计副本以 `.py.txt` 保存。
