# 新增复杂正式论文图测试（2026-09-11）

本轮使用 v0.3.2（基线 `f730ba51c51636cd84f8ed5397651bcbffe8269a`），新增三张完整顶会主架构图，以及一张主要由图片组成的三维重建示例。三张主图均导出了原生可编辑对象并实际渲染，但**均未达到严格高保真标准**。这次改进了各案例的重建场景，增加了可复现图源和保留区域评估；没有证据支持新的运行时算法修复，因此不更改技能版本。

| 正式来源 | 完整范围 | 原生对象（文字 / 形状 / 线） | 局部图片 | 最终开发区域 | 最终保留区域 |
| --- | --- | --- | --- | --- | --- |
| BEVFormer · ECCV 2022 · Figure 2 | 整体网络、空间注意力、时间注意力三面板 | 23 / 145 / 49 | 7 | 2/24 | 1/11；另 1 项无效 |
| InternImage · CVPR 2023 · Figure 3 | 四阶段、stem/downsampling、残差块、堆叠公式 | 77 / 18 / 80 | 1 | 10/28 | 2/14 |
| DUSt3R · CVPR 2024 · Figure 2 | 双分支网络、数学输出、相机坐标、点云 | 31 / 24 / 60 | 4 | 2/16 | 1/8 |

DUSt3R 的第二页是完整 Figure 3，含 17 个可以独立移动的图片区域。照片、深度图、置信图与三维重建内容仍为栅格，不能编辑内部结构，也不计为另一张可编辑主架构图。

## 图源与可复现性

- [BEVFormer 正式论文](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136690001.pdf)：PDF 第 5 页，4 倍渲染裁剪 `[530,450,1930,985]`，1400×535。
- [InternImage 正式论文](https://openaccess.thecvf.com/content/CVPR2023/papers/Wang_InternImage_Exploring_Large-Scale_Vision_Foundation_Models_With_Deformable_Convolutions_CVPR_2023_paper.pdf)：PDF 第 3 页，4 倍渲染裁剪 `[1290,280,2110,1390]`，820×1110。Figure 3 中 DCNv3 为残差块内的节点；不虚构论文该图没有的采样细节面板。
- [DUSt3R 正式论文](https://openaccess.thecvf.com/content/CVPR2024/papers/Wang_DUSt3R_Geometric_3D_Vision_Made_Easy_CVPR_2024_paper.pdf)：PDF 第 4/5 页，3 倍渲染，Figure 2 裁剪 `[146,222,1642,574]`，1496×352；Figure 3 裁剪 `[148,206,1640,450]`，1492×244。

```sh
uv run python scripts/fetch_conference_sources.py \
  --cases bevformer_main internimage_main dust3r_main dust3r_qualitative \
  --out output/complex_sources
```

下载配方固定 PDF SHA256。父侧重新下载、渲染所得四张 PNG 与独立测试输入逐字节一致，见 [来源复现记录](evidence/complex_figures/parent/fetch_comparison.json)。可公开读取论文不等于图像再分发授权；本轮未确认图像授权，论文及派生 PPTX/SVG 保留本地，GitHub 保存来源配方、测试程序和文字证据。

## 如何测试

三个独立执行者读取冻结技能，以论文栅格图重建；没有用 PDF 文字坐标、矢量路径或作者绘图代码作答案。制作场景前冻结区域与阈值，以实际 PPTX 经 LibreOffice 导出的 PDF 在源图宽度栅格化，比较墨迹边界和像素交并比：最大边界差 ≤4 px 且 IoU ≥0.70 才通过，不进行平移配准。

约三分之二的区域用于开发，三分之一的数值反馈留至最终候选哈希冻结后测量，之后不再修改候选。整张图在制作时始终可见，因此这是**同图区域数值反馈保留**，不代表未知图上的泛化能力。不同图的区域内容、大小和颜色掩码不同，不用通过率为模型或图难度排名。

父侧独立重建三个最终场景，四页实际渲染像素完全一致，并重新核验最终候选哈希以及冻结技能文件。重建输入采用 `scene.resolved.json`，其中已有实际选中的替代字体，故其自动状态均为 pass；原始 BEVFormer 和 DUSt3R 因字体替换仍为 review，不能用复跑状态抹掉警告。InternImage 原始自动状态为 pass，但区域保真依然失败。详见 [复跑](evidence/complex_figures/parent/parent_replay.json)、[完整性](evidence/complex_figures/parent/parent_integrity.json)、[人工检查](evidence/complex_figures/parent/parent_visual_review.json)。

## 修正、失败和评估限制

**BEVFormer：**完成 Carlito 字体校准、数学样式、彩色标签、三维侧面和层级修正，保留全部三面板。部分修正没有提高严格通过数；网格密度、曲线近似、下标字形仍不准确。固定 Temporal 区域的彩色掩码被黄色底色占满，原始记录 4/36 中这 1 项是指标盲区，不能证明文字还原；可信主汇总为 3/35，另列 1 项无效。原始数据不改写，最终冻结后的补充深色文字诊断不用于调参。见 [原始报告](evidence/complex_figures/bevformer/report_original.md)及[更正说明](evidence/complex_figures/bevformer/report_addendum.md)。

**InternImage：**开发区域由初次实际渲染的 4/28，经三轮修正达到 10/28；修正了加号被圆形背景遮盖、数学分段位置、斜体左侧留白和节点尺寸。保留区域仅 2/14 达标。stage i 仍使用直立 i；公式间距、维度表达式字形仍不同。固定 rule4/DCN 区域包含边框，因此部分误差是混合墨迹误差，不能全部归因于字形。见 [原始报告](evidence/complex_figures/internimage/report_original.md)。

**DUSt3R：**开发区域从 1/16 到 2/16，保留区域 1/8。修正了点云裁剪与标签/箭头空白区相交、部分基线与原生指数位置；尝试 Noto Sans 导致实际溢出，失败版本保留。字体、点云边缘曲线接缝、token 纹理简化和数学排版仍不合格。**修正预算偏离：**将失败字体试验、回退与后续指数修正都计入时，部分区域超过预定三轮；不把这些区域列作满足预算的成功案例。见 [原始报告](evidence/complex_figures/dust3r/report_original.md)。

三例均未建立因果运行时缺陷；已发现的问题主要来自识图重建、字体选择、细粒度数学排版和几何近似。下一步应针对这些失效类型做受控修正，并在新的完整图上验证，避免只调熟悉图的坐标。Microsoft PowerPoint/WPS 原生打开效果未验证，未安装新字体或依赖。

## 交付与证据

本地文件位于 `output/complex_figures_20260911/deliverables/{bevformer,internimage,dust3r}/`：包含 `editable.pptx`、`svg/`、`scene.resolved.json`、`assets/`、`fonts.json`、`validation.json` 与 `render/`。原始失败和独立测试目录路径记录在各报告及哈希清单中。

[证据索引](evidence/complex_figures/index.json)逐文件保存原始 SHA256；测试脚本以 `.py.txt` 保存原始字节，避免误作生产代码。源图、图像和完整重建场景未上传。自动检查结果与保真验收分别报告，保真结论为 **FAIL**。

交付检查：67 项测试通过（30.18 秒），Ruff、技能结构、激活样例、能力注册表和治理检查通过；重新构建的技能包 SHA256 与已发布 v0.3.2 相同。见 [检查原始记录](evidence/complex_figures/parent/final_checks.json)。三份独立清单共 438 个文件全部通过哈希复核，见 [复核记录](evidence/complex_figures/parent/independent_hash_readback.json)。
