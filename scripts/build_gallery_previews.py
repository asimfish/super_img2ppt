"""Compose labeled comparisons from the checked-in source and actual PPTX renders."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def comparison(source, actual, title, out):
    if source.size != actual.size:
        raise ValueError("Source and actual must have the same pixel dimensions")
    w, h = source.size
    pad, header = 28, 88
    canvas = Image.new("RGB", (w * 2 + pad * 3, h + header + pad), "#F1F5F9")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=24)
    small = ImageFont.load_default(size=17)
    draw.text((pad, 17), title, fill="#0F172A", font=font)
    draw.text((pad, 52), "SOURCE / full figure", fill="#475569", font=small)
    draw.text(
        (w + 2 * pad, 52), "EDITABLE PPTX / actual LibreOffice render", fill="#475569", font=small
    )
    canvas.paste(source.convert("RGB"), (pad, header))
    canvas.paste(actual.convert("RGB"), (w + 2 * pad, header))
    canvas.save(out)


def main():
    out = ROOT / "docs/previews/gallery"
    out.mkdir(parents=True, exist_ok=True)
    for name, title in [
        ("galore", "GaLore / ICML 2024 / Figure 6"),
        ("vision_mamba", "Vision Mamba / ICML 2024 / Figure 2"),
        ("mamba2", "Mamba-2 / ICML 2024 / Figure 7"),
    ]:
        case = ROOT / "examples/gallery" / name
        with Image.open(case / "source.png") as source, Image.open(case / "actual.png") as actual:
            comparison(source, actual, title, out / f"{name}.png")
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


if __name__ == "__main__":
    main()
