"""Figure-generation entry points for future final-release analyses."""

from __future__ import annotations


def planned_figure_modules() -> tuple[str, ...]:
    """Return planned figure topics without generating any artifacts."""
    return (
        "evidence_pipeline",
        "section_function_lift",
        "object_role_signatures",
        "ranking_reversal",
        "critique_bottlenecks",
        "metric_benchmark_roles",
    )
