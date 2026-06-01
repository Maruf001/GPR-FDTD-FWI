#!/usr/bin/env python3
"""Profile all multi-rebar radii jointly while holding x/z fixed."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from itertools import product
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

import config as cfg  # noqa: E402
from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from core.source import generate_time_array, ricker_wavelet  # noqa: E402
from inversion.adjoint import _build_mute_window  # noqa: E402
from inversion.source_profile import source_profiled_ls  # noqa: E402
from run_multi_rebar_common_radius_profile import (  # noqa: E402
    build_observed_cases,
    build_scan_positions,
)
from run_multi_rebar_local_geometry_profile import (  # noqa: E402
    build_variable_geometry_model,
    parse_vector_mm,
)
from run_single_rebar_frequency_weight_matrix import parse_values_mm  # noqa: E402
from run_single_rebar_inversion import _override_grid  # noqa: E402
from run_single_rebar_source_profiled_replication import parse_replication_cases  # noqa: E402
from run_single_rebar_wavelet_mismatch import parse_positive_values, parse_shift_values_ps  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CASES = (
    "noise10_seed13:1.0,0.0,1.0,0.10,13|"
    "source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13"
)


def radius_tuple_grid(radius_values_mm, count):
    """Return radius tuples in deterministic Cartesian-product order."""
    values = [float(value) for value in radius_values_mm]
    if not values:
        raise ValueError("radius_values_mm must be non-empty")
    if int(count) < 1:
        raise ValueError("count must be positive")
    return [tuple(float(value) for value in item) for item in product(values, repeat=int(count))]


def rank_joint_radius_candidates(candidates, case_label, top_k=None):
    """Rank joint-radius candidates by one observed case."""
    ranked = []
    for candidate in candidates:
        result = candidate["case_results"][case_label]
        ranked.append({
            "misfit": float(result["misfit"]),
            "radii_mm": list(candidate["radii_mm"]),
            "source_profile": dict(result["source_profile"]),
        })
    ranked.sort(key=lambda item: item["misfit"])
    if top_k is None:
        return ranked
    return ranked[:max(0, int(top_k))]


def evaluate_joint_radius_grid(
        observed_by_case,
        x_values_mm,
        z_values_mm,
        radius_tuples_mm,
        frequency_hz,
        modeled_frequency_scales,
        time_shift_values_s,
        scan_positions,
        time_values,
        mute,
        backend,
        geometry_mode="hard",
        subcell_samples=5,
        fit_amplitude=True,
        progress_every=25,
        checkpoint_every=0,
        checkpoint_callback=None,
        initial_candidates=None):
    """Evaluate all radius tuples for fixed x/z coordinates."""
    candidates = list(initial_candidates or [])
    total = len(radius_tuples_mm)
    started = time.time()
    start_index = len(candidates)
    for index, radii_mm in enumerate(radius_tuples_mm[start_index:], start=start_index + 1):
        model = build_variable_geometry_model(
            x_values_mm,
            z_values_mm,
            radii_mm,
            geometry_mode=geometry_mode,
            subcell_samples=subcell_samples,
        )
        synthetic_by_scale = {}
        for scale in modeled_frequency_scales:
            wavelet = ricker_wavelet(time_values, frequency_hz * float(scale))
            synthetic_by_scale[float(scale)] = simulate_bscan_cached(
                model,
                wavelet,
                scan_positions,
                backend,
            )
        case_results = {}
        for label, observed in observed_by_case.items():
            profile = source_profiled_ls(
                observed,
                synthetic_by_scale,
                mute,
                cfg.DT,
                time_shift_values_s=time_shift_values_s,
                fit_amplitude=fit_amplitude,
            )
            case_results[label] = {
                "misfit": float(profile.misfit),
                "source_profile": profile.as_dict(),
            }
        candidates.append({
            "radii_mm": [float(value) for value in radii_mm],
            "case_results": case_results,
        })
        if progress_every and (index == 1 or index % int(progress_every) == 0):
            elapsed = time.time() - started
            print(f"  Joint radius profile: {index}/{total}, elapsed={elapsed:.1f} s")
        if (
                checkpoint_callback is not None
                and checkpoint_every
                and (index == 1 or index % int(checkpoint_every) == 0 or index == total)):
            checkpoint_callback(index, total, candidates, time.time() - started)
    return candidates


def simulate_bscan_cached(model, wavelet, scan_positions, backend):
    """Small wrapper to keep the main evaluator readable."""
    from run_multi_rebar_common_radius_profile import simulate_bscan

    return simulate_bscan(model, wavelet, scan_positions, backend)


def write_candidates_csv(path, candidates, case_labels):
    """Write joint-radius candidate rows."""
    fieldnames = [
        "case_label",
        "misfit",
        "radii_mm",
        "source_frequency_scale",
        "source_time_shift_ps",
        "source_amplitude_scale",
    ]
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for candidate in candidates:
            for label in case_labels:
                result = candidate["case_results"][label]
                profile = result["source_profile"]
                writer.writerow({
                    "case_label": label,
                    "misfit": result["misfit"],
                    "radii_mm": json.dumps(candidate["radii_mm"]),
                    "source_frequency_scale": profile.get("frequency_scale"),
                    "source_time_shift_ps": profile.get("time_shift_ps"),
                    "source_amplitude_scale": profile.get("amplitude_scale"),
                })


def read_candidates_csv(path):
    """Read joint-radius candidates written by write_candidates_csv."""
    candidates = []
    current = None
    current_radii = None
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            radii = [float(value) for value in json.loads(row["radii_mm"])]
            if current is None or radii != current_radii:
                current = {"radii_mm": radii, "case_results": {}}
                candidates.append(current)
                current_radii = radii
            current["case_results"][row["case_label"]] = {
                "misfit": float(row["misfit"]),
                "source_profile": {
                    "frequency_scale": float(row["source_frequency_scale"]),
                    "time_shift_ps": float(row["source_time_shift_ps"]),
                    "amplitude_scale": float(row["source_amplitude_scale"]),
                },
            }
    return candidates


def checkpoint_prefix_matches_grid(candidates, radius_tuples_mm):
    """Return True when checkpoint candidates match the current tuple prefix."""
    if len(candidates) > len(radius_tuples_mm):
        return False
    for candidate, expected in zip(candidates, radius_tuples_mm):
        observed = [float(value) for value in candidate["radii_mm"]]
        if observed != [float(value) for value in expected]:
            return False
    return True


def _atomic_replace_text(path, text):
    """Write text through a temporary file so checkpoints are not half-written."""
    path = Path(path)
    tmp_path = path.with_name(f"{path.name}.tmp")
    tmp_path.write_text(text, encoding="utf-8")
    tmp_path.replace(path)


def write_checkpoint_artifacts(
        data_dir,
        candidates,
        case_labels,
        completed_count,
        total_count,
        elapsed_time_s):
    """Write partial joint-radius candidates and checkpoint metadata."""
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = data_dir / "joint_radius_candidates_checkpoint.csv"
    metadata_path = data_dir / "joint_radius_checkpoint.json"
    tmp_csv = csv_path.with_name(f"{csv_path.name}.tmp")
    write_candidates_csv(tmp_csv, candidates, case_labels)
    tmp_csv.replace(csv_path)
    metadata = {
        "completed_count": int(completed_count),
        "total_count": int(total_count),
        "elapsed_time_s": float(elapsed_time_s),
        "case_labels": list(case_labels),
        "candidate_count": len(candidates),
    }
    _atomic_replace_text(metadata_path, json.dumps(metadata, indent=2))
    return csv_path, metadata_path


def plot_top_joint_radii(candidates, case_label, save_path, top_k=20):
    """Plot the best joint-radius tuples for a case."""
    ranked = rank_joint_radius_candidates(candidates, case_label, top_k=top_k)
    labels = [",".join(f"{value:g}" for value in row["radii_mm"]) for row in ranked]
    misfits = [row["misfit"] for row in ranked]
    fig, ax = plt.subplots(figsize=(10.5, 6.0), constrained_layout=True)
    ax.bar(range(len(ranked)), misfits, color="#3E6C8A")
    ax.set_xticks(range(len(ranked)))
    ax.set_xticklabels(labels, rotation=55, ha="right", fontsize=8)
    ax.set_ylabel("Source-profiled misfit")
    ax.set_xlabel("Radius tuple [mm]")
    ax.set_title(f"Joint Radius Tuple Ranking: {case_label}")
    ax.grid(True, axis="y", alpha=0.25)
    return save_validated_figure(fig, save_path)


def write_figure_notes(path, case_label, truth_radii_mm, candidate_x_mm, candidate_z_mm):
    """Write plain-language notes for the joint-radius plot."""
    text = f"""# Figure Notes

## 1. joint_radius_top_candidates.png

This figure ranks full radius tuples for all rebars together while holding the
x/z positions fixed. Each x-axis label is one tuple, for example `5,6,8` means
left radius 5 mm, center radius 6 mm, and right radius 8 mm.

The y-axis is the source-profiled waveform misfit for case `{case_label}`.
Lower bars are better. This is a diagnostic for whether radius estimation
requires a joint/block update instead of greedy one-target-at-a-time updates.

Truth radii: {', '.join(f'{float(value):g}' for value in truth_radii_mm)} mm.
Fixed candidate x: {', '.join(f'{float(value):g}' for value in candidate_x_mm)} mm.
Fixed candidate z: {', '.join(f'{float(value):g}' for value in candidate_z_mm)} mm.
"""
    Path(path).write_text(text, encoding="utf-8")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["cpu", "gpu-cpml"], default="gpu-cpml")
    parser.add_argument("--grid-step-mm", type=float, default=1.0)
    parser.add_argument("--sources", type=int, default=5)
    parser.add_argument("--frequency-ghz", type=float, default=1.5)
    parser.add_argument("--true-x-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--true-z-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--truth-radius-values-mm", type=parse_vector_mm, required=True)
    parser.add_argument("--candidate-x-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--candidate-z-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--radius-values-mm", type=parse_values_mm, default=parse_values_mm("5:8:0.5"))
    parser.add_argument("--replication-cases", type=parse_replication_cases, default=parse_replication_cases(DEFAULT_CASES))
    parser.add_argument("--update-case-label", default="source_mismatch_noise10_seed13")
    parser.add_argument("--source-frequency-scales", type=parse_positive_values, default=parse_positive_values("0.9,1.0,1.1"))
    parser.add_argument("--source-time-shift-ps-values", type=parse_shift_values_ps, default=parse_shift_values_ps("-50,0,50"))
    parser.add_argument("--no-fit-amplitude", dest="fit_amplitude", action="store_false")
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--checkpoint-every", type=int, default=25)
    parser.add_argument("--resume-from-checkpoint", action="store_true")
    parser.add_argument("--geometry-mode", choices=["hard", "subcell"], default="hard")
    parser.add_argument("--subcell-samples", type=int, default=5)
    parser.add_argument("--run-name", default="multi_rebar_joint_radius_profile")
    parser.add_argument("--outdir", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    if len(args.true_x_values_mm) != len(args.true_z_values_mm):
        raise ValueError("truth x/z lists must have the same length")
    if len(args.true_x_values_mm) != len(args.truth_radius_values_mm):
        raise ValueError("truth x/z/radius lists must have the same length")
    candidate_x = args.candidate_x_values_mm or args.true_x_values_mm
    candidate_z = args.candidate_z_values_mm or args.true_z_values_mm
    if len(candidate_x) != len(candidate_z) or len(candidate_x) != len(args.true_x_values_mm):
        raise ValueError("candidate x/z lists must match truth target count")

    _override_grid(args.grid_step_mm)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {outdir}")

    frequency_hz = args.frequency_ghz * 1e9
    time_values = generate_time_array(cfg.NT, cfg.DT)
    mute = _build_mute_window(cfg.NT, cfg.DT)
    scan_positions, _scan_x = build_scan_positions(cfg.INVERSION_SCAN_STEP, args.sources)
    true_model = build_variable_geometry_model(
        args.true_x_values_mm,
        args.true_z_values_mm,
        args.truth_radius_values_mm,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
    )
    observed_by_case, case_metadata = build_observed_cases(
        true_model,
        time_values,
        frequency_hz,
        scan_positions,
        args.backend,
        args.replication_cases,
    )
    case_labels = [case["label"] for case in args.replication_cases]
    radius_tuples = radius_tuple_grid(args.radius_values_mm, len(candidate_x))
    checkpoint_csv = data_dir / "joint_radius_candidates_checkpoint.csv"
    initial_candidates = []
    if args.resume_from_checkpoint and checkpoint_csv.exists():
        initial_candidates = read_candidates_csv(checkpoint_csv)
        if not checkpoint_prefix_matches_grid(initial_candidates, radius_tuples):
            raise ValueError(
                "checkpoint radius tuple order does not match current radius grid; "
                "refusing to resume"
            )
        print(
            f"Resuming from checkpoint: {len(initial_candidates)}/{len(radius_tuples)} "
            "joint-radius candidates"
        )

    def checkpoint(index, total, partial_candidates, elapsed_time_s):
        write_checkpoint_artifacts(
            data_dir,
            partial_candidates,
            case_labels,
            index,
            total,
            elapsed_time_s,
        )

    started = time.time()
    candidates = evaluate_joint_radius_grid(
        observed_by_case,
        candidate_x,
        candidate_z,
        radius_tuples,
        frequency_hz,
        args.source_frequency_scales,
        [value * 1e-12 for value in args.source_time_shift_ps_values],
        scan_positions,
        time_values,
        mute,
        args.backend,
        geometry_mode=args.geometry_mode,
        subcell_samples=args.subcell_samples,
        fit_amplitude=args.fit_amplitude,
        progress_every=args.progress_every,
        checkpoint_every=args.checkpoint_every,
        checkpoint_callback=checkpoint,
        initial_candidates=initial_candidates,
    )
    elapsed = time.time() - started

    candidate_csv = data_dir / "joint_radius_candidates.csv"
    summary_path = data_dir / "joint_radius_summary.json"
    plot_path = figures_dir / "joint_radius_top_candidates.png"
    notes_path = figures_dir / "FIGURE_NOTES.md"
    write_candidates_csv(candidate_csv, candidates, case_labels)
    plot_top_joint_radii(candidates, args.update_case_label, plot_path, top_k=args.top_k)
    write_figure_notes(
        notes_path,
        args.update_case_label,
        args.truth_radius_values_mm,
        candidate_x,
        candidate_z,
    )
    ranked_by_case = {
        label: rank_joint_radius_candidates(candidates, label, top_k=args.top_k)
        for label in case_labels
    }
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "backend": args.backend,
            "grid_step_mm": args.grid_step_mm,
            "sources": args.sources,
            "frequency_ghz": args.frequency_ghz,
            "true_x_values_mm": args.true_x_values_mm,
            "true_z_values_mm": args.true_z_values_mm,
            "truth_radius_values_mm": args.truth_radius_values_mm,
            "candidate_x_values_mm": candidate_x,
            "candidate_z_values_mm": candidate_z,
            "radius_values_mm": args.radius_values_mm,
            "radius_tuple_count": len(radius_tuples),
            "case_metadata": case_metadata,
            "update_case_label": args.update_case_label,
            "ranked_by_case": ranked_by_case,
            "elapsed_time_s": float(elapsed),
            "paths": {
                "candidate_csv": str(candidate_csv),
                "plot": str(plot_path),
                "figure_notes": str(notes_path),
            },
        }, handle, indent=2)

    write_run_manifest(
        str(outdir),
        "multi_rebar_joint_radius_profile",
        {
            "summary_path": str(summary_path),
            "candidate_csv": str(candidate_csv),
            "plot": str(plot_path),
            "figure_notes": str(notes_path),
        },
    )
    print(f"Wrote summary: {summary_path}")
    print(f"Wrote candidates: {candidate_csv}")
    print(f"Wrote plot: {plot_path}")


if __name__ == "__main__":
    main()
