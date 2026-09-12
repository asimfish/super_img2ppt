# RT-2 Figure 1 完整架构图：独立转换实测

最终交付位于 `build_02/`：`editable.pptx`、`svg/page_001.svg`、`scene.resolved.json`、`fonts.json`、`validation.json`、`actual_source_width.png`。全部三栏与闭环照片下方文字完整保留。134 个原生对象（29 文本、47 形状、58 线段），以及 7 个独立照片裁块，面积 174,877 / 918,140 = 19.05%。不是全图背景叠字。

原图：Brianna Zitkovich et al., *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*, CoRL 2023, PMLR 229:2165–2183, Figure 1，PDF 第 2 页。正式来源 https://proceedings.mlr.press/v229/zitkovich23a.html ，PDF https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf 。作者保留版权；PMLR publication agreement 规定 CC BY 4.0（https://proceedings.mlr.press/pmlr-license-agreement.html）。本文件是改编重建，非作者原生文件；详细出处/哈希在 `provenance.json`。

源图生成只使用 PDFium 第 2 页的 scale=4 栅格（2448×3168），像素 crop=(432,281,2015,861)，所得 1583×580。未读取源 PDF 文本坐标、矢量坐标或作者绘图代码。运行时从生成后的 PDF 检查文本属于输出 QA。

实际验证：super-img2ppt 0.3.4，已安装字体目录与 LibreOffice。最终 preflight/pass、native_objects/pass、rendered_text/review；无阻塞错误。两个 review 为 RT-2 和 De-Tokenize 在实际渲染中相对字体测量的字宽漂移（分别约 2.48 与 3.38 像素），不是与原图的相似度证明。未在 Microsoft PowerPoint 或 WPS 检查。源字体身份不可从像素唯一确定；使用本机 Arial 常规/粗体，不分发字体。

人工看过完整 source、第一次实际渲染、源宽第二次实际渲染和动作区放大图。第一轮检查失败保留在 `check_01/`（过短箭头头部）、`check_02/`（0.1–0.25px文本框 reserve 与顶端标题/面板意图重叠）；通过扩展必要文本框并仅声明具名标题/面板关系修复。`build_01/` 保留原样。第二轮只修正动作区大号 Δ（可编辑三角形）、动作行距、标题字号及英文问句位置。没有全局 bbox overlap 免责。

仍有可见差异：源图的三张照片内浅紫运动箭头随照片保留，照片网格与极小背景产品印刷细节也是照片内容；所有图间连线、token、模块、可读标签与三张照片的 caption 原生可编辑。caption 的半透明底被可编辑纯灰底近似；圆角卡片阴影未复现；紫色弯箭头与下括号用原生折线近似，曲率有差异；字体及数学空格、度数位置与源图不完全一致，若干标签基线约 1–3px 偏高，标题和 Rotation 行字宽仍有差异。没有删减图内容来规避这些问题。

`diagnostics/` 是两个候选都已看过之后才冻结的 6 个源像素掩码诊断，冻结后没有再调图；所有源掩码已打开验证为目标标签。dev / heldout_exposed 只是分组，全部已经暴露，**不是盲测**。源宽真实输出不进行对齐配准。诊断可见文字 IoU 仅约 0.096–0.512，不能宣称高保真全部通过。其中 Rotation 输出墨迹接触固定 ROI 左边界，输出完整边缘诊断受限，不纳入任何通过率；其源掩码有效。其余 ROI 的最大边缘差分别 13、2、2、5、2px。此诊断不提供阈值通过率，也未用它继续调优。

复现：`zsh /tmp/rt2_forward_20260912/reproduce.sh /tmp/rt2_fresh_build_NAME`（输出目录必须全新）。原始重建脚本 `reconstruct.py`、场景 `job/scene.json`、照片 `job/assets/` 已保留。

最终源宽 PNG 的精确命令：

```sh
/opt/homebrew/bin/pdftoppm -png -singlefile -scale-to-x 1583 -scale-to-y 580 /tmp/rt2_forward_20260912/build_02/render/editable.pdf /tmp/rt2_forward_20260912/build_02/actual_source_width
```

本次未修改仓库、未安装依赖、未发布远端文件，未使用子代理。源码与输出检查的严格保真失败和已暴露诊断均保留。
