"""Utility condivise usate dagli script didattici.

Contiene funzioni riutilizzabili come `parse_positive_number` per evitare duplicazione.
"""
from __future__ import annotations


def parse_positive_number(s: str) -> float:
    """Parsa una stringa in numero float accettando ',' o '.' come separatore.

    Solleva ValueError se la stringa non è un numero valido o se il valore è <= 0.
    """
    try:
        v = float(s.replace(',', '.'))
    except Exception:
        raise ValueError(f"'{s}' non è un numero valido")
    if v <= 0:
        raise ValueError("Il valore deve essere maggiore di zero")
    return v
