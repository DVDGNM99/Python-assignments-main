from __future__ import annotations

"""
PubChem client for Chem-Reporter (MVP)
-------------------------------------

This module exposes a single public function:
    resolve(smiles: str) -> Result

Given a SMILES string, it:
  1) fetches the PubChem CID via PUG-REST
  2) fetches the IUPAC name (property endpoint)
  3) fetches experimental data via PUG-View JSON and extracts Melting Point entries
  4) returns a Result dataclass used by the GUI and I/O layers

Notes
-----
- We keep melting point values as strings when formats vary (e.g., ranges
  or with notes). A later parsing pass can normalize to numeric + unit.
- All HTTP calls use timeout and User-Agent from config.py
- Safe URL encoding is applied to SMILES inputs.
"""

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional
import json
from urllib.parse import quote

import requests

from .models import Result, MeltingPoint
from .config import HTTP_TIMEOUT, USER_AGENT

# Base endpoints
PUG_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUG_VIEW_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view"


# -------------------------------
# Low-level HTTP helper
# -------------------------------

def _get(url: str) -> Dict[str, Any]:
    """HTTP GET that returns decoded JSON, raising on HTTP errors.
    Uses project-wide timeout and User-Agent.
    """
    resp = requests.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.json()


# -------------------------------
# Utilities for PUG-View traversal
# -------------------------------

def _string_from_value(info_value: Dict[str, Any]) -> Optional[str]:
    """Best-effort extract a human-readable string from a PUG-View Information.Value.
    Value shapes observed:
      - {"StringWithMarkup":[{"String":"134-136 °C"}, ...]}
      - {"Number": 134.0, "Unit": "°C"}
      - {"String": "134 °C"}
      - {"Table": {...}}  # ignored at MVP level
    """
    if not isinstance(info_value, dict):
        return None

    if "StringWithMarkup" in info_value:
        swm = info_value.get("StringWithMarkup") or []
        if swm and isinstance(swm[0], dict):
            s = swm[0].get("String")
            if isinstance(s, str) and s.strip():
                return s.strip()

    # Rare: direct String
    if "String" in info_value and isinstance(info_value["String"], str):
        s = info_value["String"].strip()
        if s:
            return s

    # Numeric with unit
    if "Number" in info_value:
        num = info_value.get("Number")
        unit = info_value.get("Unit")
        if isinstance(num, (int, float)):
            if isinstance(unit, str) and unit.strip():
                return f"{num} {unit.strip()}"
            return str(num)

    return None


def _walk_sections(sections: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    """Yield each section subtree in depth-first order (PUG-View schema)."""
    for sec in sections or []:
        yield sec
        for child in _walk_sections(sec.get("Section", []) or []):
            yield child


def _extract_melting_points(view_json: Dict[str, Any]) -> List[MeltingPoint]:
    """Collect textual Melting Point entries from PUG-View JSON."""
    mps: List[MeltingPoint] = []

    record = view_json.get("Record") or {}
    top_sections = record.get("Section", []) or []

    for sec in _walk_sections(top_sections):
        toc = (sec.get("TOCHeading") or "").strip()
        if toc.lower() != "melting point":
            continue

        infos = sec.get("Information") or []
        for info in infos:
            val = _string_from_value(info.get("Value", {}))
            if not val:
                continue
            mps.append(
                MeltingPoint(
                    value=val,
                    unit="",            # unit usually embedded in text at MVP stage
                    source="PubChem",
                    notes=None,
                )
            )

    # De-duplicate while preserving order
    seen = set()
    unique: List[MeltingPoint] = []
    for mp in mps:
        key = (mp.value, mp.unit, mp.source)
        if key in seen:
            continue
        seen.add(key)
        unique.append(mp)

    return unique


# -------------------------------
# High-level fetch helpers
# -------------------------------

def _fetch_cid_from_smiles(smiles: str) -> Optional[int]:
    encoded = quote(smiles, safe="")
    url = f"{PUG_BASE}/compound/smiles/{encoded}/cids/JSON"
    data = _get(url)
    try:
        return int(data["IdentifierList"]["CID"][0])
    except Exception:
        return None


def _fetch_iupac_from_cid(cid: int) -> Optional[str]:
    # Use the lightweight property endpoint for IUPAC name
    url = f"{PUG_BASE}/compound/cid/{cid}/property/IUPACName/JSON"
    data = _get(url)
    try:
        props = data["PropertyTable"]["Properties"][0]
        name = props.get("IUPACName")
        if isinstance(name, str) and name.strip():
            return name.strip()
    except Exception:
        pass
    return None


def _fetch_view_json(cid: int) -> Dict[str, Any]:
    url = f"{PUG_VIEW_BASE}/data/compound/{cid}/JSON"
    return _get(url)


# -------------------------------
# Public API
# -------------------------------

def fetch_pubchem_by_smiles(smiles: str) -> Dict[str, Any]:
    """Convenience function that returns a plain dict with core fields.
    Kept for backward compatibility with earlier iterations.
    """
    cid = _fetch_cid_from_smiles(smiles)
    if cid is None:
        raise ValueError("Could not resolve CID from the provided SMILES.")

    iupac = _fetch_iupac_from_cid(cid)
    view = _fetch_view_json(cid)
    mps = _extract_melting_points(view)

    return {
        "cid": cid,
        "iupac_name": iupac,
        "melting_points": [asdict(mp) for mp in mps],
        "sources": {
            "pubchem_cid": f"{PUG_BASE}/compound/smiles/{quote(smiles, safe='')}/cids/JSON",
            "pubchem_property": f"{PUG_BASE}/compound/cid/{cid}/property/IUPACName/JSON",
            "pubchem_view": f"{PUG_VIEW_BASE}/data/compound/{cid}/JSON",
        },
    }


def resolve(smiles: str) -> Result:
    """High-level entrypoint used by the GUI.

    Returns a populated Result dataclass with:
      - input_smiles
      - cid
      - iupac_name
      - melting_points (List[MeltingPoint])
      - sources (Dict[str, str])
      - created_at (ISO string)
    """
    cid = _fetch_cid_from_smiles(smiles)
    if cid is None:
        raise ValueError("Could not resolve CID from the provided SMILES.")

    iupac = _fetch_iupac_from_cid(cid)
    view = _fetch_view_json(cid)
    melting_points = _extract_melting_points(view)

    sources = {
        "pubchem_cid": f"{PUG_BASE}/compound/smiles/{quote(smiles, safe='')}/cids/JSON",
        "pubchem_property": f"{PUG_BASE}/compound/cid/{cid}/property/IUPACName/JSON",
        "pubchem_view": f"{PUG_VIEW_BASE}/data/compound/{cid}/JSON",
    }

    return Result(
        input_smiles=smiles,
        cid=cid,
        iupac_name=iupac,
        melting_points=melting_points,
        sources=sources,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )
