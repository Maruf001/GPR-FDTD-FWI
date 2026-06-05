#!/usr/bin/env python3
"""Reporting-first coordinate optimizer for multi-rebar local geometry."""

from __future__ import annotations

import argparse
import csv
import json
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


def plot_coordinate_margins(rows, save_path):
    """Plot confidence margins for coordinate-search update rows."""
    if not rows:
        raise ValueError("no confidence rows to plot")
    labels = [
        f"p{row['pass_index']} t{row['step_target_index']}\n{row['case_label']}"
        for row in rows
    ]
    values = [
        0.0 if row["radius_margin_abs"] is None else float(row["radius_margin_abs"])
        for row in rows
    ]
    colors = [
        "#4575b4" if row["confidence_label"] == "moderate"
        else "#1b7837" if row["confidence_label"] == "strong"
        else "#d73027" if row["confidence_label"] == "weak"
        else "#7f7f7f"
        for row in rows
    ]
    width = max(9.0, 0.65 * len(rows))
    fig, ax = plt.subplots(figsize=(width, 5.2), constrained_layout=True)
    ax.bar(range(len(rows)), values, color=colors, edgecolor="#333333", linewidth=0.5)
    ax.set_title("Coordinate Optimizer Radius Confidence")
    ax.set_ylabel("Best-vs-next-radius objective gap")
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.grid(True, axis="y", alpha=0.25)
    ymax = max(max(values) * 1.25, 1.0e-3)
    ax.set_ylim(0.0, ymax)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def write_coordinate_figure_notes(path, rows):
    """Write plain-language notes for coordinate optimizer figures."""
    if not rows:
        raise ValueError("no confidence rows to describe")
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
        "## 1. `coordinate_confidence_margins.png` - coordinate-update radius confidence",
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
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--tx-rx-offset-mm", type=float, default=cfg.TX_RX_OFFSET * 1000.0)
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
    scan_positions, scan_x = build_scan_positions(
        cfg.INVERSION_SCAN_STEP,
        args.sources,
        tx_rx_offset_m=args.tx_rx_offset_mm / 1000.0,
    )
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
    notes_path = os.path.join(figures_dir, "FIGURE_NOTES.md")
    write_confidence_csv(confidence_rows, confidence_csv)
    if objective_diagnostic_rows:
        write_objective_diagnostic_csv(objective_diagnostic_csv, objective_diagnostic_rows)
    if objective_top_candidate_rows:
        write_objective_top_candidate_csv(objective_top_candidate_csv, objective_top_candidate_rows)
    write_state_csv(state_csv, state_history)
    plot_coordinate_margins(confidence_rows, plot_path)
    write_coordinate_figure_notes(notes_path, confidence_rows)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "tx_rx_offset_mm": args.tx_rx_offset_mm,
        "scan_x_values_mm": [float(value * 1000.0) for value in scan_x],
        "frequency_ghz": args.frequency_ghz,
        "true_x_values_mm": args.true_x_values_mm,
        "true_z_values_mm": args.true_z_values_mm,
        "truth_radius_mm": args.truth_radius_mm,
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
            "figure_notes": notes_path,
        },
    }
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
            "figure_notes": notes_path,
        },
    )
    print(f"Final state: {state.as_dict()}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote confidence CSV: {confidence_csv}")
    if objective_top_candidate_rows:
        print(f"Wrote objective top-candidate CSV: {objective_top_candidate_csv}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
