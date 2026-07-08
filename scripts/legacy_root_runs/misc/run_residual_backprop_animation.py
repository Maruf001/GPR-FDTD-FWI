#!/usr/bin/env python3
"""Generate FWI-style residual back-propagation wavefield animations."""

from __future__ import annotations

import argparse
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
from core.source import generate_time_array  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from run_multi_rebar_common_radius_profile import make_simulator  # noqa: E402
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    parse_vector_mm,
)
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import observed_wavelet  # noqa: E402
from run_wavefield_animation import (  # noqa: E402
    source_receiver_indices,
    validate_animation,
)
from visualization.plot_wavefield import animate_wavefield  # noqa: E402


def residual_source(candidate_trace, observed_trace, mute=None):
    """Return a time-reversed residual source for adjoint-style injection."""
    candidate = np.asarray(candidate_trace, dtype=np.float64)
    observed = np.asarray(observed_trace, dtype=np.float64)
    if candidate.shape != observed.shape:
        raise ValueError("candidate and observed traces must have the same shape")
    residual = candidate - observed
    if mute is not None:
        weight = np.asarray(mute, dtype=np.float64)
        if weight.shape != residual.shape:
            raise ValueError("mute must match trace shape")
        residual = residual * weight
    return residual[::-1].copy(), residual


def run_trace(backend, model, wavelet, source_x_mm):
    """Run one forward trace from Tx to Rx."""
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices(source_x_mm)
    simulator = make_simulator(model, backend)
    result = simulator.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)
    return result["trace"]


def run_backprop_snapshots(backend, model, adjoint_source, source_x_mm, save_every):
    """Inject a residual source at the physical receiver and save snapshots."""
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices(source_x_mm)
    simulator = make_simulator(model, backend)
    result = simulator.run(
        adjoint_source,
        rec_iz,
        rec_ix,
        src_iz,
        src_ix,
        save_fields_every=save_every,
    )
    snapshots = result.get("snapshots", [])
    if not snapshots:
        raise ValueError("back-propagation produced no snapshots")
    return snapshots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--truth-x-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--truth-z-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--truth-radius-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--candidate-x-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--candidate-z-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--candidate-radius-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--observed-frequency-scale", type=float, default=1.0)
    parser.add_argument("--observed-time-shift-ps", type=float, default=0.0)
    parser.add_argument("--observed-amplitude-scale", type=float, default=1.0)
    parser.add_argument("--modeled-frequency-scale", type=float, default=1.0)
    parser.add_argument("--modeled-time-shift-ps", type=float, default=0.0)
    parser.add_argument("--modeled-amplitude-scale", type=float, default=1.0)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--source-x-mm", type=float, required=True)
    parser.add_argument("--save-every", type=int, default=80)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--mute-residual", action="store_true")
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--label", required=True)
    parser.add_argument("--title", default="Residual back-propagation")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    if args.save_every <= 0:
        raise ValueError("--save-every must be positive")
    for label, xs, zs, rs in [
        ("truth", args.truth_x_values_mm, args.truth_z_values_mm, args.truth_radius_values_mm),
        ("candidate", args.candidate_x_values_mm, args.candidate_z_values_mm, args.candidate_radius_values_mm),
    ]:
        if len(xs) != len(zs) or len(xs) != len(rs):
            raise ValueError(f"{label} x, z, and radius lists must have the same length")

    _override_grid(args.grid_step_mm)
    outdir = Path(args.outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    truth_model = build_variable_geometry_model(
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        args.truth_radius_values_mm,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    candidate_model = build_variable_geometry_model(
        args.candidate_x_values_mm,
        args.candidate_z_values_mm,
        args.candidate_radius_values_mm,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    time_values = generate_time_array(cfg.NT, cfg.DT)
    observed_waveform = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=args.observed_frequency_scale,
        time_shift_ps=args.observed_time_shift_ps,
        amplitude_scale=args.observed_amplitude_scale,
    )
    modeled_waveform = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=args.modeled_frequency_scale,
        time_shift_ps=args.modeled_time_shift_ps,
        amplitude_scale=args.modeled_amplitude_scale,
    )
    started = time.time()
    observed_trace = run_trace(args.backend, truth_model, observed_waveform, args.source_x_mm)
    candidate_trace = run_trace(args.backend, candidate_model, modeled_waveform, args.source_x_mm)
    mute = _build_mute_window(cfg.NT, cfg.DT) if args.mute_residual else None
    adjoint_source, residual = residual_source(candidate_trace, observed_trace, mute=mute)
    snapshots = run_backprop_snapshots(
        args.backend,
        candidate_model,
        adjoint_source,
        args.source_x_mm,
        args.save_every,
    )
    elapsed_s = time.time() - started

    candidate_rebars = list(zip(
        args.candidate_x_values_mm,
        args.candidate_z_values_mm,
        args.candidate_radius_values_mm,
    ))
    source_receiver_mm = (
        float(args.source_x_mm),
        float(cfg.TX_Z * 1000.0),
        float(args.source_x_mm + cfg.TX_RX_OFFSET * 1000.0),
        float(cfg.RX_Z * 1000.0),
    )
    animation_path = figures_dir / f"{args.label}_residual_backprop.gif"
    animate_wavefield(
        snapshots,
        save_path=str(animation_path),
        show=False,
        fps=args.fps,
        rebar_specs_mm=candidate_rebars,
        source_receiver_mm=source_receiver_mm,
        title_prefix=args.title,
    )
    validation = validate_animation(animation_path)

    summary = {
        "backend": args.backend,
        "grid_step_mm": float(args.grid_step_mm),
        "truth_x_values_mm": args.truth_x_values_mm,
        "truth_z_values_mm": args.truth_z_values_mm,
        "truth_radius_values_mm": args.truth_radius_values_mm,
        "candidate_x_values_mm": args.candidate_x_values_mm,
        "candidate_z_values_mm": args.candidate_z_values_mm,
        "candidate_radius_values_mm": args.candidate_radius_values_mm,
        "observed_source": {
            "frequency_scale": float(args.observed_frequency_scale),
            "time_shift_ps": float(args.observed_time_shift_ps),
            "amplitude_scale": float(args.observed_amplitude_scale),
        },
        "modeled_source": {
            "frequency_scale": float(args.modeled_frequency_scale),
            "time_shift_ps": float(args.modeled_time_shift_ps),
            "amplitude_scale": float(args.modeled_amplitude_scale),
        },
        "source_x_mm": float(args.source_x_mm),
        "receiver_x_mm": float(args.source_x_mm + cfg.TX_RX_OFFSET * 1000.0),
        "source_z_mm": float(cfg.TX_Z * 1000.0),
        "receiver_z_mm": float(cfg.RX_Z * 1000.0),
        "mute_residual": bool(args.mute_residual),
        "save_every": int(args.save_every),
        "fps": int(args.fps),
        "elapsed_time_s": float(elapsed_s),
        "snapshot_count": len(snapshots),
        "observed_trace_rms": float(np.sqrt(np.mean(observed_trace ** 2))),
        "candidate_trace_rms": float(np.sqrt(np.mean(candidate_trace ** 2))),
        "residual_trace_rms": float(np.sqrt(np.mean(residual ** 2))),
        "validation": validation,
        "paths": {
            "animation": str(animation_path),
        },
    }
    summary_path = data_dir / f"{args.label}_residual_backprop_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Wrote residual back-propagation animation: {animation_path}")
    print(f"Wrote summary: {summary_path}")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
