#!/usr/bin/env python3
"""Profile multi-rebar radius evidence over a small material grid."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.radius_confidence import radius_interval_from_curve  # noqa: E402
from run_multi_rebar_common_radius_profile import (  # noqa: E402
    build_observed_cases,
    build_scan_positions,
    default_rebar_x_values_mm,
    default_rebar_z_values_mm,
)
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    evaluate_local_geometry_grid,
    parse_vector_mm,
    truth_radius_values_for_run,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_material_tradeoff import parse_log10_sigma_values  # noqa: E402
from run_single_rebar_source_profiled_replication import parse_replication_cases  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CASES = "source_mismatch_ringdown025_noise10_seed55:1.1,-50.0,1.1,0.10,55,0.25,180.0,0.8"


def parse_float_values(text):
    """Parse comma-separated float values."""
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return values


def rank_material_case(candidates, case_label, top_k=None):
    """Rank material-profiled candidates for one observed case."""
    ranked = []
    for candidate in candidates:
        result = candidate["case_results"][case_label]
        ranked.append({
            "misfit": float(result["misfit"]),
            "params": dict(candidate["params"]),
            "material": dict(candidate.get("material", {})),
            "source_profile": dict(result["source_profile"]),
        })
    ranked.sort(key=lambda item: item["misfit"])
    if top_k is not None:
        ranked = ranked[:max(0, int(top_k))]
    return ranked


def best_material_curve_by_radius(candidates, case_label):
    """Return the best material-profiled candidate at each radius."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        result = candidate["case_results"][case_label]
        current = best.get(radius)
        if current is None or float(result["misfit"]) < float(current["misfit"]):
            best[radius] = {
                "radius_mm": radius,
                "misfit": float(result["misfit"]),
                "params": dict(candidate["params"]),
                "material": dict(candidate.get("material", {})),
                "source_profile": dict(result["source_profile"]),
            }
    return [best[radius] for radius in sorted(best)]


def write_candidate_csv(path, candidates, case_labels):
    """Write the full material-profiled candidate matrix."""
    fieldnames = [
        "case_label",
        "misfit",
        "target_index",
        "x_mm",
        "z_mm",
        "radius_mm",
        "x_values_mm",
        "z_values_mm",
        "radii_mm",
        "concrete_epsr",
        "concrete_sigma",
        "rebar_epsr",
        "rebar_sigma",
        "rebar_log10_sigma",
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
        for candidate in candidates:
            params = candidate["params"]
            material = candidate.get("material", {})
            for label in case_labels:
                result = candidate["case_results"][label]
                profile = result["source_profile"]
                writer.writerow({
                    "case_label": label,
                    "misfit": result["misfit"],
                    "target_index": params["target_index"],
                    "x_mm": params["x_mm"],
                    "z_mm": params["z_mm"],
                    "radius_mm": params["radius_mm"],
                    "x_values_mm": json.dumps(params["x_values_mm"]),
                    "z_values_mm": json.dumps(params["z_values_mm"]),
                    "radii_mm": json.dumps(params["radii_mm"]),
                    "concrete_epsr": material.get("concrete_epsr"),
                    "concrete_sigma": material.get("concrete_sigma"),
                    "rebar_epsr": material.get("rebar_epsr"),
                    "rebar_sigma": material.get("rebar_sigma"),
                    "rebar_log10_sigma": material.get("rebar_log10_sigma"),
                    "source_frequency_scale": profile.get("frequency_scale"),
                    "source_time_shift_ps": profile.get("time_shift_ps"),
                    "source_amplitude_scale": profile.get("amplitude_scale"),
                    "source_ringdown_scale": profile.get("ringdown_scale", 0.0),
                    "source_ringdown_delay_ps": profile.get("ringdown_delay_ps", 0.0),
                    "source_ringdown_frequency_scale": profile.get("ringdown_frequency_scale", 1.0),
                    "source_primary_coefficient": profile.get("primary_coefficient", profile.get("amplitude_scale")),
                    "source_ringdown_coefficient": profile.get("ringdown_coefficient", 0.0),
                })


def write_case_summary_csv(path, results):
    """Write one material-profiled summary row per observed case."""
    fieldnames = [
        "case_label",
        "best_x_mm",
        "best_z_mm",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "radius_margin_rel",
        "best_misfit",
        "concrete_epsr",
        "rebar_log10_sigma",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
        "source_ringdown_scale",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for label, result in results.items():
            best = result["top_candidates"][0]
            params = best["params"]
            material = best["material"]
            profile = best["source_profile"]
            margin = result["margin"]
            writer.writerow({
                "case_label": label,
                "best_x_mm": params["x_mm"],
                "best_z_mm": params["z_mm"],
                "best_radius_mm": margin["best_radius_mm"],
                "next_radius_mm": margin["next_radius_mm"],
                "radius_margin_abs": margin["radius_margin_abs"],
                "radius_margin_rel": margin["radius_margin_rel"],
                "best_misfit": margin["best_radius_misfit"],
                "concrete_epsr": material.get("concrete_epsr"),
                "rebar_log10_sigma": material.get("rebar_log10_sigma"),
                "source_frequency_scale": profile.get("frequency_scale"),
                "source_time_shift_ps": profile.get("time_shift_ps"),
                "source_amplitude_scale": profile.get("amplitude_scale"),
                "source_ringdown_scale": profile.get("ringdown_scale", 0.0),
            })


def evaluate_material_radius_grid(
        observed_by_case,
        base_x_mm,
        base_z_mm,
        truth_radius_mm,
        target_index,
        target_x_values_mm,
        target_z_values_mm,
        target_radius_values_mm,
        base_radii_mm,
        concrete_epsr_values,
        rebar_sigma_values,
        frequency_hz,
        source_frequency_scales,
        time_shift_values_s,
        scan_positions,
        time_values,
        mute,
        backend,
        geometry_mode="hard",
        subcell_samples=5,
        fit_amplitude=True,
        fit_ringdown_coefficient=False,
        source_ringdown_delay_ps=180.0,
        source_ringdown_frequency_scale=0.8,
        progress_every=0):
    """Evaluate local radius candidates while profiling material values."""
    candidates = []
    material_count = len(concrete_epsr_values) * len(rebar_sigma_values)
    started = time.time()
    index = 0
    for concrete_epsr in concrete_epsr_values:
        for rebar_sigma in rebar_sigma_values:
            index += 1
            if material_count > 1:
                print(
                    "Material profile "
                    f"{index}/{material_count}: concrete_epsr={concrete_epsr}, "
                    f"rebar_log10_sigma={np.log10(rebar_sigma):.3g}"
                )
            material_candidates = evaluate_local_geometry_grid(
                observed_by_case,
                base_x_mm,
                base_z_mm,
                truth_radius_mm,
                target_index,
                target_x_values_mm,
                target_z_values_mm,
                target_radius_values_mm,
                base_radii_mm,
                frequency_hz,
                source_frequency_scales,
                time_shift_values_s,
                scan_positions,
                time_values,
                mute,
                backend,
                geometry_mode=geometry_mode,
                subcell_samples=subcell_samples,
                fit_amplitude=fit_amplitude,
                fit_ringdown_coefficient=fit_ringdown_coefficient,
                source_ringdown_delay_ps=source_ringdown_delay_ps,
                source_ringdown_frequency_scale=source_ringdown_frequency_scale,
                concrete_epsr=concrete_epsr,
                rebar_sigma=rebar_sigma,
                progress_every=progress_every,
            )
            candidates.extend(material_candidates)
            elapsed = time.time() - started
            print(f"  Material profile elapsed={elapsed:.1f} s, candidates={len(candidates)}")
    return candidates


def results_from_candidates(candidates, case_labels, top_k):
    """Build material-profiled result dictionaries."""
    results = {}
    for label in case_labels:
        ranked = rank_material_case(candidates, label)
        curve = best_material_curve_by_radius(candidates, label)
        results[label] = {
            "margin": radius_margin_from_ranked(ranked),
            "top_candidates": ranked[:int(top_k)],
            "best_curve_by_radius": curve,
            "radius_ambiguity": {
                "weak_interval": radius_interval_from_curve(
                    curve,
                    abs_tolerance=1.0e-3,
                    rel_tolerance=5.0e-3,
                ),
            },
        }
    return results


def plot_material_radius_profiles(results, save_path):
    """Plot the best material-profiled objective against radius."""
    fig, ax = plt.subplots(figsize=(8.8, 5.2), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radius = [item["radius_mm"] for item in curve]
        misfit = [item["misfit"] for item in curve]
        ax.plot(radius, misfit, marker="o", linewidth=1.8, markersize=4.5, label=label)
        if curve:
            best = min(curve, key=lambda item: item["misfit"])
            ax.scatter([best["radius_mm"]], [best["misfit"]], s=58, edgecolors="black", zorder=4)
    ax.set_title("Multi-Rebar Material-Profiled Radius Evidence")
    ax.set_xlabel("Target radius [mm]")
    ax.set_ylabel("Best objective over material grid")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def write_figure_notes(path, summary):
    """Write notes for material-profiled radius figures."""
    rows = []
    for label, result in summary.get("results", {}).items():
        margin = result.get("margin", {})
        interval = result.get("radius_ambiguity", {}).get("weak_interval", {})
        best = result.get("top_candidates", [{}])[0]
        material = best.get("material", {})
        rows.append(
            f"- {label}: best r={margin.get('best_radius_mm')} mm, "
            f"next r={margin.get('next_radius_mm')} mm, "
            f"margin={margin.get('radius_margin_abs')}, "
            f"weak interval={interval.get('radius_min_mm')}-{interval.get('radius_max_mm')} mm, "
            f"best concrete epsr={material.get('concrete_epsr')}, "
            f"best rebar log10 sigma={material.get('rebar_log10_sigma')}."
        )
    text = "\n".join([
        "# Figure Notes",
        "",
        "## 1. `multi_rebar_material_profiled_radius.png` - material-profiled radius evidence",
        "",
        "This plot shows the best waveform objective at each tested target radius",
        "after profiling over a small concrete-permittivity and rebar-conductivity",
        "grid. Profiling keeps the best material choice at each radius, so a flat",
        "curve means material freedom can mimic radius changes.",
        "",
        "The objective also includes the configured source-profile nuisance grid.",
        "For field-like source-shape runs this can include a fitted delayed",
        "ringdown basis, so material ambiguity is not confused with source mismatch.",
        "",
        "Main rows:",
        *rows,
        "",
        "Inspect this figure before trusting a point radius. A broad weak interval",
        "means the target radius should be reported as an interval even when the",
        "best point is correct.",
    ])
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")


def build_parser():
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
    parser.add_argument("--base-x-values-mm", type=parse_vector_mm, default=default_rebar_x_values_mm())
    parser.add_argument("--base-z-values-mm", type=parse_vector_mm, default=default_rebar_z_values_mm())
    parser.add_argument("--base-radius-values-mm", type=parse_vector_mm, default=parse_vector_mm("6.0,6.0,6.0"))
    parser.add_argument("--target-rebar-index", type=int, default=1)
    parser.add_argument("--target-x-values-mm", type=parse_values_mm, default=parse_values_mm("250"))
    parser.add_argument("--target-z-values-mm", type=parse_values_mm, default=parse_values_mm("90"))
    parser.add_argument("--target-radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.8:6.2:0.2"))
    parser.add_argument("--concrete-epsr-values", type=parse_float_values, default=parse_float_values("5.8,6.0,6.2"))
    parser.add_argument("--rebar-log10-sigma-values", type=parse_log10_sigma_values, default=parse_log10_sigma_values("5,7"))
    parser.add_argument("--replication-cases", type=parse_replication_cases, default=parse_replication_cases(DEFAULT_CASES))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("0.9,1.0,1.1"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("-50,0,50"))
    parser.set_defaults(fit_amplitude=True)
    parser.add_argument("--no-fit-amplitude", dest="fit_amplitude", action="store_false")
    parser.add_argument("--fit-ringdown-coefficient", action="store_true")
    parser.add_argument("--source-ringdown-delay-ps", type=float, default=180.0)
    parser.add_argument("--source-ringdown-frequency-scale", type=float, default=0.8)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=0)
    parser.add_argument("--run-name", default="multi_rebar_material_radius_profile")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    if args.target_rebar_index < 0 or args.target_rebar_index >= len(args.base_x_values_mm):
        raise ValueError("--target-rebar-index is outside the base geometry")
    if args.tx_rx_offset_mm < 0.0:
        raise ValueError("--tx-rx-offset-mm must be non-negative")
    _override_grid(args.grid_step_mm)

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
    started = time.time()
    candidates = evaluate_material_radius_grid(
        observed_by_case,
        args.base_x_values_mm,
        args.base_z_values_mm,
        args.truth_radius_mm,
        int(args.target_rebar_index),
        args.target_x_values_mm,
        args.target_z_values_mm,
        args.target_radius_values_mm,
        args.base_radius_values_mm,
        args.concrete_epsr_values,
        args.rebar_log10_sigma_values,
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
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started
    results = results_from_candidates(candidates, case_labels, args.top_k)

    csv_path = os.path.join(data_dir, "multi_rebar_material_radius_candidates.csv")
    case_csv_path = os.path.join(data_dir, "multi_rebar_material_radius_case_summary.csv")
    plot_path = os.path.join(figures_dir, "multi_rebar_material_profiled_radius.png")
    notes_path = os.path.join(figures_dir, "FIGURE_NOTES.md")
    write_candidate_csv(csv_path, candidates, case_labels)
    write_case_summary_csv(case_csv_path, results)
    plot_material_radius_profiles(results, plot_path)

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
        "base_x_values_mm": args.base_x_values_mm,
        "base_z_values_mm": args.base_z_values_mm,
        "base_radius_values_mm": args.base_radius_values_mm,
        "target_rebar_index": int(args.target_rebar_index),
        "target_x_values_mm": args.target_x_values_mm,
        "target_z_values_mm": args.target_z_values_mm,
        "target_radius_values_mm": args.target_radius_values_mm,
        "concrete_epsr_values": args.concrete_epsr_values,
        "rebar_sigma_values": args.rebar_log10_sigma_values,
        "replication_cases": args.replication_cases,
        "case_metadata": case_metadata,
        "source_profile_grid": {
            "frequency_scales": args.source_frequency_scales,
            "time_shift_ps_values": args.source_time_shift_ps_values,
            "fit_amplitude": bool(args.fit_amplitude),
            "fit_ringdown_coefficient": bool(args.fit_ringdown_coefficient),
            "ringdown_delay_ps": float(args.source_ringdown_delay_ps),
            "ringdown_frequency_scale": float(args.source_ringdown_frequency_scale),
        },
        "geometry_mode": args.geometry_mode,
        "subcell_samples": int(args.subcell_samples),
        "elapsed_time_s": float(elapsed),
        "candidate_count": len(candidates),
        "case_count": len(case_labels),
        "results": results,
        "paths": {
            "candidate_csv": csv_path,
            "case_summary_csv": case_csv_path,
            "plot": plot_path,
            "figure_notes": notes_path,
        },
    }
    summary_path = os.path.join(data_dir, "multi_rebar_material_radius_summary.json")
    write_figure_notes(notes_path, summary)
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_run_manifest(
        outdir,
        "multi_rebar_material_radius_profile",
        {
            "summary_path": summary_path,
            "candidate_csv": csv_path,
            "case_summary_csv": case_csv_path,
            "plot": plot_path,
            "figure_notes": notes_path,
        },
    )
    for label, result in results.items():
        margin = result["margin"]
        print(
            f"{label}: best r={margin['best_radius_mm']} mm, "
            f"next r={margin['next_radius_mm']} mm, "
            f"margin={margin['radius_margin_abs']}"
        )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
