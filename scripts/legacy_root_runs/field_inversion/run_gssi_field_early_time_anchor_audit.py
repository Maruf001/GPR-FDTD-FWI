#!/usr/bin/env python3
"""Audit early-time common-mode anchors in local GSSI field profiles."""

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
from run_gssi_dzt_qc import (  # noqa: E402
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_corrected_profile_stack import safe_float  # noqa: E402
from run_gssi_field_preprocess_feature_qc import build_axes, json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_TIME_ZERO_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_LONG_SHIFT_SENSITIVITY_RUN = "055_gssi51600s_long_profile_shift_scan_sensitivity"

WINDOWS = (
    ("early_0p00_0p55", 0.0, 0.55),
    ("early_0p00_0p70", 0.0, 0.70),
    ("early_0p10_0p55", 0.10, 0.55),
    ("shallow_0p55_1p60", 0.55, 1.60),
)

PAIR_DEFINITIONS = (
    ("short_014_016", "014", "016"),
    ("long_015_013", "015", "013"),
)


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def profile_id(record: dict) -> str:
    stem = str(record.get("stem") or Path(str(record.get("file", ""))).stem)
    return stem.split("__")[-1]


def normalized(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    center = float(np.nanmedian(arr))
    out = arr - center
    scale = float(np.nanmax(np.abs(out))) if np.any(np.isfinite(out)) else 0.0
    if not math.isfinite(scale) or scale <= 0.0:
        return np.zeros_like(out, dtype=np.float64)
    return out / scale


def median_trace(raw: np.ndarray) -> np.ndarray:
    arr = np.asarray(raw, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError("DZT profile array must be two-dimensional")
    return np.nanmedian(arr, axis=1)


def window_indices(time_ns: np.ndarray, window_min_ns: float, window_max_ns: float) -> np.ndarray:
    mask = (time_ns >= window_min_ns) & (time_ns <= window_max_ns)
    indices = np.flatnonzero(mask)
    if indices.size < 5:
        raise ValueError(
            f"time window {window_min_ns:g}-{window_max_ns:g} ns has fewer than 5 samples"
        )
    return indices


def first_threshold_time(time_ns: np.ndarray, values: np.ndarray, fraction: float) -> float:
    arr = np.asarray(values, dtype=np.float64)
    limit = fraction * float(np.nanmax(np.abs(arr)))
    if not math.isfinite(limit) or limit <= 0.0:
        return math.nan
    hits = np.flatnonzero(np.abs(arr) >= limit)
    return float(time_ns[int(hits[0])]) if hits.size else math.nan


def profile_feature_row(
    record: dict,
    raw: np.ndarray,
    *,
    window_label: str,
    window_min_ns: float,
    window_max_ns: float,
) -> dict:
    _x_m, time_ns = build_axes(record)
    indices = window_indices(time_ns, window_min_ns, window_max_ns)
    trace = normalized(median_trace(raw))
    values = trace[indices]
    times = time_ns[indices]
    abs_idx = int(np.nanargmax(np.abs(values)))
    pos_idx = int(np.nanargmax(values))
    neg_idx = int(np.nanargmin(values))
    dt_ns = float(np.median(np.diff(time_ns))) if time_ns.size > 1 else math.nan
    header_zero_samples = safe_float(record.get("header_time_zero_samples"))
    return {
        "profile_id": profile_id(record),
        "file": record.get("file", ""),
        "window_label": window_label,
        "window_min_ns": window_min_ns,
        "window_max_ns": window_max_ns,
        "samples": int(record.get("samples", raw.shape[0])),
        "traces": int(record.get("traces", raw.shape[1])),
        "dt_ns": dt_ns,
        "header_time_zero_samples": header_zero_samples,
        "header_time_zero_ns": header_zero_samples * dt_ns if math.isfinite(header_zero_samples) else math.nan,
        "max_abs_time_ns": float(times[abs_idx]),
        "max_abs_normalized_amplitude": float(values[abs_idx]),
        "positive_peak_time_ns": float(times[pos_idx]),
        "positive_peak_normalized_amplitude": float(values[pos_idx]),
        "negative_peak_time_ns": float(times[neg_idx]),
        "negative_peak_normalized_amplitude": float(values[neg_idx]),
        "first_abs_35pct_time_ns": first_threshold_time(times, values, 0.35),
        "first_abs_50pct_time_ns": first_threshold_time(times, values, 0.50),
        "rms_normalized_amplitude": float(np.sqrt(np.nanmean(values * values))),
        "claim_status": "early_common_mode_instrument_qc_not_absolute_time_zero",
    }


def normalized_window_trace(raw: np.ndarray, time_ns: np.ndarray, window_min_ns: float, window_max_ns: float) -> np.ndarray:
    indices = window_indices(time_ns, window_min_ns, window_max_ns)
    values = median_trace(raw)[indices].astype(np.float64)
    values = values - float(np.nanmean(values))
    rms = float(np.sqrt(np.nanmean(values * values)))
    if math.isfinite(rms) and rms > 0.0:
        values = values / rms
    return values


def lag_scan(
    reference: np.ndarray,
    comparison: np.ndarray,
    dt_ns: float,
    *,
    max_lag_samples: int = 40,
) -> list[dict]:
    """Return normalized lag-correlation rows.

    Positive lag means the comparison trace is later than the reference trace
    by ``lag_samples * dt_ns`` under the comparison-minus-reference convention.
    """
    ref = np.asarray(reference, dtype=np.float64)
    cmp = np.asarray(comparison, dtype=np.float64)
    rows: list[dict] = []
    for lag in range(-max_lag_samples, max_lag_samples + 1):
        if lag < 0:
            a = ref[-lag:]
            b = cmp[: a.size]
        elif lag > 0:
            a = ref[:-lag]
            b = cmp[lag:]
        else:
            a = ref
            b = cmp
        if a.size < 5:
            continue
        a = a - float(np.nanmean(a))
        b = b - float(np.nanmean(b))
        denominator = math.sqrt(float(np.nansum(a * a) * np.nansum(b * b)))
        correlation = float(np.nansum(a * b) / denominator) if denominator > 0.0 else math.nan
        rows.append(
            {
                "lag_samples": int(lag),
                "comparison_minus_reference_shift_ns": float(lag * dt_ns),
                "normalized_correlation": correlation,
                "overlap_sample_count": int(a.size),
            }
        )
    return rows


def best_lag_row(rows: list[dict]) -> dict:
    finite = [row for row in rows if math.isfinite(safe_float(row.get("normalized_correlation")))]
    if not finite:
        raise ValueError("no finite lag-correlation rows")
    ranked = sorted(finite, key=lambda row: safe_float(row["normalized_correlation"]), reverse=True)
    best = dict(ranked[0])
    second = safe_float(ranked[1]["normalized_correlation"]) if len(ranked) > 1 else math.nan
    best["second_best_normalized_correlation"] = second
    best["best_minus_second_correlation"] = (
        safe_float(best["normalized_correlation"]) - second if math.isfinite(second) else math.nan
    )
    return best


def pair_lag_rows(
    profiles: list[tuple[dict, np.ndarray]],
    *,
    max_lag_samples: int,
) -> list[dict]:
    by_id = {profile_id(record): (record, raw) for record, raw in profiles}
    rows: list[dict] = []
    for pair_label, reference_id, comparison_id in PAIR_DEFINITIONS:
        if reference_id not in by_id or comparison_id not in by_id:
            continue
        reference_record, reference_raw = by_id[reference_id]
        comparison_record, comparison_raw = by_id[comparison_id]
        _x_m, time_ns = build_axes(reference_record)
        dt_ns = float(np.median(np.diff(time_ns))) if time_ns.size > 1 else math.nan
        for window_label, window_min_ns, window_max_ns in WINDOWS:
            reference_trace = normalized_window_trace(reference_raw, time_ns, window_min_ns, window_max_ns)
            comparison_trace = normalized_window_trace(comparison_raw, time_ns, window_min_ns, window_max_ns)
            best = best_lag_row(lag_scan(reference_trace, comparison_trace, dt_ns, max_lag_samples=max_lag_samples))
            rows.append(
                {
                    "pair_label": pair_label,
                    "reference_profile_id": reference_id,
                    "comparison_profile_id": comparison_id,
                    "window_label": window_label,
                    "window_min_ns": window_min_ns,
                    "window_max_ns": window_max_ns,
                    "dt_ns": dt_ns,
                    **best,
                    "claim_status": "early_common_mode_lag_qc_not_absolute_time_zero",
                }
            )
    return rows


def build_profile_feature_rows(profiles: list[tuple[dict, np.ndarray]]) -> list[dict]:
    rows: list[dict] = []
    for record, raw in profiles:
        for window_label, window_min_ns, window_max_ns in WINDOWS:
            rows.append(
                profile_feature_row(
                    record,
                    raw,
                    window_label=window_label,
                    window_min_ns=window_min_ns,
                    window_max_ns=window_max_ns,
                )
            )
    return rows


def find_pair_window(rows: list[dict], pair_label: str, window_label: str) -> dict:
    for row in rows:
        if row.get("pair_label") == pair_label and row.get("window_label") == window_label:
            return row
    return {}


def summarize_early_time_audit(
    feature_rows: list[dict],
    lag_rows: list[dict],
    time_zero_budget: dict,
    long_shift_sensitivity: dict | None = None,
) -> dict:
    primary_window = "early_0p00_0p55"
    short_primary = find_pair_window(lag_rows, "short_014_016", primary_window)
    long_primary = find_pair_window(lag_rows, "long_015_013", primary_window)
    content_offset = safe_float(time_zero_budget.get("relative_anchor_offset_ns"))
    conservative_half_width = safe_float(time_zero_budget.get("conservative_half_width_ns"))
    short_shift = safe_float(short_primary.get("comparison_minus_reference_shift_ns"))
    long_shift = safe_float(long_primary.get("comparison_minus_reference_shift_ns"))
    short_delta = abs(short_shift - content_offset)
    short_agrees = bool(
        math.isfinite(short_delta)
        and math.isfinite(conservative_half_width)
        and short_delta <= conservative_half_width
    )
    primary_features = [row for row in feature_rows if row.get("window_label") == primary_window]
    max_abs_times = [safe_float(row.get("max_abs_time_ns")) for row in primary_features]
    peak_span = max(max_abs_times) - min(max_abs_times) if max_abs_times else math.nan
    long_pattern_offset = safe_float((long_shift_sensitivity or {}).get("best_offset_median_ns"))
    long_delta = abs(long_shift - long_pattern_offset)
    policy_label = (
        "field_early_time_common_mode_not_content_time_zero"
        if not short_agrees
        else "field_early_time_common_mode_matches_content_offset_review"
    )
    return {
        "policy_label": policy_label,
        "profile_count": len({row.get("profile_id") for row in feature_rows}),
        "feature_row_count": len(feature_rows),
        "pair_window_row_count": len(lag_rows),
        "primary_window_label": primary_window,
        "early_peak_time_span_ns": peak_span,
        "early_peak_time_median_ns": float(np.median(np.asarray(max_abs_times, dtype=np.float64))) if max_abs_times else math.nan,
        "short_pair_content_offset_ns": content_offset,
        "short_pair_conservative_half_width_ns": conservative_half_width,
        "short_pair_early_shift_ns": short_shift,
        "short_pair_early_normalized_correlation": safe_float(short_primary.get("normalized_correlation")),
        "short_pair_early_lag_samples": safe_float(short_primary.get("lag_samples")),
        "short_pair_early_vs_content_delta_ns": short_delta,
        "short_pair_early_agrees_with_content_budget": short_agrees,
        "long_pair_early_shift_ns": long_shift,
        "long_pair_early_normalized_correlation": safe_float(long_primary.get("normalized_correlation")),
        "long_pair_pattern_offset_median_ns": long_pattern_offset,
        "long_pair_early_vs_pattern_delta_ns": long_delta,
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "gpu_priority": "none",
        "ready_for_manuscript_field_boundary": True,
        "decision": (
            "Use the early-time median trace as an instrument/common-mode QC "
            "negative control only. The short 014/016 early window aligns at "
            f"{short_shift:.6f} ns, which differs from the content-backed "
            f"{content_offset:.6f} ns relative offset by {short_delta:.6f} ns. "
            "Therefore the early direct/ringdown component should not be used "
            "as an absolute time-zero calibration or as a replacement for the "
            "content-backed short-pair timing policy."
        ),
    }


def plot_early_time_audit(
    profiles: list[tuple[dict, np.ndarray]],
    feature_rows: list[dict],
    lag_rows: list[dict],
    summary: dict,
    save_path: Path,
) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(17.0, 5.6), constrained_layout=True)
    colors = {
        "013": "#4c78a8",
        "014": "#2f9d55",
        "015": "#f58518",
        "016": "#c7302b",
    }
    for record, raw in sorted(profiles, key=lambda item: profile_id(item[0])):
        _x_m, time_ns = build_axes(record)
        trace = normalized(median_trace(raw))
        mask = (time_ns >= 0.0) & (time_ns <= 0.85)
        pid = profile_id(record)
        axes[0].plot(time_ns[mask], trace[mask], label=pid, linewidth=1.7, color=colors.get(pid))
    axes[0].axvspan(0.0, 0.55, color="#dddddd", alpha=0.35, label="primary early window")
    axes[0].set_xlabel("time [ns]")
    axes[0].set_ylabel("normalized median amplitude")
    axes[0].set_title("Early common-mode median traces")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    labels = [f"{row['pair_label'].replace('_', ' ')}\n{row['window_label'].replace('_', ' ')}" for row in lag_rows]
    x = np.arange(len(lag_rows))
    shifts = [safe_float(row["comparison_minus_reference_shift_ns"]) for row in lag_rows]
    correlations = [safe_float(row["normalized_correlation"]) for row in lag_rows]
    axes[1].bar(x, shifts, color="#4c78a8", edgecolor="#333333")
    content = safe_float(summary.get("short_pair_content_offset_ns"))
    half_width = safe_float(summary.get("short_pair_conservative_half_width_ns"))
    if math.isfinite(content):
        axes[1].axhline(content, color="#c7302b", linewidth=1.8, label="short content offset")
    if math.isfinite(content) and math.isfinite(half_width):
        axes[1].axhspan(content - half_width, content + half_width, color="#c7302b", alpha=0.12)
    axes[1].set_xticks(x, labels, rotation=45, ha="right")
    axes[1].set_ylabel("comparison-reference shift [ns]")
    axes[1].set_title("Early-window lag estimates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    primary = [row for row in feature_rows if row.get("window_label") == summary["primary_window_label"]]
    px = np.arange(len(primary))
    axes[2].bar(
        px - 0.24,
        [safe_float(row["max_abs_time_ns"]) for row in primary],
        width=0.24,
        color="#2f9d55",
        label="max abs",
    )
    axes[2].bar(
        px,
        [safe_float(row["positive_peak_time_ns"]) for row in primary],
        width=0.24,
        color="#4c78a8",
        label="positive peak",
    )
    axes[2].bar(
        px + 0.24,
        [safe_float(row["negative_peak_time_ns"]) for row in primary],
        width=0.24,
        color="#f58518",
        label="negative peak",
    )
    axes[2].set_xticks(px, [row["profile_id"] for row in primary])
    axes[2].set_ylabel("time [ns]")
    axes[2].set_title("Primary early-pulse pick times")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[2].legend(frameon=False, fontsize=8)
    axes[2].text(
        0.02,
        0.98,
        (
            f"short early shift={summary['short_pair_early_shift_ns']:.6f} ns\n"
            f"content offset={summary['short_pair_content_offset_ns']:.6f} ns\n"
            f"absolute_t0_ready={summary['absolute_time_zero_ready']} | gpu={summary['gpu_priority']}"
        ),
        transform=axes[2].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#bbbbbb"},
    )

    fig.suptitle(f"GSSI 51600S early-time anchor audit: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--time-zero-budget-run", default=DEFAULT_TIME_ZERO_BUDGET_RUN)
    parser.add_argument("--long-shift-sensitivity-run", default=DEFAULT_LONG_SHIFT_SENSITIVITY_RUN)
    parser.add_argument("--max-lag-samples", type=int, default=40)
    parser.add_argument("--run-name", default="gssi51600s_field_early_time_anchor_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    profiles = read_dzt_profiles(Path(args.input_dir))
    feature_rows = build_profile_feature_rows(profiles)
    lag_rows = pair_lag_rows(profiles, max_lag_samples=args.max_lag_samples)
    time_zero_budget = read_json(
        dataset_root
        / args.time_zero_budget_run
        / "data"
        / "field_time_zero_uncertainty_budget_summary.json"
    )
    long_shift_sensitivity_path = (
        dataset_root
        / args.long_shift_sensitivity_run
        / "data"
        / "long_profile_shift_scan_sensitivity_summary.json"
    )
    long_shift_sensitivity = read_json(long_shift_sensitivity_path) if long_shift_sensitivity_path.exists() else {}
    summary = summarize_early_time_audit(
        feature_rows,
        lag_rows,
        time_zero_budget,
        long_shift_sensitivity,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    feature_csv = data_dir / "field_early_time_profile_features.csv"
    lag_csv = data_dir / "field_early_time_pair_lags.csv"
    summary_json = data_dir / "field_early_time_anchor_audit_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_early_time_audit(
        profiles,
        feature_rows,
        lag_rows,
        summary,
        figures_dir / "field_early_time_anchor_audit.png",
    ))

    write_csv(feature_csv, [json_safe(row) for row in feature_rows])
    write_csv(lag_csv, [json_safe(row) for row in lag_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "runs": {
            "time_zero_budget": args.time_zero_budget_run,
            "long_shift_sensitivity": args.long_shift_sensitivity_run,
        },
        **summary,
        "paths": {
            "profile_features_csv": str(feature_csv),
            "pair_lags_csv": str(lag_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
        "readgssi_version": readgssi_version(),
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_early_time_anchor_audit",
        {
            "summary_json": str(summary_json),
            "profile_features_csv": str(feature_csv),
            "pair_lags_csv": str(lag_csv),
            "figure_validation_csv": str(validation_csv),
            "readgssi_version": readgssi_version(),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
