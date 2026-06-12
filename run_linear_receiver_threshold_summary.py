#!/usr/bin/env python3
"""Summarize seed89 target-2 linear receiver-sampling threshold runs."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
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

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RUNS = [
    "nearest50=outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives",
    "linear50p078125=outputs/experiments/767_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p078125_linear_receiver_ringdown025_objectives",
    "linear50p15625=outputs/experiments/766_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p15625_linear_receiver_ringdown025_objectives",
    "linear50p3125=outputs/experiments/765_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown025_objectives",
    "nearest51=outputs/experiments/763_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p625_ringdown025_objectives",
]

CONFIDENCE_COLORS = {
    "strong": "#2E7D32",
    "moderate": "#F9A825",
    "weak": "#D32F2F",
    "ambiguous": "#6A1B9A",
}


def parse_run_arg(value: str) -> tuple[str, Path]:
    """Parse a labelled run-directory argument."""
    if "=" not in value:
        raise ValueError(f"expected LABEL=RUN_DIR argument, got {value!r}")
    label, path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError("run label must not be empty")
    return label, Path(path)


def _read_single_csv_row(path: Path) -> dict:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError(f"expected exactly one row in {path}, got {len(rows)}")
    return rows[0]


def _read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict, key: str) -> float:
    return float(row[key])


def _run_index(path: Path) -> int | None:
    match = re.match(r"^(\d+)_", path.name)
    return int(match.group(1)) if match else None


def _compact_float(value: float) -> str:
    text = f"{float(value):.6f}".rstrip("0").rstrip(".")
    return text or "0"


def receiver_sampling_layout(
    scan_x_values_mm: list[float],
    tx_rx_offset_mm: float,
    grid_step_mm: float,
    receiver_sampling: str,
    *,
    pml_thickness_mm: float | None = None,
    domain_x_mm: float | None = None,
) -> dict:
    """Compute effective receiver offsets for nearest or linear sampling."""
    if receiver_sampling not in ("nearest", "linear"):
        raise ValueError("receiver_sampling must be 'nearest' or 'linear'")
    if grid_step_mm <= 0.0:
        raise ValueError("grid_step_mm must be positive")
    if not scan_x_values_mm:
        raise ValueError("scan_x_values_mm must not be empty")
    if pml_thickness_mm is None:
        pml_thickness_mm = float(cfg.NPML * cfg.DX * 1000.0)
    if domain_x_mm is None:
        domain_x_mm = float(cfg.DOMAIN_X * 1000.0)

    npml = max(8, int(round(pml_thickness_mm / grid_step_mm)))
    nx_inner = int(round(domain_x_mm / grid_step_mm))
    max_rec_ix = nx_inner + npml - 1
    rows = []

    for x_mm in scan_x_values_mm:
        src_ix = int(np.round(float(x_mm) / grid_step_mm)) + npml
        raw_rec_cell = (float(x_mm) + float(tx_rx_offset_mm)) / grid_step_mm
        if receiver_sampling == "nearest":
            rec_ix = int(np.round(raw_rec_cell)) + npml
            clamped = rec_ix > max_rec_ix
            rec_ix = min(rec_ix, max_rec_ix)
            left_ix = rec_ix
            right_ix = rec_ix
            weight_right = 0.0
            effective_ix = float(rec_ix)
        else:
            left_cell = int(np.floor(raw_rec_cell))
            weight_right = float(raw_rec_cell - left_cell)
            left_ix = left_cell + npml
            right_ix = left_ix + 1
            clamped = right_ix > max_rec_ix
            if left_ix >= max_rec_ix:
                left_ix = max_rec_ix
                right_ix = max_rec_ix
                weight_right = 0.0
            elif right_ix > max_rec_ix:
                right_ix = max_rec_ix
                weight_right = min(max(weight_right, 0.0), 1.0)
            effective_ix = (1.0 - weight_right) * left_ix + weight_right * right_ix
        rows.append({
            "source_ix": int(src_ix),
            "receiver_left_ix": int(left_ix),
            "receiver_right_ix": int(right_ix),
            "receiver_weight_right": float(weight_right),
            "effective_receiver_offset_cells": float(effective_ix - src_ix),
            "clamped": bool(clamped),
        })

    unclamped = [row for row in rows if not row["clamped"]]
    averaging_rows = unclamped if unclamped else rows
    return {
        "rows": rows,
        "clamped_receiver_count": sum(bool(row["clamped"]) for row in rows),
        "mean_effective_receiver_offset_cells": float(np.mean([
            row["effective_receiver_offset_cells"] for row in averaging_rows
        ])),
        "mean_receiver_weight_right": float(np.mean([
            row["receiver_weight_right"] for row in averaging_rows
        ])),
    }


def best_truth_preserving_diagnostic(diagnostic_rows: list[dict], truth_radius_mm: float) -> dict:
    """Select the largest-margin diagnostic row that preserves the truth radius."""
    truth_rows = [
        row for row in diagnostic_rows
        if np.isclose(float(row["best_radius_mm"]), truth_radius_mm, rtol=0.0, atol=1e-9)
    ]
    candidates = truth_rows if truth_rows else diagnostic_rows
    return max(candidates, key=lambda row: float(row["radius_margin_abs"]))


def load_branch_run(label: str, run_dir: Path) -> dict:
    """Load one coordinate-optimizer run into a linear-threshold row."""
    data_dir = run_dir / "data"
    summary_path = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    with summary_path.open("r", encoding="utf-8") as handle:
        summary = json.load(handle)
    confidence = _read_single_csv_row(data_dir / "coordinate_confidence_report.csv")
    diagnostics = _read_csv_rows(data_dir / "coordinate_objective_diagnostics.csv")
    target_index = int(float(confidence["target_rebar_index"]))
    truth_radius_mm = float(summary["truth_radius_values_mm"][target_index])
    receiver_sampling = summary.get("receiver_sampling", "nearest")
    layout = receiver_sampling_layout(
        [float(value) for value in summary["scan_x_values_mm"]],
        float(summary["tx_rx_offset_mm"]),
        float(summary["grid_step_mm"]),
        receiver_sampling,
    )
    best_diag = best_truth_preserving_diagnostic(diagnostics, truth_radius_mm)
    base_margin = _float(confidence, "radius_margin_abs")
    best_margin = _float(best_diag, "radius_margin_abs")
    return {
        "label": label,
        "run_index": _run_index(run_dir),
        "run_name": summary["run_name"],
        "run_path": str(run_dir),
        "receiver_sampling": receiver_sampling,
        "tx_rx_offset_mm": float(summary["tx_rx_offset_mm"]),
        "grid_step_mm": float(summary["grid_step_mm"]),
        "target_index": target_index,
        "base_best_radius_mm": _float(confidence, "best_radius_mm"),
        "base_next_radius_mm": _float(confidence, "next_radius_mm"),
        "base_radius_margin_abs": base_margin,
        "base_radius_margin_rel": _float(confidence, "radius_margin_rel"),
        "base_confidence_label": confidence["confidence_label"],
        "base_best_misfit": _float(confidence, "best_misfit"),
        "best_truth_preserving_objective": best_diag["objective_label"],
        "best_truth_preserving_margin_abs": best_margin,
        "best_truth_preserving_ratio_to_base": best_margin / base_margin if base_margin else np.nan,
        "mean_effective_receiver_offset_cells": layout["mean_effective_receiver_offset_cells"],
        "mean_receiver_weight_right": layout["mean_receiver_weight_right"],
        "clamped_receiver_count": layout["clamped_receiver_count"],
        "receiver_weights_right": ";".join(
            _compact_float(row["receiver_weight_right"]) for row in layout["rows"]
        ),
        "effective_receiver_offsets_cells": ";".join(
            _compact_float(row["effective_receiver_offset_cells"]) for row in layout["rows"]
        ),
        "summary_json": str(summary_path),
    }


def attach_baseline_fields(rows: list[dict], baseline_label: str) -> list[dict]:
    """Attach baseline-relative margin and receiver-offset fields."""
    baseline = next(row for row in rows if row["label"] == baseline_label)
    baseline_margin = float(baseline["base_radius_margin_abs"])
    baseline_offset = float(baseline["mean_effective_receiver_offset_cells"])
    enriched = []
    for row in rows:
        new_row = dict(row)
        new_row["base_margin_ratio_to_baseline"] = (
            float(row["base_radius_margin_abs"]) / baseline_margin
            if baseline_margin else np.nan
        )
        new_row["effective_offset_delta_from_baseline_cells"] = (
            float(row["mean_effective_receiver_offset_cells"]) - baseline_offset
        )
        enriched.append(new_row)
    return sorted(enriched, key=lambda row: (float(row["effective_offset_delta_from_baseline_cells"]), row["label"]))


def summarize_rows(rows: list[dict]) -> dict:
    """Summarize the linear receiver threshold branch."""
    linear_nonzero = [
        row for row in rows
        if row["receiver_sampling"] == "linear"
        and float(row["effective_offset_delta_from_baseline_cells"]) > 1e-9
    ]
    return {
        "row_count": len(rows),
        "receiver_sampling_counts": dict(Counter(row["receiver_sampling"] for row in rows)),
        "confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in rows)),
        "best_truth_preserving_objective_counts": dict(Counter(row["best_truth_preserving_objective"] for row in rows)),
        "linear_nonzero_count": len(linear_nonzero),
        "linear_nonzero_confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in linear_nonzero)),
        "smallest_tested_nonzero_delta_cells": (
            min(float(row["effective_offset_delta_from_baseline_cells"]) for row in linear_nonzero)
            if linear_nonzero else None
        ),
        "all_nonzero_linear_weak": all(row["base_confidence_label"] == "weak" for row in linear_nonzero),
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write dictionary rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _plot_label(row: dict) -> str:
    """Return a compact label for crowded threshold plots."""
    if row["label"] == "nearest50":
        return "50 N"
    if row["label"] == "nearest51":
        return "+51 N"
    suffix = " L" if row["receiver_sampling"] == "linear" else " N"
    return f"{float(row['tx_rx_offset_mm']):.3f}{suffix}"


def _plot_annotation(row: dict) -> tuple[tuple[int, int], str]:
    """Return text offset and alignment for compact plot labels."""
    label = row["label"]
    if label.endswith("0390625"):
        return (-16, 22), "right"
    if label.endswith("078125"):
        return (12, 14), "left"
    if label.endswith("15625"):
        return (10, 20), "left"
    if label.endswith("3125"):
        return (0, 15), "center"
    if label == "nearest50":
        return (0, 14), "center"
    return (0, 13), "center"


def plot_margin_ratio_by_delta(rows: list[dict], save_path: Path) -> None:
    """Plot baseline-normalized margin by effective receiver offset delta."""
    fig, ax = plt.subplots(figsize=(8.6, 4.8), constrained_layout=True)
    for row in rows:
        color = CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64")
        x_value = float(row["effective_offset_delta_from_baseline_cells"])
        y_value = float(row["base_margin_ratio_to_baseline"])
        ax.scatter(x_value, y_value, s=90, c=color, edgecolor="#263238", linewidth=0.8, zorder=3)
        xytext, ha = _plot_annotation(row)
        ax.annotate(_plot_label(row), (x_value, y_value), textcoords="offset points", xytext=xytext, ha=ha, fontsize=7.5)
    ax.axhline(1.0, color="#263238", linestyle="--", linewidth=1.0)
    ax.set_xlabel("Effective receiver-offset delta from Tx/Rx=50 baseline (cells)")
    ax.set_ylabel("Base margin / Tx/Rx=50 base margin")
    ax.set_title("Linear Receiver Target-2 Margin Threshold")
    ratios = [float(row["base_margin_ratio_to_baseline"]) for row in rows]
    ax.set_ylim(min(ratios) * 0.90, max(ratios) * 1.08)
    ax.grid(alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_margin_by_txrx(rows: list[dict], save_path: Path) -> None:
    """Plot base margins by requested Tx/Rx offset."""
    rows = sorted(rows, key=lambda row: float(row["tx_rx_offset_mm"]))
    fig, ax = plt.subplots(figsize=(8.6, 4.8), constrained_layout=True)
    for row in rows:
        color = CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64")
        marker = "s" if row["receiver_sampling"] == "nearest" else "o"
        ax.scatter(
            float(row["tx_rx_offset_mm"]),
            float(row["base_radius_margin_abs"]),
            s=90,
            c=color,
            marker=marker,
            edgecolor="#263238",
            linewidth=0.8,
            zorder=3,
        )
        xytext, ha = _plot_annotation(row)
        ax.annotate(_plot_label(row), (float(row["tx_rx_offset_mm"]), float(row["base_radius_margin_abs"])), textcoords="offset points", xytext=xytext, ha=ha, fontsize=7.5)
    ax.set_xlabel("Requested Tx/Rx offset (mm)")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_title("Target-2 Base Margins: Nearest vs Linear Receiver Sampling")
    margins = [float(row["base_radius_margin_abs"]) for row in rows]
    ax.set_ylim(min(margins) * 0.92, max(margins) * 1.08)
    ax.grid(alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path, summary: dict) -> None:
    """Write figure notes for the linear receiver summary."""
    lines = [
        "# Figure Notes",
        "",
        "## 1. `linear_receiver_margin_ratio_by_offset_delta.png` - margin ratio by receiver perturbation",
        "",
        "This scatter plot compares each run's base radius margin against the",
        "Tx/Rx=50 baseline after converting receiver sampling to an effective",
        "offset delta in grid cells. A nonzero delta means the receiver trace",
        "contains contribution from the adjacent +51 receiver cell.",
        "",
        "## 2. `linear_receiver_base_margin_by_txrx.png` - base margin by requested Tx/Rx",
        "",
        "This scatter plot shows the same rows by requested Tx/Rx offset. Square",
        "markers are nearest-grid rows and circular markers are linear receiver",
        "sampling rows.",
        "",
        "Package summary:",
        f"- rows: {summary['row_count']}",
        f"- receiver sampling counts: {summary['receiver_sampling_counts']}",
        f"- confidence labels: {summary['confidence_label_counts']}",
        f"- nonzero linear rows: {summary['linear_nonzero_count']}",
        f"- all nonzero linear rows weak: {summary['all_nonzero_linear_weak']}",
        f"- smallest tested nonzero delta: {summary['smallest_tested_nonzero_delta_cells']}",
        "",
        "Inspect the offset-delta figure first when deciding whether another",
        "sub-grid bisection run is justified.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="*", default=DEFAULT_RUNS, help="LABEL=RUN_DIR")
    parser.add_argument("--baseline-label", default="nearest50")
    parser.add_argument("--run-name", default="linear_receiver_threshold_summary")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_specs = [parse_run_arg(value) for value in args.run]
    rows = [load_branch_run(label, path) for label, path in run_specs]
    rows = attach_baseline_fields(rows, args.baseline_label)
    summary = summarize_rows(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "linear_receiver_threshold_rows.csv"
    summary_json = data_dir / "linear_receiver_threshold_summary.json"
    delta_fig = figures_dir / "linear_receiver_margin_ratio_by_offset_delta.png"
    txrx_fig = figures_dir / "linear_receiver_base_margin_by_txrx.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    write_rows_csv(rows_csv, rows)
    summary_json.write_text(
        json.dumps({
            "input_runs": [{"label": label, "run_dir": str(path)} for label, path in run_specs],
            "summary": summary,
            "threshold_rows": rows,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    plot_margin_ratio_by_delta(rows, delta_fig)
    plot_margin_by_txrx(rows, txrx_fig)
    write_figure_notes(notes_path, summary)
    write_run_manifest(
        str(outdir),
        args.run_name,
        {
            "summary_json": str(summary_json),
            "threshold_rows_csv": str(rows_csv),
            "offset_delta_figure": str(delta_fig),
            "txrx_figure": str(txrx_fig),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote summary: {summary_json}")


if __name__ == "__main__":
    main()
