"""
Post-hoc trace-shift diagnostics for single-rebar candidate geometries.

This script recreates the observed data for a single-rebar scenario and then
evaluates trace alignment for selected candidate geometries. It is intended for
Experiment 15: comparing the known Powell high-radius basin against polished
true-radius candidates without rerunning full optimizations.
"""

import argparse
import csv
import json
import os
import sys

import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import config as cfg  # noqa: E402
from core.geometry import build_single_rebar_model  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from inversion.single_rebar_pipeline import (  # noqa: E402
    SingleRebarInversionEngine,
    SingleRebarParams,
    default_single_rebar_initial_guess,
    default_single_rebar_truth,
)
from inversion.trace_distances import least_squares_distance, trace_shift_diagnostics  # noqa: E402
from run_single_rebar_inversion import (  # noqa: E402
    _override_grid,
    _parse_frequency_list,
    _params_from_args,
)


def _parse_mm_triplet(text):
    parts = [item.strip() for item in text.split(",") if item.strip()]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Use x,z,radius in millimeters")
    try:
        return tuple(float(item) for item in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Candidate values must be numeric") from exc


def _params_from_mm_dict(values):
    return SingleRebarParams(
        x=float(values["x_mm"]) / 1000.0,
        z=float(values["z_mm"]) / 1000.0,
        radius=float(values["radius_mm"]) / 1000.0,
    )


def _candidate_from_summary(path, label, field):
    with open(path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    values = summary.get(field)
    if values is None:
        raise ValueError(f"{path} does not contain field {field!r}")
    return {
        "label": label,
        "params": _params_from_mm_dict(values),
        "source": path,
        "source_field": field,
        "source_misfit": summary.get("best_misfit"),
    }


def _top_candidates_from_summary(path, label_prefix, limit):
    with open(path, "r", encoding="utf-8") as f:
        summary = json.load(f)
    grid_polish = summary.get("grid_polish") or {}
    rows = grid_polish.get("top_candidates") or []
    candidates = []
    for index, item in enumerate(rows[:limit], start=1):
        candidates.append({
            "label": f"{label_prefix}_top{index}",
            "params": _params_from_mm_dict(item["params"]),
            "source": path,
            "source_field": "grid_polish.top_candidates",
            "source_misfit": item.get("misfit"),
        })
    return candidates


def _candidate_from_cli(text):
    label, values = text.split(":", 1) if ":" in text else ("candidate", text)
    x_mm, z_mm, radius_mm = _parse_mm_triplet(values)
    return {
        "label": label,
        "params": SingleRebarParams(
            x=x_mm / 1000.0,
            z=z_mm / 1000.0,
            radius=radius_mm / 1000.0,
        ),
        "source": "cli",
        "source_field": "candidate",
        "source_misfit": None,
    }


def _safe_label(label):
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in label)


def _evaluate_candidate(engine, candidate):
    params = candidate["params"]
    model = build_single_rebar_model(
        params.x,
        params.z,
        params.radius,
        geometry_mode=engine.geometry_mode,
        subcell_samples=engine.subcell_samples,
    )

    by_frequency = {}
    total_ls = 0.0
    for frequency in engine.frequencies:
        d_syn = engine._simulate_bscan(model, engine.wavelets[frequency])
        d_obs = engine.d_obs_by_frequency[frequency]
        ls = least_squares_distance(d_obs, d_syn, mute=engine.mute, normalize=True)
        diagnostics = trace_shift_diagnostics(
            d_obs,
            d_syn,
            cfg.DT,
            mute=engine.mute,
            dominant_frequency=frequency,
        )
        diagnostics["least_squares_distance"] = float(ls)
        by_frequency[f"{frequency / 1e9:.6g}GHz"] = diagnostics
        total_ls += ls

    primary = by_frequency[f"{engine.frequencies[0] / 1e9:.6g}GHz"]
    return {
        "label": candidate["label"],
        "params": params.as_mm(),
        "source": candidate["source"],
        "source_field": candidate["source_field"],
        "source_misfit": candidate["source_misfit"],
        "mean_least_squares_distance": float(total_ls / len(engine.frequencies)),
        "primary_nrccc": primary["nrccc_fraction_lt_half_period"],
        "primary_median_rccc": primary["median_rccc"],
        "primary_max_rccc": primary["max_rccc"],
        "primary_median_abs_shift_ps": primary["median_abs_shift_s"] * 1e12,
        "primary_max_abs_shift_ps": primary["max_abs_shift_s"] * 1e12,
        "by_frequency": by_frequency,
    }


def _write_csv(path, rows):
    fields = [
        "label",
        "x_mm",
        "z_mm",
        "radius_mm",
        "mean_least_squares_distance",
        "primary_nrccc",
        "primary_median_rccc",
        "primary_max_rccc",
        "primary_median_abs_shift_ps",
        "primary_max_abs_shift_ps",
        "source_misfit",
        "source",
        "source_field",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "label": row["label"],
                "x_mm": row["params"]["x_mm"],
                "z_mm": row["params"]["z_mm"],
                "radius_mm": row["params"]["radius_mm"],
                "mean_least_squares_distance": row["mean_least_squares_distance"],
                "primary_nrccc": row["primary_nrccc"],
                "primary_median_rccc": row["primary_median_rccc"],
                "primary_max_rccc": row["primary_max_rccc"],
                "primary_median_abs_shift_ps": row["primary_median_abs_shift_ps"],
                "primary_max_abs_shift_ps": row["primary_max_abs_shift_ps"],
                "source_misfit": row["source_misfit"],
                "source": row["source"],
                "source_field": row["source_field"],
            })


def main():
    truth = default_single_rebar_truth()
    initial = default_single_rebar_initial_guess()

    parser = argparse.ArgumentParser(description="Single-rebar trace-shift diagnostics")
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml", "auto"], default="gpu-cpml")
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--scan-step-mm", type=float, default=None)
    parser.add_argument("--grid-step-mm", type=float, default=None)
    parser.add_argument("--frequencies-ghz", type=_parse_frequency_list, default=[1.5e9])
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=0)
    parser.add_argument("--summary-candidate", action="append", default=[],
                        help="label:path:field, where field is recovered or optimizer_final")
    parser.add_argument("--summary-top-candidates", action="append", default=[],
                        help="label:path[:limit] for grid_polish.top_candidates")
    parser.add_argument("--candidate-mm", action="append", default=[],
                        help="label:x,z,radius in millimeters")
    parser.add_argument("--run-name", default="single_rebar_trace_diagnostics")
    parser.add_argument("--outdir", default=None)

    parser.add_argument("--true-x-mm", type=float, default=truth.x * 1000.0)
    parser.add_argument("--true-z-mm", type=float, default=truth.z * 1000.0)
    parser.add_argument("--true-radius-mm", type=float, default=truth.radius * 1000.0)
    parser.add_argument("--init-x-mm", type=float, default=initial.x * 1000.0)
    parser.add_argument("--init-z-mm", type=float, default=initial.z * 1000.0)
    parser.add_argument("--init-radius-mm", type=float, default=initial.radius * 1000.0)

    args = parser.parse_args()
    _override_grid(args.grid_step_mm)

    candidates = []
    for item in args.summary_candidate:
        label, path, field = item.split(":", 2)
        candidates.append(_candidate_from_summary(path, label, field))
    for item in args.summary_top_candidates:
        parts = item.split(":")
        if len(parts) not in (2, 3):
            raise ValueError("--summary-top-candidates must use label:path[:limit]")
        label, path = parts[0], parts[1]
        limit = int(parts[2]) if len(parts) == 3 else 8
        candidates.extend(_top_candidates_from_summary(path, label, limit))
    for item in args.candidate_mm:
        candidates.append(_candidate_from_cli(item))
    if not candidates:
        raise SystemExit("No candidates provided")

    true_params = _params_from_args("true", args, truth)
    initial_params = _params_from_args("init", args, initial)
    scan_step = None if args.scan_step_mm is None else args.scan_step_mm / 1000.0

    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = os.path.join(outdir, "data")
    os.makedirs(data_dir, exist_ok=True)
    print(f"Output directory: {outdir}")

    engine = SingleRebarInversionEngine(
        true_params=true_params,
        initial_params=initial_params,
        frequencies=args.frequencies_ghz,
        n_sources=args.sources,
        scan_step=scan_step,
        backend=args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        observed_noise_rms_fraction=args.observed_noise_rms_fraction,
        noise_seed=args.noise_seed,
        log_every=999999,
    )

    rows = []
    for candidate in candidates:
        print(f"Evaluating {candidate['label']}: {candidate['params'].as_mm()}")
        rows.append(_evaluate_candidate(engine, candidate))

    rows.sort(key=lambda item: item["mean_least_squares_distance"])
    summary = {
        "backend": engine.backend,
        "grid": {
            "dx_mm": float(cfg.DX * 1000.0),
            "dz_mm": float(cfg.DZ * 1000.0),
            "nx": int(cfg.NX),
            "nz": int(cfg.NZ),
            "nt": int(cfg.NT),
            "npml": int(cfg.NPML),
        },
        "sources": len(engine.scan_positions),
        "frequencies_ghz": [float(value / 1e9) for value in engine.frequencies],
        "observed_noise_rms_fraction": args.observed_noise_rms_fraction,
        "noise_seed": args.noise_seed,
        "true": true_params.as_mm(),
        "candidates": rows,
    }

    with open(os.path.join(data_dir, "trace_diagnostics_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    _write_csv(os.path.join(data_dir, "trace_diagnostics_candidates.csv"), rows)
    write_run_manifest(
        outdir,
        "single_rebar_trace_diagnostics",
        {
            "backend": engine.backend,
            "sources": len(engine.scan_positions),
            "frequencies_ghz": [float(value / 1e9) for value in engine.frequencies],
            "summary_path": os.path.join(data_dir, "trace_diagnostics_summary.json"),
            "candidate_count": len(rows),
        },
    )

    print("\nCandidate ranking:")
    for row in rows:
        params = row["params"]
        print(
            f"  {row['label']}: J={row['mean_least_squares_distance']:.6e}, "
            f"NRCCC={row['primary_nrccc']:.3f}, "
            f"median RCCC={row['primary_median_rccc']:.3f}, "
            f"max RCCC={row['primary_max_rccc']:.3f}, "
            f"x={params['x_mm']:.3f} mm, z={params['z_mm']:.3f} mm, "
            f"r={params['radius_mm']:.3f} mm"
        )

    print(f"\nSaved diagnostics under {outdir}")


if __name__ == "__main__":
    main()

