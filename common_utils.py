"""Shared utilities used by the educational scripts.

Contains reusable functions such as `parse_positive_number` to avoid duplication.
"""
from __future__ import annotations


def parse_positive_number(s: str) -> float:
    """Parses a string into a float number, accepting either ',' or '.' as the decimal separator.

    Raises ValueError if the string is not a valid number or if the value is <= 0.
    """
    try:
        v = float(s.replace(',', '.'))
    except Exception:
        raise ValueError(f"'{s}' is not a valid number")
    if v <= 0:
        raise ValueError("The value must be greater than zero")
    return v