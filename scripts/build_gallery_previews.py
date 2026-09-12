"""Compose labeled comparisons from the checked-in source and actual PPTX renders."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def comparison(source, actual, title, out, scope="full figure"):
    if source.size != actual.size:
        raise ValueError("Source and actual must have the same pixel dimensions")
    w, h = source.size
    pad, header = 28, 88
    canvas = Image.new("RGB", (w * 2 + pad * 3, h + header + pad), "#F1F5F9")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=24)
    small = ImageFont.load_default(size=17)
    draw.text((pad, 17), title, fill="#0F172A", font=font)
    draw.text((pad, 52), f"SOURCE / {scope}", fill="#475569", font=small)
    draw.text(
        (w + 2 * pad, 52), "EDITABLE PPTX / actual LibreOffice render", fill="#475569", font=small
    )
    canvas.paste(source.convert("RGB"), (pad, header))
    canvas.paste(actual.convert("RGB"), (w + 2 * pad, header))
    canvas.save(out)


def main():
    out = ROOT / "docs/previews/gallery"
    out.mkdir(parents=True, exist_ok=True)
    index = json.loads((ROOT / "examples/gallery/index.json").read_text())
    for entry in index["cases"]:
        name, title = entry["id"], entry["title"]
        case = ROOT / "examples/gallery" / name
        with Image.open(case / "source.png") as source, Image.open(case / "actual.png") as actual:
            comparison(source, actual, title, out / f"{name}.png")
            if "detail_box" in entry:
                x, y, w, h = entry["detail_box"]
                box = (x, y, x + w, y + h)
                a = source.crop(box).resize((w * 2, h * 2), Image.Resampling.NEAREST)
                b = actual.crop(box).resize((w * 2, h * 2), Image.Resampling.NEAREST)
                comparison(a, b, title + " / detail", out / f"{name}_detail.png", "detail / 2x")
    # Fixed inspected crop, identical coordinates, nearest-neighbor enlargement exposes seams.
    case = ROOT / "examples/gallery/galore"
    box = (145, 115, 345, 255)
    with Image.open(case / "before_caps.png") as before, Image.open(case / "actual.png") as after:
        before = before.crop(box).resize((800, 560), Image.Resampling.NEAREST)
        after = after.crop(box).resize((800, 560), Image.Resampling.NEAREST)
        comparison(
            before,
            after,
            "Same PPTX curve geometry / before and after round caps / 4x",
            out / "curve_caps.png",
        )
        # The first input here is an actual pre-fix render, not the paper source.
        with Image.open(out / "curve_caps.png") as im:
            draw = ImageDraw.Draw(im)
            draw.rectangle((28, 49, 750, 78), fill="#F1F5F9")
            draw.text(
                (28, 52),
                "BEFORE / actual PPTX / segmented end gaps",
                fill="#475569",
                font=ImageFont.load_default(size=17),
            )
            im.save(out / "curve_caps.png")
    formula_comparison(out / "formula_typography.png")


def formula_comparison(out):
    """Same-coordinate 4x crops: source, archived actual, revised actual."""
    case = ROOT / "examples/gallery/diffuser_actor"
    before = ROOT / "docs/evidence/formula_gallery/diffuser_actor/before_actual.png"
    if not before.exists():
        return
    regions = [
        ("Output equations", (1435, 105, 1563, 170)),
        ("Repeated denoising equations", (241, 635, 326, 670)),
        ("Initialization / residual glyph differences remain", (99, 652, 238, 689)),
    ]
    pad, scale, column, row_header = 24, 4, 556, 44
    height = 84 + sum((b[3] - b[1]) * scale + row_header + pad for _, b in regions)
    canvas = Image.new("RGB", (column * 3 + pad * 4, height), "#F1F5F9")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)
    for i, label in enumerate(["SOURCE", "BEFORE / actual PPTX", "AFTER / actual PPTX"]):
        draw.text((pad + i * (column + pad), 25), label, font=font, fill="#0F172A")
    with (
        Image.open(case / "source.png") as source,
        Image.open(before) as old,
        Image.open(case / "actual.png") as actual,
    ):
        y = 84
        for title, box in regions:
            draw.text((pad, y), title, font=font, fill="#475569")
            y += row_header
            for i, im in enumerate([source, old, actual]):
                crop = im.crop(box)
                crop = crop.resize(
                    (crop.width * scale, crop.height * scale), Image.Resampling.NEAREST
                )
                canvas.paste(crop, (pad + i * (column + pad), y))
            y += (box[3] - box[1]) * scale + pad
    canvas.save(out)


if __name__ == "__main__":
    main()
