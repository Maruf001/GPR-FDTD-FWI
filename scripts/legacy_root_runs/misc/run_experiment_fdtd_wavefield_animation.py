#!/usr/bin/env python3
"""Generate true FDTD wavefield-amplitude GIFs from experiment summaries.

This script runs one representative forward FDTD simulation for an experiment
and saves sparse Ez snapshots as a GIF. It is intended for visualization, not
for optimizer backfill: one Tx/Rx pair is selected from saved acquisition
metadata near the target rebar.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
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
from core.utils import pos_to_index  # noqa: E402
from run_experiment_scene_visualization import scene_from_summary  # noqa: E402
from run_experiment_wave_propagation_animation import choose_representative_pair  # noqa: E402
from run_multi_rebar_common_radius_profile import make_simulator  # noqa: E402
from run_multi_rebar_local_geometry_profile import build_variable_geometry_model  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_polish import observed_wavelet  # noqa: E402
from run_wavefield_animation import validate_animation  # noqa: E402
from visualization.plot_wavefield import animate_wavefield  # noqa: E402


def select_replication_case(summary, case_label=None):
    """Return the selected source/noise case from a coordinate summary."""
    cases = list(summary.get("replication_cases") or [])
    if not cases:
        return {
            "label": "nominal_source_no_observed_noise",
            "frequency_scale": 1.0,
            "time_shift_ps": 0.0,
            "amplitude_scale": 1.0,
            "noise_fraction": 0.0,
            "noise_seed": None,
            "ringdown_scale": 0.0,
            "ringdown_delay_ps": 180.0,
            "ringdown_frequency_scale": 0.8,
        }
    if case_label is None:
        return dict(cases[0])
    for case in cases:
        if case.get("label") == case_label:
            return dict(case)
    raise ValueError(f"case label not found: {case_label}")


def geometry_arrays_from_summary(summary, model_state="truth"):
    """Return x/z/r arrays in millimetres for the requested model state."""
    if model_state == "truth":
        x_values = summary.get("true_x_values_mm", [])
        z_values = summary.get("true_z_values_mm", [])
        radii = summary.get("truth_radius_values_mm", [])
    else:
        state = summary.get(f"{model_state}_state") or {}
        x_values = state.get("x_values_mm", [])
        z_values = state.get("z_values_mm", [])
        radii = state.get("radii_mm", [])

    if not x_values or not z_values or not radii:
        raise ValueError(f"summary has no {model_state} geometry")
    if len(x_values) != len(z_values) or len(x_values) != len(radii):
        raise ValueError(f"{model_state} x, z, and radius arrays must have the same length")
    return [float(v) for v in x_values], [float(v) for v in z_values], [float(v) for v in radii]


def representative_pair_from_summary(summary, summary_path=None):
    """Choose the representative Tx/Rx pair from scene metadata."""
    scene = scene_from_summary(summary, summary_path=summary_path)
    pair = choose_representative_pair(scene)
    return {
        "tx_x_mm": float(pair["tx_x_mm"]),
        "rx_x_mm": float(pair["rx_x_mm"]),
        "tx_z_mm": float(pair["tx_z_mm"]),
        "rx_z_mm": float(pair["rx_z_mm"]),
        "target_rebar_index": int(pair["target_rebar_index"]),
    }


def source_receiver_indices_for_pair(pair, receiver_sampling="nearest"):
    """Return FDTD grid indices for one summary-selected Tx/Rx pair."""
    src_x_m = float(pair["tx_x_mm"]) / 1000.0
    rx_x_m = min(float(pair["rx_x_mm"]) / 1000.0, cfg.DOMAIN_X - cfg.DX)
    src_iz = pos_to_index(float(pair["tx_z_mm"]) / 1000.0, cfg.DZ, cfg.NPML)
    rec_iz = pos_to_index(float(pair["rx_z_mm"]) / 1000.0, cfg.DZ, cfg.NPML)
    src_ix = pos_to_index(src_x_m, cfg.DX, cfg.NPML)
    if receiver_sampling == "linear":
        rec_cell = rx_x_m / cfg.DX
        left_cell = int(np.floor(rec_cell))
        weight_right = float(rec_cell - left_cell)
        rec_ix_left = left_cell + cfg.NPML
        rec_ix_right = min(rec_ix_left + 1, cfg.NX - cfg.NPML - 1)
        rec_ix = (rec_ix_left, rec_ix_right, min(max(weight_right, 0.0), 1.0))
    else:
        rec_ix = pos_to_index(rx_x_m, cfg.DX, cfg.NPML)
        rec_ix = min(rec_ix, cfg.NX - cfg.NPML - 1)
    return src_iz, src_ix, rec_iz, rec_ix


def _snapshot_amplitude_metrics(snapshots):
    cropped = [np.asarray(frame[cfg.NPML:-cfg.NPML, cfg.NPML:-cfg.NPML]) for _, frame in snapshots]
    if not cropped:
        raise ValueError("no snapshots available for amplitude metrics")
    peaks = [float(np.max(np.abs(frame))) for frame in cropped]
    rms = [float(np.sqrt(np.mean(frame ** 2))) for frame in cropped]
    return {
        "peak_abs_ez": float(max(peaks)),
        "max_rms_ez": float(max(rms)),
        "nonzero_frames": int(sum(peak > 0.0 for peak in peaks)),
    }


def compact_animation_title(summary, outdir, pair):
    """Return a short title that fits inside wavefield animation frames."""
    match = re.match(r"(\d+)_", Path(outdir).name)
    run_id = match.group(1) if match else "run"
    target = int(pair["target_rebar_index"])
    return (
        f"FDTD Ez wavefield | run {run_id} target {target} | "
        f"Tx {pair['tx_x_mm']:.0f} mm, Rx {pair['rx_x_mm']:.0f} mm"
    )


def _upsert_figure_notes(figures_dir, figure_name, summary_name):
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    start = "<!-- fdtd_wavefield_amplitude:start -->"
    end = "<!-- fdtd_wavefield_amplitude:end -->"
    section = f"""{start}
## `{figure_name}` - true FDTD wavefield amplitude animation

This GIF shows sparse Ez wavefield snapshots from one representative forward
FDTD simulation using the saved experiment geometry and source settings. The
Tx/Rx pair is selected from the run's acquisition list near the target rebar,
so it is a physical wavefield view for that scenario, not the earlier
straight-ray schematic. Observed-data noise is not injected into this field
animation because that noise is added after forward simulation to B-scans.

Validation, source settings, grid settings, and selected Tx/Rx metadata are
saved in `../data/{summary_name}`.
{end}
"""
    text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else "# Figure Notes\n"
    pattern = re.compile(rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?", flags=re.DOTALL)
    text = pattern.sub("\n", text).rstrip() + "\n\n" + section
    notes_path.write_text(text, encoding="utf-8")
    return str(notes_path)


def infer_outdir(summary_path, outdir):
    if outdir:
        return Path(outdir)
    path = Path(summary_path)
    if path.parent.name == "data":
        return path.parent.parent
    return path.parent


def write_fdtd_wavefield_artifacts(
        summary,
        outdir,
        summary_path=None,
        case_label=None,
        model_state="truth",
        label="fdtd_wavefield_amplitude",
        backend="cpu",
        grid_step_mm=None,
        frames=42,
        save_every=None,
        fps=12,
        geometry_mode="hard",
        subcell_samples=5,
        max_updates=1.2e9,
        update_notes=True):
    """Run one representative FDTD simulation and write animation artifacts."""
    outdir = Path(outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    grid_step_mm = float(summary.get("grid_step_mm", 1.0) if grid_step_mm is None else grid_step_mm)
    _override_grid(grid_step_mm)
    work_estimate = int(cfg.NX * cfg.NZ * cfg.NT)
    if work_estimate > float(max_updates):
        raise ValueError(
            f"FDTD work estimate {work_estimate} cell-steps exceeds max_updates={max_updates:g}"
        )

    x_values, z_values, radii = geometry_arrays_from_summary(summary, model_state=model_state)
    case = select_replication_case(summary, case_label=case_label)
    pair = representative_pair_from_summary(summary, summary_path=summary_path)
    receiver_sampling = summary.get("receiver_sampling") or "nearest"
    if receiver_sampling not in ("nearest", "linear"):
        receiver_sampling = "nearest"
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices_for_pair(
        pair,
        receiver_sampling=receiver_sampling,
    )

    model = build_variable_geometry_model(
        x_values,
        z_values,
        radii,
        geometry_mode=geometry_mode,
        subcell_samples=int(subcell_samples),
    )
    time_values = generate_time_array(cfg.NT, cfg.DT)
    frequency_ghz = float(summary.get("frequency_ghz", cfg.F_CENTER / 1.0e9))
    wavelet = observed_wavelet(
        time_values,
        frequency_ghz * 1.0e9,
        frequency_scale=float(case.get("frequency_scale", 1.0)),
        time_shift_ps=float(case.get("time_shift_ps", 0.0)),
        amplitude_scale=float(case.get("amplitude_scale", 1.0)),
        ringdown_scale=float(case.get("ringdown_scale", 0.0)),
        ringdown_delay_ps=float(case.get("ringdown_delay_ps", 180.0)),
        ringdown_frequency_scale=float(case.get("ringdown_frequency_scale", 0.8)),
    )
    if save_every is None:
        save_every = max(1, int(np.floor(cfg.NT / max(1, int(frames)))))
    save_every = int(save_every)
    if save_every <= 0:
        raise ValueError("save_every must be positive")

    started = time.time()
    simulator = make_simulator(model, backend)
    result = simulator.run(
        wavelet,
        src_iz,
        src_ix,
        rec_iz,
        rec_ix,
        save_fields_every=save_every,
    )
    elapsed_s = time.time() - started
    snapshots = result.get("snapshots", [])
    if not snapshots:
        raise ValueError("simulation produced no snapshots")

    animation_path = figures_dir / f"{label}.gif"
    rebar_specs_mm = list(zip(x_values, z_values, radii))
    source_receiver_mm = (
        float(pair["tx_x_mm"]),
        float(pair["tx_z_mm"]),
        float(pair["rx_x_mm"]),
        float(pair["rx_z_mm"]),
    )
    title = compact_animation_title(summary, outdir, pair)
    animate_wavefield(
        snapshots,
        save_path=str(animation_path),
        show=False,
        fps=int(fps),
        rebar_specs_mm=rebar_specs_mm,
        source_receiver_mm=source_receiver_mm,
        title_prefix=title,
    )
    validation = validate_animation(animation_path)
    amplitude = _snapshot_amplitude_metrics(snapshots)
    validation = {**validation, **amplitude}

    summary_name = f"{label}_summary.json"
    payload = {
        "animation_type": "true FDTD Ez wavefield amplitude",
        "source": "coordinate optimizer summary",
        "summary_path": None if summary_path is None else str(summary_path),
        "run_name": summary.get("run_name", ""),
        "model_state": model_state,
        "backend": backend,
        "grid": {
            "grid_step_mm": grid_step_mm,
            "nx": int(cfg.NX),
            "nz": int(cfg.NZ),
            "nt": int(cfg.NT),
            "dt_s": float(cfg.DT),
            "npml": int(cfg.NPML),
            "work_estimate_cell_steps": work_estimate,
        },
        "geometry": {
            "x_values_mm": x_values,
            "z_values_mm": z_values,
            "radius_values_mm": radii,
            "geometry_mode": geometry_mode,
            "subcell_samples": int(subcell_samples),
        },
        "representative_pair": pair,
        "receiver_sampling": receiver_sampling,
        "case": case,
        "noise_policy": (
            "Observed-data noise is not injected into the wavefield animation; "
            "the GIF shows the clean forward FDTD field for the configured source."
        ),
        "save_every": save_every,
        "requested_frames": int(frames),
        "snapshot_count": len(snapshots),
        "fps": int(fps),
        "elapsed_time_s": float(elapsed_s),
        "validation": validation,
        "paths": {
            "animation": str(animation_path),
        },
    }
    summary_path_out = data_dir / summary_name
    summary_path_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    notes_path = None
    if update_notes:
        notes_path = _upsert_figure_notes(figures_dir, animation_path.name, summary_name)
    return {
        "animation": str(animation_path),
        "summary": str(summary_path_out),
        "figure_notes": notes_path,
        "validation": validation,
        "elapsed_time_s": float(elapsed_s),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--case-label", default=None)
    parser.add_argument("--model-state", choices=["truth", "initial", "final"], default="truth")
    parser.add_argument("--label", default="fdtd_wavefield_amplitude")
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="cpu")
    parser.add_argument("--grid-step-mm", type=float, default=None)
    parser.add_argument("--frames", type=int, default=42)
    parser.add_argument("--save-every", type=int, default=None)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--max-updates", type=float, default=1.2e9)
    parser.add_argument("--skip-figure-notes", action="store_true")
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    artifacts = write_fdtd_wavefield_artifacts(
        summary,
        infer_outdir(args.summary, args.outdir),
        summary_path=args.summary,
        case_label=args.case_label,
        model_state=args.model_state,
        label=args.label,
        backend=args.backend,
        grid_step_mm=args.grid_step_mm,
        frames=args.frames,
        save_every=args.save_every,
        fps=args.fps,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        max_updates=args.max_updates,
        update_notes=not args.skip_figure_notes,
    )
    print(f"Wrote FDTD wavefield animation: {artifacts['animation']}")
    print(f"Wrote FDTD wavefield summary: {artifacts['summary']}")
    if artifacts["figure_notes"] is not None:
        print(f"Updated figure notes: {artifacts['figure_notes']}")
    print(json.dumps(artifacts["validation"], indent=2))


if __name__ == "__main__":
    main()
