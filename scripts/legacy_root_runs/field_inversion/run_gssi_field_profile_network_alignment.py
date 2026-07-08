#!/usr/bin/env python3
"""Pairwise shallow-pattern alignment network for local GSSI profiles."""

from __future__ import annotations

import argparse
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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, DEFAULT_INPUT_DIR, field_dataset_output_root  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_profile_alignment_policy import load_profile_map, profile_signature, robust_normalize  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


PROFILE_ORDER = (
    "PROJECT001C__013",
    "PROJECT001C__014",
    "PROJECT001C__015",
    "PROJECT001C__016",
)

CLASS_COLORS = {
    "repeat_candidate": "#1B7837",
    "embedded_segment_candidate": "#4575B4",
    "orientation_or_lag_ambiguous": "#D99A19",
    "weak_or_unrelated": "#C7302B",
}


def aligned_vectors_for_lag(reference: np.ndarray, comparison: np.ndarray, lag_samples: int) -> tuple[np.ndarray, np.ndarray]:
    """Return equal-length overlap for comparison start relative to reference."""
    ref = np.asarray(reference, dtype=np.float64)
    cmp = np.asarray(comparison, dtype=np.float64)
    lag = int(lag_samples)
    ref_start = max(0, lag)
    ref_stop = min(ref.size, lag + cmp.size)
    cmp_start = max(0, -lag)
    cmp_stop = cmp_start + max(0, ref_stop - ref_start)
    if ref_stop <= ref_start or cmp_stop <= cmp_start:
        return ref[:0], cmp[:0]
    return ref[ref_start:ref_stop], cmp[cmp_start:cmp_stop]


def normalized_overlap_correlation(reference: np.ndarray, comparison: np.ndarray, lag_samples: int, min_overlap: int) -> float:
    ref, cmp = aligned_vectors_for_lag(reference, comparison, lag_samples)
    if ref.size < int(min_overlap) or cmp.size < int(min_overlap):
        return math.nan
    ref = robust_normalize(ref)
    cmp = robust_normalize(cmp)
    denom = float(np.linalg.norm(ref) * np.linalg.norm(cmp))
    if denom <= 1.0e-12:
        return math.nan
    return float(np.dot(ref, cmp) / denom)


def pair_lag_rows(
    reference: np.ndarray,
    comparison: np.ndarray,
    dx_m: float,
    orientation: str,
    min_overlap_fraction: float,
) -> list[dict]:
    if orientation == "reversed":
        comparison = comparison[::-1]
    min_len = min(reference.size, comparison.size)
    min_overlap = min(min_len, max(3, int(math.ceil(min_len * float(min_overlap_fraction)))))
    lag_min = -comparison.size + min_overlap
    lag_max = reference.size - min_overlap
    rows = []
    for lag in range(lag_min, lag_max + 1):
        ref_overlap, cmp_overlap = aligned_vectors_for_lag(reference, comparison, lag)
        corr = normalized_overlap_correlation(reference, comparison, lag, min_overlap)
        rows.append({
            "orientation": orientation,
            "lag_samples": int(lag),
            "lag_mm": float(1000.0 * lag * dx_m),
            "overlap_samples": int(ref_overlap.size),
            "overlap_fraction_of_shorter": float(ref_overlap.size / min_len) if min_len else math.nan,
            "normalized_correlation": corr,
        })
    return rows


def best_alignment(rows: list[dict]) -> dict:
    valid = [row for row in rows if math.isfinite(float(row["normalized_correlation"]))]
    if not valid:
        raise ValueError("no valid pairwise alignment rows")
    return max(valid, key=lambda row: (float(row["normalized_correlation"]), float(row["overlap_fraction_of_shorter"]), -abs(float(row["lag_mm"]))))


def classify_pair(best: dict, direct_best: dict, reversed_best: dict, length_ratio: float) -> str:
    corr = float(best["normalized_correlation"])
    orientation_gap = abs(float(direct_best["normalized_correlation"]) - float(reversed_best["normalized_correlation"]))
    if corr < 0.70:
        return "weak_or_unrelated"
    if orientation_gap < 0.04:
        return "orientation_or_lag_ambiguous"
    if float(length_ratio) < 0.75:
        return "embedded_segment_candidate"
    return "repeat_candidate"


def profile_signature_entry(profile: dict, time_min_ns: float, time_max_ns: float) -> dict:
    x_m = profile["x_m"]
    signature = profile_signature(profile["processed"]["cue"], profile["time_ns"], time_min_ns, time_max_ns)
    dx_m = float(np.median(np.diff(x_m))) if x_m.size > 1 else 1.0
    return {
        "stem": profile["record"]["stem"],
        "file": profile["record"]["file"],
        "trace_count": int(x_m.size),
        "profile_length_m": float(x_m[-1]) if x_m.size else 0.0,
        "dx_m": dx_m,
        "signature": signature,
    }


def align_profile_pair(
    first: dict,
    second: dict,
    min_overlap_fraction: float,
) -> tuple[dict, list[dict]]:
    if first["trace_count"] >= second["trace_count"]:
        reference = first
        comparison = second
    else:
        reference = second
        comparison = first
    dx_m = min(float(reference["dx_m"]), float(comparison["dx_m"]))
    direct_rows = pair_lag_rows(reference["signature"], comparison["signature"], dx_m, "direct", min_overlap_fraction)
    reversed_rows = pair_lag_rows(reference["signature"], comparison["signature"], dx_m, "reversed", min_overlap_fraction)
    direct_best = best_alignment(direct_rows)
    reversed_best = best_alignment(reversed_rows)
    best = best_alignment(direct_rows + reversed_rows)
    length_ratio = min(first["trace_count"], second["trace_count"]) / max(first["trace_count"], second["trace_count"])
    label = classify_pair(best, direct_best, reversed_best, length_ratio)
    pair_summary = {
        "first_stem": first["stem"],
        "second_stem": second["stem"],
        "reference_stem": reference["stem"],
        "comparison_stem": comparison["stem"],
        "reference_trace_count": reference["trace_count"],
        "comparison_trace_count": comparison["trace_count"],
        "length_ratio": float(length_ratio),
        "best_orientation": best["orientation"],
        "best_lag_mm": best["lag_mm"],
        "best_overlap_samples": best["overlap_samples"],
        "best_overlap_fraction_of_shorter": best["overlap_fraction_of_shorter"],
        "best_normalized_correlation": best["normalized_correlation"],
        "direct_best_lag_mm": direct_best["lag_mm"],
        "direct_best_normalized_correlation": direct_best["normalized_correlation"],
        "reversed_best_lag_mm": reversed_best["lag_mm"],
        "reversed_best_normalized_correlation": reversed_best["normalized_correlation"],
        "pair_label": label,
    }
    lag_rows = []
    pair_id = f"{first['stem']}__{second['stem']}"
    for row in direct_rows + reversed_rows:
        lag_rows.append({
            "pair_id": pair_id,
            "first_stem": first["stem"],
            "second_stem": second["stem"],
            "reference_stem": reference["stem"],
            "comparison_stem": comparison["stem"],
            **row,
        })
    return pair_summary, lag_rows


def build_network(profile_entries: list[dict], min_overlap_fraction: float) -> tuple[list[dict], list[dict]]:
    pair_rows: list[dict] = []
    lag_rows: list[dict] = []
    for i, first in enumerate(profile_entries):
        for second in profile_entries[i + 1:]:
            pair, lags = align_profile_pair(first, second, min_overlap_fraction)
            pair_rows.append(pair)
            lag_rows.extend(lags)
    pair_rows.sort(key=lambda row: (row["first_stem"], row["second_stem"]))
    return pair_rows, lag_rows


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


def plot_network(pair_rows: list[dict], profile_stems: list[str], save_path: Path) -> None:
    index = {stem: i for i, stem in enumerate(profile_stems)}
    matrix = np.full((len(profile_stems), len(profile_stems)), np.nan)
    for row in pair_rows:
        i = index[row["first_stem"]]
        j = index[row["second_stem"]]
        value = float(row["best_normalized_correlation"])
        matrix[i, j] = value
        matrix[j, i] = value
    np.fill_diagonal(matrix, 1.0)

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.3), constrained_layout=True)
    im = axes[0].imshow(matrix, vmin=0.0, vmax=1.0, cmap="viridis")
    labels = [stem.replace("PROJECT001C__", "") for stem in profile_stems]
    axes[0].set_xticks(np.arange(len(labels)))
    axes[0].set_xticklabels(labels)
    axes[0].set_yticks(np.arange(len(labels)))
    axes[0].set_yticklabels(labels)
    axes[0].set_title("Best shallow-signature correlation")
    for i in range(len(labels)):
        for j in range(len(labels)):
            axes[0].text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white", fontsize=9)
    fig.colorbar(im, ax=axes[0], shrink=0.84)

    ordered_pairs = sorted(pair_rows, key=lambda row: float(row["best_normalized_correlation"]), reverse=True)
    x = np.arange(len(ordered_pairs))
    colors = [CLASS_COLORS.get(row["pair_label"], "#888888") for row in ordered_pairs]
    axes[1].bar(x, [row["best_normalized_correlation"] for row in ordered_pairs], color=colors, edgecolor="#333333")
    axes[1].axhline(0.85, color="#333333", linestyle="--", linewidth=1.0, label="strong threshold")
    axes[1].axhline(0.70, color="#666666", linestyle=":", linewidth=1.0, label="moderate threshold")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(
        [f"{row['first_stem'][-3:]}/{row['second_stem'][-3:]}\n{row['best_orientation']}" for row in ordered_pairs],
        rotation=0,
        fontsize=8,
    )
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_ylabel("best normalized correlation")
    axes[1].set_title("Pairwise alignment classes")
    axes[1].grid(True, axis="y", alpha=0.25)
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("Local GSSI profile network alignment", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)


def write_readme(path: Path, pair_rows: list[dict], summary: dict) -> None:
    strongest = max(pair_rows, key=lambda row: float(row["best_normalized_correlation"]))
    text = f"""# GSSI Profile Network Alignment

CPU-only pairwise shallow-pattern alignment across all imported local GSSI
profiles. This run tests repeat/subsegment relationships only; it is not FDTD,
FWI, geometry recovery, or 3D survey reconstruction.

Pairs: {len(pair_rows)}
Strongest pair: {strongest['first_stem']} / {strongest['second_stem']}
Best correlation: {strongest['best_normalized_correlation']:.4f}
Label: {strongest['pair_label']}

Decision:

```text
{summary['decision']}
```
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--profile-stems", default=",".join(PROFILE_ORDER))
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--min-overlap-fraction", type=float, default=0.80)
    parser.add_argument("--run-name", default="gssi51600s_profile_network_alignment")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    time_min_ns, time_max_ns = [float(part.strip()) for part in args.time_window_ns.split(",", 1)]
    requested_stems = [part.strip() for part in args.profile_stems.split(",") if part.strip()]
    profiles = load_profile_map(Path(args.input_dir))
    missing = [stem for stem in requested_stems if stem not in profiles]
    if missing:
        raise ValueError(f"missing requested profile stems: {missing}")
    entries = [profile_signature_entry(profiles[stem], time_min_ns, time_max_ns) for stem in requested_stems]
    pair_rows, lag_rows = build_network(entries, args.min_overlap_fraction)

    class_counts = {label: sum(1 for row in pair_rows if row["pair_label"] == label) for label in sorted(CLASS_COLORS)}
    strongest = max(pair_rows, key=lambda row: float(row["best_normalized_correlation"]))
    decision = (
        "The local GSSI profiles support profile-level repeat/subsegment QC, "
        "but pairwise correlations and missing survey-layout metadata still do "
        "not make the dataset a 3D survey or a field inversion benchmark."
    )
    summary = {
        "time_window_min_ns": time_min_ns,
        "time_window_max_ns": time_max_ns,
        "min_overlap_fraction": args.min_overlap_fraction,
        "profile_count": len(entries),
        "pair_count": len(pair_rows),
        "pair_label_counts": class_counts,
        "strongest_pair": strongest,
        "decision": decision,
        "policy": (
            "Use strong pairwise alignment as field repeatability/QC evidence. "
            "Do not infer crossline spacing, cover depth, radius, 3D geometry, "
            "or field FWI validity from this alignment network alone."
        ),
    }

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    pair_csv = data_dir / "profile_network_alignment_pairs.csv"
    lag_csv = data_dir / "profile_network_alignment_lag_scan.csv"
    summary_json = data_dir / "profile_network_alignment_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "profile_network_alignment.png"
    readme_path = outdir / "README.md"

    plot_network(pair_rows, requested_stems, figure_path)
    write_csv(pair_csv, [json_safe(row) for row in pair_rows])
    write_csv(lag_csv, [json_safe(row) for row in lag_rows])
    write_csv(validation_csv, [figure_stats(figure_path)])
    summary["paths"] = {
        "pair_csv": str(pair_csv),
        "lag_scan_csv": str(lag_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
        "readme": str(readme_path),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_readme(readme_path, pair_rows, summary)
    write_run_manifest(
        str(outdir),
        "gssi_field_profile_network_alignment",
        {
            "summary_json": str(summary_json),
            "pair_csv": str(pair_csv),
            "lag_scan_csv": str(lag_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
