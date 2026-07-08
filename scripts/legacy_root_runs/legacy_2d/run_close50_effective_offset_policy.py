#!/usr/bin/env python3
"""Summarize close50 requested Tx/Rx offsets against effective receiver offsets."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
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
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from run_multi_rebar_common_radius_profile import build_scan_positions  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_THRESHOLD_CSV = (
    "outputs/experiments/1268_close50_threshold_policy_after_txrx28p75_pilot/"
    "data/close50_threshold_by_txrx.csv"
)
DEFAULT_DUPLICATE_SUMMARY = (
    "outputs/experiments/1269_coordinate_optimizer_close50_seed21_sources4_txrx29p375_objectives/"
    "data/multi_rebar_coordinate_optimizer_summary.json"
)


def read_csv_rows(path: str | Path) -> list[dict]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def effective_offsets_from_positions(positions: list[tuple], dx_mm: float) -> dict:
    """Return effective receiver offsets and a duplicate-detection signature."""
    source_indices = []
    receiver_offsets = []
    receiver_signature_parts = []
    for position in positions:
        src_ix = int(position[1])
        source_indices.append(src_ix)
        if len(position) == 4:
            rec_ix = int(position[3])
            receiver_offsets.append((rec_ix - src_ix) * float(dx_mm))
            receiver_signature_parts.append(str(rec_ix))
        elif len(position) == 6:
            rec_left = int(position[3])
            rec_right = int(position[4])
            weight = float(position[5])
            receiver_offsets.append(((1.0 - weight) * rec_left + weight * rec_right - src_ix) * float(dx_mm))
            receiver_signature_parts.append(f"{rec_left}:{rec_right}:{weight:.9f}")
        else:
            raise ValueError("scan positions must have 4 or 6 entries")
    return {
        "source_indices": source_indices,
        "effective_receiver_offsets_mm": receiver_offsets,
        "receiver_signature": "|".join(receiver_signature_parts),
        "mean_effective_receiver_offset_mm": float(np.mean(receiver_offsets)),
        "min_effective_receiver_offset_mm": float(np.min(receiver_offsets)),
        "max_effective_receiver_offset_mm": float(np.max(receiver_offsets)),
        "unique_effective_receiver_offset_count": len({round(value, 9) for value in receiver_offsets}),
    }


def layout_for_requested_offset(
    tx_rx_offset_mm: float,
    *,
    sources: int,
    grid_step_mm: float,
    receiver_sampling: str,
) -> dict:
    """Build the source/receiver layout for one requested Tx/Rx offset."""
    _override_grid(grid_step_mm)
    positions, scan_x = build_scan_positions(
        cfg.INVERSION_SCAN_STEP,
        int(sources),
        tx_rx_offset_m=float(tx_rx_offset_mm) / 1000.0,
        receiver_sampling=receiver_sampling,
    )
    layout = effective_offsets_from_positions(positions, cfg.DX * 1000.0)
    layout.update({
        "scan_x_values_mm": [float(value * 1000.0) for value in scan_x],
        "receiver_sampling": receiver_sampling,
        "sources": int(sources),
        "grid_step_mm": float(grid_step_mm),
        "requested_tx_rx_offset_mm": float(tx_rx_offset_mm),
    })
    return layout


def confidence_summary_from_optimizer(summary: dict) -> dict:
    rows = list(summary.get("confidence_rows", []))
    truth_count = 0
    ambiguity_count = 0
    margins = []
    truth_x = list(summary.get("true_x_values_mm", []))
    truth_z = list(summary.get("true_z_values_mm", []))
    truth_r = list(summary.get("truth_radius_values_mm", []))
    for row in rows:
        target_index = int(safe_float(row.get("step_target_index"), -1))
        if (
            0 <= target_index < len(truth_x)
            and safe_float(row.get("best_x_mm")) == safe_float(truth_x[target_index])
            and safe_float(row.get("best_z_mm")) == safe_float(truth_z[target_index])
            and safe_float(row.get("best_radius_mm")) == safe_float(truth_r[target_index])
        ):
            truth_count += 1
        x_width = safe_float(row.get("ambiguity_x_max_mm")) - safe_float(row.get("ambiguity_x_min_mm"))
        radius_width = safe_float(row.get("ambiguity_radius_max_mm")) - safe_float(row.get("ambiguity_radius_min_mm"))
        if (math.isfinite(x_width) and x_width > 0.0) or (math.isfinite(radius_width) and radius_width > 0.0):
            ambiguity_count += 1
        margin = safe_float(row.get("radius_margin_abs"))
        if math.isfinite(margin):
            margins.append(margin)
    return {
        "row_count": len(rows),
        "truth_geometry_count": truth_count,
        "truth_geometry_fraction": truth_count / len(rows) if rows else math.nan,
        "x_ambiguity_row_count": ambiguity_count,
        "radius_margin_abs_min": min(margins) if margins else math.nan,
        "radius_margin_abs_mean": float(np.mean(margins)) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
    }


def build_effective_offset_rows(
    threshold_rows: list[dict],
    duplicate_summaries: list[dict],
    *,
    sources: int,
    grid_step_mm: float,
    receiver_sampling: str,
) -> list[dict]:
    rows: list[dict] = []
    for threshold in threshold_rows:
        tx_rx = safe_float(threshold.get("tx_rx_offset_mm"))
        layout = layout_for_requested_offset(
            tx_rx,
            sources=int(safe_float(threshold.get("sources"), sources)),
            grid_step_mm=grid_step_mm,
            receiver_sampling=receiver_sampling,
        )
        rows.append({
            **threshold,
            **layout,
            "evidence_scope": threshold.get("replication_scope", ""),
            "source_summary_path": threshold.get("summary_path", ""),
        })
    for summary in duplicate_summaries:
        tx_rx = safe_float(summary.get("tx_rx_offset_mm"))
        layout = layout_for_requested_offset(
            tx_rx,
            sources=int(safe_float(summary.get("sources"), sources)),
            grid_step_mm=grid_step_mm,
            receiver_sampling=summary.get("receiver_sampling", receiver_sampling),
        )
        rows.append({
            "evidence": f"run{summary.get('run_name', 'duplicate_check')}",
            "acquisition_key": f"sources={summary.get('sources')}|tx_rx_offset_mm={tx_rx:g}|duplicate_check",
            "sources": safe_float(summary.get("sources")),
            "tx_rx_offset_mm": tx_rx,
            **confidence_summary_from_optimizer(summary),
            "branch_policy_label": "duplicate_effective_geometry_check",
            "replication_scope": "single_seed_duplicate_check",
            "summary_path": "",
            **layout,
            "evidence_scope": "single_seed_duplicate_check",
            "source_summary_path": "",
        })
    rows = sorted(rows, key=lambda row: safe_float(row.get("requested_tx_rx_offset_mm")))
    first_seen: dict[str, float] = {}
    for row in rows:
        signature = f"{row['receiver_sampling']}|{row['sources']}|{row['receiver_signature']}"
        requested = safe_float(row["requested_tx_rx_offset_mm"])
        if signature in first_seen:
            row["duplicate_effective_layout"] = True
            row["duplicate_of_requested_tx_rx_offset_mm"] = first_seen[signature]
        else:
            row["duplicate_effective_layout"] = False
            row["duplicate_of_requested_tx_rx_offset_mm"] = math.nan
            first_seen[signature] = requested
    return rows


def summarize_effective_offset_policy(rows: list[dict]) -> dict:
    duplicates = [
        row for row in rows
        if bool(row.get("duplicate_effective_layout"))
    ]
    clean_rows = [
        row for row in rows
        if row.get("branch_policy_label") == "clean_replicated"
    ]
    nonclean_rows = [
        row for row in rows
        if row.get("branch_policy_label") not in {"clean_replicated", "duplicate_effective_geometry_check"}
    ]
    first_clean = min(clean_rows, key=lambda row: safe_float(row["requested_tx_rx_offset_mm"])) if clean_rows else None
    last_nonclean = max(
        nonclean_rows,
        key=lambda row: safe_float(row["mean_effective_receiver_offset_mm"]),
    ) if nonclean_rows else None
    return {
        "policy_label": "close50_nearest_receiver_bisection_quantized_stop",
        "requested_offset_count": len(rows),
        "duplicate_effective_layout_count": len(duplicates),
        "duplicate_requested_tx_rx_offsets_mm": ",".join(
            f"{safe_float(row['requested_tx_rx_offset_mm']):g}" for row in duplicates
        ),
        "first_clean_requested_tx_rx_offset_mm": (
            safe_float(first_clean["requested_tx_rx_offset_mm"]) if first_clean else math.nan
        ),
        "first_clean_mean_effective_offset_mm": (
            safe_float(first_clean["mean_effective_receiver_offset_mm"]) if first_clean else math.nan
        ),
        "last_nonclean_mean_effective_offset_mm": (
            safe_float(last_nonclean["mean_effective_receiver_offset_mm"]) if last_nonclean else math.nan
        ),
        "next_action": (
            "Stop nearest-sampled sub-millimeter bisection on this close50 branch. "
            "The requested 29.375 mm probe duplicates the effective 29 mm receiver "
            "layout from 28.75 mm, while requested 30 mm maps to effective 30 mm "
            "and is already clean in the replicated aggregate. If the below-30 "
            "transition must be studied, run one deliberately scoped linear "
            "receiver-sampling pilot or a finer-grid pilot instead of more "
            "nearest-sampled midpoint probes."
        ),
    }


def plot_effective_offsets(rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: safe_float(row["requested_tx_rx_offset_mm"]))
    requested = [safe_float(row["requested_tx_rx_offset_mm"]) for row in ordered]
    effective = [safe_float(row["mean_effective_receiver_offset_mm"]) for row in ordered]
    colors = []
    for row in ordered:
        label = row.get("branch_policy_label")
        if label == "clean_replicated":
            colors.append("#2f9d55")
        elif label == "duplicate_effective_geometry_check":
            colors.append("#f58518")
        else:
            colors.append("#c7302b")
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 4.8), constrained_layout=True)
    axes[0].scatter(requested, effective, c=colors, s=78)
    for row, x, y in zip(ordered, requested, effective):
        marker = " dup" if row.get("duplicate_effective_layout") else ""
        axes[0].annotate(f"{x:g}{marker}", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)
    axes[0].plot([min(requested), max(requested)], [min(requested), max(requested)], color="#777777", linewidth=0.8, linestyle="--")
    axes[0].set_xlabel("requested Tx/Rx offset [mm]")
    axes[0].set_ylabel("mean effective receiver offset [mm]")
    axes[0].set_title("Nearest receiver quantization")
    axes[0].grid(color="#dddddd", linewidth=0.6)

    width = [safe_float(row["max_effective_receiver_offset_mm"]) - safe_float(row["min_effective_receiver_offset_mm"]) for row in ordered]
    axes[1].bar(requested, width, color=colors, width=0.62)
    axes[1].set_xlabel("requested Tx/Rx offset [mm]")
    axes[1].set_ylabel("effective-offset spread [mm]")
    axes[1].set_title("Per-source offset spread")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold-csv", default=DEFAULT_THRESHOLD_CSV)
    parser.add_argument("--duplicate-summary", action="append", default=None)
    parser.add_argument("--sources", type=int, default=4)
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--receiver-sampling", choices=["nearest", "linear"], default="nearest")
    parser.add_argument("--run-name", default="close50_effective_offset_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    threshold_rows = read_csv_rows(args.threshold_csv)
    duplicate_paths = [Path(path) for path in (args.duplicate_summary or [DEFAULT_DUPLICATE_SUMMARY])]
    duplicate_summaries = [read_json(path) for path in duplicate_paths if path.exists()]
    rows = build_effective_offset_rows(
        threshold_rows,
        duplicate_summaries,
        sources=args.sources,
        grid_step_mm=args.grid_step_mm,
        receiver_sampling=args.receiver_sampling,
    )
    summary = summarize_effective_offset_policy(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close50_effective_offset_rows.csv"
    summary_json = data_dir / "close50_effective_offset_summary.json"
    figure_path = Path(plot_effective_offsets(rows, summary, figures_dir / "close50_effective_offset_policy.png"))
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "threshold_csv": args.threshold_csv,
        "duplicate_summaries": [str(path) for path in duplicate_paths if path.exists()],
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_effective_offset_policy",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
