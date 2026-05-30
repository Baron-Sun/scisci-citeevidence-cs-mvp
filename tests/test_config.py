from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from citeevidence.cli import app
from citeevidence.config import load_label_config, load_project_config


def test_project_config_loads() -> None:
    config = load_project_config(Path("configs/project.yaml"))

    assert config.project_title == "From Citation Counts to Citation Evidence"
    assert config.domain == "NLP / Computational Linguistics"
    assert config.target_contexts_min == 10000
    assert config.target_contexts_max == 50000
    assert config.max_llm_labels == 5000
    assert config.max_human_validation == 500
    assert config.datasets.labeled == ["multicite", "scicite"]
    assert config.datasets.unlabeled_large_scale == ["acl_ocl"]
    assert config.datasets.optional_extension == ["unarxive"]


def test_label_config_loads() -> None:
    labels = load_label_config(Path("configs/labels.yaml"))

    assert "background" in labels.intent
    assert "method" in labels.object_type
    assert "direct_use" in labels.relation_subtype
    assert "not_method_related" in labels.method_edge_type


def test_invalid_project_config_fails_validation(tmp_path: Path) -> None:
    invalid_config = tmp_path / "invalid-project.yaml"
    invalid_config.write_text(
        """
project_title: "Invalid"
domain: "NLP / Computational Linguistics"
target_contexts_min: 50000
target_contexts_max: 10000
max_llm_labels: 100
max_human_validation: 10
datasets:
  labeled:
    - multicite
  unlabeled_large_scale:
    - acl_ocl
  optional_extension: []
""",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="target_contexts_min"):
        load_project_config(invalid_config)


def test_config_show_cli_prints_parsed_config() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["config", "show", "--config", "configs/project.yaml"])

    assert result.exit_code == 0
    parsed = json.loads(result.stdout)
    assert parsed["project_title"] == "From Citation Counts to Citation Evidence"
    assert parsed["datasets"]["labeled"] == ["multicite", "scicite"]
