import json

import pytest
from PIL import Image, ImageDraw
from super_img2ppt.appearance import compare_region, load_plan, validate_plan
from super_img2ppt.cli import build
from super_img2ppt.scene import InputError


def region(**fields):
    return {
        "id": "line",
        "slide": "page_001",
        "roi": [0, 0, 100, 40],
        "mode": "faithful",
        "kind": "ink",
        **fields,
    }


def stroke(color="#087887", width=4):
    im = Image.new("RGB", (100, 40), "white")
    ImageDraw.Draw(im).rectangle([10, 16, 89, 15 + width], fill=color)
    return im


def test_wrong_palette_fails_even_when_geometry_matches():
    result = compare_region(stroke(), stroke("#1F6F78"), region())
    assert result["status"] == "fail"
    assert "color_drift" in result["issues"]
    assert result["max_channel_delta"] == 23
    assert result["ink_coverage_ratio"] == pytest.approx(1)


def test_thinner_line_fails_even_when_color_matches():
    result = compare_region(stroke(), stroke(width=2), region())
    assert result["max_channel_delta"] == 0
    assert result["ink_coverage_ratio"] == pytest.approx(0.5)
    assert result["issues"] == ["ink_density_drift"]


def test_matching_ink_and_solid_pass():
    assert compare_region(stroke(), stroke(), region())["status"] == "pass"
    im = Image.new("RGB", (100, 40), "#E1EFF1")
    assert compare_region(im, im, region(kind="solid"))["status"] == "pass"


def test_white_actual_does_not_hide_missing_color():
    result = compare_region(stroke(), Image.new("RGB", (100, 40), "white"), region())
    assert result["status"] == "fail"
    assert result["actual"]["issue"] == "insufficient_foreground"


def test_mixed_solid_roi_is_invalid():
    im = Image.new("RGB", (100, 40), "red")
    ImageDraw.Draw(im).rectangle([50, 0, 99, 39], fill="blue")
    assert compare_region(im, im, region(kind="solid"))["status"] == "fail"


def test_target_palette_preserves_original_measurement():
    r = region(mode="target", target_color="#1F6F78", reason="User requested darker teal")
    result = compare_region(stroke(), stroke("#1F6F78"), r)
    assert result["status"] == "pass"
    assert result["source"]["hex"] == "#087887"
    assert result["expected_rgb"] == [31, 111, 120]
    assert compare_region(stroke(), stroke("#FF0000"), r)["status"] == "fail"


def test_antialias_edges_do_not_replace_core_color():
    im = stroke()
    ImageDraw.Draw(im).line([10, 15, 89, 15], fill="#B5D6DA")
    result = compare_region(stroke(), im, region())
    assert result["status"] == "pass"
    assert result["max_channel_delta"] == 0


@pytest.mark.parametrize(
    "edit",
    [
        {"mode": "faithful", "target_color": "#000000"},
        {"mode": "target", "target_color": "#000000"},
        {"roi": [99, 0, 5, 5]},
        {"roi": [0, 0, 0, 4]},
        {"slide": "missing"},
        {"density_ratio": [float("nan"), 2]},
        {"density_ratio": [2, 3]},
        {"unexpected": True},
    ],
)
def test_invalid_contracts_fail(scene, edit):
    scene["slides"][0]["source"] = "source.png"
    scene["slides"][0]["width"] = 100
    scene["slides"][0]["height"] = 40
    with pytest.raises(InputError):
        validate_plan({"version": 1, "regions": [region(**edit)]}, scene)


def test_duplicate_keys_and_targets_fail(scene, tmp_path):
    p = tmp_path / "plan.json"
    p.write_text('{"version":1,"version":1,"regions":[]}')
    with pytest.raises(InputError):
        load_plan(p, scene)
    scene["slides"][0]["source"] = "source.png"
    with pytest.raises(InputError):
        validate_plan({"version": 1, "regions": [region(), region()]}, scene)


@pytest.mark.render
@pytest.mark.parametrize("color,expected", [("#087887", "pass"), ("#1F6F78", "fail")])
def test_real_pptx_color_gate(tmp_path, color, expected):
    im = Image.new("RGB", (400, 200), "white")
    ImageDraw.Draw(im).rectangle([40, 40, 159, 119], fill="#087887")
    im.save(tmp_path / "source.png")
    scene = {
        "version": 1,
        "slides": [
            {
                "id": "page_001",
                "width": 400,
                "height": 200,
                "source": "source.png",
                "reviewed": True,
                "elements": [
                    {
                        "id": "panel",
                        "kind": "shape",
                        "shape": "rect",
                        "box": [40, 40, 120, 80],
                        "fill": color,
                        "z": 0,
                    }
                ],
            }
        ],
    }
    source = tmp_path / "scene.json"
    source.write_text(json.dumps(scene))
    plan = tmp_path / "appearance.json"
    plan.write_text(
        json.dumps({"version": 1, "regions": [region(kind="solid", roi=[60, 60, 30, 30])]})
    )
    result = build(source, tmp_path / "build", appearance_plan=plan)
    assert result["automated_checks"]["native_objects"]["status"] == "pass"
    assert result["automated_checks"]["appearance"]["status"] == expected
    assert result["status"] == expected
    assert (tmp_path / "build/appearance/line_actual.png").exists()
    assert json.loads((tmp_path / "build/validation.json").read_text())["status"] == expected
    assert json.loads(source.read_text()) == scene


def test_no_render_cannot_pass_appearance(scene, tmp_path):
    scene["slides"][0]["source"] = "source.png"
    Image.new("RGB", (1280, 720), "white").save(tmp_path / "source.png")
    scene["slides"][0]["elements"] = [
        {
            "id": "box",
            "kind": "shape",
            "shape": "rect",
            "box": [10, 10, 30, 30],
            "fill": "#FFFFFF",
            "z": 0,
        }
    ]
    p = tmp_path / "scene.json"
    p.write_text(json.dumps(scene))
    spec = tmp_path / "plan.json"
    spec.write_text(json.dumps({"version": 1, "regions": [region(kind="solid")]}))
    result = build(p, tmp_path / "build", render=False, appearance_plan=spec)
    assert result["status"] == "unverified"
    assert result["automated_checks"]["appearance"]["status"] == "not_run"


def test_mixed_ink_hues_cannot_hide_recoloring():
    im = stroke("#000000")
    ImageDraw.Draw(im).rectangle([50, 16, 89, 19], fill="#FF0000")
    assert compare_region(im, im, region())["source"]["issue"] == "mixed_ink_hues"


@pytest.mark.render
def test_missing_plan_is_review_not_color_pass(tmp_path):
    Image.new("RGB", (100, 100), "white").save(tmp_path / "source.png")
    scene = {
        "version": 1,
        "slides": [
            {
                "id": "page_001",
                "source": "source.png",
                "width": 100,
                "height": 100,
                "reviewed": True,
                "elements": [
                    {
                        "id": "rect",
                        "kind": "shape",
                        "shape": "rect",
                        "box": [20, 20, 40, 40],
                        "fill": "#FFFFFF",
                        "z": 0,
                    }
                ],
            }
        ],
    }
    p = tmp_path / "scene.json"
    p.write_text(json.dumps(scene))
    result = build(p, tmp_path / "out")
    assert result["status"] == "review"
    assert result["automated_checks"]["appearance"]["status"] == "not_run"


def test_smaller_actual_roi_cannot_hide_thinner_line(scene):
    r = region(actual_roi=[0, 0, 100, 20])
    with pytest.raises(InputError, match="equal"):
        compare_region(stroke(), stroke(width=2), r)
    scene["slides"][0]["source"] = "source.png"
    with pytest.raises(InputError, match="equal"):
        validate_plan({"version": 1, "regions": [r]}, scene)
