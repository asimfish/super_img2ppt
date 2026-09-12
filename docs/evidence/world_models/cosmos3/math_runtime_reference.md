# Editable formula typography

Treat a formula as styled mathematical parts, not one bold-italic OCR string. Inventory
the source's variable weights, upright/italic operators and labels, script sizes, baselines
and punctuation spacing. A bold vector may sit beside a regular italic scalar and an upright
parenthesis. Do not impose a universal convention over visible evidence. Preserve epsilon
variants, minus versus hyphen, Greek letters and digit/letter distinctions.

Unicode script characters such as `ⁱ` can select another font and have unrelated dimensions.
Use ordinary `i`, `N`, `0` etc. at smaller sizes on explicit script baselines. Check repeated
instances, small transition boxes and initial distributions, not just the largest formula.

## Compose measured native parts

`compose-math` converts a baseline specification into ordinary scene text elements. It does
not parse TeX, recognize the image, infer spacing, or create an Office equation object.
The author supplies observed offsets; the helper measures font ascent, descent and italic
ink overhang to set frames without shifting the intended baseline.

```json
{
  "id": "policy", "origin": [120, 90],
  "font_family": "Liberation Serif", "font_size": 24, "z": 50,
  "parts": [
    {"text": "x", "offset": [0, 0], "bold": true, "italic": true},
    {"text": "i", "offset": [16, -13], "size_scale": 0.6, "italic": true},
    {"text": "k", "offset": [16, 7], "size_scale": 0.6, "italic": true},
    {"text": "+", "offset": [35, 0]},
    {"text": "y", "offset": [60, 0], "italic": true}
  ]
}
```

These coordinates illustrate the format; measure the actual source. `origin` is
`[x, baseline_y]` in source pixels. Each `offset` adds `[dx, baseline_dy]`; negative `dy`
raises the baseline. `size_scale` multiplies the formula font size. `bold` and `italic`
default to false independently for each part. Optional `color` at either level is `#RRGGBB`;
optional `container` names an existing background shape. Top-level `rotation` rotates the
whole formula around `origin`, including part positions; see [diagonal_text.md](diagonal_text.md). Parts receive IDs `policy_0`,
`policy_1`, etc. and consecutive z values. When replacing a formula, remove every old part,
including isolated commas, to avoid duplicated punctuation.

```bash
super-img2ppt compose-math formula.json --out job/math_01 --font-dir /path/to/existing/fonts
```

Review `elements.json`, `fonts.json` and `math.json`, insert the elements into the scene,
then run a full `build`. The helper returns `unverified`; it inserts no overlap exemptions.
If the whole formula is displaced, adjust the common origin; change individual offsets only
when the source shows a different relationship.

The requested family, glyphs, weight and italic face must be available. Substitution fails
explicitly: choose a suitable installed family and measure again. Fonts are not installed,
embedded or distributed; the editing machine still needs them.

Input is local JSON, at most 64 KiB, with 1–128 parts, 128 characters per part and 2048 total.
Parts are single-line visible text; effective font sizes are 1–300 source pixels. Unknown
keys, non-finite coordinates and Unicode superscript/subscript characters are rejected.
Nested scripts, fractions, radicals and multiline alignment are not automatically laid out;
use additional observed native parts/lines or disclose the unsupported layout.

## Actual-render acceptance

Compare source and actual PPTX crops at the same source resolution. Check variable/scalar
styles, script vertical order, commas, parentheses and repeated formulas. Inspect output
fonts for unexpected mixing. Record edge and glyph differences separately: equal bounding
boxes do not prove equal glyphs. Do not register the output, replace formulas with screenshots,
or declare success solely from text extraction.

A font found by the local measurer may still be substituted by the Office renderer. An
independent STIXGeneral trial produced native text successfully but failed the actual-render
font check. Times New Roman covered the body but not U+223C `∼`; never silently change that
relation into ASCII `~`. If no usable single family covers a formula, an explicitly disclosed,
separately composed symbol family is possible, but does not establish uniform source glyphs.
The delivered Diffuser Actor example retains such a DejaVu Sans relation beside Times New
Roman text. Remaining differences must stay visible in the source/actual comparison.
