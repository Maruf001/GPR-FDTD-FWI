#!/usr/bin/env python3
"""Run a small synthetic benchmark for the B-scan rebar detector."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

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
from core.source import generate_time_array  # noqa: E402
from inversion.rebar_detection import detect_rebar_candidates  # noqa: E402
from run_multi_rebar_common_radius_profile import build_scan_positions, simulate_bscan  # noqa: E402
from run_multi_rebar_local_geometry_profile import build_variable_geometry_model  # noqa: E402
from run_rebar_detection_pipeline import add_noise, parse_mm_range, parse_ps_values, truth_match_metrics  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import observed_wavelet  # noqa: E402


def write_rows_csv(path, rows):
    fieldnames = [
        "scenario_id",
        "x_mm",
        "z_mm",
        "radius_mm",
        "noise_fraction",
        "noise_seed",
        "detected",
        "matched_rank",
        "best_x_mm",
        "best_z_mm",
        "x_error_mm",
        "z_error_mm",
        "within_tolerance",
        "best_score",
        "best_time_offset_ps",
        "elapsed_time_s",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def summarize_rows(rows):
    total = len(rows)
    hits = sum(1 for row in rows if row["within_tolerance"])
    detected = sum(1 for row in rows if row["detected"])
    x_errors = [row["x_error_mm"] for row in rows if row["x_error_mm"] is not None]
    z_errors = [row["z_error_mm"] for row in rows if row["z_error_mm"] is not None]
    return {
        "scenario_count": total,
        "detected_count": detected,
        "hit_count": hits,
        "hit_rate": float(hits / total) if total else 0.0,
        "median_x_error_mm": None if not x_errors else float(np.median(x_errors)),
        "median_z_error_mm": None if not z_errors else float(np.median(z_errors)),
        "max_x_error_mm": None if not x_errors else float(np.max(x_errors)),
        "max_z_error_mm": None if not z_errors else float(np.max(z_errors)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=2.0)
    parser.add_argument("--scan-step-mm", type=float, default=4.0)
    parser.add_argument("--sources", type=int, default=None)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--x-mm", type=float, default=250.0)
    parser.add_argument("--z-values-mm", type=parse_mm_range, default=parse_mm_range("70:130:20"))
    parser.add_argument("--radius-values-mm", type=parse_mm_range, default=parse_mm_range("4:10:2"))
    parser.add_argument("--noise-fractions", type=parse_mm_range, default=parse_mm_range("0,0.05,0.10"))
    parser.add_argument("--noise-seed", type=int, default=13)
    parser.add_argument("--frequency-scale", type=float, default=1.0)
    parser.add_argument("--time-shift-ps", type=float, default=0.0)
    parser.add_argument("--amplitude-scale", type=float, default=1.0)
    parser.add_argument("--detector-x-values-mm", type=parse_mm_range, default=parse_mm_range("150:350:4"))
    parser.add_argument("--detector-z-values-mm", type=parse_mm_range, default=parse_mm_range("55:160:5"))
    parser.add_argument("--detector-time-offset-ps-values", type=parse_ps_values, default=parse_ps_values("400,500,600,667"))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--x-min-separation-mm", type=float, default=35.0)
    parser.add_argument("--z-min-separation-mm", type=float, default=35.0)
    parser.add_argument("--truth-tolerance-x-mm", type=float, default=12.0)
    parser.add_argument("--truth-tolerance-z-mm", type=float, default=12.0)
    parser.add_argument("--progress-every", type=int, default=1)
    parser.add_argument("--run-name", default="single_rebar_detection_benchmark")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    _override_grid(args.grid_step_mm)
    outdir = allocate_output_dir(args.outdir, args.run_name)
    data_dir = Path(outdir) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    scan_positions, scan_x = build_scan_positions(args.scan_step_mm / 1000.0, args.sources)
    time_values = generate_time_array(cfg.NT, cfg.DT)
    wavelet = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=args.frequency_scale,
        time_shift_ps=args.time_shift_ps,
        amplitude_scale=args.amplitude_scale,
    )

    rows = []
    scenario_id = 0
    started_all = time.time()
    total = len(args.z_values_mm) * len(args.radius_values_mm) * len(args.noise_fractions)
    for z_mm in args.z_values_mm:
        for radius_mm in args.radius_values_mm:
            model = build_variable_geometry_model([args.x_mm], [z_mm], [radius_mm])
            clean = simulate_bscan(model, wavelet, scan_positions, args.backend)
            for noise_fraction in args.noise_fractions:
                scenario_id += 1
                started = time.time()
                observed, _noise_stats = add_noise(clean, noise_fraction, args.noise_seed)
                candidates = detect_rebar_candidates(
                    observed,
                    scan_x,
                    time_values,
                    x_values_mm=args.detector_x_values_mm,
                    z_values_mm=args.detector_z_values_mm,
                    top_k=args.top_k,
                    x_min_separation_mm=args.x_min_separation_mm,
                    z_min_separation_mm=args.z_min_separation_mm,
                    time_offsets_s=[value * 1e-12 for value in args.detector_time_offset_ps_values],
                )
                metrics = truth_match_metrics(
                    candidates,
                    [args.x_mm],
                    [z_mm],
                    args.truth_tolerance_x_mm,
                    args.truth_tolerance_z_mm,
                )[0]
                best = candidates[0] if candidates else None
                rows.append({
                    "scenario_id": scenario_id,
                    "x_mm": float(args.x_mm),
                    "z_mm": float(z_mm),
                    "radius_mm": float(radius_mm),
                    "noise_fraction": float(noise_fraction),
                    "noise_seed": int(args.noise_seed),
                    "detected": bool(candidates),
                    "matched_rank": metrics["matched_rank"],
                    "best_x_mm": None if best is None else float(best.x_m * 1000.0),
                    "best_z_mm": None if best is None else float(best.z_m * 1000.0),
                    "x_error_mm": metrics["x_error_mm"],
                    "z_error_mm": metrics["z_error_mm"],
                    "within_tolerance": metrics["within_tolerance"],
                    "best_score": None if best is None else float(best.normalized_score),
                    "best_time_offset_ps": None if best is None else float(best.time_offset_s * 1e12),
                    "elapsed_time_s": float(time.time() - started),
                })
                if args.progress_every and scenario_id % args.progress_every == 0:
                    print(f"  Detection benchmark: {scenario_id}/{total}")

    csv_path = data_dir / "detection_benchmark.csv"
    write_rows_csv(csv_path, rows)
    aggregate = summarize_rows(rows)
    summary = {
        "backend": args.backend,
        "grid_step_mm": float(args.grid_step_mm),
        "scan_step_mm": float(args.scan_step_mm),
        "sources": len(scan_positions),
        "x_mm": float(args.x_mm),
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "noise_fractions": args.noise_fractions,
        "detector_time_offset_ps_values": args.detector_time_offset_ps_values,
        "aggregate": aggregate,
        "elapsed_time_s": float(time.time() - started_all),
        "paths": {
            "csv": str(csv_path),
        },
    }
    summary_path = data_dir / "detection_benchmark_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    write_run_manifest(
        outdir,
        "single_rebar_detection_benchmark",
        {"summary_path": str(summary_path), "csv": str(csv_path)},
    )
    print(json.dumps(aggregate, indent=2))
    print(f"Wrote summary: {summary_path}")


if __name__ == "__main__":
    main()

