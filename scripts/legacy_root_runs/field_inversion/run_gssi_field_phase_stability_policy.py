#!/usr/bin/env python3
"""Phase-convention stability policy for local GSSI field waveform probes."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402

from core.run_outputs import allocate_output_dir, write_run_manifest  # noqa: E402
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def safe_float(value, default=math.nan) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float(default)
    return out if math.isfinite(out) else float(default)


def read_shift_surface(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("geometry_valid") not in ("True", True):
                continue
            row["synthetic_time_shift_ns"] = safe_float(row.get("synthetic_time_shift_ns"))
            row["absolute_correlation"] = safe_float(row.get("absolute_correlation"))
            row["normalized_residual_rms"] = safe_float(row.get("normalized_residual_rms"))
            row["radius_mm"] = safe_float(row.get("radius_mm"))
            if math.isfinite(row["synthetic_time_shift_ns"]) and math.isfinite(row["absolute_correlation"]):
                rows.append(row)
    if not rows:
        raise ValueError(f"no valid shift-surface rows in {path}")
    return rows


def event_key(row: dict) -> str:
    return "|".join([
        str(row.get("file", "")),
        str(row.get("phase_convention", "")),
        str(row.get("apex_group", "")),
    ])


def summarize_phase_shifts(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, float], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(str(row.get("phase_convention", "")), float(row["synthetic_time_shift_ns"]))].append(row)
    out: list[dict] = []
    for (phase, shift), subset in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1])):
        values = [float(row["absolute_correlation"]) for row in subset]
        residuals = [
            float(row["normalized_residual_rms"])
            for row in subset
            if math.isfinite(float(row["normalized_residual_rms"]))
        ]
        same = sum(1 for row in subset if row.get("polarity") == "same")
        out.append({
            "phase_convention": phase,
            "synthetic_time_shift_ns": shift,
            "valid_row_count": len(subset),
            "same_polarity_count": same,
            "same_polarity_fraction": same / len(subset) if subset else math.nan,
            "mean_abs_correlation": float(np.mean(values)),
            "median_abs_correlation": float(np.median(values)),
            "min_abs_correlation": float(np.min(values)),
            "max_abs_correlation": float(np.max(values)),
            "mean_residual_rms": float(np.mean(residuals)) if residuals else math.nan,
        })
    return out


def best_row(rows: list[dict]) -> dict:
    return max(rows, key=lambda row: float(row["absolute_correlation"]))


def summarize_phase_policy(rows: list[dict], phase_shift_rows: list[dict]) -> list[dict]:
    event_sets: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        event_sets[str(row.get("phase_convention", ""))].add(event_key(row))
    by_phase: dict[str, list[dict]] = defaultdict(list)
    for row in phase_shift_rows:
        by_phase[str(row["phase_convention"])].append(row)
    out: list[dict] = []
    for phase, subset in sorted(by_phase.items()):
        best = max(
            subset,
            key=lambda row: (
                float(row["mean_abs_correlation"]),
                float(row["min_abs_correlation"]),
                float(row["same_polarity_fraction"]),
            ),
        )
        out.append({
            "phase_convention": phase,
            "event_count": len(event_sets[phase]),
            "best_shared_shift_ns": best["synthetic_time_shift_ns"],
            "best_shared_mean_abs_correlation": best["mean_abs_correlation"],
            "best_shared_min_abs_correlation": best["min_abs_correlation"],
            "best_shared_same_polarity_fraction": best["same_polarity_fraction"],
            "best_shared_mean_residual_rms": best["mean_residual_rms"],
        })
    return out


def summarize_event_stability(rows: list[dict], global_shift_ns: float) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[event_key(row)].append(row)
    out: list[dict] = []
    for key, subset in sorted(grouped.items()):
        best = best_row(subset)
        global_subset = [
            row for row in subset
            if math.isclose(float(row["synthetic_time_shift_ns"]), float(global_shift_ns), abs_tol=1.0e-9)
        ]
        global_best = best_row(global_subset) if global_subset else None
        best_abs = float(best["absolute_correlation"])
        global_abs = float(global_best["absolute_correlation"]) if global_best is not None else math.nan
        out.append({
            "event_key": key,
            "file": best.get("file", ""),
            "phase_convention": best.get("phase_convention", ""),
            "apex_group": best.get("apex_group", ""),
            "event_specific_shift_ns": best.get("synthetic_time_shift_ns"),
            "event_specific_abs_correlation": best_abs,
            "event_specific_radius_mm": best.get("radius_mm"),
            "event_specific_epsr_source": best.get("epsr_source", ""),
            "event_specific_polarity": best.get("polarity", ""),
            "global_shift_ns": global_shift_ns,
            "global_abs_correlation": global_abs,
            "global_minus_event_specific": global_abs - best_abs if math.isfinite(global_abs) else math.nan,
            "global_radius_mm": global_best.get("radius_mm") if global_best is not None else math.nan,
            "global_epsr_source": global_best.get("epsr_source", "") if global_best is not None else "",
            "global_polarity": global_best.get("polarity", "") if global_best is not None else "",
            "stable_at_global_shift": (
                bool(global_best is not None)
                and math.isclose(
                    float(best["synthetic_time_shift_ns"]),
                    float(global_shift_ns),
                    abs_tol=1.0e-9,
                )
                and global_abs >= 0.7
                and global_best.get("polarity") == "same"
            ),
        })
    return out


def figure_stats(path: Path) -> dict:
    with Image.open(path) as image:
        arr = np.asarray(image.convert("RGB"))
        gray = np.asarray(image.convert("L"))
    sample = arr.reshape(-1, 3)[:: max(1, arr.reshape(-1, 3).shape[0] // 10000)]
    return {
        "path": str(path),
        "width": int(arr.shape[1]),
        "height": int(arr.shape[0]),
        "sampled_unique_colors": int(np.unique(sample, axis=0).shape[0]),
        "nonwhite_fraction": float(np.mean(np.any(arr < 250, axis=2))),
        "dynamic_range": int(gray.max()) - int(gray.min()),
    }


def plot_phase_shift_summary(rows: list[dict], save_path: Path) -> str:
    phases = sorted({row["phase_convention"] for row in rows})
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)
    for phase in phases:
        subset = [row for row in rows if row["phase_convention"] == phase]
        shifts = [row["synthetic_time_shift_ns"] for row in subset]
        means = [row["mean_abs_correlation"] for row in subset]
        mins = [row["min_abs_correlation"] for row in subset]
        same = [row["same_polarity_fraction"] for row in subset]
        axes[0].plot(shifts, means, marker="o", label=f"{phase} mean")
        axes[0].plot(shifts, mins, marker="s", linestyle="--", label=f"{phase} min")
        axes[1].plot(shifts, same, marker="o", label=phase)
    axes[0].set_xlabel("synthetic time shift [ns]")
    axes[0].set_ylabel("absolute normalized correlation")
    axes[0].set_title("Phase-specific shift score")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].set_xlabel("synthetic time shift [ns]")
    axes[1].set_ylabel("same-polarity fraction")
    axes[1].set_ylim(-0.03, 1.03)
    axes[1].set_title("Polarity stability")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Field waveform phase-convention stability", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_event_stability(rows: list[dict], save_path: Path) -> str:
    ordered = sorted(rows, key=lambda row: (row["phase_convention"], row["file"], int(float(row["apex_group"]))))
    labels = [
        f"{Path(row['file']).stem.split('__')[-1]} {row['phase_convention']} g{row['apex_group']}"
        for row in ordered
    ]
    x = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(max(10.0, 0.75 * len(ordered)), 5.0), constrained_layout=True)
    ax.bar(x - 0.18, [row["event_specific_abs_correlation"] for row in ordered], width=0.36, label="event-specific")
    ax.bar(x + 0.18, [row["global_abs_correlation"] for row in ordered], width=0.36, label="global +0.2 ns")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("absolute normalized correlation")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("Event-specific vs global timing policy")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.legend(frameon=False)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--probe-dir", default=None)
    parser.add_argument("--global-shift-ns", type=float, default=0.2)
    parser.add_argument("--run-name", default="gssi51600s_phase_stability_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    probe_dir = (
        Path(args.probe_dir)
        if args.probe_dir is not None
        else dataset_root / "011_gssi51600s_field_synthetic_waveform_family_shift_epsr_probe"
    )
    shift_surface_csv = probe_dir / "data" / "field_synthetic_waveform_shift_surface.csv"
    rows = read_shift_surface(shift_surface_csv)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    phase_shift_rows = summarize_phase_shifts(rows)
    phase_policy_rows = summarize_phase_policy(rows, phase_shift_rows)
    event_rows = summarize_event_stability(rows, args.global_shift_ns)

    phase_shift_csv = data_dir / "phase_shift_summary.csv"
    phase_policy_csv = data_dir / "phase_policy_summary.csv"
    event_csv = data_dir / "phase_event_stability.csv"
    write_csv(phase_shift_csv, [json_safe(row) for row in phase_shift_rows])
    write_csv(phase_policy_csv, [json_safe(row) for row in phase_policy_rows])
    write_csv(event_csv, [json_safe(row) for row in event_rows])

    phase_plot = Path(plot_phase_shift_summary(phase_shift_rows, figures_dir / "phase_shift_stability.png"))
    event_plot = Path(plot_event_stability(event_rows, figures_dir / "phase_event_stability.png"))
    validation_rows = [figure_stats(phase_plot), figure_stats(event_plot)]
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, validation_rows)

    stable_count = sum(1 for row in event_rows if row["stable_at_global_shift"])
    summary = {
        "run_name": args.run_name,
        "probe_dir": str(probe_dir),
        "shift_surface_csv": str(shift_surface_csv),
        "global_shift_ns": args.global_shift_ns,
        "valid_shift_surface_rows": len(rows),
        "event_count": len(event_rows),
        "stable_at_global_shift_count": stable_count,
        "phase_policy": phase_policy_rows,
        "interpretation": (
            "Top-envelope anchoring is stable under the current +0.2 ns timing "
            "hypothesis, while cue-time anchoring is event-specific and should "
            "not be used as a field inversion anchor."
        ),
        "paths": {
            "phase_shift_summary_csv": str(phase_shift_csv),
            "phase_policy_summary_csv": str(phase_policy_csv),
            "phase_event_stability_csv": str(event_csv),
            "json": str(data_dir / "phase_stability_policy_summary.json"),
            "phase_plot": str(phase_plot),
            "event_plot": str(event_plot),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json = data_dir / "phase_stability_policy_summary.json"
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_phase_stability_policy",
        {
            "summary_json": str(summary_json),
            "shift_surface_csv": str(shift_surface_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
