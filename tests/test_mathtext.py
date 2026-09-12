import copy
import json
import shutil
import xml.etree.ElementTree as ET
import zipfile

import pypdfium2 as pdfium
import pytest
from super_img2ppt.export import write_pptx, write_svg
from super_img2ppt.layout import layout_scene, positioned_lines
from super_img2ppt.mathtext import compose_file, compose_math
from super_img2ppt.render import make_renderer, verify_rendered_text
from super_img2ppt.scene import InputError


def formula(fonts):
    family = fonts.resolve("x", None, None, False, False).family
    return {
        "id": "formula",
        "origin": [40, 85],
        "font_family": family,
        "font_size": 24,
        "parts": [
            {"text": "x", "offset": [0, 0], "bold": True, "italic": True},
            {"text": "i", "offset": [17, -14], "size_scale": 0.6, "italic": True},
            {"text": "k", "offset": [17, 8], "size_scale": 0.6, "italic": True},
            {"text": "+", "offset": [38, 0]},
            {"text": "y", "offset": [65, 0], "italic": True},
        ],
    }


def test_baselines_and_native_styles_are_preserved(fonts, scene, tmp_path):
    spec = formula(fonts)
    result = compose_math(spec, fonts)
    slide = scene["slides"][0]
    slide.update(width=240, height=160, elements=result["elements"])
    layouts = layout_scene(scene, fonts)
    for e, part in zip(slide["elements"], spec["parts"], strict=True):
        layout = layouts[slide["id"], e["id"]]
        assert layout.fits
        x, y, line = next(positioned_lines(e, layout))
        assert x == pytest.approx(40 + part["offset"][0])
        assert y + line.ascent == pytest.approx(85 + part["offset"][1])
    pptx = tmp_path / "formula.pptx"
    write_pptx(scene, layouts, tmp_path, pptx)
    write_svg(slide, layouts, tmp_path, tmp_path / "formula.svg")
    with zipfile.ZipFile(pptx) as z:
        xml = ET.fromstring(z.read("ppt/slides/slide1.xml"))
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    runs = xml.findall(".//a:r", ns)
    assert [r.find("a:t", ns).text for r in runs] == ["x", "i", "k", "+", "y"]
    assert runs[0].find("a:rPr", ns).get("b") == "1"
    assert runs[3].find("a:rPr", ns).get("b") == "0"
    assert runs[3].find("a:rPr", ns).get("i") == "0"
    assert runs[4].find("a:rPr", ns).get("b") == "0"


@pytest.mark.render
@pytest.mark.skipif(shutil.which("soffice") is None, reason="LibreOffice not installed")
def test_actual_pdf_scripts_keep_their_vertical_order(fonts, scene, tmp_path):
    spec = formula(fonts)
    scene["slides"][0].update(width=240, height=160, elements=compose_math(spec, fonts)["elements"])
    layouts = layout_scene(scene, fonts)
    pptx = tmp_path / "formula.pptx"
    write_pptx(scene, layouts, tmp_path, pptx)
    pdf = make_renderer().render(pptx, tmp_path / "render")
    report = verify_rendered_text(pdf, scene, layouts)
    assert report["status"] in {"pass", "review"}, report
    with pdfium.PdfDocument(pdf) as document:
        page = document[0]
        textpage = page.get_textpage()
        centers = {}
        for i in range(textpage.count_chars()):
            char = chr(pdfium.raw.FPDFText_GetUnicode(textpage, i))
            if char in {"x", "i", "k"}:
                left, bottom, right, top = textpage.get_charbox(i)
                centers[char] = (bottom + top) / 2
        assert centers["i"] > centers["x"] > centers["k"]
        textpage.close()
        page.close()


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s.update(extra="unsupported"),
        lambda s: s.update(font_family="A definitely unavailable formula font"),
        lambda s: s["parts"][1].update(text="ⁱ"),
        lambda s: s["parts"][0].update(offset=[float("nan"), 0]),
        lambda s: s["parts"][0].update(text="x\ny"),
        lambda s: s["parts"][0].update(bold="true"),
        lambda s: s.update(parts=s["parts"] * 26),
    ],
)
def test_formula_rejects_ambiguous_styles_and_unbounded_inputs(fonts, mutation):
    spec = copy.deepcopy(formula(fonts))
    mutation(spec)
    with pytest.raises(InputError):
        compose_math(spec, fonts)


def test_failed_file_has_fresh_failure_evidence(tmp_path):
    source = tmp_path / "large.json"
    source.write_text(" " * 65537)
    out = tmp_path / "output"
    with pytest.raises(InputError, match="64 KiB"):
        compose_file(source, out)
    assert json.loads((out / "math.json").read_text())["status"] == "fail"
    assert not (out / "elements.json").exists()
    with pytest.raises(InputError):
        compose_file(source, out)


def test_duplicate_formula_fields_are_rejected_before_composition(tmp_path):
    source = tmp_path / "duplicate.json"
    source.write_text('{"font_family": "A", "font_family": "B"}')
    out = tmp_path / "out"
    with pytest.raises(InputError):
        compose_file(source, out)
    assert json.loads((out / "math.json").read_text())["status"] == "fail"
    assert not (out / "elements.json").exists()
