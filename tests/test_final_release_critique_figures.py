from __future__ import annotations

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from citeevidence.final_release.figures import plot_critique_bottleneck_heatmap
from citeevidence.final_release.metrics import build_critique_bottleneck_matrix


def _critique_matrix() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    specs = [
        ("method", "BERT", "bert", "BLEU does not capture human judgment.", 4),
        ("method", "BERT", "bert", "Fails on out-of-domain transfer.", 3),
        ("dataset_or_database", "Treebank", "treebank", "Requires annotated data.", 4),
        ("dataset_or_database", "Treebank", "treebank", "The annotation is expensive.", 2),
        ("software_or_tool", "Toolkit", "toolkit", "The implementation code is unavailable.", 5),
    ]
    context_index = 0
    for object_type, name, object_id, evidence_span, count in specs:
        for _ in range(count):
            rows.append(
                {
                    "final_intent": "critiques",
                    "object_type": object_type,
                    "canonical_name": name,
                    "object_id": object_id,
                    "evidence_span": evidence_span,
                    "context_id": f"c{context_index}",
                    "confidence": 0.8,
                    "normalized_section": "limitations",
                }
            )
            context_index += 1
    return build_critique_bottleneck_matrix(pd.DataFrame(rows))


def test_critique_bottleneck_heatmap_writes_png_and_svg(tmp_path) -> None:
    png = tmp_path / "critique_bottleneck_heatmap.png"
    svg = tmp_path / "critique_bottleneck_heatmap.svg"

    outputs = plot_critique_bottleneck_heatmap(_critique_matrix(), png, svg)

    assert outputs["png"] == str(png)
    assert outputs["svg"] == str(svg)
    assert png.exists()
    assert svg.exists()
    assert png.stat().st_size > 0
    assert svg.stat().st_size > 0


def test_critique_bottleneck_heatmap_uses_exploratory_heuristic_wording(tmp_path) -> None:
    outputs = plot_critique_bottleneck_heatmap(
        _critique_matrix(),
        tmp_path / "critique_bottleneck_heatmap.png",
    )

    assert "exploratory" in outputs["title"].casefold()
    assert "heuristic" in outputs["caveat"].casefold()
    assert "not a validated bottleneck taxonomy" in outputs["caveat"].casefold()


def test_critique_bottleneck_heatmap_does_not_require_local_parquet_files(
    monkeypatch,
    tmp_path,
) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("critique figure should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    outputs = plot_critique_bottleneck_heatmap(
        _critique_matrix(),
        tmp_path / "critique_bottleneck_heatmap.png",
    )

    assert outputs["png"].startswith(str(tmp_path))
    assert "method" in outputs["plotted_object_types"].split("|")
