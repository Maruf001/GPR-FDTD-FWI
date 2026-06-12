#!/usr/bin/env python3
"""Summarize cross-seed target-2 linear receiver-sampling runs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
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
    "seed13_nearest50=outputs/experiments/521_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50_ringdown025_objectives",
    "seed13_linear50p3125=outputs/experiments/774_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50p3125_linear_receiver_ringdown025_objectives",
    "seed89_nearest50=outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives",
    "seed89_linear50p0390625=outputs/experiments/769_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p0390625_linear_receiver_ringdown025_objectives",
    "seed89_linear50p3125=outputs/experiments/765_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown025_objectives",
    "seed21_nearest50=outputs/experiments/741_coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50_ringdown025_objectives",
    "seed21_linear50p0390625=outputs/experiments/771_coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50p0390625_linear_receiver_ringdown025_objectives",
    "seed21_linear50p3125=outputs/experiments/772_coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50p3125_linear_receiver_ringdown025_objectives",
]

CONFIDENCE_COLORS = {
    "strong": "#2E7D32",
    "moderate": "#F9A825",
    "weak": "#D32F2F",
    "ambiguous": "#6A1B9A",
}

SEED_COLORS = {
    "seed13": "#6A1B9A",
    "seed21": "#1565C0",
    "seed89": "#00897B",
}


def extract_seed_label(row: dict) -> str:
    """Extract a stable seed label from run metadata."""
    for key in ("label", "run_name", "run_path"):
        match = re.search(r"seed(\d+)", str(row.get(key, "")))
        if match:
            return f"seed{match.group(1)}"
    raise ValueError(f"could not infer seed label for row {row.get('label')!r}")


def attach_seed_baselines(rows: list[dict], baseline_txrx_mm: float = 50.0) -> list[dict]:
    """Attach per-seed baseline-normalized margin and offset fields."""
    by_seed: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        enriched = dict(row)
        enriched["seed_label"] = extract_seed_label(enriched)
        by_seed[enriched["seed_label"]].append(enriched)

    baseline_by_seed: dict[str, dict] = {}
    for seed_label, seed_rows in by_seed.items():
        matches = [
            row for row in seed_rows
            if row["receiver_sampling"] == "nearest"
            and np.isclose(float(row["tx_rx_offset_mm"]), baseline_txrx_mm, rtol=0.0, atol=1e-9)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"expected one nearest Tx/Rx={baseline_txrx_mm:g} baseline for {seed_label}, got {len(matches)}"
            )
        baseline_by_seed[seed_label] = matches[0]

    enriched_rows = []
    for row in [item for seed_rows in by_seed.values() for item in seed_rows]:
        baseline = baseline_by_seed[row["seed_label"]]
        baseline_margin = float(baseline["base_radius_margin_abs"])
        baseline_offset = float(baseline["mean_effective_receiver_offset_cells"])
        new_row = dict(row)
        new_row["seed_baseline_margin_abs"] = baseline_margin
        new_row["seed_baseline_run_index"] = baseline["run_index"]
        new_row["base_margin_ratio_to_seed_baseline"] = (
            float(row["base_radius_margin_abs"]) / baseline_margin if baseline_margin else np.nan
        )
        new_row["effective_offset_delta_from_seed_baseline_cells"] = (
            float(row["mean_effective_receiver_offset_cells"]) - baseline_offset
        )
        enriched_rows.append(new_row)

    return sorted(
        enriched_rows,
        key=lambda row: (
            row["seed_label"],
            float(row["effective_offset_delta_from_seed_baseline_cells"]),
            float(row["tx_rx_offset_mm"]),
            row["label"],
        ),
    )


def summarize_rows(rows: list[dict]) -> dict:
    """Summarize the cross-seed linear receiver branch."""
    by_seed: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_seed[row["seed_label"]].append(row)

    seed_summaries = {}
    for seed_label, seed_rows in sorted(by_seed.items()):
        nonzero = [
            row for row in seed_rows
            if row["receiver_sampling"] == "linear"
            and float(row["effective_offset_delta_from_seed_baseline_cells"]) > 1e-9
        ]
        seed_summaries[seed_label] = {
            "row_count": len(seed_rows),
            "confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in seed_rows)),
            "nonzero_linear_count": len(nonzero),
            "nonzero_linear_confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in nonzero)),
            "nonzero_linear_margin_ratio_min": (
                min(float(row["base_margin_ratio_to_seed_baseline"]) for row in nonzero)
                if nonzero else None
            ),
            "nonzero_linear_margin_ratio_max": (
                max(float(row["base_margin_ratio_to_seed_baseline"]) for row in nonzero)
                if nonzero else None
            ),
        }

    nonzero_confidence_by_seed = {
        seed_label: values["nonzero_linear_confidence_label_counts"]
        for seed_label, values in seed_summaries.items()
    }
    nonzero_ratio_range_by_seed = {
        seed_label: {
            "min": values["nonzero_linear_margin_ratio_min"],
            "max": values["nonzero_linear_margin_ratio_max"],
        }
        for seed_label, values in seed_summaries.items()
    }
    return {
        "row_count": len(rows),
        "seed_count": len(by_seed),
        "seed_labels": sorted(by_seed),
        "confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in rows)),
        "best_truth_preserving_objective_counts": dict(Counter(row["best_truth_preserving_objective"] for row in rows)),
        "seed_summaries": seed_summaries,
        "nonzero_linear_confidence_label_counts_by_seed": nonzero_confidence_by_seed,
        "nonzero_linear_margin_ratio_range_by_seed": nonzero_ratio_range_by_seed,
        "all_seed13_nonzero_linear_moderate": all(
            row["base_confidence_label"] == "moderate"
            for row in rows
            if row["seed_label"] == "seed13"
            and row["receiver_sampling"] == "linear"
            and float(row["effective_offset_delta_from_seed_baseline_cells"]) > 1e-9
        ),
        "all_seed21_nonzero_linear_moderate": all(
            row["base_confidence_label"] == "moderate"
            for row in rows
            if row["seed_label"] == "seed21"
            and row["receiver_sampling"] == "linear"
            and float(row["effective_offset_delta_from_seed_baseline_cells"]) > 1e-9
        ),
        "all_seed89_nonzero_linear_weak": all(
            row["base_confidence_label"] == "weak"
            for row in rows
            if row["seed_label"] == "seed89"
            and row["receiver_sampling"] == "linear"
            and float(row["effective_offset_delta_from_seed_baseline_cells"]) > 1e-9
        ),
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write dictionary rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _offset_label(row: dict) -> str:
    if row["receiver_sampling"] == "nearest":
        return f"{row['seed_label']} 50 N"
    return f"{row['seed_label']} {float(row['tx_rx_offset_mm']):.4g} L"


def _annotation_offset(row: dict) -> tuple[int, int]:
    """Return a compact annotation offset that separates shared baselines."""
    delta = float(row["effective_offset_delta_from_seed_baseline_cells"])
    if abs(delta) < 1e-9:
        if row["seed_label"] == "seed13":
            return (8, -36)
        if row["seed_label"] == "seed21":
            return (8, -20)
        return (8, 14)
    if delta > 0.25:
        if row["seed_label"] == "seed13":
            return (8, 25)
        if row["seed_label"] == "seed21":
            return (8, 8)
        return (8, -12)
    if row["seed_label"] == "seed13":
        return (8, 22)
    if row["seed_label"] == "seed21":
        return (8, 10)
    return (8, -10)


def _plot_seed_rows(rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["seed_label"]].append(row)
    return {
        seed: sorted(seed_rows, key=lambda row: float(row["effective_offset_delta_from_seed_baseline_cells"]))
        for seed, seed_rows in sorted(grouped.items())
    }


def plot_margin_ratio_by_seed_delta(rows: list[dict], save_path: Path) -> None:
    """Plot per-seed baseline-normalized margin by receiver offset delta."""
    fig, ax = plt.subplots(figsize=(9.4, 5.1), constrained_layout=True)
    for seed_label, seed_rows in _plot_seed_rows(rows).items():
        seed_color = SEED_COLORS.get(seed_label, "#455A64")
        x_values = [float(row["effective_offset_delta_from_seed_baseline_cells"]) for row in seed_rows]
        y_values = [float(row["base_margin_ratio_to_seed_baseline"]) for row in seed_rows]
        ax.plot(x_values, y_values, color=seed_color, linewidth=1.6, alpha=0.75, label=seed_label)
        for row in seed_rows:
            x_value = float(row["effective_offset_delta_from_seed_baseline_cells"])
            y_value = float(row["base_margin_ratio_to_seed_baseline"])
            face = CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64")
            ax.scatter(x_value, y_value, s=92, c=face, edgecolor=seed_color, linewidth=1.4, zorder=3)
            ax.annotate(_offset_label(row), (x_value, y_value), textcoords="offset points", xytext=_annotation_offset(row), fontsize=7.2)
    ax.axhline(1.0, color="#263238", linestyle="--", linewidth=1.0)
    ax.set_xlabel("Effective receiver-offset delta from each seed baseline (cells)")
    ax.set_ylabel("Base margin / same-seed Tx/Rx=50 margin")
    ax.set_title("Cross-Seed Linear Receiver Target-2 Margin Ratio")
    ratios = [float(row["base_margin_ratio_to_seed_baseline"]) for row in rows]
    ax.set_ylim(min(ratios) * 0.88, max(ratios) * 1.08)
    deltas = [float(row["effective_offset_delta_from_seed_baseline_cells"]) for row in rows]
    ax.set_xlim(min(deltas) - 0.015, max(deltas) + 0.055)
    ax.grid(alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_base_margin_by_seed_delta(rows: list[dict], save_path: Path) -> None:
    """Plot absolute base margin by receiver offset delta and seed."""
    fig, ax = plt.subplots(figsize=(9.4, 5.1), constrained_layout=True)
    for seed_label, seed_rows in _plot_seed_rows(rows).items():
        seed_color = SEED_COLORS.get(seed_label, "#455A64")
        x_values = [float(row["effective_offset_delta_from_seed_baseline_cells"]) for row in seed_rows]
        y_values = [float(row["base_radius_margin_abs"]) for row in seed_rows]
        ax.plot(x_values, y_values, color=seed_color, linewidth=1.6, alpha=0.75, label=seed_label)
        for row in seed_rows:
            x_value = float(row["effective_offset_delta_from_seed_baseline_cells"])
            y_value = float(row["base_radius_margin_abs"])
            face = CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64")
            ax.scatter(x_value, y_value, s=92, c=face, edgecolor=seed_color, linewidth=1.4, zorder=3)
            ax.annotate(_offset_label(row), (x_value, y_value), textcoords="offset points", xytext=_annotation_offset(row), fontsize=7.2)
    ax.set_xlabel("Effective receiver-offset delta from each seed baseline (cells)")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_title("Cross-Seed Linear Receiver Target-2 Base Margins")
    margins = [float(row["base_radius_margin_abs"]) for row in rows]
    ax.set_ylim(min(margins) * 0.90, max(margins) * 1.08)
    deltas = [float(row["effective_offset_delta_from_seed_baseline_cells"]) for row in rows]
    ax.set_xlim(min(deltas) - 0.015, max(deltas) + 0.055)
    ax.grid(alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path, summary: dict) -> None:
    """Write figure notes for the cross-seed summary."""
    per_seed_lines = []
    for seed_label in summary["seed_labels"]:
        counts = summary["nonzero_linear_confidence_label_counts_by_seed"].get(seed_label, {})
        ratio_range = summary["nonzero_linear_margin_ratio_range_by_seed"].get(seed_label, {})
        per_seed_lines.append(
            f"  - {seed_label}: nonzero labels {counts}, ratio range {ratio_range}"
        )
    lines = [
        "# Figure Notes",
        "",
        "## 1. `cross_seed_linear_margin_ratio_by_delta.png` - same-seed normalized margins",
        "",
        "This plot compares target-2 base radius margins after normalizing each",
        "seed to its own nearest-grid Tx/Rx=50 baseline. The x-axis is the",
        "effective receiver-offset delta in grid cells, so linear Tx/Rx=50.3125",
        "corresponds to a 0.3125-cell nonzero contribution from the +51 receiver",
        "cell before the boundary-clamped receiver is excluded from the average.",
        "",
        "## 2. `cross_seed_linear_base_margin_by_delta.png` - absolute margins",
        "",
        "This plot shows the same rows without same-seed normalization. It is the",
        "better first plot for comparing whether the seed branches are separated",
        "by enough margin to justify another seed replication.",
        "",
        "Package summary:",
        f"- rows: {summary['row_count']}",
        f"- seeds: {summary['seed_labels']}",
        f"- confidence labels: {summary['confidence_label_counts']}",
        f"- best truth-preserving objectives: {summary['best_truth_preserving_objective_counts']}",
        "- per-seed nonzero linear rows:",
        *per_seed_lines,
        f"- seed13 nonzero linear rows all moderate: {summary['all_seed13_nonzero_linear_moderate']}",
        f"- seed21 nonzero linear rows all moderate: {summary['all_seed21_nonzero_linear_moderate']}",
        f"- seed89 nonzero linear rows all weak: {summary['all_seed89_nonzero_linear_weak']}",
        "",
        "Inspect the normalized margin-ratio plot first for seed-to-seed",
        "classification behavior, then use the absolute-margin plot to judge the",
        "gap between the weak and moderate plateaus.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="*", default=DEFAULT_RUNS, help="LABEL=RUN_DIR")
    parser.add_argument("--baseline-txrx-mm", type=float, default=50.0)
    parser.add_argument("--run-name", default="cross_seed_linear_receiver_summary")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_specs = [parse_run_arg(value) for value in args.run]
    rows = [load_branch_run(label, path) for label, path in run_specs]
    rows = attach_seed_baselines(rows, args.baseline_txrx_mm)
    summary = summarize_rows(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "cross_seed_linear_receiver_rows.csv"
    summary_json = data_dir / "cross_seed_linear_receiver_summary.json"
    ratio_fig = figures_dir / "cross_seed_linear_margin_ratio_by_delta.png"
    margin_fig = figures_dir / "cross_seed_linear_base_margin_by_delta.png"
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
    plot_margin_ratio_by_seed_delta(rows, ratio_fig)
    plot_base_margin_by_seed_delta(rows, margin_fig)
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
