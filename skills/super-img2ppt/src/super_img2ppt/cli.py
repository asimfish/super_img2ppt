"""Local command line entry point used by the skill and by reproducible checks."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.metadata
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

from .curves import trace_file
from .export import write_pptx, write_svg
from .fonts import FontCatalog
from .layout import layout_scene
from .prepare import fresh_directory, json_write, prepare
from .qa import comparison, inspect_pptx, preflight
from .render import make_renderer, rasterize_pdf, verify_rendered_text
from .scene import SCHEMA, InputError, load_scene, safe_asset, slide_transform


def resolve_scene(scene: dict, layouts: dict, root: Path, out: Path) -> dict:
    resolved = copy.deepcopy(scene)
    (out / "assets").mkdir()
    copied = {}

    def copy_asset(value: str) -> str:
        if value not in copied:
            source = safe_asset(root, value)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            relative = f"assets/{digest[:20]}{source.suffix.lower()}"
            target = out / relative
            if not target.exists():
                shutil.copyfile(source, target)
            copied[value] = relative
        return copied[value]

    for slide in resolved["slides"]:
        if "source" in slide:
            slide["source"] = copy_asset(slide["source"])
        for element in slide["elements"]:
            if element["kind"] == "image":
                element["path"] = copy_asset(element["path"])
            elif element["kind"] == "text":
                layout = layouts[slide["id"], element["id"]]
                element.pop("text", None)
                element.pop("font_group", None)
                element["fit"], element["wrap"] = "strict", False
                element["font_size"] = layout.effective_font_size
                runs = []
                for index, line in enumerate(layout.lines):
                    if index:
                        runs[-1]["text"] += "\n"
                    for fragment in line.fragments:
                        runs.append(
                            {
                                "text": fragment.text,
                                "font_family": fragment.face.family,
                                "cjk_font_family": fragment.face.family,
                                "font_size": fragment.size,
                                "bold": fragment.bold,
                                "italic": fragment.italic,
                                "color": fragment.color,
                            }
                        )
                element["runs"] = runs
    return resolved


def build(
    scene_path: Path, out: Path, render: bool = True, font_dirs: tuple[Path, ...] = ()
) -> dict:
    fresh_directory(out)
    report = {
        "status": "fail",
        "visual_review": "required",
        "automated_checks": {},
        "limitations": [
            "No claim of exact font identification from pixels.",
            "Photographs and complex artwork remain independent raster assets.",
            "PowerPoint/WPS must be checked separately from LibreOffice.",
        ],
    }
    try:
        scene = load_scene(scene_path)
        root = scene_path.resolve().parent
        report["source_scene_sha256"] = hashlib.sha256(scene_path.read_bytes()).hexdigest()
        catalog = FontCatalog(scene.get("fonts"), font_dirs)
        layouts = layout_scene(scene, catalog)
        checks = preflight(scene, layouts, root)
        report["automated_checks"]["preflight"] = checks
        font_manifest = catalog.manifest()
        json_write(out / "fonts.json", font_manifest)
        report["font_substitutions"] = font_manifest["substitutions"]
        if checks["status"] == "fail":
            return report
        resolved = resolve_scene(scene, layouts, root, out)
        json_write(out / "scene.resolved.json", resolved)
        shutil.copyfile(scene_path, out / "scene.original.json")
        pptx = out / "editable.pptx"
        write_pptx(scene, layouts, root, pptx)
        svg_dir = out / "svg"
        svg_dir.mkdir()
        for slide in scene["slides"]:
            write_svg(slide, layouts, root, svg_dir / f"{slide['id']}.svg")
        native = inspect_pptx(pptx, scene)
        report["automated_checks"]["native_objects"] = native
        report["artifacts"] = {
            "pptx": "editable.pptx",
            "svg": "svg/",
            "scene": "scene.resolved.json",
            "fonts": "fonts.json",
        }
        if native["status"] == "fail":
            return report
        if render:
            render_dir = out / "render"
            pdf = make_renderer().render(pptx, render_dir)
            previews = rasterize_pdf(pdf, render_dir)
            rendered = verify_rendered_text(pdf, scene, layouts)
            report["automated_checks"]["rendered_text"] = rendered
            comparisons = []
            for slide, preview in zip(scene["slides"], previews, strict=True):
                if "source" in slide:
                    # Remove deck letterboxing before comparing source-coordinate pages.
                    tx = slide_transform(scene, slide)
                    with Image.open(preview) as im:
                        x = tx.x / tx.width_inches * im.width
                        y = tx.y / tx.height_inches * im.height
                        width = slide["width"] * tx.scale / tx.width_inches * im.width
                        height = slide["height"] * tx.scale / tx.height_inches * im.height
                        cropped = im.crop((round(x), round(y), round(x + width), round(y + height)))
                        crop_path = render_dir / f"{slide['id']}_content.png"
                        cropped.save(crop_path)
                    comparisons.append(
                        {
                            "slide": slide["id"],
                            **comparison(
                                safe_asset(root, slide["source"]),
                                crop_path,
                                render_dir / f"{slide['id']}_comparison.png",
                            ),
                        }
                    )
            report["comparisons"] = comparisons
            report["artifacts"]["render"] = "render/"
            if rendered["status"] == "fail":
                return report
            report["status"] = (
                "review"
                if checks["status"] == "review"
                or font_manifest["substitutions"]
                or rendered["status"] == "review"
                else "pass"
            )
        else:
            report["status"] = "unverified"
            report["automated_checks"]["rendered_text"] = {
                "status": "not_run",
                "reason": "--no-render was specified",
            }
        return report
    except (InputError, OSError, ValueError, RuntimeError) as exc:
        report["error"] = str(exc)
        raise
    finally:
        json_write(out / "validation.json", report)


def check(scene_path: Path, out: Path, font_dirs: tuple[Path, ...] = ()) -> dict:
    fresh_directory(out)
    report = {"status": "fail", "findings": []}
    try:
        scene = load_scene(scene_path)
        catalog = FontCatalog(scene.get("fonts"), font_dirs)
        layouts = layout_scene(scene, catalog)
        report = preflight(scene, layouts, scene_path.resolve().parent)
        json_write(out / "fonts.json", catalog.manifest())
        return report
    except (InputError, OSError, ValueError, RuntimeError) as exc:
        report["error"] = str(exc)
        raise
    finally:
        json_write(out / "validation.json", report)


def doctor() -> dict:
    return {
        "python": sys.version.split()[0],
        "packages": {
            name: importlib.metadata.version(name)
            for name in [
                "super-img2ppt",
                "python-pptx",
                "Pillow",
                "fonttools",
                "pypdfium2",
                "jsonschema",
            ]
        },
        "tools": {
            name: shutil.which(name) for name in ["soffice", "tesseract", "swift", "fc-list"]
        },
        "network_required_for_conversion": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="super-img2ppt",
        description="Reconstruct existing image pages as editable objects with measured layout checks.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Report local dependencies without installing anything")
    commands.add_parser("schema", help="Print the scene JSON Schema")
    prep = commands.add_parser(
        "prepare", help="Normalize pages and produce OCR hints for agent reconstruction"
    )
    prep.add_argument("inputs", nargs="+", type=Path)
    prep.add_argument("--out", type=Path, required=True)
    prep.add_argument("--ocr", choices=["auto", "vision", "tesseract", "none"], default="auto")
    prep.add_argument(
        "--languages",
        help="Vision: zh-Hans,en-US; Tesseract: eng+chi_sim (installed data required)",
    )
    trace = commands.add_parser(
        "trace-curve", help="Trace one isolated chart stroke into editable line fragments"
    )
    trace.add_argument("image", type=Path)
    trace.add_argument("--roi", nargs=4, type=int, required=True, metavar=("X", "Y", "W", "H"))
    trace.add_argument("--color", required=True, help="Source stroke color as #RRGGBB")
    trace.add_argument("--out", type=Path, required=True)
    trace.add_argument("--tolerance", type=float, default=80)
    trace.add_argument(
        "--exclude-band", nargs=2, type=int, action="append", default=[], metavar=("TOP", "BOTTOM")
    )
    trace.add_argument("--max-gap", type=int, default=4)
    trace.add_argument("--simplify-px", type=float, default=0.25)
    trace.add_argument("--stroke-width", type=float, default=1.5)
    trace.add_argument("--prefix", default="curve")
    trace.add_argument("--axis", choices=["x", "y"], default="x")
    for name in ["build", "check"]:
        cmd = commands.add_parser(
            name,
            help="Export and validate"
            if name == "build"
            else "Validate the scene and measured geometry",
        )
        cmd.add_argument("scene", type=Path)
        cmd.add_argument("--out", type=Path, required=True)
        cmd.add_argument("--font-dir", type=Path, action="append", default=[])
        if name == "build":
            cmd.add_argument(
                "--no-render", action="store_true", help="Produce an explicitly unverified draft"
            )
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            result = doctor()
        elif args.command == "schema":
            result = SCHEMA
        elif args.command == "prepare":
            result = prepare(args.inputs, args.out, args.ocr, args.languages)
        elif args.command == "trace-curve":
            result = trace_file(
                args.image,
                args.out,
                roi=args.roi,
                color=args.color,
                tolerance=args.tolerance,
                exclude_bands=args.exclude_band,
                max_gap=args.max_gap,
                simplify_px=args.simplify_px,
                stroke_width=args.stroke_width,
                prefix=args.prefix,
                axis=args.axis,
            )
        elif args.command == "build":
            result = build(args.scene, args.out, not args.no_render, tuple(args.font_dir))
        else:
            result = check(args.scene, args.out, tuple(args.font_dir))
        if args.command in {"build", "prepare", "check", "trace-curve"}:
            print(
                json.dumps(
                    {"status": result["status"], "output": str(args.out.resolve())},
                    ensure_ascii=False,
                )
            )
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result.get("status") == "fail" else 0
    except (InputError, OSError, ValueError, RuntimeError) as exc:
        print(
            json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
