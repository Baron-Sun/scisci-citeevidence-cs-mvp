from __future__ import annotations

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from citeevidence.final_release.figures import plot_section_function_lift_heatmap
from citeevidence.final_release.metrics import (
    build_section_function_counts,
    build_section_function_lift,
)


def _lift_data() -> pd.DataFrame:
    labels = pd.DataFrame(
        [
            *[
                {"normalized_section": "methods", "final_intent": "uses"}
                for _ in range(8)
            ],
            *[
                {"normalized_section": "methods", "final_intent": "background"}
                for _ in range(2)
            ],
            *[
                {"normalized_section": "introduction", "final_intent": "background"}
                for _ in range(8)
            ],
            *[
                {"normalized_section": "introduction", "final_intent": "uses"}
                for _ in range(2)
            ],
            {"normalized_section": "", "final_intent": "critiques"},
            {"normalized_section": None, "final_intent": "critiques"},
        ]
    )
    counts = build_section_function_counts(labels)
    return build_section_function_lift(counts, min_section_total=1)


def test_section_function_lift_heatmap_writes_png_and_svg(tmp_path) -> None:
    png = tmp_path / "section_function_lift.png"
    svg = tmp_path / "section_function_lift.svg"

    outputs = plot_section_function_lift_heatmap(_lift_data(), png, svg)

    assert outputs["png"] == str(png)
    assert outputs["svg"] == str(svg)
    assert png.exists()
    assert svg.exists()
    assert png.stat().st_size > 0
    assert svg.stat().st_size > 0


def test_section_function_lift_heatmap_excludes_unknown_by_default(tmp_path) -> None:
    outputs = plot_section_function_lift_heatmap(
        _lift_data(),
        tmp_path / "section_function_lift.png",
    )

    assert "unknown" not in outputs["plotted_sections"].split("|")


def test_section_function_lift_heatmap_can_include_unknown(tmp_path) -> None:
    outputs = plot_section_function_lift_heatmap(
        _lift_data(),
        tmp_path / "section_function_lift_with_unknown.png",
        include_unknown=True,
    )

    assert "unknown" in outputs["plotted_sections"].split("|")


def test_section_function_lift_heatmap_does_not_require_local_parquet_files(
    monkeypatch,
    tmp_path,
) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("section figure should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    outputs = plot_section_function_lift_heatmap(
        _lift_data(),
        tmp_path / "section_function_lift.png",
    )

    assert outputs["png"]
