#!/usr/bin/env python3
"""Diagnose target2 archive ambiguity rows at the objective-near-tie level."""

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


def ambiguity_dimensions_from_raw(row: dict) -> str:
    dims: list[str] = []
    if safe_float(row.get("ambiguity_x_width_mm"), 0.0) > 0.0:
        dims.append("x")
    if safe_float(row.get("ambiguity_z_width_mm"), 0.0) > 0.0:
        dims.append("z")
    if safe_float(row.get("ambiguity_radius_width_mm"), 0.0) > 0.0:
        dims.append("radius")
    return "+".join(dims)


def diagnostic_class(row: dict) -> str:
    dims = set(str(row.get("ambiguity_dimensions", "")).split("+"))
    dims.discard("")
    x_width = safe_float(row.get("x_ambiguity_width_mm"), 0.0)
    z_width = safe_float(row.get("z_ambiguity_width_mm"), 0.0)
    radius_width = safe_float(row.get("radius_ambiguity_width_mm"), 0.0)
    dx = abs(safe_float(row.get("competitor_delta_x_mm"), 0.0))
    dz = abs(safe_float(row.get("competitor_delta_z_mm"), 0.0))
    dr = abs(safe_float(row.get("competitor_delta_radius_mm"), 0.0))
    within = bool(row.get("competitor_within_ambiguity_threshold"))
    if dims == {"x"} and x_width <= 1.0 and dx <= 1.0 and dz == 0.0 and dr == 0.0 and within:
        return "one_mm_lateral_near_tie"
    if dims == {"z", "radius"} and z_width <= 1.0 and radius_width <= 0.75 and dx == 0.0 and within:
        return "depth_radius_coupled_near_tie"
    return "mixed_objective_near_tie"


def diagnostic_rows_from_aggregates(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        aggregate_run = path.parents[1].name
        for raw in read_csv_rows(path):
            dims = ambiguity_dimensions_from_raw(raw)
            exact = boolish(raw.get("is_truth_geometry"))
            strong = str(raw.get("confidence_label", "")) == "strong"
            target_index = int(safe_float(raw.get("step_target_index", raw.get("target_rebar_index", -1)), -1))
            if not (exact and strong and dims and target_index == 2):
                continue
            best = safe_float(raw.get("best_misfit"))
            competitor = safe_float(raw.get("competing_geometry_misfit"))
            threshold = safe_float(raw.get("ambiguity_misfit_threshold"))
            objective_gap = competitor - best if math.isfinite(best) and math.isfinite(competitor) else math.nan
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
                "family_label": family_label({
                    "aggregate_run": aggregate_run,
                    "run_name": raw.get("run_name", ""),
                    "case_label": raw.get("case_label", ""),
                    "target_index": target_index,
                }),
                "target_index": target_index,
                "sources": safe_float(raw.get("sources")),
                "tx_rx_offset_mm": safe_float(raw.get("tx_rx_offset_mm")),
                "ambiguity_dimensions": dims,
                "x_ambiguity_width_mm": safe_float(raw.get("ambiguity_x_width_mm"), 0.0),
                "z_ambiguity_width_mm": safe_float(raw.get("ambiguity_z_width_mm"), 0.0),
                "radius_ambiguity_width_mm": safe_float(raw.get("ambiguity_radius_width_mm"), 0.0),
                "best_misfit": best,
                "competing_geometry_misfit": competitor,
                "ambiguity_misfit_threshold": threshold,
                "competitor_objective_gap_abs": objective_gap,
                "competitor_objective_gap_rel": objective_gap / abs(best) if math.isfinite(objective_gap) and best else math.nan,
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
                "radius_margin_abs": safe_float(raw.get("radius_margin_abs")),
                "source_frequency_scale": safe_float(raw.get("source_frequency_scale")),
                "source_time_shift_ps": safe_float(raw.get("source_time_shift_ps")),
                "source_amplitude_scale": safe_float(raw.get("source_amplitude_scale")),
                "branch_case": (
                    "source_mismatch"
                    if str(raw.get("case_label", "")).startswith("source_mismatch")
                    else "nominal"
                ),
            }
            row["diagnostic_class"] = diagnostic_class(row)
            row["recommended_action"] = "filter_from_strict_clean_claims_and_report_near_tie"
            rows.append(row)
    return sorted(rows, key=lambda item: (
        item["family_label"],
        item["aggregate_run"],
        item["run_name"],
        item["case_label"],
    ))


def summarize_objective_diagnostic(rows: list[dict]) -> dict:
    classes = {label: sum(1 for row in rows if row["diagnostic_class"] == label) for label in sorted({
        row["diagnostic_class"] for row in rows
    })}
    gaps = [
        safe_float(row.get("competitor_objective_gap_abs"))
        for row in rows
        if math.isfinite(safe_float(row.get("competitor_objective_gap_abs")))
    ]
    margins = [
        safe_float(row.get("competitor_margin_inside_threshold_abs"))
        for row in rows
        if math.isfinite(safe_float(row.get("competitor_margin_inside_threshold_abs")))
    ]
    family_count = len({row["family_label"] for row in rows})
    all_within = all(bool(row.get("competitor_within_ambiguity_threshold")) for row in rows) if rows else False
    if rows and all_within and classes.get("mixed_objective_near_tie", 0) == 0:
        label = "target2_archive_ambiguity_near_tie_diagnostic_cpu_no_gpu"
    elif rows:
        label = "target2_archive_ambiguity_mixed_objective_diagnostic_cpu_no_gpu"
    else:
        label = "target2_archive_ambiguity_no_rows"
    return {
        "policy_label": label,
        "row_count": len(rows),
        "family_count": family_count,
        "competitor_within_threshold_count": sum(
            1 for row in rows if bool(row.get("competitor_within_ambiguity_threshold"))
        ),
        "all_competitors_within_ambiguity_threshold": all_within,
        "one_mm_lateral_near_tie_count": classes.get("one_mm_lateral_near_tie", 0),
        "depth_radius_coupled_near_tie_count": classes.get("depth_radius_coupled_near_tie", 0),
        "mixed_objective_near_tie_count": classes.get("mixed_objective_near_tie", 0),
        "min_competitor_objective_gap_abs": min(gaps) if gaps else math.nan,
        "max_competitor_objective_gap_abs": max(gaps) if gaps else math.nan,
        "min_competitor_margin_inside_threshold_abs": min(margins) if margins else math.nan,
        "max_competitor_margin_inside_threshold_abs": max(margins) if margins else math.nan,
        "max_x_ambiguity_width_mm": max([row["x_ambiguity_width_mm"] for row in rows], default=math.nan),
        "max_z_ambiguity_width_mm": max([row["z_ambiguity_width_mm"] for row in rows], default=math.nan),
        "max_radius_ambiguity_width_mm": max(
            [row["radius_ambiguity_width_mm"] for row in rows],
            default=math.nan,
        ),
        "gpu_priority": "none_now",
        "decision": (
            "The target2 archive strict-clean exceptions are objective near-ties "
            "inside the ambiguity threshold. Use them to enforce reporting "
            "filters or design CPU-side objective-margin diagnostics before "
            "considering any new GPU run."
        ),
    }


def plot_objective_diagnostic(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [str(index + 1) for index in range(len(rows))]
    x = np.arange(len(rows))
    family_colors = {
        "target2_variable_radius_legacy": "#4c78a8",
        "target2_close14": "#2f9d55",
        "target2_close50": "#f58518",
        "target2_variable_depth_radius": "#7f3c8d",
    }
    colors = [family_colors.get(row["family_label"], "#6b6b6b") for row in rows]
    gap = np.asarray([safe_float(row.get("competitor_objective_gap_abs")) for row in rows], dtype=np.float64)
    threshold_margin = np.asarray(
        [safe_float(row.get("competitor_margin_inside_threshold_abs")) for row in rows],
        dtype=np.float64,
    )
    x_width = np.asarray([safe_float(row.get("x_ambiguity_width_mm")) for row in rows], dtype=np.float64)
    z_width = np.asarray([safe_float(row.get("z_ambiguity_width_mm")) for row in rows], dtype=np.float64)
    radius_width = np.asarray([safe_float(row.get("radius_ambiguity_width_mm")) for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(13.2, 9.2), constrained_layout=True)
    axes[0].bar(x, gap, color=colors)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("competitor-best misfit")
    axes[0].set_title("Near-best competitor objective gap")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, threshold_margin, color=colors)
    axes[1].axhline(0.0, color="#555555", linewidth=0.8)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("threshold-competitor misfit")
    axes[1].set_title("Positive values mean competitor remains inside ambiguity threshold")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(x, x_width, color="#c7302b", label="x")
    axes[2].bar(x, z_width, bottom=x_width, color="#f58518", label="z")
    axes[2].bar(x, radius_width, bottom=x_width + z_width, color="#7f3c8d", label="radius")
    axes[2].set_xticks(x, labels)
    axes[2].set_ylabel("ambiguity width [mm]")
    axes[2].set_xlabel("diagnostic row index")
    axes[2].set_title("Geometry ambiguity dimensions")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[2].legend(frameon=False, fontsize=8)

    fig.suptitle(
        f"Target2 archive ambiguity objective diagnostic: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--include-smoke", action="store_true")
    parser.add_argument("--run-name", default="target2_archive_ambiguity_objective_diagnostic")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    paths = aggregate_csv_paths(Path(args.experiment_root), include_smoke=args.include_smoke)
    rows = diagnostic_rows_from_aggregates(paths)
    summary = summarize_objective_diagnostic(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "target2_archive_ambiguity_objective_diagnostic_rows.csv"
    summary_json = data_dir / "target2_archive_ambiguity_objective_diagnostic_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_objective_diagnostic(
        rows,
        summary,
        figures_dir / "target2_archive_ambiguity_objective_diagnostic.png",
    ))

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
        "target2_archive_ambiguity_objective_diagnostic",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
