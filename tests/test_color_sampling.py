import json

import pytest
from PIL import Image, ImageDraw
from super_img2ppt.appearance import sample_color_file
from super_img2ppt.cli import main
from super_img2ppt.scene import InputError


def test_source_palette_is_measured_before_scene_authoring(tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (20, 20), "#CC94F1").save(source)
    result = sample_color_file(source, tmp_path / "sample", roi=[5, 5, 5, 5])
    assert result["measurement"]["hex"] == "#CC94F1"
    assert len(result["source_sha256"]) == 64
    assert result["status"] == "review"
    assert json.loads((tmp_path / "sample/color.json").read_text()) == result


def test_mixed_patch_does_not_fabricate_a_flat_palette_color(tmp_path):
    source = tmp_path / "mixed.png"
    image = Image.new("RGB", (20, 20), "blue")
    ImageDraw.Draw(image).rectangle((10, 0, 19, 19), fill="red")
    image.save(source)
    result = sample_color_file(source, tmp_path / "sample", roi=[0, 0, 20, 20])
    assert result["status"] == "fail"
    assert result["measurement"]["issue"] == "mixed_or_gradient_region"
    assert "hex" not in result["measurement"]
    with pytest.raises(InputError, match="nonnegative"):
        sample_color_file(source, tmp_path / "invalid", roi=[-1, 0, 5, 5])


def test_sample_color_cli_uses_the_same_measurement_contract(tmp_path, capsys):
    source = tmp_path / "source.png"
    Image.new("RGB", (20, 20), "#157AC3").save(source)
    assert (
        main(
            [
                "sample-color",
                str(source),
                "--roi",
                "5",
                "5",
                "5",
                "5",
                "--out",
                str(tmp_path / "sample"),
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["status"] == "review"
