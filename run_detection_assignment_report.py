#!/usr/bin/env python3
"""Assign detector candidates to a physical multi-rebar seed set."""

from __future__ import annotations

import argparse
import csv
import json
import os
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
from inversion.rebar_detection import (  # noqa: E402
    RebarDetectionCandidate,
    assign_rebar_candidates,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


def load_candidates_csv(path):
    """Load detection candidates and preserve their detector rank."""
    rows = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            candidate = RebarDetectionCandidate(
                x_m=float(row["x_mm"]) / 1000.0,
                z_m=float(row["z_mm"]) / 1000.0,
                score=float(row["score"]),
                normalized_score=float(row["normalized_score"]),
                support_fraction=float(row["support_fraction"]),
                time_offset_s=float(row.get("time_offset_ps", 0.0)) * 1e-12,
            )
            rows.append({"rank": int(row["rank"]), "candidate": candidate})
    return rows


def assign_ranked_candidates(rows, count, min_x_separation_mm):
    """Assign ranked candidate rows and return rows sorted left-to-right."""
    candidates = [row["candidate"] for row in rows]
    assigned = assign_rebar_candidates(
        candidates,
        count,
        min_x_separation_mm=min_x_separation_mm,
    )
    rank_by_identity = {id(row["candidate"]): row["rank"] for row in rows}
    return [
        {
            "assigned_order": index,
            "rank": rank_by_identity[id(candidate)],
            **candidate.as_mm(),
        }
        for index, candidate in enumerate(assigned)
    ]


def write_assignment_csv(path, rows):
    """Write assigned candidate rows."""
    fieldnames = [
        "assigned_order",
        "rank",
        "x_mm",
        "z_mm",
        "score",
        "normalized_score",
        "support_fraction",
        "time_offset_ps",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_assignment(rows, assigned_rows, save_path):
    """Plot all detector candidates and selected assignment seeds."""
    fig, ax = plt.subplots(figsize=(8.4, 5.8), constrained_layout=True)
    all_x = [row["candidate"].x_m * 1000.0 for row in rows]
    all_z = [row["candidate"].z_m * 1000.0 for row in rows]
    all_score = [row["candidate"].normalized_score for row in rows]
    image = ax.scatter(
        all_x,
        all_z,
        c=all_score,
        cmap="viridis",
        s=58,
        edgecolor="#303030",
        linewidth=0.5,
        label="detector candidates",
    )
    for row in assigned_rows:
        ax.scatter(
            [row["x_mm"]],
            [row["z_mm"]],
            s=150,
            marker="*",
            color="#C62828",
            edgecolor="white",
            linewidth=0.9,
            zorder=4,
        )
        ax.text(
            row["x_mm"] + 3.0,
            row["z_mm"],
            f"rank {row['rank']}",
            fontsize=8,
            va="center",
        )
    ax.set_title("Detector Candidate Assignment")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("z [mm]")
    ax.invert_yaxis()
    ax.grid(True, alpha=0.25)
    fig.colorbar(image, ax=ax, label="Normalized detector score")
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, assigned_rows, min_x_separation_mm):
    """Write plain-language notes for the assignment plot."""
    seed_text = ", ".join(
        f"rank {row['rank']} at x={row['x_mm']:.1f} mm, z={row['z_mm']:.1f} mm"
        for row in assigned_rows
    )
    lines = [
        "# Figure Notes",
        "",
        "## 1. `detector_assignment.png` - selected FWI seed candidates",
        "",
        "This figure shows every detector candidate as a colored point. Color is",
        "the normalized detector score. Red stars are the assigned candidates",
        "that will be used as the physical multi-rebar seed set for coordinate",
        "FWI.",
        "",
        f"The assignment requires at least {min_x_separation_mm:.1f} mm of x",
        "separation between selected seeds. That rejects duplicate hyperbola",
        "picks at nearly the same x location, even if both have high detector",
        "scores.",
        "",
        f"Selected seeds: {seed_text}.",
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates_csv")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--min-x-separation-mm", type=float, default=45.0)
    parser.add_argument("--run-name", default="detection_assignment_report")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    rows = load_candidates_csv(args.candidates_csv)
    assigned_rows = assign_ranked_candidates(
        rows,
        args.count,
        args.min_x_separation_mm,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "detection_assignment.csv"
    json_path = data_dir / "detection_assignment_summary.json"
    plot_path = figures_dir / "detector_assignment.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_assignment_csv(csv_path, assigned_rows)
    plot_assignment(rows, assigned_rows, plot_path)
    write_figure_notes(notes_path, assigned_rows, args.min_x_separation_mm)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "input_candidates_csv": args.candidates_csv,
            "count": args.count,
            "min_x_separation_mm": args.min_x_separation_mm,
            "assigned_rows": assigned_rows,
        }, handle, indent=2)

    write_run_manifest(
        str(outdir),
        "detection_assignment_report",
        {
            "input_candidates_csv": args.candidates_csv,
            "csv": str(csv_path),
            "json": str(json_path),
            "plot": str(plot_path),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps({"assigned_rows": assigned_rows}, indent=2))
    print(f"Wrote assignment: {csv_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
