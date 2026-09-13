import pytest
from PIL import Image
from super_img2ppt.appearance import compare_region, validate_plan
from super_img2ppt.color_difference import color_difference, oklab
from super_img2ppt.scene import InputError


@pytest.mark.parametrize(
    "rgb,expected",
    [
        ((0, 0, 0), (0, 0, 0)),
        ((255, 255, 255), (1, 0, 0)),
        ((255, 0, 0), (0.627955, 0.224863, 0.125846)),
        ((0, 255, 0), (0.866440, -0.233888, 0.179498)),
        ((0, 0, 255), (0.452014, -0.032457, -0.311528)),
    ],
)
def test_srgb_reference_coordinates(rgb, expected):
    assert oklab(rgb) == pytest.approx(expected, abs=0.000002)


def patch(expected, actual, **options):
    return compare_region(
        Image.new("RGB", (20, 20), expected),
        Image.new("RGB", (20, 20), actual),
        {
            "id": "patch",
            "slide": "page_001",
            "roi": [0, 0, 20, 20],
            "kind": "solid",
            "mode": "faithful",
            **options,
        },
    )


@pytest.mark.parametrize("a,b", [("#606060", "#6C6C6C"), ("#807060", "#747C6C")])
def test_channel_tolerance_does_not_hide_perceptual_drift(a, b):
    r = patch(a, b)
    assert r["max_channel_delta"] == 12
    assert r["issues"] == ["perceptual_color_drift"]
    assert r["status"] == "fail"


def test_small_quantization_passes_and_reports_direction():
    r = patch("#606060", "#616161")
    assert r["status"] == "pass"
    assert 0 < r["perceptual"]["lightness_change"] < 0.02
    assert abs(r["perceptual"]["chroma_change"]) < 0.000001


def test_redesign_is_measured_against_explicit_target():
    r = patch(
        "#606060", "#6C6C6C", mode="target", target_color="#6C6C6C", reason="Requested lighter gray"
    )
    assert r["status"] == "pass"
    assert r["perceptual"]["delta_e_ok"] == 0


def test_difference_symmetry_and_signed_changes():
    a, b = (128, 112, 96), (116, 124, 108)
    ab, ba = color_difference(a, b), color_difference(b, a)
    assert ab["delta_e_ok"] == ba["delta_e_ok"]
    for key in ("lightness_change", "chroma_change"):
        assert ab[key] == -ba[key]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -0.1, 0.11])
def test_invalid_perceptual_tolerance_rejected(value):
    scene = {"slides": [{"id": "page_001", "source": "x.png", "width": 20, "height": 20}]}
    plan = {
        "version": 1,
        "regions": [
            {
                "id": "patch",
                "slide": "page_001",
                "roi": [0, 0, 20, 20],
                "kind": "solid",
                "mode": "faithful",
                "max_delta_e_ok": value,
            }
        ],
    }
    with pytest.raises(InputError):
        validate_plan(plan, scene)
