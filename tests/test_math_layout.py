import pytest
from super_img2ppt.math_layout import fit_box
from super_img2ppt.scene import InputError


def test_fit_preserves_center_and_natural_aspect():
    result = fit_box([10, 20, 200, 40], 3, 32, 16)
    assert result == [80, 30, 60, 20]
    assert result[2] / result[3] == 3


@pytest.mark.parametrize("ratio,measured,target", [(0, 12, 12), (2, 0, 12), (2, 12, float("nan"))])
def test_invalid_measurements_rejected(ratio, measured, target):
    with pytest.raises(InputError):
        fit_box([0, 0, 100, 40], ratio, measured, target)


def test_non_target_chart_is_not_read_as_equation(tmp_path):
    from zipfile import ZipFile

    from super_img2ppt.math_layout import intrinsic_ratios

    odp = tmp_path / "objects.odp"
    xml = """<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:xlink="http://www.w3.org/1999/xlink"><draw:page><draw:frame draw:name="chart"><draw:object xlink:href="./Object 1"/></draw:frame></draw:page></office:document-content>"""
    with ZipFile(odp, "w") as z:
        z.writestr("content.xml", xml)
    assert intrinsic_ratios(odp, {(1, "formula"): 12}) == {}
    with pytest.raises(InputError, match="metrics"):
        intrinsic_ratios(odp, {(1, "chart"): 12})
