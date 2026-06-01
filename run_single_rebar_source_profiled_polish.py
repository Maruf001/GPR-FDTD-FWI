#!/usr/bin/env python3
"""Run source-profiled local radius polish for one rebar."""

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
from inversion.frequency_weighting import (  # noqa: E402
    frequency_key,
    parse_frequency_list_ghz,
    radius_margin_from_ranked,
)
from inversion.radius_confidence import radius_interval_from_curve  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    build_model_from_single_params,
)
from inversion.source_profile import (  # noqa: E402
    best_amplitude_scale,
    normalized_ls_misfit,
    shift_traces_zero_fill,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def _params_from_mm(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=float(x_mm) / 1000.0,
        z=float(z_mm) / 1000.0,
        radius=float(radius_mm) / 1000.0,
    )


def resolve_initial_params_mm(
        truth_x_mm,
        truth_z_mm,
        truth_radius_mm,
        initial_x_mm=None,
        initial_z_mm=None,
        initial_radius_mm=None):
    """Resolve a display/engine initial guess from truth and optional values."""
    x_mm = truth_x_mm if initial_x_mm is None else initial_x_mm
    z_mm = truth_z_mm if initial_z_mm is None else initial_z_mm
    radius_mm = (
        float(truth_radius_mm) + 0.8
        if initial_radius_mm is None
        else initial_radius_mm
    )
    return _params_from_mm(x_mm, z_mm, radius_mm)


def _add_noise(data, fraction, seed):
    if fraction <= 0.0:
        return data.copy(), {
            "rms_fraction": 0.0,
            "seed": int(seed),
            "clean_rms": float(np.sqrt(np.mean(data ** 2))),
            "noise_std": 0.0,
            "actual_noise_rms": 0.0,
        }
    rng = np.random.default_rng(seed)
    clean_rms = float(np.sqrt(np.mean(data ** 2)))
    noise_std = float(fraction) * clean_rms
    noise = rng.normal(loc=0.0, scale=noise_std, size=data.shape)
    return data + noise, {
        "rms_fraction": float(fraction),
        "seed": int(seed),
        "clean_rms": clean_rms,
        "noise_std": float(noise_std),
        "actual_noise_rms": float(np.sqrt(np.mean(noise ** 2))),
    }


def _add_noise_by_frequency(clean_by_frequency, fraction, seed):
    """Add deterministic observed noise independently to each frequency."""
    observed = {}
    stats = {}
    for index, frequency_hz in enumerate(sorted(clean_by_frequency)):
        observed[frequency_hz], stats[frequency_key(frequency_hz)] = _add_noise(
            clean_by_frequency[frequency_hz],
            fraction,
            int(seed) + index,
        )
    return observed, stats


def observed_wavelet(time, frequency_hz, frequency_scale=1.0, time_shift_ps=0.0, amplitude_scale=1.0):
    """Build a controlled observed source wavelet."""
    wavelet = ricker_wavelet(time, frequency_hz * float(frequency_scale))
    if time_shift_ps != 0.0:
        wavelet = shift_traces_zero_fill(wavelet, cfg.DT, float(time_shift_ps) * 1e-12)
    return float(amplitude_scale) * wavelet


def parse_frequency_weights(text, frequencies_hz):
    """Parse optional comma-separated weights for a frequency list."""
    frequencies = list(frequencies_hz)
    if text is None:
        return {frequency: 1.0 for frequency in frequencies}
    weights = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if len(weights) != len(frequencies):
        raise ValueError("frequency weight count must match frequencies")
    if any(weight < 0.0 for weight in weights) or not any(weight > 0.0 for weight in weights):
        raise ValueError("frequency weights must be non-negative with at least one positive value")
    return {
        frequency: float(weight)
        for frequency, weight in zip(frequencies, weights)
    }


def source_profiled_multifrequency_ls(
        observed_by_frequency,
        synthetic_by_frequency_scale,
        mute,
        dt,
        frequency_weights=None,
        time_shift_values_s=(0.0,),
        fit_amplitude=True):
    """Return best weighted source profile over multiple base frequencies."""
    if not observed_by_frequency:
        raise ValueError("observed_by_frequency must be non-empty")
    frequencies = list(observed_by_frequency)
    weights = frequency_weights or {frequency: 1.0 for frequency in frequencies}
    weight_sum = float(sum(weights.get(frequency, 0.0) for frequency in frequencies))
    if weight_sum <= 0.0:
        raise ValueError("at least one frequency weight must be positive")
    scale_sets = [
        set(synthetic_by_frequency_scale.get(frequency, {}).keys())
        for frequency in frequencies
    ]
    if not scale_sets or any(not scale_set for scale_set in scale_sets):
        raise ValueError("synthetic_by_frequency_scale must contain all frequencies and scales")
    shared_scales = sorted(set.intersection(*scale_sets))
    if not shared_scales:
        raise ValueError("synthetic frequencies do not share any source scales")

    shifts = list(time_shift_values_s or [0.0])
    best = None
    for scale in shared_scales:
        for shift_s in shifts:
            weighted_misfit = 0.0
            misfit_by_frequency = {}
            amplitude_by_frequency = {}
            for frequency in frequencies:
                observed = observed_by_frequency[frequency]
                synthetic = synthetic_by_frequency_scale[frequency][scale]
                shifted = (
                    shift_traces_zero_fill(synthetic, dt, shift_s)
                    if shift_s != 0.0
                    else synthetic
                )
                amplitude_scale = (
                    best_amplitude_scale(observed, shifted, mute)
                    if fit_amplitude
                    else 1.0
                )
                misfit = normalized_ls_misfit(
                    observed,
                    shifted,
                    mute,
                    amplitude_scale=amplitude_scale,
                )
                key = frequency_key(frequency)
                misfit_by_frequency[key] = float(misfit)
                amplitude_by_frequency[key] = float(amplitude_scale)
                weighted_misfit += float(weights.get(frequency, 0.0)) * float(misfit)

            result = {
                "misfit": float(weighted_misfit / weight_sum),
                "frequency_scale": float(scale),
                "time_shift_s": float(shift_s),
                "time_shift_ps": float(shift_s * 1e12),
                "amplitude_scale": float(np.mean(list(amplitude_by_frequency.values()))),
                "amplitude_scale_by_frequency": amplitude_by_frequency,
                "misfit_by_frequency": misfit_by_frequency,
            }
            if best is None or result["misfit"] < best["misfit"]:
                best = result
    return best


def rank_candidates(candidates, top_k=None):
    ranked = sorted(candidates, key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates):
    """Return the best source-profiled candidate at each radius."""
    best = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        current = best.get(radius)
        if current is None or candidate["misfit"] < current["misfit"]:
            best[radius] = candidate
    return [best[radius] for radius in sorted(best)]


def profile_frequency_keys(candidates):
    """Return frequency keys present in source-profiled diagnostic fields."""
    keys = []
    for candidate in candidates:
        profile = candidate.get("source_profile", {})
        for mapping_name in ("misfit_by_frequency", "amplitude_scale_by_frequency"):
            for key in profile.get(mapping_name, {}):
                if key not in keys:
                    keys.append(key)
    return keys


def format_metric(value):
    """Format a metric for compact plain-language notes."""
    if value is None:
        return "not available"
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def format_mm_value(value, min_decimals=1, max_decimals=3):
    """Format millimeter values without rounding away fine radius steps."""
    text = f"{float(value):.{int(max_decimals)}f}".rstrip("0").rstrip(".")
    if "." not in text and int(min_decimals) > 0:
        text += "." + ("0" * int(min_decimals))
    return text


def evaluate_source_profiled_grid(
        engine,
        observed_by_frequency,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        modeled_frequency_scales,
        time_shift_values_s,
        frequency_weights=None,
        fit_amplitude=True,
        progress_every=10):
    """Evaluate local x/z/r grid with source nuisance profiling."""
    observed_objective_by_frequency = {
        frequency: engine._apply_objective_filter(observed_by_frequency[frequency])
        for frequency in engine.frequencies
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
                synthetic_by_frequency_scale = {}
                for frequency in engine.frequencies:
                    synthetic_by_frequency_scale[frequency] = {}
                    for scale in modeled_frequency_scales:
                        wavelet = (
                            engine.wavelets[frequency]
                            if np.isclose(scale, 1.0, rtol=0.0, atol=1e-12)
                            else ricker_wavelet(engine.time, frequency * float(scale))
                        )
                        synthetic = engine._simulate_bscan(model, wavelet)
                        synthetic_by_frequency_scale[frequency][float(scale)] = (
                            engine._apply_objective_filter(synthetic)
                        )

                profile = source_profiled_multifrequency_ls(
                    observed_objective_by_frequency,
                    synthetic_by_frequency_scale,
                    engine.mute,
                    cfg.DT,
                    frequency_weights=frequency_weights,
                    time_shift_values_s=time_shift_values_s,
                    fit_amplitude=fit_amplitude,
                )
                candidates.append({
                    "misfit": float(profile["misfit"]),
                    "params": params.as_mm(),
                    "source_profile": profile,
                })
                count += 1
                if progress_every and (count == 1 or count % int(progress_every) == 0):
                    elapsed = time.time() - started
                    print(f"  Source-profiled polish: {count}/{total}, elapsed={elapsed:.1f} s")
    return candidates


def write_candidate_csv(path, candidates):
    """Write source-profiled candidates to CSV."""
    frequency_keys = profile_frequency_keys(candidates)
    fieldnames = [
        "misfit",
        "x_mm",
        "z_mm",
        "radius_mm",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
    ]
    fieldnames.extend(f"frequency_misfit_{key}" for key in frequency_keys)
    fieldnames.extend(f"frequency_amplitude_scale_{key}" for key in frequency_keys)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        for candidate in candidates:
            profile = candidate["source_profile"]
            row = {
                "misfit": candidate["misfit"],
                "x_mm": candidate["params"]["x_mm"],
                "z_mm": candidate["params"]["z_mm"],
                "radius_mm": candidate["params"]["radius_mm"],
                "source_frequency_scale": profile["frequency_scale"],
                "source_time_shift_ps": profile["time_shift_ps"],
                "source_amplitude_scale": profile["amplitude_scale"],
            }
            for key in frequency_keys:
                row[f"frequency_misfit_{key}"] = profile.get("misfit_by_frequency", {}).get(key, "")
                row[f"frequency_amplitude_scale_{key}"] = (
                    profile.get("amplitude_scale_by_frequency", {}).get(key, "")
                )
            writer.writerow(row)


def plot_radius_profile(candidates, save_path):
    """Plot best source-profiled objective by radius."""
    curve = best_curve_by_radius(candidates)
    fig, ax = plt.subplots(figsize=(8.8, 5.1), constrained_layout=True)
    radii = [item["params"]["radius_mm"] for item in curve]
    values = [item["misfit"] for item in curve]
    ax.plot(radii, values, marker="o", linewidth=1.8, markersize=4.5)
    if curve:
        best = min(curve, key=lambda item: item["misfit"])
        ax.scatter(
            [best["params"]["radius_mm"]],
            [best["misfit"]],
            s=54,
            edgecolors="black",
            linewidths=0.8,
            zorder=4,
        )
    ax.set_title("Source-Profiled Radius Polish")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Best objective over x/z/source profile")
    ax.grid(True, alpha=0.25)
    save_validated_figure(fig, save_path)
    plt.close(fig)


def plot_frequency_radius_profiles(candidates, save_path):
    """Plot per-frequency terms along the combined-best radius curve."""
    curve = best_curve_by_radius(candidates)
    frequency_keys = profile_frequency_keys(curve)
    if len(frequency_keys) <= 1:
        return None

    radii = [item["params"]["radius_mm"] for item in curve]
    fig, ax = plt.subplots(figsize=(8.8, 5.1), constrained_layout=True)
    ax.plot(
        radii,
        [item["misfit"] for item in curve],
        color="black",
        marker="o",
        linewidth=2.0,
        markersize=4.5,
        label="weighted combined objective",
    )
    for key in frequency_keys:
        values = [
            item["source_profile"].get("misfit_by_frequency", {}).get(key, np.nan)
            for item in curve
        ]
        ax.plot(
            radii,
            values,
            marker="o",
            linewidth=1.5,
            markersize=3.8,
            label=f"{key} term",
        )

    ax.set_title("Per-Frequency Terms On Combined-Best Radius Curve")
    ax.set_xlabel("Radius [mm]")
    ax.set_ylabel("Normalized least-squares objective")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8, frameon=True)
    save_validated_figure(fig, save_path)
    plt.close(fig)
    return save_path


def write_figure_notes(figures_dir, summary):
    """Write plain-language notes for source-profiled polish figures."""
    figures_path = os.path.join(figures_dir, "FIGURE_NOTES.md")
    best = summary["top_candidates"][0] if summary.get("top_candidates") else None
    margin = summary.get("margin", {})
    source_grid = summary.get("source_profile_grid", {})
    frequency_plot = summary.get("paths", {}).get("frequency_radius_profile_plot")
    best_text = "No top candidate was recorded."
    if best is not None:
        best_text = (
            "Main result: the best candidate is "
            f"x={format_mm_value(best['params']['x_mm'])} mm, "
            f"z={format_mm_value(best['params']['z_mm'])} mm, "
            f"r={format_mm_value(best['params']['radius_mm'])} mm. "
            "The best-radius margin is "
            f"{format_metric(margin.get('radius_margin_abs'))}."
        )

    sections = [
        f"""# Figure Notes

## 1. `source_profiled_radius_profile.png` - radius decision curve

This plot shows the best full-waveform inversion objective value found for each
tested rebar radius. FWI means full-waveform inversion: the code simulates
radar traces for each candidate and compares them with the observed traces.
Lower objective values mean better waveform agreement.

"Source-profiled" means the comparison also tests small source-wavelet changes
instead of forcing geometry or radius to explain source uncertainty. The source
grid used frequency scales `{source_grid.get('frequency_scales')}`, time shifts
in picoseconds `{source_grid.get('time_shift_ps_values')}`, and fitted
amplitude `{source_grid.get('fit_amplitude')}`.

{best_text} A larger radius margin is a clearer radius decision; a zero or
tiny margin means the radius should be reported as an interval rather than as a
high-confidence single size.
""",
    ]
    if frequency_plot:
        sections.append(
            """## 2. `source_profiled_frequency_radius_profile.png` - frequency-term decomposition

This plot is shown only for multifrequency runs. It uses the same candidate
chosen by the combined objective at each radius, then draws the contribution
from each base frequency. It is a diagnostic decomposition, not a separate
optimizer.

Use this figure to decide whether one frequency is carrying useful radius
separation or only adding cost and mismatch. If the per-frequency curves do not
separate the correct radius better than the combined curve, another full
multifrequency grid is not justified without a better weighting rule.
"""
        )
    with open(figures_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(sections))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument(
        "--frequencies-ghz",
        default=None,
        help="Comma-separated base frequencies for multifrequency objective. Overrides --frequency-ghz.",
    )
    parser.add_argument(
        "--frequency-weights",
        default=None,
        help="Optional comma-separated objective weights matching --frequencies-ghz.",
    )
    parser.add_argument("--truth-x-mm", type=float, default=250.0)
    parser.add_argument("--truth-z-mm", type=float, default=90.0)
    parser.add_argument("--truth-radius-mm", type=float, default=6.0)
    parser.add_argument("--initial-x-mm", type=float, default=None)
    parser.add_argument("--initial-z-mm", type=float, default=None)
    parser.add_argument("--initial-radius-mm", type=float, default=None)
    parser.add_argument("--x-values-mm", type=parse_values_mm, default=parse_values_mm("250.0"))
    parser.add_argument("--z-values-mm", type=parse_values_mm, default=parse_values_mm("90.0,90.5,91.0,91.5"))
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5.4:7.8:0.2"))
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("1.0"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("0"))
    parser.add_argument("--fit-amplitude", action="store_true")
    parser.add_argument("--observed-frequency-scale", type=float, default=1.0)
    parser.add_argument("--observed-time-shift-ps", type=float, default=0.0)
    parser.add_argument("--observed-amplitude-scale", type=float, default=1.0)
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--run-name", default="single_rebar_source_profiled_polish")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    figures_dir = os.path.join(outdir, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequencies_hz = (
        parse_frequency_list_ghz(args.frequencies_ghz)
        if args.frequencies_ghz is not None
        else [args.frequency_ghz * 1e9]
    )
    frequency_weights = parse_frequency_weights(args.frequency_weights, frequencies_hz)
    truth_params = _params_from_mm(args.truth_x_mm, args.truth_z_mm, args.truth_radius_mm)
    initial_params = resolve_initial_params_mm(
        args.truth_x_mm,
        args.truth_z_mm,
        args.truth_radius_mm,
        initial_x_mm=args.initial_x_mm,
        initial_z_mm=args.initial_z_mm,
        initial_radius_mm=args.initial_radius_mm,
    )
    engine = SingleRebarInversionEngine(
        true_params=truth_params,
        initial_params=initial_params,
        frequencies=tuple(frequencies_hz),
        n_sources=args.sources,
        backend=args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    observed_clean_by_frequency = {}
    for frequency_hz in engine.frequencies:
        obs_wavelet = observed_wavelet(
            engine.time,
            frequency_hz,
            frequency_scale=args.observed_frequency_scale,
            time_shift_ps=args.observed_time_shift_ps,
            amplitude_scale=args.observed_amplitude_scale,
        )
        observed_clean_by_frequency[frequency_hz] = engine._simulate_bscan(
            engine.true_model,
            obs_wavelet,
        )
    observed_by_frequency, noise_stats = _add_noise_by_frequency(
        observed_clean_by_frequency,
        args.observed_noise_rms_fraction,
        args.noise_seed,
    )

    started = time.time()
    candidates = evaluate_source_profiled_grid(
        engine,
        observed_by_frequency,
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        args.source_frequency_scales,
        [value * 1e-12 for value in args.source_time_shift_ps_values],
        frequency_weights=frequency_weights,
        fit_amplitude=args.fit_amplitude,
        progress_every=args.progress_every,
    )
    elapsed = time.time() - started
    ranked = rank_candidates(candidates)
    top_candidates = ranked[:args.top_k]
    margin = radius_margin_from_ranked(ranked)
    radius_curve = best_curve_by_radius(candidates)
    radius_ambiguity = {
        "exact_tie": radius_interval_from_curve(
            radius_curve,
            abs_tolerance=1e-12,
            rel_tolerance=0.0,
        ),
        "weak_interval": radius_interval_from_curve(
            radius_curve,
            abs_tolerance=1e-3,
            rel_tolerance=5e-3,
        ),
    }

    csv_path = os.path.join(data_dir, "source_profiled_polish_candidates.csv")
    plot_path = os.path.join(figures_dir, "source_profiled_radius_profile.png")
    frequency_plot_path = os.path.join(figures_dir, "source_profiled_frequency_radius_profile.png")
    write_candidate_csv(csv_path, candidates)
    plot_radius_profile(candidates, plot_path)
    saved_frequency_plot = plot_frequency_radius_profiles(candidates, frequency_plot_path)

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "frequency_ghz": args.frequency_ghz,
        "frequencies_ghz": [float(frequency / 1e9) for frequency in engine.frequencies],
        "frequency_weights": {
            frequency_key(frequency): float(frequency_weights[frequency])
            for frequency in engine.frequencies
        },
        "truth_params": truth_params.as_mm(),
        "initial_params": initial_params.as_mm(),
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "source_profile_grid": {
            "frequency_scales": args.source_frequency_scales,
            "time_shift_ps_values": args.source_time_shift_ps_values,
            "fit_amplitude": bool(args.fit_amplitude),
        },
        "observed_source": {
            "frequency_scale": float(args.observed_frequency_scale),
            "time_shift_ps": float(args.observed_time_shift_ps),
            "amplitude_scale": float(args.observed_amplitude_scale),
            "noise": noise_stats,
        },
        "geometry_mode": args.geometry_mode,
        "subcell_samples": int(args.subcell_samples),
        "elapsed_time_s": float(elapsed),
        "candidate_count": len(candidates),
        "margin": margin,
        "radius_ambiguity": radius_ambiguity,
        "top_candidates": top_candidates,
        "best_curve_by_radius": radius_curve,
        "paths": {
            "candidate_csv": csv_path,
            "radius_profile_plot": plot_path,
            "frequency_radius_profile_plot": saved_frequency_plot,
        },
    }
    summary_path = os.path.join(data_dir, "source_profiled_polish_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_figure_notes(figures_dir, summary)

    write_run_manifest(
        outdir,
        "single_rebar_source_profiled_polish",
        {
            "summary_path": summary_path,
            "candidate_csv": csv_path,
            "radius_profile_plot": plot_path,
            "frequency_radius_profile_plot": saved_frequency_plot,
        },
    )
    print(
        f"Best r={margin['best_radius_mm']} mm, "
        f"next r={margin['next_radius_mm']} mm, "
        f"margin={margin['radius_margin_abs']}"
    )
    if top_candidates:
        print(f"Best source profile: {top_candidates[0]['source_profile']}")
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
