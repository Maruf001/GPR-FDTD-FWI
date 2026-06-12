#!/usr/bin/env python3
"""Summarize the seed89 target-2 Tx/Rx acquisition-threshold branch."""

from __future__ import annotations

import argparse
import csv
import json
import math
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

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_RUNS = [
    "txrx50=outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives",
    "txrx50p625=outputs/experiments/763_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p625_ringdown025_objectives",
    "txrx51p25=outputs/experiments/762_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx51p25_ringdown025_objectives",
    "txrx52p5=outputs/experiments/761_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx52p5_ringdown025_objectives",
    "txrx55=outputs/experiments/760_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx55_ringdown025_objectives",
    "txrx60=outputs/experiments/755_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx60_ringdown025_objectives",
]

CONFIDENCE_COLORS = {
    "strong": "#2E7D32",
    "moderate": "#F9A825",
    "weak": "#D32F2F",
    "ambiguous": "#6A1B9A",
}


def parse_run_arg(value: str) -> tuple[str, Path]:
    """Parse a labelled run directory argument."""
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


def _as_float(row: dict, key: str) -> float:
    return float(row[key])


def _as_int(row: dict, key: str) -> int:
    return int(float(row[key]))


def _run_index(path: Path) -> int | None:
    match = re.match(r"^(\d+)_", path.name)
    return int(match.group(1)) if match else None


def _compact_float(value: float) -> str:
    text = f"{float(value):.6f}".rstrip("0").rstrip(".")
    return text or "0"


def receiver_layout(
    scan_x_values_mm: list[float],
    tx_rx_offset_mm: float,
    grid_step_mm: float,
    *,
    pml_thickness_mm: float | None = None,
    domain_x_mm: float | None = None,
) -> dict:
    """Return the effective source/receiver grid layout for a Tx/Rx offset."""
    if grid_step_mm <= 0.0:
        raise ValueError("grid_step_mm must be positive")
    if tx_rx_offset_mm < 0.0:
        raise ValueError("tx_rx_offset_mm must be non-negative")
    if not scan_x_values_mm:
        raise ValueError("scan_x_values_mm must not be empty")

    if pml_thickness_mm is None:
        pml_thickness_mm = float(cfg.NPML * cfg.DX * 1000.0)
    if domain_x_mm is None:
        domain_x_mm = float(cfg.DOMAIN_X * 1000.0)

    npml = max(8, int(round(pml_thickness_mm / grid_step_mm)))
    nx_inner = int(round(domain_x_mm / grid_step_mm))
    max_rec_ix = nx_inner + npml - 1

    src_ix_values = []
    raw_rec_ix_values = []
    rec_ix_values = []
    receiver_offsets_cells = []
    raw_receiver_offsets_cells = []
    clamped_flags = []

    for x_mm in scan_x_values_mm:
        src_ix = int(np.round(float(x_mm) / grid_step_mm)) + npml
        raw_rec_ix = int(np.round((float(x_mm) + tx_rx_offset_mm) / grid_step_mm)) + npml
        rec_ix = min(raw_rec_ix, max_rec_ix)
        src_ix_values.append(src_ix)
        raw_rec_ix_values.append(raw_rec_ix)
        rec_ix_values.append(rec_ix)
        receiver_offsets_cells.append(rec_ix - src_ix)
        raw_receiver_offsets_cells.append(raw_rec_ix - src_ix)
        clamped_flags.append(raw_rec_ix > max_rec_ix)

    unclamped_offsets = [
        offset for offset, clamped in zip(receiver_offsets_cells, clamped_flags)
        if not clamped
    ]
    mode_source = unclamped_offsets if unclamped_offsets else receiver_offsets_cells
    dominant_offset = Counter(mode_source).most_common(1)[0][0]

    return {
        "grid_step_mm": float(grid_step_mm),
        "npml": int(npml),
        "max_receiver_ix": int(max_rec_ix),
        "scan_x_values_mm": [float(value) for value in scan_x_values_mm],
        "source_ix_values": src_ix_values,
        "raw_receiver_ix_values": raw_rec_ix_values,
        "receiver_ix_values": rec_ix_values,
        "receiver_offsets_cells": receiver_offsets_cells,
        "raw_receiver_offsets_cells": raw_receiver_offsets_cells,
        "clamped_receiver_flags": clamped_flags,
        "clamped_receiver_count": int(sum(clamped_flags)),
        "dominant_unclamped_receiver_offset_cells": int(dominant_offset),
        "receiver_layout_key": ",".join(str(value) for value in receiver_offsets_cells),
    }


def _is_truth_geometry(row: dict, truth_x_mm: float, truth_z_mm: float, truth_radius_mm: float) -> bool:
    return (
        math.isclose(_as_float(row, "best_x_mm"), truth_x_mm, rel_tol=0.0, abs_tol=1e-9)
        and math.isclose(_as_float(row, "best_z_mm"), truth_z_mm, rel_tol=0.0, abs_tol=1e-9)
        and math.isclose(_as_float(row, "best_radius_mm"), truth_radius_mm, rel_tol=0.0, abs_tol=1e-9)
    )


def best_truth_preserving_diagnostic(
    diagnostic_rows: list[dict],
    truth_x_mm: float,
    truth_z_mm: float,
    truth_radius_mm: float,
) -> dict:
    """Select the largest-margin diagnostic row that preserves the true geometry."""
    truth_rows = [
        row for row in diagnostic_rows
        if _is_truth_geometry(row, truth_x_mm, truth_z_mm, truth_radius_mm)
    ]
    candidates = truth_rows if truth_rows else diagnostic_rows
    return max(candidates, key=lambda row: _as_float(row, "radius_margin_abs"))


def load_threshold_run(label: str, run_dir: Path) -> dict:
    """Load one coordinate-optimizer run into a threshold-summary row."""
    data_dir = run_dir / "data"
    summary_path = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    with summary_path.open("r", encoding="utf-8") as handle:
        summary = json.load(handle)

    confidence = _read_single_csv_row(data_dir / "coordinate_confidence_report.csv")
    diagnostics = _read_csv_rows(data_dir / "coordinate_objective_diagnostics.csv")
    base_diag = next(row for row in diagnostics if row["objective_label"] == "base")

    target_index = _as_int(confidence, "target_rebar_index")
    truth_x_mm = float(summary["true_x_values_mm"][target_index])
    truth_z_mm = float(summary["true_z_values_mm"][target_index])
    truth_radius_mm = float(summary["truth_radius_values_mm"][target_index])
    tx_rx_offset_mm = float(summary["tx_rx_offset_mm"])
    grid_step_mm = float(summary["grid_step_mm"])
    scan_x_values_mm = [float(value) for value in summary["scan_x_values_mm"]]
    layout = receiver_layout(scan_x_values_mm, tx_rx_offset_mm, grid_step_mm)
    best_diag = best_truth_preserving_diagnostic(
        diagnostics,
        truth_x_mm,
        truth_z_mm,
        truth_radius_mm,
    )
    base_margin = _as_float(confidence, "radius_margin_abs")
    best_margin = _as_float(best_diag, "radius_margin_abs")

    return {
        "label": label,
        "run_index": _run_index(run_dir),
        "run_name": summary["run_name"],
        "run_path": str(run_dir),
        "target_index": target_index,
        "sources": int(summary["sources"]),
        "grid_step_mm": grid_step_mm,
        "tx_rx_offset_mm": tx_rx_offset_mm,
        "scan_x_values_mm": ";".join(_compact_float(value) for value in scan_x_values_mm),
        "source_ix_values": ";".join(str(value) for value in layout["source_ix_values"]),
        "receiver_ix_values": ";".join(str(value) for value in layout["receiver_ix_values"]),
        "raw_receiver_ix_values": ";".join(str(value) for value in layout["raw_receiver_ix_values"]),
        "receiver_offsets_cells": ";".join(str(value) for value in layout["receiver_offsets_cells"]),
        "raw_receiver_offsets_cells": ";".join(str(value) for value in layout["raw_receiver_offsets_cells"]),
        "clamped_receiver_count": layout["clamped_receiver_count"],
        "dominant_unclamped_receiver_offset_cells": layout["dominant_unclamped_receiver_offset_cells"],
        "receiver_layout_key": layout["receiver_layout_key"],
        "truth_x_mm": truth_x_mm,
        "truth_z_mm": truth_z_mm,
        "truth_radius_mm": truth_radius_mm,
        "base_best_x_mm": _as_float(confidence, "best_x_mm"),
        "base_best_z_mm": _as_float(confidence, "best_z_mm"),
        "base_best_radius_mm": _as_float(confidence, "best_radius_mm"),
        "base_next_radius_mm": _as_float(confidence, "next_radius_mm"),
        "base_is_truth_geometry": _is_truth_geometry(base_diag, truth_x_mm, truth_z_mm, truth_radius_mm),
        "base_confidence_label": confidence["confidence_label"],
        "base_radius_margin_abs": base_margin,
        "base_radius_margin_rel": _as_float(confidence, "radius_margin_rel"),
        "base_best_misfit": _as_float(confidence, "best_misfit"),
        "base_next_radius_misfit": _as_float(confidence, "next_radius_misfit"),
        "best_truth_preserving_objective": best_diag["objective_label"],
        "best_truth_preserving_margin_abs": best_margin,
        "best_truth_preserving_ratio_to_base": best_margin / base_margin if base_margin else np.nan,
        "summary_json": str(summary_path),
    }


def attach_baseline_and_duplicate_fields(rows: list[dict], baseline_label: str) -> list[dict]:
    """Add baseline ratios and duplicate receiver-layout metadata to rows."""
    if not rows:
        raise ValueError("no threshold rows to summarize")
    baseline_matches = [row for row in rows if row["label"] == baseline_label]
    if len(baseline_matches) != 1:
        raise ValueError(f"expected one baseline row labelled {baseline_label!r}")
    baseline = baseline_matches[0]
    baseline_margin = float(baseline["base_radius_margin_abs"])
    baseline_layout_key = baseline["receiver_layout_key"]

    layout_groups = defaultdict(list)
    for row in rows:
        layout_groups[row["receiver_layout_key"]].append(float(row["tx_rx_offset_mm"]))

    enriched = []
    for row in rows:
        new_row = dict(row)
        duplicate_offsets = sorted(layout_groups[row["receiver_layout_key"]])
        new_row["base_margin_ratio_to_baseline"] = (
            float(row["base_radius_margin_abs"]) / baseline_margin if baseline_margin else np.nan
        )
        new_row["same_receiver_layout_as_baseline"] = row["receiver_layout_key"] == baseline_layout_key
        new_row["layout_duplicate_count"] = len(duplicate_offsets)
        new_row["layout_duplicate_tx_rx_offsets_mm"] = ";".join(
            _compact_float(value) for value in duplicate_offsets
        )
        enriched.append(new_row)
    return sorted(enriched, key=lambda row: (float(row["tx_rx_offset_mm"]), row["label"]))


def summarize_threshold_rows(rows: list[dict], baseline_label: str) -> dict:
    """Summarize the Tx/Rx target-2 threshold rows."""
    sorted_rows = sorted(rows, key=lambda row: float(row["tx_rx_offset_mm"]))
    layout_groups = defaultdict(list)
    for row in sorted_rows:
        layout_groups[row["receiver_layout_key"]].append(row)

    first_weak = next(
        (row for row in sorted_rows if row["base_confidence_label"] == "weak"),
        None,
    )
    preceding_nonweak = [
        row for row in sorted_rows
        if first_weak is not None
        and float(row["tx_rx_offset_mm"]) < float(first_weak["tx_rx_offset_mm"])
        and row["base_confidence_label"] != "weak"
    ]
    transition = None
    if first_weak is not None and preceding_nonweak:
        lower = preceding_nonweak[-1]
        transition = {
            "from_tx_rx_offset_mm": float(lower["tx_rx_offset_mm"]),
            "from_effective_receiver_offset_cells": int(lower["dominant_unclamped_receiver_offset_cells"]),
            "from_confidence_label": lower["base_confidence_label"],
            "to_tx_rx_offset_mm": float(first_weak["tx_rx_offset_mm"]),
            "to_effective_receiver_offset_cells": int(first_weak["dominant_unclamped_receiver_offset_cells"]),
            "to_confidence_label": first_weak["base_confidence_label"],
            "base_margin_ratio_to_baseline_at_transition": float(first_weak["base_margin_ratio_to_baseline"]),
        }

    duplicate_layout_groups = []
    for layout_key, members in sorted(layout_groups.items()):
        if len(members) > 1:
            duplicate_layout_groups.append({
                "receiver_layout_key": layout_key,
                "tx_rx_offsets_mm": [float(row["tx_rx_offset_mm"]) for row in members],
                "confidence_labels": [row["base_confidence_label"] for row in members],
                "base_margins": [float(row["base_radius_margin_abs"]) for row in members],
            })

    return {
        "baseline_label": baseline_label,
        "run_count": len(sorted_rows),
        "target_indices": sorted({int(row["target_index"]) for row in sorted_rows}),
        "all_base_truth_geometry": all(bool(row["base_is_truth_geometry"]) for row in sorted_rows),
        "confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in sorted_rows)),
        "best_truth_preserving_objective_counts": dict(
            Counter(row["best_truth_preserving_objective"] for row in sorted_rows)
        ),
        "unique_receiver_layout_count": len(layout_groups),
        "duplicate_receiver_layout_groups": duplicate_layout_groups,
        "first_weak_row": first_weak,
        "moderate_to_weak_transition": transition,
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write dictionary rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_base_margin_by_txrx(rows: list[dict], save_path: Path) -> None:
    """Plot target-2 base margins by requested Tx/Rx offset."""
    rows = sorted(rows, key=lambda row: float(row["tx_rx_offset_mm"]))
    x_values = [float(row["tx_rx_offset_mm"]) for row in rows]
    y_values = [float(row["base_radius_margin_abs"]) for row in rows]
    colors = [CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64") for row in rows]

    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    ax.plot(x_values, y_values, color="#263238", linewidth=1.5, alpha=0.65)
    ax.scatter(x_values, y_values, s=90, c=colors, edgecolor="#263238", linewidth=0.8, zorder=3)
    labelled_cells = set()
    for row, x_value, y_value in zip(rows, x_values, y_values):
        cell = int(row["dominant_unclamped_receiver_offset_cells"])
        if cell in labelled_cells:
            continue
        labelled_cells.add(cell)
        xytext = (-10, 12)
        ha = "right"
        ax.annotate(
            f"+{cell} cells",
            (x_value, y_value),
            textcoords="offset points",
            xytext=xytext,
            ha=ha,
            fontsize=8,
        )
    ax.set_xlabel("Requested Tx/Rx offset (mm)")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_title("Seed89 Target-2 Tx/Rx Base-Margin Threshold")
    ax.set_ylim(0.0, max(y_values) * 1.12)
    ax.grid(alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_base_margin_by_receiver_cell(rows: list[dict], save_path: Path) -> None:
    """Plot base-margin ratios by effective receiver-cell offset."""
    rows = sorted(rows, key=lambda row: (int(row["dominant_unclamped_receiver_offset_cells"]), float(row["tx_rx_offset_mm"])))
    rows_by_cell = defaultdict(list)
    for row in rows:
        rows_by_cell[int(row["dominant_unclamped_receiver_offset_cells"])].append(row)
    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    for cell, cell_rows in sorted(rows_by_cell.items()):
        jitters = np.linspace(-0.18, 0.18, len(cell_rows)) if len(cell_rows) > 1 else [0.0]
        for offset_index, (row, jitter) in enumerate(zip(cell_rows, jitters)):
            color = CONFIDENCE_COLORS.get(row["base_confidence_label"], "#455A64")
            x_value = cell + float(jitter)
            y_value = float(row["base_margin_ratio_to_baseline"])
            ax.scatter(
                x_value,
                y_value,
                s=90,
                c=color,
                edgecolor="#263238",
                linewidth=0.8,
                zorder=3,
            )
            if len(cell_rows) > 1 and offset_index == 0:
                xytext = (-6, 15)
                ha = "right"
            elif len(cell_rows) > 1:
                xytext = (6, 15)
                ha = "left"
            else:
                xytext = (0, 12)
                ha = "center"
            ax.annotate(
                f"{_compact_float(float(row['tx_rx_offset_mm']))} mm",
                (x_value, y_value),
                textcoords="offset points",
                xytext=xytext,
                ha=ha,
                fontsize=7.5,
                rotation=15 if len(cell_rows) > 1 else 0,
            )
    ax.axhline(1.0, color="#263238", linestyle="--", linewidth=1.0)
    ax.set_xlabel("Dominant effective receiver offset (grid cells)")
    ax.set_ylabel("Base margin / Tx/Rx=50 base margin")
    ax.set_title("Target-2 Margin Ratio by Effective Receiver Cell")
    ax.set_xticks(sorted({int(row["dominant_unclamped_receiver_offset_cells"]) for row in rows}))
    ratios = [float(row["base_margin_ratio_to_baseline"]) for row in rows]
    ax.set_ylim(min(ratios) * 0.88, max(ratios) * 1.08)
    ax.grid(alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path, summary: dict) -> None:
    """Write figure notes for Tx/Rx threshold summary figures."""
    transition = summary["moderate_to_weak_transition"]
    if transition is None:
        transition_text = "No moderate-to-weak transition was detected in the supplied rows."
    else:
        transition_text = (
            "The supplied rows show the first weak target-2 result when the "
            f"dominant effective receiver offset changes from "
            f"+{transition['from_effective_receiver_offset_cells']} cells to "
            f"+{transition['to_effective_receiver_offset_cells']} cells."
        )

    lines = [
        "# Figure Notes",
        "",
        "## 1. `txrx_target2_base_margin_by_requested_offset.png` - requested Tx/Rx threshold",
        "",
        "This line and scatter plot shows the production base objective's",
        "best-versus-next-radius gap for seed89 target 2 as the requested",
        "transmitter/receiver (Tx/Rx) offset changes. Point labels show the",
        "dominant effective receiver offset after grid-index rounding.",
        "",
        "## 2. `txrx_target2_margin_ratio_by_receiver_cell.png` - effective receiver-cell threshold",
        "",
        "This scatter plot divides each base margin by the Tx/Rx=50 mm base",
        "margin and places the points by effective receiver-cell offset. Duplicate",
        "requested offsets at the same receiver layout are jittered slightly so",
        "overlapping acquisition layouts are visible.",
        "",
        "Package summary:",
        f"- rows: {summary['run_count']}",
        f"- base truth geometry: {summary['all_base_truth_geometry']}",
        f"- confidence labels: {summary['confidence_label_counts']}",
        f"- unique receiver layouts: {summary['unique_receiver_layout_count']}",
        f"- duplicate receiver-layout groups: {len(summary['duplicate_receiver_layout_groups'])}",
        f"- transition: {transition_text}",
        "",
        "Inspect the receiver-cell figure first when deciding whether another",
        "fractional Tx/Rx GPU run would create new data or duplicate an existing",
        "receiver-index layout.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", nargs="*", default=DEFAULT_RUNS, help="LABEL=RUN_DIR")
    parser.add_argument("--baseline-label", default="txrx50")
    parser.add_argument("--run-name", default="txrx_target2_threshold_summary")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_specs = [parse_run_arg(value) for value in args.run]
    rows = [load_threshold_run(label, path) for label, path in run_specs]
    rows = attach_baseline_and_duplicate_fields(rows, args.baseline_label)
    summary = summarize_threshold_rows(rows, args.baseline_label)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "txrx_target2_threshold_rows.csv"
    summary_json = data_dir / "txrx_target2_threshold_summary.json"
    requested_fig = figures_dir / "txrx_target2_base_margin_by_requested_offset.png"
    receiver_fig = figures_dir / "txrx_target2_margin_ratio_by_receiver_cell.png"
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
    plot_base_margin_by_txrx(rows, requested_fig)
    plot_base_margin_by_receiver_cell(rows, receiver_fig)
    write_figure_notes(notes_path, summary)
    write_run_manifest(
        str(outdir),
        args.run_name,
        {
            "summary_json": str(summary_json),
            "threshold_rows_csv": str(rows_csv),
            "requested_offset_figure": str(requested_fig),
            "receiver_cell_figure": str(receiver_fig),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote summary: {summary_json}")


if __name__ == "__main__":
    main()
