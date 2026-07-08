#!/usr/bin/env python3
"""Reporting-first coordinate optimizer for multi-rebar local geometry."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from inversion.candidate_confidence import (  # noqa: E402
    ConfidenceThresholds,
    summarize_case_confidence,
    write_confidence_csv,
)
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.multi_rebar_coordinate import (  # noqa: E402
    CoordinateState,
    choose_case_label,
    is_weak_high_radius_branch,
    revisit_radius_offsets_from_row,
    step_report,
    target_window,
    update_state_from_candidate,
)
from run_multi_rebar_common_radius_profile import (  # noqa: E402
    build_observed_cases,
    build_scan_positions,
    default_rebar_x_values_mm,
    default_rebar_z_values_mm,
)
from run_experiment_scene_visualization import (  # noqa: E402
    scene_from_summary,
    write_scene_artifacts,
)
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    best_curve_by_radius,
    build_objective_results,
    build_variable_geometry_model,
    evaluate_local_geometry_grid,
    rank_case,
    parse_objective_variants,
    write_candidate_csv,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_replication import parse_replication_cases  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CASES = "nominal:1.0,0.0,1.0,0.0,0"


def parse_target_indices(text):
    """Parse comma-separated zero-based target indices."""
    values = [int(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one target index is required")
    if any(value < 0 for value in values):
        raise argparse.ArgumentTypeError("target indices must be non-negative")
    return values


def parse_vector_mm(text):
    """Parse comma values or ranges while preserving vector order/duplicates."""
    values = []
    for item in str(text).split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            parts = [float(part.strip()) for part in item.split(":") if part.strip()]
            if len(parts) != 3:
                raise argparse.ArgumentTypeError("ranges must use min:max:step")
            start, stop, step = parts
            if step <= 0.0 or start > stop:
                raise argparse.ArgumentTypeError("range requires positive step and start <= stop")
            count = int(np.floor((stop - start) / step + 1e-9)) + 1
            values.extend(round(float(start + step * idx), 10) for idx in range(count))
        else:
            values.append(round(float(item), 10))
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return values


def truth_radius_values_for_run(common_radius_mm, radius_values_mm, target_count):
    """Resolve common or per-target truth radii for the synthetic observed model."""
    if radius_values_mm is None:
        return [float(common_radius_mm)] * int(target_count)
    values = [float(value) for value in radius_values_mm]
    if len(values) != int(target_count):
        raise ValueError("truth radius values must match truth x/z value count")
    return values


def summary_truth_radius_mm(common_radius_mm, truth_radii_mm, target_indices):
    """Return the scalar truth radius that best represents this optimizer run."""
    targets = [int(value) for value in target_indices]
    if len(targets) == 1:
        target = targets[0]
        if 0 <= target < len(truth_radii_mm):
            return float(truth_radii_mm[target])
    return float(common_radius_mm)


def results_from_candidates(candidates, case_labels, top_k):
    """Build ranked result dictionaries for each observed case."""
    results = {}
    for label in case_labels:
        ranked = rank_case(candidates, label)
        results[label] = {
            "margin": radius_margin_from_ranked(ranked),
            "top_candidates": ranked[:int(top_k)],
            "best_curve_by_radius": best_curve_by_radius(candidates, label),
        }
    return results


def confidence_rows_for_step(
        run_name,
        pass_index,
        target_index,
        update_case_label,
        results,
        meta,
        step_kind="main"):
    """Flatten all case results for one coordinate step."""
    rows = []
    for label, result in results.items():
        row = summarize_case_confidence(run_name, label, result, meta)
        row.update({
            "pass_index": int(pass_index),
            "step_target_index": int(target_index),
            "update_case_label": update_case_label,
            "step_kind": step_kind,
        })
        rows.append(row)
    return rows


def objective_diagnostic_rows_for_step(
        run_name,
        pass_index,
        target_index,
        update_case_label,
        objective_results,
        meta,
        step_kind="main"):
    """Flatten objective-variant diagnostics for one coordinate step."""
    rows = []
    for case_label, by_objective in objective_results.items():
        for objective_label, result in by_objective.items():
            best = result["top_candidates"][0]
            params = best["params"]
            profile = best["source_profile"]
            margin = result["margin"]
            rows.append({
                "run_name": run_name,
                "case_label": case_label,
                "objective_label": objective_label,
                "backend": meta.get("backend"),
                "grid_step_mm": meta.get("grid_step_mm"),
                "target_rebar_index": meta.get("target_rebar_index"),
                "candidate_count": meta.get("candidate_count"),
                "case_count": meta.get("case_count"),
                "pass_index": int(pass_index),
                "step_target_index": int(target_index),
                "update_case_label": update_case_label,
                "step_kind": step_kind,
                "best_x_mm": params["x_mm"],
                "best_z_mm": params["z_mm"],
                "best_radius_mm": margin["best_radius_mm"],
                "next_radius_mm": margin["next_radius_mm"],
                "radius_margin_abs": margin["radius_margin_abs"],
                "radius_margin_rel": margin["radius_margin_rel"],
                "best_misfit": margin["best_radius_misfit"],
                "best_source_frequency_scale": profile.get("frequency_scale"),
                "best_source_time_shift_ps": profile.get("time_shift_ps"),
                "best_source_amplitude_scale": profile.get("amplitude_scale"),
                "best_source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                "best_source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                "best_source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                "best_source_primary_coefficient": profile.get("primary_coefficient", profile.get("amplitude_scale")),
                "best_source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
            })
    return rows


def write_objective_diagnostic_csv(path, rows):
    """Write optional objective-variant diagnostic rows to CSV."""
    fieldnames = [
        "run_name",
        "case_label",
        "objective_label",
        "backend",
        "grid_step_mm",
        "target_rebar_index",
        "candidate_count",
        "case_count",
        "pass_index",
        "step_target_index",
        "update_case_label",
        "step_kind",
        "best_x_mm",
        "best_z_mm",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "radius_margin_rel",
        "best_misfit",
        "best_source_frequency_scale",
        "best_source_time_shift_ps",
        "best_source_amplitude_scale",
        "best_source_ringdown_scale",
        "best_source_ringdown_delay_ps",
        "best_source_ringdown_frequency_scale",
        "best_source_primary_coefficient",
        "best_source_ringdown_coefficient",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _json_or_none(value):
    if value is None:
        return None
    return json.dumps(value)


def objective_top_candidate_rows_for_step(
        run_name,
        pass_index,
        target_index,
        update_case_label,
        objective_results,
        meta,
        step_kind="main"):
    """Flatten ranked objective-variant top candidates for one coordinate step."""
    rows = []
    for case_label, by_objective in objective_results.items():
        for objective_label, result in by_objective.items():
            for rank, candidate in enumerate(result["top_candidates"], start=1):
                params = candidate["params"]
                profile = candidate["source_profile"]
                rows.append({
                    "run_name": run_name,
                    "case_label": case_label,
                    "objective_label": objective_label,
                    "rank": int(rank),
                    "backend": meta.get("backend"),
                    "grid_step_mm": meta.get("grid_step_mm"),
                    "target_rebar_index": meta.get("target_rebar_index"),
                    "candidate_count": meta.get("candidate_count"),
                    "case_count": meta.get("case_count"),
                    "pass_index": int(pass_index),
                    "step_target_index": int(target_index),
                    "update_case_label": update_case_label,
                    "step_kind": step_kind,
                    "candidate_target_index": params.get("target_index"),
                    "x_mm": params.get("x_mm"),
                    "z_mm": params.get("z_mm"),
                    "radius_mm": params.get("radius_mm"),
                    "x_values_mm": _json_or_none(params.get("x_values_mm")),
                    "z_values_mm": _json_or_none(params.get("z_values_mm")),
                    "radii_mm": _json_or_none(params.get("radii_mm")),
                    "misfit": candidate["misfit"],
                    "source_frequency_scale": profile.get("frequency_scale"),
                    "source_time_shift_ps": profile.get("time_shift_ps"),
                    "source_amplitude_scale": profile.get("amplitude_scale"),
                    "source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                    "source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                    "source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                    "source_primary_coefficient": profile.get("primary_coefficient", profile.get("amplitude_scale")),
                    "source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
                })
    return rows


def write_objective_top_candidate_csv(path, rows):
    """Write ranked objective-variant top candidates to CSV."""
    fieldnames = [
        "run_name",
        "case_label",
        "objective_label",
        "rank",
        "backend",
        "grid_step_mm",
        "target_rebar_index",
        "candidate_count",
        "case_count",
        "pass_index",
        "step_target_index",
        "update_case_label",
        "step_kind",
        "candidate_target_index",
        "x_mm",
        "z_mm",
        "radius_mm",
        "x_values_mm",
        "z_values_mm",
        "radii_mm",
        "misfit",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
        "source_ringdown_scale",
        "source_ringdown_delay_ps",
        "source_ringdown_frequency_scale",
        "source_primary_coefficient",
        "source_ringdown_coefficient",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def latest_high_radius_revisit_rows(confidence_rows, case_label):
    """Return latest per-target rows that need high-radius-branch revisits."""
    latest_by_target = {}
    for row in confidence_rows:
        if row.get("case_label") != case_label:
            continue
        latest_by_target[int(row["step_target_index"])] = row
    return [
        row
        for _, row in sorted(latest_by_target.items())
        if is_weak_high_radius_branch(row)
    ]


def _number_or_none(value):
    if value in ("", None):
        return None
    return float(value)


def is_broad_radius_ambiguity(row, min_width_mm=0.2, labels=("weak", "moderate", "ambiguous")):
    """Return True when a row has a broad radius interval worth revisiting."""
    if row.get("confidence_label") not in set(labels):
        return False
    lower = _number_or_none(row.get("ambiguity_radius_min_mm"))
    upper = _number_or_none(row.get("ambiguity_radius_max_mm"))
    if lower is None or upper is None:
        return False
    return (upper - lower) >= float(min_width_mm)


def latest_broad_radius_revisit_rows(confidence_rows, case_label, min_width_mm=0.2):
    """Return latest per-target rows with broad weak/moderate radius ambiguity."""
    latest_by_target = {}
    for row in confidence_rows:
        if row.get("case_label") != case_label:
            continue
        latest_by_target[int(row["step_target_index"])] = row
    return [
        row
        for _, row in sorted(latest_by_target.items())
        if is_broad_radius_ambiguity(row, min_width_mm=min_width_mm)
    ]


def merge_revisit_rows(*row_groups):
    """Merge revisit row lists by target index while preserving first occurrence."""
    rows = []
    seen = set()
    for group in row_groups:
        for row in group:
            target_index = int(row["step_target_index"])
            if target_index in seen:
                continue
            rows.append(row)
            seen.add(target_index)
    return rows


def write_state_csv(path, state_history):
    """Write pass/target coordinate states to CSV."""
    fieldnames = [
        "step",
        "pass_index",
        "target_index",
        "case_label",
        "x_values_mm",
        "z_values_mm",
        "radii_mm",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in state_history:
            writer.writerow({
                "step": row["step"],
                "pass_index": row["pass_index"],
                "target_index": row["target_index"],
                "case_label": row["case_label"],
                "x_values_mm": json.dumps(row["state"].as_dict()["x_values_mm"]),
                "z_values_mm": json.dumps(row["state"].as_dict()["z_values_mm"]),
                "radii_mm": json.dumps(row["state"].as_dict()["radii_mm"]),
            })


def _float_or_none(value):
    if value in ("", None):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return numeric if math.isfinite(numeric) else None


def _int_or_none(value):
    numeric = _float_or_none(value)
    if numeric is None:
        return None
    return int(numeric)


def _short_case_label(label):
    text = str(label or "case")
    replacements = [
        ("source_mismatch_ringdown050_noise10_", "noise10 "),
        ("source_mismatch_ringdown025_noise10_", "noise10 "),
        ("source_mismatch_", ""),
        ("ringdown050_", ""),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text if len(text) <= 38 else text[:35] + "..."


def _step_label(row, include_case=True):
    pass_index = _int_or_none(row.get("pass_index"))
    target_index = _int_or_none(row.get("step_target_index"))
    prefix = f"p{pass_index if pass_index is not None else '?'} "
    prefix += f"t{target_index if target_index is not None else '?'}"
    if not include_case:
        return prefix
    return f"{prefix}\n{_short_case_label(row.get('case_label'))}"


def _confidence_color(label):
    return {
        "strong": "#1b7837",
        "moderate": "#4575b4",
        "weak": "#d73027",
        "ambiguous": "#7f7f7f",
        "missing": "#8c8c8c",
    }.get(str(label), "#8c8c8c")


def _objective_sort_key(label):
    order = {
        "base": 0,
        "highband": 1,
        "late": 2,
        "late_high": 3,
        "veryhigh": 4,
        "early_high": 5,
    }
    return (order.get(str(label), 100), str(label))


def _format_mm(value):
    numeric = _float_or_none(value)
    return "n/a" if numeric is None else f"{numeric:.2f} mm"


def _format_scientific(value):
    numeric = _float_or_none(value)
    return "n/a" if numeric is None else f"{numeric:.3e}"


def _updated_case_rows(rows):
    selected = [
        row for row in rows
        if row.get("case_label") == row.get("update_case_label")
    ]
    return selected or list(rows)


def _candidate_radius_limits(rows):
    values = []
    for row in rows:
        for key in ("best_radius_mm", "next_radius_mm", "competing_geometry_radius_mm", "radius_mm"):
            value = _float_or_none(row.get(key))
            if value is not None:
                values.append(value)
    if not values:
        return 0.0, 1.0
    lo = min(values)
    hi = max(values)
    if lo == hi:
        return lo - 0.5, hi + 0.5
    pad = max(0.2, 0.12 * (hi - lo))
    return lo - pad, hi + pad


def plot_coordinate_margins(rows, save_path, thresholds=None):
    """Plot confidence margins for coordinate-search update rows."""
    if not rows:
        raise ValueError("no confidence rows to plot")
    thresholds = thresholds or ConfidenceThresholds()
    labels = [_step_label(row) for row in rows]
    values = [
        0.0 if _float_or_none(row.get("radius_margin_abs")) is None
        else _float_or_none(row.get("radius_margin_abs"))
        for row in rows
    ]
    colors = [_confidence_color(row.get("confidence_label")) for row in rows]
    height = max(3.8, 0.42 * len(rows) + 2.4)
    with plt.style.context("seaborn-v0_8-whitegrid"):
        fig, ax = plt.subplots(figsize=(10.5, height), constrained_layout=True)
        y_positions = np.arange(len(rows))
        ax.barh(y_positions, values, color=colors, edgecolor="#333333", linewidth=0.5)
        ax.axvline(
            thresholds.moderate_abs,
            color="#111111",
            linestyle="--",
            linewidth=1.1,
            label=f"moderate cutoff {thresholds.moderate_abs:.1e}",
        )
        for y_pos, row, value in zip(y_positions, rows, values):
            best = _format_mm(row.get("best_radius_mm"))
            next_radius = _format_mm(row.get("next_radius_mm"))
            ax.text(
                value + max(thresholds.moderate_abs * 0.035, 1.0e-6),
                y_pos,
                f"{row.get('confidence_label', 'unknown')} | best {best}, next {next_radius}",
                va="center",
                fontsize=8,
                color="#222222",
            )
        ax.set_title("Coordinate Optimizer Radius Confidence")
        ax.set_xlabel("Best-vs-next-radius objective gap")
        ax.set_yticks(y_positions)
        ax.set_yticklabels(labels, fontsize=8)
        ax.invert_yaxis()
        ax.grid(True, axis="x", alpha=0.25)
        xmax = max(max(values) * 1.35, thresholds.moderate_abs * 1.6, 1.0e-3)
        ax.set_xlim(0.0, xmax)
        ax.legend(loc="lower right", fontsize=8, frameon=True)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_coordinate_radius_decision_panel(
        rows,
        objective_rows,
        save_path,
        thresholds=None):
    """Plot a standalone radius-decision summary for coordinate-search rows."""
    update_rows = _updated_case_rows(rows)
    if not update_rows:
        raise ValueError("no update confidence rows to plot")
    thresholds = thresholds or ConfidenceThresholds()
    objective_rows = list(objective_rows or [])

    with plt.style.context("seaborn-v0_8-whitegrid"):
        fig = plt.figure(figsize=(12.4, 9.2), constrained_layout=True)
        grid = fig.add_gridspec(3, 1, height_ratios=[1.1, 1.0, 1.35])
        ax_radius = fig.add_subplot(grid[0, 0])
        ax_margin = fig.add_subplot(grid[1, 0])
        ax_objectives = fig.add_subplot(grid[2, 0])

        y_positions = np.arange(len(update_rows))
        for y_pos, row in zip(y_positions, update_rows):
            best_radius = _float_or_none(row.get("best_radius_mm"))
            next_radius = _float_or_none(row.get("next_radius_mm"))
            color = _confidence_color(row.get("confidence_label"))
            if best_radius is not None and next_radius is not None:
                ax_radius.plot(
                    [best_radius, next_radius],
                    [y_pos, y_pos],
                    color="#9ca3af",
                    linewidth=2.0,
                    zorder=1,
                )
            if best_radius is not None:
                ax_radius.scatter(
                    [best_radius],
                    [y_pos],
                    s=180,
                    color=color,
                    edgecolor="white",
                    linewidth=1.2,
                    zorder=3,
                    label="selected radius" if y_pos == 0 else None,
                )
                ax_radius.text(
                    best_radius,
                    y_pos + 0.19,
                    f"selected\nr={best_radius:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    color="#111111",
                )
            if next_radius is not None:
                ax_radius.scatter(
                    [next_radius],
                    [y_pos],
                    s=130,
                    facecolor="white",
                    edgecolor="#4b5563",
                    linewidth=1.5,
                    zorder=2,
                    label="next radius" if y_pos == 0 else None,
                )
                ax_radius.text(
                    next_radius,
                    y_pos - 0.19,
                    f"next\nr={next_radius:.2f}",
                    ha="center",
                    va="top",
                    fontsize=8,
                    color="#374151",
                )
            comp_radius = _float_or_none(row.get("competing_geometry_radius_mm"))
            comp_z = _float_or_none(row.get("competing_geometry_z_mm"))
            if comp_radius is not None:
                ax_radius.scatter(
                    [comp_radius],
                    [y_pos],
                    marker="D",
                    s=72,
                    facecolor="#facc15",
                    edgecolor="#92400e",
                    linewidth=1.0,
                    zorder=4,
                    label="next x/z geometry" if y_pos == 0 else None,
                )
                suffix = "" if comp_z is None else f", z={comp_z:.0f}"
                ax_radius.text(
                    comp_radius,
                    y_pos + 0.36,
                    f"geom r={comp_radius:.2f}{suffix}",
                    ha="center",
                    va="bottom",
                    fontsize=7.5,
                    color="#78350f",
                )

        ax_radius.set_title(
            "Coordinate Radius Decision: Selected vs Closest Competitors",
            pad=14,
        )
        ax_radius.set_xlabel("Radius candidate (mm)")
        ax_radius.set_yticks(y_positions)
        ax_radius.set_yticklabels([_step_label(row) for row in update_rows], fontsize=8)
        ax_radius.set_xlim(*_candidate_radius_limits(update_rows))
        ax_radius.set_ylim(len(update_rows) - 0.45, -0.55)
        ax_radius.legend(loc="best", fontsize=8, frameon=True)

        deltas = [
            (_float_or_none(row.get("radius_margin_abs")) or 0.0) - thresholds.moderate_abs
            for row in update_rows
        ]
        margin_colors = [
            "#1b7837" if delta >= 0.0 else "#d73027"
            for delta in deltas
        ]
        ax_margin.axvline(0.0, color="#111111", linestyle="--", linewidth=1.1)
        ax_margin.barh(y_positions, deltas, color=margin_colors, edgecolor="#333333", linewidth=0.5)
        for y_pos, row, delta in zip(y_positions, update_rows, deltas):
            margin = _float_or_none(row.get("radius_margin_abs"))
            label = "above" if delta >= 0.0 else "below"
            place_inside_negative = (
                delta < 0.0
                and abs(delta) >= thresholds.moderate_abs * 0.18
            )
            if place_inside_negative:
                text_x = delta * 0.5
                ha = "center"
                text_color = "white"
            elif delta < 0.0:
                text_x = max(thresholds.moderate_abs * 0.012, 4.0e-6)
                ha = "left"
                text_color = "#222222"
            else:
                text_x = delta + max(abs(delta) * 0.08, 4.0e-6)
                ha = "left"
                text_color = "#222222"
            ax_margin.text(
                text_x,
                y_pos,
                f"margin={_format_scientific(margin)} ({abs(delta):.2e} {label} cutoff)",
                va="center",
                ha=ha,
                fontsize=8,
                color=text_color,
            )
        span = max(max(abs(delta) for delta in deltas), thresholds.moderate_abs * 0.16)
        ax_margin.set_xlim(-span * 1.45, span * 1.45)
        ax_margin.set_title("Confidence Margin Relative to Cutoff")
        ax_margin.set_xlabel("radius_margin_abs - 5e-4")
        ax_margin.set_yticks(y_positions)
        ax_margin.set_yticklabels([_step_label(row, include_case=False) for row in update_rows], fontsize=8)
        ax_margin.set_ylim(len(update_rows) - 0.45, -0.55)

        if objective_rows:
            filtered = [
                row for row in objective_rows
                if row.get("case_label") == update_rows[0].get("update_case_label")
            ] or objective_rows
            filtered = sorted(filtered, key=lambda row: _objective_sort_key(row.get("objective_label")))
            objective_labels = [str(row.get("objective_label", "objective")) for row in filtered]
            objective_values = [_float_or_none(row.get("radius_margin_abs")) or 0.0 for row in filtered]
            objective_colors = [
                "#2ca25f" if value >= thresholds.moderate_abs else "#de2d26"
                for value in objective_values
            ]
            objective_y = np.arange(len(filtered))
            ax_objectives.barh(
                objective_y,
                objective_values,
                color=objective_colors,
                edgecolor="#333333",
                linewidth=0.5,
            )
            ax_objectives.axvline(
                thresholds.moderate_abs,
                color="#111111",
                linestyle="--",
                linewidth=1.1,
                label="moderate cutoff",
            )
            for y_pos, row, value in zip(objective_y, filtered, objective_values):
                best = _float_or_none(row.get("best_radius_mm"))
                next_radius = _float_or_none(row.get("next_radius_mm"))
                ax_objectives.text(
                    value + max(thresholds.moderate_abs * 0.035, 1.0e-6),
                    y_pos,
                    f"best r={best:.2f}, next r={next_radius:.2f}"
                    if best is not None and next_radius is not None
                    else "radius pair n/a",
                    va="center",
                    fontsize=8,
                    color="#222222",
                )
            ax_objectives.set_yticks(objective_y)
            ax_objectives.set_yticklabels(objective_labels, fontsize=8)
            ax_objectives.set_xlim(
                0.0,
                max(max(objective_values) * 1.35, thresholds.moderate_abs * 1.7),
            )
            ax_objectives.invert_yaxis()
            ax_objectives.legend(loc="lower right", fontsize=8, frameon=True)
        else:
            ax_objectives.text(
                0.5,
                0.5,
                "No objective-variant diagnostic rows were written for this run.",
                transform=ax_objectives.transAxes,
                ha="center",
                va="center",
                fontsize=10,
            )
            ax_objectives.set_xticks([])
            ax_objectives.set_yticks([])
        ax_objectives.set_title("Objective-Variant Radius Margins")
        ax_objectives.set_xlabel("Best-vs-next-radius objective gap")

    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_coordinate_objective_radius_candidates(rows, save_path, max_rank=6):
    """Plot top ranked radius candidates for each objective variant."""
    candidate_rows = [
        row for row in rows
        if (_int_or_none(row.get("rank")) or 0) <= int(max_rank)
    ]
    if not candidate_rows:
        raise ValueError("no objective top-candidate rows to plot")

    objective_labels = sorted(
        {str(row.get("objective_label", "objective")) for row in candidate_rows},
        key=_objective_sort_key,
    )
    y_by_objective = {label: idx for idx, label in enumerate(objective_labels)}
    radii = [
        _float_or_none(row.get("radius_mm"))
        for row in candidate_rows
        if _float_or_none(row.get("radius_mm")) is not None
    ]
    vmin, vmax = _candidate_radius_limits([{"radius_mm": value} for value in radii])

    with plt.style.context("seaborn-v0_8-whitegrid"):
        fig, ax = plt.subplots(
            figsize=(11.8, max(4.8, 0.62 * len(objective_labels) + 2.2)),
            constrained_layout=True,
        )
        xs = []
        ys = []
        cs = []
        sizes = []
        labels = []
        for row in candidate_rows:
            rank = _int_or_none(row.get("rank"))
            objective = str(row.get("objective_label", "objective"))
            radius = _float_or_none(row.get("radius_mm"))
            z_mm = _float_or_none(row.get("z_mm"))
            if rank is None or radius is None:
                continue
            xs.append(rank)
            ys.append(y_by_objective[objective])
            cs.append(radius)
            sizes.append(max(45.0, 180.0 - 18.0 * rank))
            if rank <= 3:
                labels.append((rank, y_by_objective[objective], radius, z_mm))

        scatter = ax.scatter(
            xs,
            ys,
            c=cs,
            cmap="viridis",
            vmin=vmin,
            vmax=vmax,
            s=sizes,
            edgecolor="#222222",
            linewidth=0.45,
            alpha=0.92,
        )
        for rank, y_pos, radius, z_mm in labels:
            z_text = "" if z_mm is None else f"\nz={z_mm:.0f}"
            ax.text(
                rank + 0.08,
                y_pos,
                f"r={radius:.2f}{z_text}",
                va="center",
                ha="left",
                fontsize=7.2,
                color="#111111",
            )
        ax.set_title("Objective-Variant Top Radius Candidates")
        ax.set_xlabel("Candidate rank within each objective (1 = best)")
        ax.set_ylabel("Objective variant")
        ax.set_xticks(range(1, int(max_rank) + 1))
        ax.set_yticks(range(len(objective_labels)))
        ax.set_yticklabels(objective_labels, fontsize=8)
        ax.set_xlim(0.65, int(max_rank) + 0.85)
        ax.set_ylim(len(objective_labels) - 0.55, -0.55)
        colorbar = fig.colorbar(scatter, ax=ax, pad=0.01)
        colorbar.set_label("candidate radius (mm)")
    save_validated_figure(fig, save_path)
    plt.close(fig)


def write_coordinate_figure_notes(path, rows, objective_rows=None, top_candidate_rows=None):
    """Write plain-language notes for coordinate optimizer figures."""
    if not rows:
        raise ValueError("no confidence rows to describe")
    objective_rows = list(objective_rows or [])
    top_candidate_rows = list(top_candidate_rows or [])
    labels = sorted({row.get("confidence_label", "unknown") for row in rows})
    counts = {
        label: sum(row.get("confidence_label") == label for row in rows)
        for label in labels
    }
    count_text = ", ".join(f"{label}={count}" for label, count in counts.items())
    update_rows = [
        row for row in rows
        if row.get("case_label") == row.get("update_case_label")
    ]
    weak_rows = [
        row for row in update_rows
        if row.get("confidence_label") in ("weak", "ambiguous")
    ]
    weak_text = "none"
    if weak_rows:
        weak_text = ", ".join(
            f"target {row['step_target_index']} "
            f"best r={float(row['best_radius_mm']):.3g} mm"
            for row in weak_rows
        )
    broad_rows = [
        row for row in update_rows
        if is_broad_radius_ambiguity(row, min_width_mm=0.2)
    ]
    broad_text = "none"
    if broad_rows:
        broad_text = ", ".join(
            f"target {row['step_target_index']} "
            f"r={float(row['best_radius_mm']):.3g} mm "
            f"interval={float(row['ambiguity_radius_min_mm']):.3g}-"
            f"{float(row['ambiguity_radius_max_mm']):.3g} mm"
            for row in broad_rows
        )

    lines = [
        "# Figure Notes",
        "",
        "## 1. `coordinate_radius_decision_panel.png` - radius decision context",
        "",
        "This is the primary figure for a coordinate-optimizer run. It shows the",
        "selected radius next to the closest competing radius, the margin relative",
        "to the moderate-confidence cutoff, and the objective-variant margins.",
        "It is intended to answer three questions directly: which radius won, what",
        "radius nearly won, and whether the decision clears the cutoff.",
        "",
        "Markers in the first panel use filled circles for the selected radius,",
        "open circles for the next distinct-radius candidate, and diamonds for",
        "the next candidate that changes x/z geometry when such a competitor",
        "exists.",
        "",
        "## 2. `coordinate_confidence_margins.png` - legacy confidence margins",
        "",
        "This figure shows the best-versus-next-radius objective gap for each",
        "coordinate-search step and observed case. Larger bars mean the chosen",
        "radius was more clearly separated from the next competing radius. Small",
        "bars mean the radius is ambiguous even when the selected x/z location is",
        "reasonable.",
        "",
        "Bar colors encode the confidence label used by the reporting code:",
        "`strong`, `moderate`, `weak`, or `ambiguous`. A weak row is not a",
        "failure by itself; it means the result needs an interval, revisit, or",
        "diagnostic check before the point radius should be trusted.",
        "",
        f"Rows in this run: {len(rows)} ({count_text}).",
        "",
        f"Weak update-case rows to inspect first: {weak_text}.",
        "",
        f"Broad radius-ambiguity rows to inspect first: {broad_text}.",
    ]
    if top_candidate_rows:
        lines.extend([
            "",
            "## 3. `coordinate_objective_radius_candidates.png` - ranked radius candidates",
            "",
            "This figure shows the top ranked candidate radii for each diagnostic",
            "objective variant. The x-axis is candidate rank, marker color is the",
            "candidate radius in millimeters, and the first three ranks are labeled",
            "with radius and depth. Use it to see whether the objectives agree on",
            "the same point radius or are split across nearby alternatives.",
            "",
            f"Top-candidate rows included: {len(top_candidate_rows)}.",
        ])
    if objective_rows:
        below = [
            row for row in objective_rows
            if (_float_or_none(row.get("radius_margin_abs")) or 0.0) < ConfidenceThresholds().moderate_abs
        ]
        if below:
            below_text = ", ".join(str(row.get("objective_label")) for row in below)
        else:
            below_text = "none"
        lines.extend([
            "",
            f"Objective variants below moderate cutoff: {below_text}.",
        ])
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--scan-x-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--tx-rx-offset-mm", type=float, default=cfg.TX_RX_OFFSET * 1000.0)
    parser.add_argument("--receiver-sampling", choices=["nearest", "linear"], default="nearest")
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--true-x-values-mm", type=parse_vector_mm, default=default_rebar_x_values_mm())
    parser.add_argument("--true-z-values-mm", type=parse_vector_mm, default=default_rebar_z_values_mm())
    parser.add_argument("--truth-radius-mm", type=float, default=cfg.REBAR_RADIUS * 1000.0)
    parser.add_argument("--truth-radius-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--initial-x-values-mm", type=parse_vector_mm, default=default_rebar_x_values_mm())
    parser.add_argument("--initial-z-values-mm", type=parse_vector_mm, default=default_rebar_z_values_mm())
    parser.add_argument("--initial-radius-values-mm", type=parse_vector_mm, default=parse_vector_mm("6.0,6.0,6.0"))
    parser.add_argument("--target-indices", type=parse_target_indices, default=parse_target_indices("0,1,2"))
    parser.add_argument("--passes", type=int, default=1)
    parser.add_argument("--x-offsets-mm", type=parse_values_mm, default=parse_values_mm("-1:1:1"))
    parser.add_argument("--z-offsets-mm", type=parse_values_mm, default=parse_values_mm("-1:1:1"))
    parser.add_argument("--radius-offsets-mm", type=parse_values_mm, default=parse_values_mm("-0.4:0.4:0.2"))
    parser.add_argument("--replication-cases", type=parse_replication_cases, default=parse_replication_cases(DEFAULT_CASES))
    parser.add_argument("--update-case-label", default=None)
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("0.9,1.0,1.1"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("-80,-50,-25,0,25,50,80"))
    parser.add_argument("--fit-ringdown-coefficient", action="store_true")
    parser.add_argument("--source-ringdown-delay-ps", type=float, default=180.0)
    parser.add_argument("--source-ringdown-frequency-scale", type=float, default=0.8)
    parser.add_argument("--diagnostic-objective-variants", type=parse_objective_variants, default=None)
    parser.set_defaults(fit_amplitude=True)
    parser.add_argument("--no-fit-amplitude", dest="fit_amplitude", action="store_false")
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument(
        "--enforce-nonoverlap-candidates",
        action="store_true",
        help="Skip candidate geometries with overlapping circular rebar cross-sections.",
    )
    parser.add_argument("--revisit-weak-high-radius-targets", action="store_true")
    parser.add_argument("--revisit-broad-radius-ambiguity-targets", action="store_true")
    parser.add_argument("--revisit-ambiguity-min-width-mm", type=float, default=0.2)
    parser.add_argument("--revisit-x-offsets-mm", type=parse_values_mm, default=parse_values_mm("-1:1:1"))
    parser.add_argument("--revisit-z-offsets-mm", type=parse_values_mm, default=parse_values_mm("-1:1:1"))
    parser.add_argument("--revisit-radius-step-mm", type=float, default=0.2)
    parser.add_argument("--run-name", default="multi_rebar_coordinate_optimizer")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    if args.passes < 1:
        raise ValueError("--passes must be positive")
    if args.tx_rx_offset_mm < 0.0:
        raise ValueError("--tx-rx-offset-mm must be non-negative")
    if args.diagnostic_objective_variants and args.diagnostic_objective_variants[0].label != "base":
        raise ValueError("first diagnostic objective variant must be labelled 'base'")
    _override_grid(args.grid_step_mm)

    initial_state = CoordinateState.from_lists(
        args.initial_x_values_mm,
        args.initial_z_values_mm,
        args.initial_radius_values_mm,
    )
    true_radii = truth_radius_values_for_run(
        args.truth_radius_mm,
        args.truth_radius_values_mm,
        len(args.true_x_values_mm),
    )
    true_model = build_variable_geometry_model(
        args.true_x_values_mm,
        args.true_z_values_mm,
        true_radii,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequency_hz = args.frequency_ghz * 1e9
    time_values = generate_time_array(cfg.NT, cfg.DT)
    mute = _build_mute_window(cfg.NT, cfg.DT)
    scan_x_values_m = None
    if args.scan_x_values_mm is not None:
        scan_x_values_m = [value / 1000.0 for value in args.scan_x_values_mm]
    scan_positions, scan_x = build_scan_positions(
        cfg.INVERSION_SCAN_STEP,
        args.sources,
        tx_rx_offset_m=args.tx_rx_offset_mm / 1000.0,
        receiver_sampling=args.receiver_sampling,
        scan_x_values_m=scan_x_values_m,
    )
    source_count = len(scan_x)
    observed_by_case, case_metadata = build_observed_cases(
        true_model,
        time_values,
        frequency_hz,
        scan_positions,
        args.backend,
        args.replication_cases,
    )
    case_labels = [case["label"] for case in args.replication_cases]
    update_case_label = choose_case_label(case_labels, args.update_case_label)

    state = initial_state
    started = time.time()
    steps = []
    confidence_rows = []
    objective_diagnostic_rows = []
    objective_top_candidate_rows = []
    diagnostic_objective_labels = [
        variant.label
        for variant in (args.diagnostic_objective_variants or [])
    ]
    state_history = [{
        "step": 0,
        "pass_index": -1,
        "target_index": -1,
        "case_label": "initial",
        "state": state,
    }]
    step_number = 0
    for pass_index in range(int(args.passes)):
        for target_index in args.target_indices:
            window = target_window(
                state,
                int(target_index),
                args.x_offsets_mm,
                args.z_offsets_mm,
                args.radius_offsets_mm,
            )
            print(
                f"Coordinate step pass={pass_index}, target={target_index}, "
                f"state={state.as_dict()}"
            )
            candidates = evaluate_local_geometry_grid(
                observed_by_case,
                list(state.x_values_mm),
                list(state.z_values_mm),
                args.truth_radius_mm,
                int(target_index),
                window["x_values_mm"],
                window["z_values_mm"],
                window["radius_values_mm"],
                list(state.radii_mm),
                frequency_hz,
                args.source_frequency_scales,
                [value * 1e-12 for value in args.source_time_shift_ps_values],
                scan_positions,
                time_values,
                mute,
                args.backend,
                geometry_mode=args.geometry_mode,
                subcell_samples=args.subcell_samples,
                fit_amplitude=args.fit_amplitude,
                fit_ringdown_coefficient=args.fit_ringdown_coefficient,
                source_ringdown_delay_ps=args.source_ringdown_delay_ps,
                source_ringdown_frequency_scale=args.source_ringdown_frequency_scale,
                objective_variants=args.diagnostic_objective_variants,
                enforce_nonoverlap_candidates=args.enforce_nonoverlap_candidates,
                progress_every=args.progress_every,
            )
            results = results_from_candidates(candidates, case_labels, args.top_k)
            objective_results = None
            if args.diagnostic_objective_variants:
                objective_results = build_objective_results(
                    candidates,
                    case_labels,
                    diagnostic_objective_labels,
                    args.top_k,
                )
            state_before = state
            best_params = results[update_case_label]["top_candidates"][0]["params"]
            state = update_state_from_candidate(state, best_params)
            step_number += 1

            candidate_csv = os.path.join(
                data_dir,
                f"coordinate_step_{step_number:02d}_target_{int(target_index)}_candidates.csv",
            )
            write_candidate_csv(candidate_csv, candidates, case_labels)
            meta = {
                "backend": args.backend,
                "grid_step_mm": args.grid_step_mm,
                "target_rebar_index": int(target_index),
                "candidate_count": len(candidates),
                "case_count": len(case_labels),
            }
            rows = confidence_rows_for_step(
                args.run_name,
                pass_index,
                int(target_index),
                update_case_label,
                results,
                meta,
                step_kind="main",
            )
            confidence_rows.extend(rows)
            if objective_results is not None:
                objective_diagnostic_rows.extend(objective_diagnostic_rows_for_step(
                    args.run_name,
                    pass_index,
                    int(target_index),
                    update_case_label,
                    objective_results,
                    meta,
                    step_kind="main",
                ))
                objective_top_candidate_rows.extend(objective_top_candidate_rows_for_step(
                    args.run_name,
                    pass_index,
                    int(target_index),
                    update_case_label,
                    objective_results,
                    meta,
                    step_kind="main",
                ))
            step = step_report(
                pass_index,
                int(target_index),
                update_case_label,
                state_before,
                state,
                results[update_case_label],
            )
            step.update({
                "candidate_csv": candidate_csv,
                "window": window,
                "results": results,
            })
            if objective_results is not None:
                step["objective_results"] = objective_results
            steps.append(step)
            state_history.append({
                "step": step_number,
                "pass_index": pass_index,
                "target_index": int(target_index),
                "case_label": update_case_label,
                "state": state,
            })
            margin = results[update_case_label]["margin"]
            print(
                f"  updated target={target_index}: "
                f"x={state.x_values_mm[int(target_index)]} mm, "
                f"z={state.z_values_mm[int(target_index)]} mm, "
                f"r={state.radii_mm[int(target_index)]} mm, "
                f"margin={margin['radius_margin_abs']}"
            )

    if args.revisit_weak_high_radius_targets or args.revisit_broad_radius_ambiguity_targets:
        high_radius_rows = (
            latest_high_radius_revisit_rows(confidence_rows, update_case_label)
            if args.revisit_weak_high_radius_targets else []
        )
        broad_ambiguity_rows = (
            latest_broad_radius_revisit_rows(
                confidence_rows,
                update_case_label,
                min_width_mm=args.revisit_ambiguity_min_width_mm,
            )
            if args.revisit_broad_radius_ambiguity_targets else []
        )
        revisit_rows = merge_revisit_rows(high_radius_rows, broad_ambiguity_rows)
        if not revisit_rows:
            print("No radius-ambiguity revisit targets found.")
        for revisit_row in revisit_rows:
            target_index = int(revisit_row["step_target_index"])
            radius_offsets = revisit_radius_offsets_from_row(
                revisit_row,
                state.radii_mm[target_index],
                step_mm=args.revisit_radius_step_mm,
            )
            window = target_window(
                state,
                target_index,
                args.revisit_x_offsets_mm,
                args.revisit_z_offsets_mm,
                radius_offsets,
            )
            print(
                f"Revisit step target={target_index}, "
                f"state={state.as_dict()}, radius_offsets={radius_offsets}"
            )
            candidates = evaluate_local_geometry_grid(
                observed_by_case,
                list(state.x_values_mm),
                list(state.z_values_mm),
                args.truth_radius_mm,
                target_index,
                window["x_values_mm"],
                window["z_values_mm"],
                window["radius_values_mm"],
                list(state.radii_mm),
                frequency_hz,
                args.source_frequency_scales,
                [value * 1e-12 for value in args.source_time_shift_ps_values],
                scan_positions,
                time_values,
                mute,
                args.backend,
                geometry_mode=args.geometry_mode,
                subcell_samples=args.subcell_samples,
                fit_amplitude=args.fit_amplitude,
                fit_ringdown_coefficient=args.fit_ringdown_coefficient,
                source_ringdown_delay_ps=args.source_ringdown_delay_ps,
                source_ringdown_frequency_scale=args.source_ringdown_frequency_scale,
                objective_variants=args.diagnostic_objective_variants,
                enforce_nonoverlap_candidates=args.enforce_nonoverlap_candidates,
                progress_every=args.progress_every,
            )
            results = results_from_candidates(candidates, case_labels, args.top_k)
            objective_results = None
            if args.diagnostic_objective_variants:
                objective_results = build_objective_results(
                    candidates,
                    case_labels,
                    diagnostic_objective_labels,
                    args.top_k,
                )
            state_before = state
            best_params = results[update_case_label]["top_candidates"][0]["params"]
            state = update_state_from_candidate(state, best_params)
            step_number += 1

            candidate_csv = os.path.join(
                data_dir,
                f"coordinate_step_{step_number:02d}_revisit_target_{target_index}_candidates.csv",
            )
            write_candidate_csv(candidate_csv, candidates, case_labels)
            meta = {
                "backend": args.backend,
                "grid_step_mm": args.grid_step_mm,
                "target_rebar_index": target_index,
                "candidate_count": len(candidates),
                "case_count": len(case_labels),
            }
            rows = confidence_rows_for_step(
                args.run_name,
                args.passes,
                target_index,
                update_case_label,
                results,
                meta,
                step_kind="revisit",
            )
            confidence_rows.extend(rows)
            if objective_results is not None:
                objective_diagnostic_rows.extend(objective_diagnostic_rows_for_step(
                    args.run_name,
                    args.passes,
                    target_index,
                    update_case_label,
                    objective_results,
                    meta,
                    step_kind="revisit",
                ))
                objective_top_candidate_rows.extend(objective_top_candidate_rows_for_step(
                    args.run_name,
                    args.passes,
                    target_index,
                    update_case_label,
                    objective_results,
                    meta,
                    step_kind="revisit",
                ))
            step = step_report(
                args.passes,
                target_index,
                update_case_label,
                state_before,
                state,
                results[update_case_label],
            )
            step.update({
                "candidate_csv": candidate_csv,
                "window": window,
                "results": results,
                "step_kind": "revisit",
                "trigger_row": revisit_row,
            })
            if objective_results is not None:
                step["objective_results"] = objective_results
            steps.append(step)
            state_history.append({
                "step": step_number,
                "pass_index": args.passes,
                "target_index": target_index,
                "case_label": f"{update_case_label}:revisit",
                "state": state,
            })
            margin = results[update_case_label]["margin"]
            print(
                f"  revisited target={target_index}: "
                f"x={state.x_values_mm[target_index]} mm, "
                f"z={state.z_values_mm[target_index]} mm, "
                f"r={state.radii_mm[target_index]} mm, "
                f"margin={margin['radius_margin_abs']}"
            )

    elapsed = time.time() - started
    confidence_csv = os.path.join(data_dir, "coordinate_confidence_report.csv")
    objective_diagnostic_csv = os.path.join(data_dir, "coordinate_objective_diagnostics.csv")
    objective_top_candidate_csv = os.path.join(
        data_dir,
        "coordinate_objective_top_candidates.csv",
    )
    state_csv = os.path.join(data_dir, "coordinate_state_history.csv")
    plot_path = os.path.join(figures_dir, "coordinate_confidence_margins.png")
    decision_plot_path = os.path.join(figures_dir, "coordinate_radius_decision_panel.png")
    objective_candidate_plot_path = os.path.join(
        figures_dir,
        "coordinate_objective_radius_candidates.png",
    )
    notes_path = os.path.join(figures_dir, "FIGURE_NOTES.md")
    write_confidence_csv(confidence_rows, confidence_csv)
    if objective_diagnostic_rows:
        write_objective_diagnostic_csv(objective_diagnostic_csv, objective_diagnostic_rows)
    if objective_top_candidate_rows:
        write_objective_top_candidate_csv(objective_top_candidate_csv, objective_top_candidate_rows)
    write_state_csv(state_csv, state_history)
    plot_coordinate_margins(confidence_rows, plot_path)
    plot_coordinate_radius_decision_panel(
        confidence_rows,
        objective_diagnostic_rows,
        decision_plot_path,
    )
    if objective_top_candidate_rows:
        plot_coordinate_objective_radius_candidates(
            objective_top_candidate_rows,
            objective_candidate_plot_path,
        )
    write_coordinate_figure_notes(
        notes_path,
        confidence_rows,
        objective_diagnostic_rows,
        objective_top_candidate_rows,
    )

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": source_count,
        "tx_rx_offset_mm": args.tx_rx_offset_mm,
        "receiver_sampling": args.receiver_sampling,
        "scan_x_values_mm": [float(value * 1000.0) for value in scan_x],
        "frequency_ghz": args.frequency_ghz,
        "true_x_values_mm": args.true_x_values_mm,
        "true_z_values_mm": args.true_z_values_mm,
        "truth_radius_mm": summary_truth_radius_mm(
            args.truth_radius_mm,
            true_radii,
            args.target_indices,
        ),
        "truth_radius_values_mm": true_radii,
        "initial_state": initial_state.as_dict(),
        "final_state": state.as_dict(),
        "target_indices": args.target_indices,
        "passes": args.passes,
        "x_offsets_mm": args.x_offsets_mm,
        "z_offsets_mm": args.z_offsets_mm,
        "radius_offsets_mm": args.radius_offsets_mm,
        "replication_cases": args.replication_cases,
        "case_metadata": case_metadata,
        "update_case_label": update_case_label,
        "source_profile_grid": {
            "frequency_scales": args.source_frequency_scales,
            "time_shift_ps_values": args.source_time_shift_ps_values,
            "fit_amplitude": bool(args.fit_amplitude),
            "fit_ringdown_coefficient": bool(args.fit_ringdown_coefficient),
            "ringdown_delay_ps": float(args.source_ringdown_delay_ps),
            "ringdown_frequency_scale": float(args.source_ringdown_frequency_scale),
        },
        "diagnostic_objective_variants": [
            variant.as_dict()
            for variant in (args.diagnostic_objective_variants or [])
        ],
        "enforce_nonoverlap_candidates": bool(args.enforce_nonoverlap_candidates),
        "elapsed_time_s": float(elapsed),
        "steps": steps,
        "confidence_rows": confidence_rows,
        "objective_diagnostic_rows": objective_diagnostic_rows,
        "objective_top_candidate_row_count": len(objective_top_candidate_rows),
        "paths": {
            "confidence_csv": confidence_csv,
            "objective_diagnostic_csv": (
                objective_diagnostic_csv if objective_diagnostic_rows else None
            ),
            "objective_top_candidate_csv": (
                objective_top_candidate_csv if objective_top_candidate_rows else None
            ),
            "state_csv": state_csv,
            "confidence_plot": plot_path,
            "radius_decision_plot": decision_plot_path,
            "objective_radius_candidate_plot": (
                objective_candidate_plot_path if objective_top_candidate_rows else None
            ),
            "figure_notes": notes_path,
        },
    }
    scene_artifacts = write_scene_artifacts(
        scene_from_summary(summary),
        outdir,
        title=f"{args.run_name} scene",
    )
    summary["paths"].update({
        "scene_geometry_plot": scene_artifacts["figure"],
        "scene_geometry_summary": scene_artifacts["summary"],
    })
    summary["scene_geometry_validation"] = scene_artifacts["validation"]

    summary_path = os.path.join(data_dir, "multi_rebar_coordinate_optimizer_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "multi_rebar_coordinate_optimizer",
        {
            "summary_path": summary_path,
            "confidence_csv": confidence_csv,
            "objective_diagnostic_csv": (
                objective_diagnostic_csv if objective_diagnostic_rows else None
            ),
            "objective_top_candidate_csv": (
                objective_top_candidate_csv if objective_top_candidate_rows else None
            ),
            "state_csv": state_csv,
            "confidence_plot": plot_path,
            "radius_decision_plot": decision_plot_path,
            "objective_radius_candidate_plot": (
                objective_candidate_plot_path if objective_top_candidate_rows else None
            ),
            "scene_geometry_plot": scene_artifacts["figure"],
            "scene_geometry_summary": scene_artifacts["summary"],
            "figure_notes": notes_path,
        },
    )
    print(f"Final state: {state.as_dict()}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote confidence CSV: {confidence_csv}")
    if objective_top_candidate_rows:
        print(f"Wrote objective top-candidate CSV: {objective_top_candidate_csv}")
    print(f"Wrote plot: {plot_path}")
    print(f"Wrote decision plot: {decision_plot_path}")
    if objective_top_candidate_rows:
        print(f"Wrote objective candidate plot: {objective_candidate_plot_path}")
    print(f"Wrote scene geometry plot: {scene_artifacts['figure']}")


if __name__ == "__main__":
    main()
