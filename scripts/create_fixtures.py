"""Create independently drawn, original acceptance images with known source text."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from super_img2ppt.fonts import FontCatalog

ROOT = Path(__file__).resolve().parents[1]


def main():
    out = ROOT / "examples"
    catalog = FontCatalog()
    latin = catalog.resolve("Example", None, None, False, False)
    cjk = catalog.resolve("中文", None, None, False, False)
    slides = []
    for page in range(2):
        width, height = (1280, 720) if page == 0 else (960, 720)
        canvas = Image.new("RGB", (width, height), "#F6F8FC")
        draw = ImageDraw.Draw(canvas)
        elements = []

        def shape(eid, box, fill, z=0, shape_name="round_rect", draw=draw, elements=elements):
            x, y, w, h = box
            if shape_name == "ellipse":
                draw.ellipse([x, y, x + w, y + h], fill=fill)
            else:
                draw.rounded_rectangle(
                    [x, y, x + w, y + h], radius=12 if shape_name == "round_rect" else 0, fill=fill
                )
            elements.append(
                {
                    "id": eid,
                    "kind": "shape",
                    "z": z,
                    "box": box,
                    "shape": shape_name,
                    "radius": 12,
                    "fill": fill,
                }
            )

        def text(
            eid,
            box,
            value,
            size,
            color="#17233B",
            container=None,
            family=None,
            bold=False,
            draw=draw,
            elements=elements,
        ):
            face = catalog.resolve(value, family, None, bold, False)
            font = ImageFont.truetype(face.path, size, index=face.index)
            draw.multiline_text((box[0], box[1]), value, font=font, fill=color, spacing=8)
            element = {
                "id": eid,
                "kind": "text",
                "z": 5,
                "box": box,
                "text": value,
                "font_size": size,
                "font_family": face.family,
                "cjk_font_family": cjk.family,
                "color": color,
                "bold": bold,
            }
            if container:
                element["container"] = container
            elements.append(element)

        if page == 0:
            text("title", [52, 32, 1150, 72], "从图片到可编辑文稿", 44, bold=True)
            text(
                "subtitle",
                [54, 116, 1130, 48],
                "Measured fonts · Explicit layers · Actual PPTX checks",
                25,
                family=latin.family,
            )
            cards = [
                (54, "font", "字体度量", "中文与 English", "Aa WWW iii 123", "#E8EFFC"),
                (454, "layout", "布局关系", "文字放进容器", "保留间距与层级", "#E6F3EE"),
                (854, "render", "渲染验收", "检查真实输出", "缺字与溢出可定位", "#F9ECDD"),
            ]
            for x, eid, heading, row1, row2, fill in cards:
                shape(eid, [x, 212, 372, 282], fill)
                text(
                    eid + "-heading", [x + 24, 236, 324, 58], heading, 32, container=eid, bold=True
                )
                text(eid + "-row1", [x + 24, 325, 324, 46], row1, 25, container=eid)
                text(eid + "-row2", [x + 24, 390, 324, 46], row2, 25, container=eid)
            shape("footer", [54, 550, 1172, 106], "#17233B")
            text(
                "footer-text",
                [80, 568, 1120, 60],
                "文字可编辑，简单形状可调整，复杂图片独立保留。",
                30,
                color="#FFFFFF",
                container="footer",
            )
        else:
            text(
                "title",
                [52, 36, 854, 66],
                "Layout and reading order",
                38,
                family=latin.family,
                bold=True,
            )
            for x, eid, label, fill in [
                (60, "input", "INPUT", "#DCE8FB"),
                (370, "edit", "EDIT", "#D9EEE4"),
                (680, "check", "CHECK", "#F9E5D6"),
            ]:
                shape(eid, [x, 176, 220, 104], fill)
                text(
                    eid + "-label",
                    [x + 32, 194, 166, 55],
                    label,
                    31,
                    container=eid,
                    family=latin.family,
                )
            for index, (start, end) in enumerate([(280, 370), (590, 680)]):
                points = [[start + 8, 228], [end - 8, 228]]
                draw.line([tuple(p) for p in points], fill="#53637F", width=3)
                draw.polygon([(end - 8, 228), (end - 19, 222), (end - 19, 234)], fill="#53637F")
                elements.append(
                    {
                        "id": f"arrow-{index}",
                        "kind": "line",
                        "z": 3,
                        "points": points,
                        "stroke": "#53637F",
                        "stroke_width": 3,
                        "arrow": True,
                    }
                )
            shape("body", [60, 342, 840, 264], "#FFFFFF")
            text(
                "line1",
                [84, 368, 786, 55],
                "Long labels stay inside their assigned boxes.",
                29,
                container="body",
                family=latin.family,
            )
            text(
                "line2",
                [84, 447, 786, 55],
                "Punctuation: (A + B) / C = 0.125",
                29,
                container="body",
                family=latin.family,
            )
            text(
                "line3",
                [84, 520, 786, 55],
                "多页保持顺序，4:3 与 16:9 等比适配。",
                29,
                container="body",
            )
        filename = f"source_{page + 1:02d}.png"
        canvas.save(out / filename)
        slides.append(
            {
                "id": f"page_{page + 1:03d}",
                "width": width,
                "height": height,
                "background": "#F6F8FC",
                "source": filename,
                "notes": f"第 {page + 1} 页备注：逐字保留。\nKeep speaker notes intact.",
                "reviewed": True,
                "elements": elements,
            }
        )
    scene = {"version": 1, "title": "Super Img2PPT acceptance examples", "slides": slides}
    (out / "reconstruction.json").write_text(json.dumps(scene, ensure_ascii=False, indent=2) + "\n")
    print(out / "reconstruction.json")


if __name__ == "__main__":
    main()
