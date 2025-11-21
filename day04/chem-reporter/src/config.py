# src/config.py
from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if present

# ------------------------------------------------------------------
# Network settings
# ------------------------------------------------------------------
# - Increase TIMEOUT_SECONDS if your network is slow or PubChem is laggy.
# - USER_AGENT is sent with every HTTP request; keep it informative.
TIMEOUT_SECONDS = 15
USER_AGENT = "Chem-Reporter/1.0 (Windows; Tkinter)"

# Backward compatibility with older code
HTTP_TIMEOUT = TIMEOUT_SECONDS
DEFAULT_TIMEOUT = TIMEOUT_SECONDS  # <-- add this to avoid NameError

# ------------------------------------------------------------------
# Dataclass-based configuration (optional but kept for clarity)
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Settings:
    http_timeout: int = int(os.getenv("HTTP_TIMEOUT", TIMEOUT_SECONDS))
    user_agent: str = os.getenv("USER_AGENT", USER_AGENT)
    pubchem_base: str = os.getenv("PUBCHEM_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug")
    pugview_base: str = os.getenv("PUGVIEW_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view")

    @classmethod
    def load(cls) -> "Settings":
        # Future: validation or .env schema
        return cls()

settings = Settings.load()

# expose runtime config expected by other modules
USER_AGENT = settings.user_agent
TIMEOUT_SECONDS = settings.http_timeout
HTTP_TIMEOUT = settings.http_timeout
# ------------------------------------------------------------------
# Developer note:
# TIMEOUT_SECONDS and USER_AGENT are global defaults used by all
# network utilities. Change them here if needed.
# Settings dataclass provides optional .env overrides for advanced use.
# ------------------------------------------------------------------
