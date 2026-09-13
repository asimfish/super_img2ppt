import json

import pytest
from PIL import Image
from super_img2ppt.appearance import automatic_plan
from super_img2ppt.cli import build, main


def inputs(tmp_path, color="#1F6F78"):
    Image.new("RGB", (400, 200), "#087887").save(tmp_path / "source.png")
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
                        "box": [0, 0, 400, 200],
                        "fill": color,
                        "z": 0,
                    }
                ],
            }
        ],
    }
    p = tmp_path / "scene.json"
    p.write_text(json.dumps(scene))
    return scene, p


def test_automatic_plan_samples_source_without_output(tmp_path):
    scene, _ = inputs(tmp_path)
    plan = automatic_plan(scene, tmp_path)
    assert 1 <= len(plan["regions"]) <= 128
    assert all(r["mode"] == "faithful" for r in plan["regions"])


@pytest.mark.render
def test_default_build_catches_palette_drift_without_flag(tmp_path):
    _, p = inputs(tmp_path)
    result = build(p, tmp_path / "bad")
    assert result["status"] == "fail"
    assert any(
        "color_drift" in r["issues"] for r in result["automated_checks"]["appearance"]["regions"]
    )


@pytest.mark.render
def test_correct_automatic_samples_still_need_visual_review(tmp_path):
    _, p = inputs(tmp_path, "#087887")
    result = build(p, tmp_path / "good")
    assert result["status"] == "review"
    evidence = json.loads((tmp_path / "good/appearance/appearance.json").read_text())
    assert evidence["status"] == "review"
    assert evidence["selection"] == "automatic_flat_grid"
    assert all(r["status"] == "pass" for r in evidence["regions"])


def test_redesign_cli_does_not_claim_faithful_verification(tmp_path):
    _, p = inputs(tmp_path)
    assert (
        main(
            [
                "build",
                str(p),
                "--out",
                str(tmp_path / "out"),
                "--no-render",
                "--appearance-mode",
                "redesign",
            ]
        )
        == 0
    )
    r = json.loads((tmp_path / "out/validation.json").read_text())
    assert r["automated_checks"]["appearance"]["mode"] == "redesign"
    assert not r["automated_checks"]["appearance"]["automatic_sampling"]
