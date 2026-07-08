#!/usr/bin/env python3
"""Repeat-aligned long-profile stack policy for local GSSI field data."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import (  # noqa: E402
    alignment_rows,
    best_alignment,
    classify_alignment,
    figure_stats,
    load_profile_map,
    profile_signature,
)
from run_gssi_field_profile_repeatability_policy import safe_float  # noqa: E402
from run_gssi_field_short_profile_stack_policy import (  # noqa: E402
    align_comparison_to_reference,
    build_stack_rows,
    common_axis,
    find_stack_anchor_candidates,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


def summarize_long_policy(
    best: dict,
    direct_best: dict,
    reversed_best: dict,
    anchor_rows: list[dict],
    skipped_profiles: list[dict],
) -> dict:
    stable_count = sum(1 for row in anchor_rows if row["stability_label"] == "stable_stack_anchor")
    comparison_missing_phase = any(
        str(row.get("stem", "")) == "PROJECT001C__013"
        and str(row.get("reason", "")) == "no_phase_anchor_picks"
        for row in skipped_profiles
    )
    if best["normalized_correlation"] >= 0.7 and stable_count >= 2 and comparison_missing_phase:
        label = "long_repeat_stack_pattern_only_qc"
    elif best["normalized_correlation"] >= 0.7 and stable_count >= 2:
        label = "long_repeat_stack_timing_qc_candidate"
    elif best["normalized_correlation"] >= 0.5:
        label = "long_repeat_stack_weak_pattern_qc"
    else:
        label = "long_repeat_stack_not_stable"
    return {
        "best_orientation": best["orientation"],
        "best_lag_mm": best["lag_mm"],
        "best_normalized_correlation": best["normalized_correlation"],
        "direct_best_normalized_correlation": direct_best["normalized_correlation"],
        "reversed_best_normalized_correlation": reversed_best["normalized_correlation"],
        "alignment_label": classify_alignment(best, direct_best, reversed_best),
        "stack_anchor_candidate_count": len(anchor_rows),
        "stable_stack_anchor_count": stable_count,
        "comparison_profile_missing_phase_anchor_picks": comparison_missing_phase,
        "policy_label": label,
        "policy": (
            "Use the long-profile stack only as shallow-pattern repeatability QC. "
            "Profile 013 lacks usable phase-anchor picks, so this does not support "
            "field event pairing, radius, cover depth, survey geometry, or FWI validation."
        ),
    }


def plot_long_stack_policy(
    x_m: np.ndarray,
    reference_signature: np.ndarray,
    aligned_comparison_signature: np.ndarray,
    stack_rows: list[dict],
    anchor_rows: list[dict],
    summary: dict,
    save_path: Path,
) -> str:
    stack = np.asarray([safe_float(row["stack_signature_z"]) for row in stack_rows], dtype=np.float64)
    repeat_delta = np.asarray([safe_float(row["repeat_delta_z"]) for row in stack_rows], dtype=np.float64)
    repeat_score = np.asarray([safe_float(row["repeat_score_z"]) for row in stack_rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(13.0, 9.0), constrained_layout=True)
    axes[0].plot(x_m, reference_signature, color="#4c78a8", linewidth=1.2, label="015 reference")
    axes[0].plot(x_m, aligned_comparison_signature, color="#f58518", linewidth=1.0, label="013 aligned")
    axes[0].plot(x_m, stack, color="#2ca02c", linewidth=1.7, label="stack")
    for row in anchor_rows:
        axes[0].axvline(safe_float(row["x_m"]), color="#222222", linestyle="--", linewidth=0.8, alpha=0.65)
    axes[0].set_ylabel("shallow cue z")
    axes[0].set_title("Long-profile shallow-response stack")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(x_m, repeat_delta, color="#7f3c8d", linewidth=1.3)
    axes[1].axhline(1.25, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].set_ylabel("|015 - 013| z")
    axes[1].set_title("Repeat disagreement after alignment")
    axes[1].grid(color="#dddddd", linewidth=0.6)

    axes[2].plot(x_m, repeat_score, color="#6b6b6b", linewidth=1.2)
    for row in anchor_rows:
        axes[2].scatter(
            [safe_float(row["x_m"])],
            [safe_float(row["repeat_score_z"])],
            color="#c7302b",
            s=36,
            zorder=3,
        )
    axes[2].set_xlabel("profile distance [m]")
    axes[2].set_ylabel("repeat score")
    axes[2].set_title("Candidate repeat anchors")
    axes[2].grid(color="#dddddd", linewidth=0.6)

    fig.suptitle(
        "Long-profile repeat stack: "
        f"{summary['policy_label']}, corr={summary['best_normalized_correlation']:.3f}",
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
    parser.add_argument("--phase-anchor-summary", default=None)
    parser.add_argument("--reference-stem", default="PROJECT001C__015")
    parser.add_argument("--comparison-stem", default="PROJECT001C__013")
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--max-lag-m", type=float, default=0.6)
    parser.add_argument("--min-anchor-separation-m", type=float, default=0.18)
    parser.add_argument("--min-stack-z", type=float, default=0.75)
    parser.add_argument("--max-repeat-delta-z", type=float, default=1.5)
    parser.add_argument("--max-anchor-count", type=int, default=8)
    parser.add_argument("--run-name", default="gssi51600s_long_profile_stack_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    time_min_ns, time_max_ns = [float(part.strip()) for part in args.time_window_ns.split(",", 1)]
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    phase_anchor_summary = (
        Path(args.phase_anchor_summary)
        if args.phase_anchor_summary is not None
        else dataset_root / "016_gssi51600s_long_profiles_phase_anchor_qc" / "data" / "field_phase_anchor_summary.json"
    )
    skipped_profiles: list[dict] = []
    if phase_anchor_summary.exists():
        skipped_profiles = json.loads(phase_anchor_summary.read_text(encoding="utf-8")).get("skipped_profiles", [])

    profiles = load_profile_map(Path(args.input_dir))
    reference = profiles[args.reference_stem]
    comparison = profiles[args.comparison_stem]
    x_m = common_axis(reference["x_m"], comparison["x_m"])
    reference_sig = profile_signature(reference["processed"]["cue"], reference["time_ns"], time_min_ns, time_max_ns)
    comparison_sig = profile_signature(comparison["processed"]["cue"], comparison["time_ns"], time_min_ns, time_max_ns)
    if reference_sig.size != x_m.size:
        reference_sig = np.interp(x_m, reference["x_m"], reference_sig)
    if comparison_sig.size != x_m.size:
        comparison_sig = np.interp(x_m, comparison["x_m"], comparison_sig)

    dx_m = float(np.median(np.diff(x_m))) if x_m.size > 1 else 1.0
    rows = []
    rows.extend(alignment_rows(reference_sig, comparison_sig, dx_m, args.max_lag_m, "direct"))
    rows.extend(alignment_rows(reference_sig, comparison_sig, dx_m, args.max_lag_m, "reversed"))
    direct_best = best_alignment([row for row in rows if row["orientation"] == "direct"])
    reversed_best = best_alignment([row for row in rows if row["orientation"] == "reversed"])
    best = best_alignment(rows)
    aligned_cmp = align_comparison_to_reference(comparison_sig, str(best["orientation"]), int(best["lag_samples"]))

    stack_rows = build_stack_rows(x_m, reference_sig, aligned_cmp)
    anchor_rows = find_stack_anchor_candidates(
        stack_rows,
        args.min_anchor_separation_m,
        args.min_stack_z,
        args.max_repeat_delta_z,
        args.max_anchor_count,
    )
    summary = summarize_long_policy(best, direct_best, reversed_best, anchor_rows, skipped_profiles)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    lag_csv = data_dir / "long_profile_stack_lag_scan.csv"
    stack_csv = data_dir / "long_profile_stack_signal.csv"
    anchors_csv = data_dir / "long_profile_stack_anchor_candidates.csv"
    summary_json = data_dir / "long_profile_stack_policy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_long_stack_policy(
        x_m,
        reference_sig,
        aligned_cmp,
        stack_rows,
        anchor_rows,
        summary,
        figures_dir / "long_profile_stack_policy.png",
    ))

    write_csv(lag_csv, [json_safe(row) for row in rows])
    write_csv(stack_csv, [json_safe(row) for row in stack_rows])
    write_csv(anchors_csv, [json_safe(row) for row in anchor_rows])
    validation_rows = [figure_stats(figure_path)]
    write_csv(validation_csv, [json_safe(row) for row in validation_rows])

    output_summary = {
        "reference_stem": args.reference_stem,
        "comparison_stem": args.comparison_stem,
        "time_window_min_ns": time_min_ns,
        "time_window_max_ns": time_max_ns,
        "dx_m": dx_m,
        "sample_count": int(x_m.size),
        "phase_anchor_summary": str(phase_anchor_summary),
        "summary": summary,
        "paths": {
            "lag_scan_csv": str(lag_csv),
            "stack_signal_csv": str(stack_csv),
            "anchor_candidates_csv": str(anchors_csv),
            "summary_json": str(summary_json),
            "stack_policy_plot": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_long_profile_stack_policy",
        {
            "summary_json": str(summary_json),
            "phase_anchor_summary": str(phase_anchor_summary),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
