#!/usr/bin/env python3
"""Build nominal and material/source-aware radius uncertainty reports."""

from __future__ import annotations

import argparse
import csv
import json
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
from run_single_rebar_source_profiled_polish import format_metric, format_mm_value  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def load_json(path):
    """Load JSON from a path."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _weak_interval(summary, key="radius_ambiguity"):
    ambiguity = summary.get(key) or {}
    return ambiguity.get("weak_interval") or {}


def interval_width(interval):
    """Return interval width in millimeters, or NaN when unavailable."""
    lower = float(interval.get("radius_min_mm", np.nan))
    upper = float(interval.get("radius_max_mm", np.nan))
    if not np.isfinite(lower) or not np.isfinite(upper):
        return np.nan
    return max(0.0, upper - lower)


def _truth_radius(summary):
    truth = summary.get("truth") or summary.get("truth_params") or {}
    return float(truth.get("radius_mm", np.nan))


def summarize_nominal(summary):
    """Extract nominal high-band radius fields from source-profiled or two-stage summaries."""
    if "final_best" in summary or "final_margin" in summary:
        margin = summary.get("final_margin") or summary.get("fine_margin") or {}
        ambiguity = summary.get("final_radius_ambiguity") or summary.get("fine_radius_ambiguity") or {}
        best = summary.get("final_best") or summary.get("fine_best") or {}
        params = best.get("params", {})
        source = best.get("source_profile", {})
        stage = summary.get("final_stage", "fine_polish")
    else:
        margin = summary.get("margin") or {}
        ambiguity = summary.get("radius_ambiguity") or {}
        top = (summary.get("top_candidates") or [{}])[0]
        params = top.get("params", {})
        source = top.get("source_profile", {})
        stage = "source_profiled_polish"

    weak = ambiguity.get("weak_interval") or {}
    best_radius = margin.get("best_radius_mm", params.get("radius_mm", np.nan))
    return {
        "stage": stage,
        "truth_radius_mm": _truth_radius(summary),
        "best_radius_mm": float(best_radius),
        "margin_abs": float(margin.get("radius_margin_abs", 0.0)),
        "margin_rel": float(margin.get("radius_margin_rel", 0.0)),
        "weak_min_mm": float(weak.get("radius_min_mm", np.nan)),
        "weak_max_mm": float(weak.get("radius_max_mm", np.nan)),
        "weak_count": int(weak.get("radius_count", 0)),
        "weak_width_mm": interval_width(weak),
        "source_frequency_scale": float(source.get("frequency_scale", np.nan)),
        "source_time_shift_ps": float(source.get("time_shift_ps", np.nan)),
        "source_amplitude_scale": float(source.get("amplitude_scale", np.nan)),
    }


def summarize_material(summary):
    """Extract material/source-aware radius fields from a material tradeoff summary."""
    margin = summary.get("margin") or {}
    weak = _weak_interval(summary)
    top = (summary.get("top_candidates") or [{}])[0]
    params = top.get("params", {})
    material = top.get("material", {})
    source = top.get("source_profile", {})
    best_radius = margin.get("best_radius_mm", params.get("radius_mm", np.nan))
    return {
        "best_radius_mm": float(best_radius),
        "margin_abs": float(margin.get("radius_margin_abs", 0.0)),
        "margin_rel": float(margin.get("radius_margin_rel", 0.0)),
        "weak_min_mm": float(weak.get("radius_min_mm", np.nan)),
        "weak_max_mm": float(weak.get("radius_max_mm", np.nan)),
        "weak_count": int(weak.get("radius_count", 0)),
        "weak_width_mm": interval_width(weak),
        "concrete_epsr": float(material.get("concrete_epsr", np.nan)),
        "rebar_log10_sigma": float(material.get("rebar_log10_sigma", np.nan)),
        "source_frequency_scale": float(source.get("frequency_scale", np.nan)),
        "source_time_shift_ps": float(source.get("time_shift_ps", np.nan)),
        "source_amplitude_scale": float(source.get("amplitude_scale", np.nan)),
    }


def summarize_case(label, nominal_summary, material_summary):
    """Return one flat report row for a case."""
    nominal = summarize_nominal(nominal_summary)
    material = summarize_material(material_summary)
    truth_radius = nominal["truth_radius_mm"]
    return {
        "case": label,
        "truth_radius_mm": truth_radius,
        "nominal_stage": nominal["stage"],
        "nominal_best_radius_mm": nominal["best_radius_mm"],
        "nominal_radius_error_mm": nominal["best_radius_mm"] - truth_radius,
        "nominal_margin_abs": nominal["margin_abs"],
        "nominal_weak_min_mm": nominal["weak_min_mm"],
        "nominal_weak_max_mm": nominal["weak_max_mm"],
        "nominal_weak_width_mm": nominal["weak_width_mm"],
        "material_best_radius_mm": material["best_radius_mm"],
        "material_radius_error_mm": material["best_radius_mm"] - truth_radius,
        "material_margin_abs": material["margin_abs"],
        "material_weak_min_mm": material["weak_min_mm"],
        "material_weak_max_mm": material["weak_max_mm"],
        "material_weak_width_mm": material["weak_width_mm"],
        "material_minus_nominal_best_mm": material["best_radius_mm"] - nominal["best_radius_mm"],
        "material_interval_extra_width_mm": material["weak_width_mm"] - nominal["weak_width_mm"],
        "material_best_concrete_epsr": material["concrete_epsr"],
        "material_best_rebar_log10_sigma": material["rebar_log10_sigma"],
        "material_best_source_frequency_scale": material["source_frequency_scale"],
        "material_best_source_time_shift_ps": material["source_time_shift_ps"],
        "material_best_source_amplitude_scale": material["source_amplitude_scale"],
    }


def write_rows_csv(path, rows):
    """Write report rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _plot_interval(ax, y, lower, upper, point, color, label):
    if np.isfinite(lower) and np.isfinite(upper):
        ax.hlines(y, lower, upper, color=color, linewidth=5, alpha=0.75, label=label)
    if np.isfinite(point):
        ax.scatter([point], [y], s=58, color=color, edgecolor="black", linewidth=0.6, zorder=4)


def plot_report(rows, save_path):
    """Plot nominal and material/source-aware radius intervals."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), constrained_layout=True)
    y_positions = np.arange(len(rows), dtype=np.float64)
    used_labels = set()
    for index, row in enumerate(rows):
        y = y_positions[index]
        truth = row["truth_radius_mm"]
        ax.axvline(truth, color="#333333", linestyle="--", linewidth=0.9, alpha=0.6)
        nominal_label = "nominal interval" if "nominal interval" not in used_labels else None
        material_label = (
            "material/source-aware interval"
            if "material/source-aware interval" not in used_labels else None
        )
        _plot_interval(
            ax,
            y + 0.12,
            row["nominal_weak_min_mm"],
            row["nominal_weak_max_mm"],
            row["nominal_best_radius_mm"],
            "#4C78A8",
            nominal_label,
        )
        _plot_interval(
            ax,
            y - 0.12,
            row["material_weak_min_mm"],
            row["material_weak_max_mm"],
            row["material_best_radius_mm"],
            "#E45756",
            material_label,
        )
        used_labels.update(label for label in (nominal_label, material_label) if label)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([row["case"] for row in rows])
    ax.set_xlabel("Radius [mm]")
    ax.set_title("Nominal vs Material/Source-Aware Radius Intervals")
    ax.grid(axis="x", alpha=0.25)
    ax.legend(loc="best", fontsize=8, frameon=True)
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, rows):
    """Write plain-language notes for the uncertainty report."""
    lines = [
        "# Figure Notes",
        "",
        "## 1. `radius_uncertainty_report.png` - radius interval comparison",
        "",
        "This figure compares the nominal high-band radius interval with the",
        "material/source-aware interval. Nominal means only the selected source",
        "profile is fitted while material values stay fixed. Material/source-aware",
        "means the report also profiles over the tested concrete permittivity and",
        "effective rebar conductivity values.",
        "",
        "Dashed vertical lines mark the known synthetic truth radius for each case.",
        "Blue markers and bars are nominal results; red markers and bars include",
        "the material/source diagnostic. Wider red bars mean the material/source",
        "nuisance parameters can mimic radius changes and should be reported as",
        "part of the size uncertainty.",
        "",
        "Main results:",
    ]
    for row in rows:
        lines.append(
            "- "
            f"{row['case']}: nominal r={format_mm_value(row['nominal_best_radius_mm'])} mm "
            f"with interval {format_mm_value(row['nominal_weak_min_mm'])}-"
            f"{format_mm_value(row['nominal_weak_max_mm'])} mm; "
            f"material/source-aware r={format_mm_value(row['material_best_radius_mm'])} mm "
            f"with interval {format_mm_value(row['material_weak_min_mm'])}-"
            f"{format_mm_value(row['material_weak_max_mm'])} mm."
        )
    lines.extend([
        "",
        "Use this report before claiming a single radius value. If the red interval",
        "is wider than the blue interval, the final result should include the",
        "material/source-aware interval or explain why those nuisance parameters",
        "were independently calibrated.",
    ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        nargs=3,
        metavar=("LABEL", "NOMINAL_SUMMARY", "MATERIAL_SUMMARY"),
        required=True,
        help="Case label followed by nominal summary JSON and material-tradeoff summary JSON.",
    )
    parser.add_argument("--run-name", default="radius_uncertainty_report")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    rows = []
    case_inputs = []
    for label, nominal_path, material_path in args.case:
        nominal_summary = load_json(nominal_path)
        material_summary = load_json(material_path)
        rows.append(summarize_case(label, nominal_summary, material_summary))
        case_inputs.append({
            "label": label,
            "nominal_summary": nominal_path,
            "material_summary": material_path,
        })

    csv_path = data_dir / "radius_uncertainty_report.csv"
    json_path = data_dir / "radius_uncertainty_report.json"
    plot_path = figures_dir / "radius_uncertainty_report.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_rows_csv(csv_path, rows)
    plot_report(rows, plot_path)
    write_figure_notes(notes_path, rows)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({"case_inputs": case_inputs, "rows": rows}, handle, indent=2)

    write_run_manifest(
        str(outdir),
        "radius_uncertainty_report",
        {
            "csv": str(csv_path),
            "json": str(json_path),
            "plot": str(plot_path),
            "figure_notes": str(notes_path),
        },
    )
    for row in rows:
        print(
            f"{row['case']}: nominal={row['nominal_best_radius_mm']} mm, "
            f"material={row['material_best_radius_mm']} mm, "
            f"material interval={row['material_weak_min_mm']}-{row['material_weak_max_mm']} mm"
        )


if __name__ == "__main__":
    main()
