from pathlib import Path

import pandas as pd

from citeevidence.final_release.io import ensure_directory, maybe_read_csv, write_source_csv


def test_maybe_read_csv_returns_none_for_missing_source(tmp_path: Path) -> None:
    assert maybe_read_csv(tmp_path / "missing.csv") is None


def test_write_source_csv_creates_parent_directory_and_round_trips(tmp_path: Path) -> None:
    frame = pd.DataFrame([{"claim_id": "C1", "value": 1}])
    out_path = write_source_csv(frame, tmp_path / "source" / "claims.csv")

    assert out_path == tmp_path / "source" / "claims.csv"
    assert out_path.exists()
    assert maybe_read_csv(out_path).to_dict(orient="records") == [
        {"claim_id": "C1", "value": 1}
    ]


def test_ensure_directory_does_not_create_generated_report_artifacts(tmp_path: Path) -> None:
    directory = ensure_directory(tmp_path / "nested" / "source_data")

    assert directory.is_dir()
    assert list(directory.iterdir()) == []
