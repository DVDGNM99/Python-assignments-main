# src/models.py
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

@dataclass
class MeltingPoint:
    value: Optional[float]          # in Celsius if possible if not none
    unit: Optional[str]             # es. "°C", "K" (just as it was fetched)
    notes: Optional[str] = None     # commenti/condizioni riportate dalla fonte
    source_url: Optional[str] = None

@dataclass
class Result:
    input_smiles: str
    cid: Optional[int] = None
    iupac_name: Optional[str] = None
    melting_points: List[MeltingPoint] = field(default_factory=list)
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sources: List[str] = field(default_factory=list)  # URL visitated
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_smiles": self.input_smiles,
            "cid": self.cid,
            "iupac_name": self.iupac_name,
            "melting_points": [vars(mp) for mp in self.melting_points],
            "fetched_at": self.fetched_at.isoformat(),
            "sources": list(self.sources),
            "errors": list(self.errors),
        }
