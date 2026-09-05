# 六个公开真实案例的验证记录

2026-09-06，v0.1.1。**五例通过自动阻断检查，一例仍失败；不能说所有转换都已对齐、规范。**
输入为公开发布的真实图和演示页面，不是本项目绘制的测试图。六例来自三个来源，仍不足以代表所有模板。

| 案例 | 实际结果 | 可编辑对象：文字 / 形状 / 连线 | 仍需说明的差异 |
| --- | --- | --- | --- |
| [中文共识流程图](../examples/real_cases/consensus_zh/editable.pptx) | `pass` | 15 / 6 / 8 | 文字抽样边界差异最多 3 px；原生箭头头部约 5×6 px，源图约 18×18 px |
| [Matplotlib 表格与堆积柱图诊断稿](../examples/real_cases/matplotlib_table/diagnostic.pptx) | **`fail`，不是合格成品** | 41 / 31 / 22 | Verdana 的 Quake 字形与网格仍冲突；旋转纵轴标题是独立图片 |
| [NASA p6，多级密集段落](../examples/real_cases/nasa_06/editable.pptx) | `review` | 21 / 5 / 1 | 21 处文字边界最大差异 4 px；标志保留为图片 |
| [NASA p16，编号与强调框](../examples/real_cases/nasa_16/editable.pptx) | `review` | 19 / 1 / 1 | 19 处文字边界最大差异 3 px；标志和无文字的阴影边缘为图片 |
| [NASA p18，任务架构图](../examples/real_cases/nasa_18/editable.pptx) | `review` | 53 / 35 / 57 | 16 处文字抽样最多 4 px；箭头头部宽度约 13→9 px，圆柱曲线仍有差别 |
| [NASA p28，35 行缩略语表](../examples/real_cases/nasa_28/editable.pptx) | `review` | 72 / 35 / 1 | 左边缘/顶部差异至多 3 px，少数字宽差异为 4–7 px；标志为图片 |

`review` 的四张 NASA 页面均通过 preflight、原生对象和实际渲染文字检查，没有运行时字体替换；
它们含独立的标志图片，因此保留 `raster_text` 提醒。`pass` 仅代表自动检查通过。
NASA 文字页的底部双线等装饰也有细节差异，未宣称逐像素复刻。
所有页面都实际打开了 PPTX 渲染预览；没有把 JSON 或 Python 画出的预览当成 PowerPoint 输出。
正文、图例、数值和流程标签均为可编辑文字，没有整页位图背景或在原图文字上再覆盖一层文字。

## 原始失败与修复

中文流程图、Matplotlib 表格和 NASA 架构图分别在隔离工作目录中做前向评估。
评估者只得到 skill 与原始图像，没有收到期望 scene、源绘图程序、运行时代码、测试或其他案例答案。
另外三张 NASA 页面由主任务逐页看图、核对 OCR 后重建；不把它们称作独立盲测。
三项独立评估遵循 skill-creator 的 Independent Forward-Testing 要求。

1. **空白区域误报。** 初始表格检查有 131 个错误，其中 127 个是 overlap；
   70 个涉及文字框与线，另有 5 个文字框与柱体碰到的只是透明空白。
   现在文字与线/形状的检查也使用真实字体墨迹；斜边和字形角落再用有大小上限的 4 倍字形遮罩细查。
   真正覆盖笔画的负例仍报错，不会用 blanket overlap 豁免放行。
2. **菱形与行距。** 原始流程图要求整个矩形文字框塞进菱形，导致框和行距越挤越紧；
   实际导出后出现两条 `rendered_glyph_overflow`，第二行比源图高 6 px。
   修正容器规则后，只允许空白角落伸出背景，文字墨迹仍必须在内。
   恢复 1.15 行距，没有缩字号；实际文字检查通过，第二行顶部变为源图下方 3 px，仍如实记录差异。
3. **字体工具挂起没有诊断。** 本机默认 `fc-list` 指向 MiKTeX，多次在 30 秒后超时；
   旧 CLI 抛 traceback，没有 validation。现在超时/非零退出对 `check`、`build` 均记录失败并返回 2。
   后续运行只在进程 PATH 中优先选择机器已有的 Homebrew fontconfig；未安装字体或修改全局配置。
4. **页边线宽重复计算。** 线段多边形已经包含笔画宽度，旧边界检查又增加一次线宽，
   把位于页内的通栏线误报出界。现在只计一次，真正越界的线仍被拦截。

新增 10 项回归用例，均先观察到旧实现失败，再验证修复通过。全套 **43 项通过**。
字体异常测试覆盖 timeout/nonzero × check/build；几何测试同时包含可放行的空白和必须拦截的真实笔画。
另加入了大字号混合文本的边界用例：某段超过墨迹测量上限时，必须整体退回保守几何，不能只拿已测量的小字判断、遗漏大字碰撞。
未加入新的运行时依赖，遮罩上限为每项 800 万像素、最多缓存 8 项。

原始失败报告、独立文字测量及字体超时记录保存在
[证据目录](evidence/real_cases/index.json)。`.txt` 独立报告为原文存档，内部 `/tmp/` 链接属于历史工作目录；
当前可下载产物以本页和 [manifest](../examples/real_cases/manifest.json) 的仓库相对链接为准。
修复后的结果没有覆盖原始独立失败，运行时变更后的复跑也单独标记。

## 密集表格为何仍失败

在空白误报修复后，原始场景还有 61 个交集：47 个网格/刻度接点、5 个柱体与基线接点、9 个文字与线交集。
只对源图确实存在的 52 个接点声明具体对象关系；没有对文字添加 overlap 豁免。
根据字体墨迹调整表头/行标签的留白后，最佳场景仍有 `table_horizontal_1` 与 `header_3`（Quake）冲突。
尝试从源像素覆盖率重新定位网格没有改善整体结果，故保留更好的前一版，没有继续缩字或挪线掩盖问题。

生产 CLI 对此返回 2，并在导出前停止。为了让失败可检查，开发诊断流程单独导出了
`diagnostic.pptx` 和 SVG，并真的用 LibreOffice/PDFium 渲染。
这份稿的原生对象和渲染文字检查通过，**preflight 仍 fail**，`diagnostic_only=true`、
`production_cli_blocked=true`，没有伪装成正常 `build` 的成功产物。
实际预览中 Quake 的尾部也紧贴网格。下一步需要更贴近源图的字体及相应渲染证据，而非继续降低字号。

## 如何复现

每例目录包含 source 资产、`scene.resolved.json`、字体清单、validation、PPTX/SVG 和实际 PDF/PNG。
输入和 scene 的 SHA256、来源页码、原生对象数及产物哈希均在 manifest 中。
字体不分发；本次使用已有 Arial、Verdana、Hiragino Sans GB。不同机器缺字体会重新替代并报告，
不能要求另一个字体环境自动获得相同像素结果。

```bash
uv sync --frozen
uv run super-img2ppt doctor
uv run python scripts/run_real_cases.py --out output/real-rerun
```

全六例当前应退出 **2**，因为包含明确的失败表格；汇总写入 `summary.json`，不以“已知失败”为由返回全绿。
可选单例：

```bash
uv run python scripts/run_real_cases.py --cases nasa_16 nasa_28 --out output/nasa-rerun
```

在本次 Mac 上，若默认字体工具挂起，使用已有工具的进程路径：

```bash
PATH="/opt/homebrew/bin:$PATH" uv run python scripts/run_real_cases.py --out output/real-rerun-mac
```

测量以原始图像像素为单位，使用固定、隔离的文字区域和相同颜色阈值；右/下边界不含末像素。
NASA 三张文字页的区域在第一次 PPTX 渲染前保存；中文流程图沿用独立评估的区域。
流程图内部菱形掩码只用于排除边线，不能据此推断所有墨迹都在容器里。
报告不把墨迹边界匹配或平均差分换算成“还原率”。不同字体字形、抗锯齿和箭头形态仍需实际看图。

本次环境：macOS 26.2、Python 3.12.12、python-pptx 1.0.2、Pillow 12.3.0、
FontTools 4.64.0、pypdfium2 5.13.0、LibreOffice 26.2.4.2、fontconfig 2.18.3。
**未验证原生 PowerPoint/WPS**；之前 PowerPoint 自动化超时的记录仍保留在历史报告中。
没有用户自己的失败图片，不推断用户所有模板问题已经解决。

来源、署名、许可证与修改说明见 [NOTICE](../examples/real_cases/NOTICE.md)。
六例含三个来源，不把同一 NASA 文档的四页当成四个独立来源。
