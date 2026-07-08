#!/usr/bin/env python3
"""Stress-test measured-field cue-spacing context over same-time thresholds."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_cue_spacing_context_audit import (  # noqa: E402
    DEFAULT_APPARENT_DEPTH_RUN,
    DEFAULT_FIELD_POLICY_RUN,
    DEFAULT_GEOMETRY_RUN,
    DEFAULT_PREPROCESS_RUN,
    build_pair_spacing_rows,
    build_profile_context_rows,
    read_csv_rows,
    read_json,
    safe_float,
    summarize_spacing,
)
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_THRESHOLDS_NS = "0.05,0.10,0.15,0.20,0.30,0.50,1.00"


def parse_thresholds(text: str) -> list[float]:
    values = []
    for part in str(text).split(","):
        part = part.strip()
        if not part:
            continue
        value = float(part)
        if value <= 0.0 or not math.isfinite(value):
            raise ValueError(f"Invalid positive threshold: {part}")
        values.append(value)
    if not values:
        raise ValueError("At least one threshold is required")
    return sorted(set(values))


def build_threshold_rows(
    cue_rows: list[dict],
    thresholds_ns: list[float],
    *,
    duplicate_x_m: float,
    geometry: dict,
    apparent_depth: dict,
    field_policy: dict,
) -> list[dict]:
    rows = []
    for threshold_ns in thresholds_ns:
        pair_rows = build_pair_spacing_rows(
            cue_rows,
            same_time_ns=threshold_ns,
            duplicate_x_m=duplicate_x_m,
        )
        profile_rows = build_profile_context_rows(cue_rows, pair_rows)
        summary = summarize_spacing(
            profile_rows,
            pair_rows,
            same_time_ns=threshold_ns,
            geometry=geometry,
            apparent_depth=apparent_depth,
            field_policy=field_policy,
        )
        rows.append(
            {
                "same_time_threshold_ns": threshold_ns,
                "same_time_lateral_pair_count": summary["same_time_lateral_pair_count"],
                "time_separated_lateral_pair_count": summary["time_separated_lateral_pair_count"],
                "same_x_or_vertical_pair_count": summary["same_x_or_vertical_pair_count"],
                "min_dataset_same_time_lateral_spacing_mm": summary["min_dataset_same_time_lateral_spacing_mm"],
                "min_short_same_time_lateral_spacing_mm": summary["min_short_same_time_lateral_spacing_mm"],
                "min_long_same_time_lateral_spacing_mm": summary["min_long_same_time_lateral_spacing_mm"],
                "min_dataset_distinct_x_spacing_any_time_mm": summary[
                    "min_dataset_distinct_x_spacing_any_time_mm"
                ],
                "same_time_visible_cues_wider_than_synthetic_close_context": summary[
                    "same_time_visible_cues_wider_than_synthetic_close_context"
                ],
                "ready_for_resolution_benchmark": False,
                "gpu_priority": "none",
            }
        )
    return rows


def summarize_threshold_sensitivity(rows: list[dict], *, close_context_max_mm: float) -> dict:
    min_values = [
        safe_float(row.get("min_dataset_same_time_lateral_spacing_mm"))
        for row in rows
    ]
    finite_min = [value for value in min_values if math.isfinite(value)]
    global_min = min(finite_min) if finite_min else math.nan
    robust = bool(finite_min and global_min > close_context_max_mm and all(
        str(row.get("same_time_visible_cues_wider_than_synthetic_close_context")).lower() in {"true", "1"}
        for row in rows
    ))
    return {
        "policy_label": (
            "field_cue_spacing_context_threshold_robust_not_resolution_benchmark"
            if robust
            else "field_cue_spacing_context_threshold_review"
        ),
        "threshold_count": len(rows),
        "thresholds_ns": ",".join(f"{safe_float(row['same_time_threshold_ns']):.3f}" for row in rows),
        "min_same_time_lateral_spacing_mm_across_thresholds": global_min,
        "max_same_time_lateral_pair_count": max(
            [int(safe_float(row.get("same_time_lateral_pair_count"), 0.0)) for row in rows],
            default=0,
        ),
        "synthetic_close_spacing_context_max_mm": close_context_max_mm,
        "all_thresholds_wider_than_synthetic_close_context": robust,
        "ready_for_field_context": True,
        "ready_for_resolution_benchmark": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
        "decision": (
            "Use this as a robustness check for field cue-spacing context only. "
            "Across the tested same-time thresholds, measured cue spacings remain "
            "wider than the synthetic close25-close50 stress scale, so the field "
            "dataset remains context/QC rather than a known-truth close-spacing "
            "resolution benchmark."
        ),
    }


def plot_threshold_sensitivity(rows: list[dict], summary: dict, save_path: Path) -> str:
    thresholds = np.asarray([safe_float(row["same_time_threshold_ns"]) for row in rows], dtype=float)
    min_spacing = np.asarray(
        [safe_float(row["min_dataset_same_time_lateral_spacing_mm"]) for row in rows],
        dtype=float,
    )
    pair_counts = np.asarray(
        [safe_float(row["same_time_lateral_pair_count"], 0.0) for row in rows],
        dtype=float,
    )

    fig, axes = plt.subplots(1, 2, figsize=(13.6, 4.8), constrained_layout=True)
    axes[0].plot(thresholds, min_spacing, marker="o", color="#2f6f9f", linewidth=1.8)
    axes[0].axhspan(25.0, float(summary["synthetic_close_spacing_context_max_mm"]), color="#c7302b", alpha=0.14)
    axes[0].set_xlabel("same-time threshold [ns]")
    axes[0].set_ylabel("min same-time cue spacing [mm]")
    axes[0].set_title("Cue-spacing threshold sensitivity")
    axes[0].grid(color="#dddddd", linewidth=0.6)

    axes[1].bar([f"{value:.2f}" for value in thresholds], pair_counts, color="#4c9f70", width=0.62)
    axes[1].set_xlabel("same-time threshold [ns]")
    axes[1].set_ylabel("same-time lateral pair count")
    axes[1].set_title("Pairs admitted by threshold")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.5,
        0.95,
        "Field context only; not a resolution benchmark",
        transform=axes[1].transAxes,
        ha="center",
        va="top",
        fontsize=10,
        color="#333333",
    )

    fig.suptitle(
        f"{summary['policy_label']} | min={summary['min_same_time_lateral_spacing_mm_across_thresholds']:.1f} mm",
        fontsize=12,
    )
    return save_validated_figure(fig, str(save_path))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--preprocess-run", default=DEFAULT_PREPROCESS_RUN)
    parser.add_argument("--geometry-run", default=DEFAULT_GEOMETRY_RUN)
    parser.add_argument("--apparent-depth-run", default=DEFAULT_APPARENT_DEPTH_RUN)
    parser.add_argument("--field-policy-run", default=DEFAULT_FIELD_POLICY_RUN)
    parser.add_argument("--thresholds-ns", default=DEFAULT_THRESHOLDS_NS)
    parser.add_argument("--duplicate-x-m", type=float, default=0.005)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--run-name", default="gssi51600s_field_cue_spacing_sensitivity_audit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    thresholds = parse_thresholds(args.thresholds_ns)
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    cue_rows = read_csv_rows(dataset_root / args.preprocess_run / "data/field_reflector_cue_candidates.csv")
    geometry = read_json(dataset_root / args.geometry_run / "data/survey_geometry_audit_summary.json")
    apparent_depth = read_json(dataset_root / args.apparent_depth_run / "data/field_apparent_depth_qc_summary.json")
    field_policy = read_json(dataset_root / args.field_policy_run / "data/field_dataset_policy_summary.json")

    rows = build_threshold_rows(
        cue_rows,
        thresholds,
        duplicate_x_m=args.duplicate_x_m,
        geometry=geometry,
        apparent_depth=apparent_depth,
        field_policy=field_policy,
    )
    summary = summarize_threshold_sensitivity(rows, close_context_max_mm=50.0)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_cue_spacing_threshold_sensitivity_rows.csv"
    summary_json = data_dir / "field_cue_spacing_threshold_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_cue_spacing_threshold_sensitivity.png"

    plot_threshold_sensitivity(rows, summary, figure_path)
    write_csv(rows_csv, rows)
    write_csv(validation_csv, [figure_stats(figure_path)])

    summary["paths"] = {
        "threshold_rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2), encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_cue_spacing_sensitivity_audit",
        {
            "dataset_id": args.dataset_id,
            "preprocess_run": args.preprocess_run,
            "geometry_run": args.geometry_run,
            "apparent_depth_run": args.apparent_depth_run,
            "field_policy_run": args.field_policy_run,
            "thresholds_ns": args.thresholds_ns,
            "duplicate_x_m": args.duplicate_x_m,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
