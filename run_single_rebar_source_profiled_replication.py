#!/usr/bin/env python3
"""Run a compact source-profiled radius replication matrix."""

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
from core.source import ricker_wavelet  # noqa: E402
from inversion.frequency_weighting import radius_margin_from_ranked  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    build_model_from_single_params,
    default_single_rebar_truth,
)
from inversion.source_profile import source_profiled_ls  # noqa: E402
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import (  # noqa: E402
    _add_noise,
    _params_from_mm,
    observed_wavelet,
)
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_REPLICATION_CASES = (
    "nominal:1.0,0.0,1.0,0.0,13|"
    "noise05_seed13:1.0,0.0,1.0,0.05,13|"
    "noise10_seed13:1.0,0.0,1.0,0.10,13|"
    "source_mismatch:1.1,-50.0,1.1,0.0,13|"
    "source_mismatch_noise05_seed13:1.1,-50.0,1.1,0.05,13"
)


def parse_replication_cases(text):
    """
    Parse source-profiled replication cases.

    Format:

    ```text
    label:frequency_scale,time_shift_ps,amplitude_scale,noise_fraction,noise_seed|...
    ```
    """
    cases = []
    labels = set()
    for item in str(text).split("|"):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise argparse.ArgumentTypeError(
                "each replication case must be label:freq_scale,time_shift_ps,amp_scale,noise_fraction,seed"
            )
        label, values_text = item.split(":", 1)
        label = label.strip()
        if not label or label in labels:
            raise argparse.ArgumentTypeError("replication case labels must be non-empty and unique")
        parts = [part.strip() for part in values_text.split(",") if part.strip()]
        if len(parts) != 5:
            raise argparse.ArgumentTypeError("replication case requires five values")
        frequency_scale = float(parts[0])
        time_shift_ps = float(parts[1])
        amplitude_scale = float(parts[2])
        noise_fraction = float(parts[3])
        noise_seed = int(parts[4])
        if frequency_scale <= 0.0 or amplitude_scale <= 0.0:
            raise argparse.ArgumentTypeError("frequency and amplitude scales must be positive")
        if noise_fraction < 0.0:
            raise argparse.ArgumentTypeError("noise fraction must be non-negative")
        labels.add(label)
        cases.append({
            "label": label,
            "frequency_scale": float(frequency_scale),
            "time_shift_ps": float(time_shift_ps),
            "amplitude_scale": float(amplitude_scale),
            "noise_fraction": float(noise_fraction),
            "noise_seed": int(noise_seed),
        })
    if not cases:
        raise argparse.ArgumentTypeError("at least one replication case is required")
    return cases


def build_observed_cases(engine, frequency_hz, cases):
    """Build observed B-scans for each replication case."""
    observed_by_case = {}
    metadata_by_case = {}
    for case in cases:
        wavelet = observed_wavelet(
            engine.time,
            frequency_hz,
            frequency_scale=case["frequency_scale"],
            time_shift_ps=case["time_shift_ps"],
            amplitude_scale=case["amplitude_scale"],
        )
        clean = engine._simulate_bscan(engine.true_model, wavelet)
        observed, noise_stats = _add_noise(clean, case["noise_fraction"], case["noise_seed"])
        observed_by_case[case["label"]] = observed
        metadata_by_case[case["label"]] = {
            **case,
            "noise": noise_stats,
        }
    return observed_by_case, metadata_by_case


def rank_case(candidates, case_label, top_k=None):
    """Rank source-profiled candidates for one replication case."""
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
    """Return best source-profiled objective at each radius for one case."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        result = candidate["case_results"][case_label]
        current = best.get(radius)
        if current is None or result["misfit"] < current["misfit"]:
            best[radius] = {
                "radius_mm": radius,
                "misfit": float(result["misfit"]),
                "params": dict(candidate["params"]),
                "source_profile": dict(result["source_profile"]),
            }
    return [best[radius] for radius in sorted(best)]


def evaluate_replication_grid(
        engine,
        observed_by_case,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        modeled_frequency_scales,
        time_shift_values_s,
        fit_amplitude=True,
        progress_every=10):
    """Evaluate one synthetic grid against multiple observed/source cases."""
    frequency = engine.frequencies[0]
    observed_objective_by_case = {
        label: engine._apply_objective_filter(observed)
        for label, observed in observed_by_case.items()
    }
    candidates = []
    total = len(x_values_mm) * len(z_values_mm) * len(radius_values_mm)
    started = time.time()
    count = 0
    for x_mm in x_values_mm:
        for z_mm in z_values_mm:
            for radius_mm in radius_values_mm:
                params = _params_from_mm(x_mm, z_mm, radius_mm)
                model = build_model_from_single_params(
                    params.as_array(),
                    geometry_mode=engine.geometry_mode,
                    subcell_samples=engine.subcell_samples,
                )
                synthetic_by_scale = {}
                for scale in modeled_frequency_scales:
                    wavelet = (
                        engine.wavelets[frequency]
                        if np.isclose(scale, 1.0, rtol=0.0, atol=1e-12)
                        else ricker_wavelet(engine.time, frequency * float(scale))
                    )
                    synthetic = engine._simulate_bscan(model, wavelet)
                    synthetic_by_scale[float(scale)] = engine._apply_objective_filter(synthetic)

                case_results = {}
                for label, observed in observed_objective_by_case.items():
                    profile = source_profiled_ls(
                        observed,
                        synthetic_by_scale,
                        engine.mute,
                        cfg.DT,
                        time_shift_values_s=time_shift_values_s,
                        fit_amplitude=fit_amplitude,
                    )
                    case_results[label] = {
                        "misfit": float(profile.misfit),
                        "source_profile": profile.as_dict(),
                    }
                candidates.append({
                    "params": params.as_mm(),
                    "case_results": case_results,
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Source-profiled replication: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def write_candidate_csv(path, candidates, case_labels):
    """Write one row per candidate and replication case."""
    fieldnames = [
        "case_label",
        "misfit",
        "x_mm",
        "z_mm",
        "radius_mm",
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
                    "x_mm": candidate["params"]["x_mm"],
                    "z_mm": candidate["params"]["z_mm"],
                    "radius_mm": candidate["params"]["radius_mm"],
                    "source_frequency_scale": profile["frequency_scale"],
                    "source_time_shift_ps": profile["time_shift_ps"],
                    "source_amplitude_scale": profile["amplitude_scale"],
                })


def write_case_summary_csv(path, results):
    """Write one summary row per replication case."""
    fieldnames = [
        "case_label",
        "best_radius_mm",
        "next_radius_mm",
        "radius_margin_abs",
        "best_misfit",
        "best_x_mm",
        "best_z_mm",
        "best_source_frequency_scale",
        "best_source_time_shift_ps",
        "best_source_amplitude_scale",
    ]
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for label, result in results.items():
            best = result["top_candidates"][0] if result["top_candidates"] else None
            margin = result["margin"]
            profile = best["source_profile"] if best else {}
            params = best["params"] if best else {}
            writer.writerow({
                "case_label": label,
                "best_radius_mm": margin["best_radius_mm"],
                "next_radius_mm": margin["next_radius_mm"],
                "radius_margin_abs": margin["radius_margin_abs"],
                "best_misfit": margin["best_radius_misfit"],
                "best_x_mm": params.get("x_mm"),
                "best_z_mm": params.get("z_mm"),
                "best_source_frequency_scale": profile.get("frequency_scale"),
                "best_source_time_shift_ps": profile.get("time_shift_ps"),
                "best_source_amplitude_scale": profile.get("amplitude_scale"),
            })


def plot_radius_profiles(results, save_path):
    """Plot best-over-x/z radius profiles for all replication cases."""
    fig, ax = plt.subplots(figsize=(9.6, 5.4), constrained_layout=True)
    for label, result in results.items():
        curve = result["best_curve_by_radius"]
        radii = [item["radius_mm"] for item in curve]
        values = [item["misfit"] for item in curve]
        ax.plot(radii, values, marker="o", linewidth=1.6, markersize=3.8, label=label)
    ax.set_title("Source-Profiled Radius Replication")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Best objective over x/z/source profile")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument(
        "--replication-cases",
        type=parse_replication_cases,
        default=parse_replication_cases(DEFAULT_REPLICATION_CASES),
    )
    parser.add_argument("--x-values-mm", type=parse_values_mm, default=parse_values_mm("250.0"))
    parser.add_argument("--z-values-mm", type=parse_values_mm, default=parse_values_mm("90.0,90.5,91.0,91.5"))
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("0.9,1.0,1.1"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("-80,-50,-25,0,25,50,80"))
    parser.set_defaults(fit_amplitude=True)
    parser.add_argument("--no-fit-amplitude", dest="fit_amplitude", action="store_false")
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--run-name", default="single_rebar_source_profiled_replication")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequency_hz = args.frequency_ghz * 1e9
    engine = SingleRebarInversionEngine(
        true_params=default_single_rebar_truth(),
        initial_params=_params_from_mm(250.0, 90.0, 6.8),
        frequencies=(frequency_hz,),
        n_sources=args.sources,
        backend=args.backend,
    )
    observed_by_case, case_metadata = build_observed_cases(
        engine,
        frequency_hz,
        args.replication_cases,
    )

    started = time.time()
    candidates = evaluate_replication_grid(
        engine,
        observed_by_case,
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        args.source_frequency_scales,
        [value * 1e-12 for value in args.source_time_shift_ps_values],
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

    candidate_csv = os.path.join(data_dir, "source_profiled_replication_candidates.csv")
    case_summary_csv = os.path.join(data_dir, "source_profiled_replication_case_summary.csv")
    plot_path = os.path.join(figures_dir, "source_profiled_replication_radius_profiles.png")
    write_candidate_csv(candidate_csv, candidates, case_labels)
    write_case_summary_csv(case_summary_csv, results)
    plot_radius_profiles(results, plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "replication_cases": args.replication_cases,
        "case_metadata": case_metadata,
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
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
    summary_path = os.path.join(data_dir, "source_profiled_replication_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "single_rebar_source_profiled_replication",
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
