#!/usr/bin/env python3
"""Design a CPU-side reporting metric for close50 sub-30 x-ambiguity."""

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


DEFAULT_CONFIDENCE_CSV = (
    "outputs/experiments/1275_close50_linear_sub30_bracket_policy/data/"
    "close50_linear_sub30_bracket_confidence_rows.csv"
)


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


def metric_rows(confidence_rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for row in confidence_rows:
        x_width = safe_float(row.get("x_ambiguity_width_mm"), 0.0)
        radius_width = safe_float(row.get("radius_ambiguity_width_mm"), 0.0)
        exact = boolish(row.get("truth_geometry_match"))
        strong = boolish(row.get("strong_confidence")) or str(row.get("confidence_label")) == "strong"
        location_clean = x_width <= 0.0
        radius_clean = radius_width <= 0.0
        if exact and strong and location_clean and radius_clean:
            label = "exact_strong_location_clean"
        elif exact and strong and not location_clean and radius_clean:
            label = "exact_strong_x_ambiguous"
        elif exact:
            label = "exact_but_not_strict_clean"
        else:
            label = "wrong_or_mixed_branch"
        out.append({
            "seed_label": row.get("seed_label", ""),
            "case_label": row.get("case_label", ""),
            "tx_rx_offset_mm": safe_float(row.get("tx_rx_offset_mm")),
            "truth_geometry_match": exact,
            "strong_confidence": strong,
            "x_ambiguity_width_mm": x_width,
            "radius_ambiguity_width_mm": radius_width,
            "radius_margin_abs": safe_float(row.get("radius_margin_abs")),
            "location_clean": location_clean,
            "radius_clean": radius_clean,
            "ambiguity_metric_label": label,
            "paper_clean_candidate": label == "exact_strong_location_clean",
        })
    return out


def summarize_metric(rows: list[dict]) -> dict:
    exact_strong = [row for row in rows if row["truth_geometry_match"] and row["strong_confidence"]]
    x_ambiguous = [row for row in exact_strong if row["x_ambiguity_width_mm"] > 0.0]
    radius_ambiguous = [row for row in exact_strong if row["radius_ambiguity_width_mm"] > 0.0]
    paper_clean = [row for row in rows if row["paper_clean_candidate"]]
    nominal_ambiguous = [
        row for row in x_ambiguous
        if not str(row["case_label"]).startswith("source")
    ]
    source_ambiguous = [
        row for row in x_ambiguous
        if str(row["case_label"]).startswith("source")
    ]
    if x_ambiguous and not radius_ambiguous:
        label = "close50_sub30_x_ambiguity_reporting_metric_ready_cpu_no_gpu"
    elif not x_ambiguous and len(paper_clean) == len(rows):
        label = "close50_sub30_location_clean_under_reporting_metric"
    else:
        label = "close50_sub30_reporting_metric_mixed"
    return {
        "policy_label": label,
        "row_count": len(rows),
        "exact_strong_row_count": len(exact_strong),
        "paper_clean_candidate_count": len(paper_clean),
        "x_ambiguous_row_count": len(x_ambiguous),
        "radius_ambiguous_row_count": len(radius_ambiguous),
        "nominal_x_ambiguous_row_count": len(nominal_ambiguous),
        "source_mismatch_x_ambiguous_row_count": len(source_ambiguous),
        "max_x_ambiguity_width_mm": max([row["x_ambiguity_width_mm"] for row in rows], default=math.nan),
        "mean_x_ambiguity_width_mm": float(np.mean([row["x_ambiguity_width_mm"] for row in rows])) if rows else math.nan,
        "recommended_reporting_metric": (
            "paper_clean_candidate = truth_geometry_match and strong_confidence "
            "and x_ambiguity_width_mm == 0 and radius_ambiguity_width_mm == 0"
        ),
        "gpu_priority": "none_now",
        "decision": (
            "Use the strict location-clean reporting metric for sub-30 close50 "
            "linear receiver rows. The current evidence supports reporting an "
            "x-ambiguity caveat, not launching another GPU run."
        ),
    }


def plot_metric(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [
        f"{row['seed_label']}\n{row['tx_rx_offset_mm']:g} mm\n"
        f"{'src' if str(row['case_label']).startswith('source') else 'nom'}"
        for row in rows
    ]
    x = np.arange(len(rows))
    x_width = np.asarray([row["x_ambiguity_width_mm"] for row in rows], dtype=np.float64)
    radius_margin = np.asarray([row["radius_margin_abs"] for row in rows], dtype=np.float64)
    clean = np.asarray([1.0 if row["paper_clean_candidate"] else 0.0 for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 3, figsize=(14.8, 4.8), constrained_layout=True)
    axes[0].bar(x, x_width, color=["#c7302b" if value > 0 else "#2f9d55" for value in x_width])
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("x ambiguity width [mm]")
    axes[0].set_title("Location ambiguity width")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, radius_margin, color="#4c78a8")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("radius margin abs")
    axes[1].set_title("Radius branch remains separated")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(x, clean, color=["#2f9d55" if value > 0 else "#d99a19" for value in clean])
    axes[2].set_xticks(x, labels)
    axes[2].set_ylim(0.0, 1.05)
    axes[2].set_ylabel("paper clean candidate")
    axes[2].set_title("Strict location-clean reporting metric")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Close50 sub-30 x-ambiguity metric: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confidence-csv", default=DEFAULT_CONFIDENCE_CSV)
    parser.add_argument("--run-name", default="close50_x_ambiguity_metric_design")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    rows = metric_rows(read_csv_rows(Path(args.confidence_csv)))
    summary = summarize_metric(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "close50_x_ambiguity_metric_rows.csv"
    summary_json = data_dir / "close50_x_ambiguity_metric_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_metric(rows, summary, figures_dir / "close50_x_ambiguity_metric.png"))

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    output_summary = {
        "input_confidence_csv": args.confidence_csv,
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
        "close50_x_ambiguity_metric_design",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
