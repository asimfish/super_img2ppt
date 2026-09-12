import json
import math

import pytest
from PIL import Image, ImageDraw
from super_img2ppt.cli import main
from super_img2ppt.curves import trace_curve
from super_img2ppt.scene import InputError, validate_scene


def chart():
    image = Image.new("RGB", (300, 180), "white")
    draw = ImageDraw.Draw(image)
    points = [(x, 92 + 42 * math.sin(x / 24) + 8 * math.sin(x / 9)) for x in range(10, 290)]
    draw.line(points, fill="#FF0000", width=2)
    for x in range(10, 290, 8):
        draw.line([(x, 70), (x + 4, 70)], fill="#FF0000", width=2)
    return image, points


def test_trace_excludes_same_color_guide_without_fitting_a_sine():
    image, expected = chart()
    result = trace_curve(image, [10, 35, 280, 115], "#FF0000", exclude_bands=[(69, 72)])
    known = dict(expected)
    errors = [abs(y - known[int(x)]) for x, y in result["centers"]]
    assert sum(errors) / len(errors) < 1.1
    assert max(errors) < 2.6
    assert result["excluded_bands"] == [[69, 72]]
    assert result["interpolated_columns"]
    assert len(result["vertices"]) < len(result["centers"])
    assert all(e["kind"] == "line" for e in result["elements"])
    validate_scene(
        {
            "version": 1,
            "slides": [{"id": "plot", "width": 300, "height": 180, "elements": result["elements"]}],
        }
    )


def test_flat_curve_is_preserved_not_automatically_deleted_as_grid():
    image = Image.new("RGB", (220, 90), "white")
    ImageDraw.Draw(image).line([(10, 40), (210, 40)], fill="blue", width=2)
    result = trace_curve(image, [10, 30, 201, 25], "#0000FF")
    assert len(result["vertices"]) == 2
    assert result["coverage"] == 1
    assert result["excluded_bands"] == []


def test_same_color_branches_are_rejected_instead_of_averaged():
    image = Image.new("RGB", (160, 120), "white")
    draw = ImageDraw.Draw(image)
    draw.line([(10, 30), (150, 80)], fill="blue", width=2)
    draw.line([(10, 90), (150, 40)], fill="blue", width=2)
    with pytest.raises(InputError, match="ambiguous"):
        trace_curve(image, [10, 20, 141, 80], "#0000FF")


def test_long_missing_interval_is_not_invented():
    image = Image.new("RGB", (160, 90), "white")
    draw = ImageDraw.Draw(image)
    draw.line([(10, 40), (50, 40)], fill="blue", width=2)
    draw.line([(70, 40), (150, 40)], fill="blue", width=2)
    with pytest.raises(InputError, match="gap"):
        trace_curve(image, [10, 30, 141, 25], "#0000FF")


@pytest.mark.parametrize(
    "roi", [[-1, 0, 20, 20], [0, 0, 1000, 10], [0, 0, 0, 10], [0.5, 0, 10, 10]]
)
def test_trace_rejects_invalid_roi(roi):
    with pytest.raises(InputError, match="ROI"):
        trace_curve(Image.new("RGB", (100, 100)), roi, "#FF0000")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"tolerance": float("nan")},
        {"simplify_px": float("inf")},
        {"stroke_width": -1},
        {"max_gap": 1000000},
        {"exclude_bands": [(1, 80)]},
    ],
)
def test_trace_bounds_parameters(kwargs):
    with pytest.raises(InputError):
        trace_curve(Image.new("RGB", (100, 100)), [0, 0, 100, 100], "#FF0000", **kwargs)


def test_cli_fails_with_diagnostic_and_preserves_existing_output(tmp_path):
    image = tmp_path / "blank.png"
    Image.new("RGB", (80, 80), "white").save(image)
    out = tmp_path / "failed"
    cmd = [
        "trace-curve",
        str(image),
        "--roi",
        "5",
        "5",
        "50",
        "50",
        "--color",
        "#0000FF",
        "--out",
        str(out),
    ]
    assert main(cmd) == 2
    assert json.loads((out / "trace.json").read_text())["status"] == "fail"
    marker = out / "mine.txt"
    marker.write_text("preserve")
    assert main(cmd) == 2
    assert marker.read_text() == "preserve"
    assert not (out / "elements.json").exists()


def test_cli_success_exports_fragment_and_source_overlay(tmp_path):
    image, _ = chart()
    src = tmp_path / "source.png"
    image.save(src)
    out = tmp_path / "traced"
    assert (
        main(
            [
                "trace-curve",
                str(src),
                "--roi",
                "10",
                "35",
                "280",
                "115",
                "--color",
                "#FF0000",
                "--exclude-band",
                "69",
                "72",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    report = json.loads((out / "trace.json").read_text())
    assert report["status"] == "review"
    assert report["source_sha256"]
    assert (out / "overlay.png").is_file()
    elements = json.loads((out / "elements.json").read_text())
    groups = json.loads((out / "groups.json").read_text())
    assert groups[0]["members"] == [e["id"] for e in elements]
    validate_scene(
        {
            "version": 1,
            "slides": [
                {"id": "plot", "width": 300, "height": 180, "elements": elements, "groups": groups}
            ],
        }
    )
    assert not (out / "editable.pptx").exists()


def test_steep_stroke_can_be_traced_by_rows_without_changing_coordinates():
    image = Image.new("RGB", (120, 160), "white")
    ImageDraw.Draw(image).line([(35, 10), (40, 149)], fill="blue", width=2)
    with pytest.raises(InputError, match="steep"):
        trace_curve(image, [30, 10, 18, 140], "#0000FF")
    result = trace_curve(image, [30, 10, 18, 140], "#0000FF", axis="y")
    assert result["axis"] == "y"
    assert result["roi"] == [30, 10, 18, 140]
    assert all(34 <= x <= 42 and 10 <= y <= 150 for x, y in result["vertices"])
    assert max(y for x, y in result["vertices"]) > 148
