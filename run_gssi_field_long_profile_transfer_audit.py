#!/usr/bin/env python3
"""Audit whether the short-profile time-zero correction transfers to long profiles."""

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
    column_agreement_rows,
    compare_matrices,
    safe_float,
)
from run_gssi_field_preprocess_feature_qc import imshow_extent, json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import robust_normalize  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_LONG_STACK_RUN = "022_gssi51600s_long_profile_stack_policy"
DEFAULT_APPLIED_RUN = "025_gssi51600s_short_profile_time_zero_application_policy"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def crop_x_window(windows: dict, center_x_m: float, half_width_m: float) -> dict:
    x_m = np.asarray(windows["x_m"], dtype=np.float64)
    idx = np.where((x_m >= center_x_m - half_width_m) & (x_m <= center_x_m + half_width_m))[0]
    if idx.size == 0:
        raise ValueError(f"anchor window has no columns near x={center_x_m:.6f} m")
    sl = slice(int(idx[0]), int(idx[-1]) + 1)
    return {
        "x_m": x_m[sl],
        "time_ns": np.asarray(windows["time_ns"], dtype=np.float64),
        "reference_window": np.asarray(windows["reference_window"], dtype=np.float64)[:, sl],
        "raw_aligned_comparison": np.asarray(windows["raw_aligned_comparison"], dtype=np.float64)[:, sl],
        "corrected_aligned_comparison": np.asarray(windows["corrected_aligned_comparison"], dtype=np.float64)[:, sl],
        "column_start": int(idx[0]),
        "column_end": int(idx[-1]),
    }


def anchor_window_metric_rows(
    anchor_rows: list[dict],
    windows: dict,
    *,
    half_width_m: float,
    stable_only: bool = True,
) -> list[dict]:
    rows: list[dict] = []
    for anchor in anchor_rows:
        label = str(anchor.get("stability_label", ""))
        if stable_only and label != "stable_stack_anchor":
            continue
        center = safe_float(anchor.get("x_m"))
        if not math.isfinite(center):
            continue
        crop = crop_x_window(windows, center, half_width_m)
        raw_metrics = compare_matrices(crop["reference_window"], crop["raw_aligned_comparison"])
        corrected_metrics = compare_matrices(crop["reference_window"], crop["corrected_aligned_comparison"])
        raw_abs = safe_float(raw_metrics.get("absolute_correlation"))
        corrected_abs = safe_float(corrected_metrics.get("absolute_correlation"))
        rows.append({
            "anchor_index": int(safe_float(anchor.get("candidate_index"), len(rows) + 1)),
            "stability_label": label,
            "center_x_m": center,
            "center_x_mm": 1000.0 * center,
            "window_start_x_m": float(crop["x_m"][0]),
            "window_end_x_m": float(crop["x_m"][-1]),
            "window_length_m": float(crop["x_m"][-1] - crop["x_m"][0]),
            "raw_anchor_abs_correlation": raw_abs,
            "corrected_anchor_abs_correlation": corrected_abs,
            "anchor_abs_correlation_improvement": (
                corrected_abs - raw_abs if math.isfinite(raw_abs) and math.isfinite(corrected_abs) else math.nan
            ),
            "raw_anchor_residual_rms": safe_float(raw_metrics.get("normalized_residual_rms")),
            "corrected_anchor_residual_rms": safe_float(corrected_metrics.get("normalized_residual_rms")),
            "valid_anchor_sample_count": int(corrected_metrics.get("valid_sample_count", 0)),
        })
    return rows


def summarize_long_transfer_audit(
    column_rows: list[dict],
    anchor_rows: list[dict],
    raw_matrix_compare: dict,
    corrected_matrix_compare: dict,
    *,
    long_stack_summary: dict,
    transfer_offset_ns: float,
    orientation: str,
    lag_samples: int,
    lag_mm: float,
) -> dict:
    finite_columns = [
        row for row in column_rows
        if math.isfinite(safe_float(row.get("abs_correlation_improvement")))
    ]
    improvements = [safe_float(row.get("abs_correlation_improvement")) for row in finite_columns]
    corrected_columns = [
        safe_float(row.get("corrected_abs_correlation"))
        for row in finite_columns
        if math.isfinite(safe_float(row.get("corrected_abs_correlation")))
    ]
    improved_column_count = sum(1 for value in improvements if value > 0.0)
    improved_column_fraction = improved_column_count / len(finite_columns) if finite_columns else math.nan

    anchor_improvements = [
        safe_float(row.get("anchor_abs_correlation_improvement"))
        for row in anchor_rows
        if math.isfinite(safe_float(row.get("anchor_abs_correlation_improvement")))
    ]
    anchor_corrected = [
        safe_float(row.get("corrected_anchor_abs_correlation"))
        for row in anchor_rows
        if math.isfinite(safe_float(row.get("corrected_anchor_abs_correlation")))
    ]
    improved_anchor_count = sum(1 for value in anchor_improvements if value > 0.0)
    improved_anchor_fraction = improved_anchor_count / len(anchor_improvements) if anchor_improvements else math.nan

    raw_abs = safe_float(raw_matrix_compare.get("absolute_correlation"))
    corrected_abs = safe_float(corrected_matrix_compare.get("absolute_correlation"))
    matrix_improvement = corrected_abs - raw_abs if math.isfinite(raw_abs) and math.isfinite(corrected_abs) else math.nan
    missing_phase = bool(long_stack_summary.get("comparison_profile_missing_phase_anchor_picks", True))

    strong_matrix = (
        math.isfinite(matrix_improvement)
        and matrix_improvement > 0.05
        and math.isfinite(improved_column_fraction)
        and improved_column_fraction >= 0.55
        and corrected_abs >= 0.65
    )
    strong_anchors = (
        anchor_improvements
        and improved_anchor_fraction >= 0.5
        and min(anchor_corrected or [0.0]) >= 0.65
    )
    weak_improvement = (
        math.isfinite(matrix_improvement)
        and matrix_improvement > 0.0
        and math.isfinite(improved_column_fraction)
        and improved_column_fraction >= 0.45
    )

    if missing_phase and strong_matrix and strong_anchors:
        label = "long_profile_short_correction_pattern_only_transfer"
    elif weak_improvement:
        label = "long_profile_short_correction_limited_pattern_only"
    else:
        label = "long_profile_short_correction_transfer_not_supported"

    return {
        "policy_label": label,
        "reference_stem": "PROJECT001C__015",
        "comparison_stem": "PROJECT001C__013",
        "orientation": orientation,
        "lag_samples": lag_samples,
        "lag_mm": lag_mm,
        "applied_short_pair_transfer_offset_ns": transfer_offset_ns,
        "long_stack_policy_label": long_stack_summary.get("policy_label", "unknown"),
        "long_pair_missing_phase_anchor_picks": missing_phase,
        "raw_matrix_abs_correlation": raw_abs,
        "corrected_matrix_abs_correlation": corrected_abs,
        "matrix_abs_correlation_improvement": matrix_improvement,
        "finite_column_count": len(finite_columns),
        "improved_column_count": improved_column_count,
        "improved_column_fraction": improved_column_fraction,
        "mean_column_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "min_column_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "mean_corrected_column_abs_correlation": float(np.mean(corrected_columns)) if corrected_columns else math.nan,
        "stable_anchor_window_count": len(anchor_improvements),
        "improved_anchor_window_count": improved_anchor_count,
        "improved_anchor_window_fraction": improved_anchor_fraction,
        "mean_anchor_abs_correlation_improvement": float(np.mean(anchor_improvements)) if anchor_improvements else math.nan,
        "min_anchor_abs_correlation_improvement": min(anchor_improvements) if anchor_improvements else math.nan,
        "min_corrected_anchor_abs_correlation": min(anchor_corrected) if anchor_corrected else math.nan,
        "policy": (
            "Audit only whether the short-profile relative time-zero correction "
            "numerically improves the long-profile 015/013 pattern alignment. "
            "Because profile 013 lacks phase-anchor picks and the survey is not "
            "a recovered 3D grid, this cannot support field event pairing, "
            "radius, cover-depth, 3D, or measured-data FWI claims."
        ),
    }


def plot_long_transfer_audit(windows: dict, column_rows: list[dict], anchor_rows: list[dict], summary: dict, save_path: Path) -> str:
    x_m = np.asarray(windows["x_m"], dtype=np.float64)
    time_ns = np.asarray(windows["time_ns"], dtype=np.float64)
    reference = np.asarray(windows["reference_window"], dtype=np.float64)
    raw = np.asarray(windows["raw_aligned_comparison"], dtype=np.float64)
    corrected = np.asarray(windows["corrected_aligned_comparison"], dtype=np.float64)
    residual = robust_normalize(reference) - robust_normalize(corrected)
    limits = safe_symmetric_limits(
        np.concatenate([
            reference[np.isfinite(reference)].ravel(),
            raw[np.isfinite(raw)].ravel(),
            corrected[np.isfinite(corrected)].ravel(),
        ]),
        percentile=98.0,
        floor=1.0,
    )
    extent = imshow_extent(x_m, time_ns)
    gain_x = np.asarray([safe_float(row.get("x_m")) for row in column_rows], dtype=np.float64)
    gain = np.asarray([safe_float(row.get("abs_correlation_improvement")) for row in column_rows], dtype=np.float64)

    fig, axes = plt.subplots(2, 2, figsize=(14.0, 8.4), constrained_layout=True)
    panels = [
        (axes[0, 0], reference, "015 reference", "seismic", limits),
        (axes[0, 1], raw, f"013 aligned before |corr|={summary['raw_matrix_abs_correlation']:.3f}", "seismic", limits),
        (axes[1, 0], corrected, f"013 after short correction |corr|={summary['corrected_matrix_abs_correlation']:.3f}", "seismic", limits),
        (axes[1, 1], residual, "normalized residual after correction", "coolwarm", (-2.5, 2.5)),
    ]
    for ax, matrix, title, cmap, clim in panels:
        image = ax.imshow(matrix, aspect="auto", extent=extent, cmap=cmap, vmin=clim[0], vmax=clim[1])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("aligned profile distance [m]")
        ax.set_ylabel("time [ns]")
        fig.colorbar(image, ax=ax, shrink=0.78)
        for anchor in anchor_rows:
            ax.axvline(safe_float(anchor.get("center_x_m")), color="#222222", alpha=0.28, linewidth=0.8)

    inset = axes[1, 1].inset_axes([0.08, 0.08, 0.84, 0.25])
    inset.plot(gain_x, gain, color="#2f9d55", linewidth=1.0)
    inset.axhline(0.0, color="#555555", linewidth=0.8)
    inset.set_title("column |corr| gain", fontsize=8)
    inset.tick_params(labelsize=7)
    inset.grid(color="#dddddd", linewidth=0.5)

    fig.suptitle(
        (
            "Long-profile short-correction transfer audit: "
            f"{summary['policy_label']}, matrix gain={summary['matrix_abs_correlation_improvement']:.3f}"
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
    parser.add_argument("--anchor-half-width-m", type=float, default=0.05)
    parser.add_argument("--run-name", default="gssi51600s_long_profile_transfer_audit")
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

    profiles = load_profile_map(Path(args.input_dir))
    windows = build_profile_windows(
        profiles,
        reference_stem=str(long_root.get("reference_stem", "PROJECT001C__015")),
        comparison_stem=str(long_root.get("comparison_stem", "PROJECT001C__013")),
        time_window_ns=time_window,
        transfer_offset_ns=transfer_offset_ns,
        orientation=orientation,
        lag_samples=lag_samples,
    )
    raw_compare = compare_matrices(windows["reference_window"], windows["raw_aligned_comparison"])
    corrected_compare = compare_matrices(windows["reference_window"], windows["corrected_aligned_comparison"])
    column_rows = column_agreement_rows(
        windows["x_m"],
        windows["reference_window"],
        windows["raw_aligned_comparison"],
        windows["corrected_aligned_comparison"],
    )
    anchor_rows = anchor_window_metric_rows(
        read_csv_rows(anchors_csv),
        windows,
        half_width_m=args.anchor_half_width_m,
        stable_only=True,
    )
    summary = summarize_long_transfer_audit(
        column_rows,
        anchor_rows,
        raw_compare,
        corrected_compare,
        long_stack_summary=long_summary,
        transfer_offset_ns=transfer_offset_ns,
        orientation=orientation,
        lag_samples=lag_samples,
        lag_mm=lag_mm,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    columns_csv = data_dir / "long_profile_transfer_column_agreement.csv"
    anchor_windows_csv = data_dir / "long_profile_transfer_anchor_windows.csv"
    summary_json = data_dir / "long_profile_transfer_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_long_transfer_audit(
            windows,
            column_rows,
            anchor_rows,
            summary,
            figures_dir / "long_profile_transfer_audit.png",
        )
    )

    write_csv(columns_csv, [json_safe(row) for row in column_rows])
    write_csv(anchor_windows_csv, [json_safe(row) for row in anchor_rows])
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
            "column_agreement_csv": str(columns_csv),
            "anchor_windows_csv": str(anchor_windows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_long_profile_transfer_audit",
        {
            "summary_json": str(summary_json),
            "column_agreement_csv": str(columns_csv),
            "anchor_windows_csv": str(anchor_windows_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
