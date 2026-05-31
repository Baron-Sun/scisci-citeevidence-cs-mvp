from __future__ import annotations

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from citeevidence.final_release.figures import plot_object_role_signature_map
from citeevidence.final_release.metrics import (
    build_object_role_signature,
    classify_object_role_quadrant,
)


def _role_map_data() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    specs = [
        ("bert", "BERT", "method", {"background": 80, "uses": 20}),
        ("moses", "Moses", "software_or_tool", {"background": 5, "uses": 30}),
        ("bleu", "BLEU", "metric", {"background": 5, "compares_against": 25}),
        ("critic", "CriticalBenchmark", "benchmark_or_protocol", {"critiques": 15, "uses": 5}),
    ]
    for object_id, canonical_name, object_type, intent_counts in specs:
        for intent, count in intent_counts.items():
            for index in range(count):
                rows.append(
                    {
                        "object_id": object_id,
                        "canonical_name": canonical_name,
                        "object_type": object_type,
                        "final_intent": intent,
                        "context_id": f"{object_id}-{intent}-{index}",
                        "evidence_span": f"{canonical_name} {intent} {index}",
                        "confidence": 0.82,
                    }
                )
    return classify_object_role_quadrant(build_object_role_signature(pd.DataFrame(rows)))


def test_object_role_signature_map_writes_png_and_svg(tmp_path) -> None:
    png = tmp_path / "object_role_signature_map.png"
    svg = tmp_path / "object_role_signature_map.svg"

    outputs = plot_object_role_signature_map(_role_map_data(), png, svg)

    assert outputs["png"] == str(png)
    assert outputs["svg"] == str(svg)
    assert png.exists()
    assert svg.exists()
    assert png.stat().st_size > 0
    assert svg.stat().st_size > 0


def test_object_role_signature_map_wording_avoids_all_nlp_objects(tmp_path) -> None:
    outputs = plot_object_role_signature_map(
        _role_map_data(),
        tmp_path / "object_role_signature_map.png",
    )
    visible_text = " ".join([outputs["title"], outputs["x_label"], outputs["y_label"]])

    assert "all nlp objects" not in visible_text.casefold()
    assert "seed-registry objects" in outputs["title"].casefold()


def test_object_role_signature_map_does_not_require_local_parquet_files(
    monkeypatch,
    tmp_path,
) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("object figure should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    outputs = plot_object_role_signature_map(
        _role_map_data(),
        tmp_path / "object_role_signature_map.png",
    )

    assert outputs["png"]
    assert "BERT" in outputs["plotted_objects"]
