# src/config.py
from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # load environment variables from a .env file if present

DEFAULT_USER_AGENT = "Chem-Reporter/0.1 (+https://example.local)"
DEFAULT_TIMEOUT = 20  # secondi

@dataclass(frozen=True)
class Settings:
    http_timeout: int = int(os.getenv("HTTP_TIMEOUT", DEFAULT_TIMEOUT))
    user_agent: str = os.getenv("USER_AGENT", DEFAULT_USER_AGENT)
    pubchem_base: str = os.getenv("PUBCHEM_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug")
    pugview_base: str = os.getenv("PUGVIEW_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view")

    @classmethod
    def load(cls) -> "Settings":
        # in the future, we could add validation here
        return cls()

settings = Settings.load()

# -- expose runtime config expected by other modules --


USER_AGENT = os.getenv("USER_AGENT", DEFAULT_USER_AGENT)
HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", DEFAULT_TIMEOUT))

