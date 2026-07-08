#!/usr/bin/env python3
"""Repeatable-content window policy for the short local GSSI field profiles."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_STACK_RUN = "021_gssi51600s_short_profile_stack_policy"
DEFAULT_BOOTSTRAP_RUN = "029_gssi51600s_short_profile_timing_bootstrap_policy"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def boolish(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def stable_anchor_rows(anchor_rows: list[dict]) -> list[dict]:
    return [
        row for row in anchor_rows
        if str(row.get("stability_label", "")) == "stable_stack_anchor"
        and math.isfinite(safe_float(row.get("x_m")))
    ]


def nearest_anchor(event_x_m: float, anchors: list[dict]) -> tuple[dict | None, float]:
    if not anchors:
        return None, math.inf
    event_x = float(event_x_m)
    best = min(anchors, key=lambda row: abs(safe_float(row.get("x_m")) - event_x))
    return best, abs(safe_float(best.get("x_m")) - event_x)


def _rows_in_window(stack_rows: list[dict], center_x_m: float, half_width_m: float) -> list[dict]:
    lower = float(center_x_m) - float(half_width_m)
    upper = float(center_x_m) + float(half_width_m)
    return [
        row for row in stack_rows
        if lower <= safe_float(row.get("x_m")) <= upper
        and boolish(row.get("both_profiles_present"))
    ]


def _finite_values(rows: list[dict], key: str) -> list[float]:
    values = []
    for row in rows:
        value = safe_float(row.get(key))
        if math.isfinite(value):
            values.append(value)
    return values


def build_content_windows(
    stack_rows: list[dict],
    anchor_rows: list[dict],
    event_pairs: list[dict],
    *,
    half_width_m: float,
) -> list[dict]:
    """Build repeatable-content windows centered on stable stack anchors."""
    stable = stable_anchor_rows(anchor_rows)
    windows: list[dict] = []
    for idx, anchor in enumerate(sorted(stable, key=lambda row: safe_float(row.get("x_m"))), start=1):
        center = safe_float(anchor.get("x_m"))
        rows = _rows_in_window(stack_rows, center, half_width_m)
        stack_values = _finite_values(rows, "stack_signature_z")
        repeat_values = _finite_values(rows, "repeat_delta_z")
        score_values = _finite_values(rows, "repeat_score_z")
        event, event_distance_m = nearest_anchor(
            center,
            [
                {"x_m": row.get("reference_x_m"), **row}
                for row in event_pairs
                if math.isfinite(safe_float(row.get("reference_x_m")))
            ],
        )
        windows.append({
            "content_window_index": idx,
            "anchor_candidate_index": int(safe_float(anchor.get("candidate_index"), idx)),
            "center_x_m": center,
            "center_x_mm": 1000.0 * center,
            "x_min_m": center - half_width_m,
            "x_max_m": center + half_width_m,
            "x_min_mm": 1000.0 * (center - half_width_m),
            "x_max_mm": 1000.0 * (center + half_width_m),
            "window_sample_count": len(rows),
            "anchor_stack_signature_z": safe_float(anchor.get("stack_signature_z")),
            "anchor_repeat_delta_z": safe_float(anchor.get("repeat_delta_z")),
            "anchor_repeat_score_z": safe_float(anchor.get("repeat_score_z")),
            "window_peak_stack_signature_z": max(stack_values) if stack_values else math.nan,
            "window_median_repeat_delta_z": float(np.median(repeat_values)) if repeat_values else math.nan,
            "window_mean_repeat_score_z": float(np.mean(score_values)) if score_values else math.nan,
            "nearest_event_pair_index": (
                int(safe_float(event.get("pair_index"))) if event is not None else None
            ),
            "nearest_event_reference_x_mm": (
                1000.0 * safe_float(event.get("reference_x_m")) if event is not None else math.nan
            ),
            "nearest_event_distance_mm": 1000.0 * event_distance_m if event is not None else math.nan,
        })
    return windows


def classify_event_content(
    event_pairs: list[dict],
    anchor_rows: list[dict],
    bootstrap_summary: dict,
    *,
    max_event_anchor_distance_m: float,
) -> list[dict]:
    """Classify event pairs as content-backed or timing-only."""
    anchors = stable_anchor_rows(anchor_rows)
    bootstrap = bootstrap_summary.get("summary", bootstrap_summary)
    median_offset = safe_float(bootstrap.get("observed_median_offset_ns"))
    min_ci = safe_float(bootstrap.get("min_bootstrap_ci_lower_ns"))
    max_ci = safe_float(bootstrap.get("max_bootstrap_ci_upper_ns"))
    rows: list[dict] = []
    for event in sorted(event_pairs, key=lambda row: int(safe_float(row.get("pair_index"), 0))):
        reference_x = safe_float(event.get("reference_x_m"))
        anchor, distance_m = nearest_anchor(reference_x, anchors)
        delta_ns = safe_float(event.get("comparison_minus_reference_phase_time_ns"))
        content_backed = distance_m <= max_event_anchor_distance_m
        within_bootstrap_envelope = (
            math.isfinite(delta_ns)
            and math.isfinite(min_ci)
            and math.isfinite(max_ci)
            and min_ci <= delta_ns <= max_ci
        )
        rows.append({
            "pair_index": int(safe_float(event.get("pair_index"))),
            "reference_apex_group": int(safe_float(event.get("reference_apex_group"))),
            "comparison_apex_group": int(safe_float(event.get("comparison_apex_group"))),
            "reference_x_mm": 1000.0 * reference_x,
            "comparison_aligned_x_mm": 1000.0 * safe_float(event.get("comparison_aligned_x_m")),
            "aligned_x_residual_mm": safe_float(event.get("aligned_x_residual_mm")),
            "nearest_anchor_candidate_index": (
                int(safe_float(anchor.get("candidate_index"))) if anchor is not None else None
            ),
            "nearest_anchor_x_mm": (
                1000.0 * safe_float(anchor.get("x_m")) if anchor is not None else math.nan
            ),
            "nearest_anchor_distance_mm": 1000.0 * distance_m if anchor is not None else math.nan,
            "content_backed": content_backed,
            "content_label": (
                "repeat_content_anchor" if content_backed else "timing_only_no_stable_content_anchor"
            ),
            "comparison_minus_reference_phase_time_ns": delta_ns,
            "bootstrap_median_offset_ns": median_offset,
            "timing_residual_to_bootstrap_median_ns": (
                delta_ns - median_offset if math.isfinite(delta_ns) and math.isfinite(median_offset) else math.nan
            ),
            "within_bootstrap_ci_envelope": within_bootstrap_envelope,
            "reference_best_radius_mm": safe_float(event.get("reference_best_radius_mm")),
            "comparison_best_radius_mm": safe_float(event.get("comparison_best_radius_mm")),
            "radius_match": boolish(event.get("radius_match")),
        })
    return rows


def summarize_content_policy(
    content_windows: list[dict],
    event_rows: list[dict],
    bootstrap_summary: dict,
    *,
    min_content_windows: int,
) -> dict:
    event_count = len(event_rows)
    content_count = sum(1 for row in event_rows if bool(row.get("content_backed")))
    timing_only_count = event_count - content_count
    content_distances = [
        safe_float(row.get("nearest_anchor_distance_mm"))
        for row in event_rows
        if bool(row.get("content_backed"))
    ]
    timing_residuals = [
        abs(safe_float(row.get("timing_residual_to_bootstrap_median_ns")))
        for row in event_rows
        if math.isfinite(safe_float(row.get("timing_residual_to_bootstrap_median_ns")))
    ]
    content_timing_residuals = [
        abs(safe_float(row.get("timing_residual_to_bootstrap_median_ns")))
        for row in event_rows
        if bool(row.get("content_backed"))
        and math.isfinite(safe_float(row.get("timing_residual_to_bootstrap_median_ns")))
    ]
    bootstrap = bootstrap_summary.get("summary", bootstrap_summary)
    bootstrap_label = str(bootstrap.get("policy_label", "not_available"))
    enough_content = len(content_windows) >= min_content_windows and content_count >= min_content_windows
    timing_supported = bootstrap_label == "bootstrap_relative_time_zero_supported_qc"
    if enough_content and content_count == event_count and timing_supported:
        label = "repeat_content_windows_supported_qc"
    elif enough_content and timing_supported:
        label = "repeat_content_windows_limited_qc"
    elif len(content_windows) > 0:
        label = "repeat_content_windows_insufficient_timing_qc"
    else:
        label = "repeat_content_windows_not_supported"
    return {
        "policy_label": label,
        "timing_bootstrap_policy_label": bootstrap_label,
        "stable_content_window_count": len(content_windows),
        "event_pair_count": event_count,
        "content_backed_event_pair_count": content_count,
        "timing_only_event_pair_count": timing_only_count,
        "content_backed_event_fraction": content_count / event_count if event_count else math.nan,
        "max_content_anchor_distance_mm": max(content_distances) if content_distances else math.nan,
        "max_abs_timing_residual_to_bootstrap_median_ns": max(timing_residuals) if timing_residuals else math.nan,
        "max_abs_content_timing_residual_to_bootstrap_median_ns": (
            max(content_timing_residuals) if content_timing_residuals else math.nan
        ),
        "bootstrap_observed_median_offset_ns": safe_float(bootstrap.get("observed_median_offset_ns")),
        "bootstrap_min_ci_lower_ns": safe_float(bootstrap.get("min_bootstrap_ci_lower_ns")),
        "bootstrap_max_ci_upper_ns": safe_float(bootstrap.get("max_bootstrap_ci_upper_ns")),
        "policy": (
            "Use repeat-backed content windows for field profile QC and later "
            "field-to-synthetic visual comparison only. Timing-only cues remain "
            "relative timing evidence. This does not support field radius, cover "
            "depth, geometry, 3D, or FWI claims."
        ),
    }


def plot_content_policy(
    stack_rows: list[dict],
    content_windows: list[dict],
    event_rows: list[dict],
    summary: dict,
    save_path: Path,
) -> str:
    x_mm = np.asarray([safe_float(row.get("x_mm")) for row in stack_rows], dtype=np.float64)
    ref = np.asarray([safe_float(row.get("reference_signature_z")) for row in stack_rows], dtype=np.float64)
    cmp = np.asarray([safe_float(row.get("aligned_comparison_signature_z")) for row in stack_rows], dtype=np.float64)
    stack = np.asarray([safe_float(row.get("stack_signature_z")) for row in stack_rows], dtype=np.float64)
    repeat_delta = np.asarray([safe_float(row.get("repeat_delta_z")) for row in stack_rows], dtype=np.float64)

    fig, axes = plt.subplots(2, 1, figsize=(11.6, 7.2), constrained_layout=True)
    axes[0].plot(x_mm, ref, color="#4c78a8", linewidth=1.0, label="014 signature")
    axes[0].plot(x_mm, cmp, color="#f58518", linewidth=1.0, label="016 aligned signature")
    axes[0].plot(x_mm, stack, color="#222222", linewidth=1.6, label="repeat stack")
    for window in content_windows:
        axes[0].axvspan(
            safe_float(window.get("x_min_mm")),
            safe_float(window.get("x_max_mm")),
            color="#59a14f",
            alpha=0.18,
        )
        axes[0].scatter(
            [safe_float(window.get("center_x_mm"))],
            [safe_float(window.get("anchor_stack_signature_z"))],
            marker="o",
            color="#237033",
            zorder=4,
        )
    for row in event_rows:
        color = "#237033" if bool(row.get("content_backed")) else "#b23a48"
        axes[0].axvline(safe_float(row.get("reference_x_mm")), color=color, linestyle="--", linewidth=0.9)
    axes[0].set_ylabel("profile signature z-score")
    axes[0].set_title("Short-profile repeat content windows")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8, ncols=3)

    axes[1].plot(x_mm, repeat_delta, color="#7f7f7f", linewidth=1.0, label="repeat delta")
    event_x = [safe_float(row.get("reference_x_mm")) for row in event_rows]
    event_distance = [safe_float(row.get("nearest_anchor_distance_mm")) for row in event_rows]
    colors = ["#237033" if bool(row.get("content_backed")) else "#b23a48" for row in event_rows]
    axes[1].scatter(event_x, event_distance, color=colors, zorder=4, label="event-to-anchor distance")
    for row in event_rows:
        axes[1].text(
            safe_float(row.get("reference_x_mm")),
            safe_float(row.get("nearest_anchor_distance_mm")) + 1.2,
            f"p{int(safe_float(row.get('pair_index')))}",
            fontsize=8,
            ha="center",
        )
    axes[1].set_xlabel("profile x [mm]")
    axes[1].set_ylabel("delta z / event distance [mm]")
    axes[1].set_title("Event content classification")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle(
        f"{summary['policy_label']}: "
        f"{summary['content_backed_event_pair_count']}/{summary['event_pair_count']} events content-backed",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--stack-dir", default=None)
    parser.add_argument("--bootstrap-dir", default=None)
    parser.add_argument("--content-half-window-m", type=float, default=0.04)
    parser.add_argument("--max-event-anchor-distance-m", type=float, default=0.04)
    parser.add_argument("--min-content-windows", type=int, default=2)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_content_window_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    stack_dir = Path(args.stack_dir) if args.stack_dir else dataset_root / DEFAULT_STACK_RUN
    bootstrap_dir = Path(args.bootstrap_dir) if args.bootstrap_dir else dataset_root / DEFAULT_BOOTSTRAP_RUN

    stack_rows = read_csv_rows(stack_dir / "data" / "short_profile_stack_signal.csv")
    anchor_rows = read_csv_rows(stack_dir / "data" / "short_profile_stack_anchor_candidates.csv")
    event_pairs = read_csv_rows(stack_dir / "data" / "short_profile_reversed_event_pairs.csv")
    bootstrap_summary = load_json(bootstrap_dir / "data" / "short_profile_timing_bootstrap_policy_summary.json")

    content_windows = build_content_windows(
        stack_rows,
        anchor_rows,
        event_pairs,
        half_width_m=args.content_half_window_m,
    )
    event_rows = classify_event_content(
        event_pairs,
        anchor_rows,
        bootstrap_summary,
        max_event_anchor_distance_m=args.max_event_anchor_distance_m,
    )
    summary = summarize_content_policy(
        content_windows,
        event_rows,
        bootstrap_summary,
        min_content_windows=args.min_content_windows,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    content_windows_csv = data_dir / "short_profile_content_windows.csv"
    event_classification_csv = data_dir / "short_profile_event_content_classification.csv"
    summary_json = data_dir / "short_profile_content_window_policy_summary.json"
    figure_path = Path(plot_content_policy(
        stack_rows,
        content_windows,
        event_rows,
        summary,
        figures_dir / "short_profile_content_window_policy.png",
    ))
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(content_windows_csv, [json_safe(row) for row in content_windows])
    write_csv(event_classification_csv, [json_safe(row) for row in event_rows])
    validation_rows = [figure_stats(figure_path)]
    write_csv(validation_csv, [json_safe(row) for row in validation_rows])

    output_summary = {
        "stack_dir": str(stack_dir),
        "bootstrap_dir": str(bootstrap_dir),
        "thresholds": {
            "content_half_window_m": args.content_half_window_m,
            "max_event_anchor_distance_m": args.max_event_anchor_distance_m,
            "min_content_windows": args.min_content_windows,
        },
        "summary": summary,
        "paths": {
            "content_windows_csv": str(content_windows_csv),
            "event_classification_csv": str(event_classification_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_content_window_policy",
        {
            "summary_json": str(summary_json),
            "stack_dir": str(stack_dir),
            "bootstrap_dir": str(bootstrap_dir),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
