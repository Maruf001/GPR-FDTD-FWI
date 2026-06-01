#!/usr/bin/env python3
"""Generate a representative FDTD wavefield animation for an experiment."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageSequence

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import config as cfg  # noqa: E402
from core.source import generate_time_array  # noqa: E402
from core.utils import pos_to_index  # noqa: E402
from run_multi_rebar_common_radius_profile import make_simulator  # noqa: E402
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    parse_vector_mm,
)
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_material_tradeoff import build_single_rebar_material_model  # noqa: E402
from run_single_rebar_source_profiled_polish import observed_wavelet  # noqa: E402
from visualization.plot_wavefield import animate_wavefield  # noqa: E402


def source_receiver_indices(source_x_mm):
    """Return source/receiver grid indices for one surface scan location."""
    src_x = float(source_x_mm) / 1000.0
    rec_x = min(src_x + cfg.TX_RX_OFFSET, cfg.DOMAIN_X - cfg.DX)
    src_iz = pos_to_index(cfg.TX_Z, cfg.DZ, cfg.NPML)
    rec_iz = pos_to_index(cfg.RX_Z, cfg.DZ, cfg.NPML)
    src_ix = pos_to_index(src_x, cfg.DX, cfg.NPML)
    rec_ix = pos_to_index(rec_x, cfg.DX, cfg.NPML)
    rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)
    return src_iz, src_ix, rec_iz, rec_ix


def validate_animation(path):
    """Return simple nonblank validation metrics for a saved animation."""
    frame_count = 0
    std_values = []
    dynamic_ranges = []
    size = None
    with Image.open(path) as image:
        for frame in ImageSequence.Iterator(image):
            gray = np.asarray(frame.convert("L"))
            if size is None:
                size = frame.size
            frame_count += 1
            std_values.append(float(gray.std()))
            dynamic_ranges.append(int(gray.max()) - int(gray.min()))
    if frame_count == 0:
        raise ValueError(f"Saved animation has no frames: {path}")
    max_dynamic_range = max(dynamic_ranges)
    mean_std = float(np.mean(std_values))
    if max_dynamic_range < 2:
        raise ValueError(f"Saved near-blank animation: {path}")
    return {
        "frame_count": int(frame_count),
        "width_px": int(size[0]),
        "height_px": int(size[1]),
        "max_dynamic_range": int(max_dynamic_range),
        "mean_frame_std": mean_std,
    }


def _material_overrides_present(*values):
    return any(value is not None for value in values)


def build_animation_model(
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        geometry_mode="hard",
        subcell_samples=5,
        concrete_epsr=None,
        concrete_sigma=None,
        rebar_epsr=None,
        rebar_sigma=None):
    """Build a geometry or single-rebar material-aware model for animation."""
    has_material_overrides = _material_overrides_present(
        concrete_epsr,
        concrete_sigma,
        rebar_epsr,
        rebar_sigma,
    )
    if not has_material_overrides:
        return build_variable_geometry_model(
            x_values_mm,
            z_values_mm,
            radius_values_mm,
            geometry_mode=geometry_mode,
            subcell_samples=subcell_samples,
        )

    if len(x_values_mm) != 1 or len(z_values_mm) != 1 or len(radius_values_mm) != 1:
        raise ValueError("material override animations currently support exactly one rebar")
    return build_single_rebar_material_model(
        float(x_values_mm[0]) / 1000.0,
        float(z_values_mm[0]) / 1000.0,
        float(radius_values_mm[0]) / 1000.0,
        concrete_epsr=cfg.CONCRETE_EPSR if concrete_epsr is None else float(concrete_epsr),
        concrete_sigma=cfg.CONCRETE_SIGMA if concrete_sigma is None else float(concrete_sigma),
        rebar_epsr=cfg.REBAR_EPSR if rebar_epsr is None else float(rebar_epsr),
        rebar_sigma=cfg.REBAR_SIGMA if rebar_sigma is None else float(rebar_sigma),
        geometry_mode=geometry_mode,
        subcell_samples=subcell_samples,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--x-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--z-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--radius-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--frequency-scale", type=float, default=1.0)
    parser.add_argument("--time-shift-ps", type=float, default=0.0)
    parser.add_argument("--amplitude-scale", type=float, default=1.0)
    parser.add_argument("--source-x-mm", type=float, required=True)
    parser.add_argument("--save-every", type=int, default=60)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--concrete-epsr", type=float, default=None)
    parser.add_argument("--concrete-sigma", type=float, default=None)
    parser.add_argument("--rebar-epsr", type=float, default=None)
    parser.add_argument("--rebar-sigma", type=float, default=None)
    parser.add_argument("--label", default="wavefield")
    parser.add_argument("--title", default="Ez field")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    if len(args.x_values_mm) != len(args.z_values_mm):
        raise ValueError("x and z lists must have the same length")
    if len(args.x_values_mm) != len(args.radius_values_mm):
        raise ValueError("x, z, and radius lists must have the same length")
    if args.save_every <= 0:
        raise ValueError("--save-every must be positive")

    _override_grid(args.grid_step_mm)
    outdir = Path(args.outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    model = build_animation_model(
        args.x_values_mm,
        args.z_values_mm,
        args.radius_values_mm,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        concrete_epsr=args.concrete_epsr,
        concrete_sigma=args.concrete_sigma,
        rebar_epsr=args.rebar_epsr,
        rebar_sigma=args.rebar_sigma,
    )
    time_values = generate_time_array(cfg.NT, cfg.DT)
    wavelet = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=args.frequency_scale,
        time_shift_ps=args.time_shift_ps,
        amplitude_scale=args.amplitude_scale,
    )
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices(args.source_x_mm)

    started = time.time()
    simulator = make_simulator(model, args.backend)
    result = simulator.run(
        wavelet,
        src_iz,
        src_ix,
        rec_iz,
        rec_ix,
        save_fields_every=args.save_every,
    )
    elapsed_s = time.time() - started
    snapshots = result.get("snapshots", [])
    if not snapshots:
        raise ValueError("simulation produced no snapshots")

    animation_path = figures_dir / f"{args.label}_wavefield.gif"
    rebar_specs_mm = [
        (float(x_mm), float(z_mm), float(radius_mm))
        for x_mm, z_mm, radius_mm in zip(args.x_values_mm, args.z_values_mm, args.radius_values_mm)
    ]
    source_receiver_mm = (
        float(args.source_x_mm),
        float(cfg.TX_Z * 1000.0),
        float(args.source_x_mm + cfg.TX_RX_OFFSET * 1000.0),
        float(cfg.RX_Z * 1000.0),
    )
    animate_wavefield(
        snapshots,
        save_path=str(animation_path),
        show=False,
        fps=args.fps,
        rebar_specs_mm=rebar_specs_mm,
        source_receiver_mm=source_receiver_mm,
        title_prefix=args.title,
    )
    validation = validate_animation(animation_path)

    summary = {
        "backend": args.backend,
        "grid_step_mm": float(args.grid_step_mm),
        "x_values_mm": args.x_values_mm,
        "z_values_mm": args.z_values_mm,
        "radius_values_mm": args.radius_values_mm,
        "frequency_ghz": float(args.frequency_ghz),
        "frequency_scale": float(args.frequency_scale),
        "time_shift_ps": float(args.time_shift_ps),
        "amplitude_scale": float(args.amplitude_scale),
        "material": {
            "concrete_epsr": None if args.concrete_epsr is None else float(args.concrete_epsr),
            "concrete_sigma": None if args.concrete_sigma is None else float(args.concrete_sigma),
            "rebar_epsr": None if args.rebar_epsr is None else float(args.rebar_epsr),
            "rebar_sigma": None if args.rebar_sigma is None else float(args.rebar_sigma),
        },
        "source_x_mm": float(args.source_x_mm),
        "receiver_x_mm": float(args.source_x_mm + cfg.TX_RX_OFFSET * 1000.0),
        "source_z_mm": float(cfg.TX_Z * 1000.0),
        "receiver_z_mm": float(cfg.RX_Z * 1000.0),
        "save_every": int(args.save_every),
        "fps": int(args.fps),
        "elapsed_time_s": float(elapsed_s),
        "snapshot_count": len(snapshots),
        "validation": validation,
        "paths": {
            "animation": str(animation_path),
        },
    }
    summary_path = data_dir / f"{args.label}_wavefield_animation_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Wrote animation: {animation_path}")
    print(f"Wrote summary: {summary_path}")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
