import pytest
from PIL import Image, ImageCms
from super_img2ppt.color_management import to_srgb
from super_img2ppt.prepare import _normalize_image
from super_img2ppt.scene import InputError


def test_lab_profile_applied_before_channel_conversion(tmp_path):
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("LAB"))
    im = Image.new("LAB", (32, 32), (140, 155, 105))
    im.info["icc_profile"] = profile.tobytes()
    expected = ImageCms.profileToProfile(
        im, profile, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB"
    )
    im.save(tmp_path / "lab.tiff", icc_profile=profile.tobytes())
    _normalize_image(tmp_path / "lab.tiff", tmp_path / "source.png")
    with Image.open(tmp_path / "source.png") as actual:
        assert actual.getpixel((16, 16)) == expected.getpixel((16, 16))
        assert "icc_profile" not in actual.info
    assert (tmp_path / "source.color.json").exists()


def test_srgb_profile_and_alpha_preserved():
    im = Image.new("RGBA", (20, 20), (10, 100, 200, 128))
    im.info["icc_profile"] = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    actual, report = to_srgb(im)
    assert actual.getpixel((5, 5)) == (132, 177, 227)
    assert report["status"] == "converted"


def test_untagged_rgb_is_unchanged():
    im = Image.new("RGB", (20, 20), (80, 150, 180))
    actual, report = to_srgb(im)
    assert actual.tobytes() == im.tobytes()
    assert report["status"] == "assumed_srgb"


@pytest.mark.parametrize("mode,profile", [("RGB", b"broken"), ("CMYK", None), ("LAB", None)])
def test_invalid_or_ambiguous_profile_is_not_silently_dropped(mode, profile):
    im = Image.new(mode, (20, 20))
    if profile:
        im.info["icc_profile"] = profile
    with pytest.raises(InputError):
        to_srgb(im)


def test_palette_transparency_keeps_color_before_compositing():
    im = Image.new("P", (20, 20), 0)
    im.putpalette([10, 100, 200] + [0] * 765)
    im.info["transparency"] = bytes([128])
    actual, _ = to_srgb(im)
    assert actual.getpixel((4, 4)) == (132, 177, 227)


def test_export_asset_converts_profile_and_preserves_alpha(tmp_path):
    from super_img2ppt.export import _image_data

    im = Image.new("LAB", (32, 32), (140, 155, 105))
    profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("LAB"))
    im.save(tmp_path / "asset.tiff", icc_profile=profile.tobytes())
    expected = ImageCms.profileToProfile(
        im, profile, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB"
    )
    data, size = _image_data(tmp_path / "asset.tiff")
    with Image.open(data) as actual:
        assert actual.tobytes() == expected.tobytes()
        assert "icc_profile" not in actual.info
    assert size == (32, 32)
    rgba = Image.new("RGBA", (20, 20), (10, 100, 200, 128))
    rgba.save(tmp_path / "alpha.png")
    data, _ = _image_data(tmp_path / "alpha.png")
    with Image.open(data) as actual:
        assert actual.getpixel((5, 5)) == (10, 100, 200, 128)


@pytest.mark.parametrize("mode,color,key", [("RGB", (255, 0, 0), (255, 0, 0)), ("L", 0, 0)])
def test_color_key_transparency(mode, color, key):
    im = Image.new(mode, (20, 20), color)
    im.info["transparency"] = key
    opaque, _ = to_srgb(im)
    assert opaque.getpixel((0, 0)) == (255, 255, 255)
    transparent, _ = to_srgb(im, preserve_alpha=True)
    assert transparent.getpixel((0, 0))[3] == 0


def test_gray_alpha_profile_transform_receives_l_channel(monkeypatch):
    # Portable contract: Pillow cannot synthesize a gray ICC for redistribution.
    def transform(source, incoming, outgoing, **kwargs):
        assert source.mode == "L"
        return source.convert("RGB")

    monkeypatch.setattr(ImageCms, "profileToProfile", transform)
    im = Image.new("LA", (20, 20), (128, 100))
    im.info["icc_profile"] = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    actual, _ = to_srgb(im, preserve_alpha=True)
    assert actual.getpixel((0, 0)) == (128, 128, 128, 100)
