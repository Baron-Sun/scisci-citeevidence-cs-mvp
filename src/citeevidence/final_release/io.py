"""Small IO helpers for final-release source-data artifacts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if needed and return it as a ``Path``."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def maybe_read_csv(path: str | Path) -> pd.DataFrame | None:
    """Read a CSV when present, returning ``None`` for missing inputs."""
    csv_path = Path(path)
    if not csv_path.exists():
        return None
    try:
        return pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def write_source_csv(frame: pd.DataFrame, path: str | Path) -> Path:
    """Write a small reproducibility source CSV and return the output path."""
    csv_path = Path(path)
    ensure_directory(csv_path.parent)
    frame.to_csv(csv_path, index=False)
    return csv_path
