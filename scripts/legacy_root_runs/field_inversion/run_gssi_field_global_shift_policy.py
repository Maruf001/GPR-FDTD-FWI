#!/usr/bin/env python3
"""Global shift policy analysis for local GSSI field-to-synthetic probes."""

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
            row["normalized_correlation"] = safe_float(row.get("normalized_correlation"))
            row["normalized_residual_rms"] = safe_float(row.get("normalized_residual_rms"))
            row["radius_mm"] = safe_float(row.get("radius_mm"))
            if math.isfinite(row["synthetic_time_shift_ns"]) and math.isfinite(row["absolute_correlation"]):
                rows.append(row)
    if not rows:
        raise ValueError(f"no valid shift-surface rows in {path}")
    return rows


def candidate_key(row: dict) -> str:
    return str(row["candidate_id"])


def event_key(row: dict) -> str:
    return "|".join([
        str(row.get("file", "")),
        str(row.get("phase_convention", "")),
        str(row.get("apex_group", "")),
        str(row.get("epsr_source", "")),
    ])


def summarize_by_shift(rows: list[dict]) -> list[dict]:
    grouped: dict[float, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[float(row["synthetic_time_shift_ns"])].append(row)
    out = []
    for shift, subset in sorted(grouped.items()):
        values = [float(row["absolute_correlation"]) for row in subset]
        residuals = [float(row["normalized_residual_rms"]) for row in subset if math.isfinite(row["normalized_residual_rms"])]
        same = sum(1 for row in subset if row.get("polarity") == "same")
        out.append({
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


def summarize_by_shift_and_group(rows: list[dict], group_field: str) -> list[dict]:
    grouped: dict[tuple[str, float], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(str(row.get(group_field, "")), float(row["synthetic_time_shift_ns"]))].append(row)
    out = []
    for (group_value, shift), subset in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][1])):
        values = [float(row["absolute_correlation"]) for row in subset]
        out.append({
            group_field: group_value,
            "synthetic_time_shift_ns": shift,
            "valid_row_count": len(subset),
            "mean_abs_correlation": float(np.mean(values)),
            "min_abs_correlation": float(np.min(values)),
            "max_abs_correlation": float(np.max(values)),
            "same_polarity_count": sum(1 for row in subset if row.get("polarity") == "same"),
        })
    return out


def best_rows_by_key(rows: list[dict], key_fn) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[key_fn(row)].append(row)
    out = []
    for key, subset in sorted(grouped.items()):
        best = max(subset, key=lambda row: float(row["absolute_correlation"]))
        out.append({
            "group_key": key,
            "candidate_id": best.get("candidate_id", ""),
            "file": best.get("file", ""),
            "phase_convention": best.get("phase_convention", ""),
            "apex_group": best.get("apex_group", ""),
            "epsr_source": best.get("epsr_source", ""),
            "radius_mm": best.get("radius_mm"),
            "best_time_shift_ns": best.get("synthetic_time_shift_ns"),
            "best_abs_correlation": best.get("absolute_correlation"),
            "best_polarity": best.get("polarity", ""),
        })
    return out


def rows_at_shift(rows: list[dict], shift_ns: float) -> list[dict]:
    return [
        row for row in rows
        if math.isclose(float(row["synthetic_time_shift_ns"]), float(shift_ns), abs_tol=1.0e-9)
    ]


def compare_global_to_best(rows: list[dict], global_shift_ns: float) -> list[dict]:
    best_by_candidate = {row["group_key"]: row for row in best_rows_by_key(rows, candidate_key)}
    global_by_candidate = {
        candidate_key(row): row
        for row in rows_at_shift(rows, global_shift_ns)
    }
    out = []
    for key, best in sorted(best_by_candidate.items()):
        global_row = global_by_candidate.get(key)
        if global_row is None:
            continue
        best_abs = float(best["best_abs_correlation"])
        global_abs = float(global_row["absolute_correlation"])
        out.append({
            "candidate_id": key,
            "file": best["file"],
            "phase_convention": best["phase_convention"],
            "epsr_source": best["epsr_source"],
            "radius_mm": best["radius_mm"],
            "event_specific_shift_ns": best["best_time_shift_ns"],
            "global_shift_ns": global_shift_ns,
            "event_specific_abs_correlation": best_abs,
            "global_abs_correlation": global_abs,
            "global_minus_event_specific": global_abs - best_abs,
            "global_polarity": global_row.get("polarity", ""),
            "event_specific_polarity": best["best_polarity"],
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


def plot_global_shift(summary_rows: list[dict], save_path: Path) -> str:
    shifts = [row["synthetic_time_shift_ns"] for row in summary_rows]
    mean_values = [row["mean_abs_correlation"] for row in summary_rows]
    min_values = [row["min_abs_correlation"] for row in summary_rows]
    same_frac = [row["same_polarity_fraction"] for row in summary_rows]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), constrained_layout=True)
    axes[0].plot(shifts, mean_values, marker="o", label="mean |corr|")
    axes[0].plot(shifts, min_values, marker="s", label="min |corr|")
    axes[0].set_xlabel("synthetic time shift [ns]")
    axes[0].set_ylabel("absolute normalized correlation")
    axes[0].set_title("Global shift score")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False)
    axes[1].plot(shifts, same_frac, marker="o", color="#2f7f5f")
    axes[1].set_xlabel("synthetic time shift [ns]")
    axes[1].set_ylabel("same-polarity fraction")
    axes[1].set_ylim(-0.03, 1.03)
    axes[1].set_title("Polarity consistency")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    fig.suptitle("Global field-to-synthetic time-shift policy", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def plot_global_penalty(comparison_rows: list[dict], save_path: Path) -> str:
    rows = sorted(comparison_rows, key=lambda row: float(row["event_specific_abs_correlation"]), reverse=True)
    labels = [
        f"{Path(row['file']).stem.split('__')[-1]} {row['phase_convention']} "
        f"{row['epsr_source']} r{float(row['radius_mm']):.0f}"
        for row in rows
    ]
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(max(10.0, 0.55 * len(rows)), 5.2), constrained_layout=True)
    ax.bar(x - 0.18, [row["event_specific_abs_correlation"] for row in rows], width=0.36, label="event-specific")
    ax.bar(x + 0.18, [row["global_abs_correlation"] for row in rows], width=0.36, label="global shift")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("absolute normalized correlation")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("Global shift penalty by candidate")
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
    parser.add_argument("--run-name", default="gssi51600s_global_shift_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    probe_dir = (
        Path(args.probe_dir)
        if args.probe_dir is not None
        else dataset_root / "009_gssi51600s_field_synthetic_waveform_shift_epsr_probe"
    )
    shift_surface_csv = probe_dir / "data" / "field_synthetic_waveform_shift_surface.csv"
    rows = read_shift_surface(shift_surface_csv)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    shift_summary = summarize_by_shift(rows)
    epsr_shift_summary = summarize_by_shift_and_group(rows, "epsr_source")
    phase_shift_summary = summarize_by_shift_and_group(rows, "phase_convention")
    event_specific_best = best_rows_by_key(rows, candidate_key)
    global_best = max(
        shift_summary,
        key=lambda row: (
            float(row["mean_abs_correlation"]),
            float(row["min_abs_correlation"]),
            float(row["same_polarity_fraction"]),
        ),
    )
    global_shift_ns = float(global_best["synthetic_time_shift_ns"])
    global_comparison = compare_global_to_best(rows, global_shift_ns)
    penalties = [float(row["global_minus_event_specific"]) for row in global_comparison]

    csv_paths = {
        "shift_summary_csv": data_dir / "global_shift_summary.csv",
        "epsr_shift_summary_csv": data_dir / "global_shift_by_epsr.csv",
        "phase_shift_summary_csv": data_dir / "global_shift_by_phase.csv",
        "event_specific_best_csv": data_dir / "event_specific_best_candidates.csv",
        "global_vs_event_csv": data_dir / "global_vs_event_specific_shift.csv",
    }
    write_csv(csv_paths["shift_summary_csv"], [json_safe(row) for row in shift_summary])
    write_csv(csv_paths["epsr_shift_summary_csv"], [json_safe(row) for row in epsr_shift_summary])
    write_csv(csv_paths["phase_shift_summary_csv"], [json_safe(row) for row in phase_shift_summary])
    write_csv(csv_paths["event_specific_best_csv"], [json_safe(row) for row in event_specific_best])
    write_csv(csv_paths["global_vs_event_csv"], [json_safe(row) for row in global_comparison])

    global_plot = Path(plot_global_shift(shift_summary, figures_dir / "global_shift_policy.png"))
    penalty_plot = Path(plot_global_penalty(global_comparison, figures_dir / "global_shift_penalty.png"))
    validation_rows = [figure_stats(global_plot), figure_stats(penalty_plot)]
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, validation_rows)

    summary = {
        "run_name": args.run_name,
        "probe_dir": str(probe_dir),
        "shift_surface_csv": str(shift_surface_csv),
        "valid_shift_surface_rows": len(rows),
        "candidate_count": len(event_specific_best),
        "global_shift_ns": global_shift_ns,
        "global_mean_abs_correlation": global_best["mean_abs_correlation"],
        "global_min_abs_correlation": global_best["min_abs_correlation"],
        "global_same_polarity_fraction": global_best["same_polarity_fraction"],
        "event_specific_mean_abs_correlation": float(np.mean([
            float(row["best_abs_correlation"]) for row in event_specific_best
        ])),
        "global_mean_abs_correlation_at_candidate_level": float(np.mean([
            float(row["global_abs_correlation"]) for row in global_comparison
        ])),
        "global_penalty_mean": float(np.mean(penalties)) if penalties else math.nan,
        "global_penalty_min": float(np.min(penalties)) if penalties else math.nan,
        "global_penalty_max": float(np.max(penalties)) if penalties else math.nan,
        "interpretation": (
            "A shared positive shift explains most waveform agreement, but "
            "candidate correlations remain clustered and are not geometry-unique."
        ),
        "paths": {
            **{name: str(path) for name, path in csv_paths.items()},
            "json": str(data_dir / "global_shift_policy_summary.json"),
            "global_plot": str(global_plot),
            "penalty_plot": str(penalty_plot),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json = data_dir / "global_shift_policy_summary.json"
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_global_shift_policy",
        {
            "summary_json": str(summary_json),
            "shift_surface_csv": str(shift_surface_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
