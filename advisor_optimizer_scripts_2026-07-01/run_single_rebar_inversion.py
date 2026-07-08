"""
Entry point: one-rebar geometry inversion.

This is the systematic starter pipeline for estimating one circular rebar's
lateral position, depth, and radius from synthetic GPR B-scan data.

Examples
--------
CPU, quick local run:
    python run_single_rebar_inversion.py --sources 5 --max-evals 25

DGX Spark, CPML-capable GPU run:
    python run_single_rebar_inversion.py --backend gpu-cpml --sources 15

Multi-frequency objective:
    python run_single_rebar_inversion.py --frequencies-ghz 1.4,1.5,1.6
"""
import argparse
import json
import os
import sys

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

# Keep matplotlib cache local on systems where the home directory is read-only.
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    default_single_rebar_initial_guess,
    default_single_rebar_truth,
)


def _parse_frequency_list(text):
    try:
        values = [float(item.strip()) * 1e9 for item in text.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use comma-separated GHz values, e.g. 1.4,1.5,1.6") from exc
    if not values:
        raise argparse.ArgumentTypeError("At least one frequency is required")
    return values


def _parse_weight_list(text):
    try:
        values = [float(item.strip()) for item in text.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use comma-separated numeric weights, e.g. 0.5,1,2") from exc
    if not values:
        raise argparse.ArgumentTypeError("At least one weight is required")
    if any(value < 0.0 for value in values) or not any(value > 0.0 for value in values):
        raise argparse.ArgumentTypeError("Weights must be non-negative with at least one positive value")
    return values


def _parse_mm_bounds(text):
    try:
        values = [float(item.strip()) for item in text.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use min,max in millimeters, e.g. 60,130") from exc
    if len(values) != 2 or values[0] >= values[1]:
        raise argparse.ArgumentTypeError("Bounds must be two increasing values: min,max")
    return values


def _parse_ghz_bandpass(text):
    try:
        values = [float(item.strip()) for item in text.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use low,high in GHz, e.g. 0.2,1.1") from exc
    if len(values) != 2 or values[0] < 0.0 or values[0] >= values[1]:
        raise argparse.ArgumentTypeError("Bandpass must be two increasing GHz values: low,high")
    return tuple(value * 1e9 for value in values)


def _override_grid(grid_step_mm):
    if grid_step_mm is None:
        return
    old_pml_thickness = cfg.NPML * cfg.DX
    step_m = grid_step_mm / 1000.0
    cfg.DX = step_m
    cfg.DZ = step_m
    cfg.DT = cfg.COURANT * cfg.DX / (cfg.C0 * np.sqrt(2.0))
    cfg.NT = int(np.ceil(cfg.T_MAX / cfg.DT))
    cfg.NPML = max(8, int(round(old_pml_thickness / step_m)))
    cfg.NX_INNER = int(np.round(cfg.DOMAIN_X / cfg.DX))
    cfg.NZ_INNER = int(np.round(cfg.DOMAIN_Z / cfg.DZ))
    cfg.NX = cfg.NX_INNER + 2 * cfg.NPML
    cfg.NZ = cfg.NZ_INNER + 2 * cfg.NPML
    print(
        f"Grid override: dx=dz={grid_step_mm:.3f} mm, "
        f"NPML={cfg.NPML}, NX={cfg.NX}, NZ={cfg.NZ}, NT={cfg.NT}"
    )


def _params_from_args(prefix, args, default):
    x_mm = getattr(args, f"{prefix}_x_mm")
    z_mm = getattr(args, f"{prefix}_z_mm")
    radius_mm = getattr(args, f"{prefix}_radius_mm")
    return SingleRebarParams(
        x=(x_mm if x_mm is not None else default.x * 1000.0) / 1000.0,
        z=(z_mm if z_mm is not None else default.z * 1000.0) / 1000.0,
        radius=(radius_mm if radius_mm is not None else default.radius * 1000.0) / 1000.0,
    )


def _grid_polish_config_from_args(args):
    presets = {
        "custom": {
            "x_half_window_mm": 0.0,
            "z_half_window_mm": 1.0,
            "radius_half_window_mm": 1.0,
            "x_step_mm": 1.0,
            "z_step_mm": 0.25,
            "radius_step_mm": 0.1,
            "progress_every": 25,
        },
        "fine": {
            "x_half_window_mm": 0.0,
            "z_half_window_mm": 1.0,
            "radius_half_window_mm": 1.0,
            "x_step_mm": 1.0,
            "z_step_mm": 0.25,
            "radius_step_mm": 0.1,
            "progress_every": 25,
        },
        "coarse": {
            "x_half_window_mm": 0.0,
            "z_half_window_mm": 1.0,
            "radius_half_window_mm": 1.0,
            "x_step_mm": 1.0,
            "z_step_mm": 0.5,
            "radius_step_mm": 0.2,
            "progress_every": 10,
        },
    }
    config = dict(presets[args.grid_polish_preset])
    overrides = {
        "x_half_window_mm": args.polish_x_half_window_mm,
        "z_half_window_mm": args.polish_z_half_window_mm,
        "radius_half_window_mm": args.polish_radius_half_window_mm,
        "x_step_mm": args.polish_x_step_mm,
        "z_step_mm": args.polish_z_step_mm,
        "radius_step_mm": args.polish_radius_step_mm,
        "progress_every": args.polish_progress_every,
    }
    for key, value in overrides.items():
        if value is not None:
            config[key] = value
    config["top_k"] = args.polish_top_k
    config["stop_misfit"] = args.polish_stop_misfit
    config["preset"] = args.grid_polish_preset
    return config


def _write_outputs(results, outdir, backend):
    from visualization.plot_bscan import plot_bscan
    from visualization.plot_inversion import plot_convergence, plot_inversion_comparison

    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "figures"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "data"), exist_ok=True)

    frequencies = results["frequencies"]
    obs_stack = np.stack([results["d_obs_by_frequency"][f] for f in frequencies])
    obs_clean_stack = np.stack([results["d_obs_clean_by_frequency"][f] for f in frequencies])
    syn_stack = np.stack([results["d_syn_final_by_frequency"][f] for f in frequencies])

    np.savez(
        os.path.join(outdir, "data", "single_rebar_results.npz"),
        initial_epsr=results["initial_epsr"],
        inverted_epsr=results["inverted_epsr"],
        true_epsr=results["true_epsr"],
        observed_bscans=obs_stack,
        observed_clean_bscans=obs_clean_stack,
        synthetic_bscans=syn_stack,
        scan_x=results["scan_x"],
        time=results["time"],
        frequencies=frequencies,
        misfit_history=results["misfit_history"],
        initial_params=results["initial_params"],
        optimal_params=results["optimal_params"],
        true_params=results["true_params"],
    )

    true_x, true_z, true_r = results["true_params"]
    rebar_params = [(true_z, true_x, true_r)]
    plot_inversion_comparison(
        results["initial_epsr"],
        results["inverted_epsr"],
        results["true_epsr"],
        rebar_params=rebar_params,
        save_path=os.path.join(outdir, "figures", "single_rebar_model_comparison.png"),
        show=False,
    )
    plot_convergence(
        results["misfit_history"],
        save_path=os.path.join(outdir, "figures", "single_rebar_convergence.png"),
        show=False,
    )
    plot_bscan(
        results["d_obs"],
        results["scan_x"],
        results["time"],
        title="Observed one-rebar B-scan",
        save_path=os.path.join(outdir, "figures", "single_rebar_observed_bscan.png"),
        show=False,
    )
    plot_bscan(
        results["d_syn_final"],
        results["scan_x"],
        results["time"],
        title="Recovered one-rebar B-scan",
        save_path=os.path.join(outdir, "figures", "single_rebar_recovered_bscan.png"),
        show=False,
    )

    metadata = {
        "backend": backend,
        "elapsed_time_s": results["elapsed_time"],
        "optimizer_elapsed_time_s": results.get("optimizer_elapsed_time"),
        "optimizer": results.get("optimizer", "powell"),
        "geometry_mode": results.get("geometry_mode", "hard"),
        "subcell_samples": results.get("subcell_samples", None),
        "objective_bandpass": results.get("objective_bandpass"),
        "objective_frequency_weights": {
            f"{f / 1e9:.6g}GHz": float(v)
            for f, v in results.get("objective_frequency_weights", {}).items()
        },
        "observed_noise": results.get("observed_noise"),
        "grid_polish": results.get("grid_polish"),
        "grid": {
            "dx_mm": float(cfg.DX * 1000.0),
            "dz_mm": float(cfg.DZ * 1000.0),
            "nx": int(cfg.NX),
            "nz": int(cfg.NZ),
            "nt": int(cfg.NT),
            "npml": int(cfg.NPML),
        },
        "optimizer_success": results["optimizer_success"],
        "optimizer_message": results["optimizer_message"],
        "frequencies_ghz": [float(f / 1e9) for f in frequencies],
        "true": SingleRebarParams.from_array(results["true_params"]).as_mm(),
        "initial": SingleRebarParams.from_array(results["initial_params"]).as_mm(),
        "recovered": SingleRebarParams.from_array(results["optimal_params"]).as_mm(),
        "optimizer_final": SingleRebarParams.from_array(
            results.get("optimizer_final_params", results["optimal_params"])
        ).as_mm(),
        "best_misfit": float(results.get("best_misfit", np.nan)),
        "parameter_bounds_mm": {
            "lower": SingleRebarParams.from_array(results["parameter_bounds"][0]).as_mm(),
            "upper": SingleRebarParams.from_array(results["parameter_bounds"][1]).as_mm(),
        },
        "nrms_model": float(results["nrms_model"]),
        "nrms_data_by_frequency": {
            f"{f / 1e9:.6g}GHz": float(v)
            for f, v in results["nrms_data_by_frequency"].items()
        },
        "objective_misfit_average": float(results.get("objective_misfit_average", np.nan)),
        "objective_misfit_by_frequency": {
            f"{f / 1e9:.6g}GHz": float(v)
            for f, v in results.get("objective_misfit_by_frequency", {}).items()
        },
        "trace_shift_by_frequency": {
            f"{f / 1e9:.6g}GHz": value
            for f, value in results.get("trace_shift_by_frequency", {}).items()
        },
    }
    with open(os.path.join(outdir, "data", "single_rebar_summary.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSaved outputs under {outdir}")


def main():
    truth = default_single_rebar_truth()
    initial = default_single_rebar_initial_guess()

    parser = argparse.ArgumentParser(description="Single-rebar geometry inversion")
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="cpu")
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--sources", type=int, default=9,
                        help="Number of scan positions to use in the objective")
    parser.add_argument("--scan-step-mm", type=float, default=None,
                        help="Candidate scan spacing before source subsampling")
    parser.add_argument("--grid-step-mm", type=float, default=None,
                        help="Temporary uniform dx=dz grid override for resolution diagnostics")
    parser.add_argument("--frequencies-ghz", type=_parse_frequency_list,
                        default=[1.5e9],
                        help="Comma-separated frequencies in GHz, e.g. 1.4,1.5,1.6")
    parser.add_argument("--frequency-weights", type=_parse_weight_list, default=None,
                        help="Comma-separated objective weights matching --frequencies-ghz")
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0,
                        help="Add Gaussian observed-data noise as a fraction of clean B-scan RMS")
    parser.add_argument("--noise-seed", type=int, default=0)
    parser.add_argument("--objective-bandpass-ghz", type=_parse_ghz_bandpass, default=None,
                        help="Apply same objective bandpass to observed and synthetic traces as low,high in GHz")
    parser.add_argument("--objective-bandpass-taper-ghz", type=float, default=0.05,
                        help="Cosine taper width for objective bandpass edges in GHz")
    parser.add_argument("--max-iter", type=int, default=20)
    parser.add_argument("--max-evals", type=int, default=None)
    parser.add_argument("--optimizer", choices=["powell", "differential-evolution"],
                        default="powell")
    parser.add_argument("--de-popsize", type=int, default=5,
                        help="Population multiplier for differential evolution")
    parser.add_argument("--de-seed", type=int, default=7,
                        help="Random seed for differential evolution")
    parser.add_argument("--de-polish", action="store_true",
                        help="Enable SciPy's final polishing step for differential evolution")
    parser.add_argument("--grid-polish", action="store_true",
                        help="Run deterministic local grid polish after the optimizer")
    parser.add_argument("--grid-polish-preset", choices=["custom", "coarse", "fine"],
                        default="custom",
                        help="Named local grid-polish settings; explicit polish flags override it")
    parser.add_argument("--polish-x-half-window-mm", type=float, default=None)
    parser.add_argument("--polish-z-half-window-mm", type=float, default=None)
    parser.add_argument("--polish-radius-half-window-mm", type=float, default=None)
    parser.add_argument("--polish-x-step-mm", type=float, default=None)
    parser.add_argument("--polish-z-step-mm", type=float, default=None)
    parser.add_argument("--polish-radius-step-mm", type=float, default=None)
    parser.add_argument("--polish-progress-every", type=int, default=None)
    parser.add_argument("--polish-top-k", type=int, default=8,
                        help="Number of best local grid-polish candidates to save")
    parser.add_argument("--polish-stop-misfit", type=float, default=None,
                        help="Stop local grid polish once this objective value is reached")
    parser.add_argument("--x-bounds-mm", type=_parse_mm_bounds, default=None,
                        help="Lateral search bounds as min,max in mm")
    parser.add_argument("--z-bounds-mm", type=_parse_mm_bounds, default=None,
                        help="Depth search bounds as min,max in mm")
    parser.add_argument("--radius-bounds-mm", type=_parse_mm_bounds, default=None,
                        help="Radius search bounds as min,max in mm")
    parser.add_argument("--outdir", default=None,
                        help="Output directory. Defaults to outputs/experiments/NNN_single_rebar_inversion")
    parser.add_argument("--run-name", default="single_rebar_inversion",
                        help="Name used when allocating a numbered output directory")

    parser.add_argument("--true-x-mm", type=float, default=truth.x * 1000.0)
    parser.add_argument("--true-z-mm", type=float, default=truth.z * 1000.0)
    parser.add_argument("--true-radius-mm", type=float, default=truth.radius * 1000.0)
    parser.add_argument("--init-x-mm", type=float, default=initial.x * 1000.0)
    parser.add_argument("--init-z-mm", type=float, default=initial.z * 1000.0)
    parser.add_argument("--init-radius-mm", type=float, default=initial.radius * 1000.0)

    args = parser.parse_args()
    if args.frequency_weights is not None and len(args.frequency_weights) != len(args.frequencies_ghz):
        parser.error("--frequency-weights must have the same count as --frequencies-ghz")
    _override_grid(args.grid_step_mm)

    true_params = _params_from_args("true", args, truth)
    initial_params = _params_from_args("init", args, initial)
    scan_step = None if args.scan_step_mm is None else args.scan_step_mm / 1000.0

    bounds = None
    if any(item is not None for item in (args.x_bounds_mm, args.z_bounds_mm, args.radius_bounds_mm)):
        lower = np.array([
            cfg.SCAN_START_X,
            cfg.CONCRETE_TOP + 0.010,
            0.003,
        ])
        upper = np.array([
            cfg.SCAN_END_X,
            min(cfg.DOMAIN_Z - 0.020, cfg.CONCRETE_TOP + 0.160),
            0.015,
        ])
        for index, pair in enumerate((args.x_bounds_mm, args.z_bounds_mm, args.radius_bounds_mm)):
            if pair is not None:
                lower[index] = pair[0] / 1000.0
                upper[index] = pair[1] / 1000.0
        bounds = (lower, upper)

    outdir = allocate_output_dir(args.outdir, args.run_name)
    print(f"Output directory: {outdir}")

    grid_polish = None
    if args.grid_polish:
        grid_polish = _grid_polish_config_from_args(args)

    engine = SingleRebarInversionEngine(
        true_params=true_params,
        initial_params=initial_params,
        frequencies=args.frequencies_ghz,
        n_sources=args.sources,
        scan_step=scan_step,
        backend=args.backend,
        parameter_bounds=bounds,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        observed_noise_rms_fraction=args.observed_noise_rms_fraction,
        noise_seed=args.noise_seed,
        objective_bandpass_hz=args.objective_bandpass_ghz,
        objective_bandpass_taper_hz=args.objective_bandpass_taper_ghz * 1e9,
        frequency_weights=args.frequency_weights,
    )
    results = engine.run(
        max_iter=args.max_iter,
        max_evals=args.max_evals,
        optimizer=args.optimizer,
        de_popsize=args.de_popsize,
        de_seed=args.de_seed,
        de_polish=args.de_polish,
        grid_polish=grid_polish,
    )
    _write_outputs(results, outdir, engine.backend)
    write_run_manifest(
        outdir,
        "single_rebar_inversion",
        {
            "backend": engine.backend,
            "sources": len(engine.scan_positions),
            "frequencies_ghz": [float(value / 1e9) for value in args.frequencies_ghz],
            "geometry_mode": args.geometry_mode,
            "subcell_samples": args.subcell_samples,
            "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
            "noise_seed": args.noise_seed,
            "objective_bandpass_ghz": None if args.objective_bandpass_ghz is None else [
                float(value / 1e9) for value in args.objective_bandpass_ghz
            ],
            "objective_bandpass_taper_ghz": float(args.objective_bandpass_taper_ghz),
            "frequency_weights": args.frequency_weights,
            "grid_polish": grid_polish,
            "grid_step_mm": None if args.grid_step_mm is None else float(args.grid_step_mm),
            "dx_mm": float(cfg.DX * 1000.0),
            "dz_mm": float(cfg.DZ * 1000.0),
            "nt": int(cfg.NT),
            "summary_path": os.path.join(outdir, "data", "single_rebar_summary.json"),
        },
    )


if __name__ == "__main__":
    main()
