import pytest
from App.logic import (
    load_regions_from_json, InvalidJSON, EmptyRegions,
    validate_acronyms, normalize_hex, cycle_colors,
    selection_from_display, prepare_render_inputs,
)
from pathlib import Path
import json

def test_load_regions_dict(tmp_path: Path):
    data = {"MOs": "Secondary motor area", "VISp": "Primary visual area"}
    p = tmp_path / "regions.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    items = load_regions_from_json(p)
    acrs = [i.acronym for i in items]
    assert "MOs" in acrs and "VISp" in acrs

def test_load_regions_list(tmp_path: Path):
    data = [{"acronym": "ACA", "name": "Anterior cingulate area"}]
    p = tmp_path / "regions.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    items = load_regions_from_json(p)
    assert items[0].display.startswith("ACA — ")

def test_load_regions_invalid_raises(tmp_path: Path):
    p = tmp_path / "regions.json"
    p.write_text("42", encoding="utf-8")
    with pytest.raises(InvalidJSON):
        load_regions_from_json(p)

def test_validate_acronyms():
    valid, invalid = validate_acronyms(["MOs", "XYZ"], ["MOs", "VISp"])
    assert valid == ["MOs"] and invalid == ["XYZ"]

def test_color_utils():
    assert normalize_hex("#AABBCC") == "#aabbcc"
    with pytest.raises(ValueError):
        normalize_hex("blue")
    assert len(cycle_colors(3)) == 3

def test_selection_from_display():
    assert selection_from_display("MOs — Secondary motor area") == "MOs"
    with pytest.raises(ValueError):
        selection_from_display("")

def test_prepare_render_inputs_autocolor():
    acrs, cols, alpha = prepare_render_inputs(
        ["MOs — X", "VISp — Y"], None, 0.5
    )
    assert acrs == ["MOs", "VISp"]
    assert len(cols) == 2
    assert alpha == 0.5

def test_prepare_render_inputs_custom_colors_len_check():
    with pytest.raises(ValueError):
        prepare_render_inputs(["MOs — X"], ["#ff00aa", "#00ffaa"], 0.3)
