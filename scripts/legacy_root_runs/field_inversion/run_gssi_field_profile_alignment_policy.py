#!/usr/bin/env python3
"""Profile-level shallow-pattern alignment for local GSSI field data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root, read_dzt_profiles  # noqa: E402
from run_gssi_field_preprocess_feature_qc import build_axes, json_safe, preprocess_profile, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def _nearest_index(values: np.ndarray, target: float) -> int:
    return int(np.argmin(np.abs(np.asarray(values, dtype=np.float64) - float(target))))


def robust_normalize(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    med = float(np.nanmedian(arr))
    mad = float(np.nanmedian(np.abs(arr - med)))
    scale = 1.4826 * mad
    if not math.isfinite(scale) or scale <= 1.0e-12:
        scale = float(np.nanstd(arr))
    if not math.isfinite(scale) or scale <= 1.0e-12:
        scale = 1.0
    return (arr - med) / scale


def profile_signature(cue: np.ndarray, time_ns: np.ndarray, time_min_ns: float, time_max_ns: float) -> np.ndarray:
    mask = (time_ns >= time_min_ns) & (time_ns <= time_max_ns)
    if not np.any(mask):
        raise ValueError(f"empty time window {time_min_ns}..{time_max_ns} ns")
    signature = np.nanpercentile(np.asarray(cue, dtype=np.float64)[mask, :], 95.0, axis=0)
    return robust_normalize(signature)


def _aligned_vectors(reference: np.ndarray, comparison: np.ndarray, lag_samples: int) -> tuple[np.ndarray, np.ndarray]:
    if lag_samples > 0:
        ref = reference[:-lag_samples]
        cmp = comparison[lag_samples:]
    elif lag_samples < 0:
        ref = reference[-lag_samples:]
        cmp = comparison[:lag_samples]
    else:
        ref = reference
        cmp = comparison
    return ref, cmp


def normalized_correlation(reference: np.ndarray, comparison: np.ndarray, lag_samples: int) -> float:
    ref, cmp = _aligned_vectors(reference, comparison, lag_samples)
    if ref.size < 5 or cmp.size < 5:
        return math.nan
    ref = robust_normalize(ref)
    cmp = robust_normalize(cmp)
    denom = float(np.linalg.norm(ref) * np.linalg.norm(cmp))
    if denom <= 1.0e-12:
        return math.nan
    return float(np.dot(ref, cmp) / denom)


def alignment_rows(
    reference: np.ndarray,
    comparison: np.ndarray,
    dx_m: float,
    max_lag_m: float,
    orientation: str,
) -> list[dict]:
    if orientation == "reversed":
        comparison = comparison[::-1]
    max_lag_samples = max(0, int(round(float(max_lag_m) / float(dx_m))))
    rows = []
    for lag in range(-max_lag_samples, max_lag_samples + 1):
        corr = normalized_correlation(reference, comparison, lag)
        overlap = len(_aligned_vectors(reference, comparison, lag)[0])
        rows.append({
            "orientation": orientation,
            "lag_samples": lag,
            "lag_m": lag * dx_m,
            "lag_mm": 1000.0 * lag * dx_m,
            "overlap_samples": overlap,
            "normalized_correlation": corr,
            "absolute_correlation": abs(corr) if math.isfinite(corr) else math.nan,
        })
    return rows


def best_alignment(rows: list[dict]) -> dict:
    valid = [row for row in rows if math.isfinite(float(row["normalized_correlation"]))]
    if not valid:
        raise ValueError("no valid alignment rows")
    return max(valid, key=lambda row: (float(row["normalized_correlation"]), -abs(float(row["lag_mm"]))))


def classify_alignment(best: dict, direct_best: dict, reversed_best: dict) -> str:
    corr = float(best["normalized_correlation"])
    if corr >= 0.85:
        strength = "strong"
    elif corr >= 0.70:
        strength = "moderate"
    elif corr >= 0.55:
        strength = "weak"
    else:
        strength = "not_repeatable"
    orientation_gap = float(direct_best["normalized_correlation"]) - float(reversed_best["normalized_correlation"])
    if abs(orientation_gap) < 0.05:
        orientation = "orientation_ambiguous"
    elif orientation_gap > 0.0:
        orientation = "direct_scan_preferred"
    else:
        orientation = "reversed_scan_preferred"
    return f"{strength}_{orientation}"


def shift_signature(values: np.ndarray, lag_samples: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.arange(values.size, dtype=np.float64)
    shifted_x = x - lag_samples
    return shifted_x, values


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


def plot_alignment(
    reference_label: str,
    comparison_label: str,
    x_m: np.ndarray,
    reference_signature: np.ndarray,
    comparison_signature: np.ndarray,
    rows: list[dict],
    best: dict,
    save_path: Path,
) -> str:
    direct = [row for row in rows if row["orientation"] == "direct"]
    reversed_rows = [row for row in rows if row["orientation"] == "reversed"]
    oriented_comparison = comparison_signature[::-1] if best["orientation"] == "reversed" else comparison_signature
    shifted_index, shifted_values = shift_signature(oriented_comparison, int(best["lag_samples"]))
    dx_m = float(np.median(np.diff(x_m))) if x_m.size > 1 else 1.0
    shifted_x_m = shifted_index * dx_m

    fig, axes = plt.subplots(1, 2, figsize=(13.0, 4.8), constrained_layout=True)
    axes[0].plot([row["lag_mm"] for row in direct], [row["normalized_correlation"] for row in direct], marker="o", label="direct")
    axes[0].plot([row["lag_mm"] for row in reversed_rows], [row["normalized_correlation"] for row in reversed_rows], marker="s", label="reversed")
    axes[0].axvline(best["lag_mm"], color="#222222", linestyle="--", linewidth=1.0)
    axes[0].set_xlabel("comparison lag (mm)")
    axes[0].set_ylabel("normalized correlation")
    axes[0].set_title("Lag scan")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(x_m, reference_signature, color="#4c78a8", linewidth=1.7, label=reference_label)
    axes[1].plot(shifted_x_m, shifted_values, color="#f58518", linewidth=1.5, label=f"{comparison_label} aligned")
    axes[1].set_xlabel("profile distance after alignment (m)")
    axes[1].set_ylabel("robust normalized shallow cue")
    axes[1].set_title(f"Best alignment: {best['orientation']}, lag={best['lag_mm']:.1f} mm")
    axes[1].grid(color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Field profile shallow-pattern alignment", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def load_profile_map(input_dir: Path) -> dict[str, dict]:
    profiles = {}
    for record, raw in read_dzt_profiles(input_dir):
        processed = preprocess_profile(raw)
        x_m, time_ns = build_axes(record)
        profiles[record["stem"]] = {
            "record": record,
            "raw": raw,
            "processed": processed,
            "x_m": x_m,
            "time_ns": time_ns,
        }
    return profiles


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--reference-stem", default="PROJECT001C__014")
    parser.add_argument("--comparison-stem", default="PROJECT001C__016")
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--max-lag-m", type=float, default=0.12)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_alignment_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    time_min_ns, time_max_ns = [float(part.strip()) for part in args.time_window_ns.split(",", 1)]
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    profiles = load_profile_map(Path(args.input_dir))
    reference = profiles[args.reference_stem]
    comparison = profiles[args.comparison_stem]
    reference_x = reference["x_m"]
    comparison_x = comparison["x_m"]
    if reference_x.size != comparison_x.size:
        common_count = min(reference_x.size, comparison_x.size)
        common_x = np.linspace(0.0, min(float(reference_x[-1]), float(comparison_x[-1])), common_count)
    else:
        common_count = reference_x.size
        common_x = reference_x

    reference_sig = profile_signature(reference["processed"]["cue"], reference["time_ns"], time_min_ns, time_max_ns)
    comparison_sig = profile_signature(comparison["processed"]["cue"], comparison["time_ns"], time_min_ns, time_max_ns)
    if reference_sig.size != common_count:
        reference_sig = np.interp(common_x, reference_x, reference_sig)
    if comparison_sig.size != common_count:
        comparison_sig = np.interp(common_x, comparison_x, comparison_sig)

    dx_m = float(np.median(np.diff(common_x))) if common_x.size > 1 else 1.0
    rows = []
    rows.extend(alignment_rows(reference_sig, comparison_sig, dx_m, args.max_lag_m, "direct"))
    rows.extend(alignment_rows(reference_sig, comparison_sig, dx_m, args.max_lag_m, "reversed"))
    direct_best = best_alignment([row for row in rows if row["orientation"] == "direct"])
    reversed_best = best_alignment([row for row in rows if row["orientation"] == "reversed"])
    best = best_alignment(rows)
    label = classify_alignment(best, direct_best, reversed_best)

    lag_csv = data_dir / "profile_alignment_lag_scan.csv"
    summary_csv = data_dir / "profile_alignment_summary.csv"
    summary_json = data_dir / "profile_alignment_policy_summary.json"
    plot_path = Path(plot_alignment(
        args.reference_stem,
        args.comparison_stem,
        common_x,
        reference_sig,
        comparison_sig,
        rows,
        best,
        figures_dir / "short_profile_alignment.png",
    ))
    validation_csv = data_dir / "figure_validation.csv"

    summary = {
        "reference_stem": args.reference_stem,
        "comparison_stem": args.comparison_stem,
        "time_window_min_ns": time_min_ns,
        "time_window_max_ns": time_max_ns,
        "max_lag_m": args.max_lag_m,
        "sample_count": int(common_count),
        "dx_m": dx_m,
        "best_orientation": best["orientation"],
        "best_lag_mm": best["lag_mm"],
        "best_normalized_correlation": best["normalized_correlation"],
        "direct_best_lag_mm": direct_best["lag_mm"],
        "direct_best_normalized_correlation": direct_best["normalized_correlation"],
        "reversed_best_lag_mm": reversed_best["lag_mm"],
        "reversed_best_normalized_correlation": reversed_best["normalized_correlation"],
        "alignment_label": label,
        "policy": (
            "Use this as profile-level repeatability QC only. Strong or moderate "
            "alignment supports repeated shallow response structure, but it does "
            "not provide survey geometry, cover depth, radius, or FWI validation."
        ),
        "paths": {
            "lag_scan_csv": str(lag_csv),
            "summary_csv": str(summary_csv),
            "summary_json": str(summary_json),
            "alignment_plot": str(plot_path),
            "figure_validation_csv": str(validation_csv),
        },
    }

    write_csv(lag_csv, [json_safe(row) for row in rows])
    write_csv(summary_csv, [json_safe(summary)])
    write_csv(validation_csv, [figure_stats(plot_path)])
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_profile_alignment_policy",
        {
            "summary_json": str(summary_json),
            "lag_scan_csv": str(lag_csv),
            "summary_csv": str(summary_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
