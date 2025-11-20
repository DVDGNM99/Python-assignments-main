# tests/test_pubchem_offline.py
from pathlib import Path
from unittest.mock import patch
import json

from src.io_utils import build_outputs

FAKE_PUBCHEM = {
    "cid": 2244,
    "iupac_name": "2-(acetyloxy)benzoic acid",
    "properties": {
        "melting_points": [{"value": "134-136", "unit": "°C", "source": "PubChem", "notes": "range"}]
    },
    "sources": {
        "cid": "https://pubchem.ncbi.nlm.nih.gov/compound/2244",
        "pug_view": "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/2244/JSON"
    }
}

def _fake_fetch(smiles: str):
    return FAKE_PUBCHEM

@patch("src.pubchem.fetch_pubchem_by_smiles", side_effect=_fake_fetch)
def test_build_outputs_offline(mock_fetch, tmp_path, monkeypatch):
    # temporary dir for test
    monkeypatch.chdir(tmp_path)

    out = build_outputs(
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        results_dir=Path("results"),
        preferred_name="aspirin_mock",
        num_confs=2,
        random_seed=1
    )
    assert out is not None

    base = Path("results") / "aspirin_mock"
    assert (base / "structure.sdf").exists()
    assert (base / "metadata.json").exists()

    meta = json.loads((base / "metadata.json").read_text(encoding="utf-8"))
    assert meta.get("cid") == FAKE_PUBCHEM["cid"]
    assert meta.get("iupac_name") == FAKE_PUBCHEM["iupac_name"]
