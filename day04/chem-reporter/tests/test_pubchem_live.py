# tests/test_pubchem_live.py
import json
from pathlib import Path
import pytest

from src.io_utils import build_outputs

@pytest.mark.network
def test_aspirin_live(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    out = build_outputs(
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        results_dir=Path("results"),
        preferred_name="aspirin_live",
        num_confs=2,
        random_seed=0
    )
    assert out is not None

    base = Path("results") / "aspirin_live"
    meta = json.loads((base / "metadata.json").read_text(encoding="utf-8"))
    
    assert meta.get("iupac_name")
   
