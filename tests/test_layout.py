import pytest
from super_img2ppt.fonts import measure
from super_img2ppt.layout import fit_text, layout_scene


def test_real_font_width_rejects_wide_letters_but_accepts_narrow(fonts):
    face = fonts.resolve("Wi", None, None, False, False)
    wide, narrow = measure(face, "WWWWWW", 32)[0], measure(face, "iiiiii", 32)[0]
    assert wide > narrow * 2
    element = {"box": [0, 0, (wide + narrow) / 2, 60], "font_size": 32, "text": "iiiiii"}
    assert fit_text(element, fonts).fits
    element["text"] = "WWWWWW"
    assert not fit_text(element, fonts).fits


def test_shrink_respects_floor_and_does_not_enlarge(fonts):
    e = {
        "box": [0, 0, 40, 40],
        "font_size": 32,
        "min_font_size": 28,
        "fit": "shrink",
        "text": "WWWWWW",
    }
    result = fit_text(e, fonts)
    assert result.effective_font_size == 28
    assert not result.fits
    e["box"] = [0, 0, 1000, 200]
    assert fit_text(e, fonts).effective_font_size == 32


def test_cjk_wrap_preserves_text_and_punctuation(fonts):
    text = "中文换行（完整内容），English words。"
    e = {"box": [0, 0, 210, 230], "font_size": 26, "text": text, "wrap": True}
    result = fit_text(e, fonts)
    assert result.fits
    assert "".join(line.text for line in result.lines) == text
    assert len(result.lines) >= 2
    assert all(not line.text.startswith(("）", "，", "。")) for line in result.lines)


def test_explicit_blank_lines_and_mixed_runs_survive(fonts):
    e = {
        "box": [0, 0, 900, 250],
        "font_size": 28,
        "runs": [
            {"text": "Normal ", "font_size": 28},
            {"text": "BIG\n\n中文", "font_size": 40, "bold": True},
        ],
    }
    result = fit_text(e, fonts)
    assert result.fits
    assert [line.text for line in result.lines] == ["Normal BIG", "", "中文"]
    assert result.lines[0].fragments[0].size == 28
    assert result.lines[0].fragments[-1].size == 40


def test_font_group_shrinks_together_and_strict_member_blocks_reflow(scene, fonts):
    first = scene["slides"][0]["elements"][0]
    first.update(
        text="WWWWWW",
        box=[60, 60, 185, 80],
        font_size=40,
        font_group="title",
        fit="shrink",
        min_font_size=30,
    )
    second = {**first, "id": "second", "box": [60, 260, 700, 80], "text": "Hi"}
    scene["slides"][0]["elements"].append(second)
    result = layout_scene(scene, fonts)
    assert 0.75 <= result["page_001", "title"].scale < 1
    assert result["page_001", "title"].scale == result["page_001", "second"].scale
    second["fit"] = "strict"
    result = layout_scene(scene, fonts)
    assert result["page_001", "title"].scale == 1
    assert not result["page_001", "title"].fits


def test_unknown_font_substitution_is_recorded():
    from super_img2ppt.fonts import FontCatalog

    catalog = FontCatalog()
    face = catalog.resolve("Hello", "Definitely Missing Font 123", None, False, False)
    assert ("font_substitution", "Definitely Missing Font 123", face.family) in catalog.events


def test_missing_glyph_is_error(fonts):
    from super_img2ppt.scene import InputError

    with pytest.raises(InputError, match="No configured font covers"):
        fonts.resolve("\U0010ffff", None, None, False, False)


def test_report_explains_exact_width_safety_margin(fonts):
    element = {"box": [0, 0, 1000, 100], "font_size": 32, "text": "Exact width"}
    initial = fit_text(element, fonts)
    element["box"][2] = initial.width
    result = fit_text(element, fonts)
    assert not result.fits
    report = result.report()
    assert report["required_width_px"] == pytest.approx(result.width + 0.5, abs=0.001)
    assert report["required_width_px"] > report["available_width_px"]


def test_visible_ink_excludes_trailing_punctuation_advance(fonts):
    from super_img2ppt.fonts import ink_bounds

    face = fonts.resolve("。", None, None, False, False)
    bounds = ink_bounds(face, "。", 32)
    assert bounds is not None
    assert bounds[2] - bounds[0] < measure(face, "。", 32)[0] * 0.7
