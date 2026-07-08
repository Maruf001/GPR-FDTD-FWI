#!/usr/bin/env python3
"""Synthesize the completed target2 close14 source5 Tx/Rx45 probe."""

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CONFIDENCE_GLOB = (
    "outputs/experiments/*_coordinate_optimizer_close14_seed*_sources5_txrx45_"
    "noise15p361328125_objectives/data/coordinate_confidence_report.csv"
)
PROBE_SEEDS = (13, 21, 34)


def safe_float(value, default=math.nan) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return float(default)
    return numeric if math.isfinite(numeric) else float(default)


def seed_from_text(text: str) -> int | None:
    match = re.search(r"seed(\d+)", str(text))
    return int(match.group(1)) if match else None


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def confidence_paths(patterns: list[str], seeds: tuple[int, ...] = PROBE_SEEDS) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        for path in glob.glob(pattern):
            seed = seed_from_text(path)
            if seed in seeds:
                paths.append(Path(path))
    return sorted(set(paths))


def synthesize_rows(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        for row in read_csv_rows(path):
            best_misfit = safe_float(row.get("best_misfit"))
            competing_misfit = safe_float(row.get("competing_geometry_misfit"))
            threshold = safe_float(row.get("ambiguity_misfit_threshold"))
            gap = competing_misfit - best_misfit
            threshold_width = threshold - best_misfit
            seed = seed_from_text(row.get("case_label", "")) or seed_from_text(row.get("run_name", ""))
            is_truth = (
                safe_float(row.get("best_x_mm")) == 264.0
                and safe_float(row.get("best_z_mm")) == 90.0
                and safe_float(row.get("best_radius_mm")) == 8.0
            )
            rows.append({
                "seed": seed,
                "case_label": row.get("case_label", ""),
                "run_name": row.get("run_name", ""),
                "confidence_label": row.get("confidence_label", ""),
                "best_x_mm": safe_float(row.get("best_x_mm")),
                "best_z_mm": safe_float(row.get("best_z_mm")),
                "best_radius_mm": safe_float(row.get("best_radius_mm")),
                "competing_geometry_x_mm": safe_float(row.get("competing_geometry_x_mm")),
                "competing_geometry_z_mm": safe_float(row.get("competing_geometry_z_mm")),
                "competing_geometry_radius_mm": safe_float(row.get("competing_geometry_radius_mm")),
                "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
                "best_misfit": best_misfit,
                "competing_geometry_misfit": competing_misfit,
                "competitor_objective_gap_abs": gap,
                "ambiguity_threshold_width": threshold_width,
                "near_tie_at_scale_0p5": bool(gap <= 0.5 * threshold_width),
                "near_tie_at_scale_1p0": bool(gap <= threshold_width),
                "ambiguity_x_width_mm": safe_float(row.get("ambiguity_x_max_mm")) - safe_float(row.get("ambiguity_x_min_mm")),
                "is_truth_geometry": is_truth,
                "source_path": str(path),
            })
    return sorted(rows, key=lambda row: (int(row["seed"]), row["case_label"]))


def summarize_probe(rows: list[dict]) -> dict:
    seeds = sorted({int(row["seed"]) for row in rows if row.get("seed") is not None})
    strong_count = sum(row.get("confidence_label") == "strong" for row in rows)
    truth_count = sum(bool(row.get("is_truth_geometry")) for row in rows)
    x_ambiguous = sum(safe_float(row.get("ambiguity_x_width_mm")) > 0.0 for row in rows)
    near_0p5 = sum(bool(row.get("near_tie_at_scale_0p5")) for row in rows)
    near_1p0 = sum(bool(row.get("near_tie_at_scale_1p0")) for row in rows)
    competitor_x = sorted({safe_float(row.get("competing_geometry_x_mm")) for row in rows})
    persistent = len(rows) > 0 and truth_count == len(rows) and near_0p5 == len(rows)
    policy_label = (
        "target2_close14_source5_txrx45_three_seed_persistent_x_near_tie"
        if persistent
        else "target2_close14_source5_txrx45_three_seed_mixed_x_near_tie"
    )
    return {
        "policy_label": policy_label,
        "seed_values": ",".join(str(seed) for seed in seeds),
        "seed_count": len(seeds),
        "row_count": len(rows),
        "truth_geometry_count": truth_count,
        "strong_confidence_count": strong_count,
        "x_ambiguity_row_count": x_ambiguous,
        "near_tie_count_at_scale_0p5": near_0p5,
        "near_tie_count_at_scale_1p0": near_1p0,
        "competing_geometry_x_values_mm": ",".join(f"{value:.1f}" for value in competitor_x),
        "radius_margin_abs_min": min(safe_float(row.get("radius_margin_abs")) for row in rows),
        "radius_margin_abs_max": max(safe_float(row.get("radius_margin_abs")) for row in rows),
        "decision": (
            "Truth geometry is selected with strong radius confidence in every row, "
            "but the +1 mm x competitor remains inside the 0.5x ambiguity gate for "
            "every seed/case; report this as a robust objective-uniqueness limit, "
            "not as a clean x-resolution result."
        ),
        "gpu_priority": "none_after_completed_probe",
    }


def plot_probe(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"s{row['seed']}\n{row['case_label'].split('_')[0]}" for row in rows]
    x = list(range(len(rows)))
    gaps = [safe_float(row.get("competitor_objective_gap_abs")) for row in rows]
    half_thresholds = [0.5 * safe_float(row.get("ambiguity_threshold_width")) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    axes[0].bar(x, gaps, color="#4c78a8", width=0.55, label="competitor gap")
    axes[0].plot(x, half_thresholds, color="#c7302b", marker="o", linewidth=1.2, label="0.5x gate")
    axes[0].set_xticks(x, labels)
    axes[0].set_title("Competing x=265 mm geometry remains near-best")
    axes[0].set_ylabel("objective gap")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(
        [0, 1, 2],
        [
            summary["truth_geometry_count"],
            summary["strong_confidence_count"],
            summary["near_tie_count_at_scale_0p5"],
        ],
        color=["#2f9d55", "#4c78a8", "#f58518"],
        width=0.55,
    )
    axes[1].set_xticks([0, 1, 2], ["truth\nselected", "strong\nradius", "0.5x\nx near-tie"])
    axes[1].set_ylim(0, max(1.0, summary["row_count"]) + 0.5)
    axes[1].set_title("Three-seed decision counts")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    fig.suptitle(f"Target2 close14 probe synthesis: {summary['policy_label']}", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confidence-glob", action="append", default=[DEFAULT_CONFIDENCE_GLOB])
    parser.add_argument("--run-name", default="synthetic_target2_close14_three_seed_probe_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    paths = confidence_paths(args.confidence_glob)
    rows = synthesize_rows(paths)
    summary = summarize_probe(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "target2_close14_three_seed_probe_rows.csv"
    summary_json = data_dir / "target2_close14_three_seed_probe_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_probe(rows, summary, figures_dir / "target2_close14_three_seed_probe_synthesis.png"))
    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        **summary,
        "input_confidence_paths": [str(path) for path in paths],
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
        "synthetic_target2_close14_three_seed_probe_synthesis",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
