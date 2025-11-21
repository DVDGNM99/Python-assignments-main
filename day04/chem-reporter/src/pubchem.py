from __future__ import annotations
"""
PubChem client for Chem-Reporter (MVP)

Public entrypoints:
    - resolve(smiles: str) -> Result
    - fetch_pubchem_by_smiles(smiles: str) -> dict

Workflow:
  1) Resolve CID from SMILES (PUG-REST).
  2) Fetch IUPAC name (property endpoint).
  3) Fetch PUG-View JSON and extract "Melting Point" entries.
  4) Normalize values to °C, compact ranges, deduplicate, keep notes.
  5) Return a Result dataclass (used by the GUI/IO layers).

Notes
-----
- We keep the human-readable value in `MeltingPoint.value` (string),
  e.g. "135 °C" or "138–140 °C". This is friendlier for CSV/GUI.
- Units are standardized to "°C". If converted from °F, we append a note.
- All HTTP calls use timeout/User-Agent from config.
"""

from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import quote
import re
import unicodedata

import requests

from .models import Result, MeltingPoint
from .config import HTTP_TIMEOUT, USER_AGENT

# ------------------------------------------------------------------
# Text normalization & numeric parsing
# ------------------------------------------------------------------

_DEG_PATTERN = re.compile(r"(?i)\s*(?:deg(?:rees?)?\s*)?([CF])")
_NUM_RANGE_PATTERN = re.compile(
    r"(?P<n1>[-+]?\d+(?:[\.,]\d+)?)\s*(?:[-–—~to]{1,3}\s*(?P<n2>[-+]?\d+(?:[\.,]\d+)?))?"
)

def _u(text: str | None) -> str:
    """Unicode normalize; remove NBSP/soft hyphen; collapse whitespace."""
    if text is None:
        return ""
    t = unicodedata.normalize("NFKC", str(text))
    t = t.replace("\xa0", " ").replace("\u00ad", "")
    return " ".join(t.split())

def _split_notes(raw: str) -> tuple[str, str | None]:
    """
    Extract the first parenthetical note, e.g. "135 °C (rapid heating)" ->
    ("135 °C", "(rapid heating)").
    """
    raw = _u(raw)
    notes = None
    if "(" in raw and ")" in raw:
        try:
            i = raw.index("(")
            j = raw.index(")", i + 1)
            notes = raw[i : j + 1]
            raw = (raw[:i] + raw[j + 1 :]).strip()
        except ValueError:
            pass
    return raw, notes

def _extract_unit(raw: str) -> str | None:
    """Return 'C' or 'F' if a degree unit is detected; otherwise None."""
    m = _DEG_PATTERN.search(raw.replace("°", ""))
    return m.group(1).upper() if m else None

def _parse_numbers(raw: str) -> list[float]:
    """Return [n] or [n1, n2] (range) parsed as floats; [] if none found."""
    m = _NUM_RANGE_PATTERN.search(raw)
    if not m:
        return []
    def to_float(s: str) -> float:
        return float(s.replace(",", "."))
    n1 = to_float(m.group("n1"))
    n2 = m.group("n2")
    return [n1] if not n2 else [min(n1, to_float(n2)), max(n1, to_float(n2))]

def _to_celsius(vals: list[float], unit: str | None) -> list[float]:
    """Convert values to Celsius if unit is 'F'."""
    if not vals:
        return vals
    if unit == "F":
        return [(v - 32.0) * 5.0 / 9.0 for v in vals]
    return vals

def _fmt_c(v: float) -> str:
    """Format a Celsius number with minimal decimals."""
    return str(int(round(v))) if abs(v - round(v)) < 1e-6 else f"{v:.1f}".rstrip("0").rstrip(".")

def _format_range(vals_c: list[float]) -> str:
    """Return '135 °C' or '138–140 °C'."""
    if len(vals_c) == 1:
        return f"{_fmt_c(vals_c[0])} °C"
    return f"{_fmt_c(vals_c[0])}–{_fmt_c(vals_c[1])} °C"

def _norm_key(vals_c: list[float]) -> tuple:
    """
    Deduplication key:
      single -> round to nearest 0.5 °C
      range  -> round both ends to nearest 0.5 °C
    """
    def r05(x: float) -> float:
        return round(x * 2) / 2.0
    if len(vals_c) == 1:
        return ("single", r05(vals_c[0]))
    return ("range", r05(vals_c[0]), r05(vals_c[1]))

# ------------------------------------------------------------------
# PUG endpoints
# ------------------------------------------------------------------

PUG_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUG_VIEW_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view"

def _get(url: str) -> Dict[str, Any]:
    """HTTP GET -> JSON, raising on HTTP errors; uses global timeout/UA."""
    resp = requests.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.json()

# ------------------------------------------------------------------
# PUG-View traversal helpers
# ------------------------------------------------------------------

def _string_from_value(val: Dict[str, Any]) -> Optional[str]:
    """
    Extract a readable string from a PUG-View 'Information.Value' object.
    Observed shapes:
      - {"StringWithMarkup":[{"String":"134-136 °C"}, ...]}
      - {"Number": 134.0, "Unit": "°C"}
      - {"String": "134 °C"}
      - {"Table": {...}}  (ignored)
    """
    if not isinstance(val, dict):
        return None

    swm = val.get("StringWithMarkup")
    if isinstance(swm, list) and swm and isinstance(swm[0], dict):
        s = swm[0].get("String")
        if isinstance(s, str) and s.strip():
            return s.strip()

    s = val.get("String")
    if isinstance(s, str) and s.strip():
        return s.strip()

    if "Number" in val:
        num = val.get("Number")
        unit = val.get("Unit")
        if isinstance(num, (int, float)):
            return f"{num} {unit.strip()}" if isinstance(unit, str) and unit.strip() else str(num)

    return None

def _walk_sections(sections: Iterable[Dict[str, Any]]) -> Iterable[Dict[str, Any]]:
    """Depth-first traversal yielding every section subtree."""
    for sec in sections or []:
        yield sec
        for child in _walk_sections(sec.get("Section") or []):
            yield child

def _collect_melting_texts(view_json: Dict[str, Any]) -> List[str]:
    """
    Find all 'Melting Point' sections and collect textual entries.
    """
    out: List[str] = []
    record = view_json.get("Record") or {}
    top_sections = record.get("Section") or []
    for sec in _walk_sections(top_sections):
        toc = _u(sec.get("TOCHeading"))
        if toc.lower() != "melting point":
            continue
        infos = sec.get("Information") or []
        for info in infos:
            s = _string_from_value(info.get("Value", {}))
            if s:
                out.append(_u(s))
    return out

def _extract_melting_points(view_json: Dict[str, Any]) -> List[MeltingPoint]:
    """
    Normalize/merge melting point strings from PUG-View:
      - extract numbers and unit
      - convert to °C
      - compact ranges
      - deduplicate (≈0.5 °C tolerance)
      - keep parenthetical notes
    """
    texts = _collect_melting_texts(view_json)
    results: List[MeltingPoint] = []
    seen: set[Tuple] = set()

    for raw in texts:
        base, paren_note = _split_notes(raw)
        unit = _extract_unit(base)
        nums = _parse_numbers(base)
        if not nums:
            continue

        vals_c = _to_celsius(nums, unit)
        key = _norm_key(vals_c)
        if key in seen:
            continue
        seen.add(key)

        formatted = _format_range(vals_c)
        notes = paren_note
        if unit == "F":
            notes = f"{(notes + ' ' if notes else '')}[converted from °F]"

        results.append(
            MeltingPoint(
                value=formatted,
                unit="°C",
                source="PubChem",
                notes=notes or None,
            )
        )

    # Stable sort by numeric center (for nicer output)
    def _center(v: str) -> float:
        # quick parse back: "a °C" or "a–b °C"
        core = v.replace(" °C", "")
        if "–" in core:
            a, b = core.split("–", 1)
            return (float(a) + float(b)) / 2.0
        return float(core)

    results.sort(key=lambda mp: _center(mp.value))
    return results

# ------------------------------------------------------------------
# High-level fetch utilities
# ------------------------------------------------------------------

def _fetch_cid_from_smiles(smiles: str) -> Optional[int]:
    encoded = quote(smiles, safe="")
    url = f"{PUG_BASE}/compound/smiles/{encoded}/cids/JSON"
    data = _get(url)
    try:
        return int(data["IdentifierList"]["CID"][0])
    except Exception:
        return None

def _fetch_iupac_from_cid(cid: int) -> Optional[str]:
    url = f"{PUG_BASE}/compound/cid/{cid}/property/IUPACName/JSON"
    data = _get(url)
    try:
        props = data["PropertyTable"]["Properties"][0]
        name = props.get("IUPACName")
        return name.strip() if isinstance(name, str) and name.strip() else None
    except Exception:
        return None
    
def _fetch_title_from_cid(cid: int) -> Optional[str]:
    url = f"{PUG_BASE}/compound/cid/{cid}/property/Title/JSON"
    data = _get(url)
    try:
        props = data["PropertyTable"]["Properties"][0]
        title = props.get("Title")
        return title.strip() if isinstance(title, str) and title.strip() else None
    except Exception:
        return None


def _fetch_view_json(cid: int) -> Dict[str, Any]:
    url = f"{PUG_VIEW_BASE}/data/compound/{cid}/JSON"
    return _get(url)

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def fetch_pubchem_by_smiles(smiles: str) -> Dict[str, Any]:
    cid = _fetch_cid_from_smiles(smiles)
    if cid is None:
        raise ValueError("Could not resolve CID from the provided SMILES.")

    iupac = _fetch_iupac_from_cid(cid)
    title = _fetch_title_from_cid(cid)        
    view = _fetch_view_json(cid)
    mps = _extract_melting_points(view)

    return {
        "cid": cid,
        "title": title,                        
        "iupac_name": iupac,
        "melting_points": [asdict(mp) for mp in mps],
        "sources": {
            "pubchem_cid": f"{PUG_BASE}/compound/smiles/{quote(smiles, safe='')}/cids/JSON",
            "pubchem_property": f"{PUG_BASE}/compound/cid/{cid}/property/IUPACName/JSON",
            "pubchem_title": f"{PUG_BASE}/compound/cid/{cid}/property/Title/JSON",  
            "pubchem_view": f"{PUG_VIEW_BASE}/data/compound/{cid}/JSON",
        },
    }

def resolve(smiles: str) -> Result:
    cid = _fetch_cid_from_smiles(smiles)
    if cid is None:
        raise ValueError("Could not resolve CID from the provided SMILES.")

    iupac = _fetch_iupac_from_cid(cid)
    title = _fetch_title_from_cid(cid)        
    view = _fetch_view_json(cid)
    melting_points = _extract_melting_points(view)

    sources = {
        "pubchem_cid": f"{PUG_BASE}/compound/smiles/{quote(smiles, safe='')}/cids/JSON",
        "pubchem_property": f"{PUG_BASE}/compound/cid/{cid}/property/IUPACName/JSON",
        "pubchem_title": f"{PUG_BASE}/compound/cid/{cid}/property/Title/JSON",      
        "pubchem_view": f"{PUG_VIEW_BASE}/data/compound/{cid}/JSON",
    }

    return Result(
        input_smiles=smiles,
        cid=cid,
        iupac_name=iupac,
        preferred_name=title,                  
        melting_points=melting_points,
        sources=sources,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )

