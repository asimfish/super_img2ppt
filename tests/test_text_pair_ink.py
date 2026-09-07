import copy

import pytest
from super_img2ppt.layout import layout_scene
from super_img2ppt.qa import preflight


@pytest.mark.parametrize("rotation", [0, 90])
def test_separate_subscript_ink_is_allowed_but_duplicate_ink_is_blocked(
    scene, fonts, tmp_path, rotation
):
    page = scene["slides"][0]
    page.update(width=300, height=300)
    page["elements"] = [
        {
            "id": "base",
            "kind": "text",
            "z": 1,
            "box": [61.25, 43.5, 17.75, 33.6],
            "text": "T",
            "font_family": "Times New Roman",
            "font_size": 24,
        },
        {
            "id": "sub",
            "kind": "text",
            "z": 2,
            "box": [75, 52.5, 13, 28],
            "text": "2",
            "font_family": "Times New Roman",
            "font_size": 20,
        },
    ]
    if rotation:
        for e in page["elements"]:
            x, y, w, h = e["box"]
            cx, cy = 200 - (y + h / 2), x + w / 2
            e["box"] = [cx - w / 2, cy - h / 2, w, h]
            e["rotation"] = rotation
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert not any(f["code"] == "unintended_overlap" for f in result["findings"]), result
    duplicate = copy.deepcopy(page["elements"][0])
    duplicate.update(id="sub", z=2)
    page["elements"][1] = duplicate
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert any(f["code"] == "unintended_overlap" for f in result["findings"])
