"""Pure metric helpers for future final-release analyses."""

from __future__ import annotations


def safe_rate(numerator: int | float, denominator: int | float) -> float:
    """Return a numeric rate with zero-denominator protection."""
    return float(numerator / denominator) if denominator else 0.0
