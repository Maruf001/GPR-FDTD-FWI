#!/usr/bin/env python3
"""Build manuscript-ready synthetic claim tiers from geometry and competitor audits."""

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
from run_archive_location_clean_metric_audit import safe_float  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_GEOMETRY_SUMMARY_ROWS = (
    "outputs/experiments/1285_cross_target_objective_reporting_tiers/data/"
    "cross_target_objective_reporting_tier_summary_rows.csv"
)
DEFAULT_COMPETITOR_SUMMARY_ROWS = (
    "outputs/experiments/1287_competing_geometry_near_tie_audit/data/"
    "competing_geometry_near_tie_summary_rows.csv"
)


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def claim_tier_rows(geometry_rows: list[dict], competitor_rows: list[dict]) -> list[dict]:
    competitor_by_target = {str(row["target_index"]): row for row in competitor_rows}
    out: list[dict] = []
    for geo in sorted(geometry_rows, key=lambda row: int(safe_float(row.get("target_index"), -1))):
        target = str(geo["target_index"])
        comp = competitor_by_target.get(target, {})
        exact = int(safe_float(geo.get("exact_strong_row_count"), 0))
        geometry_clean = int(safe_float(geo.get("strict_location_clean_count"), 0))
        geometry_ambiguous = int(safe_float(geo.get("geometry_ambiguous_count"), 0))
        objective_unique = int(safe_float(comp.get("competitor_separated_count"), 0))
        hidden = int(safe_float(comp.get("zero_width_competing_geometry_near_tie_count"), 0))
        reported = int(safe_float(comp.get("reported_width_near_tie_count"), 0))
        out.append({
            "target_index": int(safe_float(target, -1)),
            "exact_strong_row_count": exact,
            "geometry_clean_row_count": geometry_clean,
            "geometry_ambiguous_row_count": geometry_ambiguous,
            "objective_unique_row_count": objective_unique,
            "reported_width_near_tie_count": reported,
            "zero_width_competing_geometry_near_tie_count": hidden,
            "geometry_clean_fraction": geometry_clean / exact if exact else math.nan,
            "objective_unique_fraction": objective_unique / exact if exact else math.nan,
            "claim_tier_label": (
                "all_objective_unique"
                if exact and objective_unique == exact
                else "geometry_clean_but_objective_near_ties"
                if geometry_clean == exact
                else "geometry_and_objective_near_ties"
            ),
            "recommended_wording": (
                "Can support exact-strong, geometry-clean, and objective-unique wording."
                if exact and objective_unique == exact
                else "Can support geometry-clean wording, but objective uniqueness needs caveats."
                if geometry_clean == exact
                else "Requires both geometry-clean and objective-uniqueness caveats."
            ),
        })
    return out


def summarize_claim_tiers(rows: list[dict]) -> dict:
    exact = sum(row["exact_strong_row_count"] for row in rows)
    geometry_clean = sum(row["geometry_clean_row_count"] for row in rows)
    objective_unique = sum(row["objective_unique_row_count"] for row in rows)
    hidden = sum(row["zero_width_competing_geometry_near_tie_count"] for row in rows)
    reported = sum(row["reported_width_near_tie_count"] for row in rows)
    if hidden and reported:
        label = "synthetic_claim_tiers_geometry_clean_and_objective_unique_separated_cpu_no_gpu"
    elif reported:
        label = "synthetic_claim_tiers_reported_near_ties_only_cpu_no_gpu"
    else:
        label = "synthetic_claim_tiers_all_objective_unique_cpu_no_gpu"
    return {
        "policy_label": label,
        "target_count": len(rows),
        "exact_strong_row_count": exact,
        "geometry_clean_row_count": geometry_clean,
        "objective_unique_row_count": objective_unique,
        "reported_width_near_tie_count": reported,
        "zero_width_competing_geometry_near_tie_count": hidden,
        "geometry_clean_fraction": geometry_clean / exact if exact else math.nan,
        "objective_unique_fraction": objective_unique / exact if exact else math.nan,
        "gpu_priority": "none_now",
        "decision": (
            "Manuscript tables should distinguish exact-strong, geometry-clean, "
            "and objective-unique claims. Objective uniqueness must use raw "
            "competitor threshold separation, not ambiguity-width fields alone."
        ),
    }


def plot_claim_tiers(rows: list[dict], summary: dict, save_path: Path) -> str:
    targets = [f"target {row['target_index']}" for row in rows]
    x = np.arange(len(rows))
    exact = np.asarray([row["exact_strong_row_count"] for row in rows], dtype=np.float64)
    geometry = np.asarray([row["geometry_clean_row_count"] for row in rows], dtype=np.float64)
    objective = np.asarray([row["objective_unique_row_count"] for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    axes[0].bar(x - 0.24, exact, width=0.24, color="#6b6b6b", label="exact strong")
    axes[0].bar(x, geometry, width=0.24, color="#4c78a8", label="geometry clean")
    axes[0].bar(x + 0.24, objective, width=0.24, color="#2f9d55", label="objective unique")
    axes[0].set_xticks(x, targets)
    axes[0].set_ylabel("row count")
    axes[0].set_title("Claim tier row counts")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    geometry_frac = np.asarray([row["geometry_clean_fraction"] for row in rows], dtype=np.float64)
    objective_frac = np.asarray([row["objective_unique_fraction"] for row in rows], dtype=np.float64)
    axes[1].bar(x - 0.18, geometry_frac, width=0.36, color="#4c78a8", label="geometry clean")
    axes[1].bar(x + 0.18, objective_frac, width=0.36, color="#2f9d55", label="objective unique")
    axes[1].set_xticks(x, targets)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_ylabel("fraction of exact-strong rows")
    axes[1].set_title("Claim tier fractions")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Synthetic claim tier table: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry-summary-rows-csv", default=DEFAULT_GEOMETRY_SUMMARY_ROWS)
    parser.add_argument("--competitor-summary-rows-csv", default=DEFAULT_COMPETITOR_SUMMARY_ROWS)
    parser.add_argument("--run-name", default="synthetic_claim_tier_table")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = claim_tier_rows(
        read_csv_rows(Path(args.geometry_summary_rows_csv)),
        read_csv_rows(Path(args.competitor_summary_rows_csv)),
    )
    summary = summarize_claim_tiers(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_claim_tier_rows.csv"
    summary_json = data_dir / "synthetic_claim_tier_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_claim_tiers(rows, summary, figures_dir / "synthetic_claim_tier_table.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "geometry_summary_rows_csv": args.geometry_summary_rows_csv,
        "competitor_summary_rows_csv": args.competitor_summary_rows_csv,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_claim_tier_table",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
