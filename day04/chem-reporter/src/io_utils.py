# placeholder IO utilities
# src/io_utils.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, Optional
import json
import csv

from src.rdkit_utils import smiles_to_sdf

# --- FS helpers --------------------------------------------------------------

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_json(data: Dict[str, Any], path: Path) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def write_csv(rows: Dict[str, Any] | list[Dict[str, Any]], path: Path) -> None:
    ensure_dir(path.parent)
    if isinstance(rows, dict):
        # write a single-row CSV
        rows = [rows]
    if not rows:
        # nothing to write
        write_json({"warning": "no rows"}, path.with_suffix(".json"))
        return
    fieldnames = sorted({k for r in rows for k in r.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

# --- PubChem adapter ---------------------------------------------------------

def get_pubchem_metadata(smiles: str) -> Dict[str, Any]:
    """
    Adapter to call whatever function your pubchem.py exposes.
    Must return a dict with keys like: cid, iupac_name, molecular_formula, melting_point, etc.
    This tries common function names to avoid tight coupling.
    """
    try:
        from src import pubchem as _pc  # local module
    except Exception:
        return {}

    # Try several likely API shapes without crashing the pipeline.
    for fn_name in (
        "fetch_pubchem_by_smiles",
        "fetch_properties_by_smiles",
        "get_by_smiles",
        "get_properties",
        "resolve_smiles",
    ):
        fn = getattr(_pc, fn_name, None)
        if callable(fn):
            try:
                data = fn(smiles)  # expected to be a dict-like
                if isinstance(data, dict):
                    return data
            except Exception:
                pass

    # As a last resort, try a generic 'search' returning a list
    fn = getattr(_pc, "search_by_smiles", None)
    if callable(fn):
        try:
            res = fn(smiles)
            if isinstance(res, list) and res:
                return res[0] if isinstance(res[0], dict) else {}
        except Exception:
            pass

    return {}

# --- Naming helpers ----------------------------------------------------------

def safe_name(text: str) -> str:
    """Create a filesystem-friendly name (Windows-safe)."""
    invalid = '<>:"/\\|?*'
    out = "".join("_" if c in invalid else c for c in text.strip())
    return out or "compound"

# --- Main pipeline -----------------------------------------------------------

def build_outputs(
    smiles: str,
    results_dir: Path,
    preferred_name: Optional[str] = None,
    num_confs: int = 1,
    random_seed: int = 0xF00D,
) -> Dict[str, Any]:
    """
    High-level pipeline:
    1) Fetch PubChem metadata from SMILES
    2) Generate 3D SDF with RDKit and attach metadata as SD fields
    3) Save JSON and CSV summaries

    Returns a manifest dict with useful paths and metadata.
    """
    metadata = get_pubchem_metadata(smiles) or {}

    # Determine compound folder name
    base_name = preferred_name or metadata.get("iupac_name") or metadata.get("cid") or smiles
    compound_name = safe_name(str(base_name))
    compound_dir = results_dir / compound_name
    ensure_dir(compound_dir)

    # Write SDF with properties
    sdf_path = compound_dir / "structure.sdf"
    props = {
        "smiles": smiles,
        **metadata,  # cid, iupac_name, molecular_formula, melting_point, etc. (if available)
    }
    smiles_to_sdf(
        smiles=smiles,
        output_path=sdf_path,
        props=props,
        num_confs=num_confs,
        random_seed=random_seed,
    )

    # Write metadata files
    json_path = compound_dir / "metadata.json"
    write_json(props, json_path)

    # Optional: a flat CSV with the main properties (present if provided by PubChem)
    csv_row = {
        "name": compound_name,
        "smiles": smiles,
        "cid": metadata.get("cid"),
        "iupac_name": metadata.get("iupac_name"),
        "molecular_formula": metadata.get("molecular_formula"),
        "molecular_weight": metadata.get("molecular_weight"),
        "melting_point": metadata.get("melting_point"),
    }
    csv_path = results_dir / "summary.csv"
    if csv_row["cid"] or csv_row["iupac_name"]:
        write_csv(csv_row, csv_path)

    manifest = {
        "compound_dir": str(compound_dir),
        "sdf": str(sdf_path),
        "json": str(json_path),
        "csv": str(csv_path),
        "props": props,
    }
    # Also write a manifest for quick inspection
    write_json(manifest, compound_dir / "manifest.json")
    return manifest
