#!/usr/bin/env python3
"""Quantify content-backed short-profile time-zero anchor evidence."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CONTENT_RUN = "031_gssi51600s_short_profile_content_window_policy"
DEFAULT_CONTENT_SYNTHETIC_RUN = "033_gssi51600s_short_profile_content_synthetic_policy"
DEFAULT_PANEL_RUN = "035_gssi51600s_content_backed_waveform_panels"


def read_csv_rows(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_safe(row.get(key, "")) for key in fieldnames})


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _panel_stats(panel_rows: list[dict]) -> dict:
    valid = [row for row in panel_rows if boolish(row.get("simulation_valid"))]
    correlations = [
        safe_float(row.get("absolute_correlation"))
        for row in valid
        if math.isfinite(safe_float(row.get("absolute_correlation")))
    ]
    residuals = [
        safe_float(row.get("normalized_residual_rms"))
        for row in valid
        if math.isfinite(safe_float(row.get("normalized_residual_rms")))
    ]
    shifts = [
        safe_float(row.get("synthetic_time_shift_ns"))
        for row in valid
        if math.isfinite(safe_float(row.get("synthetic_time_shift_ns")))
    ]
    return {
        "panel_count": len(panel_rows),
        "valid_panel_count": len(valid),
        "min_panel_absolute_correlation": min(correlations) if correlations else math.nan,
        "mean_panel_absolute_correlation": float(np.mean(correlations)) if correlations else math.nan,
        "max_panel_normalized_residual_rms": max(residuals) if residuals else math.nan,
        "mean_panel_normalized_residual_rms": float(np.mean(residuals)) if residuals else math.nan,
        "synthetic_time_shift_mean_ns": float(np.mean(shifts)) if shifts else math.nan,
        "synthetic_time_shift_span_ns": max(shifts) - min(shifts) if shifts else math.nan,
    }


def build_anchor_rows(
    event_rows: list[dict],
    match_rows: list[dict],
    panel_rows: list[dict],
    *,
    max_abs_content_residual_ns: float,
    min_abs_correlation: float,
    max_shift_span_ns: float,
) -> list[dict]:
    matches_by_pair = {
        int(safe_float(row.get("pair_index"), -1)): row
        for row in match_rows
    }
    panels_by_pair: dict[int, list[dict]] = {}
    for row in panel_rows:
        panels_by_pair.setdefault(int(safe_float(row.get("pair_index"), -1)), []).append(row)

    rows: list[dict] = []
    for event in sorted(event_rows, key=lambda row: int(safe_float(row.get("pair_index"), 0))):
        pair_index = int(safe_float(event.get("pair_index"), -1))
        match = matches_by_pair.get(pair_index, {})
        panels = panels_by_pair.get(pair_index, [])
        stats = _panel_stats(panels)
        content_backed = boolish(event.get("content_backed"))
        abs_residual = abs(safe_float(event.get("timing_residual_to_bootstrap_median_ns")))
        min_corr = safe_float(match.get("pair_min_absolute_correlation"), stats["min_panel_absolute_correlation"])
        shift_span = stats["synthetic_time_shift_span_ns"]
        supported = (
            content_backed
            and math.isfinite(abs_residual)
            and abs_residual <= max_abs_content_residual_ns
            and math.isfinite(min_corr)
            and min_corr >= min_abs_correlation
            and stats["valid_panel_count"] >= 2
            and (not math.isfinite(shift_span) or shift_span <= max_shift_span_ns)
        )
        if supported:
            label = "content_time_zero_anchor_supported"
        elif content_backed:
            label = "content_time_zero_anchor_limited"
        else:
            label = "timing_only_no_content_anchor"
        rows.append({
            "pair_index": pair_index,
            "content_backed": content_backed,
            "content_label": event.get("content_label", ""),
            "reference_apex_group": int(safe_float(event.get("reference_apex_group"), -1)),
            "comparison_apex_group": int(safe_float(event.get("comparison_apex_group"), -1)),
            "reference_x_mm": safe_float(event.get("reference_x_mm")),
            "comparison_aligned_x_mm": safe_float(event.get("comparison_aligned_x_mm")),
            "aligned_x_residual_mm": safe_float(event.get("aligned_x_residual_mm")),
            "nearest_anchor_distance_mm": safe_float(event.get("nearest_anchor_distance_mm")),
            "timing_residual_to_bootstrap_median_ns": safe_float(
                event.get("timing_residual_to_bootstrap_median_ns")
            ),
            "abs_timing_residual_to_bootstrap_median_ns": abs_residual,
            "within_bootstrap_ci_envelope": boolish(event.get("within_bootstrap_ci_envelope")),
            "pair_min_absolute_correlation": min_corr,
            "pair_mean_absolute_correlation": safe_float(match.get("pair_mean_absolute_correlation")),
            "waveform_support_label": match.get("waveform_support_label", ""),
            **stats,
            "anchor_policy_label": label,
        })
    return rows


def summarize_anchor_policy(
    rows: list[dict],
    *,
    max_abs_content_residual_ns: float,
    min_abs_correlation: float,
    max_shift_span_ns: float,
    min_supported_content_pairs: int,
) -> dict:
    content_rows = [row for row in rows if bool(row.get("content_backed"))]
    supported_rows = [
        row for row in content_rows
        if row.get("anchor_policy_label") == "content_time_zero_anchor_supported"
    ]
    timing_only_rows = [row for row in rows if not bool(row.get("content_backed"))]
    content_residuals = [
        safe_float(row.get("abs_timing_residual_to_bootstrap_median_ns"))
        for row in content_rows
        if math.isfinite(safe_float(row.get("abs_timing_residual_to_bootstrap_median_ns")))
    ]
    all_residuals = [
        safe_float(row.get("abs_timing_residual_to_bootstrap_median_ns"))
        for row in rows
        if math.isfinite(safe_float(row.get("abs_timing_residual_to_bootstrap_median_ns")))
    ]
    content_corr = [
        safe_float(row.get("pair_min_absolute_correlation"))
        for row in content_rows
        if math.isfinite(safe_float(row.get("pair_min_absolute_correlation")))
    ]
    panel_rms = [
        safe_float(row.get("max_panel_normalized_residual_rms"))
        for row in content_rows
        if math.isfinite(safe_float(row.get("max_panel_normalized_residual_rms")))
    ]
    if len(supported_rows) >= min_supported_content_pairs:
        label = "short_profile_content_time_zero_anchor_supported_for_visual_qc"
    elif supported_rows:
        label = "short_profile_content_time_zero_anchor_limited"
    else:
        label = "short_profile_content_time_zero_anchor_not_supported"
    return {
        "policy_label": label,
        "event_pair_count": len(rows),
        "content_backed_event_pair_count": len(content_rows),
        "supported_content_anchor_pair_count": len(supported_rows),
        "timing_only_event_pair_count": len(timing_only_rows),
        "max_abs_content_timing_residual_ns": max(content_residuals) if content_residuals else math.nan,
        "max_abs_all_timing_residual_ns": max(all_residuals) if all_residuals else math.nan,
        "min_content_pair_absolute_correlation": min(content_corr) if content_corr else math.nan,
        "mean_content_pair_absolute_correlation": float(np.mean(content_corr)) if content_corr else math.nan,
        "max_content_panel_normalized_residual_rms": max(panel_rms) if panel_rms else math.nan,
        "max_abs_content_residual_threshold_ns": max_abs_content_residual_ns,
        "min_abs_correlation_threshold": min_abs_correlation,
        "max_shift_span_threshold_ns": max_shift_span_ns,
        "policy": (
            "Use the supported repeat-content short-profile pairs as measured-data "
            "time-zero and visual-QC anchors only. This does not support field "
            "radius, cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_anchor_policy(rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: row["pair_index"])
    labels = [f"pair {int(row['pair_index'])}" for row in ordered]
    colors = [
        "#2f9d55" if row["anchor_policy_label"] == "content_time_zero_anchor_supported"
        else "#d99a19" if bool(row.get("content_backed"))
        else "#c7302b"
        for row in ordered
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    axes[0].bar(
        labels,
        [safe_float(row["abs_timing_residual_to_bootstrap_median_ns"]) for row in ordered],
        color=colors,
    )
    axes[0].axhline(
        summary["max_abs_content_residual_threshold_ns"],
        color="#222222",
        linestyle="--",
        linewidth=0.9,
    )
    axes[0].set_ylabel("abs residual to bootstrap median [ns]")
    axes[0].set_title("Relative time-zero residual")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    x = np.arange(len(ordered))
    axes[1].bar(
        x - 0.18,
        [safe_float(row["pair_min_absolute_correlation"]) for row in ordered],
        width=0.36,
        color=colors,
        label="min |corr|",
    )
    axes[1].bar(
        x + 0.18,
        [safe_float(row["max_panel_normalized_residual_rms"], 0.0) for row in ordered],
        width=0.36,
        color="#4c78a8",
        label="max panel RMS",
    )
    axes[1].axhline(summary["min_abs_correlation_threshold"], color="#222222", linestyle="--", linewidth=0.9)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0.0, 1.0)
    axes[1].set_title("Waveform support for anchor pairs")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--content-run", default=DEFAULT_CONTENT_RUN)
    parser.add_argument("--content-synthetic-run", default=DEFAULT_CONTENT_SYNTHETIC_RUN)
    parser.add_argument("--panel-run", default=DEFAULT_PANEL_RUN)
    parser.add_argument("--max-abs-content-residual-ns", type=float, default=0.02)
    parser.add_argument("--min-abs-correlation", type=float, default=0.80)
    parser.add_argument("--max-shift-span-ns", type=float, default=0.05)
    parser.add_argument("--min-supported-content-pairs", type=int, default=2)
    parser.add_argument("--run-name", default="gssi51600s_content_time_zero_anchor_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    content_dir = dataset_root / args.content_run
    content_synthetic_dir = dataset_root / args.content_synthetic_run
    panel_dir = dataset_root / args.panel_run
    event_csv = content_dir / "data" / "short_profile_event_content_classification.csv"
    match_csv = content_synthetic_dir / "data" / "short_profile_content_synthetic_event_matches.csv"
    panel_csv = panel_dir / "data" / "content_backed_waveform_panel_rows.csv"
    for path in (event_csv, match_csv, panel_csv):
        if not path.exists():
            raise FileNotFoundError(path)

    rows = build_anchor_rows(
        read_csv_rows(event_csv),
        read_csv_rows(match_csv),
        read_csv_rows(panel_csv),
        max_abs_content_residual_ns=args.max_abs_content_residual_ns,
        min_abs_correlation=args.min_abs_correlation,
        max_shift_span_ns=args.max_shift_span_ns,
    )
    summary = summarize_anchor_policy(
        rows,
        max_abs_content_residual_ns=args.max_abs_content_residual_ns,
        min_abs_correlation=args.min_abs_correlation,
        max_shift_span_ns=args.max_shift_span_ns,
        min_supported_content_pairs=args.min_supported_content_pairs,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "short_profile_content_time_zero_anchor_rows.csv"
    summary_json = data_dir / "short_profile_content_time_zero_anchor_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_anchor_policy(rows, summary, figures_dir / "short_profile_content_time_zero_anchor_policy.png"))

    write_csv_rows(rows_csv, rows)
    write_csv_rows(validation_csv, [figure_stats(figure_path)])
    output_summary = {
        **summary,
        "event_csv": str(event_csv),
        "match_csv": str(match_csv),
        "panel_csv": str(panel_csv),
        "paths": {
            "anchor_rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_content_time_zero_anchor_policy",
        {
            "summary_json": str(summary_json),
            "anchor_rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
