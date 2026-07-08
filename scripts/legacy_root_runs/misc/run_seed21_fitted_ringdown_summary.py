#!/usr/bin/env python3
"""Summarize all-target fitted-ringdown coordinate diagnostics."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
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
from run_coordinate_objective_diagnostic_report import (  # noqa: E402
    build_ratio_rows,
    enrich_objective_rows,
    float_or_nan,
    objective_confidence_rows,
    summarize_objective_confidence,
    summarize_ratio_rows,
)
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SUMMARIES = [
    "outputs/experiments/740_coordinate_optimizer_variable_depth_radius_seed21_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/742_coordinate_optimizer_variable_depth_radius_seed21_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
    "outputs/experiments/741_coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json",
]


def load_summary(path: str | Path) -> dict:
    """Load one coordinate optimizer summary JSON."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _truth_radius(summary: dict, target_index: int) -> float:
    radii = summary.get("truth_radius_values_mm")
    if radii is not None:
        return float(radii[target_index])
    return float(summary["truth_radius_mm"])


def _is_truth_match(row: dict, truth: dict) -> bool:
    return (
        float(row["best_x_mm"]) == float(truth["x_mm"])
        and float(row["best_z_mm"]) == float(truth["z_mm"])
        and float(row["best_radius_mm"]) == float(truth["radius_mm"])
    )


def base_confidence_rows(summaries: list[dict], summary_paths: list[str]) -> list[dict]:
    """Return one base confidence row per input target summary."""
    rows = []
    for summary, summary_path in zip(summaries, summary_paths):
        for row in summary.get("confidence_rows", []):
            target_index = int(row["step_target_index"])
            truth = {
                "x_mm": float(summary["true_x_values_mm"][target_index]),
                "z_mm": float(summary["true_z_values_mm"][target_index]),
                "radius_mm": _truth_radius(summary, target_index),
            }
            rows.append({
                "summary_path": summary_path,
                "run_name": summary["run_name"],
                "case_label": row["case_label"],
                "target_index": target_index,
                "truth_x_mm": truth["x_mm"],
                "truth_z_mm": truth["z_mm"],
                "truth_radius_mm": truth["radius_mm"],
                "best_x_mm": float(row["best_x_mm"]),
                "best_z_mm": float(row["best_z_mm"]),
                "best_radius_mm": float(row["best_radius_mm"]),
                "next_radius_mm": row.get("next_radius_mm"),
                "radius_margin_abs": float(row["radius_margin_abs"]),
                "radius_margin_rel": float(row["radius_margin_rel"]),
                "confidence_label": row.get("confidence_label"),
                "is_truth_geometry": _is_truth_match(row, truth),
            })
    rows.sort(key=lambda row: row["target_index"])
    return rows


def best_truth_preserving_diagnostics(ratio_rows: list[dict]) -> dict[int, dict]:
    """Return the highest-ratio truth-preserving diagnostic row per target."""
    winners: dict[int, dict] = {}
    for row in ratio_rows:
        if not row.get("variant_is_truth_geometry"):
            continue
        ratio = float_or_nan(row.get("margin_ratio_to_base"))
        if not np.isfinite(ratio):
            continue
        target_index = int(row["target_index"])
        previous = winners.get(target_index)
        if previous is None or ratio > float(previous["margin_ratio_to_base"]):
            winners[target_index] = row
    return winners


def target_summary_rows(base_rows: list[dict], ratio_rows: list[dict]) -> list[dict]:
    """Build compact one-row-per-target summary rows."""
    winners = best_truth_preserving_diagnostics(ratio_rows)
    rows = []
    for base in sorted(base_rows, key=lambda row: row["target_index"]):
        target_index = int(base["target_index"])
        winner = winners.get(target_index)
        rows.append({
            "target_index": target_index,
            "case_label": base["case_label"],
            "base_best_x_mm": base["best_x_mm"],
            "base_best_z_mm": base["best_z_mm"],
            "base_best_radius_mm": base["best_radius_mm"],
            "truth_x_mm": base["truth_x_mm"],
            "truth_z_mm": base["truth_z_mm"],
            "truth_radius_mm": base["truth_radius_mm"],
            "base_is_truth_geometry": bool(base["is_truth_geometry"]),
            "base_confidence_label": base["confidence_label"],
            "base_radius_margin_abs": base["radius_margin_abs"],
            "base_radius_margin_rel": base["radius_margin_rel"],
            "best_truth_preserving_objective": None if winner is None else winner["objective_label"],
            "best_truth_preserving_margin_abs": None if winner is None else winner["variant_margin_abs"],
            "best_truth_preserving_ratio_to_base": None if winner is None else winner["margin_ratio_to_base"],
        })
    return rows


def summarize_seed21_package(target_rows: list[dict], ratio_rows: list[dict], confidence_rows: list[dict]) -> dict:
    """Return a compact package-level summary."""
    return {
        "target_count": len(target_rows),
        "base_truth_count": sum(row["base_is_truth_geometry"] for row in target_rows),
        "base_confidence_label_counts": dict(Counter(row["base_confidence_label"] for row in target_rows)),
        "best_truth_preserving_objective_counts": dict(
            Counter(row["best_truth_preserving_objective"] for row in target_rows)
        ),
        "target_rows": target_rows,
        "ratio_summary": summarize_ratio_rows(ratio_rows),
        "objective_confidence": summarize_objective_confidence(confidence_rows),
    }


def write_rows_csv(path: Path, rows: list[dict]) -> None:
    """Write a list of dictionaries to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def normalize_label(label: str) -> str:
    """Return a filesystem-safe package label."""
    normalized = label.strip()
    if not normalized:
        raise ValueError("label must not be empty")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", normalized):
        raise ValueError(f"label contains unsupported characters: {label!r}")
    return normalized


def _display_label(label: str) -> str:
    return label[:1].upper() + label[1:]


def plot_base_margins(target_rows: list[dict], save_path: Path, label: str = "seed21") -> None:
    """Plot base-objective confidence margins by target."""
    labels = [f"target {row['target_index']}" for row in target_rows]
    values = [float(row["base_radius_margin_abs"]) for row in target_rows]
    colors = ["#2E7D32" if row["base_is_truth_geometry"] else "#C62828" for row in target_rows]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
    ax.bar(labels, values, color=colors, edgecolor="#333333", linewidth=0.5)
    ax.set_title(f"{_display_label(label)} Fitted-Ringdown Base Margins")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def plot_objective_ratios(ratio_rows: list[dict], save_path: Path, label: str = "seed21") -> None:
    """Plot diagnostic/base margin ratios grouped by target."""
    objectives = sorted({row["objective_label"] for row in ratio_rows})
    targets = sorted({int(row["target_index"]) for row in ratio_rows})
    width = 0.13
    x_values = np.arange(len(targets))
    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    for offset, objective in enumerate(objectives):
        values = []
        for target in targets:
            matches = [
                row for row in ratio_rows
                if int(row["target_index"]) == target and row["objective_label"] == objective
            ]
            values.append(float_or_nan(matches[0]["margin_ratio_to_base"]) if matches else np.nan)
        positions = x_values + (offset - (len(objectives) - 1) / 2.0) * width
        ax.bar(positions, np.nan_to_num(values, nan=0.0), width=width, label=objective)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1.0)
    ax.set_xticks(x_values, [f"target {target}" for target in targets])
    ax.set_ylabel("Diagnostic margin / base margin")
    ax.set_title(f"{_display_label(label)} Objective Diagnostic Ratios")
    ax.legend(fontsize=8, ncols=3)
    ax.grid(axis="y", alpha=0.25)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_figure_notes(path: Path, summary: dict, label: str = "seed21") -> None:
    """Write figure notes for a labelled fitted-ringdown summary."""
    display_label = _display_label(label)
    lines = [
        "# Figure Notes",
        "",
        f"## 1. `{label}_base_margins_by_target.png` - base-objective target margins",
        "",
        "This bar chart shows the base production objective's best-versus-next-radius",
        f"gap for each target under the {label} source-mismatch/ringdown stress.",
        "All three bars are truth-geometry rows in this run package.",
        "",
        f"## 2. `{label}_objective_ratios_by_target.png` - diagnostic objective ratios",
        "",
        "This grouped chart compares each diagnostic objective to the base objective",
        "for the same target. A ratio above 1.0 means the diagnostic increased the",
        "radius separation margin while preserving the same target context.",
        "",
        "Package summary:",
        f"- base truth rows: {summary['base_truth_count']}/{summary['target_count']}",
        f"- base confidence labels: {summary['base_confidence_label_counts']}",
        f"- strongest truth-preserving objectives: {summary['best_truth_preserving_objective_counts']}",
        "",
        f"Use these figures as a compact decision aid for the {display_label} robustness",
        "extension. They do not change the production objective rule by themselves.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summary_json", nargs="*", default=DEFAULT_SUMMARIES)
    parser.add_argument("--run-name", default="seed21_fitted_ringdown_all_target_summary")
    parser.add_argument("--label", default="seed21", help="Short package label used in filenames and figure titles.")
    parser.add_argument("--outdir", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    label = normalize_label(args.label)
    summary_paths = [str(Path(path)) for path in args.summary_json]
    summaries = [load_summary(path) for path in summary_paths]
    objective_rows = []
    confidence_rows = []
    for summary, path in zip(summaries, summary_paths):
        objective_rows.extend(enrich_objective_rows(summary, path))
        confidence_rows.extend(objective_confidence_rows(summary, path))
    ratio_rows = build_ratio_rows(objective_rows)
    base_rows = base_confidence_rows(summaries, summary_paths)
    target_rows = target_summary_rows(base_rows, ratio_rows)
    package_summary = summarize_seed21_package(target_rows, ratio_rows, confidence_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    target_csv = data_dir / f"{label}_target_summary.csv"
    ratio_csv = data_dir / f"{label}_objective_ratios.csv"
    confidence_csv = data_dir / f"{label}_objective_confidence_rows.csv"
    summary_json = data_dir / f"{label}_fitted_ringdown_summary.json"
    base_fig = figures_dir / f"{label}_base_margins_by_target.png"
    ratio_fig = figures_dir / f"{label}_objective_ratios_by_target.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    write_rows_csv(target_csv, target_rows)
    write_rows_csv(ratio_csv, ratio_rows)
    write_rows_csv(confidence_csv, confidence_rows)
    summary_json.write_text(
        json.dumps({
            "input_summary_json": summary_paths,
            "summary": package_summary,
            "target_rows": target_rows,
            "ratio_rows": ratio_rows,
            "objective_confidence_rows": confidence_rows,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    plot_base_margins(target_rows, base_fig, label)
    plot_objective_ratios(ratio_rows, ratio_fig, label)
    write_figure_notes(notes_path, package_summary, label)
    write_run_manifest(
        str(outdir),
        args.run_name,
        {
            "summary_json": str(summary_json),
            "target_csv": str(target_csv),
            "ratio_csv": str(ratio_csv),
            "objective_confidence_csv": str(confidence_csv),
            "base_margin_figure": str(base_fig),
            "objective_ratio_figure": str(ratio_fig),
            "figure_notes": str(notes_path),
        },
    )
    print(json.dumps(package_summary, indent=2))
    print(f"Wrote summary: {summary_json}")


if __name__ == "__main__":
    main()
