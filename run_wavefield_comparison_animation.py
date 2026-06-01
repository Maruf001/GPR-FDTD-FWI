#!/usr/bin/env python3
"""Generate side-by-side true-vs-candidate FDTD wavefield animations."""

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

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation  # noqa: E402
import matplotlib.patches as patches  # noqa: E402

import config as cfg  # noqa: E402
from core.source import generate_time_array  # noqa: E402
from run_multi_rebar_common_radius_profile import make_simulator  # noqa: E402
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    parse_vector_mm,
)
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import observed_wavelet  # noqa: E402
from run_wavefield_animation import source_receiver_indices, validate_animation  # noqa: E402
from visualization.plot_style import safe_symmetric_limits  # noqa: E402


def validate_same_length(name, x_values_mm, z_values_mm, radius_values_mm):
    if len(x_values_mm) != len(z_values_mm) or len(x_values_mm) != len(radius_values_mm):
        raise ValueError(f"{name} x, z, and radius lists must have the same length")


def simulate_snapshots(
        backend,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        wavelet,
        source_x_mm,
        save_every,
        geometry_mode,
        subcell_samples):
    """Run one model and return sparse Ez snapshots."""
    model = build_variable_geometry_model(
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        geometry_mode=geometry_mode,
        subcell_samples=subcell_samples,
    )
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices(source_x_mm)
    simulator = make_simulator(model, backend)
    result = simulator.run(
        wavelet,
        src_iz,
        src_ix,
        rec_iz,
        rec_ix,
        save_fields_every=save_every,
    )
    snapshots = result.get("snapshots", [])
    if not snapshots:
        raise ValueError("simulation produced no snapshots")
    return snapshots


def _cropped_frame(snapshot):
    n = cfg.NPML
    return np.asarray(snapshot[1][n:-n, n:-n], dtype=np.float64)


def comparison_frame_count(truth_snapshots, candidate_snapshots):
    """Return the number of paired frames usable for comparison."""
    return min(len(truth_snapshots), len(candidate_snapshots))


def source_parameters_from_args(args, prefix):
    """Return source parameters, falling back to common legacy values."""
    frequency_scale = getattr(args, f"{prefix}_frequency_scale")
    time_shift_ps = getattr(args, f"{prefix}_time_shift_ps")
    amplitude_scale = getattr(args, f"{prefix}_amplitude_scale")
    return {
        "frequency_scale": float(args.frequency_scale if frequency_scale is None else frequency_scale),
        "time_shift_ps": float(args.time_shift_ps if time_shift_ps is None else time_shift_ps),
        "amplitude_scale": float(args.amplitude_scale if amplitude_scale is None else amplitude_scale),
    }


def _draw_overlays(ax, rebar_specs_mm, source_receiver_mm):
    for x_mm, z_mm, radius_mm in rebar_specs_mm:
        ax.add_patch(patches.Circle(
            (float(x_mm), float(z_mm)),
            float(radius_mm),
            linewidth=1,
            edgecolor="black",
            facecolor="none",
        ))
    src_x, src_z, rec_x, rec_z = source_receiver_mm
    ax.scatter(
        [src_x],
        [src_z],
        marker="^",
        s=44,
        color="#1b7837",
        edgecolor="black",
        linewidth=0.5,
        label="Tx",
        zorder=4,
    )
    ax.scatter(
        [rec_x],
        [rec_z],
        marker="v",
        s=44,
        color="#762a83",
        edgecolor="black",
        linewidth=0.5,
        label="Rx",
        zorder=4,
    )
    ax.axhline(y=cfg.CONCRETE_TOP * 1000.0, color="gray", linestyle="--", linewidth=0.5)


def animate_comparison(
        truth_snapshots,
        candidate_snapshots,
        save_path,
        truth_rebars_mm,
        candidate_rebars_mm,
        source_receiver_mm,
        title,
        fps=12):
    """Save a true/candidate/difference wavefield comparison GIF."""
    frame_count = comparison_frame_count(truth_snapshots, candidate_snapshots)
    if frame_count <= 0:
        raise ValueError("no paired snapshots to compare")

    first = _cropped_frame(truth_snapshots[0])
    x_extent = cfg.DX * 1000.0 * first.shape[1]
    z_extent = cfg.DZ * 1000.0 * first.shape[0]
    extent = [0.0, x_extent, z_extent, 0.0]

    truth_frames = [_cropped_frame(snapshot) for snapshot in truth_snapshots[:frame_count]]
    candidate_frames = [_cropped_frame(snapshot) for snapshot in candidate_snapshots[:frame_count]]
    diff_frames = [
        candidate - truth
        for truth, candidate in zip(truth_frames, candidate_frames)
    ]

    vmin, vmax = safe_symmetric_limits(truth_frames + candidate_frames, percentile=99.5)
    dmin, dmax = safe_symmetric_limits(diff_frames, percentile=99.5)

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.6), constrained_layout=True)
    panels = [
        (axes[0], truth_frames[0], "True model", vmin, vmax, truth_rebars_mm),
        (axes[1], candidate_frames[0], "Candidate model", vmin, vmax, candidate_rebars_mm),
        (axes[2], diff_frames[0], "Candidate - true", dmin, dmax, candidate_rebars_mm),
    ]
    images = []
    for ax, data, panel_title, lo, hi, rebars in panels:
        im = ax.imshow(data, cmap="RdBu_r", extent=extent, vmin=lo, vmax=hi, aspect="equal")
        ax.set_title(panel_title, fontsize=11, fontweight="bold")
        ax.set_xlabel("x [mm]")
        ax.set_ylabel("z [mm]")
        _draw_overlays(ax, rebars, source_receiver_mm)
        images.append(im)
    axes[0].legend(loc="upper right", fontsize=8, frameon=True)
    fig.colorbar(images[0], ax=axes[:2], shrink=0.82, label="Ez [V/m]")
    fig.colorbar(images[2], ax=axes[2], shrink=0.82, label="Delta Ez [V/m]")
    suptitle = fig.suptitle("", fontsize=13, fontweight="bold")

    def update(frame_index):
        images[0].set_data(truth_frames[frame_index])
        images[1].set_data(candidate_frames[frame_index])
        images[2].set_data(diff_frames[frame_index])
        step = truth_snapshots[frame_index][0]
        t_ns = step * cfg.DT * 1e9
        suptitle.set_text(f"{title}: t = {t_ns:.2f} ns (step {step})")
        return [*images, suptitle]

    animation = FuncAnimation(
        fig,
        update,
        frames=frame_count,
        interval=1000 // int(fps),
        blit=False,
    )
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    animation.save(str(save_path), writer="pillow", fps=int(fps))
    plt.close(fig)
    return str(save_path)


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
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--frequency-scale", type=float, default=1.0)
    parser.add_argument("--time-shift-ps", type=float, default=0.0)
    parser.add_argument("--amplitude-scale", type=float, default=1.0)
    parser.add_argument("--truth-frequency-scale", type=float, default=None)
    parser.add_argument("--truth-time-shift-ps", type=float, default=None)
    parser.add_argument("--truth-amplitude-scale", type=float, default=None)
    parser.add_argument("--candidate-frequency-scale", type=float, default=None)
    parser.add_argument("--candidate-time-shift-ps", type=float, default=None)
    parser.add_argument("--candidate-amplitude-scale", type=float, default=None)
    parser.add_argument("--source-x-mm", type=float, required=True)
    parser.add_argument("--save-every", type=int, default=80)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--label", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    validate_same_length(
        "truth",
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        args.truth_radius_values_mm,
    )
    validate_same_length(
        "candidate",
        args.candidate_x_values_mm,
        args.candidate_z_values_mm,
        args.candidate_radius_values_mm,
    )
    if args.save_every <= 0:
        raise ValueError("--save-every must be positive")

    _override_grid(args.grid_step_mm)
    outdir = Path(args.outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    time_values = generate_time_array(cfg.NT, cfg.DT)
    truth_source = source_parameters_from_args(args, "truth")
    candidate_source = source_parameters_from_args(args, "candidate")
    truth_wavelet = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=truth_source["frequency_scale"],
        time_shift_ps=truth_source["time_shift_ps"],
        amplitude_scale=truth_source["amplitude_scale"],
    )
    candidate_wavelet = observed_wavelet(
        time_values,
        args.frequency_ghz * 1e9,
        frequency_scale=candidate_source["frequency_scale"],
        time_shift_ps=candidate_source["time_shift_ps"],
        amplitude_scale=candidate_source["amplitude_scale"],
    )

    started = time.time()
    truth_snapshots = simulate_snapshots(
        args.backend,
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        args.truth_radius_values_mm,
        truth_wavelet,
        args.source_x_mm,
        args.save_every,
        args.geometry_mode,
        args.subcell_samples,
    )
    candidate_snapshots = simulate_snapshots(
        args.backend,
        args.candidate_x_values_mm,
        args.candidate_z_values_mm,
        args.candidate_radius_values_mm,
        candidate_wavelet,
        args.source_x_mm,
        args.save_every,
        args.geometry_mode,
        args.subcell_samples,
    )
    elapsed_s = time.time() - started

    truth_rebars = list(zip(
        args.truth_x_values_mm,
        args.truth_z_values_mm,
        args.truth_radius_values_mm,
    ))
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
    animation_path = figures_dir / f"{args.label}_comparison.gif"
    animate_comparison(
        truth_snapshots,
        candidate_snapshots,
        animation_path,
        truth_rebars,
        candidate_rebars,
        source_receiver_mm,
        args.title,
        fps=args.fps,
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
        "frequency_ghz": float(args.frequency_ghz),
        "frequency_scale": float(args.frequency_scale),
        "time_shift_ps": float(args.time_shift_ps),
        "amplitude_scale": float(args.amplitude_scale),
        "truth_source": truth_source,
        "candidate_source": candidate_source,
        "source_x_mm": float(args.source_x_mm),
        "receiver_x_mm": float(args.source_x_mm + cfg.TX_RX_OFFSET * 1000.0),
        "source_z_mm": float(cfg.TX_Z * 1000.0),
        "receiver_z_mm": float(cfg.RX_Z * 1000.0),
        "save_every": int(args.save_every),
        "fps": int(args.fps),
        "elapsed_time_s": float(elapsed_s),
        "truth_snapshot_count": len(truth_snapshots),
        "candidate_snapshot_count": len(candidate_snapshots),
        "paired_frame_count": comparison_frame_count(truth_snapshots, candidate_snapshots),
        "validation": validation,
        "paths": {
            "animation": str(animation_path),
        },
    }
    summary_path = data_dir / f"{args.label}_comparison_animation_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(f"Wrote comparison animation: {animation_path}")
    print(f"Wrote summary: {summary_path}")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
