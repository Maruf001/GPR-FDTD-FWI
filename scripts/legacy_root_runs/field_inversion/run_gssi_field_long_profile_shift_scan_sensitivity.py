#!/usr/bin/env python3
"""Check long-profile shift-scan stability across shallow time windows."""

from __future__ import annotations

import argparse
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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_long_profile_shift_scan import (  # noqa: E402
    DEFAULT_APPLIED_RUN,
    DEFAULT_LONG_STACK_RUN,
    read_csv_rows,
    scan_offsets,
    summarize_shift_scan,
)
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_windows(value: str) -> list[tuple[float, float]]:
    windows: list[tuple[float, float]] = []
    for item in str(value).split(";"):
        item = item.strip()
        if not item:
            continue
        start, stop = [float(part.strip()) for part in item.split(",", 1)]
        if stop <= start:
            raise ValueError(f"invalid time window {item!r}")
        windows.append((start, stop))
    if not windows:
        raise ValueError("at least one time window is required")
    return windows


def summarize_sensitivity(rows: list[dict]) -> dict:
    best_offsets = [
        safe_float(row.get("best_matrix_offset_ns"))
        for row in rows
        if math.isfinite(safe_float(row.get("best_matrix_offset_ns")))
    ]
    best_gains = [
        safe_float(row.get("best_matrix_gain_vs_zero"))
        for row in rows
        if math.isfinite(safe_float(row.get("best_matrix_gain_vs_zero")))
    ]
    short_gains = [
        safe_float(row.get("short_pair_offset_gain_vs_zero"))
        for row in rows
        if math.isfinite(safe_float(row.get("short_pair_offset_gain_vs_zero")))
    ]
    anchor_counts = [
        safe_float(row.get("best_anchor_improved_window_count"))
        for row in rows
        if math.isfinite(safe_float(row.get("best_anchor_improved_window_count")))
    ]
    reject_count = sum(1 for row in rows if row.get("policy_label") == "long_profile_shift_scan_rejects_short_transfer")
    offset_spread = max(best_offsets) - min(best_offsets) if best_offsets else math.nan
    robust = (
        len(rows) > 0
        and reject_count == len(rows)
        and math.isfinite(offset_spread)
        and offset_spread <= 0.03
        and best_gains
        and min(best_gains) > 0.05
        and anchor_counts
        and min(anchor_counts) >= 3
        and short_gains
        and max(short_gains) < 0.0
    )
    if robust:
        label = "long_profile_pattern_shift_window_robust_rejects_short_transfer"
    elif reject_count:
        label = "long_profile_pattern_shift_window_variable_rejects_short_transfer"
    else:
        label = "long_profile_pattern_shift_window_not_stable"
    return {
        "policy_label": label,
        "window_count": len(rows),
        "reject_short_transfer_window_count": reject_count,
        "best_offset_min_ns": min(best_offsets) if best_offsets else math.nan,
        "best_offset_max_ns": max(best_offsets) if best_offsets else math.nan,
        "best_offset_spread_ns": offset_spread,
        "best_offset_median_ns": float(np.median(best_offsets)) if best_offsets else math.nan,
        "min_best_matrix_gain_vs_zero": min(best_gains) if best_gains else math.nan,
        "max_short_pair_offset_gain_vs_zero": max(short_gains) if short_gains else math.nan,
        "min_best_anchor_improved_window_count": min(anchor_counts) if anchor_counts else math.nan,
        "policy": (
            "Use this only to decide whether the long-profile pattern-only "
            "shift is stable enough for QC visualization. It does not create "
            "phase-anchor, absolute time-zero, 3D, radius, cover-depth, or FWI "
            "evidence."
        ),
    }


def plot_sensitivity(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [str(row.get("window_label")) for row in rows]
    x = np.arange(len(rows))
    best_offsets = np.asarray([safe_float(row.get("best_matrix_offset_ns")) for row in rows], dtype=np.float64)
    best_gains = np.asarray([safe_float(row.get("best_matrix_gain_vs_zero")) for row in rows], dtype=np.float64)
    short_gains = np.asarray([safe_float(row.get("short_pair_offset_gain_vs_zero")) for row in rows], dtype=np.float64)
    anchor_counts = np.asarray([safe_float(row.get("best_anchor_improved_window_count")) for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(11.8, 8.4), constrained_layout=True)
    axes[0].plot(x, best_offsets, marker="o", color="#4c78a8", linewidth=1.4)
    axes[0].axhline(safe_float(summary.get("best_offset_median_ns")), color="#555555", linestyle="--", linewidth=0.9)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("best offset [ns]")
    axes[0].set_title("Best long-profile pattern shift by time window")
    axes[0].grid(color="#dddddd", linewidth=0.6)

    axes[1].bar(x - 0.18, best_gains, width=0.36, color="#2f9d55", label="best gain")
    axes[1].bar(x + 0.18, short_gains, width=0.36, color="#c7302b", label="short-offset gain")
    axes[1].axhline(0.0, color="#555555", linewidth=0.8)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("gain vs zero")
    axes[1].set_title("Best shift remains positive while short-pair offset hurts")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(x, anchor_counts, color="#f58518", width=0.5)
    axes[2].set_xticks(x, labels)
    axes[2].set_ylabel("improved anchors")
    axes[2].set_title("Stable anchor-window support at each best shift")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        (
            "Long-profile shift-window sensitivity: "
            f"{summary['policy_label']}, offset spread={summary['best_offset_spread_ns']:.3f} ns"
        ),
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--long-stack-run", default=DEFAULT_LONG_STACK_RUN)
    parser.add_argument("--applied-run", default=DEFAULT_APPLIED_RUN)
    parser.add_argument("--time-windows-ns", default="0.40,1.15;0.45,1.25;0.50,1.35")
    parser.add_argument("--shift-min-ns", type=float, default=-0.25)
    parser.add_argument("--shift-max-ns", type=float, default=0.25)
    parser.add_argument("--shift-step-ns", type=float, default=0.01)
    parser.add_argument("--anchor-half-width-m", type=float, default=0.05)
    parser.add_argument("--run-name", default="gssi51600s_long_profile_shift_scan_sensitivity")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    long_json = dataset_root / args.long_stack_run / "data" / "long_profile_stack_policy_summary.json"
    anchors_csv = dataset_root / args.long_stack_run / "data" / "long_profile_stack_anchor_candidates.csv"
    applied_json = dataset_root / args.applied_run / "data" / "short_profile_time_zero_application_summary.json"
    long_root = json.loads(long_json.read_text(encoding="utf-8"))
    applied_root = json.loads(applied_json.read_text(encoding="utf-8"))
    long_summary = long_root.get("summary", {})
    applied_summary = applied_root.get("summary", {})
    dx_m = safe_float(long_root.get("dx_m"))
    lag_mm = safe_float(long_summary.get("best_lag_mm"))
    lag_samples = int(round((lag_mm / 1000.0) / dx_m)) if math.isfinite(lag_mm) and dx_m > 0.0 else 0
    orientation = str(long_summary.get("best_orientation", "direct"))
    transfer_offset_ns = safe_float(applied_summary.get("applied_transfer_offset_ns"))
    offsets = np.arange(args.shift_min_ns, args.shift_max_ns + 0.5 * args.shift_step_ns, args.shift_step_ns)
    if not np.any(np.isclose(offsets, 0.0)):
        offsets = np.sort(np.append(offsets, 0.0))
    if math.isfinite(transfer_offset_ns) and not np.any(np.isclose(offsets, transfer_offset_ns, atol=0.5 * args.shift_step_ns)):
        offsets = np.sort(np.append(offsets, transfer_offset_ns))

    profiles = load_profile_map(Path(args.input_dir))
    anchor_candidates = read_csv_rows(anchors_csv)
    rows: list[dict] = []
    for start_ns, stop_ns in parse_windows(args.time_windows_ns):
        scan_rows = scan_offsets(
            profiles,
            anchor_candidates,
            reference_stem=str(long_root.get("reference_stem", "PROJECT001C__015")),
            comparison_stem=str(long_root.get("comparison_stem", "PROJECT001C__013")),
            time_window_ns=(start_ns, stop_ns),
            orientation=orientation,
            lag_samples=lag_samples,
            offsets_ns=offsets,
            anchor_half_width_m=args.anchor_half_width_m,
        )
        window_summary = summarize_shift_scan(
            scan_rows,
            short_pair_transfer_offset_ns=transfer_offset_ns,
            long_pair_missing_phase_anchor_picks=bool(
                long_summary.get("comparison_profile_missing_phase_anchor_picks", True)
            ),
            offset_step_ns=args.shift_step_ns,
        )
        rows.append({
            "window_label": f"{start_ns:.2f}-{stop_ns:.2f} ns",
            "time_window_min_ns": start_ns,
            "time_window_max_ns": stop_ns,
            **window_summary,
        })
    summary = summarize_sensitivity(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "long_profile_shift_scan_sensitivity_rows.csv"
    summary_json = data_dir / "long_profile_shift_scan_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_sensitivity(rows, summary, figures_dir / "long_profile_shift_scan_sensitivity.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "input_long_stack_summary_json": str(long_json),
        "input_anchor_candidates_csv": str(anchors_csv),
        "input_applied_time_zero_summary_json": str(applied_json),
        "time_windows_ns": args.time_windows_ns,
        "anchor_half_width_m": args.anchor_half_width_m,
        **summary,
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
        "gssi_field_long_profile_shift_scan_sensitivity",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
