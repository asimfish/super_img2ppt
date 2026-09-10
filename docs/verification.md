# 验收记录

## v0.3.2：正式完整主架构图压力测试

2026-09-11：Grounding DINO（ECCV2024）、GLaMM（CVPR2024）、UniAD（CVPR2023）
三张完整主图完成独立重建、真实渲染、预设区域测量和父任务复跑。
**严格源图保真三例均 FAIL**；自动检查均 review，不把这解释成字体或布局正确。
范围、原始失败与源图版本核验见 [正式主图报告](main_figures.md)。
运行时实现与v0.3.1相同，仅版本常量变化；本轮改进说明、测试场景与固定源图下载配方。
本地全套 **67 passed in 35.67s**，无跳过；lint、格式、skill结构和治理检查通过。
最终质量检查、安装包smoke与哈希见 [verification_v032.json](evidence/main_figures/verification_v032.json)。
交付结论 **CONDITIONAL**：转换文件和失败可复查，但复杂主图高保真能力未通过验收，
PowerPoint/WPS原生外观仍未验证。

## v0.3.1：super_teaser 三类图与 PDF 归属修复

2026-09-10：全套 **67 passed in 41.08s**，无跳过。新增两项真实渲染回归覆盖
相邻标签的水平/90° 字形归属，以及缺字、真实越界、归属歧义负例。
独立基线、候选复测、最终场景与剩余保真失败见 [三类复杂图报告](teaser_cases.md)。
验收为 **CONDITIONAL**：自动检查修复有效，但具身图 22 个文字区域仍不满足保真阈值，
LoRA 仍有公式字形差异；原生 PowerPoint/WPS 外观未验证。
命令、复跑结果与产物摘要见 [verification_v031.json](evidence/teaser_cases/verification_v031.json)。

## v0.3.0：四种新图与实际失败修复

2026-09-07，本地 **65 passed in 58.88s**，无跳过。新增九项回归覆盖原生凸多边形、
水平/垂直渐变的真实渲染、主字符/下标相交误报及真正重叠的负例。
旧版本运行这些新增测试的失败输出与最终全套结果均保留。

CLIP、Swin、热力图完成冻结基线和独立前向测试；DDPM 表格/曲线为父任务的开发验证。
三组可分发产物包含 PPTX、SVG、源图、scene、实际 PDF/PNG、字体与验证报告。
CLIP 保留两条字宽审阅提示，热力图保留七个斜排标签的图片区域；DDPM 数学字宽仍有差异。
范围、测量方法、失败与可编辑文件见 [四种新案例报告](diverse_cases.md)。

最终代码已复跑上述四例、原有六个通用案例以及两例可分发 ICLR 场景。
旧密集表格仍失败，批处理退出码为 2；未把通过自动检查解释成全图对齐验收。
渲染器为本机 LibreOffice 26.2.4.2 / PDFium 5.13.0，PowerPoint/WPS 未新增验证。
没有新增第三方依赖或安装字体。字体解析依赖本机现有文件，清单与文件哈希随产物保留。

最终命令、产物与原始证据摘要见 [verification_v030.json](evidence/diverse_cases/verification_v030.json)，
独立安装见 [package_smoke_v030.json](evidence/diverse_cases/package_smoke_v030.json)。
安装包 SHA-256、对应提交和 GitHub Actions 结果在
[v0.3.0 发布记录](https://github.com/asimfish/super_img2ppt/releases/tag/v0.3.0)中固定。

## v0.2.0：真实顶会复杂图

2026-09-06：本地 **56 passed in 139.71s**，无跳过，包含 13 项新增回归。
原生旋转文字、自定义箭头、虚线经过实际 LibreOffice 导出；透明图片角落检测包含三个
缩放模式和旋转文字，并验证真实不透明碰撞、烘焙文字覆盖依然阻断。
ruff、格式、skill 结构与 8 个激活/排除静态案例、能力登记、确定性治理审计均通过。

ViT、MobileViT、Spatial-Mamba 三张正式 ICLR 论文图完成独立重建和候选复测，全部通过
自动阻断检查。两组可分发归档场景已在父任务重新导出并测量 23 / 33 个文字 ROI；
最大边缘差分别 2 / 1 px。MobileViT 的本地最终产物保留数学间距和斜角文字差异。
细节、来源、可编辑文件和失败证据见 [顶会测试报告](conference_cases.md)。
原有六例复跑仍为五例通过阻断检查、一例失败，运行器保持退出码 2。
这些检查不表示所有图像均能对齐或正确识别，也没有新增 PowerPoint/WPS 原生验收。

最终检查与归档文件哈希见 [verification_v020.json](evidence/conference_cases/verification_v020.json)。
安装包 SHA256 为 `6ac1655a25619379ebcd1b72d0782d72299a88f5cd6c1d8a32f1ee03ba08e227`；
已在全新临时环境离线安装锁定依赖和解包后的 skill，并实际重建 ViT、Spatial-Mamba，
两例均 pass，详见 [独立安装记录](evidence/conference_cases/package_smoke_v020.json)。

运行环境和依赖保持与 v0.1.1 相同，没有引入新的第三方依赖。安装包与远程 CI 证据见
[v0.2.0 发布记录](https://github.com/asimfish/super_img2ppt/releases/tag/v0.2.0)。

## v0.1.1：真实案例与几何修复

2026-09-06：全套 **43 项测试通过**，新增 10 项回归；ruff、格式、skill 元数据/引用和能力登记检查通过。
六个公开真实案例已从归档场景复跑，五例通过自动阻断检查，密集表格仍有一处字体/网格冲突。
全案例运行器保持退出码 2，不将已知失败改成成功。详细范围、源图与可编辑文件见
[真实案例记录](real_cases.md)，机器证据见
[verification_v011.json](evidence/real_cases/verification_v011.json)。

独立安装包 SHA256：`84a04e0b1510322b712da1c42a2c21131ef31801ce7c0aecc6ffdd676b4c5930`。
解包后的独立虚拟环境离线安装哈希锁定依赖，并实际重建中文真实案例；
步骤及退出码见 [package_smoke_v011.json](evidence/real_cases/package_smoke_v011.json)。
不包含字体或测试素材，原生 PowerPoint/WPS 仍未验证。

## 历史 v0.1.0 验收记录

日期：2026-09-06。发布候选结论：**CONDITIONAL**。
本地重建、原生对象导出、真实 LibreOffice 渲染及独立安装包检查通过；
原生 PowerPoint/WPS 外观、其他操作系统和用户真实失败样本尚未完成验证。
本记录支持本地开发版本交付，不包含 GitHub 发布或跨编辑器认证。

## 验收范围

用户要求创建自己的 `super_img2ppt` 图片转可编辑文件 skill，重点改善字体和形状重叠。
采用 Agent 看图重建场景、本地程序测量/检查/导出的分工，交付 PPTX、SVG、场景 JSON。
要求文字和简单形状保持原生可编辑，不用源图充当整页背景；异常有证据，不凭预览模拟图宣告成功。
自动识别任意图片结构、原字体的唯一识别、照片内部矢量化均不属于本版已实现能力。

| 验收项 | 证据与结果 |
| --- | --- |
| 原生可编辑性 | 示例 11 文本框、4 形状、2 线条，无 PPTX 媒体图片；修改文字后重新保存/读取测试通过 |
| 实际字体与字号 | 字形覆盖、真实宽度、严格字号/缩放下限、同组字号测试通过；故意替换渲染字体被阻断 |
| 间距漂移 | 故意增加 2 pt 字距、保持文字和字体不变，真实渲染返回 review；旧混排候选也被识别 |
| 重叠与越界 | 真实文字重叠、容器遮挡、烘焙文字重影被阻断；仅文本框留白相交不会误判为遮挡 |
| 多页与比例 | 图片输入顺序、PDF/PPTX 页序、原备注、4:3/16:9 等比适配与 resolved scene 重建测试通过 |
| 实际文件验收 | 原生 PPTX → LibreOffice PDF → PDFium PNG；修复后样例三组自动检查均 pass |
| 本地资产边界 | 相对路径、符号链接、危险 PPTX 结构及既有输出保护测试通过；独立越界用例实际阻断 |
| Skill 包 | 元数据、引用、schema、来源、能力登记检查通过；新虚拟环境按哈希安装并实际 build 成功 |
| 独立前向试用 | 从原图完成 OCR 校正、重建、预览与有限修复；发现混排间距缺口，已保留原始结论及后续修复证据 |

## 环境与运行结果

macOS 26.2（25C56），Python 3.12.12，uv 0.9.28，LibreOffice 26.2.4.2。
python-pptx 1.0.2、Pillow 12.3.0、fonttools 4.64.0、pypdfium2 5.13.0、jsonschema 4.26.0。
示例使用本机 Arial Regular/Bold、PingFang SC Regular，字体未嵌入或分发。

以下检查针对最终运行时代码；之后只补充了文档和交付产物。

| 命令/检查 | 实际结果 |
| --- | --- |
| `uv run ruff check .` | 通过 |
| `uv run ruff format --check .` | 28 个 Python 文件格式通过 |
| `uv run pytest -q` | **33 passed in 44.74s**；实际渲染测试已执行，未跳过 |
| `uv run python scripts/verify_skill.py` | pass，检查 8 个激活/排除案例和包结构 |
| `uv run python scripts/build_capability_registry.py --check` | 登记无漂移 |
| skill-creator `quick_validate.py skills/super-img2ppt` | Skill is valid |
| skill-quality-gate `audit_skill_governance.py --repo REPO --json` | 确定性审计 PASS，无 findings |
| `uv run python scripts/build_package.py` | 生成自包含 ZIP 格式 `.skill` 和 SHA256SUMS |
| 独立环境安装/调用 | 解包、哈希依赖安装、本地包安装、doctor、Swift 资源检查、实际 build 共 6 步退出 0；最终 pass |

8 个激活案例包含 4 个正例、4 个相邻负例及显式排除。静态检查验证的是这些案例及声明
的完整性，不是宣称进行了 8 次独立模型路由实验。另有一次独立重建任务和一次对抗输入
实际运行；详情见 [独立试用](forward_eval.md)。语义安全检查见 [security_review.md](security_review.md)。

两页 roundtrip 测试接受 pass 或 review，以允许报告平台字体替代与混排宽度差异；
原生对象和实际文字/字体阻断检查必须通过。专门的字体/字距注入测试验证错误不会被静默放行。

## 可复现的样例

在仓库根目录执行，输出目录必须尚不存在：

```bash
uv sync --frozen
uv run super-img2ppt doctor
uv run super-img2ppt build examples/flow_reconstruction.json --out output/reproduce_flow
uv run super-img2ppt build examples/flow_before_spacing_fix.json --out output/reproduce_before
uv run super-img2ppt build examples/reconstruction.json --out output/reproduce_multipage
```

前两条 build 命令的输入已实际运行：本机分别返回 pass、review。多页场景在 roundtrip 测试
中实际导出并再次重建。另一台机器字体不同可能返回 review，需读取字体清单与报告。

- [修复后原生 PPTX](../examples/editable_demo.pptx)、[原图](../examples/source_02.png)、[实际对比图](previews/comparison.png)
- [修复后 validation](evidence/flow_validation.json)、[旧候选 validation](evidence/before_validation.json)
- [文字边界测量](evidence/mixed_spacing.json)、[原生对象审计](evidence/native_objects.json)、[产物 SHA256 清单](evidence/artifacts.json)
- [测量方法和边界](../skills/super-img2ppt/BENCHMARK.md)、[安装包检查摘要](evidence/package_smoke.json)

已查看 `page_001` 全页及文字/图形细节的真实 PPTX 对比。标题边界保持，正文无截断或遮挡；
混排行的右界从多出 27 个源像素恢复到原图边界。箭头头部仍略小，抗锯齿和少数字形边缘有
差异。匹配墨迹边界不等于像素完全相同；机器报告中的 `visual_review: required` 保留不变。

开发初版曾出现请求 PingFang、实际 PDF 却使用宋体族的情况，文字内容检查仍成功。
本版显式使用字体文件中的本地化族名并检查 PDF 字体身份；当前检查回放旧产物识别出
11 处字体替代。这是本项目开发过程的失败复现，没有对上游运行效果进行量化对比。

## 安装包和来源

`dist/super-img2ppt.skill` 的本次检查 SHA256：

```text
ee1104a6edba6d81a3320b4e42898001cf981833076f3b0e6c2765be689f1418
```

包包含运行时、Swift OCR 资源、schema、说明、能力卡、激活案例及带哈希的运行依赖锁。
安装测试从新临时虚拟环境开始，用 `uv pip --require-hashes` 安装锁定依赖，再 `--no-deps`
安装解包后的 skill；在该环境中调用实际 build，未借用仓库的 editable Python 安装。
依赖和构建后端的初次安装可以访问包索引；离线转换要求它们及系统渲染器、字体事先可用。

上游只作为方法参考，固定提交、MIT 许可证和独立实现关系见
[UPSTREAM.md](../skills/super-img2ppt/UPSTREAM.md)。运行时声明与观察一致：读取指定输入及
本地字体，写入新输出目录，不含凭据读取、远程 OCR、上传或发布行为。

## 未完成的兼容性证据

- 原生 PowerPoint 16.112.3：尝试用生成的样例导出 PDF，自动化在 50 秒后超时，未取得 PDF；无法验证。
- WPS：未运行原生外观验收。Linux/Windows：工作流已配置，尚无对应实际运行结果。
- GitHub Actions `Verify`：配置了固定 action 提交及渲染依赖，本地仓库尚未推送，远程 CI 未执行。
- 未取得用户真实失败图片；现有样例不能代表任意论文图、复杂表格、特殊字体和历史模板。
- 复杂文字塑形、竖排、任意路径、数学排版不在本版外观保证内；当前 Pillow 构建无 RAQM。
- 未运行漏洞数据库扫描；原生文档/字体解析器的残余风险与限制已记入安全审查。
