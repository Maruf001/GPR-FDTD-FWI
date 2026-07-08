#!/usr/bin/env python3
"""Audit target2 exact-strong objective margins across archive aggregates."""

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
from run_archive_location_clean_metric_audit import (  # noqa: E402
    aggregate_csv_paths,
    boolish,
    read_csv_rows,
    safe_float,
)
from run_archive_location_ambiguity_family_breakdown import family_label  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def margin_label(row: dict) -> str:
    if bool(row.get("geometry_ambiguous")):
        return "geometry_ambiguous_near_tie"
    if bool(row.get("competitor_within_ambiguity_threshold")) and safe_float(row.get("ambiguity_candidate_count"), 0.0) > 1.0:
        return "zero_width_objective_near_tie"
    return "strict_location_clean_margin_separated"


def objective_margin_rows(paths: list[Path]) -> list[dict]:
    out: list[dict] = []
    for path in paths:
        aggregate_run = path.parents[1].name
        for raw in read_csv_rows(path):
            exact = boolish(raw.get("is_truth_geometry"))
            strong = str(raw.get("confidence_label", "")) == "strong"
            target_index = int(safe_float(raw.get("step_target_index", raw.get("target_rebar_index", -1)), -1))
            if not (exact and strong and target_index == 2):
                continue
            x_width = safe_float(raw.get("ambiguity_x_width_mm"), 0.0)
            z_width = safe_float(raw.get("ambiguity_z_width_mm"), 0.0)
            radius_width = safe_float(raw.get("ambiguity_radius_width_mm"), 0.0)
            best = safe_float(raw.get("best_misfit"))
            competitor = safe_float(raw.get("competing_geometry_misfit"))
            threshold = safe_float(raw.get("ambiguity_misfit_threshold"))
            objective_gap = competitor - best if math.isfinite(best) and math.isfinite(competitor) else math.nan
            threshold_margin = threshold - competitor if math.isfinite(threshold) and math.isfinite(competitor) else math.nan
            geometry_ambiguous = x_width > 0.0 or z_width > 0.0 or radius_width > 0.0
            row = {
                "aggregate_run": aggregate_run,
                "source_csv": str(path),
                "run_name": raw.get("run_name", ""),
                "case_label": raw.get("case_label", ""),
                "family_label": family_label({
                    "aggregate_run": aggregate_run,
                    "run_name": raw.get("run_name", ""),
                    "case_label": raw.get("case_label", ""),
                    "target_index": target_index,
                }),
                "target_index": target_index,
                "sources": safe_float(raw.get("sources")),
                "tx_rx_offset_mm": safe_float(raw.get("tx_rx_offset_mm")),
                "ambiguity_candidate_count": safe_float(raw.get("ambiguity_candidate_count"), 0.0),
                "x_ambiguity_width_mm": x_width,
                "z_ambiguity_width_mm": z_width,
                "radius_ambiguity_width_mm": radius_width,
                "strict_location_clean": not geometry_ambiguous,
                "geometry_ambiguous": geometry_ambiguous,
                "best_misfit": best,
                "competing_geometry_misfit": competitor,
                "ambiguity_misfit_threshold": threshold,
                "competitor_objective_gap_abs": objective_gap,
                "competitor_objective_gap_rel": objective_gap / abs(best) if math.isfinite(objective_gap) and best else math.nan,
                "competitor_margin_inside_threshold_abs": threshold_margin,
                "competitor_within_ambiguity_threshold": threshold_margin >= 0.0 if math.isfinite(threshold_margin) else False,
                "radius_margin_abs": safe_float(raw.get("radius_margin_abs")),
                "branch_case": (
                    "source_mismatch"
                    if str(raw.get("case_label", "")).startswith("source_mismatch")
                    else "nominal"
                ),
            }
            row["margin_label"] = margin_label(row)
            out.append(row)
    return sorted(out, key=lambda item: (
        item["margin_label"],
        item["family_label"],
        item["aggregate_run"],
        item["run_name"],
        item["case_label"],
    ))


def summarize_margin_audit(rows: list[dict]) -> dict:
    strict_clean = [row for row in rows if bool(row.get("strict_location_clean"))]
    geometry_ambiguous = [row for row in rows if bool(row.get("geometry_ambiguous"))]
    zero_width_near_ties = [row for row in rows if row.get("margin_label") == "zero_width_objective_near_tie"]
    separated = [row for row in rows if row.get("margin_label") == "strict_location_clean_margin_separated"]
    gaps = [
        safe_float(row.get("competitor_objective_gap_abs"))
        for row in rows
        if math.isfinite(safe_float(row.get("competitor_objective_gap_abs")))
    ]
    separated_gaps = [
        safe_float(row.get("competitor_objective_gap_abs"))
        for row in separated
        if math.isfinite(safe_float(row.get("competitor_objective_gap_abs")))
    ]
    if geometry_ambiguous and zero_width_near_ties:
        label = "target2_objective_margin_geometry_clean_but_near_ties_present_cpu_no_gpu"
    elif geometry_ambiguous:
        label = "target2_objective_margin_geometry_ambiguity_present_cpu_no_gpu"
    else:
        label = "target2_objective_margin_all_strict_clean_cpu_no_gpu"
    return {
        "policy_label": label,
        "row_count": len(rows),
        "strict_location_clean_count": len(strict_clean),
        "geometry_ambiguous_count": len(geometry_ambiguous),
        "zero_width_objective_near_tie_count": len(zero_width_near_ties),
        "strict_location_clean_margin_separated_count": len(separated),
        "competitor_within_threshold_count": sum(
            1 for row in rows if bool(row.get("competitor_within_ambiguity_threshold"))
        ),
        "strict_location_clean_fraction": len(strict_clean) / len(rows) if rows else math.nan,
        "min_competitor_objective_gap_abs": min(gaps) if gaps else math.nan,
        "max_competitor_objective_gap_abs": max(gaps) if gaps else math.nan,
        "min_separated_competitor_objective_gap_abs": min(separated_gaps) if separated_gaps else math.nan,
        "gpu_priority": "none_now",
        "decision": (
            "Target2 exact-strong rows need two reporting tiers: strict "
            "location-clean geometry and objective-margin separation. "
            "Zero-width near-ties do not undermine location-clean claims, but "
            "they should prevent claims of a uniquely isolated objective basin."
        ),
    }


def plot_margin_audit(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [
        "geometry\nambiguous",
        "zero-width\nnear tie",
        "strict clean\nseparated",
    ]
    counts = [
        summary["geometry_ambiguous_count"],
        summary["zero_width_objective_near_tie_count"],
        summary["strict_location_clean_margin_separated_count"],
    ]
    class_colors = {
        "geometry_ambiguous_near_tie": "#c7302b",
        "zero_width_objective_near_tie": "#d99a19",
        "strict_location_clean_margin_separated": "#2f9d55",
    }
    sorted_rows = sorted(
        rows,
        key=lambda row: safe_float(row.get("competitor_objective_gap_abs"), math.inf),
    )
    x = np.arange(len(sorted_rows))
    gaps = np.asarray([safe_float(row.get("competitor_objective_gap_abs")) for row in sorted_rows], dtype=np.float64)
    colors = [class_colors.get(row["margin_label"], "#6b6b6b") for row in sorted_rows]

    fig, axes = plt.subplots(1, 2, figsize=(13.4, 4.8), constrained_layout=True)
    axes[0].bar(labels, counts, color=["#c7302b", "#d99a19", "#2f9d55"])
    axes[0].set_ylabel("target2 exact-strong row count")
    axes[0].set_title("Objective-margin reporting tiers")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, gaps, color=colors, width=0.8)
    axes[1].set_ylabel("competitor-best misfit")
    axes[1].set_xlabel("target2 exact-strong rows sorted by objective gap")
    axes[1].set_title("Objective gap distribution")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Target2 objective-margin archive audit: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--include-smoke", action="store_true")
    parser.add_argument("--run-name", default="target2_objective_margin_archive_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    paths = aggregate_csv_paths(Path(args.experiment_root), include_smoke=args.include_smoke)
    rows = objective_margin_rows(paths)
    summary = summarize_margin_audit(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "target2_objective_margin_archive_rows.csv"
    summary_json = data_dir / "target2_objective_margin_archive_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_margin_audit(rows, summary, figures_dir / "target2_objective_margin_archive_audit.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "aggregate_file_count": len(paths),
        "include_smoke": args.include_smoke,
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
        "target2_objective_margin_archive_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
