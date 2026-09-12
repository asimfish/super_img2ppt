# compose-math 初始化分布独立前向测试

结论：helper 能生成9个原生文本parts及明确脚本基线，但本轮尚未达到源图字形一致。可实际审阅候选是 `build_03/editable.pptx`（自动pass）及 `build_03/comparison_8x.png`（上源、下实际）。不应将其直接标记为高保真最终图。

源图仅从 `/Users/liyufeng/Code/super_img2ppt/examples/gallery/diffuser_actor/source.png` 读取像素；ROI `[100,655,137,34]`。未读原PDF、旧场景、旧排版答案，也未改repo或安装。全图坐标保留，`spec_03.json` 与 `math_03/elements.json` 可以嵌回完整场景。

观察源图：τ为粗斜体，上标N粗斜体，分布N常规斜体，括号/逗号常规正体，0与1粗正体。源上标N的基线明显高于τ。候选spec采用origin `[104.5,680.5]`、26px，N上标16px、baseline−10.5px（size ratio0.6153846）。所有9parts均原生text，无raster、无overlap豁免。不存在下标。

## 有界候选过程

1. `spec_01.json` / `math_01` 使用STIXGeneral，compose成功/unverified、preflight/native pass，但LibreOffice实际替换全部parts，rendered_text fail。τ和N替为LiberationSerif，∼替SimSun，0/1替Arial-Black，括号/逗号替ArialUnicodeMS；actual明确不可接受。详见build_01/validation.json。此为实际渲染字体可用性边界，不是compose错误。
2. 第一次修正：`spec_02.json` Times New Roman，保留U+223C，helper拒绝；本地字体cmap查明缺少∼。错误仅称需字体/glyph/style，未指出失败part，是诊断信息不足。
3. 第二次修正：`spec_03.json`采用可见波浪号ASCII `~`，Times New Roman；compose成功，build_03 pass。真实8×比较显示字体仍不匹配：0内孔更窄、τ字形不同，分布N偏大，括号/逗号形态不同，波浪号位置略左。这是编辑性的有效结果，不是源图一致性成功。字符从U+223C变成U+007E明确披露，源像素无法证明原Unicode码点。
4. 第三次修正：`spec_04.json` DejaVu Serif（支持U+223C）、主体24px、上标16px、distribution N0.9scale。compose成功，build_04 preflight阻断τ/N墨迹碰撞（没有掩盖或添加豁免），未产生实际PPTX。达到修正预算，停止继续试字体/移动对象。

## helper边界

- math.md写明spec整体一个family，parts不支持font_family，因此混合数学字体不能通过一个spec表达；可以由调用者分多个spec，但本轮未扩展为另一轮修正。
- compose不保证LibreOffice可使用本地量到的字体；build实际字体检查正确捕获STIXGeneral替代。
- 未找到明确helper代码缺陷；缺glyph错误没有part id是可改进诊断。没有修改任何helper代码。

## 复现命令

```sh
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt compose-math /tmp/diffuser-init-math-20260912/spec_03.json --out /tmp/diffuser-math-NEW --font-dir /System/Library/Fonts/Supplemental
```

`build_scene.py 03` 将已有math_03/elements.json放入原始尺寸场景，保持源坐标。build必须新目录：

```sh
PATH=/opt/homebrew/bin:$PATH /Users/liyufeng/Code/super_img2ppt/.venv/bin/super-img2ppt build /tmp/diffuser-init-math-20260912/scene_03.json --out /tmp/diffuser-build-NEW --font-dir /System/Library/Fonts/Supplemental
```

本次已用 `python render.py 03` 对build_03真实LibreOffice PDF执行 `page.render(scale=source.width/page.get_width())`，保存actual_raw.png、actual.png、actual_roi.png和comparison_8x.png；没有配准、叠加源图或截图替代。源/实际尺寸及比例见build_03/rasterization.json。该脚本的版本号映射build目录，重现本次固定目录结果时使用原03；其他输出目录需把路径参数化。真实字号与face见math_03/math.json和build_03/fonts.json。
