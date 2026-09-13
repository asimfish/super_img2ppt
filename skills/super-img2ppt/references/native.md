# Replace raster interiors with native editing objects

Use this when selected pictures in an existing PPTX contain simple tensor blocks or formulas
that need internal editing. `compose-math` produces text fragments; this route creates actual
Office equations. It does not recognize image contents or parse arbitrary TeX automatically.

```bash
super-img2ppt replace-raster build_02/editable.pptx --plan native-plan.json --out build_native
```

The plan binds the exact input SHA256 and names unique, top-level picture targets. It keeps
all other shapes and the replacement's position in paint order. Each cuboid is an independent
three-face group; each equation is a text shape containing `a14:m / m:oMathPara / m:oMath`.
Photographs remain images. Do not flatten whole arrays or formulas to avoid reconstruction.

```json
{
  "version": 1,
  "source_sha256": "REPLACE_WITH_ACTUAL_64_CHARACTER_SHA256",
  "width": 1000, "height": 500,
  "replacements": [{
    "slide": 1, "image": "formula_crop",
    "items": [{
      "id": "formula_crop", "kind": "equation", "box": [100,100,200,50],
      "font_size": 24, "color": "#101522",
      "expression": [{"base": {"hat":"x"}, "sub":"0", "sup":"2"}, "=", {"num":"a", "den":"b"}]
    }]
  }]
}
```

Coordinates and font sizes use the declared source canvas; it must match the slide aspect
ratio. `box` must stay on canvas. A cuboid item uses `kind: cuboid`, `box`, positive `depth:
[dx,dy]` smaller than its box, and `front`, `top`, `side` hex colors. A text item uses `kind:
text`, `text`, `font_size`, `color`. No line/path or generic OOXML insertion is supported.
Cuboid faces are native freeforms with theme effects explicitly disabled.

Equation expressions accept strings; nonempty sequences; `{text,style}` with `p/b/i/bi`;
`{base,sub}`, `{base,sup}`, `{base,sub,sup}`; `{hat:...}`; `{num:...,den:...}`;
and `{sqrt:...}`. Unsupported structures fail. Variables use italic single letters by default;
set styles explicitly when the source differs. Equations request STIX Two Math, text requests
Times New Roman. Fonts are not embedded or installed; verify the target editing machine.
This is a bounded subset, not a full TeX compiler, matrix editor or automatic formula OCR.

Input limits: 2 MB plan; 200 MB PPTX plus archive guards; 200 replacements; 1500 native items;
512 nodes and depth 16 per equation; token length 256. Duplicate targets/items, existing name
collisions, invalid source hashes and non-picture targets fail. No input is overwritten.

Inspect `editable.pptx`, `render/page_001.png`, `plan.json`, `native.json`. `review` means
rendered and ready for human review, not color/layout certification. `--no-render` yields
`unverified`. Remaining pictures are listed recursively. The original scene and SVG are not
updated: regenerate and rebind/replay the plan if the input PPTX changes. This route does not
inherit the previous build's fidelity verdict. Compare changed regions with the source and
verify Office editing separately from LibreOffice rendering.

Schema references: [Microsoft TextMath](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.linq.a14.m)
and [OfficeMath](https://devblogs.microsoft.com/math-in-office/officemath/).
