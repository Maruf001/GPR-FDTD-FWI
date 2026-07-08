#!/usr/bin/env python3
"""Audit short-anchor event signal contrast without promoting field inversion."""

from __future__ import annotations

import argparse
import csv
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
from run_gssi_dzt_qc import (  # noqa: E402
    DEFAULT_DATASET_ID,
    DEFAULT_FIELD_ROOT,
    DEFAULT_INPUT_DIR,
    field_dataset_output_root,
    read_dzt_profiles,
    readgssi_version,
)
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import build_axes, json_safe, preprocess_profile, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_ALIGNMENT_RUN = "039_gssi51600s_content_anchor_trace_alignment"
DEFAULT_SIGNED_MORPHOLOGY_RUN = "126_gssi51600s_field_short_anchor_signed_morphology_audit"
DEFAULT_TIMING_MARGIN_RUN = "129_gssi51600s_field_short_anchor_signed_morphology_timing_margin"
DEFAULT_APERTURE_HALF_WIDTH_M = 0.020
DEFAULT_EVENT_PRE_NS = 0.08
DEFAULT_EVENT_POST_NS = 0.18
DEFAULT_NOISE_PRE_START_NS = 0.50
DEFAULT_NOISE_PRE_END_NS = 0.20
DEFAULT_MIN_EVENT_TO_NOISE_RMS = 3.0
DEFAULT_MIN_PEAK_TO_NOISE_P95 = 8.0


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _rms(values: np.ndarray) -> float:
    arr = np.asarray(values, dtype=np.float64)
    return float(np.sqrt(np.nanmean(arr**2))) if arr.size else math.nan


def _safe_db(ratio: float) -> float:
    return 20.0 * math.log10(ratio) if ratio > 0.0 and math.isfinite(ratio) else math.nan


def window_contrast_metrics(
    corrected: np.ndarray,
    x_m: np.ndarray,
    time_ns: np.ndarray,
    *,
    center_x_m: float,
    event_time_ns: float,
    aperture_half_width_m: float = DEFAULT_APERTURE_HALF_WIDTH_M,
    event_pre_ns: float = DEFAULT_EVENT_PRE_NS,
    event_post_ns: float = DEFAULT_EVENT_POST_NS,
    noise_pre_start_ns: float = DEFAULT_NOISE_PRE_START_NS,
    noise_pre_end_ns: float = DEFAULT_NOISE_PRE_END_NS,
) -> dict:
    arr = np.asarray(corrected, dtype=np.float64)
    x_axis = np.asarray(x_m, dtype=np.float64)
    t_axis = np.asarray(time_ns, dtype=np.float64)
    x_mask = np.abs(x_axis - float(center_x_m)) <= float(aperture_half_width_m)
    event_mask = (
        (t_axis >= float(event_time_ns) - float(event_pre_ns))
        & (t_axis <= float(event_time_ns) + float(event_post_ns))
    )
    noise_start = max(0.0, float(event_time_ns) - float(noise_pre_start_ns))
    noise_end = max(0.0, float(event_time_ns) - float(noise_pre_end_ns))
    noise_mask = (t_axis >= noise_start) & (t_axis <= noise_end)
    if not np.any(x_mask) or not np.any(event_mask) or not np.any(noise_mask):
        return {
            "valid_window": False,
            "event_sample_count": int(np.count_nonzero(event_mask) * np.count_nonzero(x_mask)),
            "noise_sample_count": int(np.count_nonzero(noise_mask) * np.count_nonzero(x_mask)),
            "event_rms": math.nan,
            "noise_rms": math.nan,
            "event_to_noise_rms": math.nan,
            "event_to_noise_rms_db": math.nan,
            "event_peak_abs": math.nan,
            "noise_abs_p95": math.nan,
            "peak_to_noise_p95": math.nan,
        }
    event_window = arr[np.ix_(event_mask, x_mask)]
    noise_window = arr[np.ix_(noise_mask, x_mask)]
    event_rms = _rms(event_window)
    noise_rms = max(_rms(noise_window), 1.0e-12)
    event_peak = float(np.nanmax(np.abs(event_window))) if event_window.size else math.nan
    noise_p95 = float(np.nanpercentile(np.abs(noise_window), 95.0)) if noise_window.size else math.nan
    peak_ratio = event_peak / max(noise_p95, 1.0e-12)
    rms_ratio = event_rms / noise_rms
    return {
        "valid_window": True,
        "event_sample_count": int(event_window.size),
        "noise_sample_count": int(noise_window.size),
        "event_rms": event_rms,
        "noise_rms": noise_rms,
        "event_to_noise_rms": rms_ratio,
        "event_to_noise_rms_db": _safe_db(rms_ratio),
        "event_peak_abs": event_peak,
        "noise_abs_p95": noise_p95,
        "peak_to_noise_p95": peak_ratio,
    }


def load_processed_profiles(input_dir: Path, file_names: set[str]) -> tuple[dict[str, dict], dict[str, tuple[np.ndarray, np.ndarray]]]:
    processed_by_file: dict[str, dict] = {}
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for record, raw in read_dzt_profiles(input_dir):
        if record.get("file") not in file_names:
            continue
        processed_by_file[record["file"]] = preprocess_profile(raw)
        axes_by_file[record["file"]] = build_axes(record)
    return processed_by_file, axes_by_file


def contrast_specs_from_alignment(row: dict) -> list[dict]:
    corrected_time = (
        safe_float(row.get("reference_phase_time_ns"))
        + safe_float(row.get("corrected_comparison_minus_reference_phase_time_ns"))
    )
    return [
        {
            "side": "reference",
            "file": row.get("reference_file", ""),
            "apex_group": row.get("reference_apex_group", ""),
            "x_m": safe_float(row.get("reference_x_m")),
            "event_time_ns": safe_float(row.get("reference_phase_time_ns")),
        },
        {
            "side": "comparison_aligned",
            "file": row.get("comparison_file", ""),
            "apex_group": row.get("comparison_apex_group", ""),
            "x_m": safe_float(row.get("comparison_aligned_x_m")),
            "event_time_ns": corrected_time,
        },
    ]


def build_signal_contrast_rows(
    alignment_rows: list[dict],
    processed_by_file: dict[str, dict],
    axes_by_file: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    aperture_half_width_m: float = DEFAULT_APERTURE_HALF_WIDTH_M,
    event_pre_ns: float = DEFAULT_EVENT_PRE_NS,
    event_post_ns: float = DEFAULT_EVENT_POST_NS,
    noise_pre_start_ns: float = DEFAULT_NOISE_PRE_START_NS,
    noise_pre_end_ns: float = DEFAULT_NOISE_PRE_END_NS,
    min_event_to_noise_rms: float = DEFAULT_MIN_EVENT_TO_NOISE_RMS,
    min_peak_to_noise_p95: float = DEFAULT_MIN_PEAK_TO_NOISE_P95,
) -> list[dict]:
    outputs: list[dict] = []
    for row in alignment_rows:
        if not boolish(row.get("anchor_content_backed")):
            continue
        pair_index = int(safe_float(row.get("pair_index"), -1))
        for spec in contrast_specs_from_alignment(row):
            file_name = spec["file"]
            if file_name not in processed_by_file:
                continue
            x_axis, t_axis = axes_by_file[file_name]
            metrics = window_contrast_metrics(
                processed_by_file[file_name]["corrected"],
                x_axis,
                t_axis,
                center_x_m=spec["x_m"],
                event_time_ns=spec["event_time_ns"],
                aperture_half_width_m=aperture_half_width_m,
                event_pre_ns=event_pre_ns,
                event_post_ns=event_post_ns,
                noise_pre_start_ns=noise_pre_start_ns,
                noise_pre_end_ns=noise_pre_end_ns,
            )
            supported = (
                boolish(metrics["valid_window"])
                and safe_float(metrics["event_to_noise_rms"]) >= min_event_to_noise_rms
                and safe_float(metrics["peak_to_noise_p95"]) >= min_peak_to_noise_p95
            )
            outputs.append(
                {
                    "pair_index": pair_index,
                    "side": spec["side"],
                    "file": file_name,
                    "apex_group": spec["apex_group"],
                    "x_m": spec["x_m"],
                    "event_time_ns": spec["event_time_ns"],
                    "aperture_half_width_m": aperture_half_width_m,
                    "event_window_start_ns": spec["event_time_ns"] - event_pre_ns,
                    "event_window_end_ns": spec["event_time_ns"] + event_post_ns,
                    "noise_window_start_ns": max(0.0, spec["event_time_ns"] - noise_pre_start_ns),
                    "noise_window_end_ns": max(0.0, spec["event_time_ns"] - noise_pre_end_ns),
                    **metrics,
                    "signal_contrast_supported": supported,
                    "ready_for_morphology_qc": supported,
                    "ready_for_absolute_amplitude_calibration": False,
                    "ready_for_field_fwi": False,
                    "allowed_use": "short-anchor field event signal-contrast QC",
                    "blocked_use": "absolute amplitude calibration, radius/geometry/cover-depth recovery, field FWI, 3D/HPC",
                }
            )
    return sorted(outputs, key=lambda item: (item["pair_index"], item["side"]))


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def summarize_signal_contrast(
    rows: list[dict],
    alignment_summary: dict,
    signed_summary: dict,
    timing_summary: dict,
) -> dict:
    supported = [row for row in rows if boolish(row.get("signal_contrast_supported"))]
    rms_ratios = _finite([safe_float(row.get("event_to_noise_rms")) for row in rows])
    rms_db = _finite([safe_float(row.get("event_to_noise_rms_db")) for row in rows])
    peak_ratios = _finite([safe_float(row.get("peak_to_noise_p95")) for row in rows])
    event_rms = _finite([safe_float(row.get("event_rms")) for row in rows])
    noise_rms = _finite([safe_float(row.get("noise_rms")) for row in rows])
    signal_ready = len(rows) > 0 and len(supported) == len(rows)
    return {
        "policy_label": "gssi51600s_field_short_anchor_signal_contrast_qc_only",
        "source_alignment_policy_label": alignment_summary.get("policy_label", ""),
        "source_signed_morphology_policy_label": signed_summary.get("policy_label", ""),
        "source_timing_margin_policy_label": timing_summary.get("policy_label", ""),
        "content_pair_count": len({row.get("pair_index") for row in rows}),
        "side_window_count": len(rows),
        "signal_contrast_supported_count": len(supported),
        "min_event_to_noise_rms": min(rms_ratios) if rms_ratios else math.nan,
        "mean_event_to_noise_rms": float(np.mean(rms_ratios)) if rms_ratios else math.nan,
        "min_event_to_noise_rms_db": min(rms_db) if rms_db else math.nan,
        "min_peak_to_noise_p95": min(peak_ratios) if peak_ratios else math.nan,
        "mean_event_rms": float(np.mean(event_rms)) if event_rms else math.nan,
        "mean_noise_rms": float(np.mean(noise_rms)) if noise_rms else math.nan,
        "ready_for_signal_contrast_qc": signal_ready,
        "ready_for_signed_morphology_qc": boolish(
            signed_summary.get("ready_for_signed_waveform_morphology_qc", False)
        ),
        "ready_for_timing_margin_qc": boolish(
            timing_summary.get("ready_for_content_only_morphology_timing_qc", False)
        ),
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_radius_or_geometry_seed": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "The content-backed short-anchor event windows have enough local "
            "pre-event signal contrast to support morphology QC. The calculation "
            "uses background-removed DZT amplitudes and local pre-event baselines, "
            "not calibrated antenna/system amplitudes, so amplitude calibration, "
            "radius/geometry/depth recovery, field FWI, 3D/HPC, and heavy field "
            "work remain blocked."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "signal_contrast_qc",
            "ready": summary["ready_for_signal_contrast_qc"],
            "allowed_use": "short-anchor event signal-contrast QC",
            "blocked_use": "absolute amplitude calibration",
            "evidence": (
                f"supported windows={summary['signal_contrast_supported_count']}/"
                f"{summary['side_window_count']}; min rms ratio={summary['min_event_to_noise_rms']:.3f}"
            ),
        },
        {
            "gate_key": "signed_morphology_qc",
            "ready": summary["ready_for_signed_morphology_qc"],
            "allowed_use": "field supplement signed morphology QC",
            "blocked_use": "geometry/radius seed",
            "evidence": "inherits run 126 signed morphology boundary",
        },
        {
            "gate_key": "absolute_amplitude_calibration",
            "ready": summary["ready_for_absolute_amplitude_calibration"],
            "allowed_use": "none",
            "blocked_use": "amplitude-calibrated field inversion or material inference",
            "evidence": "contrast uses local pre-event baseline after background removal",
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI / 3D HPC",
            "evidence": "no geometry/radius/depth/absolute-amplitude calibration",
        },
    ]


def plot_signal_contrast(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"p{row['pair_index']}\n{row['side'].replace('_', ' ')}" for row in rows]
    rms_db = [safe_float(row.get("event_to_noise_rms_db")) for row in rows]
    peak_ratio = [safe_float(row.get("peak_to_noise_p95")) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x - 0.18, rms_db, width=0.36, color="#4e79a7", label="RMS ratio dB")
    axes[0].axhline(_safe_db(DEFAULT_MIN_EVENT_TO_NOISE_RMS), color="#222222", linestyle=":", linewidth=1.0)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("event/pre-event RMS [dB]")
    axes[0].set_title("Short-anchor event contrast")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, peak_ratio, width=0.5, color="#59a14f")
    axes[1].axhline(DEFAULT_MIN_PEAK_TO_NOISE_P95, color="#222222", linestyle=":", linewidth=1.0)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("event peak / pre-event p95")
    axes[1].set_title("Peak contrast")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.04,
        0.94,
        f"supported: {summary['signal_contrast_supported_count']}/{summary['side_window_count']}\n"
        f"min RMS ratio: {summary['min_event_to_noise_rms']:.2f}x\n"
        f"min peak ratio: {summary['min_peak_to_noise_p95']:.2f}x\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[1].transAxes,
        ha="left",
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short-anchor signal-contrast audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_signal_contrast_audit.png`",
                "",
                "This CPU-only figure checks whether the content-backed short-anchor",
                "event windows rise above local pre-event baseline energy.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Supported signal-contrast windows: `{summary['signal_contrast_supported_count']}` / `{summary['side_window_count']}`.",
                f"Minimum event/noise RMS ratio: `{summary['min_event_to_noise_rms']}`.",
                f"Minimum event/noise RMS dB: `{summary['min_event_to_noise_rms_db']}`.",
                f"Minimum peak/pre-event-p95 ratio: `{summary['min_peak_to_noise_p95']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This is local signal-contrast QC after background removal. It is not",
                "absolute amplitude calibration, radius/geometry/depth recovery, field",
                "FWI, 3D/HPC, or neural-network evidence.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--alignment-run", default=DEFAULT_ALIGNMENT_RUN)
    parser.add_argument("--signed-morphology-run", default=DEFAULT_SIGNED_MORPHOLOGY_RUN)
    parser.add_argument("--timing-margin-run", default=DEFAULT_TIMING_MARGIN_RUN)
    parser.add_argument("--aperture-half-width-m", type=float, default=DEFAULT_APERTURE_HALF_WIDTH_M)
    parser.add_argument("--event-pre-ns", type=float, default=DEFAULT_EVENT_PRE_NS)
    parser.add_argument("--event-post-ns", type=float, default=DEFAULT_EVENT_POST_NS)
    parser.add_argument("--noise-pre-start-ns", type=float, default=DEFAULT_NOISE_PRE_START_NS)
    parser.add_argument("--noise-pre-end-ns", type=float, default=DEFAULT_NOISE_PRE_END_NS)
    parser.add_argument("--min-event-to-noise-rms", type=float, default=DEFAULT_MIN_EVENT_TO_NOISE_RMS)
    parser.add_argument("--min-peak-to-noise-p95", type=float, default=DEFAULT_MIN_PEAK_TO_NOISE_P95)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_signal_contrast_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    alignment_dir = dataset_root / args.alignment_run
    signed_dir = dataset_root / args.signed_morphology_run
    timing_dir = dataset_root / args.timing_margin_run

    alignment_rows = read_csv_rows(alignment_dir / "data/content_anchor_trace_alignment_rows.csv")
    alignment_summary = read_json(alignment_dir / "data/content_anchor_trace_alignment_summary.json")
    signed_summary = read_json(signed_dir / "data/field_short_anchor_signed_morphology_summary.json")
    timing_summary = read_json(timing_dir / "data/field_short_anchor_signed_morphology_timing_margin_summary.json")

    file_names = {
        row.get("reference_file", "")
        for row in alignment_rows
        if boolish(row.get("anchor_content_backed"))
    } | {
        row.get("comparison_file", "")
        for row in alignment_rows
        if boolish(row.get("anchor_content_backed"))
    }
    processed_by_file, axes_by_file = load_processed_profiles(Path(args.input_dir), file_names)
    rows = build_signal_contrast_rows(
        alignment_rows,
        processed_by_file,
        axes_by_file,
        aperture_half_width_m=args.aperture_half_width_m,
        event_pre_ns=args.event_pre_ns,
        event_post_ns=args.event_post_ns,
        noise_pre_start_ns=args.noise_pre_start_ns,
        noise_pre_end_ns=args.noise_pre_end_ns,
        min_event_to_noise_rms=args.min_event_to_noise_rms,
        min_peak_to_noise_p95=args.min_peak_to_noise_p95,
    )
    summary = summarize_signal_contrast(rows, alignment_summary, signed_summary, timing_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_short_anchor_signal_contrast_rows.csv"
    gates_csv = data_dir / "field_short_anchor_signal_contrast_gates.csv"
    summary_json = data_dir / "field_short_anchor_signal_contrast_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_signal_contrast_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_signal_contrast(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "readgssi_version": readgssi_version(),
        "parameters": {
            "aperture_half_width_m": args.aperture_half_width_m,
            "event_pre_ns": args.event_pre_ns,
            "event_post_ns": args.event_post_ns,
            "noise_pre_start_ns": args.noise_pre_start_ns,
            "noise_pre_end_ns": args.noise_pre_end_ns,
            "min_event_to_noise_rms": args.min_event_to_noise_rms,
            "min_peak_to_noise_p95": args.min_peak_to_noise_p95,
        },
        "paths": {
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_alignment_summary_json": str(alignment_dir / "data/content_anchor_trace_alignment_summary.json"),
            "source_signed_morphology_summary_json": str(
                signed_dir / "data/field_short_anchor_signed_morphology_summary.json"
            ),
            "source_timing_margin_summary_json": str(
                timing_dir / "data/field_short_anchor_signed_morphology_timing_margin_summary.json"
            ),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_signal_contrast_audit",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
