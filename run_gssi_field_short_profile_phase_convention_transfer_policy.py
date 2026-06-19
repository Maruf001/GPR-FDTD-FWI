#!/usr/bin/env python3
"""Cross-check short-profile relative timing transfer across phase conventions."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import figure_stats  # noqa: E402
from run_gssi_field_profile_repeatability_policy import read_csv_rows, safe_float  # noqa: E402
from run_gssi_field_short_profile_time_zero_transfer_policy import robust_sigma  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


PHASE_CONVENTIONS = {
    "current_cue": "current_cue_time_ns",
    "top_envelope_35pct": "top_envelope_35pct_time_ns",
    "envelope_max": "envelope_max_time_ns",
    "signed_positive_peak": "signed_positive_peak_time_ns",
    "signed_negative_peak": "signed_negative_peak_time_ns",
    "nearest_zero_crossing": "nearest_zero_crossing_time_ns",
}


def finite_values(values: list[float]) -> list[float]:
    return [float(value) for value in values if math.isfinite(float(value))]


def phase_pick_lookup(phase_rows: list[dict]) -> dict[tuple[str, int], dict]:
    lookup = {}
    for row in phase_rows:
        lookup[(str(row.get("file", "")), int(safe_float(row.get("apex_group"), -1)))] = row
    return lookup


def convention_event_offset_rows(event_pairs: list[dict], phase_rows: list[dict]) -> list[dict]:
    lookup = phase_pick_lookup(phase_rows)
    rows = []
    for pair in event_pairs:
        ref_key = (str(pair.get("reference_file", "")), int(safe_float(pair.get("reference_apex_group"), -1)))
        cmp_key = (str(pair.get("comparison_file", "")), int(safe_float(pair.get("comparison_apex_group"), -1)))
        reference = lookup.get(ref_key, {})
        comparison = lookup.get(cmp_key, {})
        for convention, column in PHASE_CONVENTIONS.items():
            ref_time = safe_float(reference.get(column))
            cmp_time = safe_float(comparison.get(column))
            delta = cmp_time - ref_time if math.isfinite(ref_time) and math.isfinite(cmp_time) else math.nan
            rows.append({
                "pair_index": int(safe_float(pair.get("pair_index"), -1)),
                "phase_convention": convention,
                "reference_file": pair.get("reference_file", ""),
                "comparison_file": pair.get("comparison_file", ""),
                "reference_apex_group": int(safe_float(pair.get("reference_apex_group"), -1)),
                "comparison_apex_group": int(safe_float(pair.get("comparison_apex_group"), -1)),
                "aligned_x_residual_mm": safe_float(pair.get("aligned_x_residual_mm")),
                "reference_time_ns": ref_time,
                "comparison_time_ns": cmp_time,
                "comparison_minus_reference_time_ns": delta,
            })
    return rows


def convention_summary_rows(
    event_rows: list[dict],
    *,
    max_range_ns: float,
    max_robust_sigma_ns: float,
) -> list[dict]:
    rows = []
    for convention in PHASE_CONVENTIONS:
        subset = [row for row in event_rows if row["phase_convention"] == convention]
        deltas = finite_values([safe_float(row.get("comparison_minus_reference_time_ns")) for row in subset])
        delta_range = max(deltas) - min(deltas) if deltas else math.nan
        sigma = robust_sigma(deltas)
        median_delta = float(np.median(deltas)) if deltas else math.nan
        all_positive = bool(deltas and all(value > 0.0 for value in deltas))
        stable = (
            len(deltas) >= 3
            and all_positive
            and math.isfinite(delta_range)
            and delta_range <= max_range_ns
            and math.isfinite(sigma)
            and sigma <= max_robust_sigma_ns
        )
        rows.append({
            "phase_convention": convention,
            "event_pair_count": len(deltas),
            "median_delta_ns": median_delta,
            "mean_delta_ns": float(np.mean(deltas)) if deltas else math.nan,
            "min_delta_ns": min(deltas) if deltas else math.nan,
            "max_delta_ns": max(deltas) if deltas else math.nan,
            "range_delta_ns": delta_range,
            "robust_sigma_delta_ns": sigma,
            "all_deltas_positive": all_positive,
            "stable_transfer_convention": stable,
        })
    return rows


def summarize_phase_convention_transfer(
    summary_rows: list[dict],
    *,
    accepted_convention: str,
    min_stable_conventions: int,
    max_stable_median_spread_ns: float,
) -> dict:
    stable_rows = [row for row in summary_rows if bool(row.get("stable_transfer_convention"))]
    stable_medians = finite_values([safe_float(row.get("median_delta_ns")) for row in stable_rows])
    median_spread = max(stable_medians) - min(stable_medians) if stable_medians else math.nan
    accepted_stable = any(
        row["phase_convention"] == accepted_convention and bool(row.get("stable_transfer_convention"))
        for row in summary_rows
    )
    supported = (
        len(stable_rows) >= min_stable_conventions
        and accepted_stable
        and math.isfinite(median_spread)
        and median_spread <= max_stable_median_spread_ns
    )
    if supported:
        policy_label = "multi_phase_relative_time_zero_supported_qc"
    elif accepted_stable:
        policy_label = "accepted_phase_relative_time_zero_supported_limited"
    else:
        policy_label = "phase_convention_transfer_not_stable"
    return {
        "phase_convention_count": len(summary_rows),
        "stable_phase_convention_count": len(stable_rows),
        "stable_phase_conventions": ", ".join(row["phase_convention"] for row in stable_rows),
        "accepted_phase_convention": accepted_convention,
        "accepted_phase_convention_stable": accepted_stable,
        "stable_median_delta_min_ns": min(stable_medians) if stable_medians else math.nan,
        "stable_median_delta_max_ns": max(stable_medians) if stable_medians else math.nan,
        "stable_median_delta_spread_ns": median_spread,
        "policy_label": policy_label,
        "policy": (
            "Use the 014/016 short-profile phase-convention agreement as relative "
            "timing-transfer QC only. It is not an absolute time-zero calibration "
            "and does not support field radius, cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def plot_phase_convention_transfer(summary_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["phase_convention"] for row in summary_rows]
    medians = [safe_float(row.get("median_delta_ns")) for row in summary_rows]
    ranges = [safe_float(row.get("range_delta_ns")) for row in summary_rows]
    stable = [bool(row.get("stable_transfer_convention")) for row in summary_rows]
    colors = ["#2f9d55" if value else "#b05a00" for value in stable]

    fig, axes = plt.subplots(1, 2, figsize=(13.4, 4.8), constrained_layout=True)
    x = np.arange(len(labels))
    axes[0].bar(x, medians, color=colors, width=0.62)
    axes[0].set_xticks(x, labels, rotation=35, ha="right")
    axes[0].set_ylabel("median 016 - 014 time [ns]")
    axes[0].set_title("Relative offset by phase convention")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, ranges, color=colors, width=0.62)
    axes[1].axhline(0.10, color="#c7302b", linestyle="--", linewidth=1.0, label="0.10 ns range")
    axes[1].set_xticks(x, labels, rotation=35, ha="right")
    axes[1].set_ylabel("event-pair range [ns]")
    axes[1].set_title("Convention stability across reversed event pairs")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle(
        "Short-profile multi-phase timing transfer: "
        f"{summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--phase-anchor-dir", default=None)
    parser.add_argument("--stack-policy-dir", default=None)
    parser.add_argument("--max-range-ns", type=float, default=0.10)
    parser.add_argument("--max-robust-sigma-ns", type=float, default=0.04)
    parser.add_argument("--min-stable-conventions", type=int, default=4)
    parser.add_argument("--max-stable-median-spread-ns", type=float, default=0.05)
    parser.add_argument("--accepted-convention", default="top_envelope_35pct")
    parser.add_argument("--run-name", default="gssi51600s_short_profile_phase_convention_transfer_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    phase_dir = (
        Path(args.phase_anchor_dir)
        if args.phase_anchor_dir
        else dataset_root / "006_gssi51600s_phase_anchor_qc"
    )
    stack_dir = (
        Path(args.stack_policy_dir)
        if args.stack_policy_dir
        else dataset_root / "021_gssi51600s_short_profile_stack_policy"
    )
    phase_csv = phase_dir / "data" / "field_phase_anchor_picks.csv"
    event_pairs_csv = stack_dir / "data" / "short_profile_reversed_event_pairs.csv"
    phase_rows = read_csv_rows(phase_csv)
    event_pairs = read_csv_rows(event_pairs_csv)

    event_rows = convention_event_offset_rows(event_pairs, phase_rows)
    convention_rows = convention_summary_rows(
        event_rows,
        max_range_ns=args.max_range_ns,
        max_robust_sigma_ns=args.max_robust_sigma_ns,
    )
    summary = summarize_phase_convention_transfer(
        convention_rows,
        accepted_convention=args.accepted_convention,
        min_stable_conventions=args.min_stable_conventions,
        max_stable_median_spread_ns=args.max_stable_median_spread_ns,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    event_csv = data_dir / "short_profile_phase_convention_event_offsets.csv"
    convention_csv = data_dir / "short_profile_phase_convention_summary.csv"
    summary_json = data_dir / "short_profile_phase_convention_transfer_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(
        plot_phase_convention_transfer(
            convention_rows,
            summary,
            figures_dir / "short_profile_phase_convention_transfer.png",
        )
    )

    write_csv(event_csv, [json_safe(row) for row in event_rows])
    write_csv(convention_csv, [json_safe(row) for row in convention_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "phase_anchor_dir": str(phase_dir),
        "stack_policy_dir": str(stack_dir),
        "input_phase_anchor_csv": str(phase_csv),
        "input_event_pairs_csv": str(event_pairs_csv),
        "thresholds": {
            "max_range_ns": args.max_range_ns,
            "max_robust_sigma_ns": args.max_robust_sigma_ns,
            "min_stable_conventions": args.min_stable_conventions,
            "max_stable_median_spread_ns": args.max_stable_median_spread_ns,
            "accepted_convention": args.accepted_convention,
        },
        "summary": summary,
        "paths": {
            "event_offsets_csv": str(event_csv),
            "convention_summary_csv": str(convention_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_phase_convention_transfer_policy",
        {
            "summary_json": str(summary_json),
            "event_offsets_csv": str(event_csv),
            "convention_summary_csv": str(convention_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
