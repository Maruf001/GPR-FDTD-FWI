#!/usr/bin/env python3
"""Compare fitted-ringdown all-target summary packages across seeds."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
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
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PACKAGES = [
    "seed21=outputs/experiments/743_seed21_fitted_ringdown_all_target_summary/data/seed21_fitted_ringdown_summary.json",
    "seed89=outputs/experiments/747_seed89_fitted_ringdown_all_target_summary/data/seed89_fitted_ringdown_summary.json",
]


def parse_package_arg(value: str) -> tuple[str, Path]:
    """Parse a labelled summary-package argument."""
    if "=" not in value:
        raise ValueError(f"expected LABEL=PATH package argument, got {value!r}")
    label, path = value.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError("package label must not be empty")
    return label, Path(path)


def load_package(label: str, path: Path) -> dict:
    """Load one labelled all-target summary package JSON."""
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    summary = payload["summary"]
    return {
        "label": label,
        "path": str(path),
        "summary": summary,
        "target_rows": summary["target_rows"],
    }


def package_target_rows(packages: list[dict]) -> list[dict]:
    """Return one row per seed/target base and best-diagnostic result."""
    rows = []
    for package in packages:
        for row in package["target_rows"]:
            rows.append({
                "seed_label": package["label"],
                "summary_path": package["path"],
                "target_index": int(row["target_index"]),
                "truth_x_mm": float(row["truth_x_mm"]),
                "truth_z_mm": float(row["truth_z_mm"]),
                "truth_radius_mm": float(row["truth_radius_mm"]),
                "base_best_x_mm": float(row["base_best_x_mm"]),
                "base_best_z_mm": float(row["base_best_z_mm"]),
                "base_best_radius_mm": float(row["base_best_radius_mm"]),
                "base_is_truth_geometry": bool(row["base_is_truth_geometry"]),
                "base_confidence_label": row["base_confidence_label"],
                "base_radius_margin_abs": float(row["base_radius_margin_abs"]),
                "base_radius_margin_rel": float(row["base_radius_margin_rel"]),
                "best_truth_preserving_objective": row["best_truth_preserving_objective"],
                "best_truth_preserving_margin_abs": float(row["best_truth_preserving_margin_abs"]),
                "best_truth_preserving_ratio_to_base": float(row["best_truth_preserving_ratio_to_base"]),
            })
    return sorted(rows, key=lambda row: (row["target_index"], row["seed_label"]))


def compare_seed_pair(rows: list[dict], baseline_label: str, comparison_label: str) -> list[dict]:
    """Compare one comparison seed against one baseline seed by target."""
    by_key = {(row["seed_label"], int(row["target_index"])): row for row in rows}
    target_indices = sorted({int(row["target_index"]) for row in rows})
    comparisons = []
    for target_index in target_indices:
        baseline = by_key[(baseline_label, target_index)]
        comparison = by_key[(comparison_label, target_index)]
        baseline_margin = float(baseline["base_radius_margin_abs"])
        comparison_margin = float(comparison["base_radius_margin_abs"])
        ratio = comparison_margin / baseline_margin if baseline_margin else np.nan
        if np.isclose(ratio, 1.0, rtol=1e-9, atol=0.0):
            direction = "same"
        elif ratio > 1.0:
            direction = "stronger"
        else:
            direction = "weaker"
        comparisons.append({
            "target_index": target_index,
            "baseline_seed": baseline_label,
            "comparison_seed": comparison_label,
            "baseline_base_margin_abs": baseline_margin,
            "comparison_base_margin_abs": comparison_margin,
            "comparison_to_baseline_margin_ratio": ratio,
            "comparison_direction": direction,
            "baseline_best_objective": baseline["best_truth_preserving_objective"],
            "comparison_best_objective": comparison["best_truth_preserving_objective"],
            "best_objective_same": (
                baseline["best_truth_preserving_objective"]
                == comparison["best_truth_preserving_objective"]
            ),
            "baseline_best_ratio_to_base": baseline["best_truth_preserving_ratio_to_base"],
            "comparison_best_ratio_to_base": comparison["best_truth_preserving_ratio_to_base"],
            "both_base_truth_geometry": (
                bool(baseline["base_is_truth_geometry"])
                and bool(comparison["base_is_truth_geometry"])
            ),
        })
    return comparisons


def summarize_cross_seed(rows: list[dict], comparisons: list[dict]) -> dict:
    """Summarize cross-seed fitted-ringdown robustness."""
    seed_labels = sorted({row["seed_label"] for row in rows})
    target_indices = sorted({int(row["target_index"]) for row in rows})
    return {
        "seed_count": len(seed_labels),
        "seed_labels": seed_labels,
        "target_count": len(target_indices),
        "base_truth_rows": sum(bool(row["base_is_truth_geometry"]) for row in rows),
        "total_seed_target_rows": len(rows),
        "base_confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in rows)),
        "best_truth_preserving_objective_counts": dict(
            Counter(row["best_truth_preserving_objective"] for row in rows)
        ),
        "comparison_direction_counts": dict(Counter(row["comparison_direction"] for row in comparisons)),
        "best_objective_same_count": sum(bool(row["best_objective_same"]) for row in comparisons),
        "comparison_rows": comparisons,
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write dictionary rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_base_margins(rows: list[dict], save_path: Path) -> None:
    """Plot base margins grouped by target and seed."""
    seeds = sorted({row["seed_label"] for row in rows})
    targets = sorted({int(row["target_index"]) for row in rows})
    width = 0.34
    x_values = np.arange(len(targets))
    fig, ax = plt.subplots(figsize=(8.4, 4.8), constrained_layout=True)
    for offset, seed in enumerate(seeds):
        values = []
        for target in targets:
            match = next(
                row for row in rows
                if row["seed_label"] == seed and int(row["target_index"]) == target
            )
            values.append(float(match["base_radius_margin_abs"]))
        positions = x_values + (offset - (len(seeds) - 1) / 2.0) * width
        ax.bar(positions, values, width=width, label=seed)
    ax.set_xticks(x_values, [f"target {target}" for target in targets])
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_title("Cross-Seed Fitted-Ringdown Base Margins")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_margin_ratios(comparisons: list[dict], save_path: Path) -> None:
    """Plot comparison/baseline base margin ratios by target."""
    targets = [int(row["target_index"]) for row in comparisons]
    ratios = [float(row["comparison_to_baseline_margin_ratio"]) for row in comparisons]
    colors = ["#2E7D32" if ratio >= 1.0 else "#C62828" for ratio in ratios]
    fig, ax = plt.subplots(figsize=(7.8, 4.4), constrained_layout=True)
    ax.bar([f"target {target}" for target in targets], ratios, color=colors, edgecolor="#333333", linewidth=0.5)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1.0)
    ax.set_ylabel("Comparison seed / baseline seed base margin")
    ax.set_title("Seed89 vs Seed21 Base-Margin Ratios")
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path, summary: dict) -> None:
    """Write figure notes for cross-seed summary figures."""
    lines = [
        "# Figure Notes",
        "",
        "## 1. `cross_seed_base_margins_by_target.png` - base margins by seed",
        "",
        "This grouped bar chart compares the base production objective's",
        "best-versus-next-radius gap for each target and seed package.",
        "",
        "## 2. `cross_seed_margin_ratios_by_target.png` - seed89/seed21 margin ratios",
        "",
        "This bar chart divides the seed89 base margin by the seed21 base margin",
        "for each target. Bars below 1.0 identify targets where seed89 has a",
        "smaller base separation margin despite preserving geometry.",
        "",
        "Package summary:",
        f"- seed labels: {summary['seed_labels']}",
        f"- base truth rows: {summary['base_truth_rows']}/{summary['total_seed_target_rows']}",
        f"- comparison directions: {summary['comparison_direction_counts']}",
        f"- unchanged best diagnostic objectives: {summary['best_objective_same_count']}/{summary['target_count']}",
        "",
        "Use these figures to decide whether the fitted-ringdown branch is robust",
        "across the tested seeds and where seed sensitivity remains.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", nargs="*", default=DEFAULT_PACKAGES, help="LABEL=summary_json")
    parser.add_argument("--baseline-label", default="seed21")
    parser.add_argument("--comparison-label", default="seed89")
    parser.add_argument("--run-name", default="cross_seed_fitted_ringdown_summary")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    package_specs = [parse_package_arg(value) for value in args.package]
    packages = [load_package(label, path) for label, path in package_specs]
    target_rows = package_target_rows(packages)
    comparisons = compare_seed_pair(target_rows, args.baseline_label, args.comparison_label)
    summary = summarize_cross_seed(target_rows, comparisons)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    target_csv = data_dir / "cross_seed_target_rows.csv"
    comparison_csv = data_dir / "cross_seed_target_comparison.csv"
    summary_json = data_dir / "cross_seed_fitted_ringdown_summary.json"
    base_fig = figures_dir / "cross_seed_base_margins_by_target.png"
    ratio_fig = figures_dir / "cross_seed_margin_ratios_by_target.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    write_rows_csv(target_csv, target_rows)
    write_rows_csv(comparison_csv, comparisons)
    summary_json.write_text(
        json.dumps({
            "input_packages": [{"label": label, "summary_json": str(path)} for label, path in package_specs],
            "summary": summary,
            "target_rows": target_rows,
            "comparison_rows": comparisons,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    plot_base_margins(target_rows, base_fig)
    plot_margin_ratios(comparisons, ratio_fig)
    write_figure_notes(notes_path, summary)
    write_run_manifest(
        str(outdir),
        args.run_name,
        {
            "summary_json": str(summary_json),
            "target_csv": str(target_csv),
            "comparison_csv": str(comparison_csv),
            "base_margin_figure": str(base_fig),
            "margin_ratio_figure": str(ratio_fig),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote summary: {summary_json}")


if __name__ == "__main__":
    main()
