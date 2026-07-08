#!/usr/bin/env python3
"""Synthesize close50 sub-30 mm linear receiver bracket evidence."""

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
from run_close50_linear_receiver_policy import (  # noqa: E402
    STRONG_MARGIN_THRESHOLD,
    confidence_detail_rows,
    figure_stats,
    objective_detail_rows,
    read_json,
    safe_float,
    summarize_run,
    write_csv_rows,
)
from run_gssi_field_preprocess_feature_qc import json_safe  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SUMMARY_PATHS = [
    (
        "outputs/experiments/1271_coordinate_optimizer_close50_seed21_sources4_"
        "txrx29p5_linear_receiver_objectives/data/"
        "multi_rebar_coordinate_optimizer_summary.json"
    ),
    (
        "outputs/experiments/1272_coordinate_optimizer_close50_seed13_sources4_"
        "txrx29p5_linear_receiver_objectives/data/"
        "multi_rebar_coordinate_optimizer_summary.json"
    ),
    (
        "outputs/experiments/1274_coordinate_optimizer_close50_seed13_sources4_"
        "txrx29p75_linear_receiver_objectives/data/"
        "multi_rebar_coordinate_optimizer_summary.json"
    ),
]


def _format_offsets(values) -> str:
    finite = sorted({safe_float(value) for value in values if math.isfinite(safe_float(value))})
    return ",".join(f"{value:g}" for value in finite)


def summarize_bracket_policy(run_rows: list[dict], confidence_rows: list[dict], diagnostic_rows: list[dict]) -> dict:
    sub30_rows = [row for row in confidence_rows if safe_float(row.get("tx_rx_offset_mm")) < 30.0]
    truth_count = sum(1 for row in sub30_rows if row["truth_geometry_match"])
    strong_count = sum(1 for row in sub30_rows if row["strong_confidence"])
    strict_clean_count = sum(1 for row in sub30_rows if row["strict_clean_row"])
    x_ambiguity_count = sum(1 for row in sub30_rows if row["x_ambiguity_width_mm"] > 0.0)
    radius_ambiguity_count = sum(1 for row in sub30_rows if row["radius_ambiguity_width_mm"] > 0.0)
    margins = [row["radius_margin_abs"] for row in sub30_rows if math.isfinite(row["radius_margin_abs"])]

    seed13_rows = [row for row in sub30_rows if row.get("seed_label") == "seed13"]
    seed13_offsets = sorted({safe_float(row["tx_rx_offset_mm"]) for row in seed13_rows})
    seed13_x_offsets = sorted({
        safe_float(row["tx_rx_offset_mm"])
        for row in seed13_rows
        if row["x_ambiguity_width_mm"] > 0.0
    })
    highband_rows = [row for row in diagnostic_rows if row.get("objective_label") == "highband"]
    highband_truth_count = sum(1 for row in highband_rows if row["truth_geometry_match"])
    all_exact_strong = truth_count == len(sub30_rows) and strong_count == len(sub30_rows)
    if not sub30_rows:
        label = "close50_linear_sub30_missing_evidence"
    elif seed13_offsets and set(seed13_x_offsets) == set(seed13_offsets):
        label = "close50_linear_sub30_seed13_x_ambiguity_persists"
    elif all_exact_strong and x_ambiguity_count == 0 and radius_ambiguity_count == 0:
        label = "close50_linear_sub30_clean_candidate"
    elif all_exact_strong:
        label = "close50_linear_sub30_exact_strong_but_x_ambiguous"
    else:
        label = "close50_linear_sub30_mixed_or_wrong_branch"
    return {
        "policy_label": label,
        "run_count": len(run_rows),
        "sub30_confidence_row_count": len(sub30_rows),
        "truth_geometry_row_count": truth_count,
        "strong_confidence_row_count": strong_count,
        "strict_clean_row_count": strict_clean_count,
        "x_ambiguity_row_count": x_ambiguity_count,
        "radius_ambiguity_row_count": radius_ambiguity_count,
        "tested_offsets_mm": _format_offsets(row.get("tx_rx_offset_mm") for row in sub30_rows),
        "seed13_tested_offsets_mm": _format_offsets(seed13_offsets),
        "seed13_x_ambiguous_offsets_mm": _format_offsets(seed13_x_offsets),
        "radius_margin_abs_min": min(margins) if margins else math.nan,
        "radius_margin_abs_mean": float(np.mean(margins)) if margins else math.nan,
        "radius_margin_abs_max": max(margins) if margins else math.nan,
        "highband_row_count": len(highband_rows),
        "highband_truth_row_count": highband_truth_count,
        "next_action": (
            "Stop sub-30 linear receiver bracketing for clean-threshold claims "
            "under the current objective. Seed13 remains x-ambiguous at both "
            "29.5 and 29.75 mm, even though all tested sub-30 rows are exact "
            "and strong. Keep the nearest-sampled 30 mm replicated threshold as "
            "the paper-safe clean result unless a new objective or acquisition "
            "question is explicitly introduced."
        ),
    }


def plot_bracket_policy(confidence_rows: list[dict], summary: dict, save_path: Path) -> str:
    ordered = sorted(confidence_rows, key=lambda row: (safe_float(row["tx_rx_offset_mm"]), row["seed_label"], row["case_label"]))
    labels = [
        f"{row['seed_label']} {safe_float(row['tx_rx_offset_mm']):g}\\n"
        f"{'src' if str(row['case_label']).startswith('source') else 'nom'}"
        for row in ordered
    ]
    colors = ["#2f9d55" if row["strict_clean_row"] else "#d99a19" for row in ordered]
    offsets = sorted({safe_float(row["tx_rx_offset_mm"]) for row in ordered})
    ambiguous_by_offset = [
        sum(
            1 for row in ordered
            if safe_float(row["tx_rx_offset_mm"]) == offset and row["x_ambiguity_width_mm"] > 0.0
        )
        for offset in offsets
    ]

    fig, axes = plt.subplots(1, 2, figsize=(13.6, 4.8), constrained_layout=True)
    axes[0].bar(labels, [row["radius_margin_abs"] for row in ordered], color=colors)
    axes[0].axhline(STRONG_MARGIN_THRESHOLD, color="#444444", linestyle="--", linewidth=1.0)
    axes[0].set_ylabel("radius margin abs")
    axes[0].set_title("Sub-30 linear confidence rows")
    axes[0].tick_params(axis="x", rotation=30, labelsize=8)
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar([f"{offset:g}" for offset in offsets], ambiguous_by_offset, color="#d99a19")
    axes[1].set_xlabel("linear Tx/Rx offset [mm]")
    axes[1].set_ylabel("x-ambiguous confidence rows")
    axes[1].set_title("Seed13 ambiguity persistence")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(summary["policy_label"], fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="*", help="optimizer summary JSON paths")
    parser.add_argument("--run-name", default="close50_linear_sub30_bracket_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    summary_paths = [Path(path) for path in (args.summary_json or DEFAULT_SUMMARY_PATHS)]
    for path in summary_paths:
        if not path.exists():
            raise FileNotFoundError(path)

    confidence_rows: list[dict] = []
    diagnostic_rows: list[dict] = []
    run_rows: list[dict] = []
    for path in summary_paths:
        summary = read_json(path)
        confidence_rows.extend(confidence_detail_rows(summary, path))
        diagnostic_rows.extend(objective_detail_rows(summary, path))
        run_rows.append(summarize_run(summary, path))
    policy_summary = summarize_bracket_policy(run_rows, confidence_rows, diagnostic_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    run_csv = data_dir / "close50_linear_sub30_bracket_run_rows.csv"
    confidence_csv = data_dir / "close50_linear_sub30_bracket_confidence_rows.csv"
    diagnostic_csv = data_dir / "close50_linear_sub30_bracket_objective_diagnostics.csv"
    summary_json = data_dir / "close50_linear_sub30_bracket_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_bracket_policy(confidence_rows, policy_summary, figures_dir / "close50_linear_sub30_bracket_policy.png"))

    write_csv_rows(run_csv, run_rows)
    write_csv_rows(confidence_csv, confidence_rows)
    write_csv_rows(diagnostic_csv, diagnostic_rows)
    write_csv_rows(validation_csv, [figure_stats(figure_path)])
    output_summary = {
        **policy_summary,
        "input_summary_jsons": [str(path) for path in summary_paths],
        "paths": {
            "run_csv": str(run_csv),
            "confidence_csv": str(confidence_csv),
            "diagnostic_csv": str(diagnostic_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close50_linear_sub30_bracket_policy",
        {
            "summary_json": str(summary_json),
            "run_csv": str(run_csv),
            "confidence_csv": str(confidence_csv),
            "diagnostic_csv": str(diagnostic_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
