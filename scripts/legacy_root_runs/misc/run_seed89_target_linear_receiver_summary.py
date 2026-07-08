#!/usr/bin/env python3
"""Summarize seed89 all-target linear receiver-sampling sensitivity."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_linear_receiver_threshold_summary import load_branch_run, parse_run_arg  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RUNS = [
    "target0_nearest50=outputs/experiments/744_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50_ringdown025_objectives",
    "target0_linear50p3125=outputs/experiments/777_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50p3125_linear_receiver_ringdown025_objectives",
    "target1_nearest50=outputs/experiments/746_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown025_objectives",
    "target1_linear50p3125=outputs/experiments/776_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50p3125_linear_receiver_ringdown025_objectives",
    "target2_nearest50=outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives",
    "target2_linear50p3125=outputs/experiments/765_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown025_objectives",
]

CONFIDENCE_COLORS = {
    "strong": "#2E7D32",
    "moderate": "#F9A825",
    "weak": "#D32F2F",
    "ambiguous": "#6A1B9A",
}


def attach_target_baselines(rows: list[dict], baseline_txrx_mm: float = 50.0) -> list[dict]:
    """Attach per-target baseline-normalized margin and offset fields."""
    by_target: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        by_target[int(row["target_index"])].append(dict(row))

    baseline_by_target: dict[int, dict] = {}
    for target_index, target_rows in by_target.items():
        matches = [
            row for row in target_rows
            if row["receiver_sampling"] == "nearest"
            and np.isclose(float(row["tx_rx_offset_mm"]), baseline_txrx_mm, rtol=0.0, atol=1e-9)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"expected one nearest Tx/Rx={baseline_txrx_mm:g} baseline for target {target_index}, got {len(matches)}"
            )
        baseline_by_target[target_index] = matches[0]

    enriched = []
    for target_rows in by_target.values():
        for row in target_rows:
            baseline = baseline_by_target[int(row["target_index"])]
            baseline_margin = float(baseline["base_radius_margin_abs"])
            baseline_offset = float(baseline["mean_effective_receiver_offset_cells"])
            new_row = dict(row)
            new_row["target_label"] = f"target {int(row['target_index'])}"
            new_row["target_baseline_margin_abs"] = baseline_margin
            new_row["target_baseline_run_index"] = baseline["run_index"]
            new_row["base_margin_ratio_to_target_baseline"] = (
                float(row["base_radius_margin_abs"]) / baseline_margin if baseline_margin else np.nan
            )
            new_row["effective_offset_delta_from_target_baseline_cells"] = (
                float(row["mean_effective_receiver_offset_cells"]) - baseline_offset
            )
            enriched.append(new_row)

    return sorted(
        enriched,
        key=lambda row: (
            int(row["target_index"]),
            float(row["effective_offset_delta_from_target_baseline_cells"]),
            row["label"],
        ),
    )


def summarize_rows(rows: list[dict]) -> dict:
    """Summarize all-target linear receiver sensitivity."""
    by_target: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        by_target[int(row["target_index"])].append(row)

    target_summaries = {}
    for target_index, target_rows in sorted(by_target.items()):
        nonzero = [
            row for row in target_rows
            if row["receiver_sampling"] == "linear"
            and float(row["effective_offset_delta_from_target_baseline_cells"]) > 1e-9
        ]
        target_summaries[str(target_index)] = {
            "row_count": len(target_rows),
            "confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in target_rows)),
            "nonzero_linear_count": len(nonzero),
            "nonzero_linear_confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in nonzero)),
            "nonzero_linear_margin_ratio_min": (
                min(float(row["base_margin_ratio_to_target_baseline"]) for row in nonzero)
                if nonzero else None
            ),
            "nonzero_linear_margin_ratio_max": (
                max(float(row["base_margin_ratio_to_target_baseline"]) for row in nonzero)
                if nonzero else None
            ),
        }

    linear_rows = [
        row for row in rows
        if row["receiver_sampling"] == "linear"
        and float(row["effective_offset_delta_from_target_baseline_cells"]) > 1e-9
    ]
    return {
        "row_count": len(rows),
        "target_count": len(by_target),
        "target_indices": sorted(by_target),
        "confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in rows)),
        "linear_confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in linear_rows)),
        "best_truth_preserving_objective_counts": dict(Counter(row["best_truth_preserving_objective"] for row in rows)),
        "target_summaries": target_summaries,
        "weak_linear_targets": [
            int(row["target_index"]) for row in linear_rows if row["base_confidence_label"] == "weak"
        ],
        "moderate_linear_targets": [
            int(row["target_index"]) for row in linear_rows if row["base_confidence_label"] == "moderate"
        ],
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write dictionary rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _linear_rows(rows: list[dict]) -> list[dict]:
    return [
        row for row in rows
        if row["receiver_sampling"] == "linear"
        and float(row["effective_offset_delta_from_target_baseline_cells"]) > 1e-9
    ]


def plot_linear_ratio_by_target(rows: list[dict], save_path: Path) -> None:
    """Plot linear margin ratios by target index."""
    linear_rows = _linear_rows(rows)
    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    x_values = [int(row["target_index"]) for row in linear_rows]
    y_values = [float(row["base_margin_ratio_to_target_baseline"]) for row in linear_rows]
    colors = [CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64") for row in linear_rows]
    ax.bar(x_values, y_values, color=colors, edgecolor="#263238", linewidth=0.8, width=0.55)
    ax.axhline(1.0, color="#263238", linestyle="--", linewidth=1.0)
    for row, x_value, y_value in zip(linear_rows, x_values, y_values):
        ax.annotate(
            f"{row['base_confidence_label']}\n{y_value:.3f}x",
            (x_value, y_value),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
        )
    ax.set_xticks(x_values)
    ax.set_xticklabels([f"target {value}" for value in x_values])
    ax.set_xlabel("Seed89 target index")
    ax.set_ylabel("Linear Tx/Rx=50.3125 margin / same-target Tx/Rx=50 margin")
    ax.set_title("Seed89 Linear Receiver Target Sensitivity")
    ax.set_ylim(0.0, max(1.08, max(y_values) * 1.18))
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_margin_by_target(rows: list[dict], save_path: Path) -> None:
    """Plot absolute baseline and linear margins by target."""
    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    for row in rows:
        target = int(row["target_index"])
        offset = -0.16 if row["receiver_sampling"] == "nearest" else 0.16
        marker = "s" if row["receiver_sampling"] == "nearest" else "o"
        color = CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64")
        ax.scatter(
            target + offset,
            float(row["base_radius_margin_abs"]),
            s=90,
            c=color,
            marker=marker,
            edgecolor="#263238",
            linewidth=0.8,
            zorder=3,
        )
    ax.set_xticks(sorted({int(row["target_index"]) for row in rows}))
    ax.set_xticklabels([f"target {value}" for value in sorted({int(row["target_index"]) for row in rows})])
    ax.set_xlabel("Seed89 target index")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_title("Seed89 Target Margins: Nearest vs Linear Receiver")
    margins = [float(row["base_radius_margin_abs"]) for row in rows]
    ax.set_ylim(min(margins) * 0.88, max(margins) * 1.10)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(
        handles=[
            plt.Line2D([0], [0], marker="s", color="w", label="nearest Tx/Rx=50", markerfacecolor="#B0BEC5", markeredgecolor="#263238", markersize=8),
            plt.Line2D([0], [0], marker="o", color="w", label="linear Tx/Rx=50.3125", markerfacecolor="#B0BEC5", markeredgecolor="#263238", markersize=8),
        ],
        loc="best",
        fontsize=8,
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path, summary: dict) -> None:
    """Write figure notes for the all-target seed89 summary."""
    lines = [
        "# Figure Notes",
        "",
        "## 1. `seed89_linear_ratio_by_target.png` - normalized linear receiver margins",
        "",
        "This bar chart compares each target's linear Tx/Rx=50.3125 base radius",
        "margin against its own nearest-grid Tx/Rx=50 baseline. Values near one",
        "mean the linear receiver perturbation did not change confidence; values",
        "well below one show margin degradation.",
        "",
        "## 2. `seed89_margin_by_target.png` - absolute target margins",
        "",
        "This scatter plot shows the same target rows as absolute best-versus-next",
        "radius objective gaps. Squares are nearest-grid baselines and circles",
        "are linear receiver rows.",
        "",
        "Package summary:",
        f"- rows: {summary['row_count']}",
        f"- confidence labels: {summary['confidence_label_counts']}",
        f"- linear confidence labels: {summary['linear_confidence_label_counts']}",
        f"- weak linear targets: {summary['weak_linear_targets']}",
        f"- moderate linear targets: {summary['moderate_linear_targets']}",
        "",
        "Inspect the normalized ratio plot first; it directly shows that target 2",
        "is the only weak nonzero-linear row in this package.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="*", default=DEFAULT_RUNS, help="LABEL=RUN_DIR")
    parser.add_argument("--baseline-txrx-mm", type=float, default=50.0)
    parser.add_argument("--run-name", default="seed89_target_linear_receiver_summary")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_specs = [parse_run_arg(value) for value in args.run]
    rows = [load_branch_run(label, path) for label, path in run_specs]
    rows = attach_target_baselines(rows, args.baseline_txrx_mm)
    summary = summarize_rows(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "seed89_target_linear_receiver_rows.csv"
    summary_json = data_dir / "seed89_target_linear_receiver_summary.json"
    ratio_fig = figures_dir / "seed89_linear_ratio_by_target.png"
    margin_fig = figures_dir / "seed89_margin_by_target.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    write_rows_csv(rows_csv, rows)
    summary_json.write_text(
        json.dumps({
            "input_runs": [{"label": label, "run_dir": str(path)} for label, path in run_specs],
            "summary": summary,
            "rows": rows,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    plot_linear_ratio_by_target(rows, ratio_fig)
    plot_margin_by_target(rows, margin_fig)
    write_figure_notes(notes_path, summary)
    write_run_manifest(
        str(outdir),
        args.run_name,
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "ratio_figure": str(ratio_fig),
            "margin_figure": str(margin_fig),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote summary: {summary_json}")


if __name__ == "__main__":
    main()
