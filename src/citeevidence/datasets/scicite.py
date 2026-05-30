from __future__ import annotations

from pathlib import Path

import pandas as pd

from citeevidence.datasets.normalize import load_labeled_records


def load_scicite(root: str | Path) -> pd.DataFrame:
    """Load and normalize SciCite labeled citation contexts."""
    return load_labeled_records(root, dataset_name="scicite", label_source="scicite_gold")
