# v0.3.3：从复杂图反馈到可复用能力

2026-09-12。新增 GaLore Figure 6、Vision Mamba Figure 2、Mamba-2 Figure 7 三张
ICML 2024 完整图。独立任务从官方论文的栅格图开始重建，没有用原 PDF 文本/向量坐标
或作者绘图代码作为答案。完整画廊见 [README](../README.md#真实复杂图效果)，
[来源与许可](../examples/gallery/NOTICE.md)。用户提供的未公开稿件图像未进入公开资产。

## 固定验收范围

本轮要求：把曲线和字体的实际问题反馈到通用运行时；补正反向回归；新增三张完整复杂图，
保留实际 PPTX 渲染、编辑边界和未达标区域；README 提供完整对照、下载与证据。
不把“原生对象多”或自动 `pass` 等同于像素保真，也不宣称原生 PowerPoint/WPS 已验证。

| 案例 | 原生文字 / 形状 / 线条 | 图片 | 原始构建状态 | 区域联合阈值达标 |
| --- | --- | --- | --- | --- |
| GaLore | 74 / 4 / 675 | 1 块无文字交叉区，占 1.8058% | pass | 初始记录 3/7；冻结后补充 1/3 |
| Vision Mamba | 42 / 45 / 71 | 3 块图像/patch | pass | 开发 5/8；保留 0/4 |
| Mamba-2 | 202 / 25 / 248 | 0 可见图片 | review，字体替代 | 初始记录 2/6；冻结后补充 0/3 |

各任务固定区域要求墨迹边界最大误差 ≤4 源像素，且未配准二值掩码 IoU ≥0.70。
灰度/颜色阈值、ROI 是否包含相邻几何各不相同，详见各自 contract；不能合并为转换准确率。
GaLore 额外绿色曲线区域使用颜色掩码，IoU 0.949、边界误差 0 px；仅是该片段的诊断。

## 流程偏差与失败

- Vision Mamba 在最终哈希冻结后才查看四个保留区域，之后未再修场景，0/4 达标。
  Forward/Backward Conv、小 token 和箭头仍存在可见差异。
- GaLore 的测量脚本在调整阶段输出了原保留区域结果；这些属于已接触复查区域。
  冻结后新增三个区域仅测一次，不能恢复整次实验的盲测资格。
- Mamba-2 在看过原保留区域后修改了共享几何；同样不能当盲测。
  公式区域严格计数为四次有意义修复，超过三次预算，报告原样披露。
- 三例都还有严格保真失败。标题字宽、公式字形、细线相位、token 间距是下一步待解决项。
  未删除失败区域、放宽阈值、配准移位或通过栅格文字覆盖来制造达标。

## 真正进入运行时的改进

1. `trace-curve`：明确 ROI/颜色、显式参考线排除、小缺口记录、三点平滑与有界 RDP，
   输出原生线段、overlay 和可审计诊断。真实平台保留；同色分支/长遮挡拒绝猜测。
   GaLore 首轮陡线失败促成 `--axis y`，长遮挡继续保留失败并采用可见片段/小图像。
2. `line_cap`：PPTX `a:ln cap="rnd"` 与 SVG `stroke-linecap="round"` 一致，端点
   圆盘参与几何检查。GaLore build03 → build04 的 558 个对象只改变 cap 属性；
   [实际前后图](previews/gallery/curve_caps.png)与[差异列表](evidence/public_figures/galore/cap_scene_diff.json)保留。
3. 字体识别：Avenir Next Condensed TTC 斜体 face 的 OS/2 标志为 0，但 `head.macStyle`
   为 2。此前把 index 4 当 regular；修复后 regular 选 index 7。测试构造相同元数据矛盾，
   先观察 False 的失败，再修实现。字体文件未分发。
4. 文字越界：报告 left/top/right/bottom 的点值和源像素值；阻断阈值保持 0.75 pt。
   指南说明左侧斜体越界应调整左边框与内边距，保持字形原点，不能只扩大右侧。

[曲线用法](../skills/super-img2ppt/references/curves.md) · [场景端点协议](../skills/super-img2ppt/references/scene.md#plain-line-end-caps)

## 复建与证据

```bash
uv run super-img2ppt build examples/gallery/galore/scene.resolved.json --out output/galore
uv run super-img2ppt build examples/gallery/vision_mamba/scene.resolved.json --out output/vim
uv run super-img2ppt build examples/gallery/mamba2/scene.resolved.json --out output/mamba2
uv run super-img2ppt trace-curve examples/gallery/galore/source.png \
  --roi 220 75 160 107 --color '#ADC477' --tolerance 35 \
  --stroke-width 4.7 --prefix green130 --out output/green130
uv run python scripts/build_gallery_previews.py
```

字体以各例 `fonts.json` 为准；无这些字体的环境会产生替代/失败，不能保证相同截图。
本机显式使用已安装 LibreOffice 和系统字体目录，没有安装新字体或第三方依赖。
在最终运行时中，从公开的 resolved scene + assets 对三例重新执行完整 build，全部退出 0、
自动状态 pass。Mamba-2 原始构建的替代记录仍为 review；resolved scene 已保存选定字体，
因此复建 pass 不抹除原始替代事实。[独立复跑记录](evidence/public_figures/replay.json)。三例按原方法重新栅格化后，与画廊冻结 PNG
的差异像素数均为 0，见[逐例像素复核](evidence/public_figures/replay_pixels.json)。

公开 `actual.png` 来自冻结候选的实际 PPTX → LibreOffice PDF → 源宽 PNG；Mamba-2
源宽图用 Poppler 栅格化，另外两例使用 PDFium。未做图像配准。
`source.png` 和场景 `assets/` 中的源图用于对照，不是覆盖整页的可见背景。

原始报告中的 `/tmp/...` 是当时的工作目录；发布后的可下载产物在
`examples/gallery/{galore,vision_mamba,mamba2}/`，原始报告/命令/ROI/失败证据在
`docs/evidence/public_figures/`。作者脚本以 `.py.txt` 保留审计，不作为运行时入口。

- [GaLore 报告](evidence/public_figures/galore/REPORT.md)
- [Vision Mamba 报告](evidence/public_figures/vision_mamba/REPORT.md)
- [Mamba-2 报告](evidence/public_figures/mamba2/REPORT.md)
- [回归、打包与治理结果](evidence/public_figures/verification.json)
- [独立包烟测](evidence/public_figures/package_smoke_v033.json)

代码验收与画面保真分开判定：回归/导出可通过，复杂图整体高保真目标仍未通过。
