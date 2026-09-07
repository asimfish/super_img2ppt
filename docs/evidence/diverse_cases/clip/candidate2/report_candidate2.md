CLIP 候选二复测：原生梯形与 20 px 数学下标

最终保留 `/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/editable.pptx`。候选二 check pass，实际 build 为 review；preflight/native_objects 均 pass，实际 PDF 无缺字、无字体替换。仍仅有两条 Text 标签的宽度审阅提示，其源墨宽及实际渲染均约 43 px，不能据此宣称构建完全像素一致。

本轮在候选一的 4 个原生 polygon 基础上，原样恢复已保留 scene_03 中的 106 个 Times New Roman 数学文字对象，包括 20 px 下标与既有源坐标修正。没有增加任何重叠豁免，没有降低严格 fit 限制，没有移动矩阵。此前冻结 v0.2.0 对该数学子场景报告的 9 个基字/下标碰撞，在候选二成为 text_frame_overlap_only 信息项；具体原始对与新结果见 nine_pair_retest.json。运行时修复来自父任务；本独立试用没有检查或修改其实现，也未访问父任务的回归测试。

实际 PPTX 的 295 个对象包含 131 个非空原生文字对象、153 个原生无文字形状和 9 条连接线，合计 293 个原生非图片对象；另有 2 个独立照片区域。4 个编码器为原生可编辑多边形，包含填充与轮廓；矩阵文字、格线、点号、连接线均为原生对象。左侧照片叠放保持一个独立图片区域，无法恢复被遮住的照片内容。

已打开实际 PPTX 整页渲染及源像素矩阵/预测部分对照，20 px 下标正常显示，无相邻字符被 PDF 检查误认。固定 30 ROI 沿用最初冻结的坐标与掩码，不以新区域替代：21 个文字 ROI 的最大绝对边差为 1 px，中位为 0 px，墨迹下缘代理最大差为 1 px；9 个形状/网格 ROI 的线中心偏差均为 0 px。基线方法中的墨迹下缘是可见基线代理，非真实字体基线识别。原始逐项偏差及两个紫色表头掩码的抗锯齿 bbox 干扰仍完整保留。

| 版本 | 数学下标 | 原生非图片 / 照片及填充图片 | 固定文字最大边差 | 网格/形状线中心最大差 | 自动构建 |
| --- | --- | --- | --- | --- | --- |
| 冻结原始 build_04 | 18 px | 305 / 6 | 2 px | 0 px | review |
| 候选一 build_01 | 18 px | 293 / 2 | 2 px | 0 px | review |
| 候选二 build_01 | 20 px | 293 / 2 | 1 px | 0 px | review |

四个梯形还用相同的 28 条源行扫描填充边界，连续填充段左右边的最大偏差为 0 px。候选一初始宽松颜色 min/max 曾将绿色描边外侧一个孤立抗锯齿像素误记为填充，得到 +11 px；该初始数据未覆盖。像素值诊断及同一行坐标的连续段复测在候选一 measurement_addendum.md 与两轮 polygon_contiguous_fill_evidence.json 中保留。这个更正不改变原先固定 30 ROI 的任何结果。

最终字体仍为 Arial、Courier New、Times New Roman regular，fonts.json 无替换、无嵌入。源字体身份不能由位图唯一证明。实际渲染器为 LibreOffice 26.2.4.2，未做 Microsoft PowerPoint/WPS 原生应用验证。剩余视觉差异包括小字号抗锯齿、部分省略点较轻，以及源图凹尾箭头与原生实心三角箭头的轮廓差别。

原始报告及其 93 个文件均通过 SHA-256 复验；候选一快照内全部文件也未改变。两次冻结失败候选 scene_01 / scene_03、对应 check/build 报告和后续成功候选均保留。完整性证据为 `/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/prior_evidence_integrity.json`。

主要产物：

- 本报告：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/report_candidate2.md`
- 最终 PPTX：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/editable.pptx`
- 可编辑 SVG：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/svg/page_001.svg`
- Scene：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/scene_candidate2_01.json`
- Resolved scene：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/scene.resolved.json`
- 字体：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/fonts.json`
- 验证：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/validation.json`
- 实际整页渲染：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/render/page_001.png`
- 实际 PDF：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/render/editable.pdf`
- 源像素实际渲染：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/render/page_001_source_px.png`
- 源/实际矩阵对照：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_01/render/compare_matrix_source_px.png`
- 冻结 30 ROI：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/fixed_rois.json`
- 最终测量：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/measurements_build_01.json`
- 梯形连续填充边测量：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/polygon_contiguous_fill_evidence.json`
- 9 对原始失败区域复测：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/nine_pair_retest.json`
- 命令及日志：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/commands.jsonl`、`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/logs/`
- 运行时版本/hash：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/provenance_candidate2.json`
- 所有本轮产物绝对路径/hash：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/candidate2_artifacts_manifest.json`
- 冻结原始报告：`/tmp/super-img2ppt-diverse-clip-f11ta96b/report_original.md`
- 候选一报告：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/report_candidate.md`

本轮加载 `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v030-candidate2-074ftier/super-img2ppt/src/super_img2ppt/__init__.py`，版本 0.3.0；Python 文件树 SHA-256 `785d64e8ad3a4cd7128de31811b04da9a014b444f8c593f215bda857e1b11112`；SKILL.md SHA-256 `f524d1b7c99fa0502e289d31f0348c061af3251e3d145c7eada013d6177634c6`；场景 SHA-256 `559b7163f764245052215a43aa8fa576fda4a4ea17c4437123b3689625496fb4`。所有写入均位于独立临时目录，未修改仓库、冻结运行时、依赖或字体。

复现命令（使用新输出目录）：

```sh
PATH=/opt/homebrew/bin:$PATH PYTHONPATH=/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v030-candidate2-074ftier/super-img2ppt/src /Users/liyufeng/Code/super_img2ppt/.venv/bin/python -m super_img2ppt build /tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/scene_candidate2_01.json --out /tmp/super-img2ppt-diverse-clip-f11ta96b/candidate2/job/build_reproduction_NEW
```
