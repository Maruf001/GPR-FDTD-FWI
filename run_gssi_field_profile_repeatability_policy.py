#!/usr/bin/env python3
"""Short-profile repeatability policy for local GSSI field data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict
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


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _mode(values: list[float]) -> tuple[float, int]:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    if not finite:
        return math.nan, 0
    key, count = Counter(finite).most_common(1)[0]
    return float(key), int(count)


def _file_selected(file_name: str, profile_stems: set[str]) -> bool:
    if not profile_stems:
        return True
    return Path(file_name).stem in profile_stems


def build_event_rows(
    phase_pick_rows: list[dict],
    phase_fit_rows: list[dict],
    identifiability_rows: list[dict],
    phase_convention: str,
    profile_stems: set[str],
) -> list[dict]:
    picks_by_key = {
        (str(row.get("file", "")), int(safe_float(row.get("apex_group"), -1))): row
        for row in phase_pick_rows
        if _file_selected(str(row.get("file", "")), profile_stems)
    }
    ident_by_key = {
        (str(row.get("file", "")), int(safe_float(row.get("apex_group"), -1))): row
        for row in identifiability_rows
        if _file_selected(str(row.get("file", "")), profile_stems)
    }
    rows: list[dict] = []
    for fit in phase_fit_rows:
        if str(fit.get("phase_convention", "")) != phase_convention:
            continue
        file_name = str(fit.get("file", ""))
        if not _file_selected(file_name, profile_stems):
            continue
        apex_group = int(safe_float(fit.get("apex_group"), -1))
        key = (file_name, apex_group)
        pick = picks_by_key.get(key, {})
        ident = ident_by_key.get(key, {})
        rows.append({
            "file": file_name,
            "profile_stem": Path(file_name).stem,
            "channel": int(safe_float(fit.get("channel"), 0)),
            "apex_group": apex_group,
            "x_m": safe_float(fit.get("x_m")),
            "phase_convention": phase_convention,
            "accepted_phase_time_ns": safe_float(fit.get("apex_time_ns")),
            "current_cue_time_ns": safe_float(pick.get("current_cue_time_ns")),
            "top_envelope_35pct_time_ns": safe_float(pick.get("top_envelope_35pct_time_ns")),
            "local_snr": safe_float(pick.get("local_snr")),
            "phase_quality_flag": str(pick.get("phase_quality_flag", "")),
            "fitted_tx_rx_offset_mm": safe_float(fit.get("tx_rx_offset_mm")),
            "fitted_velocity_m_per_ns": safe_float(fit.get("fitted_velocity_m_per_ns")),
            "fitted_epsr": safe_float(fit.get("fitted_epsr")),
            "fitted_time_zero_ns": safe_float(fit.get("fitted_time_zero_ns")),
            "fitted_depth_mm": 1000.0 * safe_float(fit.get("fitted_depth_m")),
            "template_score": safe_float(fit.get("template_score")),
            "support_fraction": safe_float(fit.get("support_fraction")),
            "best_abs_correlation": safe_float(ident.get("best_abs_correlation")),
            "best_radius_mm": safe_float(ident.get("best_radius_mm")),
            "radius_margin_abs": safe_float(ident.get("radius_margin_abs")),
            "best_epsr_source": str(ident.get("best_epsr_source", "")),
            "epsr_margin_abs": safe_float(ident.get("epsr_margin_abs")),
            "best_polarity": str(ident.get("best_polarity", "")),
        })
    rows.sort(key=lambda row: (row["profile_stem"], row["x_m"], row["apex_group"]))
    return rows


def summarize_profiles(event_rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in event_rows:
        grouped[str(row["file"])].append(row)
    out: list[dict] = []
    for file_name, rows in sorted(grouped.items()):
        rows = sorted(rows, key=lambda row: row["x_m"])
        x_values = np.asarray([safe_float(row["x_m"]) for row in rows], dtype=np.float64)
        spacings = np.diff(x_values) if x_values.size >= 2 else np.asarray([], dtype=np.float64)
        radii = [safe_float(row["best_radius_mm"]) for row in rows]
        radius_mode, radius_mode_count = _mode(radii)
        correlations = [safe_float(row["best_abs_correlation"]) for row in rows]
        depths = [safe_float(row["fitted_depth_mm"]) for row in rows]
        times = [safe_float(row["accepted_phase_time_ns"]) for row in rows]
        out.append({
            "file": file_name,
            "profile_stem": Path(file_name).stem,
            "event_count": len(rows),
            "x_min_m": float(np.nanmin(x_values)) if x_values.size else math.nan,
            "x_max_m": float(np.nanmax(x_values)) if x_values.size else math.nan,
            "mean_spacing_mm": float(1000.0 * np.nanmean(spacings)) if spacings.size else math.nan,
            "min_spacing_mm": float(1000.0 * np.nanmin(spacings)) if spacings.size else math.nan,
            "max_spacing_mm": float(1000.0 * np.nanmax(spacings)) if spacings.size else math.nan,
            "spacing_cv": (
                float(np.nanstd(spacings) / np.nanmean(spacings))
                if spacings.size and abs(float(np.nanmean(spacings))) > 1.0e-12
                else math.nan
            ),
            "mean_phase_time_ns": float(np.nanmean(times)) if times else math.nan,
            "mean_fitted_depth_mm": float(np.nanmean(depths)) if depths else math.nan,
            "radius_mode_mm": radius_mode,
            "radius_mode_count": radius_mode_count,
            "radius_consensus_fraction": radius_mode_count / len(rows) if rows else math.nan,
            "mean_best_abs_correlation": float(np.nanmean(correlations)) if correlations else math.nan,
            "min_best_abs_correlation": float(np.nanmin(correlations)) if correlations else math.nan,
        })
    return out


def pair_profiles(event_rows: list[dict]) -> tuple[list[dict], list[dict], dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in event_rows:
        grouped[str(row["file"])].append(row)
    files = sorted(grouped)
    if len(files) != 2:
        raise ValueError(f"profile repeatability pairing requires exactly two profiles, got {len(files)}")
    reference_file, comparison_file = files
    reference = sorted(grouped[reference_file], key=lambda row: row["x_m"])
    comparison = sorted(grouped[comparison_file], key=lambda row: row["x_m"])
    pair_count = min(len(reference), len(comparison))
    if pair_count == 0:
        raise ValueError("no events available for profile pairing")
    raw_shifts = np.asarray(
        [safe_float(comparison[idx]["x_m"]) - safe_float(reference[idx]["x_m"]) for idx in range(pair_count)],
        dtype=np.float64,
    )
    median_lateral_shift_m = float(np.nanmedian(raw_shifts))
    pair_rows: list[dict] = []
    for idx in range(pair_count):
        ref = reference[idx]
        cmp = comparison[idx]
        aligned_cmp_x = safe_float(cmp["x_m"]) - median_lateral_shift_m
        residual_m = aligned_cmp_x - safe_float(ref["x_m"])
        pair_rows.append({
            "pair_index": idx + 1,
            "reference_file": reference_file,
            "comparison_file": comparison_file,
            "reference_apex_group": ref["apex_group"],
            "comparison_apex_group": cmp["apex_group"],
            "reference_x_m": ref["x_m"],
            "comparison_x_m": cmp["x_m"],
            "raw_lateral_shift_mm": 1000.0 * (safe_float(cmp["x_m"]) - safe_float(ref["x_m"])),
            "aligned_comparison_x_m": aligned_cmp_x,
            "aligned_x_residual_mm": 1000.0 * residual_m,
            "reference_phase_time_ns": ref["accepted_phase_time_ns"],
            "comparison_phase_time_ns": cmp["accepted_phase_time_ns"],
            "phase_time_delta_ns": safe_float(cmp["accepted_phase_time_ns"]) - safe_float(ref["accepted_phase_time_ns"]),
            "reference_fitted_depth_mm": ref["fitted_depth_mm"],
            "comparison_fitted_depth_mm": cmp["fitted_depth_mm"],
            "fitted_depth_delta_mm": safe_float(cmp["fitted_depth_mm"]) - safe_float(ref["fitted_depth_mm"]),
            "reference_best_abs_correlation": ref["best_abs_correlation"],
            "comparison_best_abs_correlation": cmp["best_abs_correlation"],
            "best_abs_correlation_delta": safe_float(cmp["best_abs_correlation"]) - safe_float(ref["best_abs_correlation"]),
            "reference_best_radius_mm": ref["best_radius_mm"],
            "comparison_best_radius_mm": cmp["best_radius_mm"],
            "radius_match": bool(math.isclose(safe_float(ref["best_radius_mm"]), safe_float(cmp["best_radius_mm"]), abs_tol=1.0e-9)),
            "reference_radius_margin_abs": ref["radius_margin_abs"],
            "comparison_radius_margin_abs": cmp["radius_margin_abs"],
        })
    spacing_rows: list[dict] = []
    for idx in range(pair_count - 1):
        ref_spacing_m = safe_float(reference[idx + 1]["x_m"]) - safe_float(reference[idx]["x_m"])
        cmp_spacing_m = safe_float(comparison[idx + 1]["x_m"]) - safe_float(comparison[idx]["x_m"])
        spacing_rows.append({
            "spacing_index": idx + 1,
            "reference_file": reference_file,
            "comparison_file": comparison_file,
            "reference_spacing_mm": 1000.0 * ref_spacing_m,
            "comparison_spacing_mm": 1000.0 * cmp_spacing_m,
            "spacing_delta_mm": 1000.0 * (cmp_spacing_m - ref_spacing_m),
            "abs_spacing_delta_mm": abs(1000.0 * (cmp_spacing_m - ref_spacing_m)),
        })
    summary = build_repeatability_summary(pair_rows, spacing_rows, reference_file, comparison_file, median_lateral_shift_m)
    return pair_rows, spacing_rows, summary


def build_repeatability_summary(
    pair_rows: list[dict],
    spacing_rows: list[dict],
    reference_file: str,
    comparison_file: str,
    median_lateral_shift_m: float,
) -> dict:
    residuals = [abs(safe_float(row["aligned_x_residual_mm"])) for row in pair_rows]
    spacing_deltas = [safe_float(row["abs_spacing_delta_mm"]) for row in spacing_rows]
    time_deltas = [abs(safe_float(row["phase_time_delta_ns"])) for row in pair_rows]
    corr_values = [
        safe_float(row[key])
        for row in pair_rows
        for key in ("reference_best_abs_correlation", "comparison_best_abs_correlation")
    ]
    radius_matches = sum(1 for row in pair_rows if row["radius_match"])
    mean_abs_spacing_delta_mm = float(np.nanmean(spacing_deltas)) if spacing_deltas else math.nan
    max_abs_aligned_x_residual_mm = float(np.nanmax(residuals)) if residuals else math.nan
    radius_match_fraction = radius_matches / len(pair_rows) if pair_rows else math.nan
    if (
        math.isfinite(mean_abs_spacing_delta_mm)
        and mean_abs_spacing_delta_mm <= 35.0
        and math.isfinite(max_abs_aligned_x_residual_mm)
        and max_abs_aligned_x_residual_mm <= 35.0
        and radius_match_fraction < 0.67
    ):
        label = "spacing_repeatable_radius_not_repeatable"
    elif (
        math.isfinite(mean_abs_spacing_delta_mm)
        and mean_abs_spacing_delta_mm <= 35.0
        and math.isfinite(max_abs_aligned_x_residual_mm)
        and max_abs_aligned_x_residual_mm <= 35.0
    ):
        label = "spacing_repeatable"
    else:
        label = "weak_profile_repeatability"
    return {
        "reference_file": reference_file,
        "comparison_file": comparison_file,
        "event_pair_count": len(pair_rows),
        "spacing_pair_count": len(spacing_rows),
        "median_lateral_shift_mm": 1000.0 * median_lateral_shift_m,
        "mean_abs_aligned_x_residual_mm": float(np.nanmean(residuals)) if residuals else math.nan,
        "max_abs_aligned_x_residual_mm": max_abs_aligned_x_residual_mm,
        "mean_abs_spacing_delta_mm": mean_abs_spacing_delta_mm,
        "max_abs_spacing_delta_mm": float(np.nanmax(spacing_deltas)) if spacing_deltas else math.nan,
        "mean_abs_phase_time_delta_ns": float(np.nanmean(time_deltas)) if time_deltas else math.nan,
        "max_abs_phase_time_delta_ns": float(np.nanmax(time_deltas)) if time_deltas else math.nan,
        "radius_match_count": radius_matches,
        "radius_match_fraction": radius_match_fraction,
        "mean_best_abs_correlation": float(np.nanmean(corr_values)) if corr_values else math.nan,
        "min_best_abs_correlation": float(np.nanmin(corr_values)) if corr_values else math.nan,
        "repeatability_label": label,
        "policy": (
            "Use the short profiles as repeatable shallow-reflector QC evidence only. "
            "The paired spacing pattern is informative, but absent survey geometry and "
            "weak radius-repeatability margins still block field geometry/radius claims."
        ),
    }


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


def plot_repeatability(pair_rows: list[dict], spacing_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [str(row["pair_index"]) for row in pair_rows]
    ref_x = [safe_float(row["reference_x_m"]) * 1000.0 for row in pair_rows]
    cmp_x = [safe_float(row["aligned_comparison_x_m"]) * 1000.0 for row in pair_rows]
    time_delta = [safe_float(row["phase_time_delta_ns"]) for row in pair_rows]
    spacing_labels = [str(row["spacing_index"]) for row in spacing_rows]
    spacing_delta = [safe_float(row["spacing_delta_mm"]) for row in spacing_rows]

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), constrained_layout=True)
    axes[0].plot(labels, ref_x, marker="o", label="reference")
    axes[0].plot(labels, cmp_x, marker="s", label="comparison aligned")
    axes[0].set_xlabel("event order")
    axes[0].set_ylabel("aligned x (mm)")
    axes[0].set_title("Aligned event positions")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(labels, time_delta, color="#4c78a8")
    axes[1].axhline(0.0, color="#444444", linewidth=0.8)
    axes[1].set_xlabel("event order")
    axes[1].set_ylabel("phase-time delta (ns)")
    axes[1].set_title("Accepted-phase timing")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[2].bar(spacing_labels, spacing_delta, color="#f58518")
    axes[2].axhline(0.0, color="#444444", linewidth=0.8)
    axes[2].set_xlabel("adjacent spacing")
    axes[2].set_ylabel("comparison - reference (mm)")
    axes[2].set_title("Spacing delta")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Short-profile field repeatability: {summary['repeatability_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--phase-anchor-dir", default=None)
    parser.add_argument("--identifiability-dir", default=None)
    parser.add_argument("--phase-convention", default="top_envelope_35pct")
    parser.add_argument("--profile-stems", default="PROJECT001C__014,PROJECT001C__016")
    parser.add_argument("--run-name", default="gssi51600s_short_profile_repeatability_policy")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    phase_anchor_dir = (
        Path(args.phase_anchor_dir)
        if args.phase_anchor_dir is not None
        else dataset_root / "006_gssi51600s_phase_anchor_qc"
    )
    identifiability_dir = (
        Path(args.identifiability_dir)
        if args.identifiability_dir is not None
        else dataset_root / "014_gssi51600s_field_identifiability_policy"
    )
    profile_stems = {part.strip() for part in args.profile_stems.split(",") if part.strip()}

    phase_pick_csv = phase_anchor_dir / "data" / "field_phase_anchor_picks.csv"
    phase_fit_csv = phase_anchor_dir / "data" / "field_phase_convention_apex_fits.csv"
    identifiability_csv = identifiability_dir / "data" / "event_identifiability_summary.csv"

    event_rows = build_event_rows(
        read_csv_rows(phase_pick_csv),
        read_csv_rows(phase_fit_csv),
        read_csv_rows(identifiability_csv),
        args.phase_convention,
        profile_stems,
    )
    if not event_rows:
        raise ValueError(f"no event rows for phase_convention={args.phase_convention!r}")
    profile_rows = summarize_profiles(event_rows)
    pair_rows, spacing_rows, repeatability_summary = pair_profiles(event_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    event_csv = data_dir / "short_profile_event_table.csv"
    profile_csv = data_dir / "short_profile_summary.csv"
    pair_csv = data_dir / "short_profile_pair_repeatability.csv"
    spacing_csv = data_dir / "short_profile_spacing_repeatability.csv"
    write_csv(event_csv, [json_safe(row) for row in event_rows])
    write_csv(profile_csv, [json_safe(row) for row in profile_rows])
    write_csv(pair_csv, [json_safe(row) for row in pair_rows])
    write_csv(spacing_csv, [json_safe(row) for row in spacing_rows])

    repeatability_plot = Path(plot_repeatability(
        pair_rows,
        spacing_rows,
        repeatability_summary,
        figures_dir / "short_profile_repeatability.png",
    ))
    validation_rows = [figure_stats(repeatability_plot)]
    validation_csv = data_dir / "figure_validation.csv"
    write_csv(validation_csv, validation_rows)

    summary = {
        "phase_convention": args.phase_convention,
        "profile_stems": sorted(profile_stems),
        "event_count": len(event_rows),
        "profile_summary": profile_rows,
        "repeatability_summary": repeatability_summary,
        "paths": {
            "event_csv": str(event_csv),
            "profile_csv": str(profile_csv),
            "pair_csv": str(pair_csv),
            "spacing_csv": str(spacing_csv),
            "summary_json": str(data_dir / "short_profile_repeatability_policy_summary.json"),
            "repeatability_plot": str(repeatability_plot),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json = data_dir / "short_profile_repeatability_policy_summary.json"
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_profile_repeatability_policy",
        {
            "summary_json": str(summary_json),
            "phase_pick_csv": str(phase_pick_csv),
            "phase_fit_csv": str(phase_fit_csv),
            "identifiability_csv": str(identifiability_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
