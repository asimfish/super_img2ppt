import copy
import json
import zipfile

import pytest
from PIL import Image
from super_img2ppt.layout import layout_scene
from super_img2ppt.prepare import fresh_directory, inspect_archive, prepare
from super_img2ppt.qa import preflight
from super_img2ppt.scene import InputError, load_scene, safe_asset, slide_transform, validate_scene


def test_bad_coordinates_and_duplicate_ids_rejected(scene):
    e = scene["slides"][0]["elements"][0]
    e["box"][0] = float("nan")
    with pytest.raises(InputError, match="NaN"):
        validate_scene(scene)
    e["box"][0] = 0
    scene["slides"][0]["elements"].append(copy.deepcopy(e))
    with pytest.raises(InputError, match="Duplicate element"):
        validate_scene(scene)


def test_duplicate_json_keys_rejected(tmp_path):
    path = tmp_path / "scene.json"
    path.write_text('{"version":1,"version":2,"slides":[]}')
    with pytest.raises(InputError, match="Duplicate JSON"):
        load_scene(path)


def test_kind_specific_fields_cannot_silently_drop_text(scene):
    element = scene["slides"][0]["elements"][0]
    element.update(kind="shape", shape="rect")
    with pytest.raises(InputError, match="fields not supported for shape"):
        validate_scene(scene)


def test_renamed_full_source_image_is_not_a_reconstruction(scene, fonts, tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (1280, 720), "white").save(source)
    (tmp_path / "renamed.png").write_bytes(source.read_bytes())
    slide = scene["slides"][0]
    slide["source"] = "source.png"
    slide["elements"].append(
        {
            "id": "background",
            "kind": "image",
            "role": "background",
            "z": 0,
            "box": [0, 0, 1280, 720],
            "path": "renamed.png",
            "contains_text": False,
            "provenance": "Copy of whole source image",
        }
    )
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert any(f["code"] == "source_image_as_asset" for f in result["findings"])


def test_asset_paths_confine_symlinks_and_traversal(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    secret = tmp_path / "outside.png"
    secret.write_bytes(b"private")
    (root / "link.png").symlink_to(secret)
    for path in [
        "../outside.png",
        "link.png",
        str(secret),
        "https://example.com/image.png",
        "C:\\outside.png",
    ]:
        with pytest.raises(InputError):
            safe_asset(root, path)


def test_existing_output_is_preserved(tmp_path):
    marker = tmp_path / "mine.txt"
    marker.write_text("user content")
    with pytest.raises(InputError, match="already exists"):
        fresh_directory(tmp_path)
    assert marker.read_text() == "user content"


def test_line_stroke_is_counted_once_at_page_boundary(scene, tmp_path):
    line = {
        "id": "rule",
        "kind": "line",
        "z": 0,
        "points": [[0, 1], [1280, 1]],
        "stroke": "#000000",
        "stroke_width": 2,
    }
    scene["slides"][0]["elements"] = [line]
    assert preflight(scene, {}, tmp_path)["status"] == "pass"
    line["points"] = [[0, 0], [1280, 0]]
    result = preflight(scene, {}, tmp_path)
    assert any(f["code"] == "out_of_bounds" for f in result["findings"])


def test_diamond_contains_visible_text_without_requiring_empty_frame_corners(
    scene, fonts, tmp_path
):
    text = scene["slides"][0]["elements"][0]
    text.update(text="A", font_family="Arial", box=[130, 40, 200, 130], container="decision")
    scene["slides"][0]["elements"].append(
        {
            "id": "decision",
            "kind": "shape",
            "shape": "diamond",
            "z": 0,
            "box": [0, 0, 400, 200],
            "fill": "#FFFFFF",
        }
    )
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert result["status"] == "pass"
    assert any(f["code"] == "text_frame_outside_container_only" for f in result["findings"])
    text["box"][0] = 60
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert any(f["code"] == "outside_container" for f in result["findings"])


def test_blank_glyph_corner_is_not_ink_but_letter_stroke_is(scene, fonts, tmp_path):
    text = scene["slides"][0]["elements"][0]
    text.update(text="A", font_family="Arial", box=[100, 60, 100, 100])
    corner = {
        "id": "corner",
        "kind": "shape",
        "shape": "rect",
        "z": 3,
        "box": [100, 68, 5, 5],
        "fill": "#000000",
    }
    scene["slides"][0]["elements"].append(corner)
    assert preflight(scene, layout_scene(scene, fonts), tmp_path)["status"] == "pass"
    corner["box"][0] = 110
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert any(f["code"] == "unintended_overlap" for f in result["findings"])


def test_partial_ink_measurement_cannot_hide_a_large_run_collision(scene, fonts, tmp_path):
    slide = scene["slides"][0]
    slide["width"] = 3000
    text = slide["elements"][0]
    text.pop("text")
    text.update(
        font_family="Arial",
        font_size=320,
        box=[80, 60, 2600, 420],
        runs=[{"text": "MMMMMMMM"}, {"text": " A", "font_size": 36}],
    )
    slide["elements"].append(
        {
            "id": "obstacle",
            "kind": "shape",
            "shape": "rect",
            "z": 3,
            "box": [100, 120, 100, 100],
            "fill": "#000000",
        }
    )
    result = preflight(validate_scene(scene), layout_scene(scene, fonts), tmp_path)
    assert any(f["code"] == "unintended_overlap" for f in result["findings"])


def test_container_is_allowed_but_obstruction_is_blocked(scene, fonts, tmp_path):
    elements = scene["slides"][0]["elements"]
    elements[0]["container"] = "card"
    elements.append(
        {
            "id": "card",
            "kind": "shape",
            "z": 1,
            "shape": "rect",
            "box": [60, 40, 760, 160],
            "fill": "#FFFFFF",
        }
    )
    result = preflight(validate_scene(scene), layout_scene(scene, fonts), tmp_path)
    assert result["status"] == "pass"
    elements.append(
        {
            "id": "cover",
            "kind": "shape",
            "z": 4,
            "shape": "rect",
            "box": [90, 65, 80, 80],
            "fill": "#000000",
        }
    )
    result = preflight(validate_scene(scene), layout_scene(scene, fonts), tmp_path)
    assert any(
        f["code"] == "unintended_overlap" and "title" in f["elements"] for f in result["findings"]
    )


def test_unreviewed_and_empty_are_not_success(scene, fonts, tmp_path):
    scene["slides"][0].update(reviewed=False, elements=[])
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert result["status"] == "fail"
    assert {f["code"] for f in result["findings"]} == {"empty_slide", "unreviewed_scene"}


def test_text_frame_padding_overlap_is_distinct_from_visible_collision(scene, fonts, tmp_path):
    elements = scene["slides"][0]["elements"]
    elements[0].update(text="A", box=[80, 60, 150, 100])
    elements.append({**elements[0], "id": "second", "box": [160, 60, 150, 100]})
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert result["status"] == "pass"
    assert any(f["code"] == "text_frame_overlap_only" for f in result["findings"])
    elements[1]["box"][0] = 85
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert result["status"] == "fail"
    assert any(f["code"] == "unintended_overlap" for f in result["findings"])


@pytest.mark.parametrize("obstacle", ["line", "shape"])
def test_text_padding_can_touch_grid_or_shape_but_ink_cannot(scene, fonts, tmp_path, obstacle):
    text = scene["slides"][0]["elements"][0]
    text.update(text="Hello", font_family="Arial", box=[80, 60, 250, 100], font_size=36)
    element = {"id": "obstacle", "kind": obstacle, "z": 3}
    if obstacle == "line":
        element.update(points=[[70, 63], [340, 63]], stroke_width=1)
    else:
        element.update(box=[70, 61, 270, 3], shape="rect", fill="#000000")
    scene["slides"][0]["elements"].append(element)
    report = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert report["status"] == "pass", report["findings"]
    assert any(f["code"] == "text_frame_overlap_only" for f in report["findings"])
    if obstacle == "line":
        element["points"] = [[70, 85], [340, 85]]
    else:
        element["box"][1] = 83
    report = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert report["status"] == "fail"
    assert any(f["code"] == "unintended_overlap" for f in report["findings"])


def test_baked_text_overlap_cannot_be_exempted(scene, fonts, tmp_path):
    Image.new("RGB", (100, 100), "white").save(tmp_path / "raster.png")
    scene["slides"][0]["elements"].append(
        {
            "id": "baked",
            "kind": "image",
            "z": 0,
            "box": [80, 60, 700, 100],
            "path": "raster.png",
            "provenance": "Original plot with axis labels",
            "contains_text": True,
            "allow_overlap_with": ["title"],
            "overlap_reason": "This deliberate exemption must not suppress baked text",
        }
    )
    result = preflight(scene, layout_scene(scene, fonts), tmp_path)
    assert any(f["code"] == "baked_text_overlap" for f in result["findings"])


def test_mixed_aspect_pages_are_letterboxed_not_stretched(scene):
    other = {**scene["slides"][0], "width": 960, "height": 720}
    tx = slide_transform(scene, other)
    assert tx.x > 0
    assert tx.y == pytest.approx(0)
    box = tx.box([0, 0, 300, 300])
    assert box[2] == box[3]


@pytest.mark.parametrize(
    "name,body",
    [
        ("../bad.xml", "<x/>"),
        (
            "ppt/_rels/presentation.xml.rels",
            '<Relationships><Relationship TargetMode="External" Target="https://example.com"/></Relationships>',
        ),
        ("ppt/slides/slide1.xml", '<!DOCTYPE x [<!ENTITY bad "test">]><x/>'),
        ("ppt/vbaProject.bin", "binary"),
    ],
)
def test_unsafe_archive_never_reaches_renderer(tmp_path, name, body):
    path = tmp_path / "malicious.pptx"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(name, body)
    with pytest.raises(InputError):
        inspect_archive(path)


def test_prepare_preserves_argument_order_and_pixel_size(tmp_path):
    paths = []
    for n, size in [(2, (320, 180)), (1, (240, 180))]:
        path = tmp_path / f"source{n}.png"
        Image.new("RGB", size, "white").save(path)
        paths.append(path)
    out = tmp_path / "prepared"
    result = prepare(paths, out, ocr="none")
    scene = load_scene(out / "scene.json")
    assert result["page_count"] == 2
    assert [(s["width"], s["height"]) for s in scene["slides"]] == [(320, 180), (240, 180)]
    assert all(not s["elements"] for s in scene["slides"])
    assert json.loads((out / "pages/page_001/ocr.json").read_text())["status"] == "unavailable"
