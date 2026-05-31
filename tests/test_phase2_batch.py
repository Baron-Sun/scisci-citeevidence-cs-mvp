from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from citeevidence.phase2 import (
    check_phase2_batch_status,
    collect_phase2_batch_results,
    estimate_phase2_batch_cost,
    phase2_batch_custom_id,
    prepare_phase2_batch_requests,
    submit_phase2_batch,
)


def _queue_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "context_id": "ctx1",
                "sentence_text": "We use BERT as the encoder.",
                "context_window_s3": "We use BERT as the encoder.",
                "resolved_cited_title": "BERT",
                "primary_candidate_intent": "uses",
                "candidate_intents": "uses",
                "evidence_span": "use BERT",
                "confidence": 0.9,
                "llm_priority": "high",
                "llm_reason": "test",
                "phase2_candidate_type": "explicit_current_paper_relation",
                "object_names": "BERT",
                "object_types": "model",
                "graph_candidate_object_names": "BERT",
                "primary_candidate_object_type": "model",
                "object_type_source": "object_graph_candidate",
                "object_type_confidence": 0.95,
                "candidate_relation_subtypes": "direct_use",
                "matched_rules": "current_paper_use_cue",
            },
            {
                "context_id": "ctx2",
                "sentence_text": "BLEU does not capture meaning.",
                "context_window_s3": "BLEU does not capture meaning.",
                "resolved_cited_title": "BLEU",
                "primary_candidate_intent": "critiques",
                "candidate_intents": "critiques",
                "evidence_span": "does not capture",
                "confidence": 0.8,
                "llm_priority": "high",
                "llm_reason": "test",
                "phase2_candidate_type": "critique",
                "object_names": "BLEU",
                "object_types": "metric",
                "graph_candidate_object_names": "BLEU",
                "primary_candidate_object_type": "metric",
                "object_type_source": "object_graph_candidate",
                "object_type_confidence": 0.95,
                "candidate_relation_subtypes": "critique_limitation",
                "matched_rules": "critique_cue",
            },
        ]
    )


def _valid_batch_line(custom_id: str = "phase2:ctx1:phase2_test") -> str:
    body = {
        "id": "resp_1",
        "output_text": json.dumps(
            {
                "final_intent": "uses",
                "final_object_type": "model",
                "final_relation_subtype": "direct_use",
                "method_edge_type": "uses_component",
                "stance": "neutral",
                "evidence_span": "use BERT as the encoder",
                "problem_or_motivation_quote": None,
                "usage_or_mechanism_quote": "use BERT as the encoder",
                "comparison_or_tradeoff_quote": None,
                "evidence_supports_label": "true",
                "abstain": False,
                "abstain_reason": "null",
                "confidence": 0.9,
                "rationale_short": "The current paper says it uses BERT.",
            }
        ),
        "usage": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120},
    }
    return json.dumps(
        {
            "custom_id": custom_id,
            "response": {"status_code": 200, "body": body},
        }
    )


def test_prepare_batch_generates_jsonl_and_manifest(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.parquet"
    _queue_rows().to_parquet(queue_path, index=False)

    manifest = prepare_phase2_batch_requests(
        queue_paths=[queue_path],
        out_jsonl_path=tmp_path / "requests.jsonl",
        manifest_path=tmp_path / "manifest.json",
        candidates_path=None,
        contexts_path=None,
        object_mentions_path=None,
        object_graph_candidates_path=None,
        cited_title_profiles_path=None,
        model="gpt-5.4-mini",
        prompt_version="phase2_test",
        max_requests_per_file=1,
    )

    assert manifest["total_rows"] == 2
    assert len(manifest["request_files"]) == 2
    first = json.loads(Path(manifest["request_files"][0]["path"]).read_text().splitlines()[0])
    assert first["custom_id"] == "phase2:ctx1:phase2_test"
    assert first["url"] == "/v1/responses"
    assert first["body"]["model"] == "gpt-5.4-mini"
    assert first["body"]["text"]["format"]["type"] == "json_schema"


def test_custom_id_is_deterministic() -> None:
    row = {"context_id": "ctx1", "prompt_version": "phase2_test"}
    assert phase2_batch_custom_id(row) == "phase2:ctx1:phase2_test"


def test_collect_batch_parses_valid_and_failed_rows(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.parquet"
    output_path = tmp_path / "batch_output.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _queue_rows().to_parquet(queue_path, index=False)
    bad_line = json.dumps(
        {
            "custom_id": "phase2:ctx2:phase2_test",
            "response": {
                "status_code": 200,
                "body": {
                    "id": "resp_2",
                    "output_text": json.dumps(
                        {
                            "final_intent": "critiques",
                            "final_object_type": "metric",
                            "final_relation_subtype": "critique_limitation",
                            "method_edge_type": "not_method_related",
                            "stance": "negative",
                            "evidence_span": "not an exact span",
                            "problem_or_motivation_quote": None,
                            "usage_or_mechanism_quote": None,
                            "comparison_or_tradeoff_quote": None,
                            "evidence_supports_label": "true",
                            "abstain": False,
                            "abstain_reason": "null",
                            "confidence": 0.8,
                            "rationale_short": "Invalid evidence span.",
                        }
                    ),
                },
            },
        }
    )
    output_path.write_text(_valid_batch_line() + "\n" + bad_line + "\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(
            {
                "model": "gpt-5.4-mini",
                "prompt_version": "phase2_test",
                "request_files": [
                    {
                        "path": str(tmp_path / "requests.jsonl"),
                        "batch_id": "batch_1",
                        "output_path": str(output_path),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    metrics = collect_phase2_batch_results(
        manifest_path=manifest_path,
        queue_paths=[queue_path],
        out_labels_path=tmp_path / "labels.parquet",
        out_failed_path=tmp_path / "failed.jsonl",
        report_path=tmp_path / "report.md",
    )

    labels = pd.read_parquet(tmp_path / "labels.parquet")
    failed_lines = (tmp_path / "failed.jsonl").read_text(encoding="utf-8").splitlines()
    assert metrics["successful_rows"] == 1
    assert labels.iloc[0]["context_id"] == "ctx1"
    assert len(failed_lines) == 1
    assert "evidence_span" in failed_lines[0]


def test_collect_batch_records_missing_output_rows(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.parquet"
    output_path = tmp_path / "batch_output.jsonl"
    manifest_path = tmp_path / "manifest.json"
    _queue_rows().to_parquet(queue_path, index=False)
    output_path.write_text(_valid_batch_line() + "\n", encoding="utf-8")
    manifest_path.write_text(
        json.dumps(
            {
                "model": "gpt-5.4-mini",
                "prompt_version": "phase2_test",
                "request_files": [
                    {
                        "path": str(tmp_path / "requests.jsonl"),
                        "batch_id": "batch_1",
                        "output_path": str(output_path),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    metrics = collect_phase2_batch_results(
        manifest_path=manifest_path,
        queue_paths=[queue_path],
        out_labels_path=tmp_path / "labels.parquet",
        out_failed_path=tmp_path / "failed.jsonl",
        report_path=tmp_path / "report.md",
    )

    failed_text = (tmp_path / "failed.jsonl").read_text(encoding="utf-8")
    assert metrics["processed_rows"] == 2
    assert metrics["missing_batch_output_rows"] == 1
    assert "missing_batch_output" in failed_text


def test_cost_estimate_uses_pilot_averages(tmp_path: Path) -> None:
    queue_path = tmp_path / "queue.parquet"
    pilot_path = tmp_path / "pilot.parquet"
    _queue_rows().to_parquet(queue_path, index=False)
    pd.DataFrame(
        [{"input_tokens": 100, "output_tokens": 20}, {"input_tokens": 200, "output_tokens": 40}]
    ).to_parquet(pilot_path, index=False)

    metrics = estimate_phase2_batch_cost(
        queue_paths=[queue_path],
        out_report_path=tmp_path / "cost.md",
        model="gpt-5.4-mini",
        pilot_labels_path=pilot_path,
    )

    assert metrics["total_rows"] == 2
    assert metrics["input_tokens_per_row"] == 150
    assert metrics["output_tokens_per_row"] == 30
    assert (tmp_path / "cost.md").exists()


class _FakeObject:
    def __init__(self, **kwargs: object) -> None:
        self.__dict__.update(kwargs)

    def model_dump(self) -> dict[str, object]:
        return dict(self.__dict__)


class _FakeFiles:
    def __init__(self) -> None:
        self.created = 0

    def create(self, **_: object) -> _FakeObject:
        self.created += 1
        return _FakeObject(id=f"file_{self.created}")


class _FakeBatches:
    def __init__(self) -> None:
        self.created = 0

    def create(self, **kwargs: object) -> _FakeObject:
        self.created += 1
        return _FakeObject(
            id=f"batch_{self.created}",
            status="validating",
            input_file_id=kwargs["input_file_id"],
        )

    def retrieve(self, batch_id: str) -> _FakeObject:
        return _FakeObject(
            id=batch_id,
            status="completed",
            output_file_id=f"output_{batch_id}",
            error_file_id=None,
            request_counts={"total": 1, "completed": 1, "failed": 0},
        )


class _FakeClient:
    def __init__(self) -> None:
        self.files = _FakeFiles()
        self.batches = _FakeBatches()


def test_submit_and_check_use_fake_client(tmp_path: Path) -> None:
    request_path = tmp_path / "requests.jsonl"
    manifest_path = tmp_path / "manifest.json"
    request_path.write_text(_valid_batch_line(), encoding="utf-8")
    manifest_path.write_text(
        json.dumps({"request_files": [{"path": str(request_path), "rows": 1}]}),
        encoding="utf-8",
    )
    client = _FakeClient()

    submitted = submit_phase2_batch(
        manifest_path=manifest_path,
        status_out_path=tmp_path / "status.json",
        client=client,
    )
    checked = check_phase2_batch_status(
        manifest_path=manifest_path,
        status_out_path=tmp_path / "status2.json",
        client=client,
    )

    assert submitted["status_distribution"] == {"completed": 1}
    assert checked["status_distribution"] == {"completed": 1}
