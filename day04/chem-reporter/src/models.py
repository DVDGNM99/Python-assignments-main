# src/models.py
# src/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

@dataclass
class MeltingPoint:
    # Keep textual value (may contain ranges/notes like "134–136 °C")
    value: Optional[str]
    unit: Optional[str] = None          # often empty because unit is in value
    source: str = "PubChem PUG-View"
    notes: Optional[str] = None
    source_url: Optional[str] = None    # optional, for future use

@dataclass
class Result:
    input_smiles: str
    cid: Optional[int] = None
    iupac_name: Optional[str] = None
    melting_points: List[MeltingPoint] = field(default_factory=list)

    # Match what pubchem.resolve builds (created_at as ISO string; sources as dict)
    sources: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Keep optional diagnostics compatible with existing code
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_smiles": self.input_smiles,
            "cid": self.cid,
            "iupac_name": self.iupac_name,
            "melting_points": [vars(mp) for mp in self.melting_points],
            "created_at": self.created_at,
            "sources": dict(self.sources),
            "errors": list(self.errors),
        }
