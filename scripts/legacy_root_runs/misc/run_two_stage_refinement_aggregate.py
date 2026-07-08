#!/usr/bin/env python3
"""Aggregate packaged two-stage single-rebar refinement runs."""

from __future__ import annotations

import argparse
import csv
import json
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
import numpy as np  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.radius_confidence import radius_interval_from_curve  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


SUMMARY_RELATIVE_PATH = Path("data") / "two_stage_refinement_summary.json"


def run_id_from_path(path):
    """Return the leading numbered experiment id when present."""
    name = Path(path).name
    match = re.match(r"^(\d{3,})_", name)
    return match.group(1) if match else name


def confidence_label(margin_abs, margin_rel):
    """Classify final radius-margin confidence for quick triage."""
    margin_abs = float(margin_abs or 0.0)
    margin_rel = float(margin_rel or 0.0)
    if margin_abs >= 1.0e-3 or margin_rel >= 1.0e-2:
        return "strong"
    if margin_abs < 1.0e-3 and margin_rel < 5.0e-3:
        return "weak"
    return "moderate"


def radius_ambiguity_from_summary(summary):
    """Return radius ambiguity metadata, computing it from child summaries if needed."""
    final_ambiguity = summary.get("final_radius_ambiguity")
    if final_ambiguity:
        return final_ambiguity

    ambiguity = summary.get("fine_radius_ambiguity")
    if ambiguity:
        return ambiguity

    final_stage = summary.get("final_stage", "fine_polish")
    if final_stage == "highband_polish":
        summary_key = "highband_summary"
    elif final_stage == "guarded_polish":
        summary_key = "guarded_summary"
    else:
        summary_key = "fine_summary"
    fine_summary_path = summary.get("paths", {}).get(summary_key)
    if fine_summary_path and Path(fine_summary_path).exists():
        with Path(fine_summary_path).open("r", encoding="utf-8") as handle:
            fine_summary = json.load(handle)
        ambiguity = fine_summary.get("radius_ambiguity")
        if ambiguity:
            return ambiguity
        curve = fine_summary.get("best_curve_by_radius")
        if curve:
            return {
                "exact_tie": radius_interval_from_curve(curve, abs_tolerance=1e-12),
                "weak_interval": radius_interval_from_curve(
                    curve,
                    abs_tolerance=1e-3,
                    rel_tolerance=5e-3,
                ),
            }
    return None


def material_uncertainty_row_from_summary(summary):
    """Return the first material/source uncertainty report row when available."""
    report_path = summary.get("paths", {}).get("radius_uncertainty_report_summary")
    if not report_path:
        return None
    path = Path(report_path)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        report = json.load(handle)
    rows = report.get("rows") or []
    return rows[0] if rows else None


def _float_or_nan(mapping, key):
    try:
        return float(mapping.get(key, np.nan))
    except (TypeError, ValueError):
        return np.nan


def summarize_two_stage_summary(summary, run_dir):
    """Flatten one two-stage summary into a CSV/JSON row."""
    truth = summary["truth"]
    observed = summary.get("observed_source", {})
    detection = summary.get("selected_detection", {})
    fine_stage_best = summary.get("fine_best", {})
    fine_stage_margin = summary.get("fine_margin", {})
    final_best = summary.get("final_best") or fine_stage_best
    final_margin = summary.get("final_margin") or fine_stage_margin
    final_stage = summary.get("final_stage") or "fine_polish"
    errors = summary.get("truth_errors", {})
    elapsed = summary.get("elapsed_time_s", {})
    fine_stage_params = fine_stage_best.get("params", {})
    final_source = final_best.get("source_profile", {})
    final_params = final_best.get("params", {})
    radius_ambiguity = radius_ambiguity_from_summary(summary) or {}
    exact_interval = radius_ambiguity.get("exact_tie", {})
    weak_interval = radius_ambiguity.get("weak_interval", {})
    fine_stage_margin_abs = float(fine_stage_margin.get("radius_margin_abs", 0.0))
    fine_stage_margin_rel = float(fine_stage_margin.get("radius_margin_rel", 0.0))
    final_margin_abs = float(final_margin.get("radius_margin_abs", 0.0))
    final_margin_rel = float(final_margin.get("radius_margin_rel", 0.0))
    material_row = material_uncertainty_row_from_summary(summary) or {}
    material_enabled = bool(summary.get("material_uncertainty_enabled") or material_row)
    return {
        "run_id": run_id_from_path(run_dir),
        "run_dir": str(run_dir),
        "final_stage": final_stage,
        "truth_x_mm": float(truth["x_mm"]),
        "truth_z_mm": float(truth["z_mm"]),
        "truth_radius_mm": float(truth["radius_mm"]),
        "observed_frequency_scale": float(observed.get("frequency_scale", 1.0)),
        "observed_time_shift_ps": float(observed.get("time_shift_ps", 0.0)),
        "observed_amplitude_scale": float(observed.get("amplitude_scale", 1.0)),
        "noise_rms_fraction": float(observed.get("noise_rms_fraction", 0.0)),
        "noise_seed": int(observed.get("noise_seed", 0)),
        "detection_rank": int(detection.get("rank", 0)),
        "detection_x_mm": float(detection.get("x_mm", np.nan)),
        "detection_z_mm": float(detection.get("z_mm", np.nan)),
        "coarse_candidate_count": int(summary.get("coarse_grid", {}).get("candidate_count", 0)),
        "fine_candidate_count": int(summary.get("fine_grid", {}).get("candidate_count", 0)),
        "fine_x_mm": float(final_params.get("x_mm", np.nan)),
        "fine_z_mm": float(final_params.get("z_mm", np.nan)),
        "fine_radius_mm": float(final_params.get("radius_mm", np.nan)),
        "fine_stage_radius_mm": float(fine_stage_params.get("radius_mm", np.nan)),
        "fine_stage_margin_abs": fine_stage_margin_abs,
        "fine_stage_margin_rel": fine_stage_margin_rel,
        "fine_stage_confidence": confidence_label(fine_stage_margin_abs, fine_stage_margin_rel),
        "final_radius_mm": float(final_params.get("radius_mm", np.nan)),
        "final_margin_abs": final_margin_abs,
        "final_margin_rel": final_margin_rel,
        "final_confidence": confidence_label(final_margin_abs, final_margin_rel),
        "x_error_mm": float(errors.get("x_error_mm", np.nan)),
        "z_error_mm": float(errors.get("z_error_mm", np.nan)),
        "radius_error_mm": float(errors.get("radius_error_mm", np.nan)),
        "fine_margin_abs": final_margin_abs,
        "fine_margin_rel": final_margin_rel,
        "confidence": confidence_label(final_margin_abs, final_margin_rel),
        "exact_radius_min_mm": float(exact_interval.get("radius_min_mm", np.nan)),
        "exact_radius_max_mm": float(exact_interval.get("radius_max_mm", np.nan)),
        "exact_radius_count": int(exact_interval.get("radius_count", 0)),
        "weak_radius_min_mm": float(weak_interval.get("radius_min_mm", np.nan)),
        "weak_radius_max_mm": float(weak_interval.get("radius_max_mm", np.nan)),
        "weak_radius_count": int(weak_interval.get("radius_count", 0)),
        "fine_source_frequency_scale": float(final_source.get("frequency_scale", np.nan)),
        "fine_source_time_shift_ps": float(final_source.get("time_shift_ps", np.nan)),
        "fine_source_amplitude_scale": float(final_source.get("amplitude_scale", np.nan)),
        "material_uncertainty_enabled": material_enabled,
        "material_best_radius_mm": _float_or_nan(material_row, "material_best_radius_mm"),
        "material_radius_error_mm": _float_or_nan(material_row, "material_radius_error_mm"),
        "material_margin_abs": _float_or_nan(material_row, "material_margin_abs"),
        "material_weak_radius_min_mm": _float_or_nan(material_row, "material_weak_min_mm"),
        "material_weak_radius_max_mm": _float_or_nan(material_row, "material_weak_max_mm"),
        "material_weak_interval_width_mm": _float_or_nan(material_row, "material_weak_width_mm"),
        "material_minus_nominal_best_mm": _float_or_nan(
            material_row,
            "material_minus_nominal_best_mm",
        ),
        "material_best_concrete_epsr": _float_or_nan(material_row, "material_best_concrete_epsr"),
        "material_best_rebar_log10_sigma": _float_or_nan(
            material_row,
            "material_best_rebar_log10_sigma",
        ),
        "overall_wall_s": float(elapsed.get("overall_wall", 0.0)),
    }


def find_summary_paths(root, run_dirs):
    """Find two-stage summary files from explicit dirs or by scanning root."""
    if run_dirs:
        return [Path(run_dir) / SUMMARY_RELATIVE_PATH for run_dir in run_dirs]

    root_path = Path(root)
    return sorted(root_path.glob(f"[0-9][0-9][0-9]*/{SUMMARY_RELATIVE_PATH}"))


def write_rows_csv(path, rows):
    """Write aggregate rows to CSV."""
    if not rows:
        raise ValueError("no rows to write")
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def symmetric_error_limits(values, floor=0.05):
    """Return useful symmetric y-limits for error plots, including all-zero data."""
    data = np.asarray(values, dtype=np.float64)
    finite = np.abs(data[np.isfinite(data)])
    max_value = float(finite.max()) if finite.size else 0.0
    limit = max(float(floor), 1.25 * max_value)
    return -limit, limit


def interval_width(row, prefix):
    """Return a non-negative radius interval width for an aggregate row."""
    lower = float(row.get(f"{prefix}_radius_min_mm", np.nan))
    upper = float(row.get(f"{prefix}_radius_max_mm", np.nan))
    if not np.isfinite(lower) or not np.isfinite(upper):
        return np.nan
    return max(0.0, upper - lower)


def positive_axis_limit(values, floor=0.1):
    """Return a positive y-limit that keeps all-zero bar data visible."""
    data = np.asarray(values, dtype=np.float64)
    finite = data[np.isfinite(data)]
    max_value = float(finite.max()) if finite.size else 0.0
    return max(float(floor), 1.25 * max_value)


def finite_value_notice(values, all_zero_text, missing_text):
    """Return a plot annotation when finite values are all zero or missing."""
    data = np.asarray(values, dtype=np.float64)
    finite = data[np.isfinite(data)]
    missing_count = int(data.size - finite.size)
    if finite.size == 0:
        return f"{missing_text}: no finite values available"
    message = None
    if np.allclose(finite, 0.0, rtol=0.0, atol=1e-12):
        message = all_zero_text
    if missing_count:
        suffix = f"{missing_count} run(s) missing finite values"
        message = f"{message}; {suffix}" if message else f"{missing_text}: {suffix}"
    return message


def add_panel_notice(ax, text):
    """Add a small explanatory note inside a plot panel."""
    if not text:
        return
    ax.text(
        0.01,
        0.90,
        text,
        transform=ax.transAxes,
        fontsize=9,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#B0B0B0"},
    )


def plot_margin_summary(rows, save_path):
    """Plot point-error and margin summary for packaged two-stage runs."""
    labels = [row["run_id"] for row in rows]
    margin_abs = np.asarray([row["fine_margin_abs"] for row in rows], dtype=np.float64)
    radius_error = np.asarray([row["radius_error_mm"] for row in rows], dtype=np.float64)
    colors = [
        "#2E7D32" if row["confidence"] == "strong"
        else "#F9A825" if row["confidence"] == "moderate"
        else "#C62828"
        for row in rows
    ]

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 7.2), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, radius_error, color="#A8B2BA", edgecolor="#546A7B", linewidth=0.8)
    axes[0].scatter(
        x,
        radius_error,
        s=54,
        color="#1B3A4B",
        edgecolor="white",
        linewidth=0.8,
        zorder=4,
        label="final radius error",
    )
    axes[0].axhline(0.0, color="black", linewidth=0.9)
    axes[0].set_ylim(*symmetric_error_limits(radius_error))
    add_panel_notice(
        axes[0],
        finite_value_notice(
            radius_error,
            "All finite runs have 0.000 mm final radius error",
            "Final radius error",
        ),
    )
    axes[0].set_ylabel("Radius error [mm]")
    axes[0].set_title("Two-Stage Final Radius Error")
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar(x, margin_abs, color=colors)
    axes[1].axhline(1.0e-3, color="black", linestyle="--", linewidth=1.0, label="strong abs threshold")
    axes[1].set_ylabel("Fine radius margin")
    axes[1].set_title("Final Radius-Margin Confidence")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].legend(loc="upper right", fontsize=8, frameon=True)

    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha="right")
        ax.set_xlabel("Experiment")

    return save_validated_figure(fig, save_path)


def plot_interval_runtime_summary(rows, save_path):
    """Plot ambiguity interval widths and runtime for packaged two-stage runs."""
    labels = [row["run_id"] for row in rows]
    exact_width = np.asarray([interval_width(row, "exact") for row in rows], dtype=np.float64)
    weak_width = np.asarray([interval_width(row, "weak") for row in rows], dtype=np.float64)
    runtime_min = np.asarray([row["overall_wall_s"] / 60.0 for row in rows], dtype=np.float64)
    colors = [
        "#2E7D32" if row["confidence"] == "strong"
        else "#F9A825" if row["confidence"] == "moderate"
        else "#C62828"
        for row in rows
    ]

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 7.2), constrained_layout=True)
    x = np.arange(len(rows))
    width = 0.36

    axes[0].bar(
        x - width / 2,
        exact_width,
        width=width,
        color="#4C78A8",
        alpha=0.85,
        label="exact tie width",
    )
    axes[0].bar(
        x + width / 2,
        weak_width,
        width=width,
        color="#E45756",
        alpha=0.85,
        label="weak interval width",
    )
    axes[0].scatter(
        x - width / 2,
        exact_width,
        s=34,
        color="#17324D",
        edgecolor="white",
        linewidth=0.6,
        zorder=4,
    )
    axes[0].scatter(
        x + width / 2,
        weak_width,
        s=34,
        color="#7A1F1F",
        edgecolor="white",
        linewidth=0.6,
        zorder=4,
    )
    axes[0].set_ylim(0.0, positive_axis_limit(np.concatenate([exact_width, weak_width]), floor=0.25))
    axes[0].set_ylabel("Radius interval width [mm]")
    axes[0].set_title("Final Radius Ambiguity Intervals")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(loc="upper left", fontsize=8, frameon=True)

    axes[1].bar(x, runtime_min, color=colors)
    axes[1].set_ylim(0.0, positive_axis_limit(runtime_min, floor=5.0))
    axes[1].set_ylabel("Wall time [min]")
    axes[1].set_title("Packaged Pipeline Runtime")
    axes[1].grid(axis="y", alpha=0.25)

    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha="right")
        ax.set_xlabel("Experiment")

    return save_validated_figure(fig, save_path)


def plot_stage_confidence_summary(rows, save_path):
    """Plot fine-stage and final-stage radius margins side by side."""
    labels = [row["run_id"] for row in rows]
    fine_margin = np.asarray([row["fine_stage_margin_abs"] for row in rows], dtype=np.float64)
    final_margin = np.asarray([row["final_margin_abs"] for row in rows], dtype=np.float64)
    final_stage_labels = [row["final_stage"] for row in rows]

    fig, ax = plt.subplots(figsize=(11.0, 4.8), constrained_layout=True)
    x = np.arange(len(rows))
    width = 0.34
    ax.bar(
        x - width / 2,
        fine_margin,
        width=width,
        color="#4C78A8",
        alpha=0.85,
        label="fine-stage margin",
    )
    ax.bar(
        x + width / 2,
        final_margin,
        width=width,
        color="#E45756",
        alpha=0.85,
        label="final-stage margin",
    )
    ax.scatter(
        x - width / 2,
        fine_margin,
        s=32,
        color="#17324D",
        edgecolor="white",
        linewidth=0.6,
        zorder=4,
    )
    ax.scatter(
        x + width / 2,
        final_margin,
        s=32,
        color="#7A1F1F",
        edgecolor="white",
        linewidth=0.6,
        zorder=4,
    )
    ax.axhline(1.0e-3, color="black", linestyle="--", linewidth=1.0, label="strong abs threshold")
    ax.set_ylim(0.0, positive_axis_limit(np.concatenate([fine_margin, final_margin]), floor=0.003))
    ax.set_ylabel("Radius margin")
    ax.set_title("Fine-Stage vs Final-Stage Radius Confidence")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(loc="upper right", fontsize=8, frameon=True)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_xlabel("Experiment")

    for index, stage_name in enumerate(final_stage_labels):
        if stage_name != "fine_polish":
            ax.text(
                index,
                0.02,
                stage_name.replace("_", " "),
                transform=ax.get_xaxis_transform(),
                ha="center",
                va="bottom",
                fontsize=7,
                rotation=90,
                color="#555555",
            )

    return save_validated_figure(fig, save_path)


def plot_material_uncertainty_summary(rows, save_path):
    """Plot nominal and material/source-aware interval widths when present."""
    material_rows = [row for row in rows if row.get("material_uncertainty_enabled")]
    if not material_rows:
        return None
    labels = [row["run_id"] for row in material_rows]
    nominal_width = np.asarray([interval_width(row, "weak") for row in material_rows], dtype=np.float64)
    material_width = np.asarray(
        [row["material_weak_interval_width_mm"] for row in material_rows],
        dtype=np.float64,
    )
    point_shift = np.asarray(
        [row["material_minus_nominal_best_mm"] for row in material_rows],
        dtype=np.float64,
    )

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 6.8), constrained_layout=True)
    x = np.arange(len(material_rows))
    width = 0.34
    axes[0].bar(
        x - width / 2,
        nominal_width,
        width=width,
        color="#4C78A8",
        alpha=0.85,
        label="nominal weak width",
    )
    axes[0].bar(
        x + width / 2,
        material_width,
        width=width,
        color="#E45756",
        alpha=0.85,
        label="material/source weak width",
    )
    axes[0].set_ylim(0.0, positive_axis_limit(np.concatenate([nominal_width, material_width]), floor=0.12))
    axes[0].set_ylabel("Interval width [mm]")
    axes[0].set_title("Nominal vs Material/Source-Aware Radius Interval Width")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(loc="upper right", fontsize=8, frameon=True)

    axes[1].bar(x, point_shift, color="#7A5195", alpha=0.9)
    axes[1].axhline(0.0, color="black", linewidth=0.9)
    axes[1].set_ylim(*symmetric_error_limits(point_shift, floor=0.06))
    axes[1].set_ylabel("Material minus nominal point [mm]")
    axes[1].set_title("Material/Source Point Shift")
    axes[1].grid(axis="y", alpha=0.25)

    for ax in axes:
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=35, ha="right")
        ax.set_xlabel("Experiment")
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, rows):
    """Write plain-language notes for the aggregate figure."""
    weak = [row["run_id"] for row in rows if row["confidence"] == "weak"]
    downgraded = [
        row["run_id"]
        for row in rows
        if row["fine_stage_confidence"] != "weak" and row["final_confidence"] == "weak"
    ]
    upgraded = [
        row["run_id"]
        for row in rows
        if row["fine_stage_confidence"] == "weak" and row["final_confidence"] != "weak"
    ]
    guarded = [
        (
            row["run_id"],
            row["weak_radius_min_mm"],
            row["weak_radius_max_mm"],
        )
        for row in rows
        if row.get("final_stage") == "guarded_polish"
    ]
    highband = [
        (
            row["run_id"],
            row["weak_radius_min_mm"],
            row["weak_radius_max_mm"],
        )
        for row in rows
        if row.get("final_stage") == "highband_polish"
    ]
    max_weak_width = max(interval_width(row, "weak") for row in rows)
    widest_runs = [
        row["run_id"]
        for row in rows
        if np.isclose(interval_width(row, "weak"), max_weak_width, rtol=0.0, atol=1e-9)
    ]
    material_rows = [
        (
            row["run_id"],
            row["material_best_radius_mm"],
            row["material_weak_radius_min_mm"],
            row["material_weak_radius_max_mm"],
            row["material_minus_nominal_best_mm"],
        )
        for row in rows
        if row.get("material_uncertainty_enabled")
    ]
    text = f"""# Figure Notes

## 1. `two_stage_margin_summary.png` - packaged pipeline comparison

This figure compares packaged detector-to-refinement runs. The top panel shows
final radius error in millimeters. Markers sitting on the horizontal zero line
mean the final radius matched the known synthetic truth exactly. The bottom
panel shows the final radius margin from each run's final stage. For older
runs this is the fine-polish stage; for guarded runs it is the guarded-polish
stage; for high-band runs it is the separately acquired high-band polish
stage. The margin is the objective-value gap between the best radius and the
next tested radius; larger means the radius decision is clearer.

Colors in the bottom panel are quick confidence labels: green is strong,
yellow is moderate, and red is weak. These labels are triage aids, not formal
uncertainty intervals.

Main result: all included runs have zero final radius error, but not all have
the same confidence. Weak-margin runs are: `{weak}`. Inspect those first when
deciding where the next replication effort should go.

## 2. `two_stage_stage_confidence_summary.png` - fine versus final confidence

This figure compares the radius margin before and after the final stage. The
fine-stage margin is the cheaper local FWI check. The final-stage margin is
the result used for the final report; for guarded runs this is the guarded
subcell multifrequency polish, and for high-band runs this is a separate
high-band local acquisition. A smaller final-stage margin means the more
careful comparison found a nearby radius that should remain in the uncertainty
interval. A larger final-stage margin means the added final stage improved
radius separation.

Main result: runs where confidence is downgraded from the fine stage to the
final stage are `{downgraded}`. Runs where confidence is upgraded are
`{upgraded}`. Downgraded runs should be reported with both the best radius and
the final weak interval; upgraded runs still need their interval reported if
the interval width is nonzero.

## 3. `two_stage_interval_runtime_summary.png` - ambiguity and cost

This figure makes the interval result visible directly. The top panel shows
two radius-uncertainty widths in millimeters. The exact tie width is the span
of radii that are numerically tied with the best candidate. A zero width means
only one sampled radius was exactly best. The weak interval width is the wider
span of radii whose objective values are close enough that a confident single
radius estimate would be misleading.

The bottom panel shows total packaged runtime in minutes. Use it to judge
whether an objective variant bought enough extra confidence to justify its
cost.

Main result: the widest weak interval width is `{max_weak_width:.3f} mm`,
shared by runs `{widest_runs}`. Guarded-polish runs and weak intervals are
`{guarded}`. High-band-polish runs and weak intervals are `{highband}`. A final
stage with a smaller weak interval is a useful pipeline improvement, but the
interval still needs to be reported if it remains nonzero.

## 4. `two_stage_material_uncertainty_summary.png` - optional material/source uncertainty

This figure is present when any packaged run includes the optional
material/source-aware radius report. The top panel compares the nominal weak
radius interval width with the material/source-aware interval width. The bottom
panel shows how far the material/source-aware point radius moved from the
nominal final-stage point estimate.

Material/source-aware rows are `{material_rows}`. A nonzero point shift means
the nuisance-parameter diagnostic found a different best radius than the
nominal high-band polish. That should be reported as uncertainty evidence, not
silently used to overwrite the final geometry estimate.
"""
    Path(path).write_text(text, encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="outputs/experiments")
    parser.add_argument("--run-dirs", nargs="*", default=None)
    parser.add_argument("--run-name", default="two_stage_refinement_aggregate")
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

    summary_paths = find_summary_paths(args.root, args.run_dirs)
    rows = []
    for summary_path in summary_paths:
        if not summary_path.exists():
            raise FileNotFoundError(summary_path)
        with summary_path.open("r", encoding="utf-8") as handle:
            summary = json.load(handle)
        rows.append(summarize_two_stage_summary(summary, summary_path.parent.parent))

    if not rows:
        raise ValueError("no two-stage summaries found")

    rows.sort(key=lambda row: row["run_id"])
    csv_path = data_dir / "two_stage_refinement_aggregate.csv"
    json_path = data_dir / "two_stage_refinement_aggregate.json"
    plot_path = figures_dir / "two_stage_margin_summary.png"
    stage_plot_path = figures_dir / "two_stage_stage_confidence_summary.png"
    interval_plot_path = figures_dir / "two_stage_interval_runtime_summary.png"
    material_plot_path = figures_dir / "two_stage_material_uncertainty_summary.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_rows_csv(csv_path, rows)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({"rows": rows}, handle, indent=2)
    plot_margin_summary(rows, plot_path)
    plot_stage_confidence_summary(rows, stage_plot_path)
    plot_interval_runtime_summary(rows, interval_plot_path)
    saved_material_plot = plot_material_uncertainty_summary(rows, material_plot_path)
    plt.close("all")
    write_figure_notes(notes_path, rows)
    write_run_manifest(
        str(outdir),
        "two_stage_refinement_aggregate",
        {
            "csv": str(csv_path),
            "json": str(json_path),
            "plot": str(plot_path),
            "stage_confidence_plot": str(stage_plot_path),
            "interval_runtime_plot": str(interval_plot_path),
            "material_uncertainty_plot": str(saved_material_plot) if saved_material_plot else None,
        },
    )

    print(f"Rows: {len(rows)}")
    print(f"Weak confidence runs: {[row['run_id'] for row in rows if row['confidence'] == 'weak']}")
    print(f"Wrote CSV: {csv_path}")
    print(f"Wrote plot: {plot_path}")
    print(f"Wrote stage-confidence plot: {stage_plot_path}")
    print(f"Wrote interval/runtime plot: {interval_plot_path}")
    if saved_material_plot:
        print(f"Wrote material-uncertainty plot: {saved_material_plot}")


if __name__ == "__main__":
    main()
