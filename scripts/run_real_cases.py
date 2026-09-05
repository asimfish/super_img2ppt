"""Rebuild published cases; any blocked case keeps the overall run unsuccessful."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image
from super_img2ppt.cli import build
from super_img2ppt.prepare import fresh_directory, json_write
from super_img2ppt.scene import InputError, load_scene, safe_asset

CORPUS = Path(__file__).resolve().parents[1] / "examples" / "real_cases"


def compare_anchors(source: Path, preview: Path, anchors: list[dict]) -> dict:
    """Diagnostic source-pixel bounds; does not certify visual acceptance."""
    with Image.open(source) as original, Image.open(preview) as rendered:
        images = [original.convert("RGB"), rendered.convert("RGB")]
        images[1] = images[1].resize(images[0].size, Image.Resampling.LANCZOS)
    results = []
    for anchor in anchors:
        roi = anchor["roi"]
        boxes = []
        for im in images:
            mask = Image.new("L", (roi[2] - roi[0], roi[3] - roi[1]))
            pixels = mask.load()
            for y in range(roi[1], roi[3]):
                for x in range(roi[0], roi[2]):
                    rgb = im.getpixel((x, y))
                    selected = (
                        min(rgb) > anchor["threshold"]
                        if anchor["polarity"] == "light"
                        else max(rgb) < anchor["threshold"]
                    )
                    if "interior_diamond" in anchor:
                        cx, cy, rx, ry, fraction = anchor["interior_diamond"]
                        selected &= abs(x - cx) / rx + abs(y - cy) / ry < fraction
                    if selected:
                        pixels[x - roi[0], y - roi[1]] = 255
            box = mask.getbbox()
            boxes.append(
                [box[0] + roi[0], box[1] + roi[1], box[2] + roi[0], box[3] + roi[1]]
                if box
                else None
            )
        results.append(
            {
                "id": anchor["id"],
                "source": boxes[0],
                "rendered": boxes[1],
                "edge_delta_px": [b - a for a, b in zip(*boxes, strict=True)]
                if all(boxes)
                else None,
            }
        )
    return {
        "method": "Frozen isolated regions; original source size; exclusive right/bottom edges",
        "interpretation": "Diagnostic bounds only, not a fidelity score or a full-page acceptance gate",
        "regions": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--cases", nargs="+")
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument("--font-dir", type=Path, action="append", default=[])
    args = parser.parse_args()
    corpus = args.corpus.resolve()
    manifest = json.loads((corpus / "manifest.json").read_text())
    known = {c["id"]: c for c in manifest["cases"]}
    requested = args.cases or list(known)
    if len(set(requested)) != len(requested) or any(c not in known for c in requested):
        parser.error("Case IDs must be unique members of the selected corpus manifest.json")
    fresh_directory(args.out)
    summary = {"all_blocking_checks_passed": False, "visual_review": "required", "cases": []}
    for case_id in requested:
        case = known[case_id]
        scene_path = safe_asset(corpus, case["scene"])
        out = args.out / case_id
        try:
            report = build(scene_path, out, font_dirs=tuple(args.font_dir))
            anchors_path = scene_path.parent / "anchors.json"
            scene = load_scene(scene_path)
            content_png = out / "render" / f"{scene['slides'][0]['id']}_content.png"
            if anchors_path.exists() and content_png.exists():
                anchors = json.loads(anchors_path.read_text())["anchors"]
                source = safe_asset(scene_path.parent, scene["slides"][0]["source"])
                json_write(out / "alignment.json", compare_anchors(source, content_png, anchors))
        except (InputError, OSError, ValueError, RuntimeError) as exc:
            report = {"status": "fail", "error": str(exc)}
        summary["cases"].append(
            {"id": case_id, "status": report["status"], "error": report.get("error")}
        )
        print(f"{case_id}: {report['status']}", flush=True)
    summary["all_blocking_checks_passed"] = all(
        c["status"] in {"pass", "review"} for c in summary["cases"]
    )
    json_write(args.out / "summary.json", summary)
    return 0 if summary["all_blocking_checks_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
