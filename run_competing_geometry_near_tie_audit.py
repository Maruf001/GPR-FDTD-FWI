#!/usr/bin/env python3
"""Audit exact-strong rows for near-threshold competing geometry deltas."""

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


def geometry_delta_class(row: dict) -> str:
    dx = abs(safe_float(row.get("competitor_delta_x_mm"), 0.0))
    dz = abs(safe_float(row.get("competitor_delta_z_mm"), 0.0))
    dr = abs(safe_float(row.get("competitor_delta_radius_mm"), 0.0))
    parts: list[str] = []
    if dx > 0.0:
        parts.append("x")
    if dz > 0.0:
        parts.append("z")
    if dr > 0.0:
        parts.append("radius")
    return "+".join(parts) if parts else "none"


def near_tie_tier(row: dict) -> str:
    if not bool(row.get("competitor_within_ambiguity_threshold")):
        return "competitor_separated"
    if bool(row.get("ambiguity_width_nonzero")):
        return "reported_width_near_tie"
    if geometry_delta_class(row) != "none":
        return "zero_width_competing_geometry_near_tie"
    return "zero_width_duplicate_objective_near_tie"


def audit_rows(paths: list[Path]) -> list[dict]:
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
            threshold_margin = threshold - competitor if math.isfinite(threshold) and math.isfinite(competitor) else math.nan
            best_x = safe_float(raw.get("best_x_mm"))
            best_z = safe_float(raw.get("best_z_mm"))
            best_radius = safe_float(raw.get("best_radius_mm"))
            comp_x = safe_float(raw.get("competing_geometry_x_mm"))
            comp_z = safe_float(raw.get("competing_geometry_z_mm"))
            comp_radius = safe_float(raw.get("competing_geometry_radius_mm"))
            row = {
                "aggregate_run": aggregate_run,
                "source_csv": str(path),
                "run_name": raw.get("run_name", ""),
                "case_label": raw.get("case_label", ""),
                "target_index": target_index,
                "sources": safe_float(raw.get("sources")),
                "tx_rx_offset_mm": safe_float(raw.get("tx_rx_offset_mm")),
                "ambiguity_candidate_count": safe_float(raw.get("ambiguity_candidate_count"), 0.0),
                "ambiguity_width_nonzero": x_width > 0.0 or z_width > 0.0 or radius_width > 0.0,
                "x_ambiguity_width_mm": x_width,
                "z_ambiguity_width_mm": z_width,
                "radius_ambiguity_width_mm": radius_width,
                "best_misfit": best,
                "competing_geometry_misfit": competitor,
                "ambiguity_misfit_threshold": threshold,
                "competitor_objective_gap_abs": (
                    competitor - best if math.isfinite(best) and math.isfinite(competitor) else math.nan
                ),
                "competitor_margin_inside_threshold_abs": threshold_margin,
                "competitor_within_ambiguity_threshold": threshold_margin >= 0.0 if math.isfinite(threshold_margin) else False,
                "best_x_mm": best_x,
                "best_z_mm": best_z,
                "best_radius_mm": best_radius,
                "competing_geometry_x_mm": comp_x,
                "competing_geometry_z_mm": comp_z,
                "competing_geometry_radius_mm": comp_radius,
                "competitor_delta_x_mm": comp_x - best_x if math.isfinite(comp_x) and math.isfinite(best_x) else math.nan,
                "competitor_delta_z_mm": comp_z - best_z if math.isfinite(comp_z) and math.isfinite(best_z) else math.nan,
                "competitor_delta_radius_mm": (
                    comp_radius - best_radius
                    if math.isfinite(comp_radius) and math.isfinite(best_radius)
                    else math.nan
                ),
            }
            row["geometry_delta_class"] = geometry_delta_class(row)
            row["near_tie_tier"] = near_tie_tier(row)
            row["recommended_reporting_action"] = (
                "exclude_from_objective_unique_claim"
                if row["near_tie_tier"] != "competitor_separated"
                else "eligible_for_objective_separated_claim"
            )
            rows.append(row)
    return sorted(rows, key=lambda item: (
        item["target_index"],
        item["near_tie_tier"],
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
        reported = [row for row in group if row["near_tie_tier"] == "reported_width_near_tie"]
        hidden = [row for row in group if row["near_tie_tier"] == "zero_width_competing_geometry_near_tie"]
        duplicates = [row for row in group if row["near_tie_tier"] == "zero_width_duplicate_objective_near_tie"]
        separated = [row for row in group if row["near_tie_tier"] == "competitor_separated"]
        out.append({
            "target_index": target,
            "exact_strong_row_count": len(group),
            "reported_width_near_tie_count": len(reported),
            "zero_width_competing_geometry_near_tie_count": len(hidden),
            "zero_width_duplicate_objective_near_tie_count": len(duplicates),
            "competitor_separated_count": len(separated),
            "objective_unique_eligible_fraction": len(separated) / len(group) if group else math.nan,
            "geometry_delta_classes": ";".join(sorted({
                row["geometry_delta_class"]
                for row in reported + hidden
                if row["geometry_delta_class"] != "none"
            })),
        })
    return out


def summarize_audit(rows: list[dict], summary_rows: list[dict]) -> dict:
    reported = sum(row["reported_width_near_tie_count"] for row in summary_rows)
    hidden = sum(row["zero_width_competing_geometry_near_tie_count"] for row in summary_rows)
    duplicates = sum(row["zero_width_duplicate_objective_near_tie_count"] for row in summary_rows)
    separated = sum(row["competitor_separated_count"] for row in summary_rows)
    hidden_targets = [
        row["target_index"]
        for row in summary_rows
        if row["zero_width_competing_geometry_near_tie_count"] > 0
    ]
    if hidden:
        label = "competing_geometry_near_tie_zero_width_metric_gap_cpu_no_gpu"
    elif reported:
        label = "competing_geometry_near_tie_reported_width_only_cpu_no_gpu"
    else:
        label = "competing_geometry_near_tie_not_present_cpu_no_gpu"
    return {
        "policy_label": label,
        "exact_strong_row_count": len(rows),
        "reported_width_near_tie_count": reported,
        "zero_width_competing_geometry_near_tie_count": hidden,
        "zero_width_duplicate_objective_near_tie_count": duplicates,
        "competitor_separated_count": separated,
        "hidden_near_tie_targets": ";".join(str(value) for value in hidden_targets),
        "objective_unique_eligible_fraction": separated / len(rows) if rows else math.nan,
        "gpu_priority": "none_now",
        "recommended_metric": (
            "objective_unique_candidate = exact_strong and "
            "not competitor_within_ambiguity_threshold"
        ),
        "decision": (
            "Ambiguity-width-only reporting misses zero-width competing-geometry "
            "near-ties. Use the raw competitor threshold test for objective "
            "uniqueness wording; keep geometry-clean and objective-unique as "
            "separate claims."
        ),
    }


def plot_audit(summary_rows: list[dict], summary: dict, save_path: Path) -> str:
    targets = [f"target {row['target_index']}" for row in summary_rows]
    x = np.arange(len(summary_rows))
    reported = np.asarray([row["reported_width_near_tie_count"] for row in summary_rows], dtype=np.float64)
    hidden = np.asarray([row["zero_width_competing_geometry_near_tie_count"] for row in summary_rows], dtype=np.float64)
    duplicates = np.asarray([row["zero_width_duplicate_objective_near_tie_count"] for row in summary_rows], dtype=np.float64)
    separated = np.asarray([row["competitor_separated_count"] for row in summary_rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    axes[0].bar(x, reported, color="#c7302b", label="reported-width near tie")
    axes[0].bar(x, hidden, bottom=reported, color="#d99a19", label="zero-width competing geometry")
    axes[0].bar(x, duplicates, bottom=reported + hidden, color="#7f3c8d", label="zero-width duplicate")
    axes[0].bar(x, separated, bottom=reported + hidden + duplicates, color="#2f9d55", label="competitor separated")
    axes[0].set_xticks(x, targets)
    axes[0].set_ylabel("exact-strong row count")
    axes[0].set_title("Competing-geometry near-tie tiers")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    fractions = np.asarray([row["objective_unique_eligible_fraction"] for row in summary_rows], dtype=np.float64)
    axes[1].bar(x, fractions, color="#4c78a8")
    axes[1].set_xticks(x, targets)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_ylabel("objective-unique eligible fraction")
    axes[1].set_title("Rows eligible for objective-unique wording")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Competing geometry near-tie audit: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--include-smoke", action="store_true")
    parser.add_argument("--run-name", default="competing_geometry_near_tie_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    paths = aggregate_csv_paths(Path(args.experiment_root), include_smoke=args.include_smoke)
    rows = audit_rows(paths)
    summary_rows = target_summary_rows(rows)
    summary = summarize_audit(rows, summary_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "competing_geometry_near_tie_rows.csv"
    summary_rows_csv = data_dir / "competing_geometry_near_tie_summary_rows.csv"
    summary_json = data_dir / "competing_geometry_near_tie_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_audit(summary_rows, summary, figures_dir / "competing_geometry_near_tie_audit.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(summary_rows_csv, [json_safe(row) for row in summary_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "aggregate_file_count": len(paths),
        "include_smoke": args.include_smoke,
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_rows_csv": str(summary_rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "competing_geometry_near_tie_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "summary_rows_csv": str(summary_rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
