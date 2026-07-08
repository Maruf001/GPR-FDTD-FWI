#!/usr/bin/env python3
"""Run detector-seeded coarse-to-fine single-rebar refinement.

This runner packages the manual experiment pattern from runs 116-117:

1. detect likely one-rebar x/z seed windows from a B-scan,
2. run a cheap 2 mm source-profiled geometry/radius screen,
3. run a narrow 1 mm source-profiled polish around the coarse winner.

The current runner is single-rebar only. Multi-rebar refinement still uses the
separate local multi-rebar profile and coordinate-optimizer scripts.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402


DEFAULT_TRUTH_X_MM = 250.0
DEFAULT_TRUTH_Z_MM = 90.0
DEFAULT_TRUTH_RADIUS_MM = 6.0


def format_number(value):
    """Format a numeric CLI value without noisy floating-point tails."""
    value = float(value)
    if abs(value) < 5e-11:
        value = 0.0
    return f"{value:.10g}"


def format_values_arg(values):
    """Format a list of numeric values for comma-separated runner arguments."""
    return ",".join(format_number(value) for value in values)


def axis_values_mm(center_mm, half_window_mm, step_mm, min_value_mm=None, max_value_mm=None):
    """Build an inclusive millimeter axis centered on a selected candidate."""
    center = float(center_mm)
    half_window = float(half_window_mm)
    step = float(step_mm)
    if half_window < 0.0:
        raise ValueError("half_window_mm must be non-negative")
    if step <= 0.0:
        raise ValueError("step_mm must be positive")

    start = center - half_window
    stop = center + half_window
    if min_value_mm is not None:
        start = max(start, float(min_value_mm))
    if max_value_mm is not None:
        stop = min(stop, float(max_value_mm))
    if stop < start:
        raise ValueError("axis bounds are empty after clipping")

    count = int(math.floor((stop - start) / step + 1e-9)) + 1
    values = [round(start + step * index, 10) for index in range(count)]
    if not values or values[-1] < stop - 1e-8:
        values.append(round(stop, 10))
    return values


def load_json(path):
    """Load a JSON file from a path-like object."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def select_detection_candidate(detection_summary, rank):
    """Return a detection candidate by one-based rank."""
    for candidate in detection_summary.get("candidates", []):
        if int(candidate["rank"]) == int(rank):
            return candidate
    raise ValueError(f"detection rank {rank} not found")


def best_source_profiled_candidate(summary):
    """Return the best source-profiled candidate from a polish summary."""
    candidates = summary.get("top_candidates", [])
    if not candidates:
        raise ValueError("source-profiled summary has no top_candidates")
    return min(candidates, key=lambda item: float(item["misfit"]))


def format_metric(value):
    """Format a metric compactly for plain-language figure notes."""
    if value is None:
        return "not available"
    try:
        return f"{float(value):.6g}"
    except (TypeError, ValueError):
        return str(value)


def build_detection_command(args, outdir):
    """Build the detector subprocess command."""
    command = [
        sys.executable,
        "-u",
        "run_rebar_detection_pipeline.py",
        "--backend",
        args.backend,
        "--grid-step-mm",
        format_number(args.detection_grid_step_mm),
        "--scan-step-mm",
        format_number(args.detection_scan_step_mm),
        "--frequency-ghz",
        format_number(args.frequency_ghz),
        "--truth-x-values-mm",
        format_number(args.truth_x_mm),
        "--truth-z-values-mm",
        format_number(args.truth_z_mm),
        "--truth-radius-values-mm",
        format_number(args.truth_radius_mm),
        "--frequency-scale",
        format_number(args.observed_frequency_scale),
        "--time-shift-ps",
        format_number(args.observed_time_shift_ps),
        "--amplitude-scale",
        format_number(args.observed_amplitude_scale),
        "--noise-fraction",
        format_number(args.observed_noise_rms_fraction),
        "--noise-seed",
        str(args.noise_seed),
        "--detector-x-values-mm",
        args.detector_x_values_mm,
        "--detector-z-values-mm",
        args.detector_z_values_mm,
        "--detector-time-offset-ps-values",
        args.detector_time_offset_ps_values,
        "--geometry-mode",
        args.detection_geometry_mode,
        "--subcell-samples",
        str(args.detection_subcell_samples),
        "--top-k",
        str(args.detector_top_k),
        "--window-half-x-mm",
        format_number(args.detector_window_half_x_mm),
        "--window-half-z-mm",
        format_number(args.detector_window_half_z_mm),
        "--run-name",
        "detection_stage",
        "--outdir",
        str(outdir),
    ]
    if args.detection_sources is not None:
        command.extend(["--sources", str(args.detection_sources)])
    return command


def build_polish_command(
        args,
        outdir,
        run_name,
        grid_step_mm,
        x_values_mm,
        z_values_mm,
        radius_values_mm,
        progress_every,
        sources=None,
        geometry_mode=None,
        subcell_samples=None,
        base_frequency_ghz=None,
        frequencies_ghz=None,
        frequency_weights=None):
    """Build a source-profiled polish subprocess command."""
    sources = args.refinement_sources if sources is None else sources
    geometry_mode = args.refinement_geometry_mode if geometry_mode is None else geometry_mode
    subcell_samples = args.refinement_subcell_samples if subcell_samples is None else subcell_samples
    base_frequency_ghz = args.frequency_ghz if base_frequency_ghz is None else base_frequency_ghz
    frequencies_ghz = args.refinement_frequencies_ghz if frequencies_ghz is None else frequencies_ghz
    frequency_weights = args.refinement_frequency_weights if frequency_weights is None else frequency_weights
    command = [
        sys.executable,
        "-u",
        "run_single_rebar_source_profiled_polish.py",
        "--backend",
        args.backend,
        "--grid-step-mm",
        format_number(grid_step_mm),
        "--sources",
        str(sources),
        "--frequency-ghz",
        format_number(base_frequency_ghz),
        "--truth-x-mm",
        format_number(args.truth_x_mm),
        "--truth-z-mm",
        format_number(args.truth_z_mm),
        "--truth-radius-mm",
        format_number(args.truth_radius_mm),
        "--x-values-mm",
        format_values_arg(x_values_mm),
        "--z-values-mm",
        format_values_arg(z_values_mm),
        "--radius-values-mm",
        format_values_arg(radius_values_mm),
        "--source-frequency-scales",
        args.source_frequency_scales,
        f"--source-time-shift-ps-values={args.source_time_shift_ps_values}",
        "--observed-frequency-scale",
        format_number(args.observed_frequency_scale),
        "--observed-time-shift-ps",
        format_number(args.observed_time_shift_ps),
        "--observed-amplitude-scale",
        format_number(args.observed_amplitude_scale),
        "--observed-noise-rms-fraction",
        format_number(args.observed_noise_rms_fraction),
        "--noise-seed",
        str(args.noise_seed),
        "--geometry-mode",
        geometry_mode,
        "--subcell-samples",
        str(subcell_samples),
        "--top-k",
        str(args.refinement_top_k),
        "--progress-every",
        str(progress_every),
        "--run-name",
        run_name,
        "--outdir",
        str(outdir),
    ]
    if frequencies_ghz is not None:
        command.extend(["--frequencies-ghz", frequencies_ghz])
    if frequency_weights is not None:
        command.extend(["--frequency-weights", frequency_weights])
    if args.fit_amplitude:
        command.append("--fit-amplitude")
    return command


def build_material_uncertainty_command(args, outdir, x_mm, z_mm, radius_values_mm):
    """Build a bounded material/source uncertainty subprocess command."""
    frequency_ghz = (
        args.material_uncertainty_frequency_ghz
        if args.material_uncertainty_frequency_ghz is not None
        else args.highband_frequency_ghz if args.enable_highband_polish
        else args.frequency_ghz
    )
    command = [
        sys.executable,
        "-u",
        "run_single_rebar_material_tradeoff.py",
        "--backend",
        args.backend,
        "--grid-step-mm",
        format_number(args.material_uncertainty_grid_step_mm),
        "--sources",
        str(args.material_uncertainty_sources),
        "--frequency-ghz",
        format_number(frequency_ghz),
        "--truth-x-mm",
        format_number(args.truth_x_mm),
        "--truth-z-mm",
        format_number(args.truth_z_mm),
        "--truth-radius-mm",
        format_number(args.truth_radius_mm),
        "--x-mm",
        format_number(x_mm),
        "--z-mm",
        format_number(z_mm),
        "--radius-values-mm",
        format_values_arg(radius_values_mm),
        "--concrete-epsr-values",
        args.material_uncertainty_concrete_epsr_values,
        "--rebar-log10-sigma-values",
        args.material_uncertainty_rebar_log10_sigma_values,
        "--source-frequency-scales",
        args.source_frequency_scales,
        f"--source-time-shift-ps-values={args.source_time_shift_ps_values}",
        "--observed-frequency-scale",
        format_number(args.observed_frequency_scale),
        "--observed-time-shift-ps",
        format_number(args.observed_time_shift_ps),
        "--observed-amplitude-scale",
        format_number(args.observed_amplitude_scale),
        "--observed-noise-rms-fraction",
        format_number(args.observed_noise_rms_fraction),
        "--noise-seed",
        str(args.noise_seed),
        "--geometry-mode",
        args.material_uncertainty_geometry_mode,
        "--subcell-samples",
        str(args.material_uncertainty_subcell_samples),
        "--top-k",
        str(args.material_uncertainty_top_k),
        "--progress-every",
        str(args.material_uncertainty_progress_every),
        "--run-name",
        "material_uncertainty",
        "--outdir",
        str(outdir),
    ]
    if args.fit_amplitude:
        command.append("--fit-amplitude")
    return command


def build_radius_uncertainty_report_command(
        args,
        outdir,
        nominal_summary_path,
        material_summary_path):
    """Build the nominal-vs-material/source uncertainty report command."""
    return [
        sys.executable,
        "-u",
        "run_radius_uncertainty_report.py",
        "--run-name",
        "radius_uncertainty_report",
        "--case",
        args.material_uncertainty_case_label,
        str(nominal_summary_path),
        str(material_summary_path),
        "--outdir",
        str(outdir),
    ]


def run_subprocess(command):
    """Run a child command and return wall-clock seconds."""
    print("Running:")
    print("  " + " ".join(command))
    started = time.time()
    completed = subprocess.run(command, check=False)
    elapsed_s = time.time() - started
    if completed.returncode != 0:
        raise RuntimeError(f"command failed with code {completed.returncode}: {' '.join(command)}")
    return elapsed_s


def write_detection_figure_notes(figures_dir, summary, candidate_rank):
    """Write plain-language notes for the detection overlay."""
    figures_path = Path(figures_dir)
    figures_path.mkdir(parents=True, exist_ok=True)
    candidate = select_detection_candidate(summary, candidate_rank)
    truth_x = summary["truth_x_values_mm"][0]
    truth_z = summary["truth_z_values_mm"][0]
    match = summary["match_metrics"][0] if summary.get("match_metrics") else {}
    text = f"""# Figure Notes

## 1. `detection_overlay.png` - detector seed used for refinement

This figure shows a B-scan, meaning a radar image built from one time trace at
each scan position along the concrete surface. The color shows signal
amplitude. Curved lines are the detector's likely rebar reflection paths, and
the dashed black curve marks the known synthetic truth.

The packaged runner used detection rank `{candidate_rank}` as the refinement
seed: `x={candidate['x_mm']:.1f} mm`, `z={candidate['z_mm']:.1f} mm`, detector
time offset `{candidate['time_offset_ps']:.1f} ps`. The truth is
`x={truth_x:.1f} mm`, `z={truth_z:.1f} mm`.

Main result: the selected seed has `x` error
`{float(match.get('x_error_mm', 0.0)):.1f} mm` and `z` error
`{float(match.get('z_error_mm', 0.0)):.1f} mm` for the known rebar. This is
the first figure to inspect because every later FWI refinement step depends on
whether this seed window contains the true target. FWI means full-waveform
inversion: candidate simulations are compared against the observed traces.
"""
    (figures_path / "FIGURE_NOTES.md").write_text(text, encoding="utf-8")


def write_polish_figure_notes(figures_dir, summary, stage_title, stage_purpose):
    """Write plain-language notes for a source-profiled radius plot."""
    figures_path = Path(figures_dir)
    figures_path.mkdir(parents=True, exist_ok=True)
    best = best_source_profiled_candidate(summary)
    margin = summary.get("margin", {})
    source_grid = summary.get("source_profile_grid", {})
    frequency_plot = summary.get("paths", {}).get("frequency_radius_profile_plot")
    text = f"""# Figure Notes

## 1. `source_profiled_radius_profile.png` - {stage_title}

This plot shows the best full-waveform inversion objective value found for each
tested rebar radius. FWI means full-waveform inversion: the code simulates
radar traces for each candidate and compares them with the observed traces.
Lower objective values mean better waveform agreement.

This stage is {stage_purpose}. "Source-profiled" means the comparison also
tests small source-wavelet changes instead of forcing geometry or radius to
explain source uncertainty. The source grid was frequency scales
`{source_grid.get('frequency_scales')}`, time shifts in picoseconds
`{source_grid.get('time_shift_ps_values')}`, and fitted amplitude
`{source_grid.get('fit_amplitude')}`.

Main result: the best candidate is `x={best['params']['x_mm']:.1f} mm`,
`z={best['params']['z_mm']:.1f} mm`, `r={best['params']['radius_mm']:.1f} mm`.
The best-radius margin is `{format_metric(margin.get('radius_margin_abs'))}`, which is the
objective gap between the best radius and the next tested radius. A larger
margin is a clearer radius decision; a zero or tiny margin means this stage is
ambiguous and should be treated as a screen rather than a final answer.
"""
    if frequency_plot:
        text += """
## 2. `source_profiled_frequency_radius_profile.png` - frequency-term decomposition

This plot is shown for multifrequency runs. It uses the same candidate chosen
by the combined objective at each radius, then draws the contribution from each
base frequency. It is a diagnostic decomposition, not a separate optimizer.

Use this figure to decide whether one frequency is carrying useful radius
separation or only adding cost and mismatch. If the per-frequency curves do not
separate the correct radius better than the combined curve, another full
multifrequency grid is not justified without a better weighting rule.
"""
    (figures_path / "FIGURE_NOTES.md").write_text(text, encoding="utf-8")


def write_summary(path, summary):
    """Write the root summary JSON."""
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["gpu-cpml", "cpu", "auto"], default="gpu-cpml")
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--truth-x-mm", type=float, default=DEFAULT_TRUTH_X_MM)
    parser.add_argument("--truth-z-mm", type=float, default=DEFAULT_TRUTH_Z_MM)
    parser.add_argument("--truth-radius-mm", type=float, default=DEFAULT_TRUTH_RADIUS_MM)
    parser.add_argument("--observed-frequency-scale", type=float, default=1.0)
    parser.add_argument("--observed-time-shift-ps", type=float, default=0.0)
    parser.add_argument("--observed-amplitude-scale", type=float, default=1.0)
    parser.add_argument("--observed-noise-rms-fraction", type=float, default=0.0)
    parser.add_argument("--noise-seed", type=int, default=13)

    parser.add_argument("--detection-grid-step-mm", type=float, default=2.0)
    parser.add_argument("--detection-scan-step-mm", type=float, default=4.0)
    parser.add_argument("--detection-sources", type=int, default=None)
    parser.add_argument("--detector-x-values-mm", default="150:350:4")
    parser.add_argument("--detector-z-values-mm", default="65:125:5")
    parser.add_argument("--detector-time-offset-ps-values", default="400,500,600,667")
    parser.add_argument("--detector-top-k", type=int, default=5)
    parser.add_argument("--detector-candidate-rank", type=int, default=1)
    parser.add_argument("--detector-window-half-x-mm", type=float, default=24.0)
    parser.add_argument("--detector-window-half-z-mm", type=float, default=24.0)
    parser.add_argument("--detection-geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--detection-subcell-samples", type=int, default=5)

    parser.add_argument("--refinement-sources", type=int, default=5)
    parser.add_argument("--refinement-top-k", type=int, default=12)
    parser.add_argument("--refinement-geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--refinement-subcell-samples", type=int, default=5)
    parser.add_argument("--refinement-frequencies-ghz", default=None)
    parser.add_argument("--refinement-frequency-weights", default=None)
    parser.add_argument("--source-frequency-scales", default="0.9,1.0,1.1")
    parser.add_argument("--source-time-shift-ps-values", default="-50,0,50")
    parser.add_argument("--fit-amplitude", action=argparse.BooleanOptionalAction, default=True)

    parser.add_argument("--coarse-grid-step-mm", type=float, default=2.0)
    parser.add_argument("--coarse-x-half-window-mm", type=float, default=0.0)
    parser.add_argument("--coarse-x-step-mm", type=float, default=2.0)
    parser.add_argument("--coarse-z-half-window-mm", type=float, default=15.0)
    parser.add_argument("--coarse-z-step-mm", type=float, default=5.0)
    parser.add_argument("--coarse-z-min-mm", type=float, default=50.0)
    parser.add_argument("--coarse-z-max-mm", type=float, default=180.0)
    parser.add_argument("--coarse-radius-min-mm", type=float, default=5.4)
    parser.add_argument("--coarse-radius-max-mm", type=float, default=7.4)
    parser.add_argument("--coarse-radius-step-mm", type=float, default=0.2)
    parser.add_argument("--coarse-progress-every", type=int, default=20)

    parser.add_argument("--fine-grid-step-mm", type=float, default=1.0)
    parser.add_argument("--fine-x-half-window-mm", type=float, default=0.0)
    parser.add_argument("--fine-x-step-mm", type=float, default=1.0)
    parser.add_argument("--fine-z-half-window-mm", type=float, default=2.0)
    parser.add_argument("--fine-z-step-mm", type=float, default=1.0)
    parser.add_argument("--fine-z-min-mm", type=float, default=50.0)
    parser.add_argument("--fine-z-max-mm", type=float, default=180.0)
    parser.add_argument("--fine-radius-half-window-mm", type=float, default=0.2)
    parser.add_argument("--fine-radius-step-mm", type=float, default=0.2)
    parser.add_argument("--fine-radius-min-mm", type=float, default=2.0)
    parser.add_argument("--fine-radius-max-mm", type=float, default=14.0)
    parser.add_argument("--fine-progress-every", type=int, default=10)

    parser.add_argument("--enable-guarded-polish", action="store_true")
    parser.add_argument("--guarded-sources", type=int, default=9)
    parser.add_argument("--guarded-grid-step-mm", type=float, default=1.0)
    parser.add_argument("--guarded-x-half-window-mm", type=float, default=0.0)
    parser.add_argument("--guarded-x-step-mm", type=float, default=1.0)
    parser.add_argument("--guarded-z-half-window-mm", type=float, default=1.0)
    parser.add_argument("--guarded-z-step-mm", type=float, default=1.0)
    parser.add_argument("--guarded-z-min-mm", type=float, default=50.0)
    parser.add_argument("--guarded-z-max-mm", type=float, default=180.0)
    parser.add_argument("--guarded-radius-half-window-mm", type=float, default=0.1)
    parser.add_argument("--guarded-radius-step-mm", type=float, default=0.1)
    parser.add_argument("--guarded-radius-min-mm", type=float, default=2.0)
    parser.add_argument("--guarded-radius-max-mm", type=float, default=14.0)
    parser.add_argument("--guarded-geometry-mode", choices=["hard", "subcell"], default="subcell")
    parser.add_argument("--guarded-subcell-samples", type=int, default=9)
    parser.add_argument("--guarded-frequencies-ghz", default=None)
    parser.add_argument("--guarded-frequency-weights", default=None)
    parser.add_argument("--guarded-progress-every", type=int, default=1)

    parser.add_argument("--enable-highband-polish", action="store_true")
    parser.add_argument("--highband-frequency-ghz", type=float, default=2.5)
    parser.add_argument("--highband-sources", type=int, default=9)
    parser.add_argument("--highband-grid-step-mm", type=float, default=1.0)
    parser.add_argument("--highband-x-half-window-mm", type=float, default=0.0)
    parser.add_argument("--highband-x-step-mm", type=float, default=1.0)
    parser.add_argument("--highband-z-half-window-mm", type=float, default=1.0)
    parser.add_argument("--highband-z-step-mm", type=float, default=1.0)
    parser.add_argument("--highband-z-min-mm", type=float, default=50.0)
    parser.add_argument("--highband-z-max-mm", type=float, default=180.0)
    parser.add_argument("--highband-radius-half-window-mm", type=float, default=0.1)
    parser.add_argument("--highband-radius-step-mm", type=float, default=0.1)
    parser.add_argument("--highband-radius-min-mm", type=float, default=2.0)
    parser.add_argument("--highband-radius-max-mm", type=float, default=14.0)
    parser.add_argument("--highband-geometry-mode", choices=["hard", "subcell"], default="subcell")
    parser.add_argument("--highband-subcell-samples", type=int, default=9)
    parser.add_argument("--highband-frequencies-ghz", default=None)
    parser.add_argument("--highband-frequency-weights", default=None)
    parser.add_argument("--highband-progress-every", type=int, default=1)

    parser.add_argument("--enable-material-uncertainty-report", action="store_true")
    parser.add_argument("--material-uncertainty-case-label", default="single_rebar")
    parser.add_argument("--material-uncertainty-frequency-ghz", type=float, default=None)
    parser.add_argument("--material-uncertainty-sources", type=int, default=9)
    parser.add_argument("--material-uncertainty-grid-step-mm", type=float, default=1.0)
    parser.add_argument("--material-uncertainty-radius-half-window-mm", type=float, default=0.1)
    parser.add_argument("--material-uncertainty-radius-step-mm", type=float, default=0.05)
    parser.add_argument("--material-uncertainty-radius-min-mm", type=float, default=2.0)
    parser.add_argument("--material-uncertainty-radius-max-mm", type=float, default=14.0)
    parser.add_argument("--material-uncertainty-concrete-epsr-values", default="5.8,6.0,6.2")
    parser.add_argument("--material-uncertainty-rebar-log10-sigma-values", default="6,7")
    parser.add_argument("--material-uncertainty-geometry-mode", choices=["hard", "subcell"], default="subcell")
    parser.add_argument("--material-uncertainty-subcell-samples", type=int, default=13)
    parser.add_argument("--material-uncertainty-top-k", type=int, default=16)
    parser.add_argument("--material-uncertainty-progress-every", type=int, default=1)

    parser.add_argument("--run-name", default="detection_seeded_two_stage_refinement")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()

    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    stages_dir = outdir / "stages"
    data_dir.mkdir(parents=True, exist_ok=True)
    stages_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    overall_started = time.time()

    detection_dir = stages_dir / "detection"
    detection_elapsed_s = run_subprocess(build_detection_command(args, detection_dir))
    detection_summary_path = detection_dir / "data" / "detection_summary.json"
    detection_summary = load_json(detection_summary_path)
    selected_detection = select_detection_candidate(
        detection_summary,
        args.detector_candidate_rank,
    )
    write_detection_figure_notes(
        detection_dir / "figures",
        detection_summary,
        args.detector_candidate_rank,
    )

    coarse_x_values = axis_values_mm(
        selected_detection["x_mm"],
        args.coarse_x_half_window_mm,
        args.coarse_x_step_mm,
    )
    coarse_z_values = axis_values_mm(
        selected_detection["z_mm"],
        args.coarse_z_half_window_mm,
        args.coarse_z_step_mm,
        min_value_mm=args.coarse_z_min_mm,
        max_value_mm=args.coarse_z_max_mm,
    )
    coarse_radius_values = axis_values_mm(
        0.5 * (args.coarse_radius_min_mm + args.coarse_radius_max_mm),
        0.5 * (args.coarse_radius_max_mm - args.coarse_radius_min_mm),
        args.coarse_radius_step_mm,
        min_value_mm=args.coarse_radius_min_mm,
        max_value_mm=args.coarse_radius_max_mm,
    )

    coarse_dir = stages_dir / "coarse_screen"
    coarse_elapsed_s = run_subprocess(build_polish_command(
        args,
        coarse_dir,
        "coarse_screen",
        args.coarse_grid_step_mm,
        coarse_x_values,
        coarse_z_values,
        coarse_radius_values,
        args.coarse_progress_every,
    ))
    coarse_summary_path = coarse_dir / "data" / "source_profiled_polish_summary.json"
    coarse_summary = load_json(coarse_summary_path)
    coarse_best = best_source_profiled_candidate(coarse_summary)
    write_polish_figure_notes(
        coarse_dir / "figures",
        coarse_summary,
        "coarse 2 mm radius and depth screen",
        "a screening pass that should find the correct branch cheaply, not a final radius decision",
    )

    fine_x_values = axis_values_mm(
        coarse_best["params"]["x_mm"],
        args.fine_x_half_window_mm,
        args.fine_x_step_mm,
    )
    fine_z_values = axis_values_mm(
        coarse_best["params"]["z_mm"],
        args.fine_z_half_window_mm,
        args.fine_z_step_mm,
        min_value_mm=args.fine_z_min_mm,
        max_value_mm=args.fine_z_max_mm,
    )
    fine_radius_values = axis_values_mm(
        coarse_best["params"]["radius_mm"],
        args.fine_radius_half_window_mm,
        args.fine_radius_step_mm,
        min_value_mm=args.fine_radius_min_mm,
        max_value_mm=args.fine_radius_max_mm,
    )

    fine_dir = stages_dir / "fine_polish"
    fine_elapsed_s = run_subprocess(build_polish_command(
        args,
        fine_dir,
        "fine_polish",
        args.fine_grid_step_mm,
        fine_x_values,
        fine_z_values,
        fine_radius_values,
        args.fine_progress_every,
    ))
    fine_summary_path = fine_dir / "data" / "source_profiled_polish_summary.json"
    fine_summary = load_json(fine_summary_path)
    fine_best = best_source_profiled_candidate(fine_summary)
    write_polish_figure_notes(
        fine_dir / "figures",
        fine_summary,
        "narrow 1 mm final polish",
        "the final local refinement around the coarse-screen winner",
    )

    final_stage = "fine_polish"
    final_best = fine_best
    final_summary = fine_summary
    guarded_elapsed_s = None
    guarded_summary_path = None
    guarded_grid = None
    guarded_best = None
    guarded_summary = None
    highband_elapsed_s = None
    highband_summary_path = None
    highband_grid = None
    highband_best = None
    highband_summary = None
    material_uncertainty_elapsed_s = None
    material_uncertainty_summary_path = None
    material_uncertainty_grid = None
    radius_uncertainty_report_elapsed_s = None
    radius_uncertainty_report_summary_path = None
    if args.enable_guarded_polish:
        guarded_x_values = axis_values_mm(
            fine_best["params"]["x_mm"],
            args.guarded_x_half_window_mm,
            args.guarded_x_step_mm,
        )
        guarded_z_values = axis_values_mm(
            fine_best["params"]["z_mm"],
            args.guarded_z_half_window_mm,
            args.guarded_z_step_mm,
            min_value_mm=args.guarded_z_min_mm,
            max_value_mm=args.guarded_z_max_mm,
        )
        guarded_radius_values = axis_values_mm(
            fine_best["params"]["radius_mm"],
            args.guarded_radius_half_window_mm,
            args.guarded_radius_step_mm,
            min_value_mm=args.guarded_radius_min_mm,
            max_value_mm=args.guarded_radius_max_mm,
        )
        guarded_grid = {
            "x_values_mm": guarded_x_values,
            "z_values_mm": guarded_z_values,
            "radius_values_mm": guarded_radius_values,
            "candidate_count": int(
                len(guarded_x_values) * len(guarded_z_values) * len(guarded_radius_values)
            ),
        }

        guarded_dir = stages_dir / "guarded_polish"
        guarded_elapsed_s = run_subprocess(build_polish_command(
            args,
            guarded_dir,
            "guarded_polish",
            args.guarded_grid_step_mm,
            guarded_x_values,
            guarded_z_values,
            guarded_radius_values,
            args.guarded_progress_every,
            sources=args.guarded_sources,
            geometry_mode=args.guarded_geometry_mode,
            subcell_samples=args.guarded_subcell_samples,
            frequencies_ghz=args.guarded_frequencies_ghz,
            frequency_weights=args.guarded_frequency_weights,
        ))
        guarded_summary_path = guarded_dir / "data" / "source_profiled_polish_summary.json"
        guarded_summary = load_json(guarded_summary_path)
        guarded_best = best_source_profiled_candidate(guarded_summary)
        write_polish_figure_notes(
            guarded_dir / "figures",
            guarded_summary,
            "guarded high-information local polish",
            "a tightly scoped confidence check around the fine-polish winner",
        )
        final_stage = "guarded_polish"
        final_best = guarded_best
        final_summary = guarded_summary

    if args.enable_highband_polish:
        highband_x_values = axis_values_mm(
            final_best["params"]["x_mm"],
            args.highband_x_half_window_mm,
            args.highband_x_step_mm,
        )
        highband_z_values = axis_values_mm(
            final_best["params"]["z_mm"],
            args.highband_z_half_window_mm,
            args.highband_z_step_mm,
            min_value_mm=args.highband_z_min_mm,
            max_value_mm=args.highband_z_max_mm,
        )
        highband_radius_values = axis_values_mm(
            final_best["params"]["radius_mm"],
            args.highband_radius_half_window_mm,
            args.highband_radius_step_mm,
            min_value_mm=args.highband_radius_min_mm,
            max_value_mm=args.highband_radius_max_mm,
        )
        highband_grid = {
            "x_values_mm": highband_x_values,
            "z_values_mm": highband_z_values,
            "radius_values_mm": highband_radius_values,
            "candidate_count": int(
                len(highband_x_values) * len(highband_z_values) * len(highband_radius_values)
            ),
            "base_frequency_ghz": float(args.highband_frequency_ghz),
        }

        highband_dir = stages_dir / "highband_polish"
        highband_elapsed_s = run_subprocess(build_polish_command(
            args,
            highband_dir,
            "highband_polish",
            args.highband_grid_step_mm,
            highband_x_values,
            highband_z_values,
            highband_radius_values,
            args.highband_progress_every,
            sources=args.highband_sources,
            geometry_mode=args.highband_geometry_mode,
            subcell_samples=args.highband_subcell_samples,
            base_frequency_ghz=args.highband_frequency_ghz,
            frequencies_ghz=args.highband_frequencies_ghz,
            frequency_weights=args.highband_frequency_weights,
        ))
        highband_summary_path = highband_dir / "data" / "source_profiled_polish_summary.json"
        highband_summary = load_json(highband_summary_path)
        highband_best = best_source_profiled_candidate(highband_summary)
        write_polish_figure_notes(
            highband_dir / "figures",
            highband_summary,
            "high-band local radius-confidence polish",
            "a separate high-band acquisition diagnostic centered on the current best candidate",
        )
        final_stage = "highband_polish"
        final_best = highband_best
        final_summary = highband_summary

    final_stage_summary_path = {
        "fine_polish": fine_summary_path,
        "guarded_polish": guarded_summary_path,
        "highband_polish": highband_summary_path,
    }[final_stage]

    if args.enable_material_uncertainty_report:
        material_radius_values = axis_values_mm(
            final_best["params"]["radius_mm"],
            args.material_uncertainty_radius_half_window_mm,
            args.material_uncertainty_radius_step_mm,
            min_value_mm=args.material_uncertainty_radius_min_mm,
            max_value_mm=args.material_uncertainty_radius_max_mm,
        )
        material_uncertainty_grid = {
            "x_mm": float(final_best["params"]["x_mm"]),
            "z_mm": float(final_best["params"]["z_mm"]),
            "radius_values_mm": material_radius_values,
            "candidate_count": int(
                len(material_radius_values)
                * len([
                    part for part in args.material_uncertainty_concrete_epsr_values.split(",")
                    if part.strip()
                ])
                * len([
                    part for part in args.material_uncertainty_rebar_log10_sigma_values.split(",")
                    if part.strip()
                ])
            ),
        }
        material_dir = stages_dir / "material_uncertainty"
        material_uncertainty_elapsed_s = run_subprocess(build_material_uncertainty_command(
            args,
            material_dir,
            final_best["params"]["x_mm"],
            final_best["params"]["z_mm"],
            material_radius_values,
        ))
        material_uncertainty_summary_path = (
            material_dir / "data" / "material_tradeoff_summary.json"
        )
        report_dir = stages_dir / "radius_uncertainty_report"
        radius_uncertainty_report_elapsed_s = run_subprocess(
            build_radius_uncertainty_report_command(
                args,
                report_dir,
                final_stage_summary_path,
                material_uncertainty_summary_path,
            )
        )
        radius_uncertainty_report_summary_path = (
            report_dir / "data" / "radius_uncertainty_report.json"
        )

    overall_elapsed_s = time.time() - overall_started
    truth_errors = {
        "x_error_mm": float(abs(final_best["params"]["x_mm"] - args.truth_x_mm)),
        "z_error_mm": float(abs(final_best["params"]["z_mm"] - args.truth_z_mm)),
        "radius_error_mm": float(abs(final_best["params"]["radius_mm"] - args.truth_radius_mm)),
    }
    summary = {
        "run_name": args.run_name,
        "backend": args.backend,
        "truth": {
            "x_mm": float(args.truth_x_mm),
            "z_mm": float(args.truth_z_mm),
            "radius_mm": float(args.truth_radius_mm),
        },
        "observed_source": {
            "frequency_scale": float(args.observed_frequency_scale),
            "time_shift_ps": float(args.observed_time_shift_ps),
            "amplitude_scale": float(args.observed_amplitude_scale),
            "noise_rms_fraction": float(args.observed_noise_rms_fraction),
            "noise_seed": int(args.noise_seed),
        },
        "selected_detection": selected_detection,
        "coarse_grid": {
            "x_values_mm": coarse_x_values,
            "z_values_mm": coarse_z_values,
            "radius_values_mm": coarse_radius_values,
            "candidate_count": int(len(coarse_x_values) * len(coarse_z_values) * len(coarse_radius_values)),
        },
        "coarse_best": coarse_best,
        "coarse_margin": coarse_summary.get("margin"),
        "coarse_radius_ambiguity": coarse_summary.get("radius_ambiguity"),
        "fine_grid": {
            "x_values_mm": fine_x_values,
            "z_values_mm": fine_z_values,
            "radius_values_mm": fine_radius_values,
            "candidate_count": int(len(fine_x_values) * len(fine_z_values) * len(fine_radius_values)),
        },
        "fine_best": fine_best,
        "fine_margin": fine_summary.get("margin"),
        "fine_radius_ambiguity": fine_summary.get("radius_ambiguity"),
        "guarded_grid": guarded_grid,
        "guarded_best": guarded_best,
        "guarded_margin": guarded_summary.get("margin") if guarded_summary else None,
        "guarded_radius_ambiguity": (
            guarded_summary.get("radius_ambiguity") if guarded_summary else None
        ),
        "highband_grid": highband_grid,
        "highband_best": highband_best,
        "highband_margin": highband_summary.get("margin") if highband_summary else None,
        "highband_radius_ambiguity": (
            highband_summary.get("radius_ambiguity") if highband_summary else None
        ),
        "final_stage": final_stage,
        "final_best": final_best,
        "final_margin": final_summary.get("margin"),
        "final_radius_ambiguity": final_summary.get("radius_ambiguity"),
        "material_uncertainty_grid": material_uncertainty_grid,
        "material_uncertainty_enabled": bool(args.enable_material_uncertainty_report),
        "truth_errors": truth_errors,
        "elapsed_time_s": {
            "overall_wall": float(overall_elapsed_s),
            "detection_subprocess_wall": float(detection_elapsed_s),
            "coarse_subprocess_wall": float(coarse_elapsed_s),
            "fine_subprocess_wall": float(fine_elapsed_s),
            "guarded_subprocess_wall": (
                float(guarded_elapsed_s) if guarded_elapsed_s is not None else None
            ),
            "highband_subprocess_wall": (
                float(highband_elapsed_s) if highband_elapsed_s is not None else None
            ),
            "material_uncertainty_subprocess_wall": (
                float(material_uncertainty_elapsed_s)
                if material_uncertainty_elapsed_s is not None else None
            ),
            "radius_uncertainty_report_subprocess_wall": (
                float(radius_uncertainty_report_elapsed_s)
                if radius_uncertainty_report_elapsed_s is not None else None
            ),
            "detection_reported": float(detection_summary.get("elapsed_time_s", 0.0)),
            "coarse_reported": float(coarse_summary.get("elapsed_time_s", 0.0)),
            "fine_reported": float(fine_summary.get("elapsed_time_s", 0.0)),
            "guarded_reported": (
                float(guarded_summary.get("elapsed_time_s", 0.0)) if guarded_summary else None
            ),
            "highband_reported": (
                float(highband_summary.get("elapsed_time_s", 0.0)) if highband_summary else None
            ),
        },
        "paths": {
            "detection_summary": str(detection_summary_path),
            "coarse_summary": str(coarse_summary_path),
            "fine_summary": str(fine_summary_path),
            "guarded_summary": str(guarded_summary_path) if guarded_summary_path else None,
            "highband_summary": str(highband_summary_path) if highband_summary_path else None,
            "final_stage_summary": str(final_stage_summary_path),
            "material_uncertainty_summary": (
                str(material_uncertainty_summary_path)
                if material_uncertainty_summary_path else None
            ),
            "radius_uncertainty_report_summary": (
                str(radius_uncertainty_report_summary_path)
                if radius_uncertainty_report_summary_path else None
            ),
        },
    }
    summary_path = data_dir / "two_stage_refinement_summary.json"
    write_summary(summary_path, summary)
    write_run_manifest(
        str(outdir),
        "detection_seeded_two_stage_refinement",
        {"summary_path": str(summary_path), "stage_paths": summary["paths"]},
    )

    print(
        "Final best: "
        f"x={final_best['params']['x_mm']:.1f} mm, "
        f"z={final_best['params']['z_mm']:.1f} mm, "
        f"r={final_best['params']['radius_mm']:.1f} mm "
        f"from {final_stage}"
    )
    print(f"Truth errors: {truth_errors}")
    print(f"Final radius margin: {summary['final_margin']}")
    print(f"Wrote summary: {summary_path}")


if __name__ == "__main__":
    main()
