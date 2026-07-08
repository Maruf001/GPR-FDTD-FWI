#!/usr/bin/env python3
"""Bootstrap uncertainty for the short-profile multi-phase timing transfer."""

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


DEFAULT_SOURCE_RUN = "027_gssi51600s_short_profile_phase_convention_transfer_policy"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_union_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        write_csv(path, [])
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    write_csv(path, [{key: row.get(key, "") for key in fieldnames} for row in rows])


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def stable_phase_conventions(summary_rows: list[dict]) -> list[str]:
    return [
        str(row["phase_convention"])
        for row in summary_rows
        if boolish(row.get("stable_transfer_convention"))
    ]


def stable_offset_rows(event_rows: list[dict], stable_conventions: list[str]) -> list[dict]:
    stable = set(stable_conventions)
    return [
        row for row in event_rows
        if str(row.get("phase_convention")) in stable
        and math.isfinite(safe_float(row.get("comparison_minus_reference_time_ns")))
    ]


def _quantile_summary(values: np.ndarray, alpha: float) -> tuple[float, float, float]:
    lower_q = 0.5 * alpha
    upper_q = 1.0 - 0.5 * alpha
    lower, median, upper = np.quantile(values, [lower_q, 0.5, upper_q])
    return float(lower), float(median), float(upper)


def bootstrap_cell_medians(
    values: np.ndarray,
    *,
    iterations: int,
    alpha: float,
    rng: np.random.Generator,
) -> dict:
    draws = np.empty(iterations, dtype=np.float64)
    for idx in range(iterations):
        draws[idx] = float(np.median(rng.choice(values, size=len(values), replace=True)))
    lower, median, upper = _quantile_summary(draws, alpha)
    return {
        "bootstrap_method": "cell",
        "sample_count": int(len(values)),
        "observed_median_ns": float(np.median(values)),
        "bootstrap_median_ns": median,
        "ci_lower_ns": lower,
        "ci_upper_ns": upper,
        "ci_width_ns": upper - lower,
    }


def bootstrap_cluster_medians(
    rows: list[dict],
    *,
    cluster_key: str,
    iterations: int,
    alpha: float,
    rng: np.random.Generator,
) -> dict:
    clusters = sorted({str(row[cluster_key]) for row in rows})
    by_cluster = {
        cluster: np.asarray([
            safe_float(row["comparison_minus_reference_time_ns"])
            for row in rows
            if str(row[cluster_key]) == cluster
        ], dtype=np.float64)
        for cluster in clusters
    }
    draws = np.empty(iterations, dtype=np.float64)
    for idx in range(iterations):
        selected = rng.choice(clusters, size=len(clusters), replace=True)
        draws[idx] = float(np.median(np.concatenate([by_cluster[cluster] for cluster in selected])))
    values = np.concatenate([by_cluster[cluster] for cluster in clusters])
    lower, median, upper = _quantile_summary(draws, alpha)
    return {
        "bootstrap_method": f"{cluster_key}_cluster",
        "cluster_count": int(len(clusters)),
        "sample_count": int(len(values)),
        "observed_median_ns": float(np.median(values)),
        "bootstrap_median_ns": median,
        "ci_lower_ns": lower,
        "ci_upper_ns": upper,
        "ci_width_ns": upper - lower,
    }


def summarize_bootstrap_policy(
    bootstrap_rows: list[dict],
    stable_rows: list[dict],
    *,
    min_ci_lower_ns: float,
    max_ci_width_ns: float,
    min_stable_conventions: int,
) -> dict:
    all_positive = all(safe_float(row.get("comparison_minus_reference_time_ns")) > 0.0 for row in stable_rows)
    lower_ok = all(safe_float(row.get("ci_lower_ns")) >= min_ci_lower_ns for row in bootstrap_rows)
    width_ok = all(safe_float(row.get("ci_width_ns")) <= max_ci_width_ns for row in bootstrap_rows)
    stable_convention_count = len({str(row["phase_convention"]) for row in stable_rows})
    supported = (
        all_positive
        and lower_ok
        and width_ok
        and stable_convention_count >= min_stable_conventions
    )
    if supported:
        label = "bootstrap_relative_time_zero_supported_qc"
    elif all_positive and lower_ok:
        label = "bootstrap_relative_time_zero_supported_limited"
    else:
        label = "bootstrap_relative_time_zero_not_stable"
    medians = [safe_float(row.get("observed_median_ns")) for row in bootstrap_rows]
    return {
        "policy_label": label,
        "stable_offset_count": len(stable_rows),
        "stable_phase_convention_count": stable_convention_count,
        "observed_median_offset_ns": float(np.median(medians)) if medians else math.nan,
        "all_stable_offsets_positive": all_positive,
        "all_bootstrap_ci_lower_bounds_clear_threshold": lower_ok,
        "all_bootstrap_ci_widths_within_threshold": width_ok,
        "min_bootstrap_ci_lower_ns": min(safe_float(row.get("ci_lower_ns")) for row in bootstrap_rows),
        "max_bootstrap_ci_upper_ns": max(safe_float(row.get("ci_upper_ns")) for row in bootstrap_rows),
        "max_bootstrap_ci_width_ns": max(safe_float(row.get("ci_width_ns")) for row in bootstrap_rows),
        "policy": (
            "Use this as uncertainty-bounded relative timing QC only. The interval "
            "is not an absolute calibrated time zero and does not support field "
            "radius, cover-depth, geometry, 3D, or FWI claims."
        ),
    }


def plot_bootstrap(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["bootstrap_method"] for row in rows]
    medians = np.asarray([safe_float(row.get("observed_median_ns")) for row in rows], dtype=np.float64)
    lower = np.asarray([safe_float(row.get("ci_lower_ns")) for row in rows], dtype=np.float64)
    upper = np.asarray([safe_float(row.get("ci_upper_ns")) for row in rows], dtype=np.float64)
    x = np.arange(len(rows))
    lower_err = medians - lower
    upper_err = upper - medians

    fig, ax = plt.subplots(figsize=(9.8, 4.8), constrained_layout=True)
    ax.errorbar(
        x,
        medians,
        yerr=np.vstack([lower_err, upper_err]),
        fmt="o",
        markersize=7,
        color="#2f6f9f",
        ecolor="#2f6f9f",
        elinewidth=2.0,
        capsize=5,
    )
    ax.axhline(0.0, color="#222222", linewidth=0.8)
    ax.set_xticks(x, labels, rotation=20, ha="right")
    ax.set_ylabel("016 - 014 relative offset [ns]")
    ax.set_title("Bootstrap uncertainty for short-profile relative timing")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--phase-convention-dir", default=None)
    parser.add_argument("--iterations", type=int, default=20000)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260617)
    parser.add_argument("--min-ci-lower-ns", type=float, default=0.09)
    parser.add_argument("--max-ci-width-ns", type=float, default=0.05)
    parser.add_argument("--min-stable-conventions", type=int, default=4)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_timing_bootstrap_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    source_dir = (
        Path(args.phase_convention_dir)
        if args.phase_convention_dir
        else dataset_root / DEFAULT_SOURCE_RUN
    )
    convention_summary_csv = source_dir / "data" / "short_profile_phase_convention_summary.csv"
    event_offsets_csv = source_dir / "data" / "short_profile_phase_convention_event_offsets.csv"
    convention_rows = read_csv_rows(convention_summary_csv)
    event_rows = read_csv_rows(event_offsets_csv)
    stable_conventions = stable_phase_conventions(convention_rows)
    stable_rows = stable_offset_rows(event_rows, stable_conventions)
    values = np.asarray([
        safe_float(row["comparison_minus_reference_time_ns"])
        for row in stable_rows
    ], dtype=np.float64)

    rng = np.random.default_rng(args.seed)
    bootstrap_rows = [
        bootstrap_cell_medians(values, iterations=args.iterations, alpha=args.alpha, rng=rng),
        bootstrap_cluster_medians(stable_rows, cluster_key="phase_convention", iterations=args.iterations, alpha=args.alpha, rng=rng),
        bootstrap_cluster_medians(stable_rows, cluster_key="pair_index", iterations=args.iterations, alpha=args.alpha, rng=rng),
    ]
    summary = summarize_bootstrap_policy(
        bootstrap_rows,
        stable_rows,
        min_ci_lower_ns=args.min_ci_lower_ns,
        max_ci_width_ns=args.max_ci_width_ns,
        min_stable_conventions=args.min_stable_conventions,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    stable_offsets_csv = data_dir / "short_profile_stable_phase_offsets.csv"
    bootstrap_csv = data_dir / "short_profile_timing_bootstrap_summary.csv"
    summary_json = data_dir / "short_profile_timing_bootstrap_policy_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_bootstrap(bootstrap_rows, summary, figures_dir / "short_profile_timing_bootstrap.png"))

    write_csv(stable_offsets_csv, [json_safe(row) for row in stable_rows])
    write_union_csv(bootstrap_csv, [json_safe(row) for row in bootstrap_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "phase_convention_dir": str(source_dir),
        "input_convention_summary_csv": str(convention_summary_csv),
        "input_event_offsets_csv": str(event_offsets_csv),
        "bootstrap": {
            "iterations": args.iterations,
            "alpha": args.alpha,
            "seed": args.seed,
        },
        "thresholds": {
            "min_ci_lower_ns": args.min_ci_lower_ns,
            "max_ci_width_ns": args.max_ci_width_ns,
            "min_stable_conventions": args.min_stable_conventions,
        },
        "summary": summary,
        "paths": {
            "stable_offsets_csv": str(stable_offsets_csv),
            "bootstrap_summary_csv": str(bootstrap_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_timing_bootstrap_policy",
        {
            "summary_json": str(summary_json),
            "stable_offsets_csv": str(stable_offsets_csv),
            "bootstrap_summary_csv": str(bootstrap_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
