from pathlib import Path
import json
from src.pubchem import _extract_melting_point

DATA = Path(__file__).parent / "data"

def _j(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))

def test_aspirin_offline_mp():
    data = _j("aspirin_pugview.json")
    values = _extract_melting_point(data)
    assert any("135" in str(v) for v in values)

def test_caffeine_offline_mp():
    data = _j("caffeine_pugview.json")
    values = _extract_melting_point(data)
    assert any("235" in str(v) for v in values)
