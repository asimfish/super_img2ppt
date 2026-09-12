import json
import zipfile
from xml.etree import ElementTree as ET

import pytest
from super_img2ppt.export import write_pptx, write_svg
from super_img2ppt.qa import preflight
from super_img2ppt.scene import InputError, validate_scene


def specimen():
    return {
        "version": 1,
        "slides": [
            {
                "id": "curve",
                "width": 200,
                "height": 100,
                "elements": [
                    {
                        "id": "stroke",
                        "kind": "line",
                        "z": 1,
                        "points": [[20, 30], [90, 55]],
                        "stroke": "#0033FF",
                        "stroke_width": 8,
                        "line_cap": "round",
                    }
                ],
            }
        ],
    }


def test_round_caps_export_to_both_native_pptx_and_svg(tmp_path):
    scene = specimen()
    validate_scene(scene)
    pptx, svg = tmp_path / "line.pptx", tmp_path / "line.svg"
    write_pptx(scene, {}, tmp_path, pptx)
    write_svg(scene["slides"][0], {}, tmp_path, svg)
    ns = {
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "s": "http://www.w3.org/2000/svg",
    }
    with zipfile.ZipFile(pptx) as z:
        xml = ET.fromstring(z.read("ppt/slides/slide1.xml"))
        assert xml.find(".//a:ln", ns).get("cap") == "rnd"
    assert ET.parse(svg).find(".//s:line", ns).get("stroke-linecap") == "round"


def test_caps_participate_in_bounds_and_collision_checks(tmp_path):
    scene = specimen()
    line = scene["slides"][0]["elements"][0]
    line["points"] = [[1, 30], [90, 30]]
    assert any(f["code"] == "out_of_bounds" for f in preflight(scene, {}, tmp_path)["findings"])
    line["points"] = [[20, 30], [90, 30]]
    scene["slides"][0]["elements"].append(
        {
            "id": "neighbor",
            "kind": "shape",
            "z": 2,
            "shape": "rect",
            "box": [92, 28, 6, 4],
            "fill": "#FF0000",
        }
    )
    assert any(
        f["code"] == "unintended_overlap" for f in preflight(scene, {}, tmp_path)["findings"]
    )
    line["line_cap"] = "butt"
    assert not any(
        f["code"] == "unintended_overlap" for f in preflight(scene, {}, tmp_path)["findings"]
    )


def test_cap_cannot_silently_change_custom_arrow_outline():
    scene = specimen()
    scene["slides"][0]["elements"][0]["arrow"] = True
    with pytest.raises(InputError, match="cap"):
        validate_scene(scene)


def test_cap_schema_is_portable():
    scene = json.loads(json.dumps(specimen()))
    validate_scene(scene)
    scene["slides"][0]["elements"][0]["line_cap"] = "ignored"
    with pytest.raises(InputError):
        validate_scene(scene)
