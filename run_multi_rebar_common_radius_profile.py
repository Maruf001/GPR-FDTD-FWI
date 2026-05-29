#!/usr/bin/env python3
"""Profile common radius for a fixed-position multi-rebar scene."""

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
from core.fdtd import FDTDSimulator  # noqa: E402
from core.geometry import build_rebar_model  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array, ricker_wavelet  # noqa: E402
from core.utils import pos_to_index  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.source_profile import source_profiled_ls  # noqa: E402
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import _add_noise, observed_wavelet  # noqa: E402
from run_single_rebar_source_profiled_replication import parse_replication_cases  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CASES = (
    "nominal:1.0,0.0,1.0,0.0,13|"
    "noise10_seed13:1.0,0.0,1.0,0.10,13|"
    "source_mismatch:1.1,-50.0,1.1,0.0,13|"
    "source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13"
)


def default_rebar_x_values_mm():
    return [float(x_center * 1000.0) for _, x_center in cfg.REBAR_POSITIONS]


def default_rebar_z_values_mm():
    return [float(z_center * 1000.0) for z_center, _ in cfg.REBAR_POSITIONS]


def build_rebar_specs_mm(x_values_mm, z_values_mm, radius_mm):
    """Build `(z, x, radius)` specs in meters from millimeter axes."""
    if len(x_values_mm) != len(z_values_mm):
        raise ValueError("x and z rebar lists must have the same length")
    if not x_values_mm:
        raise ValueError("at least one rebar is required")
    return [
        (float(z_mm) / 1000.0, float(x_mm) / 1000.0, float(radius_mm) / 1000.0)
        for x_mm, z_mm in zip(x_values_mm, z_values_mm)
    ]


def build_common_radius_model(
        x_values_mm,
        z_values_mm,
        radius_mm,
        geometry_mode="hard",
        subcell_samples=5):
    """Build a fixed-position multi-rebar model with one shared radius."""
    return build_rebar_model(
        rebars=build_rebar_specs_mm(x_values_mm, z_values_mm, radius_mm),
        geometry_mode=geometry_mode,
        subcell_samples=subcell_samples,
    )


def radii_for_candidate(n_rebars, truth_radius_mm, candidate_radius_mm, sweep_rebar_index=-1):
    """Return per-rebar radii for common or one-at-a-time radius sweeps."""
    if n_rebars <= 0:
        raise ValueError("n_rebars must be positive")
    if sweep_rebar_index < -1 or sweep_rebar_index >= n_rebars:
        raise ValueError("sweep_rebar_index must be -1 or a valid zero-based rebar index")
    if sweep_rebar_index == -1:
        return [float(candidate_radius_mm)] * n_rebars
    radii = [float(truth_radius_mm)] * n_rebars
    radii[int(sweep_rebar_index)] = float(candidate_radius_mm)
    return radii


def build_variable_radius_model(
        x_values_mm,
        z_values_mm,
        radii_mm,
        geometry_mode="hard",
        subcell_samples=5):
    """Build a fixed-position multi-rebar model with per-rebar radii."""
    if len(x_values_mm) != len(z_values_mm) or len(x_values_mm) != len(radii_mm):
        raise ValueError("x, z, and radius rebar lists must have the same length")
    rebars = [
        (float(z_mm) / 1000.0, float(x_mm) / 1000.0, float(radius_mm) / 1000.0)
        for x_mm, z_mm, radius_mm in zip(x_values_mm, z_values_mm, radii_mm)
    ]
    return build_rebar_model(
        rebars=rebars,
        geometry_mode=geometry_mode,
        subcell_samples=subcell_samples,
    )


def build_scan_positions(scan_step, n_sources):
    """Build scan positions compatible with the single-rebar GPU CPML engine."""
    scan_x_all = np.arange(cfg.SCAN_START_X, cfg.SCAN_END_X + 1e-10, scan_step)
    if n_sources is not None and n_sources < len(scan_x_all):
        idx = np.linspace(0, len(scan_x_all) - 1, n_sources, dtype=int)
        idx = np.unique(idx)
        scan_x = scan_x_all[idx]
    else:
        scan_x = scan_x_all

    src_iz = pos_to_index(cfg.TX_Z, cfg.DZ, cfg.NPML)
    rec_iz = pos_to_index(cfg.RX_Z, cfg.DZ, cfg.NPML)
    positions = []
    for x_pos in scan_x:
        src_ix = pos_to_index(x_pos, cfg.DX, cfg.NPML)
        rec_ix = pos_to_index(x_pos + cfg.TX_RX_OFFSET, cfg.DX, cfg.NPML)
        rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)
        positions.append((src_iz, src_ix, rec_iz, rec_ix))
    return positions, scan_x


def make_simulator(model, backend):
    if backend == "cpu":
        return FDTDSimulator(model)
    if backend != "gpu-cpml":
        raise ValueError(f"Unsupported backend: {backend}")
    from gpu.fdtd_gpu_v2 import FDTDSimulatorGPU_v2

    return FDTDSimulatorGPU_v2(model, cfg)


def simulate_bscan(model, wavelet, scan_positions, backend):
    """Simulate a B-scan using GPU batch execution when available."""
    sim = make_simulator(model, backend)
    if backend == "gpu-cpml" and hasattr(sim, "run_batch"):
        return sim.run_batch(wavelet, scan_positions)["bscan"]

    bscan = np.zeros((cfg.NT, len(scan_positions)), dtype=np.float64)
    for i, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(scan_positions):
        result = sim.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)
        bscan[:, i] = result["trace"]
    return bscan


def build_observed_cases(
        true_model,
        time_values,
        frequency_hz,
        scan_positions,
        backend,
        cases):
    """Build observed multi-rebar B-scans for each source/noise case."""
    observed_by_case = {}
    metadata_by_case = {}
    for case in cases:
        wavelet = observed_wavelet(
            time_values,
            frequency_hz,
            frequency_scale=case["frequency_scale"],
            time_shift_ps=case["time_shift_ps"],
            amplitude_scale=case["amplitude_scale"],
        )
        clean = simulate_bscan(true_model, wavelet, scan_positions, backend)
        observed, noise_stats = _add_noise(clean, case["noise_fraction"], case["noise_seed"])
        observed_by_case[case["label"]] = observed
        metadata_by_case[case["label"]] = {
            **case,
            "noise": noise_stats,
        }
    return observed_by_case, metadata_by_case


def rank_case(candidates, case_label, top_k=None):
    """Rank candidate common radii for one observed case."""
    ranked = []
    for candidate in candidates:
        result = candidate["case_results"][case_label]
        ranked.append({
            "misfit": float(result["misfit"]),
            "params": dict(candidate["params"]),
            "source_profile": dict(result["source_profile"]),
        })
    ranked.sort(key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates, case_label):
    """Return common-radius objective curve for one case."""
    curve = []
    for candidate in candidates:
        result = candidate["case_results"][case_label]
        curve.append({
            "radius_mm": candidate["params"]["radius_mm"],
            "misfit": float(result["misfit"]),
            "params": dict(candidate["params"]),
            "source_profile": dict(result["source_profile"]),
        })
    return sorted(curve, key=lambda item: item["radius_mm"])


def evaluate_common_radius_grid(
        observed_by_case,
        x_values_mm,
        z_values_mm,
        truth_radius_mm,
        radius_values_mm,
        frequency_hz,
        modeled_frequency_scales,
        time_shift_values_s,
        scan_positions,
        time_values,
        mute,
        backend,
        geometry_mode="hard",
        subcell_samples=5,
        sweep_rebar_index=-1,
        fit_amplitude=True,
        progress_every=5):
    """Evaluate a common-radius multi-rebar grid with source profiling."""
    observed_objective_by_case = {
        label: np.asarray(observed, dtype=np.float64)
        for label, observed in observed_by_case.items()
    }
    candidates = []
    started = time.time()
    for count, radius_mm in enumerate(radius_values_mm, start=1):
        radii_mm = radii_for_candidate(
            len(x_values_mm),
            truth_radius_mm,
            radius_mm,
            sweep_rebar_index=sweep_rebar_index,
        )
        model = build_variable_radius_model(
            x_values_mm,
            z_values_mm,
            radii_mm,
            geometry_mode=geometry_mode,
            subcell_samples=subcell_samples,
        )
        synthetic_by_scale = {}
        for scale in modeled_frequency_scales:
            wavelet = ricker_wavelet(time_values, frequency_hz * float(scale))
            synthetic_by_scale[float(scale)] = simulate_bscan(
                model,
                wavelet,
                scan_positions,
                backend,
            )

        case_results = {}
        for label, observed in observed_objective_by_case.items():
            profile = source_profiled_ls(
                observed,
                synthetic_by_scale,
                mute,
                cfg.DT,
                time_shift_values_s=time_shift_values_s,
                fit_amplitude=fit_amplitude,
            )
            case_results[label] = {
                "misfit": float(profile.misfit),
                "source_profile": profile.as_dict(),
            }
        candidates.append({
            "params": {
                "radius_mm": float(radius_mm),
                "common_radius_mm": float(radius_mm),
                "swept_radius_mm": float(radius_mm),
                "sweep_rebar_index": int(sweep_rebar_index),
                "radii_mm": [float(value) for value in radii_mm],
            },
            "case_results": case_results,
        })
        if progress_every and (count == 1 or count % int(progress_every) == 0):
            elapsed = time.time() - started
            print(f"  Multi-rebar common-radius profile: {count}/{len(radius_values_mm)}, elapsed={elapsed:.1f} s")
    return candidates


def write_candidate_csv(path, candidates, case_labels):
    fieldnames = [
        "case_label",
        "misfit",
        "common_radius_mm",
        "sweep_rebar_index",
        "radii_mm",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            for label in case_labels:
                result = candidate["case_results"][label]
                profile = result["source_profile"]
                writer.writerow({
                    "case_label": label,
                    "misfit": result["misfit"],
                    "common_radius_mm": candidate["params"]["common_radius_mm"],
                    "sweep_rebar_index": candidate["params"]["sweep_rebar_index"],
                    "radii_mm": json.dumps(candidate["params"]["radii_mm"]),
                    "source_frequency_scale": profile["frequency_scale"],
                    "source_time_shift_ps": profile["time_shift_ps"],
                    "source_amplitude_scale": profile["amplitude_scale"],
                })


def write_case_summary_csv(path, results):
    fieldnames = [
        "case_label",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "best_misfit",
        "best_source_frequency_scale",
        "best_source_time_shift_ps",
        "best_source_amplitude_scale",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for label, result in results.items():
            best = result["top_candidates"][0]
            profile = best["source_profile"]
            margin = result["margin"]
            writer.writerow({
                "case_label": label,
                "best_radius_mm": margin["best_radius_mm"],
                "next_radius_mm": margin["next_radius_mm"],
                "radius_margin_abs": margin["radius_margin_abs"],
                "best_misfit": margin["best_radius_misfit"],
                "best_source_frequency_scale": profile["frequency_scale"],
                "best_source_time_shift_ps": profile["time_shift_ps"],
                "best_source_amplitude_scale": profile["amplitude_scale"],
            })


def plot_radius_profiles(results, save_path):
    fig, ax = plt.subplots(figsize=(9.4, 5.3), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radii = [item["radius_mm"] for item in curve]
        values = [item["misfit"] for item in curve]
        ax.plot(radii, values, marker="o", linewidth=1.6, markersize=3.8, label=label)
    ax.set_title("Multi-Rebar Radius Profile")
    ax.set_xlabel("Swept radius [mm]")
    ax.set_ylabel("Source-profiled objective")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--rebar-x-values-mm", type=parse_values_mm, default=default_rebar_x_values_mm())
    parser.add_argument("--rebar-z-values-mm", type=parse_values_mm, default=default_rebar_z_values_mm())
    parser.add_argument("--truth-radius-mm", type=float, default=cfg.REBAR_RADIUS * 1000.0)
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument(
        "--sweep-rebar-index",
        type=int,
        default=-1,
        help="Zero-based rebar index to sweep; -1 sweeps a common radius for all rebars",
    )
    parser.add_argument("--replication-cases", type=parse_replication_cases, default=parse_replication_cases(DEFAULT_CASES))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("0.9,1.0,1.1"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("-80,-50,-25,0,25,50,80"))
    parser.set_defaults(fit_amplitude=True)
    parser.add_argument("--no-fit-amplitude", dest="fit_amplitude", action="store_false")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--progress-every", type=int, default=5)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--run-name", default="multi_rebar_common_radius_profile")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    if len(args.rebar_x_values_mm) != len(args.rebar_z_values_mm):
        raise ValueError("--rebar-x-values-mm and --rebar-z-values-mm must have the same length")
    radii_for_candidate(
        len(args.rebar_x_values_mm),
        args.truth_radius_mm,
        args.truth_radius_mm,
        sweep_rebar_index=args.sweep_rebar_index,
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
    scan_positions, scan_x = build_scan_positions(cfg.INVERSION_SCAN_STEP, args.sources)
    true_model = build_common_radius_model(
        args.rebar_x_values_mm,
        args.rebar_z_values_mm,
        args.truth_radius_mm,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    observed_by_case, case_metadata = build_observed_cases(
        true_model,
        time_values,
        frequency_hz,
        scan_positions,
        args.backend,
        args.replication_cases,
    )

    started = time.time()
    candidates = evaluate_common_radius_grid(
        observed_by_case,
        args.rebar_x_values_mm,
        args.rebar_z_values_mm,
        args.truth_radius_mm,
        args.radius_values_mm,
        frequency_hz,
        args.source_frequency_scales,
        [value * 1e-12 for value in args.source_time_shift_ps_values],
        scan_positions,
        time_values,
        mute,
        args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        sweep_rebar_index=args.sweep_rebar_index,
        fit_amplitude=args.fit_amplitude,
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started

    case_labels = [case["label"] for case in args.replication_cases]
    results = {}
    for label in case_labels:
        ranked = rank_case(candidates, label)
        results[label] = {
            "margin": radius_margin_from_ranked(ranked),
            "top_candidates": ranked[:args.top_k],
            "best_curve_by_radius": best_curve_by_radius(candidates, label),
        }

    candidate_csv = os.path.join(data_dir, "multi_rebar_common_radius_candidates.csv")
    case_summary_csv = os.path.join(data_dir, "multi_rebar_common_radius_case_summary.csv")
    plot_path = os.path.join(figures_dir, "multi_rebar_common_radius_profiles.png")
    write_candidate_csv(candidate_csv, candidates, case_labels)
    write_case_summary_csv(case_summary_csv, results)
    plot_radius_profiles(results, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "rebar_x_values_mm": args.rebar_x_values_mm,
        "rebar_z_values_mm": args.rebar_z_values_mm,
        "truth_radius_mm": args.truth_radius_mm,
        "sweep_rebar_index": args.sweep_rebar_index,
        "radius_values_mm": args.radius_values_mm,
        "replication_cases": args.replication_cases,
        "case_metadata": case_metadata,
        "source_profile_grid": {
            "frequency_scales": args.source_frequency_scales,
            "time_shift_ps_values": args.source_time_shift_ps_values,
            "fit_amplitude": bool(args.fit_amplitude),
        },
        "elapsed_time_s": float(elapsed),
        "candidate_count": len(candidates),
        "case_count": len(case_labels),
        "results": results,
        "paths": {
            "candidate_csv": candidate_csv,
            "case_summary_csv": case_summary_csv,
            "radius_profiles_plot": plot_path,
        },
    }
    summary_path = os.path.join(data_dir, "multi_rebar_common_radius_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "multi_rebar_common_radius_profile",
        {
            "summary_path": summary_path,
            "candidate_csv": candidate_csv,
            "case_summary_csv": case_summary_csv,
            "radius_profiles_plot": plot_path,
        },
    )
    for label, result in results.items():
        margin = result["margin"]
        best = result["top_candidates"][0]
        profile = best["source_profile"]
        print(
            f"{label}: best r={margin['best_radius_mm']} mm, "
            f"next r={margin['next_radius_mm']} mm, "
            f"margin={margin['radius_margin_abs']}, "
            f"source=({profile['frequency_scale']}, {profile['time_shift_ps']} ps, "
            f"{profile['amplitude_scale']})"
        )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
