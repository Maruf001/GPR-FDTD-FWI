#!/usr/bin/env python3
"""Scan long-profile time shifts without upgrading them to phase-anchor evidence."""

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

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import (  # noqa: E402
    build_profile_windows,
    compare_matrices,
    safe_float,
)
from run_gssi_field_long_profile_transfer_audit import (  # noqa: E402
    DEFAULT_APPLIED_RUN,
    DEFAULT_LONG_STACK_RUN,
    anchor_window_metric_rows,
    read_csv_rows,
)
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def scan_offsets(
    profiles: dict,
    anchor_candidates: list[dict],
    *,
    reference_stem: str,
    comparison_stem: str,
    time_window_ns: tuple[float, float],
    orientation: str,
    lag_samples: int,
    offsets_ns: np.ndarray,
    anchor_half_width_m: float,
) -> list[dict]:
    rows: list[dict] = []
    zero_corr = math.nan
    zero_residual = math.nan
    for offset in offsets_ns:
        windows = build_profile_windows(
            profiles,
            reference_stem=reference_stem,
            comparison_stem=comparison_stem,
            time_window_ns=time_window_ns,
            transfer_offset_ns=float(offset),
            orientation=orientation,
            lag_samples=lag_samples,
        )
        metrics = compare_matrices(windows["reference_window"], windows["corrected_aligned_comparison"])
        anchor_rows = anchor_window_metric_rows(
            anchor_candidates,
            windows,
            half_width_m=anchor_half_width_m,
            stable_only=True,
        )
        anchor_improvements = [
            safe_float(row.get("anchor_abs_correlation_improvement"))
            for row in anchor_rows
            if math.isfinite(safe_float(row.get("anchor_abs_correlation_improvement")))
        ]
        anchor_corr = [
            safe_float(row.get("corrected_anchor_abs_correlation"))
            for row in anchor_rows
            if math.isfinite(safe_float(row.get("corrected_anchor_abs_correlation")))
        ]
        corr = safe_float(metrics.get("absolute_correlation"))
        residual = safe_float(metrics.get("normalized_residual_rms"))
        if abs(float(offset)) < 1.0e-12:
            zero_corr = corr
            zero_residual = residual
        rows.append({
            "offset_ns": float(offset),
            "matrix_abs_correlation": corr,
            "matrix_residual_rms": residual,
            "matrix_abs_correlation_gain_vs_zero": math.nan,
            "matrix_residual_rms_change_vs_zero": math.nan,
            "stable_anchor_window_count": len(anchor_improvements),
            "improved_anchor_window_count": sum(1 for value in anchor_improvements if value > 0.0),
            "mean_anchor_abs_correlation_improvement": float(np.mean(anchor_improvements)) if anchor_improvements else math.nan,
            "min_anchor_abs_correlation_improvement": min(anchor_improvements) if anchor_improvements else math.nan,
            "mean_corrected_anchor_abs_correlation": float(np.mean(anchor_corr)) if anchor_corr else math.nan,
            "min_corrected_anchor_abs_correlation": min(anchor_corr) if anchor_corr else math.nan,
        })

    if math.isfinite(zero_corr):
        for row in rows:
            row["matrix_abs_correlation_gain_vs_zero"] = safe_float(row["matrix_abs_correlation"]) - zero_corr
            row["matrix_residual_rms_change_vs_zero"] = safe_float(row["matrix_residual_rms"]) - zero_residual
    return rows


def closest_row(rows: list[dict], offset_ns: float) -> dict:
    if not rows:
        return {}
    return min(rows, key=lambda row: abs(safe_float(row.get("offset_ns")) - offset_ns))


def summarize_shift_scan(
    rows: list[dict],
    *,
    short_pair_transfer_offset_ns: float,
    long_pair_missing_phase_anchor_picks: bool,
    offset_step_ns: float,
) -> dict:
    valid_rows = [row for row in rows if math.isfinite(safe_float(row.get("matrix_abs_correlation")))]
    zero = closest_row(valid_rows, 0.0)
    short = closest_row(valid_rows, short_pair_transfer_offset_ns)
    best_matrix = max(valid_rows, key=lambda row: safe_float(row.get("matrix_abs_correlation")), default={})
    best_anchor = max(
        valid_rows,
        key=lambda row: (
            safe_float(row.get("improved_anchor_window_count"), -1.0),
            safe_float(row.get("mean_anchor_abs_correlation_improvement"), -999.0),
            safe_float(row.get("matrix_abs_correlation"), -999.0),
        ),
        default={},
    )
    zero_corr = safe_float(zero.get("matrix_abs_correlation"))
    short_corr = safe_float(short.get("matrix_abs_correlation"))
    best_corr = safe_float(best_matrix.get("matrix_abs_correlation"))
    short_gain = short_corr - zero_corr if math.isfinite(short_corr) and math.isfinite(zero_corr) else math.nan
    best_gain = best_corr - zero_corr if math.isfinite(best_corr) and math.isfinite(zero_corr) else math.nan
    best_offset = safe_float(best_matrix.get("offset_ns"))
    short_scan_offset = safe_float(short.get("offset_ns"))
    best_anchor_count = safe_float(best_anchor.get("improved_anchor_window_count"))

    if math.isfinite(short_gain) and short_gain < 0.0 and math.isfinite(best_gain) and best_gain > 0.02:
        label = "long_profile_shift_scan_rejects_short_transfer"
    elif math.isfinite(best_gain) and best_gain > 0.05 and best_anchor_count >= 3:
        label = "long_profile_shift_scan_pattern_only_candidate"
    else:
        label = "long_profile_shift_scan_no_stable_transfer"

    return {
        "policy_label": label,
        "offset_step_ns": offset_step_ns,
        "scanned_offset_count": len(rows),
        "short_pair_transfer_offset_ns": short_pair_transfer_offset_ns,
        "nearest_short_pair_scan_offset_ns": short_scan_offset,
        "long_pair_missing_phase_anchor_picks": bool(long_pair_missing_phase_anchor_picks),
        "zero_offset_matrix_abs_correlation": zero_corr,
        "short_pair_offset_matrix_abs_correlation": short_corr,
        "short_pair_offset_gain_vs_zero": short_gain,
        "best_matrix_offset_ns": best_offset,
        "best_matrix_abs_correlation": best_corr,
        "best_matrix_gain_vs_zero": best_gain,
        "best_matrix_offset_distance_from_short_pair_ns": (
            abs(best_offset - short_pair_transfer_offset_ns)
            if math.isfinite(best_offset) and math.isfinite(short_pair_transfer_offset_ns)
            else math.nan
        ),
        "best_anchor_offset_ns": safe_float(best_anchor.get("offset_ns")),
        "best_anchor_improved_window_count": best_anchor_count,
        "best_anchor_mean_improvement": safe_float(best_anchor.get("mean_anchor_abs_correlation_improvement")),
        "best_anchor_min_corrected_abs_correlation": safe_float(best_anchor.get("min_corrected_anchor_abs_correlation")),
        "policy": (
            "Use this as a long-profile pattern-only shift audit. A scanned "
            "offset may describe shallow-pattern alignment, but profile 013 "
            "lacks phase-anchor picks, so this is not time-zero calibration, "
            "field inversion, 3D, radius, or cover-depth evidence."
        ),
    }


def plot_shift_scan(rows: list[dict], summary: dict, save_path: Path) -> str:
    offsets = np.asarray([safe_float(row.get("offset_ns")) for row in rows], dtype=np.float64)
    corr = np.asarray([safe_float(row.get("matrix_abs_correlation")) for row in rows], dtype=np.float64)
    gain = np.asarray([safe_float(row.get("matrix_abs_correlation_gain_vs_zero")) for row in rows], dtype=np.float64)
    anchors = np.asarray([safe_float(row.get("improved_anchor_window_count")) for row in rows], dtype=np.float64)
    anchor_mean = np.asarray([safe_float(row.get("mean_anchor_abs_correlation_improvement")) for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(12.8, 8.6), constrained_layout=True)
    axes[0].plot(offsets, corr, color="#4c78a8", linewidth=1.5)
    axes[0].set_ylabel("matrix |corr|")
    axes[0].set_title("Long-profile matrix agreement by scanned time shift")
    axes[0].grid(color="#dddddd", linewidth=0.6)

    axes[1].plot(offsets, gain, color="#2f9d55", linewidth=1.3)
    axes[1].axhline(0.0, color="#555555", linewidth=0.8)
    axes[1].set_ylabel("gain vs zero")
    axes[1].set_title("Matrix gain relative to zero shift")
    axes[1].grid(color="#dddddd", linewidth=0.6)

    axes[2].plot(offsets, anchors, color="#f58518", linewidth=1.3, label="improved anchors")
    axes[2].plot(offsets, anchor_mean, color="#7f3c8d", linewidth=1.1, label="mean anchor gain")
    axes[2].axhline(0.0, color="#555555", linewidth=0.8)
    axes[2].set_xlabel("comparison time shift [ns]")
    axes[2].set_ylabel("anchor metric")
    axes[2].set_title("Stable anchor-window response")
    axes[2].grid(color="#dddddd", linewidth=0.6)
    axes[2].legend(frameon=False, fontsize=8)

    for ax in axes:
        ax.axvline(0.0, color="#555555", linestyle="--", linewidth=0.9, alpha=0.8)
        ax.axvline(
            safe_float(summary.get("nearest_short_pair_scan_offset_ns")),
            color="#c7302b",
            linestyle="--",
            linewidth=0.9,
            alpha=0.85,
        )
        ax.axvline(
            safe_float(summary.get("best_matrix_offset_ns")),
            color="#2f9d55",
            linestyle=":",
            linewidth=1.2,
            alpha=0.9,
        )

    fig.suptitle(
        (
            "Long-profile time-shift scan: "
            f"{summary['policy_label']}, best gain={summary['best_matrix_gain_vs_zero']:.3f}"
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
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--shift-min-ns", type=float, default=-0.25)
    parser.add_argument("--shift-max-ns", type=float, default=0.25)
    parser.add_argument("--shift-step-ns", type=float, default=0.01)
    parser.add_argument("--anchor-half-width-m", type=float, default=0.05)
    parser.add_argument("--run-name", default="gssi51600s_long_profile_shift_scan")
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
    time_window = tuple(float(part.strip()) for part in args.time_window_ns.split(",", 1))
    if args.shift_step_ns <= 0.0:
        raise ValueError("--shift-step-ns must be positive")
    offsets = np.arange(args.shift_min_ns, args.shift_max_ns + 0.5 * args.shift_step_ns, args.shift_step_ns)
    if not np.any(np.isclose(offsets, 0.0)):
        offsets = np.sort(np.append(offsets, 0.0))
    if math.isfinite(transfer_offset_ns) and not np.any(np.isclose(offsets, transfer_offset_ns, atol=0.5 * args.shift_step_ns)):
        offsets = np.sort(np.append(offsets, transfer_offset_ns))

    profiles = load_profile_map(Path(args.input_dir))
    rows = scan_offsets(
        profiles,
        read_csv_rows(anchors_csv),
        reference_stem=str(long_root.get("reference_stem", "PROJECT001C__015")),
        comparison_stem=str(long_root.get("comparison_stem", "PROJECT001C__013")),
        time_window_ns=time_window,
        orientation=orientation,
        lag_samples=lag_samples,
        offsets_ns=offsets,
        anchor_half_width_m=args.anchor_half_width_m,
    )
    summary = summarize_shift_scan(
        rows,
        short_pair_transfer_offset_ns=transfer_offset_ns,
        long_pair_missing_phase_anchor_picks=bool(
            long_summary.get("comparison_profile_missing_phase_anchor_picks", True)
        ),
        offset_step_ns=args.shift_step_ns,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    scan_csv = data_dir / "long_profile_shift_scan.csv"
    summary_json = data_dir / "long_profile_shift_scan_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_shift_scan(rows, summary, figures_dir / "long_profile_shift_scan.png"))

    write_csv(scan_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "input_long_stack_summary_json": str(long_json),
        "input_anchor_candidates_csv": str(anchors_csv),
        "input_applied_time_zero_summary_json": str(applied_json),
        "time_window_min_ns": time_window[0],
        "time_window_max_ns": time_window[1],
        "anchor_half_width_m": args.anchor_half_width_m,
        "summary": summary,
        "paths": {
            "scan_csv": str(scan_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_long_profile_shift_scan",
        {
            "summary_json": str(summary_json),
            "scan_csv": str(scan_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
