from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Self

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

DatasetName = Literal["multicite", "scicite", "acl_ocl", "unarxive"]
IntentLabel = Literal["background", "uses", "compares_against", "extends", "critiques", "applies"]
ObjectTypeLabel = Literal[
    "method",
    "dataset_or_database",
    "software_or_tool",
    "benchmark_or_protocol",
    "metric",
    "claim_or_finding",
    "theory_or_concept",
]
RelationSubtypeLabel = Literal[
    "direct_use",
    "adapt_to_domain",
    "combine_with",
    "compare_against",
    "critique_limitation",
    "improve",
    "replace",
    "component_use",
]
MethodEdgeTypeLabel = Literal[
    "extends",
    "improves",
    "replaces",
    "adapts",
    "uses_component",
    "compares",
    "background",
    "not_method_related",
]


class ConfigLoadError(ValueError):
    """Raised when a YAML config file cannot be loaded as a mapping."""


class DatasetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    labeled: list[DatasetName] = Field(min_length=1)
    unlabeled_large_scale: list[DatasetName] = Field(min_length=1)
    optional_extension: list[DatasetName] = Field(default_factory=list)


class ProjectConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_title: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    target_contexts_min: int = Field(gt=0)
    target_contexts_max: int = Field(gt=0)
    max_llm_labels: int = Field(ge=0)
    max_human_validation: int = Field(ge=0)
    datasets: DatasetConfig

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        if self.target_contexts_min > self.target_contexts_max:
            msg = "target_contexts_min must be less than or equal to target_contexts_max"
            raise ValueError(msg)
        if self.max_human_validation > self.max_llm_labels:
            msg = "max_human_validation must be less than or equal to max_llm_labels"
            raise ValueError(msg)
        return self


class LabelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intent: list[IntentLabel] = Field(min_length=1)
    object_type: list[ObjectTypeLabel] = Field(min_length=1)
    relation_subtype: list[RelationSubtypeLabel] = Field(min_length=1)
    method_edge_type: list[MethodEdgeTypeLabel] = Field(min_length=1)


def load_project_config(path: str | Path) -> ProjectConfig:
    """Load and validate project defaults from a YAML file."""
    return ProjectConfig.model_validate(_read_yaml_mapping(path))


def load_label_config(path: str | Path) -> LabelConfig:
    """Load and validate label taxonomy from a YAML file."""
    return LabelConfig.model_validate(_read_yaml_mapping(path))


def _read_yaml_mapping(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    try:
        loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigLoadError(f"Config file not found: {config_path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigLoadError(f"Invalid YAML in config file: {config_path}") from exc

    if not isinstance(loaded, dict):
        raise ConfigLoadError(f"Config file must contain a YAML mapping: {config_path}")

    return loaded
