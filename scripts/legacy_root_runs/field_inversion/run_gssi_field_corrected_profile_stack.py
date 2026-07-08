#!/usr/bin/env python3
"""Build a time-zero-corrected short-profile B-scan stack for local GSSI data."""

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
from run_gssi_field_preprocess_feature_qc import imshow_extent, json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map  # noqa: E402
from run_gssi_field_short_profile_stack_policy import common_axis  # noqa: E402
from run_gssi_field_synthetic_waveform_probe import interpolate_matrix, robust_normalize  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, save_validated_figure  # noqa: E402


DEFAULT_STACK_RUN = "021_gssi51600s_short_profile_stack_policy"
DEFAULT_APPLIED_RUN = "025_gssi51600s_short_profile_time_zero_application_policy"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def align_matrix_to_reference(matrix: np.ndarray, orientation: str, lag_samples: int) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.float64)
    if orientation == "reversed":
        values = values[:, ::-1]
    elif orientation != "direct":
        raise ValueError(f"unknown orientation {orientation!r}")

    aligned = np.full(values.shape, np.nan, dtype=np.float64)
    if lag_samples > 0:
        aligned[:, :-lag_samples] = values[:, lag_samples:]
    elif lag_samples < 0:
        aligned[:, -lag_samples:] = values[:, :lag_samples]
    else:
        aligned[:, :] = values
    return aligned


def compare_matrices(reference: np.ndarray, comparison: np.ndarray) -> dict:
    ref = robust_normalize(np.asarray(reference, dtype=np.float64))
    cmp = robust_normalize(np.asarray(comparison, dtype=np.float64))
    mask = np.isfinite(ref) & np.isfinite(cmp)
    if int(np.count_nonzero(mask)) < 8:
        return {
            "valid_sample_count": int(np.count_nonzero(mask)),
            "normalized_correlation": math.nan,
            "absolute_correlation": math.nan,
            "polarity": "insufficient",
            "normalized_residual_rms": math.nan,
        }
    r = ref[mask]
    c = cmp[mask]
    denom = float(np.linalg.norm(r) * np.linalg.norm(c))
    corr = float(np.dot(r, c) / denom) if denom > 0.0 else math.nan
    polarity = "same" if math.isfinite(corr) and corr >= 0.0 else "opposite"
    signed = c if polarity == "same" else -c
    return {
        "valid_sample_count": int(np.count_nonzero(mask)),
        "normalized_correlation": corr,
        "absolute_correlation": abs(corr) if math.isfinite(corr) else math.nan,
        "polarity": polarity,
        "normalized_residual_rms": float(np.sqrt(np.mean((r - signed) ** 2))),
    }


def column_agreement_rows(
    x_m: np.ndarray,
    reference: np.ndarray,
    raw_comparison: np.ndarray,
    corrected_comparison: np.ndarray,
) -> list[dict]:
    rows: list[dict] = []
    for col, x_val in enumerate(np.asarray(x_m, dtype=np.float64)):
        raw = compare_matrices(reference[:, [col]], raw_comparison[:, [col]])
        corrected = compare_matrices(reference[:, [col]], corrected_comparison[:, [col]])
        raw_abs = safe_float(raw.get("absolute_correlation"))
        corrected_abs = safe_float(corrected.get("absolute_correlation"))
        rows.append({
            "column_index": col,
            "x_m": float(x_val),
            "x_mm": 1000.0 * float(x_val),
            "raw_abs_correlation": raw_abs,
            "corrected_abs_correlation": corrected_abs,
            "abs_correlation_improvement": (
                corrected_abs - raw_abs
                if math.isfinite(raw_abs) and math.isfinite(corrected_abs)
                else math.nan
            ),
            "raw_residual_rms": safe_float(raw.get("normalized_residual_rms")),
            "corrected_residual_rms": safe_float(corrected.get("normalized_residual_rms")),
            "raw_valid_sample_count": int(raw.get("valid_sample_count", 0)),
            "corrected_valid_sample_count": int(corrected.get("valid_sample_count", 0)),
        })
    return rows


def summarize_corrected_stack(
    rows: list[dict],
    raw_matrix_compare: dict,
    corrected_matrix_compare: dict,
    *,
    transfer_offset_ns: float,
    orientation: str,
    lag_samples: int,
    lag_mm: float,
) -> dict:
    improvements = [
        safe_float(row.get("abs_correlation_improvement"))
        for row in rows
        if math.isfinite(safe_float(row.get("abs_correlation_improvement")))
    ]
    corrected_corr = [
        safe_float(row.get("corrected_abs_correlation"))
        for row in rows
        if math.isfinite(safe_float(row.get("corrected_abs_correlation")))
    ]
    improved_count = sum(1 for value in improvements if value > 0.0)
    row_count = len(improvements)
    raw_abs = safe_float(raw_matrix_compare.get("absolute_correlation"))
    corrected_abs = safe_float(corrected_matrix_compare.get("absolute_correlation"))
    matrix_improvement = corrected_abs - raw_abs if math.isfinite(raw_abs) and math.isfinite(corrected_abs) else math.nan
    improvement_fraction = improved_count / row_count if row_count else math.nan

    if (
        math.isfinite(matrix_improvement)
        and matrix_improvement > 0.05
        and math.isfinite(improvement_fraction)
        and improvement_fraction >= 0.55
        and corrected_abs >= 0.65
    ):
        label = "corrected_profile_stack_time_zero_supported"
    elif math.isfinite(matrix_improvement) and matrix_improvement > 0.0:
        label = "corrected_profile_stack_time_zero_limited"
    else:
        label = "corrected_profile_stack_time_zero_not_supported"

    return {
        "policy_label": label,
        "orientation": orientation,
        "lag_samples": lag_samples,
        "lag_mm": lag_mm,
        "applied_transfer_offset_ns": transfer_offset_ns,
        "column_count": len(rows),
        "finite_column_count": row_count,
        "improved_column_count": improved_count,
        "improved_column_fraction": improvement_fraction,
        "mean_column_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "min_column_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "max_column_abs_correlation_improvement": max(improvements) if improvements else math.nan,
        "mean_corrected_column_abs_correlation": float(np.mean(corrected_corr)) if corrected_corr else math.nan,
        "raw_matrix_abs_correlation": raw_abs,
        "corrected_matrix_abs_correlation": corrected_abs,
        "matrix_abs_correlation_improvement": matrix_improvement,
        "raw_matrix_residual_rms": safe_float(raw_matrix_compare.get("normalized_residual_rms")),
        "corrected_matrix_residual_rms": safe_float(corrected_matrix_compare.get("normalized_residual_rms")),
        "valid_matrix_sample_count": int(corrected_matrix_compare.get("valid_sample_count", 0)),
        "policy": (
            "Use the corrected short-profile stack as measured-data timing and "
            "repeatability QC only. It is not field FWI, absolute time-zero, 3D "
            "geometry, radius, or cover-depth evidence."
        ),
    }


def build_profile_windows(
    profiles: dict,
    *,
    reference_stem: str,
    comparison_stem: str,
    time_window_ns: tuple[float, float],
    transfer_offset_ns: float,
    orientation: str,
    lag_samples: int,
) -> dict:
    reference = profiles[reference_stem]
    comparison = profiles[comparison_stem]
    x_m = common_axis(reference["x_m"], comparison["x_m"])
    time_mask = (reference["time_ns"] >= time_window_ns[0]) & (reference["time_ns"] <= time_window_ns[1])
    time_ns = np.asarray(reference["time_ns"][time_mask], dtype=np.float64)
    if time_ns.size < 8:
        raise ValueError(f"empty or too-short time window {time_window_ns}")
    reference_window = interpolate_matrix(
        reference["processed"]["corrected"],
        reference["x_m"],
        reference["time_ns"],
        x_m,
        time_ns,
    )
    comparison_raw = interpolate_matrix(
        comparison["processed"]["corrected"],
        comparison["x_m"],
        comparison["time_ns"],
        x_m,
        time_ns,
    )
    comparison_corrected = interpolate_matrix(
        comparison["processed"]["corrected"],
        comparison["x_m"],
        comparison["time_ns"],
        x_m,
        time_ns + transfer_offset_ns,
    )
    return {
        "x_m": x_m,
        "time_ns": time_ns,
        "reference_window": reference_window,
        "raw_aligned_comparison": align_matrix_to_reference(comparison_raw, orientation, lag_samples),
        "corrected_aligned_comparison": align_matrix_to_reference(comparison_corrected, orientation, lag_samples),
    }


def plot_corrected_stack(windows: dict, rows: list[dict], summary: dict, save_path: Path) -> str:
    x_m = windows["x_m"]
    time_ns = windows["time_ns"]
    reference = windows["reference_window"]
    raw = windows["raw_aligned_comparison"]
    corrected = windows["corrected_aligned_comparison"]
    stack = 0.5 * (robust_normalize(reference) + robust_normalize(corrected))
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

    fig, axes = plt.subplots(2, 2, figsize=(13.2, 8.6), constrained_layout=True)
    panels = [
        (axes[0, 0], reference, "014 reference"),
        (axes[0, 1], raw, f"016 aligned before time-zero |corr|={summary['raw_matrix_abs_correlation']:.3f}"),
        (axes[1, 0], corrected, f"016 aligned after time-zero |corr|={summary['corrected_matrix_abs_correlation']:.3f}"),
        (axes[1, 1], stack, "corrected normalized stack"),
    ]
    for ax, matrix, title in panels:
        image = ax.imshow(matrix, aspect="auto", extent=extent, cmap="seismic", vmin=limits[0], vmax=limits[1])
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("profile distance after alignment [m]")
        ax.set_ylabel("time [ns]")
        fig.colorbar(image, ax=ax, shrink=0.82)

    improved_x = [
        safe_float(row.get("x_m"))
        for row in rows
        if safe_float(row.get("abs_correlation_improvement")) > 0.0
    ]
    for ax in axes.ravel():
        for x_val in improved_x[:: max(1, len(improved_x) // 24)]:
            ax.axvline(x_val, color="#222222", alpha=0.12, linewidth=0.6)

    fig.suptitle(
        (
            "Short-profile corrected stack: "
            f"{summary['policy_label']}, matrix improvement="
            f"{summary['matrix_abs_correlation_improvement']:.3f}"
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
    parser.add_argument("--stack-run", default=DEFAULT_STACK_RUN)
    parser.add_argument("--applied-run", default=DEFAULT_APPLIED_RUN)
    parser.add_argument("--reference-stem", default="PROJECT001C__014")
    parser.add_argument("--comparison-stem", default="PROJECT001C__016")
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--run-name", default="gssi51600s_corrected_profile_stack")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_json = dataset_root / args.stack_run / "data" / "short_profile_stack_policy_summary.json"
    applied_json = dataset_root / args.applied_run / "data" / "short_profile_time_zero_application_summary.json"
    stack_root = json.loads(stack_json.read_text(encoding="utf-8"))
    applied_root = json.loads(applied_json.read_text(encoding="utf-8"))
    stack_summary = stack_root.get("summary", {})
    applied_summary = applied_root.get("summary", {})
    dx_m = safe_float(stack_root.get("dx_m"))
    lag_mm = safe_float(stack_summary.get("best_lag_mm"))
    lag_samples = int(round((lag_mm / 1000.0) / dx_m)) if math.isfinite(lag_mm) and dx_m > 0.0 else 0
    orientation = str(stack_summary.get("best_orientation", "direct"))
    transfer_offset_ns = safe_float(applied_summary.get("applied_transfer_offset_ns"))
    time_window = tuple(float(part.strip()) for part in args.time_window_ns.split(",", 1))

    profiles = load_profile_map(Path(args.input_dir))
    windows = build_profile_windows(
        profiles,
        reference_stem=args.reference_stem,
        comparison_stem=args.comparison_stem,
        time_window_ns=time_window,
        transfer_offset_ns=transfer_offset_ns,
        orientation=orientation,
        lag_samples=lag_samples,
    )
    raw_compare = compare_matrices(windows["reference_window"], windows["raw_aligned_comparison"])
    corrected_compare = compare_matrices(windows["reference_window"], windows["corrected_aligned_comparison"])
    rows = column_agreement_rows(
        windows["x_m"],
        windows["reference_window"],
        windows["raw_aligned_comparison"],
        windows["corrected_aligned_comparison"],
    )
    summary = summarize_corrected_stack(
        rows,
        raw_compare,
        corrected_compare,
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

    columns_csv = data_dir / "corrected_profile_stack_column_agreement.csv"
    summary_json = data_dir / "corrected_profile_stack_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_corrected_stack(windows, rows, summary, figures_dir / "corrected_profile_stack.png"))

    write_csv(columns_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "reference_stem": args.reference_stem,
        "comparison_stem": args.comparison_stem,
        "time_window_min_ns": time_window[0],
        "time_window_max_ns": time_window[1],
        "input_stack_summary_json": str(stack_json),
        "input_applied_summary_json": str(applied_json),
        "summary": summary,
        "paths": {
            "column_agreement_csv": str(columns_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_corrected_profile_stack",
        {
            "summary_json": str(summary_json),
            "column_agreement_csv": str(columns_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
