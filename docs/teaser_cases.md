# super_teaser 三类复杂图测试

2026-09-10，使用用户指定的 [super_teaser](https://github.com/asimfish/super_teaser/tree/6b1d41b0b81ed09ed5cd692182ae05fc5573ac12) 中三张图片。
它们是生成的概念示意图，**不是论文原始图，也不是实验结果证据**。
下载固定到提交 `6b1d41b0b81ed09ed5cd692182ae05fc5573ac12`，文件 SHA-256 与 MIT-0 声明见
[来源证据](evidence/teaser_cases/sources.json)和[素材说明](../examples/teaser_cases/NOTICE.md)。

## 实际结果

| 图 | 原生可编辑对象 | 局部图片 | 自动检查 | 固定区域测量 |
| --- | --- | --- | --- | --- |
| [LoRA 矩阵/公式](../examples/teaser_cases/lora/editable.pptx) | 15 文字、13 形状、61 线条 | 3 | pass | 8/18 达标；四个补充圆角距离均 ≤2 px |
| [专家路由/加权合并](../examples/teaser_cases/routing/editable.pptx) | 37 文字、22 形状、28 线条 | 0 | pass | 25/25 达标 |
| [具身分层推理](../examples/teaser_cases/embodied/editable.pptx) | 45 文字、16 形状、20 线条 | 14 | review | 4/26 达标，22 个文字区域仍失败 |

每个链接旁的目录包含源图资产、SVG、scene JSON、字体清单、实际 LibreOffice PDF/PNG 和验证报告。
**自动 pass 不代表像素保真通过。** 各例阈值不同，不能把这些比例合并成转换准确率。

- LoRA 原始 18 区域：源尺寸暗像素阈值 RGB 最大通道 <110，边界最大误差 ≤3 px 且 IoU≥0.70。
  所有区域边界已在 3 px 内，十个区域字形/线条 IoU 仍不达标，底部公式 IoU 约 0.182。
  锁图标和两处图例纹理是可移动图片；字体为本机 Arial，无替换，但无法从源像素证明字体身份相同。
  四处弯角使用原生短线近似，P95 双向轮廓距离从 2.236/3/2.236/2.236 降至 2/2/1/1 px。
  此补充测量在发现弯角问题后冻结，未改变原 18 区域；文字与公式不变。
- 路由图 25 区域：RGB 最大通道 <170，或色差 >45 且最小通道 <170；边界、质心最大误差 ≤4 px，
  墨迹数量相对差 ≤25%。这是宽松的边界/覆盖检查，没有字形 IoU 门槛。
  从首次实际渲染 4/25，经 21/25 到 25/25；E1/E3 的 0.6/0.4 路径和加法合并保留，E2 无执行路径。
  阴影、纸纹、图标渐变简化，部分字重更轻，仍不是逐像素还原。
- 具身图 26 区域：最小通道 <160，边界/质心误差 ≤4 px，IoU≥0.45。
  四个线条区域达标；标题、正文基线、窄体字、数学斜体和多行间距仍有差异。
  机器人场景、花括号、关节和复杂轨迹保留局部图片；轨迹图片内的省略号明确声明为烘焙文字。
  `(Task)` 仍有字宽提示（测量 54.75 px，实际 51.952 px）。

## 从真实失败修复运行时

原 v0.3.0 将邻近 `Action` 的首字母 `A` 归入 `Flow matching` 的空白文本框，错误报告越界和字宽漂移。
原始 `Flow matching` 自身墨迹 x=1051.845–1142.106，框右边界为 1171；外来 `A` 的墨迹为
1166.242–1175.432。把框宽从 120 缩到 96 会消除误报，但不解决字形归属。

v0.3.1 根据完整 PDF 原生文字对象的文本与位置，仅在唯一归属明确时排除邻居字形。
归属不明确时继续保守检查，不增加重叠豁免或放宽误差阈值。
原失败场景字节完全相同的候选复测从阻断变为 review；最终场景恢复 120 宽度，保留图片文字声明。
前后实际渲染像素完全一致，所以本次运行时修复改善的是检查准确性，**没有改善具身图的字体保真**。

新增两项真实 LibreOffice 回归覆盖 0°/90°；负例覆盖缺字、真实越界和重复候选归属。
原版本两项均失败，修复后全套 **67 passed in 41.08s**，无跳过。
源失败、独立报告、候选报告及哈希索引见 [原始证据目录](evidence/teaser_cases)。

## 可复现边界

三位独立评估者只使用指定图片、冻结的 v0.3.0 skill 和现有工具重建，未把上游生成脚本、场景数据或提示词作为答案。
每例的 ROI 在重建前固定。具身图候选复测单独冻结运行时；父任务复跑最终三个场景并比较实际渲染像素，
同时复跑原六个通用案例、两个可分发 ICLR 案例、CLIP/Swin/热力图及本地 DDPM。
旧密集表格的失败必须保留，不能把批处理退出码 2 改为成功。

```bash
uv run python scripts/fetch_conference_sources.py \
  --cases teaser_lora teaser_routing teaser_embodied --out output/teaser-download
uv run python scripts/run_real_cases.py \
  --corpus examples/teaser_cases --out output/teaser-replay
```

字体来自本机现有文件，必要时通过 `--font-dir` 指向现有字体目录。素材和字体不进入独立 skill 包。
本轮未安装新第三方依赖或字体。运行环境为 macOS、LibreOffice 26.2.4.2 / PDFium 5.13.0；
PowerPoint/WPS 原生外观仍未验证。最终命令和哈希见 [验收证据](evidence/teaser_cases/verification_v031.json)。
