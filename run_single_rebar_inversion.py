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


def _params_from_args(prefix, args, default):
    x_mm = getattr(args, f"{prefix}_x_mm")
    z_mm = getattr(args, f"{prefix}_z_mm")
    radius_mm = getattr(args, f"{prefix}_radius_mm")
    return SingleRebarParams(
        x=(x_mm if x_mm is not None else default.x * 1000.0) / 1000.0,
        z=(z_mm if z_mm is not None else default.z * 1000.0) / 1000.0,
        radius=(radius_mm if radius_mm is not None else default.radius * 1000.0) / 1000.0,
    )


def _write_outputs(results, outdir, backend):
    from visualization.plot_bscan import plot_bscan
    from visualization.plot_inversion import plot_convergence, plot_inversion_comparison

    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "figures"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "data"), exist_ok=True)

    frequencies = results["frequencies"]
    obs_stack = np.stack([results["d_obs_by_frequency"][f] for f in frequencies])
    syn_stack = np.stack([results["d_syn_final_by_frequency"][f] for f in frequencies])

    np.savez(
        os.path.join(outdir, "data", "single_rebar_results.npz"),
        initial_epsr=results["initial_epsr"],
        inverted_epsr=results["inverted_epsr"],
        true_epsr=results["true_epsr"],
        observed_bscans=obs_stack,
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
        "optimizer_success": results["optimizer_success"],
        "optimizer_message": results["optimizer_message"],
        "frequencies_ghz": [float(f / 1e9) for f in frequencies],
        "true": SingleRebarParams.from_array(results["true_params"]).as_mm(),
        "initial": SingleRebarParams.from_array(results["initial_params"]).as_mm(),
        "recovered": SingleRebarParams.from_array(results["optimal_params"]).as_mm(),
        "nrms_model": float(results["nrms_model"]),
        "nrms_data_by_frequency": {
            f"{f / 1e9:.6g}GHz": float(v)
            for f, v in results["nrms_data_by_frequency"].items()
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
    parser.add_argument("--sources", type=int, default=9,
                        help="Number of scan positions to use in the objective")
    parser.add_argument("--scan-step-mm", type=float, default=None,
                        help="Candidate scan spacing before source subsampling")
    parser.add_argument("--frequencies-ghz", type=_parse_frequency_list,
                        default=[1.5e9],
                        help="Comma-separated frequencies in GHz, e.g. 1.4,1.5,1.6")
    parser.add_argument("--max-iter", type=int, default=20)
    parser.add_argument("--max-evals", type=int, default=None)
    parser.add_argument("--outdir", default="outputs/single_rebar")

    parser.add_argument("--true-x-mm", type=float, default=truth.x * 1000.0)
    parser.add_argument("--true-z-mm", type=float, default=truth.z * 1000.0)
    parser.add_argument("--true-radius-mm", type=float, default=truth.radius * 1000.0)
    parser.add_argument("--init-x-mm", type=float, default=initial.x * 1000.0)
    parser.add_argument("--init-z-mm", type=float, default=initial.z * 1000.0)
    parser.add_argument("--init-radius-mm", type=float, default=initial.radius * 1000.0)

    args = parser.parse_args()

    true_params = _params_from_args("true", args, truth)
    initial_params = _params_from_args("init", args, initial)
    scan_step = None if args.scan_step_mm is None else args.scan_step_mm / 1000.0

    engine = SingleRebarInversionEngine(
        true_params=true_params,
        initial_params=initial_params,
        frequencies=args.frequencies_ghz,
        n_sources=args.sources,
        scan_step=scan_step,
        backend=args.backend,
    )
    results = engine.run(max_iter=args.max_iter, max_evals=args.max_evals)
    _write_outputs(results, args.outdir, engine.backend)


if __name__ == "__main__":
    main()
