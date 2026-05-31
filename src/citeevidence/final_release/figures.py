"""Figure-generation entry points for final-release analyses."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from citeevidence.final_release.metrics import INTENT_ORDER


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


def plot_section_function_lift_heatmap(
    data: pd.DataFrame,
    output_png: str | Path,
    output_svg: str | Path | None = None,
    *,
    include_unknown: bool = False,
    max_sections: int = 20,
) -> dict[str, str]:
    """Plot a claim-driven section-function log-odds lift heatmap."""
    import matplotlib.pyplot as plt

    frame = _prepare_section_function_frame(data, include_unknown=include_unknown)
    section_order = _section_order(frame, max_sections=max_sections)
    intent_order = _intent_order(frame)
    output_png = Path(output_png)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    if output_svg is not None:
        output_svg = Path(output_svg)
        output_svg.parent.mkdir(parents=True, exist_ok=True)

    if not section_order or not intent_order:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No section-function lift data", ha="center", va="center")
        ax.axis("off")
        plotted_sections: list[str] = []
        plotted_intents: list[str] = []
    else:
        frame = frame.loc[
            frame["normalized_section"].isin(section_order)
            & frame["final_intent"].isin(intent_order)
        ].copy()
        matrix = _pivot_metric(frame, section_order, intent_order, "log_odds_lift")
        share_matrix = _pivot_metric(frame, section_order, intent_order, "row_share")
        section_labels = _section_labels(frame, section_order)

        width = max(8, len(intent_order) * 1.45)
        height = max(4, len(section_order) * 0.45 + 1.8)
        fig, ax = plt.subplots(figsize=(width, height))
        values = matrix.to_numpy(dtype=float)
        limit = max(float(abs(values).max()), 0.1)
        image = ax.imshow(
            values,
            cmap="RdBu_r",
            vmin=-limit,
            vmax=limit,
            aspect="auto",
        )
        ax.set_xticks(range(len(intent_order)))
        ax.set_xticklabels(intent_order, rotation=35, ha="right")
        ax.set_yticks(range(len(section_order)))
        ax.set_yticklabels(section_labels)
        ax.set_xlabel("Final citation function")
        ax.set_ylabel("Paper section")
        ax.set_title("Citation roles follow paper rhetorical structure")
        fig.colorbar(image, ax=ax, label="Log-odds lift")
        _annotate_section_heatmap(ax, matrix, share_matrix, color_limit=limit)
        plotted_sections = section_order
        plotted_intents = intent_order

    fig.tight_layout()
    fig.savefig(output_png, dpi=200, bbox_inches="tight")
    outputs = {
        "png": str(output_png),
        "plotted_sections": "|".join(plotted_sections),
        "plotted_intents": "|".join(plotted_intents),
    }
    if output_svg is not None:
        fig.savefig(output_svg, bbox_inches="tight")
        outputs["svg"] = str(output_svg)
    plt.close(fig)
    return outputs


def _prepare_section_function_frame(
    data: pd.DataFrame,
    *,
    include_unknown: bool,
) -> pd.DataFrame:
    columns = [
        "normalized_section",
        "final_intent",
        "section_total",
        "section_label",
        "row_share",
        "log_odds_lift",
        "is_unknown_section",
    ]
    frame = data.copy()
    for column in columns:
        if column not in frame:
            frame[column] = ""
    frame["normalized_section"] = frame["normalized_section"].map(_clean_text)
    frame["final_intent"] = frame["final_intent"].map(_clean_text)
    frame["section_label"] = frame["section_label"].map(_clean_text)
    frame["section_total"] = pd.to_numeric(frame["section_total"], errors="coerce").fillna(0)
    frame["row_share"] = pd.to_numeric(frame["row_share"], errors="coerce").fillna(0.0)
    frame["log_odds_lift"] = pd.to_numeric(
        frame["log_odds_lift"],
        errors="coerce",
    ).fillna(0.0)
    frame["is_unknown_section"] = frame["is_unknown_section"].map(_parse_bool)
    if not include_unknown:
        frame = frame.loc[~frame["is_unknown_section"]].copy()
    return frame.loc[
        frame["normalized_section"].ne("") & frame["final_intent"].ne("")
    ].copy()


def _section_order(frame: pd.DataFrame, *, max_sections: int) -> list[str]:
    if frame.empty or max_sections <= 0:
        return []
    section_totals = (
        frame.groupby("normalized_section", dropna=False)["section_total"]
        .max()
        .sort_values(ascending=False)
    )
    ordered = sorted(
        section_totals.index,
        key=lambda section: (-section_totals.loc[section], section),
    )
    return ordered[:max_sections]


def _intent_order(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    intents = {_clean_text(intent) for intent in frame["final_intent"]}
    intents.discard("")
    ordered = [intent for intent in INTENT_ORDER if intent in intents]
    ordered.extend(sorted(intents.difference(INTENT_ORDER)))
    return ordered


def _pivot_metric(
    frame: pd.DataFrame,
    section_order: list[str],
    intent_order: list[str],
    value_column: str,
) -> pd.DataFrame:
    matrix = frame.pivot_table(
        index="normalized_section",
        columns="final_intent",
        values=value_column,
        aggfunc="first",
        fill_value=0.0,
    )
    return matrix.reindex(index=section_order, columns=intent_order, fill_value=0.0)


def _section_labels(frame: pd.DataFrame, section_order: list[str]) -> list[str]:
    labels = (
        frame.drop_duplicates("normalized_section")
        .set_index("normalized_section")["section_label"]
        .to_dict()
    )
    return [labels.get(section) or section for section in section_order]


def _annotate_section_heatmap(
    ax: object,
    matrix: pd.DataFrame,
    share_matrix: pd.DataFrame,
    *,
    color_limit: float,
) -> None:
    for row_index, section in enumerate(matrix.index):
        for column_index, intent in enumerate(matrix.columns):
            lift = float(matrix.loc[section, intent])
            row_share = float(share_matrix.loc[section, intent])
            if abs(lift) < 0.75 and row_share < 0.25:
                continue
            text_color = "white" if abs(lift) > color_limit * 0.55 else "black"
            ax.text(
                column_index,
                row_index,
                f"{row_share:.0%}",
                ha="center",
                va="center",
                color=text_color,
                fontsize=8,
            )


def _parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except (TypeError, ValueError):
        pass
    if isinstance(value, int | float):
        return value != 0
    return str(value).strip().casefold() in {"1", "t", "true", "y", "yes"}


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()
