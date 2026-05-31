"""Figure-generation entry points for final-release analyses."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from citeevidence.final_release.metrics import (
    INTENT_ORDER,
    build_ranking_reversal_plot_table,
    classify_object_role_quadrant,
)


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


def plot_object_role_signature_map(
    data: pd.DataFrame,
    output_png: str | Path,
    output_svg: str | Path | None = None,
    *,
    top_n_labels: int = 12,
    min_non_background_edges: int = 20,
) -> dict[str, str]:
    """Plot seed-registry object role signatures as a citation-use map."""
    import matplotlib.pyplot as plt

    title = "Seed-registry objects occupy distinct citation-use roles"
    x_label = "Use share among non-background object edges"
    y_label = "Compare/critique share among non-background object edges"
    frame = _prepare_object_role_frame(data, min_non_background_edges=min_non_background_edges)
    output_png = Path(output_png)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    if output_svg is not None:
        output_svg = Path(output_svg)
        output_svg.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    labeled_objects: list[str] = []
    if frame.empty:
        ax.text(0.5, 0.5, "No object role signature data", ha="center", va="center")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
    else:
        for object_type, group in frame.groupby("object_type", sort=True):
            ax.scatter(
                group["use_share_non_background"],
                group["compare_critique_share_non_background"],
                s=_object_point_sizes(group["non_background_edges"]),
                alpha=0.72,
                label=object_type or "unknown",
                edgecolors="white",
                linewidths=0.6,
            )
        ax.axvline(
            frame["use_share_non_background"].median(),
            color="0.75",
            linewidth=1,
            linestyle="--",
        )
        ax.axhline(
            frame["compare_critique_share_non_background"].median(),
            color="0.75",
            linewidth=1,
            linestyle="--",
        )
        labeled = _object_label_rows(frame, top_n_labels=top_n_labels)
        for _, row in labeled.iterrows():
            ax.annotate(
                row["canonical_name"],
                (
                    row["use_share_non_background"],
                    row["compare_critique_share_non_background"],
                ),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=8,
            )
        labeled_objects = list(labeled["canonical_name"])
        ax.legend(title="Object type", loc="best", fontsize=8)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    fig.tight_layout()
    fig.savefig(output_png, dpi=200, bbox_inches="tight")
    outputs = {
        "png": str(output_png),
        "title": title,
        "x_label": x_label,
        "y_label": y_label,
        "plotted_objects": "|".join(frame["canonical_name"]) if not frame.empty else "",
        "labeled_objects": "|".join(labeled_objects),
    }
    if output_svg is not None:
        fig.savefig(output_svg, bbox_inches="tight")
        outputs["svg"] = str(output_svg)
    plt.close(fig)
    return outputs


def plot_context_volume_vs_evidence_use_reversal(
    data: pd.DataFrame,
    output_png: str | Path,
    output_svg: str | Path | None = None,
    *,
    top_n: int = 20,
    mode: str = "count",
) -> dict[str, str]:
    """Plot citation-context volume vs evidence-use ranking reversals."""
    import matplotlib.pyplot as plt

    table = build_ranking_reversal_plot_table(data, top_n=top_n, mode=mode)
    title = "Citation-context volume and evidence use rank papers differently"
    left_label = "Rank by citation-context volume"
    right_label = (
        "Rank by evidence-use count"
        if mode == "count"
        else "Rank by shrunk evidence-use share"
    )
    footnote = "Default eligibility: total_strong_contexts >= 20 and evidence_use_count >= 5"
    output_png = Path(output_png)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    if output_svg is not None:
        output_svg = Path(output_svg)
        output_svg.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, max(4, len(table) * 0.42 + 1.8)))
    if table.empty:
        ax.text(0.5, 0.5, "No eligible ranking reversal rows", ha="center", va="center")
        ax.axis("off")
    else:
        right_rank_column = (
            "rank_by_evidence_use_count"
            if mode == "count"
            else "rank_by_shrunk_evidence_use_share"
        )
        _draw_rank_reversal_panel(ax, table, right_rank_column=right_rank_column)
    ax.set_title(title, pad=18)
    fig.text(0.5, 0.01, footnote, ha="center", fontsize=8, color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_png, dpi=200, bbox_inches="tight")
    outputs = {
        "png": str(output_png),
        "plotted_rows": str(len(table)),
        "title": title,
        "left_label": left_label,
        "right_label": right_label,
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


def _draw_rank_reversal_panel(
    ax: object,
    table: pd.DataFrame,
    *,
    right_rank_column: str,
) -> None:
    y_positions = list(range(len(table)))
    colors = table["reversal_type"].map(
        {
            "evidence-use riser": "#2a9d8f",
            "context-volume riser": "#e76f51",
            "balanced": "#6c757d",
        }
    ).fillna("#6c757d")
    ax.hlines(y_positions, 0, 1, color="0.82", linewidth=1.4)
    ax.scatter([0] * len(table), y_positions, s=52, color="#577590", zorder=3)
    ax.scatter([1] * len(table), y_positions, s=52, color=colors, zorder=3)
    for y_position, (_, row) in zip(y_positions, table.iterrows(), strict=True):
        ax.text(
            -0.06,
            y_position,
            f"#{int(row['rank_by_context_volume'])}",
            ha="right",
            va="center",
            fontsize=8,
            color="0.25",
        )
        ax.text(
            1.06,
            y_position,
            f"#{int(row[right_rank_column])}",
            ha="left",
            va="center",
            fontsize=8,
            color="0.25",
        )
    ax.set_xlim(-0.22, 1.22)
    ax.set_ylim(-0.8, len(table) - 0.2)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(table["plot_label"])
    ax.invert_yaxis()
    ax.set_xticks([0, 1])
    ax.set_xticklabels(
        ["Rank by citation-context volume", _right_rank_axis_label(right_rank_column)]
    )
    ax.tick_params(axis="x", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)


def _right_rank_axis_label(right_rank_column: str) -> str:
    if right_rank_column == "rank_by_shrunk_evidence_use_share":
        return "Rank by shrunk evidence-use share"
    return "Rank by evidence-use count"


def _prepare_object_role_frame(
    data: pd.DataFrame,
    *,
    min_non_background_edges: int,
) -> pd.DataFrame:
    frame = data.copy()
    if "role_quadrant" not in frame:
        frame = classify_object_role_quadrant(frame)
    columns = [
        "canonical_name",
        "object_type",
        "non_background_edges",
        "use_share_non_background",
        "compare_critique_share_non_background",
        "role_quadrant",
    ]
    for column in columns:
        if column not in frame:
            frame[column] = ""
    frame["canonical_name"] = frame["canonical_name"].map(_clean_text)
    frame["object_type"] = frame["object_type"].map(_clean_text).replace("", "unknown")
    for column in [
        "non_background_edges",
        "use_share_non_background",
        "compare_critique_share_non_background",
    ]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0)
    frame = frame.loc[
        frame["canonical_name"].ne("")
        & frame["non_background_edges"].ge(min_non_background_edges)
    ].copy()
    return frame.sort_values(
        ["non_background_edges", "canonical_name"],
        ascending=[False, True],
    ).reset_index(drop=True)


def _object_point_sizes(non_background_edges: pd.Series) -> pd.Series:
    counts = pd.to_numeric(non_background_edges, errors="coerce").fillna(0)
    if counts.empty:
        return counts
    max_count = max(float(counts.max()), 1.0)
    return 40 + (counts / max_count) * 360


def _object_label_rows(frame: pd.DataFrame, *, top_n_labels: int) -> pd.DataFrame:
    if frame.empty or top_n_labels <= 0:
        return frame.head(0).copy()
    top = frame.nlargest(top_n_labels, "non_background_edges")
    extremes = []
    for quadrant in sorted(frame["role_quadrant"].dropna().unique()):
        subset = frame.loc[frame["role_quadrant"].eq(quadrant)]
        if subset.empty:
            continue
        extremes.append(
            subset.sort_values(
                [
                    "non_background_edges",
                    "use_share_non_background",
                    "compare_critique_share_non_background",
                ],
                ascending=[False, False, False],
            ).head(1)
        )
    if extremes:
        top = pd.concat([top, *extremes], ignore_index=True)
    return top.drop_duplicates("canonical_name").head(top_n_labels)


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
