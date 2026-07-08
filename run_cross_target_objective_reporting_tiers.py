#!/usr/bin/env python3
"""Summarize objective-reporting tiers across target0/1/2 archive rows."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict
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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def reporting_tier(row: dict) -> str:
    if bool(row.get("geometry_ambiguous")):
        return "geometry_ambiguous_near_tie"
    if bool(row.get("competitor_within_ambiguity_threshold")) and safe_float(row.get("ambiguity_candidate_count"), 0.0) > 1.0:
        return "zero_width_objective_near_tie"
    return "strict_location_clean_margin_separated"


def reporting_tier_rows(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        aggregate_run = path.parents[1].name
        for raw in read_csv_rows(path):
            exact = boolish(raw.get("is_truth_geometry"))
            strong = str(raw.get("confidence_label", "")) == "strong"
            if not (exact and strong):
                continue
            target_index = int(safe_float(raw.get("step_target_index", raw.get("target_rebar_index", -1)), -1))
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
                "target_index": target_index,
                "sources": safe_float(raw.get("sources")),
                "tx_rx_offset_mm": safe_float(raw.get("tx_rx_offset_mm")),
                "ambiguity_candidate_count": safe_float(raw.get("ambiguity_candidate_count"), 0.0),
                "x_ambiguity_width_mm": x_width,
                "z_ambiguity_width_mm": z_width,
                "radius_ambiguity_width_mm": radius_width,
                "geometry_ambiguous": geometry_ambiguous,
                "strict_location_clean": not geometry_ambiguous,
                "competitor_within_ambiguity_threshold": threshold_margin >= 0.0 if math.isfinite(threshold_margin) else False,
                "competitor_objective_gap_abs": objective_gap,
                "competitor_margin_inside_threshold_abs": threshold_margin,
                "radius_margin_abs": safe_float(raw.get("radius_margin_abs")),
            }
            row["reporting_tier"] = reporting_tier(row)
            rows.append(row)
    return sorted(rows, key=lambda item: (
        item["target_index"],
        item["reporting_tier"],
        item["aggregate_run"],
        item["run_name"],
        item["case_label"],
    ))


def target_summary_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[int(row["target_index"])].append(row)
    out: list[dict] = []
    for target, group in sorted(grouped.items()):
        strict_clean = [row for row in group if bool(row.get("strict_location_clean"))]
        geometry_ambiguous = [row for row in group if bool(row.get("geometry_ambiguous"))]
        zero_width = [row for row in group if row.get("reporting_tier") == "zero_width_objective_near_tie"]
        separated = [row for row in group if row.get("reporting_tier") == "strict_location_clean_margin_separated"]
        separated_gaps = [
            safe_float(row.get("competitor_objective_gap_abs"))
            for row in separated
            if math.isfinite(safe_float(row.get("competitor_objective_gap_abs")))
        ]
        out.append({
            "target_index": target,
            "exact_strong_row_count": len(group),
            "strict_location_clean_count": len(strict_clean),
            "geometry_ambiguous_count": len(geometry_ambiguous),
            "zero_width_objective_near_tie_count": len(zero_width),
            "strict_clean_margin_separated_count": len(separated),
            "competitor_within_threshold_count": sum(
                1 for row in group if bool(row.get("competitor_within_ambiguity_threshold"))
            ),
            "strict_location_clean_fraction": len(strict_clean) / len(group) if group else math.nan,
            "geometry_ambiguous_fraction": len(geometry_ambiguous) / len(group) if group else math.nan,
            "min_separated_competitor_objective_gap_abs": min(separated_gaps) if separated_gaps else math.nan,
        })
    return out


def summarize_cross_target(rows: list[dict], summary_rows: list[dict]) -> dict:
    geometry_targets = [
        row["target_index"]
        for row in summary_rows
        if row["geometry_ambiguous_count"] > 0
    ]
    zero_width_targets = [
        row["target_index"]
        for row in summary_rows
        if row["zero_width_objective_near_tie_count"] > 0
    ]
    if geometry_targets == [2] and set(zero_width_targets) == {1, 2}:
        label = "cross_target_reporting_tiers_target2_geometry_target1_target2_zero_width_cpu_no_gpu"
    elif geometry_targets:
        label = "cross_target_reporting_tiers_geometry_ambiguity_present_cpu_no_gpu"
    else:
        label = "cross_target_reporting_tiers_no_geometry_ambiguity_cpu_no_gpu"
    return {
        "policy_label": label,
        "exact_strong_row_count": len(rows),
        "target_count": len(summary_rows),
        "geometry_ambiguous_row_count": sum(row["geometry_ambiguous_count"] for row in summary_rows),
        "zero_width_objective_near_tie_row_count": sum(
            row["zero_width_objective_near_tie_count"] for row in summary_rows
        ),
        "strict_clean_margin_separated_row_count": sum(
            row["strict_clean_margin_separated_count"] for row in summary_rows
        ),
        "geometry_ambiguous_targets": ";".join(str(value) for value in geometry_targets),
        "zero_width_objective_near_tie_targets": ";".join(str(value) for value in zero_width_targets),
        "gpu_priority": "none_now",
        "decision": (
            "Use cross-target reporting tiers in manuscript tables: target2 "
            "has geometry ambiguity, while target1 and target2 also have "
            "zero-width objective near-ties that limit objective-uniqueness "
            "wording without undermining location-clean geometry claims."
        ),
    }


def plot_cross_target(summary_rows: list[dict], summary: dict, save_path: Path) -> str:
    targets = [f"target {row['target_index']}" for row in summary_rows]
    x = np.arange(len(summary_rows))
    geometry = np.asarray([row["geometry_ambiguous_count"] for row in summary_rows], dtype=np.float64)
    zero_width = np.asarray([row["zero_width_objective_near_tie_count"] for row in summary_rows], dtype=np.float64)
    separated = np.asarray([row["strict_clean_margin_separated_count"] for row in summary_rows], dtype=np.float64)
    strict_fraction = np.asarray([row["strict_location_clean_fraction"] for row in summary_rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    axes[0].bar(x, geometry, color="#c7302b", label="geometry ambiguous")
    axes[0].bar(x, zero_width, bottom=geometry, color="#d99a19", label="zero-width near tie")
    axes[0].bar(x, separated, bottom=geometry + zero_width, color="#2f9d55", label="strict clean separated")
    axes[0].set_xticks(x, targets)
    axes[0].set_ylabel("exact-strong row count")
    axes[0].set_title("Cross-target reporting tiers")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x, strict_fraction, color="#4c78a8")
    axes[1].set_xticks(x, targets)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_ylabel("strict location-clean fraction")
    axes[1].set_title("Geometry-clean fraction by target")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Cross-target objective reporting tiers: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--include-smoke", action="store_true")
    parser.add_argument("--run-name", default="cross_target_objective_reporting_tiers")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    paths = aggregate_csv_paths(Path(args.experiment_root), include_smoke=args.include_smoke)
    rows = reporting_tier_rows(paths)
    summary_rows = target_summary_rows(rows)
    summary = summarize_cross_target(rows, summary_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "cross_target_objective_reporting_tier_rows.csv"
    summary_csv = data_dir / "cross_target_objective_reporting_tier_summary_rows.csv"
    summary_json = data_dir / "cross_target_objective_reporting_tiers_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_cross_target(
        summary_rows,
        summary,
        figures_dir / "cross_target_objective_reporting_tiers.png",
    ))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(summary_csv, [json_safe(row) for row in summary_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "aggregate_file_count": len(paths),
        "include_smoke": args.include_smoke,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_rows_csv": str(summary_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "cross_target_objective_reporting_tiers",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "summary_rows_csv": str(summary_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
