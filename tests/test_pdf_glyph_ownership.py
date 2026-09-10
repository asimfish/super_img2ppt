import copy
import shutil

import pypdfium2 as pdfium
import pytest
from super_img2ppt.export import write_pptx
from super_img2ppt.layout import layout_scene
from super_img2ppt.render import make_renderer, verify_rendered_text


def adjacent_labels(scene):
    page = scene["slides"][0]
    page.update(width=300, height=200)
    page["elements"] = [
        {
            "id": "flow",
            "kind": "text",
            "z": 1,
            "box": [51, 30.75, 120, 25],
            "text": "Flow matching",
            "font_family": "Arial",
            "font_size": 16,
        },
        {
            "id": "action",
            "kind": "text",
            "z": 2,
            "box": [146, 40, 79, 40],
            "text": "Action\ntrajectories",
            "font_family": "Arial",
            "font_size": 14,
            "align": "center",
        },
    ]
    return scene


@pytest.mark.render
@pytest.mark.skipif(shutil.which("soffice") is None, reason="LibreOffice not installed")
@pytest.mark.parametrize("rotation", [0, 90])
def test_neighbor_pdf_text_object_does_not_pollute_ink_checks(
    scene, fonts, tmp_path, rotation, monkeypatch
):
    spec = adjacent_labels(scene)
    if rotation:
        spec["slides"][0].update(width=300, height=300)
        for element in spec["slides"][0]["elements"]:
            x, y, w, h = element["box"]
            cx, cy = 200 - y - h / 2, x + w / 2
            element["box"] = [cx - w / 2, cy - h / 2, w, h]
            element["rotation"] = rotation
    layouts = layout_scene(spec, fonts)
    pptx = tmp_path / "adjacent.pptx"
    write_pptx(spec, layouts, tmp_path, pptx)
    pdf = make_renderer().render(pptx, tmp_path / "render")
    report = verify_rendered_text(pdf, spec, layouts)
    assert not [f for f in report["findings"] if f["element"] == "flow"], report
    assert all(b["matches"] for b in report["text_boxes"])

    # The same actual PDF must still reveal missing content and real ink overflow.
    missing = copy.deepcopy(spec)
    missing["slides"][0]["elements"][0]["text"] = "Absent label"
    result = verify_rendered_text(pdf, missing, layout_scene(missing, fonts))
    assert any(f["code"] == "rendered_text_mismatch" for f in result["findings"])
    if not rotation:
        narrow = copy.deepcopy(spec)
        narrow["slides"][0]["elements"][1]["box"][2] = 29
        result = verify_rendered_text(pdf, narrow, layout_scene(narrow, fonts))
        assert any(
            f["code"] == "rendered_glyph_overflow" and f["element"] == "action"
            for f in result["findings"]
        ), result

        # Duplicate plausible owners must preserve conservative bounds, not hide ink.
        ambiguous = copy.deepcopy(spec)
        duplicate = copy.deepcopy(ambiguous["slides"][0]["elements"][1])
        duplicate["id"] = "duplicate_action"
        ambiguous["slides"][0]["elements"].append(duplicate)
        result = verify_rendered_text(pdf, ambiguous, layout_scene(ambiguous, fonts))
        assert any(
            f["code"] == "rendered_glyph_overflow" and f["element"] == "flow"
            for f in result["findings"]
        ), result

        with monkeypatch.context() as patch:
            patch.delattr(pdfium.raw, "FPDFText_GetTextObject")
            result = verify_rendered_text(pdf, spec, layouts)
        assert any(
            f["code"] == "rendered_glyph_overflow" and f["element"] == "flow"
            for f in result["findings"]
        ), result
