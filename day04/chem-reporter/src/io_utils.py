# placeholder IO utilities
# src/io_utils.py
# src/io_utils.py
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Iterable, Optional

from .rdkit_utils import smiles_to_sdf

# Try to import your dataclasses, but keep the code robust if fields differ
try:
    from .models import Result  # type: ignore
except Exception:
    Result = object  # fallback for type checkers


def safe_name(text: str) -> str:
    """
    Make a filesystem-safe name (folders/files).
    """
    unsafe = r'<>:"/\\|?*'
    cleaned = "".join("_" if c in unsafe else c for c in str(text)).strip()
    return cleaned or "unnamed"


def _result_folder_name(result: Any) -> str:
    """
    Prefer IUPAC name; otherwise use a shortened SMILES.
    """
    iupac = getattr(result, "iupac_name", None)
    if iupac:
        return safe_name(iupac)

    smi = getattr(result, "input_smiles", "") or ""
    smi = smi if len(smi) <= 40 else smi[:40] + "..."
    return safe_name(smi or "compound")


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _coerce_sources(sources: Any) -> Dict[str, str]:
    """
    Normalize sources to a dict[str, str].
    Accepts dict, list, str, or None.
    """
    if isinstance(sources, dict):
        return {str(k): str(v) for k, v in sources.items()}
    if isinstance(sources, (list, tuple)):
        return {f"source_{i+1}": str(v) for i, v in enumerate(sources)}
    if isinstance(sources, str):
        return {"source": sources}
    return {}


def _iter_melting_points(mps: Optional[Iterable[Any]]) -> Iterable[Dict[str, Any]]:
    """
    Convert melting point objects/rows into a uniform dict form.
    Handles both text and numeric values, with optional unit/source/notes.
    """
    if not mps:
        return []

    out = []
    for mp in mps:
        # Try common attribute names; fall back to dict-style access
        value = getattr(mp, "value", None)
        unit = getattr(mp, "unit", None)
        source = getattr(mp, "source", None)
        notes = getattr(mp, "notes", None)
        source_url = getattr(mp, "source_url", None)

        if isinstance(mp, dict):
            value = mp.get("value", value)
            unit = mp.get("unit", unit)
            source = mp.get("source", source)
            notes = mp.get("notes", notes)
            source_url = mp.get("source_url", source_url)

        # Coerce value to string (MVP keeps free text like "134–136 °C")
        if value is None:
            value_str = ""
        else:
            value_str = str(value)

        out.append(
            {
                "value": value_str,
                "unit": "" if unit is None else str(unit),
                "source": "PubChem" if source is None else str(source),
                "notes": None if notes is None else str(notes),
                "source_url": None if source_url is None else str(source_url),
            }
        )
    return out


def write_outputs(result: Any, base_dir: str = "results") -> str:
    """
    Create results/<CompoundName>/ and write:
      - metadata.json   (rich, machine-friendly)
      - IUPAC.txt       (plain text)
      - melting_point.csv
      - structure.sdf   (with minimal properties)
    Returns the absolute path to the created folder.
    """
    folder_name = _result_folder_name(result)
    out_dir = os.path.abspath(os.path.join(base_dir, folder_name))
    _ensure_dir(out_dir)

    # Metadata
    created_at = getattr(result, "created_at", None)
    if not created_at:
        created_at = datetime.utcnow().isoformat() + "Z"

    metadata = {
        "created_at": created_at,
        "input_smiles": getattr(result, "input_smiles", ""),
        "cid": getattr(result, "cid", None),
        "iupac_name": getattr(result, "iupac_name", None),
        "sources": _coerce_sources(getattr(result, "sources", None)),
        "melting_points": list(_iter_melting_points(getattr(result, "melting_points", None))),
        "errors": getattr(result, "errors", None),
    }

    with open(os.path.join(out_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # IUPAC.txt
    with open(os.path.join(out_dir, "IUPAC.txt"), "w", encoding="utf-8") as f:
        f.write(str(getattr(result, "iupac_name", "") or ""))

    # melting_point.csv
    csv_path = os.path.join(out_dir, "melting_point.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("source,value,unit,notes,source_url\n")
        for row in metadata["melting_points"]:
            notes = "" if row["notes"] is None else row["notes"].replace("\n", " ").strip()
            source_url = "" if row["source_url"] is None else row["source_url"]
            f.write(f"{row['source']},{row['value']},{row['unit']},{notes},{source_url}\n")

    # structure.sdf
    props: Dict[str, Any] = {
        "CID": "" if metadata["cid"] is None else str(metadata["cid"]),
        "IUPAC": metadata["iupac_name"] or "",
    }
    sdf_path = os.path.join(out_dir, "structure.sdf")
    smiles_to_sdf(metadata["input_smiles"], sdf_path, props=props)

    return out_dir
