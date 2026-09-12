import copy
import shutil

import pypdfium2 as pdfium
import pytest
from super_img2ppt.export import write_pptx
from super_img2ppt.layout import layout_scene
from super_img2ppt.render import make_renderer, verify_rendered_text


@pytest.mark.render
@pytest.mark.skipif(shutil.which("soffice") is None, reason="LibreOffice not installed")
@pytest.mark.parametrize("label", ["User-\nPurchase", "Cross-\nAttention"])
def test_actual_pdf_hyphen_marker_preserves_visible_dash(
    scene, fonts, tmp_path, monkeypatch, label
):
    slide = scene["slides"][0]
    slide.update(width=300, height=180)
    slide["elements"] = [
        {
            "id": "label",
            "kind": "text",
            "z": 1,
            "box": [30, 30, 140, 85],
            "text": label,
            "font_family": "Times New Roman",
            "font_size": 24,
        }
    ]
    layouts = layout_scene(scene, fonts)
    pptx = tmp_path / "hyphen.pptx"
    write_pptx(scene, layouts, tmp_path, pptx)
    pdf = make_renderer().render(pptx, tmp_path / "render")
    with pdfium.PdfDocument(pdf) as doc:
        page = doc[0]
        textpage = page.get_textpage()
        assert any(
            pdfium.raw.FPDFText_GetUnicode(textpage, i) == 2
            and pdfium.raw.FPDFText_IsHyphen(textpage, i) == 1
            for i in range(textpage.count_chars())
        )
        textpage.close()
        page.close()
    report = verify_rendered_text(pdf, scene, layouts)
    assert all(b["matches"] for b in report["text_boxes"]), report
    assert report["text_boxes"][0]["rendered"] != report["text_boxes"][0]["rendered_normalized"]

    # Restoring a renderer marker must not invent other characters or remove a visible dash.
    wrong = copy.deepcopy(scene)
    wrong["slides"][0]["elements"][0]["text"] = label.replace("-", "")
    assert any(
        f["code"] == "rendered_text_mismatch" for f in verify_rendered_text(pdf, wrong)["findings"]
    )
    wrong["slides"][0]["elements"][0]["text"] = label.replace("-", "X-")
    assert any(
        f["code"] == "rendered_text_mismatch" for f in verify_rendered_text(pdf, wrong)["findings"]
    )

    # An unconfirmed control character must remain a mismatch, even if the expected text has '-'.
    monkeypatch.setattr(pdfium.raw, "FPDFText_IsHyphen", lambda *args: 0)
    assert any(
        f["code"] == "rendered_text_mismatch" for f in verify_rendered_text(pdf, scene)["findings"]
    )
    monkeypatch.delattr(pdfium.raw, "FPDFText_IsHyphen")
    assert any(
        f["code"] == "rendered_text_mismatch" for f in verify_rendered_text(pdf, scene)["findings"]
    )
