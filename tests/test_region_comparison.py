import json

import pytest
from PIL import Image, ImageDraw
from super_img2ppt.regions import compare_region, compare_region_files
from super_img2ppt.scene import InputError


def fixture_image():
    image = Image.new("RGB", (48, 32), "white")
    ImageDraw.Draw(image).rectangle((10, 8, 19, 17), fill="black")
    return image


def test_known_translation_preserves_coordinates_and_exposes_iou():
    source = fixture_image()
    actual = Image.new("RGB", source.size, "white")
    ImageDraw.Draw(actual).rectangle((13, 10, 22, 19), fill="black")
    report = compare_region(source, actual, [4, 4, 30, 24], "#000000", tolerance=0)
    assert report["source_ink_box"] == [10, 8, 20, 18]
    assert report["actual_ink_box"] == [13, 10, 23, 20]
    assert report["edge_delta_px"] == [3, 2, 3, 2]
    assert report["mask_iou"] == pytest.approx(56 / 144)
    assert report["edge_metrics_valid"] is True
    assert report["status"] == "review"


def test_equal_extrema_do_not_hide_missing_interior_ink():
    source = fixture_image()
    actual = source.copy()
    ImageDraw.Draw(actual).rectangle((12, 10, 17, 15), fill="white")
    report = compare_region(source, actual, [4, 4, 30, 24], "#000000", tolerance=0)
    assert report["edge_delta_px"] == [0, 0, 0, 0]
    assert report["mask_iou"] == pytest.approx(0.64)
    assert report["status"] != "pass"


def test_clipped_ink_invalidates_complete_bounds_even_when_images_match():
    source = fixture_image()
    report = compare_region(source, source, [10, 4, 20, 24], "#000000", tolerance=0)
    assert report["mask_iou"] == 1
    assert report["source_touches_roi"] == ["left"]
    assert report["actual_touches_roi"] == ["left"]
    assert report["edge_metrics_valid"] is False
    assert report["edge_delta_px"] is None
    assert "ink_touches_roi_boundary" in report["issues"]


def test_blank_source_is_not_a_perfect_comparison():
    blank = Image.new("RGB", (48, 32), "white")
    report = compare_region(blank, blank, [4, 4, 30, 24], "#000000", tolerance=0)
    assert report["mask_iou"] is None
    assert report["edge_delta_px"] is None
    assert report["edge_metrics_valid"] is False
    assert "empty_source_mask" in report["issues"]
    missing = compare_region(fixture_image(), blank, [4, 4, 30, 24], "#000000", tolerance=0)
    assert missing["mask_iou"] == 0
    assert "empty_actual_mask" in missing["issues"]


def test_white_text_requires_explicit_white_mask():
    source = Image.new("RGB", (48, 32), "#2040B0")
    ImageDraw.Draw(source).rectangle((10, 8, 19, 17), fill="white")
    report = compare_region(source, source, [4, 4, 30, 24], "#FFFFFF", tolerance=0)
    assert report["source_pixels"] == 100
    assert report["edge_metrics_valid"] is True
    assert report["mask_iou"] == 1


@pytest.mark.parametrize(
    "options",
    [
        {"roi": [-1, 0, 10, 10]},
        {"roi": [0, 0, 49, 10]},
        {"roi": [0, 0, True, 10]},
        {"roi": [0, 0, 0, 10]},
        {"color": "black"},
        {"tolerance": float("nan")},
        {"tolerance": 256},
    ],
)
def test_invalid_inputs_fail_without_comparing(options):
    args = {"roi": [4, 4, 30, 24], "color": "#000000", "tolerance": 0, **options}
    with pytest.raises(InputError):
        compare_region(fixture_image(), fixture_image(), **args)


def test_different_canvas_sizes_fail_with_fresh_evidence(tmp_path):
    source, actual = tmp_path / "source.png", tmp_path / "actual.png"
    fixture_image().save(source)
    Image.new("RGB", (49, 32), "white").save(actual)
    out = tmp_path / "check"
    report = compare_region_files(source, actual, out, roi=[4, 4, 30, 24], color="#000000")
    assert report["status"] == "fail"
    assert report["source_size"] == [48, 32]
    assert report["actual_size"] == [49, 32]
    assert json.loads((out / "region.json").read_text())["status"] == "fail"
    assert not (out / "comparison.png").exists()
    with pytest.raises(InputError):
        compare_region_files(source, actual, out, roi=[4, 4, 30, 24], color="#000000")
