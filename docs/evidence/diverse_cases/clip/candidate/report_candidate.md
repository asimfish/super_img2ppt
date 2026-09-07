CLIP 候选一复测：4 个原生梯形

在冻结原始报告与 93 个文件的 SHA-256 后，单独复测 v0.3.0 多边形接口。仅把 4 个编码器的填充图片及 16 条独立轮廓线替换成 4 个原生 polygon，并为其 8 行内部文字声明 container；文字、字号、网格、照片及原始 30 个 ROI 均保持基线 scene_04 的内容。实际 check pass，build 为 review；preflight/native_objects pass，rendered_text 保留原有两条 Text 宽度提示。未发生缺字或字体替换。

实际 PPTX 有 295 个对象：131 个含非空原生文字、153 个原生无文字形状、9 条连接线及 2 个照片图片。4 个新增多边形均在实际 PPTX XML 中验证为 a:custGeom 原生自由形状。除两个照片区域外，页面文字、矩阵、编码器填充/轮廓与连接线均可编辑。原始基线的 6 张图片减为 2 张。编码器采用源坐标 [301,81,160,240]、[301,441,160,240]、[1581,91,160,240]、[1441,461,160,240]，归一化顶点为 [[0,0],[1,1/6],[1,5/6],[0,1]]。

已打开实际 PPTX 整页渲染、提示词/梯形源像素对照。固定 30 ROI 的测量完全保持原基线：文字最大边差 2 px，中位 0 px，墨迹下缘代理最大差 1 px，9 处形状/网格线中心差全部 0 px。另对每个新梯形记录了 7 条源像素填充横截线和实际原生 XML，见 polygon_native_evidence.json。该补充验证针对新增的四个编码器，不替换原先固定 ROI。

候选一保留了原始 size-18 数学下标及其略细的视觉差异；没有重新改变数学字体来扩张本次试用。父任务后续提供的双方 glyph mask 修复将另做 candidate2，不覆盖本报告。箭头凹尾、部分省略点及 PowerPoint/WPS 未验证的限制与原始报告相同。字体仍为 Arial、Courier New、Times New Roman，无替换、无嵌入。

主要产物：

- PPTX：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/editable.pptx`
- SVG：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/svg/page_001.svg`
- 场景：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/scene_candidate_01.json`
- Resolved scene：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/scene.resolved.json`
- 字体：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/fonts.json`
- 验证：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/validation.json`
- 实际渲染：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/render/page_001.png`
- 源像素实际渲染：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/job/build_01/render/page_001_source_px.png`
- 固定 ROI 测量：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/measurements_build_01.json`
- 多边形实际 XML / 像素证据：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/polygon_native_evidence.json`
- 命令及输出日志：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/commands.jsonl`、`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/logs/`
- 运行时版本/hash：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/provenance_candidate.json`
- 原始证据完整性：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/original_integrity_check.json`（93 文件均未改变）
- 全部候选一产物：`/tmp/super-img2ppt-diverse-clip-f11ta96b/candidate/candidate_artifacts_manifest.json`

候选运行时路径 `/var/folders/ld/nb8clbcn2_nbslzr9xxl4scw0000gn/T/super-img2ppt-v030-candidate-k50on3nk/super-img2ppt/src/super_img2ppt/__init__.py`；版本 0.3.0；Python 文件树 SHA-256 `6307b3eaef166badd23e215e4dd68fbdd9d0089348416a82ac6d067fcfc144f4`；SKILL.md SHA-256 `f524d1b7c99fa0502e289d31f0348c061af3251e3d145c7eada013d6177634c6`。场景 SHA-256 `0a34aeba3f94d83db4c55351d450061e74677d2efcd39c44074cbe2920eaa6de`。构建使用显式候选 PYTHONPATH 与 `python -m super_img2ppt`，不修改仓库或运行时。
