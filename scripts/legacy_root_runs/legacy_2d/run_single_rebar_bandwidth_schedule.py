#!/usr/bin/env python3
"""Run staged PEBDD-style objective-bandpass inversion for one rebar."""
import argparse
import json
import os
import sys

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

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
    default_single_rebar_truth,
)
from run_single_rebar_inversion import _override_grid, _write_outputs  # noqa: E402


def parse_band_schedule(text):
    """Parse `low,high|low,high` GHz band schedule text."""
    stages = []
    for item in text.split("|"):
        item = item.strip()
        if not item:
            continue
        values = [float(part.strip()) for part in item.split(",") if part.strip()]
        if len(values) != 2 or values[0] < 0.0 or values[0] >= values[1]:
            raise argparse.ArgumentTypeError("Use stages like 0.35,1.1|0.35,1.5")
        stages.append((values[0] * 1e9, values[1] * 1e9))
    if not stages:
        raise argparse.ArgumentTypeError("At least one band stage is required")
    return stages


def coarse_polish_config(top_k=10):
    """Default local coarse-polish settings used in the current pipeline."""
    return {
        "x_half_window_mm": 0.0,
        "z_half_window_mm": 1.0,
        "radius_half_window_mm": 1.0,
        "x_step_mm": 1.0,
        "z_step_mm": 0.5,
        "radius_step_mm": 0.2,
        "progress_every": 10,
        "top_k": int(top_k),
        "stop_misfit": None,
        "preset": "coarse",
    }


def _params_from_mm(x_mm, z_mm, radius_mm):
    return SingleRebarParams(
        x=x_mm / 1000.0,
        z=z_mm / 1000.0,
        radius=radius_mm / 1000.0,
    )


def _bounds_from_mm(x_bounds_mm, z_bounds_mm, radius_bounds_mm):
    lower = np.array([
        x_bounds_mm[0] / 1000.0,
        z_bounds_mm[0] / 1000.0,
        radius_bounds_mm[0] / 1000.0,
    ])
    upper = np.array([
        x_bounds_mm[1] / 1000.0,
        z_bounds_mm[1] / 1000.0,
        radius_bounds_mm[1] / 1000.0,
    ])
    return lower, upper


def _parse_bounds(text):
    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    if len(values) != 2 or values[0] >= values[1]:
        raise argparse.ArgumentTypeError("Use min,max")
    return values


def _stage_record(stage_name, stage_dir, band_hz, results):
    params = SingleRebarParams.from_array(results["optimal_params"]).as_mm()
    return {
        "stage": stage_name,
        "output_dir": stage_dir,
        "bandpass_hz": None if band_hz is None else {
            "low_hz": float(band_hz[0]),
            "high_hz": float(band_hz[1]),
        },
        "recovered": params,
        "best_misfit": float(results["best_misfit"]),
        "nrms_model": float(results["nrms_model"]),
        "nrms_data_by_frequency": {
            f"{f / 1e9:.6g}GHz": float(v)
            for f, v in results["nrms_data_by_frequency"].items()
        },
        "elapsed_time_s": float(results["elapsed_time"]),
        "grid_polish": results.get("grid_polish"),
    }


def main():
    truth = default_single_rebar_truth()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--bands-ghz", type=parse_band_schedule,
                        default=parse_band_schedule("0.35,1.1|0.35,1.5|0.35,2.0|0.35,2.5"))
    parser.add_argument("--bandpass-taper-ghz", type=float, default=0.05)
    parser.add_argument("--stage-max-iter", type=int, default=8)
    parser.add_argument("--stage-max-evals", type=int, default=35)
    parser.add_argument("--final-polish", action="store_true")
    parser.add_argument("--polish-top-k", type=int, default=10)
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--init-x-mm", type=float, default=252.5)
    parser.add_argument("--init-z-mm", type=float, default=91.8)
    parser.add_argument("--init-radius-mm", type=float, default=6.76)
    parser.add_argument("--x-bounds-mm", type=_parse_bounds, default=[220.0, 280.0])
    parser.add_argument("--z-bounds-mm", type=_parse_bounds, default=[70.0, 110.0])
    parser.add_argument("--radius-bounds-mm", type=_parse_bounds, default=[4.0, 10.0])
    parser.add_argument("--run-name", default="single_rebar_bandwidth_schedule")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    os.makedirs(os.path.join(outdir, "data"), exist_ok=True)
    print(f"Output directory: {outdir}")

    bounds = _bounds_from_mm(args.x_bounds_mm, args.z_bounds_mm, args.radius_bounds_mm)
    current = _params_from_mm(args.init_x_mm, args.init_z_mm, args.init_radius_mm)
    stage_records = []

    for index, band_hz in enumerate(args.bands_ghz, start=1):
        stage_name = f"stage{index:02d}_{band_hz[0] / 1e9:.2f}_{band_hz[1] / 1e9:.2f}GHz"
        stage_dir = os.path.join(outdir, stage_name)
        print(f"\n=== {stage_name} ===")
        engine = SingleRebarInversionEngine(
            true_params=truth,
            initial_params=current,
            frequencies=(cfg.F_CENTER,),
            n_sources=args.sources,
            backend=args.backend,
            parameter_bounds=bounds,
            observed_noise_rms_fraction=args.observed_noise_rms_fraction,
            noise_seed=args.noise_seed,
            objective_bandpass_hz=band_hz,
            objective_bandpass_taper_hz=args.bandpass_taper_ghz * 1e9,
        )
        results = engine.run(
            max_iter=args.stage_max_iter,
            max_evals=args.stage_max_evals,
            optimizer="powell",
            grid_polish=None,
        )
        _write_outputs(results, stage_dir, engine.backend)
        current = SingleRebarParams.from_array(results["optimal_params"])
        stage_records.append(_stage_record(stage_name, stage_dir, band_hz, results))

    if args.final_polish:
        stage_name = "final_fullband_coarse_polish"
        stage_dir = os.path.join(outdir, stage_name)
        print(f"\n=== {stage_name} ===")
        engine = SingleRebarInversionEngine(
            true_params=truth,
            initial_params=current,
            frequencies=(cfg.F_CENTER,),
            n_sources=args.sources,
            backend=args.backend,
            parameter_bounds=bounds,
            observed_noise_rms_fraction=args.observed_noise_rms_fraction,
            noise_seed=args.noise_seed,
        )
        results = engine.run(
            max_iter=1,
            max_evals=1,
            optimizer="powell",
            grid_polish=coarse_polish_config(top_k=args.polish_top_k),
        )
        _write_outputs(results, stage_dir, engine.backend)
        current = SingleRebarParams.from_array(results["optimal_params"])
        stage_records.append(_stage_record(stage_name, stage_dir, None, results))

    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "grid_step_mm": args.grid_step_mm,
        "sources": args.sources,
        "stage_count": len(stage_records),
        "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
        "noise_seed": args.noise_seed,
        "initial": _params_from_mm(args.init_x_mm, args.init_z_mm, args.init_radius_mm).as_mm(),
        "final": current.as_mm(),
        "stages": stage_records,
    }
    summary_path = os.path.join(outdir, "data", "bandwidth_schedule_summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    write_run_manifest(
        outdir,
        "single_rebar_bandwidth_schedule",
        {
            "backend": args.backend,
            "grid_step_mm": args.grid_step_mm,
            "sources": args.sources,
            "bands_ghz": [[float(lo / 1e9), float(hi / 1e9)] for lo, hi in args.bands_ghz],
            "final_polish": args.final_polish,
            "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
            "noise_seed": args.noise_seed,
            "summary_path": summary_path,
        },
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
