from unittest.mock import MagicMock
import pytest

from App.rendering import add_regions

def test_add_regions_calls_scene():
    scene = MagicMock()
    acrs = ["MOs", "VISp", "ACA"]
    cols = ["#112233", "#445566", "#778899"]
    add_regions(scene, acrs, cols, 0.5)
    # una chiamata per regione
    assert scene.add_brain_region.call_count == 3
    # prima call ha parametri giusti
    first_call = scene.add_brain_region.call_args_list[0]
    assert first_call.kwargs["alpha"] == 0.5
    assert first_call.kwargs["color"] == "#112233"
