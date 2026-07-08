#!/usr/bin/env python3
"""Build confidence reports from ranked candidate summary JSON files."""

from __future__ import annotations

import argparse
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.candidate_confidence import (  # noqa: E402
    ConfidenceThresholds,
    load_profile_confidence_rows,
    write_confidence_csv,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


LABEL_COLORS = {
    "strong": "#1b7837",
    "moderate": "#4575b4",
    "weak": "#d73027",
    "ambiguous": "#7f7f7f",
    "missing": "#bdbdbd",
}


def plot_confidence_margins(rows, save_path):
    """Plot absolute radius margins with confidence labels."""
    if not rows:
        raise ValueError("no rows to plot")
    labels = [
        f"{row['run_name']}\n{row['case_label']}"
        for row in rows
    ]
    margins = [
        0.0 if row["radius_margin_abs"] is None else float(row["radius_margin_abs"])
        for row in rows
    ]
    colors = [LABEL_COLORS.get(row["confidence_label"], "#7f7f7f") for row in rows]
    width = max(8.5, 0.9 * len(rows))
    fig, ax = plt.subplots(figsize=(width, 5.2), constrained_layout=True)
    bars = ax.bar(range(len(rows)), margins, color=colors, edgecolor="#333333", linewidth=0.6)
    ax.axhline(ConfidenceThresholds().moderate_abs, color="#555555", linestyle="--", linewidth=1.0)
    ax.axhline(ConfidenceThresholds().strong_abs, color="#111111", linestyle=":", linewidth=1.2)
    ax.set_title("Radius Confidence Margins")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.grid(True, axis="y", alpha=0.25)
    ymax = max(max(margins) * 1.28, ConfidenceThresholds().strong_abs * 1.15)
    ax.set_ylim(0.0, ymax)
    for bar, row in zip(bars, rows):
        rel = row["radius_margin_rel"]
        rel_text = "n/a" if rel is None else f"{100.0 * float(rel):.2f}%"
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + ymax * 0.025,
            f"{row['confidence_label']}\nrel {rel_text}",
            ha="center",
            va="bottom",
            fontsize=7,
        )
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="+", help="profile-style summary JSON paths")
    parser.add_argument("--run-name", default="multi_rebar_confidence_report")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    thresholds = ConfidenceThresholds()
    rows = []
    for summary_path in args.summary_json:
        rows.extend(load_profile_confidence_rows(summary_path, thresholds))

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, "candidate_confidence_report.csv")
    json_path = os.path.join(data_dir, "candidate_confidence_report.json")
    plot_path = os.path.join(figures_dir, "candidate_confidence_margins.png")
    write_confidence_csv(rows, csv_path)
    plot_confidence_margins(rows, plot_path)

    report = {
        "run_name": args.run_name,
        "input_summary_json": args.summary_json,
        "thresholds": thresholds.as_dict(),
        "rows": rows,
        "paths": {
            "csv": csv_path,
            "json": json_path,
            "plot": plot_path,
        },
    }
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)

    write_run_manifest(
        outdir,
        "candidate_confidence_report",
        {
            "csv": csv_path,
            "json": json_path,
            "plot": plot_path,
        },
    )
    for row in rows:
        print(
            f"{row['run_name']} / {row['case_label']}: "
            f"r={row['best_radius_mm']} mm, next={row['next_radius_mm']} mm, "
            f"margin={row['radius_margin_abs']}, rel={row['radius_margin_rel']}, "
            f"confidence={row['confidence_label']}"
        )
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote JSON: {json_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
