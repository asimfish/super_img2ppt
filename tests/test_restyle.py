import copy
import json

import pytest
from super_img2ppt.cli import main
from super_img2ppt.restyle import apply_plan, stage_variants
from super_img2ppt.scene import InputError


def plan(fields):
    return {
        "version": 1,
        "changes": [
            {
                "slide": "page_001",
                "element": "title",
                "set": fields,
                "reason": "Consistent label styling",
            }
        ],
    }


def test_style_copy_and_audit(scene):
    original = copy.deepcopy(scene)
    refined, audit = apply_plan(scene, plan({"color": "#123456"}))
    assert scene == original
    assert refined["slides"][0]["elements"][0]["text"] == "Hello 中文 123"
    assert refined["slides"][0]["elements"][0]["box"] == original["slides"][0]["elements"][0]["box"]
    assert not refined["slides"][0]["reviewed"]
    assert audit[0]["edits"][0]["after"] == "#123456"


@pytest.mark.parametrize(
    "fields",
    [
        {"text": "fake"},
        {"box": [1, 2, 3, 4]},
        {"allow_overlap_with": []},
        {"z": 9},
        {"color": "invalid"},
        {"font_size": -1},
    ],
)
def test_reject_content_geometry_and_invalid_style(scene, fields):
    with pytest.raises(InputError):
        apply_plan(scene, plan(fields))


def test_formula_protected(scene):
    element = scene["slides"][0]["elements"][0]
    element["runs"] = [{"text": element.pop("text"), "italic": True}]
    with pytest.raises(InputError, match="protected"):
        apply_plan(scene, plan({"bold": True}))


def test_duplicate_and_noop(scene):
    p = plan({"font_size": 36})
    with pytest.raises(InputError, match="no effective"):
        apply_plan(scene, p)
    p["changes"] *= 2
    with pytest.raises(InputError, match="repeated"):
        apply_plan(scene, p)


def test_stage_fresh(scene, tmp_path):
    out = tmp_path / "variants"
    stage_variants(scene, tmp_path, plan({"color": "#123456"}), out)
    assert json.loads((out / "baseline.json").read_text()) == scene
    with pytest.raises((InputError, FileExistsError)):
        stage_variants(scene, tmp_path, plan({"color": "#123456"}), out)


def test_cli_exports_both_drafts(scene, tmp_path):
    scene["slides"][0]["elements"][0]["text"] = "Hello 123"
    source, spec, out = tmp_path / "scene.json", tmp_path / "plan.json", tmp_path / "out"
    source.write_text(json.dumps(scene))
    spec.write_text(json.dumps(plan({"color": "#123456"})))
    assert (
        main(["restyle", str(source), "--plan", str(spec), "--out", str(out), "--no-render"]) == 0
    )
    report = json.loads((out / "restyle.json").read_text())
    assert report["status"] == "unverified"
    for variant in ("baseline", "refined"):
        assert (out / variant / "editable.pptx").is_file()


def test_gradient_flatten_preserves_group_and_curve(scene):
    slide = scene["slides"][0]
    slide["elements"].extend(
        [
            {
                "id": "box",
                "kind": "shape",
                "shape": "rect",
                "box": [80, 200, 300, 100],
                "z": 3,
                "gradient": {
                    "direction": "horizontal",
                    "stops": [{"offset": 0, "color": "#FFFFFF"}, {"offset": 1, "color": "#000000"}],
                },
            },
            {
                "id": "curve",
                "kind": "line",
                "points": [[400, 300], [450, 250]],
                "stroke": "#123456",
                "z": 4,
            },
        ]
    )
    slide["groups"] = [{"id": "module", "members": ["box", "curve"]}]
    p = plan({"gradient": None, "fill": "#EEF3F8"})
    p["changes"][0]["element"] = "box"
    result, _ = apply_plan(scene, p)
    actual = result["slides"][0]
    assert actual["groups"] == slide["groups"]
    assert actual["elements"][-1] == slide["elements"][-1]
    assert "gradient" not in actual["elements"][-2]
    assert "gradient" in slide["elements"][-2]


def test_missing_asset_does_not_create_output(scene, tmp_path):
    scene["slides"][0]["source"] = "../outside.png"
    out = tmp_path / "out"
    with pytest.raises(InputError):
        stage_variants(scene, tmp_path, plan({"color": "#123456"}), out)
    assert not out.exists()


def test_failed_variant_is_not_success(scene, tmp_path, monkeypatch):
    import super_img2ppt.cli as cli

    source, spec, out = tmp_path / "scene.json", tmp_path / "plan.json", tmp_path / "out"
    source.write_text(json.dumps(scene))
    spec.write_text(json.dumps(plan({"color": "#123456"})))
    monkeypatch.setattr(cli, "build", lambda *args: {"status": "fail"})
    assert main(["restyle", str(source), "--plan", str(spec), "--out", str(out)]) == 2
    assert json.loads((out / "restyle.json").read_text())["status"] == "fail"


def test_duplicate_plan_keys_rejected(scene, tmp_path):
    source, spec, out = tmp_path / "scene.json", tmp_path / "plan.json", tmp_path / "out"
    source.write_text(json.dumps(scene))
    spec.write_text('{"version": 1, "version": 1, "changes": []}')
    assert main(["restyle", str(source), "--plan", str(spec), "--out", str(out)]) == 2
    assert not out.exists()
