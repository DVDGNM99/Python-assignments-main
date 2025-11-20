# tests/test_rdkit_utils.py
from pathlib import Path
from src.rdkit_utils import validate_smiles, smiles_to_sdf

ASPIRIN = "CC(=O)OC1=CC=CC=C1C(=O)O"

def test_validate_smiles():
    assert validate_smiles(ASPIRIN) is True
    assert validate_smiles("") is False
    assert validate_smiles("not_a_smiles") is False

def test_smiles_to_sdf_tmp(tmp_path: Path):
    out = tmp_path / "aspirin.sdf"
    p = smiles_to_sdf(ASPIRIN, out, props={"source": "unit-test"})
    assert p.exists()
    # basic sanity: SDF should contain a property block
    txt = p.read_text(encoding="utf-8", errors="ignore")
    assert ">  <source>" in txt
