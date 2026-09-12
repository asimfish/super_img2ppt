from fontTools.ttLib import TTFont
from super_img2ppt import fonts as font_module


def test_mac_style_italic_is_not_misclassified_when_os2_flag_is_missing(
    fonts, tmp_path, monkeypatch
):
    face = fonts.faces[0]
    path = tmp_path / "italic.ttf"
    with TTFont(face.path, fontNumber=face.index) as font:
        font["OS/2"].fsSelection &= ~1
        font["head"].macStyle |= 2
        font.save(path)
    monkeypatch.setattr(font_module, "font_candidates", lambda extra_dirs=(): [(str(path), 0)])
    font_module.discover_fonts.cache_clear()
    try:
        discovered = font_module.discover_fonts()
        assert len(discovered) == 1
        assert discovered[0].italic is True
    finally:
        font_module.discover_fonts.cache_clear()
