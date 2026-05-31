from __future__ import annotations

import pandas as pd

from citeevidence.final_release.metrics import (
    build_object_role_signature,
    classify_object_role_quadrant,
)


def _rows_for_object(
    object_id: str,
    canonical_name: str,
    object_type: str,
    intent_counts: dict[str, int],
    *,
    confidence: float | None = 0.84,
) -> list[dict[str, object]]:
    rows = []
    for intent, count in intent_counts.items():
        for index in range(count):
            rows.append(
                {
                    "object_id": object_id,
                    "canonical_name": canonical_name,
                    "object_type": object_type,
                    "final_intent": intent,
                    "context_id": f"{object_id}-{intent}-{index}",
                    "evidence_span": f"{canonical_name} {intent} evidence {index}",
                    "confidence": confidence,
                    "normalized_section": "methods",
                }
            )
    return rows


def _object_edges() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    rows.extend(
        _rows_for_object(
            "bert",
            "BERT",
            "method",
            {"background": 80, "uses": 20},
        )
    )
    rows.extend(
        _rows_for_object(
            "moses",
            "Moses",
            "software_or_tool",
            {"background": 5, "uses": 30, "applies": 10},
        )
    )
    rows.extend(
        _rows_for_object(
            "bleu",
            "BLEU",
            "metric",
            {"background": 5, "compares_against": 20, "uses": 5},
        )
    )
    rows.extend(
        _rows_for_object(
            "critique",
            "FragileBenchmark",
            "benchmark_or_protocol",
            {"background": 2, "critiques": 12, "uses": 4},
        )
    )
    rows.extend(
        _rows_for_object(
            "background_only",
            "BackgroundOnly",
            "theory_or_concept",
            {"background": 5},
        )
    )
    rows.extend(
        _rows_for_object(
            "no_confidence",
            "NoConfidenceTool",
            "software_or_tool",
            {"uses": 2},
            confidence=None,
        )
    )
    duplicate = next(
        row
        for row in rows
        if row["object_id"] == "moses" and row["final_intent"] == "uses"
    ).copy()
    duplicate["evidence_span"] = "duplicate text should not inflate context-object-intent"
    rows.append(duplicate)
    rows.extend(
        [
            {"object_id": "", "canonical_name": "MissingObject", "final_intent": "uses"},
            {"object_id": "missing_name", "canonical_name": "", "final_intent": "uses"},
            {"object_id": "empty_intent", "canonical_name": "EmptyIntent", "final_intent": ""},
        ]
    )
    return pd.DataFrame(rows)


def _classified_signatures() -> pd.DataFrame:
    return classify_object_role_quadrant(build_object_role_signature(_object_edges()))


def test_background_is_excluded_from_evidence_use_count() -> None:
    table = build_object_role_signature(_object_edges())
    bert = table.loc[table["object_id"].eq("bert")].iloc[0]

    assert bert["background_edges"] == 80
    assert bert["evidence_use_count"] == 20
    assert bert["non_background_edges"] == 20
    assert bert["total_edges"] == 100
    assert bert["background_share"] == 0.8


def test_duplicate_context_object_intent_rows_do_not_inflate_counts() -> None:
    table = build_object_role_signature(_object_edges())
    moses = table.loc[table["object_id"].eq("moses")].iloc[0]

    assert moses["uses_count"] == 30
    assert moses["applies_count"] == 10
    assert moses["evidence_use_count"] == 40
    assert moses["distinct_contexts"] == 45


def test_zero_non_background_edges_do_not_crash() -> None:
    table = _classified_signatures()
    background_only = table.loc[table["object_id"].eq("background_only")].iloc[0]

    assert background_only["non_background_edges"] == 0
    assert background_only["use_share_non_background"] == 0
    assert background_only["compare_critique_share_non_background"] == 0
    assert background_only["critique_share_non_background"] == 0
    assert background_only["role_quadrant"] == "mixed_role"


def test_bert_like_background_heavy_object_gets_canonical_background() -> None:
    table = _classified_signatures()
    bert = table.loc[table["object_id"].eq("bert")].iloc[0]

    assert bert["role_quadrant"] == "canonical_background"
    assert bert["role_quadrant_rule_version"] == "v1_heuristic"


def test_moses_like_use_heavy_object_gets_operational_infrastructure() -> None:
    table = _classified_signatures()
    moses = table.loc[table["object_id"].eq("moses")].iloc[0]

    assert moses["role_quadrant"] == "operational_infrastructure"


def test_bleu_like_compare_heavy_object_gets_evaluation_anchor() -> None:
    table = _classified_signatures()
    bleu = table.loc[table["object_id"].eq("bleu")].iloc[0]

    assert bleu["role_quadrant"] == "evaluation_anchor"


def test_critique_heavy_object_gets_critique_target() -> None:
    table = _classified_signatures()
    critique = table.loc[table["object_id"].eq("critique")].iloc[0]

    assert critique["role_quadrant"] == "critique_target"


def test_missing_confidence_produces_missing_mean_confidence() -> None:
    table = build_object_role_signature(_object_edges())
    no_confidence = table.loc[table["object_id"].eq("no_confidence")].iloc[0]

    assert pd.isna(no_confidence["mean_confidence"])


def test_object_metrics_do_not_require_local_parquet_files(monkeypatch) -> None:
    def fail_read_parquet(*_: object, **__: object) -> None:
        raise AssertionError("object metrics should use provided DataFrames")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    table = classify_object_role_quadrant(build_object_role_signature(_object_edges()))

    assert not table.empty
