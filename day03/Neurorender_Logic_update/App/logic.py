"""
Pure business logic for region loading/validation and color handling.
No GUI, no brainrender imports here. Safe to unit-test.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple, Dict
import json
import re
import itertools

# ---------------- Exceptions ---------------- #

class LogicError(Exception):
    """Base logic error."""

class InvalidJSON(LogicError):
    """regions.json invalid or unsupported structure."""

class EmptyRegions(LogicError):
    """No regions could be parsed from the JSON."""

# ---------------- Models ---------------- #

@dataclass(frozen=True)
class RegionItem:
    acronym: str
    name: str

    @property
    def display(self) -> str:
        # Human-friendly combined label
        return f"{self.acronym} — {self.name}"

# ---------------- JSON Loading ---------------- #

def _coerce_region_obj(obj: Dict) -> RegionItem:
    """
    Accepts flexible keys like:
      {"acronym": "MOs", "name": "Secondary motor area"}
      {"acr": "MOs", "label": "Secondary motor area"}
    """
    # Liberal key lookup
    a = obj.get("acronym") or obj.get("acr") or obj.get("code")
    n = obj.get("name") or obj.get("label") or obj.get("fullname")
    if not a or not n:
        raise InvalidJSON("Missing 'acronym'/'name' (or aliases) in region object.")
    a = str(a).strip()
    n = str(n).strip()
    return RegionItem(acronym=a, name=n)

def load_regions_from_json(json_path: str | Path) -> List[RegionItem]:
    """
    Supports two shapes:
      1) {"MOs": "Secondary motor area", "VISp": "Primary visual area", ...}
      2) [{"acronym":"MOs","name":"Secondary motor area"}, ...]
    Deduplicates by acronym; preserves first name seen.
    """
    p = Path(json_path)
    if not p.exists():
        raise InvalidJSON(f"File not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise InvalidJSON(f"Cannot parse JSON: {e}") from e

    items: List[RegionItem] = []
    if isinstance(data, dict):
        for acr, name in data.items():
            if acr and name:
                items.append(RegionItem(acronym=str(acr).strip(), name=str(name).strip()))
    elif isinstance(data, list):
        for obj in data:
            if not isinstance(obj, dict):
                raise InvalidJSON("List form must contain objects.")
            items.append(_coerce_region_obj(obj))
    else:
        raise InvalidJSON("Unsupported JSON root (must be object or array).")

    # Deduplicate by acronym (keep first occurrence)
    seen = set()
    deduped: List[RegionItem] = []
    for it in items:
        if it.acronym not in seen:
            deduped.append(it)
            seen.add(it.acronym)

    if not deduped:
        raise EmptyRegions("No valid regions found in JSON.")
    # Sort by acronym for stable UI
    deduped.sort(key=lambda r: r.acronym.upper())
    return deduped

# ---------------- Validation vs atlas structures ---------------- #

def validate_acronyms(
    acronyms: Iterable[str],
    atlas_structures: Iterable[str],
) -> Tuple[List[str], List[str]]:
    """
    Split input acronyms into (valid, invalid) based on atlas structures.
    """
    atlas_set = {str(s).strip() for s in atlas_structures}
    valid, invalid = [], []
    for a in acronyms:
        a_norm = str(a).strip()
        (valid if a_norm in atlas_set else invalid).append(a_norm)
    return valid, invalid

# ---------------- Color utilities ---------------- #

_HEX_RE = re.compile(r"^#([0-9A-Fa-f]{6})$")

# A small, readable default palette (can be extended)
_DEFAULT_COLORS = [
    "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e",
    "#9467bd", "#8c564b", "#17becf", "#7f7f7f",
    "#bcbd22", "#e377c2",
]

def normalize_hex(color: str) -> str:
    """
    Ensure color is a #RRGGBB hex. Raise ValueError otherwise.
    """
    c = str(color).strip()
    if not _HEX_RE.match(c):
        raise ValueError(f"Invalid hex color: {color!r} (expected #RRGGBB)")
    return c.lower()

def cycle_colors(n: int) -> List[str]:
    """
    Return n colors cycling over the default list.
    """
    if n <= 0:
        return []
    return list(itertools.islice(itertools.cycle(_DEFAULT_COLORS), n))

# ---------------- Selections ---------------- #

def selection_from_display(display: str) -> str:
    """
    Extract acronym from 'ACR — Name' display string.
    """
    if not display:
        raise ValueError("Empty display string.")
    parts = [p.strip() for p in display.split("—", 1)]
    if not parts or not parts[0]:
        raise ValueError(f"Cannot extract acronym from: {display!r}")
    return parts[0]

def prepare_render_inputs(
    selected_displays: List[str],
    custom_colors: List[str] | None,
    alpha: float,
) -> Tuple[List[str], List[str], float]:
    """
    Normalize user selections and colors for renderer:
      - extract acronyms from display strings
      - normalize or auto-generate colors to match len(acronyms)
      - validate alpha in [0, 1]
    """
    if not (0.0 <= alpha <= 1.0):
        raise ValueError("alpha must be in [0, 1].")

    acronyms = [selection_from_display(d) for d in selected_displays]

    if custom_colors:
        colors = [normalize_hex(c) for c in custom_colors]
        if len(colors) != len(acronyms):
            raise ValueError("Colors length must match selected regions.")
    else:
        colors = cycle_colors(len(acronyms))

    return acronyms, colors, float(alpha)
