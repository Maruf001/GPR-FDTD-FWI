#!/usr/bin/env python3
"""Apply the strict location-clean metric across coordinate aggregate outputs."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def boolish(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def is_smoke_path(path: Path) -> bool:
    return "smoke" in str(path).lower()


def aggregate_csv_paths(root: Path, *, include_smoke: bool = False) -> list[Path]:
    paths = sorted(root.glob("*/data/coordinate_confidence_aggregate.csv"))
    if include_smoke:
        return paths
    return [path for path in paths if not is_smoke_path(path)]


def metric_rows_from_aggregates(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        run_dir = path.parents[1]
        for row in read_csv_rows(path):
            x_width = safe_float(row.get("ambiguity_x_width_mm"), 0.0)
            z_width = safe_float(row.get("ambiguity_z_width_mm"), 0.0)
            radius_width = safe_float(row.get("ambiguity_radius_width_mm"), 0.0)
            exact = boolish(row.get("is_truth_geometry"))
            confidence = str(row.get("confidence_label", ""))
            strong = confidence == "strong"
            rows.append({
                "aggregate_run": run_dir.name,
                "source_csv": str(path),
                "run_name": row.get("run_name", ""),
                "case_label": row.get("case_label", ""),
                "target_index": int(safe_float(row.get("step_target_index"), -1)),
                "sources": safe_float(row.get("sources")),
                "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm")),
                "confidence_label": confidence,
                "truth_geometry_match": exact,
                "strong_confidence": strong,
                "x_ambiguity_width_mm": x_width,
                "z_ambiguity_width_mm": z_width,
                "radius_ambiguity_width_mm": radius_width,
                "location_clean": x_width <= 0.0 and z_width <= 0.0,
                "radius_clean": radius_width <= 0.0,
                "strict_location_clean_strong": exact and strong and x_width <= 0.0 and z_width <= 0.0 and radius_width <= 0.0,
                "exact_strong_x_ambiguous": exact and strong and x_width > 0.0,
                "exact_strong_z_ambiguous": exact and strong and z_width > 0.0,
                "exact_strong_radius_ambiguous": exact and strong and radius_width > 0.0,
            })
    return rows


def summarize_archive_metric(rows: list[dict], aggregate_file_count: int, *, include_smoke: bool) -> dict:
    exact = [row for row in rows if row["truth_geometry_match"]]
    exact_strong = [row for row in rows if row["truth_geometry_match"] and row["strong_confidence"]]
    location_clean = [row for row in exact_strong if row["strict_location_clean_strong"]]
    x_ambiguous = [row for row in exact_strong if row["exact_strong_x_ambiguous"]]
    z_ambiguous = [row for row in exact_strong if row["exact_strong_z_ambiguous"]]
    radius_ambiguous = [row for row in exact_strong if row["exact_strong_radius_ambiguous"]]
    x_values = [row["x_ambiguity_width_mm"] for row in exact_strong if math.isfinite(row["x_ambiguity_width_mm"])]
    if x_ambiguous:
        label = "archive_location_clean_metric_x_ambiguity_present_cpu_no_gpu"
    elif exact_strong:
        label = "archive_location_clean_metric_all_exact_strong_rows_clean"
    else:
        label = "archive_location_clean_metric_insufficient_exact_strong_rows"
    return {
        "policy_label": label,
        "aggregate_file_count": aggregate_file_count,
        "include_smoke": include_smoke,
        "row_count": len(rows),
        "exact_row_count": len(exact),
        "exact_strong_row_count": len(exact_strong),
        "strict_location_clean_strong_count": len(location_clean),
        "exact_strong_x_ambiguous_count": len(x_ambiguous),
        "exact_strong_z_ambiguous_count": len(z_ambiguous),
        "exact_strong_radius_ambiguous_count": len(radius_ambiguous),
        "exact_strong_location_clean_fraction": (
            len(location_clean) / len(exact_strong) if exact_strong else math.nan
        ),
        "max_exact_strong_x_ambiguity_width_mm": max(x_values) if x_values else math.nan,
        "mean_exact_strong_x_ambiguity_width_mm": float(np.mean(x_values)) if x_values else math.nan,
        "gpu_priority": "none_now",
        "decision": (
            "Use the strict location-clean metric as an archive reporting audit. "
            "Rows that are exact and strong but have nonzero x/z/radius ambiguity "
            "should not be presented as strict clean thresholds."
        ),
    }


def plot_archive_metric(rows: list[dict], summary: dict, save_path: Path) -> str:
    exact_strong = [row for row in rows if row["truth_geometry_match"] and row["strong_confidence"]]
    categories = ["strict clean", "x ambig", "z ambig", "r ambig"]
    counts = [
        summary["strict_location_clean_strong_count"],
        summary["exact_strong_x_ambiguous_count"],
        summary["exact_strong_z_ambiguous_count"],
        summary["exact_strong_radius_ambiguous_count"],
    ]
    x_widths = sorted(
        [row["x_ambiguity_width_mm"] for row in exact_strong if row["x_ambiguity_width_mm"] > 0.0],
        reverse=True,
    )[:20]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8), constrained_layout=True)
    axes[0].bar(categories, counts, color=["#2f9d55", "#c7302b", "#f58518", "#7f3c8d"])
    axes[0].set_ylabel("row count")
    axes[0].set_title("Exact strong rows under strict location-clean metric")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(np.arange(len(x_widths)), x_widths, color="#c7302b")
    axes[1].set_xlabel("top x-ambiguous exact-strong rows")
    axes[1].set_ylabel("x ambiguity width [mm]")
    axes[1].set_title("Largest x ambiguity widths")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Archive location-clean metric audit: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--include-smoke", action="store_true")
    parser.add_argument("--run-name", default="archive_location_clean_metric_audit")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    paths = aggregate_csv_paths(Path(args.experiment_root), include_smoke=args.include_smoke)
    rows = metric_rows_from_aggregates(paths)
    summary = summarize_archive_metric(rows, len(paths), include_smoke=args.include_smoke)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.experiment_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "archive_location_clean_metric_rows.csv"
    summary_json = data_dir / "archive_location_clean_metric_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_archive_metric(rows, summary, figures_dir / "archive_location_clean_metric_audit.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
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
        "archive_location_clean_metric_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
