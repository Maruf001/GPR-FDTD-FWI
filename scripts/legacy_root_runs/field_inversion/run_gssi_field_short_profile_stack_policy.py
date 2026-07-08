#!/usr/bin/env python3
"""Repeat-aligned short-profile stack policy for local GSSI field data."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

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
from run_gssi_field_profile_alignment_policy import (  # noqa: E402
    alignment_rows,
    best_alignment,
    classify_alignment,
    figure_stats,
    load_profile_map,
    profile_signature,
)
from run_gssi_field_profile_repeatability_policy import read_csv_rows, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def common_axis(reference_x: np.ndarray, comparison_x: np.ndarray) -> np.ndarray:
    if reference_x.size != comparison_x.size:
        count = min(reference_x.size, comparison_x.size)
        xmax = min(float(reference_x[-1]), float(comparison_x[-1]))
        return np.linspace(0.0, xmax, count)
    return np.asarray(reference_x, dtype=np.float64)


def align_comparison_to_reference(
    comparison: np.ndarray,
    orientation: str,
    lag_samples: int,
) -> np.ndarray:
    values = np.asarray(comparison, dtype=np.float64)
    if orientation == "reversed":
        values = values[::-1]
    elif orientation != "direct":
        raise ValueError(f"unknown orientation {orientation!r}")

    aligned = np.full(values.shape, np.nan, dtype=np.float64)
    if lag_samples > 0:
        aligned[:-lag_samples] = values[lag_samples:]
    elif lag_samples < 0:
        aligned[-lag_samples:] = values[:lag_samples]
    else:
        aligned[:] = values
    return aligned


def aligned_event_x_m(
    original_x_m: float,
    profile_length_m: float,
    orientation: str,
    lag_m: float,
) -> float:
    x = float(original_x_m)
    if orientation == "reversed":
        x = float(profile_length_m) - x
    elif orientation != "direct":
        raise ValueError(f"unknown orientation {orientation!r}")
    return x - float(lag_m)


def build_stack_rows(
    x_m: np.ndarray,
    reference_signature: np.ndarray,
    aligned_comparison_signature: np.ndarray,
) -> list[dict]:
    rows = []
    for idx, (x_val, ref_val, cmp_val) in enumerate(zip(x_m, reference_signature, aligned_comparison_signature)):
        both_present = math.isfinite(float(ref_val)) and math.isfinite(float(cmp_val))
        if both_present:
            stack = 0.5 * (float(ref_val) + float(cmp_val))
            delta = abs(float(ref_val) - float(cmp_val))
            repeat_score = stack - 0.5 * delta
        else:
            stack = math.nan
            delta = math.nan
            repeat_score = math.nan
        rows.append({
            "sample_index": idx,
            "x_m": float(x_val),
            "x_mm": 1000.0 * float(x_val),
            "reference_signature_z": float(ref_val),
            "aligned_comparison_signature_z": float(cmp_val) if math.isfinite(float(cmp_val)) else math.nan,
            "stack_signature_z": stack,
            "repeat_delta_z": delta,
            "repeat_score_z": repeat_score,
            "both_profiles_present": both_present,
        })
    return rows


def find_stack_anchor_candidates(
    stack_rows: list[dict],
    min_separation_m: float,
    min_stack_z: float,
    max_repeat_delta_z: float,
    max_count: int,
) -> list[dict]:
    values = np.asarray([safe_float(row["stack_signature_z"]) for row in stack_rows], dtype=np.float64)
    repeat_delta = np.asarray([safe_float(row["repeat_delta_z"]) for row in stack_rows], dtype=np.float64)
    x_values = np.asarray([safe_float(row["x_m"]) for row in stack_rows], dtype=np.float64)
    peaks: list[dict] = []
    for idx in range(1, len(values) - 1):
        if not (math.isfinite(values[idx]) and math.isfinite(repeat_delta[idx])):
            continue
        if values[idx] < min_stack_z or repeat_delta[idx] > max_repeat_delta_z:
            continue
        if values[idx] < values[idx - 1] or values[idx] < values[idx + 1]:
            continue
        prominence = values[idx] - max(values[idx - 1], values[idx + 1])
        peaks.append({
            **stack_rows[idx],
            "candidate_rank_score": float(values[idx] - 0.5 * repeat_delta[idx] + max(0.0, prominence)),
            "local_prominence_z": float(prominence),
        })

    selected: list[dict] = []
    for peak in sorted(peaks, key=lambda row: row["candidate_rank_score"], reverse=True):
        if all(abs(float(peak["x_m"]) - float(prev["x_m"])) >= min_separation_m for prev in selected):
            selected.append(peak)
        if len(selected) >= max_count:
            break
    selected.sort(key=lambda row: row["x_m"])
    for idx, row in enumerate(selected, start=1):
        row["candidate_index"] = idx
        row["stability_label"] = (
            "stable_stack_anchor"
            if float(row["repeat_delta_z"]) <= 0.75 and float(row["stack_signature_z"]) >= min_stack_z
            else "repeat_limited_anchor"
        )
    return selected


def _event_file_selected(file_name: str, stem: str) -> bool:
    return Path(file_name).stem == stem


def reversed_event_pairs(
    event_rows: list[dict],
    reference_stem: str,
    comparison_stem: str,
    comparison_profile_length_m: float,
    orientation: str,
    lag_m: float,
    max_pair_distance_m: float,
) -> list[dict]:
    reference = sorted(
        [row for row in event_rows if _event_file_selected(str(row.get("file", "")), reference_stem)],
        key=lambda row: safe_float(row.get("x_m")),
    )
    comparison = sorted(
        [row for row in event_rows if _event_file_selected(str(row.get("file", "")), comparison_stem)],
        key=lambda row: aligned_event_x_m(
            safe_float(row.get("x_m")),
            comparison_profile_length_m,
            orientation,
            lag_m,
        ),
    )
    available = set(range(len(comparison)))
    pairs: list[dict] = []
    for ref in reference:
        ref_x = safe_float(ref.get("x_m"))
        best_idx = None
        best_distance = math.inf
        for idx in available:
            cmp = comparison[idx]
            cmp_x = aligned_event_x_m(
                safe_float(cmp.get("x_m")),
                comparison_profile_length_m,
                orientation,
                lag_m,
            )
            distance = abs(cmp_x - ref_x)
            if distance < best_distance:
                best_distance = distance
                best_idx = idx
        if best_idx is None or best_distance > max_pair_distance_m:
            continue
        available.remove(best_idx)
        cmp = comparison[best_idx]
        cmp_x = aligned_event_x_m(safe_float(cmp.get("x_m")), comparison_profile_length_m, orientation, lag_m)
        ref_time = safe_float(ref.get("accepted_phase_time_ns"))
        cmp_time = safe_float(cmp.get("accepted_phase_time_ns"))
        ref_radius = safe_float(ref.get("best_radius_mm"))
        cmp_radius = safe_float(cmp.get("best_radius_mm"))
        pairs.append({
            "pair_index": len(pairs) + 1,
            "reference_file": ref.get("file", ""),
            "comparison_file": cmp.get("file", ""),
            "reference_apex_group": int(safe_float(ref.get("apex_group"), -1)),
            "comparison_apex_group": int(safe_float(cmp.get("apex_group"), -1)),
            "reference_x_m": ref_x,
            "comparison_original_x_m": safe_float(cmp.get("x_m")),
            "comparison_aligned_x_m": cmp_x,
            "aligned_x_residual_mm": 1000.0 * (cmp_x - ref_x),
            "reference_phase_time_ns": ref_time,
            "comparison_phase_time_ns": cmp_time,
            "comparison_minus_reference_phase_time_ns": cmp_time - ref_time,
            "reference_best_radius_mm": ref_radius,
            "comparison_best_radius_mm": cmp_radius,
            "radius_match": bool(math.isclose(ref_radius, cmp_radius, abs_tol=1.0e-9)),
            "reference_best_abs_correlation": safe_float(ref.get("best_abs_correlation")),
            "comparison_best_abs_correlation": safe_float(cmp.get("best_abs_correlation")),
        })
    return pairs


def summarize_policy(best: dict, direct_best: dict, reversed_best: dict, anchor_rows: list[dict], event_pairs: list[dict]) -> dict:
    residuals = [abs(safe_float(row["aligned_x_residual_mm"])) for row in event_pairs]
    time_deltas = [safe_float(row["comparison_minus_reference_phase_time_ns"]) for row in event_pairs]
    radius_matches = sum(1 for row in event_pairs if bool(row["radius_match"]))
    stable_count = sum(1 for row in anchor_rows if row["stability_label"] == "stable_stack_anchor")
    if stable_count >= 3 and len(event_pairs) >= 3 and np.nanmax(residuals) <= 25.0:
        label = "repeat_stack_timing_qc_ready"
    elif stable_count >= 2 and len(event_pairs) >= 2:
        label = "repeat_stack_limited_qc"
    else:
        label = "repeat_stack_not_stable"
    return {
        "best_orientation": best["orientation"],
        "best_lag_mm": best["lag_mm"],
        "best_normalized_correlation": best["normalized_correlation"],
        "direct_best_normalized_correlation": direct_best["normalized_correlation"],
        "reversed_best_normalized_correlation": reversed_best["normalized_correlation"],
        "alignment_label": classify_alignment(best, direct_best, reversed_best),
        "stack_anchor_candidate_count": len(anchor_rows),
        "stable_stack_anchor_count": stable_count,
        "event_pair_count": len(event_pairs),
        "mean_abs_aligned_event_residual_mm": float(np.nanmean(residuals)) if residuals else math.nan,
        "max_abs_aligned_event_residual_mm": float(np.nanmax(residuals)) if residuals else math.nan,
        "median_comparison_minus_reference_phase_time_ns": float(np.nanmedian(time_deltas)) if time_deltas else math.nan,
        "mean_abs_comparison_minus_reference_phase_time_ns": float(np.nanmean(np.abs(time_deltas))) if time_deltas else math.nan,
        "radius_match_count": radius_matches,
        "radius_match_fraction": radius_matches / len(event_pairs) if event_pairs else math.nan,
        "policy_label": label,
        "policy": (
            "Use the reversed short-profile stack as repeatability and timing-QC evidence. "
            "It does not provide field radius, cover depth, survey geometry, or field FWI validation."
        ),
    }


def plot_stack_policy(
    x_m: np.ndarray,
    reference_signature: np.ndarray,
    aligned_comparison_signature: np.ndarray,
    stack_rows: list[dict],
    anchor_rows: list[dict],
    event_pairs: list[dict],
    summary: dict,
    save_path: Path,
) -> str:
    stack = np.asarray([safe_float(row["stack_signature_z"]) for row in stack_rows], dtype=np.float64)
    repeat_delta = np.asarray([safe_float(row["repeat_delta_z"]) for row in stack_rows], dtype=np.float64)

    fig, axes = plt.subplots(3, 1, figsize=(13.0, 9.2), constrained_layout=True)
    axes[0].plot(x_m, reference_signature, color="#4c78a8", linewidth=1.4, label="014 reference")
    axes[0].plot(x_m, aligned_comparison_signature, color="#f58518", linewidth=1.2, label="016 aligned")
    axes[0].plot(x_m, stack, color="#2ca02c", linewidth=1.8, label="stack")
    for row in anchor_rows:
        axes[0].axvline(safe_float(row["x_m"]), color="#222222", linestyle="--", linewidth=0.8, alpha=0.65)
    axes[0].set_ylabel("shallow cue z")
    axes[0].set_title("Repeat-aligned shallow-response stack")
    axes[0].grid(color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].plot(x_m, repeat_delta, color="#7f3c8d", linewidth=1.4)
    axes[1].axhline(0.75, color="#555555", linestyle="--", linewidth=0.9)
    axes[1].set_ylabel("|014 - 016| z")
    axes[1].set_title("Repeat disagreement after alignment")
    axes[1].grid(color="#dddddd", linewidth=0.6)

    pair_labels = [str(row["pair_index"]) for row in event_pairs]
    residuals = [safe_float(row["aligned_x_residual_mm"]) for row in event_pairs]
    time_deltas = [safe_float(row["comparison_minus_reference_phase_time_ns"]) for row in event_pairs]
    x = np.arange(len(event_pairs))
    axes[2].bar(x - 0.18, residuals, width=0.36, color="#4c78a8", label="x residual mm")
    axes[2].bar(x + 0.18, [100.0 * value for value in time_deltas], width=0.36, color="#f58518", label="phase delta x100 ns")
    axes[2].axhline(0.0, color="#444444", linewidth=0.8)
    axes[2].set_xticks(x, pair_labels)
    axes[2].set_xlabel("reversed event pair")
    axes[2].set_ylabel("residual / scaled time")
    axes[2].set_title("Nearest event pairs under reversed alignment")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[2].legend(frameon=False, fontsize=8)

    fig.suptitle(
        "Short-profile repeat stack: "
        f"{summary['policy_label']}, corr={summary['best_normalized_correlation']:.3f}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--repeatability-dir", default=None)
    parser.add_argument("--reference-stem", default="PROJECT001C__014")
    parser.add_argument("--comparison-stem", default="PROJECT001C__016")
    parser.add_argument("--time-window-ns", default="0.45,1.25")
    parser.add_argument("--max-lag-m", type=float, default=0.12)
    parser.add_argument("--min-anchor-separation-m", type=float, default=0.08)
    parser.add_argument("--min-stack-z", type=float, default=0.75)
    parser.add_argument("--max-repeat-delta-z", type=float, default=1.25)
    parser.add_argument("--max-anchor-count", type=int, default=6)
    parser.add_argument("--max-event-pair-distance-m", type=float, default=0.06)
    parser.add_argument("--run-name", default="gssi51600s_short_profile_stack_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    time_min_ns, time_max_ns = [float(part.strip()) for part in args.time_window_ns.split(",", 1)]
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    repeatability_dir = (
        Path(args.repeatability_dir)
        if args.repeatability_dir is not None
        else dataset_root / "018_gssi51600s_short_profile_repeatability_policy"
    )

    profiles = load_profile_map(Path(args.input_dir))
    reference = profiles[args.reference_stem]
    comparison = profiles[args.comparison_stem]
    x_m = common_axis(reference["x_m"], comparison["x_m"])
    reference_sig = profile_signature(reference["processed"]["cue"], reference["time_ns"], time_min_ns, time_max_ns)
    comparison_sig = profile_signature(comparison["processed"]["cue"], comparison["time_ns"], time_min_ns, time_max_ns)
    if reference_sig.size != x_m.size:
        reference_sig = np.interp(x_m, reference["x_m"], reference_sig)
    if comparison_sig.size != x_m.size:
        comparison_sig = np.interp(x_m, comparison["x_m"], comparison_sig)

    dx_m = float(np.median(np.diff(x_m))) if x_m.size > 1 else 1.0
    rows = []
    rows.extend(alignment_rows(reference_sig, comparison_sig, dx_m, args.max_lag_m, "direct"))
    rows.extend(alignment_rows(reference_sig, comparison_sig, dx_m, args.max_lag_m, "reversed"))
    direct_best = best_alignment([row for row in rows if row["orientation"] == "direct"])
    reversed_best = best_alignment([row for row in rows if row["orientation"] == "reversed"])
    best = best_alignment(rows)
    lag_samples = int(best["lag_samples"])
    lag_m = float(best["lag_m"])
    aligned_cmp = align_comparison_to_reference(comparison_sig, str(best["orientation"]), lag_samples)

    stack_rows = build_stack_rows(x_m, reference_sig, aligned_cmp)
    anchor_rows = find_stack_anchor_candidates(
        stack_rows,
        args.min_anchor_separation_m,
        args.min_stack_z,
        args.max_repeat_delta_z,
        args.max_anchor_count,
    )

    event_csv = repeatability_dir / "data" / "short_profile_event_table.csv"
    event_pairs = reversed_event_pairs(
        read_csv_rows(event_csv),
        args.reference_stem,
        args.comparison_stem,
        float(x_m[-1]) if x_m.size else 0.0,
        str(best["orientation"]),
        lag_m,
        args.max_event_pair_distance_m,
    )
    summary = summarize_policy(best, direct_best, reversed_best, anchor_rows, event_pairs)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    lag_csv = data_dir / "short_profile_stack_lag_scan.csv"
    stack_csv = data_dir / "short_profile_stack_signal.csv"
    anchors_csv = data_dir / "short_profile_stack_anchor_candidates.csv"
    event_pairs_csv = data_dir / "short_profile_reversed_event_pairs.csv"
    summary_json = data_dir / "short_profile_stack_policy_summary.json"
    figure_path = Path(plot_stack_policy(
        x_m,
        reference_sig,
        aligned_cmp,
        stack_rows,
        anchor_rows,
        event_pairs,
        summary,
        figures_dir / "short_profile_stack_policy.png",
    ))
    validation_csv = data_dir / "figure_validation.csv"

    write_csv(lag_csv, [json_safe(row) for row in rows])
    write_csv(stack_csv, [json_safe(row) for row in stack_rows])
    write_csv(anchors_csv, [json_safe(row) for row in anchor_rows])
    write_csv(event_pairs_csv, [json_safe(row) for row in event_pairs])
    validation_rows = [figure_stats(figure_path)]
    write_csv(validation_csv, [json_safe(row) for row in validation_rows])

    output_summary = {
        "reference_stem": args.reference_stem,
        "comparison_stem": args.comparison_stem,
        "time_window_min_ns": time_min_ns,
        "time_window_max_ns": time_max_ns,
        "dx_m": dx_m,
        "sample_count": int(x_m.size),
        "summary": summary,
        "paths": {
            "lag_scan_csv": str(lag_csv),
            "stack_signal_csv": str(stack_csv),
            "anchor_candidates_csv": str(anchors_csv),
            "event_pairs_csv": str(event_pairs_csv),
            "summary_json": str(summary_json),
            "stack_policy_plot": str(figure_path),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_profile_stack_policy",
        {
            "summary_json": str(summary_json),
            "event_csv": str(event_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
