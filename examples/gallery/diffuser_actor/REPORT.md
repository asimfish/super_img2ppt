# 3D Diffuser Actor 完整 Figure 1 原生重建

正式来源：Tsung-Wei Ke、Nikolaos Gkanatsios、Katerina Fragkiadaki，*3D Diffuser Actor: Policy Diffusion with 3D Scene Representations*，CoRL 2024 / PMLR 270:1949–1974，2025。https://proceedings.mlr.press/v270/ke25a.html

此图实际是 Figure 1，位于官方 PDF 第 4 页。保留 (a) 全部架构、(b) 五阶段去噪过程、(c) 六张真实任务照片及两个缩略图；未用简化示意图替换论文主图。原始 PDF 经 PDFium 4 倍（288 dpi）栅格化，整页 2448×3168；直接裁切像素矩形 (427,248,2016,1300)，得到 1589×1052。没有后续裁白、对齐注册、几何拉伸或原图覆底。没有读取 PDF 文本坐标、矢量路径、作者画图代码来获得重建答案。

交付：
- `job/build_06/editable.pptx`：最终 PPTX。
- `job/build_06/svg/`、`job/build_06/scene.resolved.json`：可编辑 SVG、解析后的场景。
- `job/build_06/fonts.json`、`job/build_06/validation.json`：字体及验证结果。
- `figure1.png`：完整来源裁切。
- `actual_final_source_width.png`：从最终 PPTX 导出的 PDF 按来源宽度真实栅格化，1589×1052。
- `actual_final_equations.png` / `actual_final_transition.png`：从上述真实图裁切放大的公式核验图。
- `provenance.json` / `assets_manifest.json`：来源、坐标、SHA256、资产边界与统计。

原生对象共 274 个：74 个原生文本框，90 个原生形状，110 条原生线。所有可读标签、任务描述及公式均为原生文字；数学上下标由独立原生文本框定位。19 个独立可移动无字栅格资产保留照片、深度图和点云艺术；矩形面积加总为 35.883%，并集为 35.307%。点云内无法独立裁开的 gripper 轨迹、部分相机射线、multiview 的三个短彩色箭尾仍随局部资产保留；它们不是全部独立可编辑。

最终自动检查：preflight PASS、native_objects PASS、rendered_text PASS。总状态 REVIEW 的具体原因是部分数学字符 Times New Roman → DejaVu Sans 字形替代；其余主要字体为 Arial、Times New Roman、Courier New。字体未嵌入。实际验证使用 LibreOffice / PDFium，未在 PowerPoint/WPS 中验证。

已逐图核验整图、右上输出公式及蓝色转移公式、雪花图标和任务描述。仍有明确可见差异：右上公式的字重、字形与源图数学字体不完全一致；部分标签宽度更宽；原图模块阴影省略；长去噪箭头为实色而非渐变；短弯箭头由折线近似；彩色小网格使用单色采样单元，未复现单元内部细微渐变。固定来源坐标下的后验开发测量见 `development_ink_diagnostics.json`：五个标签左/上边差约 -2～+2 px，右边差 +2～+9 px。该诊断在看过候选图后进行，不是盲测或独立测试，不能作为整体保真度百分比。

每轮失败报告保留于 `job/check_01`、`check_02`、`build_01`～`build_05`（check_01 为凸多边形校验失败，工具在生成 validation 前退出；其后各轮 validation 保留）。所有重叠声明均限定实际存在的具体对象对：雪花与抓手连接处、相机射线端点、点云白边旁数学框、照片缩略图覆盖角等，没有通用碰撞豁免。

版权仍归原作者。独立转换任务未在摘要页找到明确许可；发布前父任务另行核对了 PMLR 官方 publication agreement 第 2–3 条，其规定论文以 CC BY 4.0 授权并要求链接原论文：https://proceedings.mlr.press/pmlr-license-agreement.html 。该通用协议网页已存证，不声称取得作者单独签署文件，也不套用代码仓库许可证。原始独立报告和 provenance 保留于证据目录。

复跑（使用现有环境，不安装）：

```sh
zsh /tmp/diffuser_fig2_zPTOQk/reproduce.sh /tmp/diffuser_figure1_rebuild_NEW
```

最终真实图的确切栅格命令：

```sh
/Users/liyufeng/Code/super_img2ppt/.venv/bin/python /tmp/diffuser_fig2_zPTOQk/render_source_width.py /tmp/diffuser_fig2_zPTOQk/job/build_06 /tmp/diffuser_fig2_zPTOQk/actual_final_source_width.png
```

`render_source_width.py` 直接读取最终 `render/editable.pdf`，用 `scale=1589/page.get_width()` 调用 PDFium，断言输出尺寸 1589×1052；不重采样/移动输出。其 PDF 尺寸为 960.0094604492188 × 635.555908203125 pt，scale=1.6551920220207588。


交付路径说明：报告中的 build/job 与 /tmp 路径是独立测试的历史目录。当前目录的 scene.resolved.json 与 assets/ 可直接复建；完整失败和诊断证据位于 [GitHub 测试记录](https://github.com/asimfish/super_img2ppt/tree/main/docs/evidence/embodied_figures/diffuser_actor)。

## v0.3.5 formula revision (2026-09-12)

The current distributed files replace 32 old formula text objects with 60 explicitly styled
native text parts: two output equations, three repeated denoising equations and initialization.
Current counts: 102 text, 90 shapes, 110 lines (302 native), 19 raster assets. All automated
checks PASS. Source fidelity remains incomplete, including numeral widths, Greek glyphs,
parentheses and commas. U+223C remains an explicitly selected DejaVu Sans symbol beside
Times New Roman body text; no ASCII tilde substitution is delivered. Text parts are not OMML.
The previous report above describes the v0.3.4 original; its PPTX/render/scene/font/check records
are archived in docs/evidence/formula_gallery/diffuser_actor/before_* at repository root.
See docs/formula_gallery.md for changes, actual before/after crops and failed attempts.
