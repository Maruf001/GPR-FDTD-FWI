#!/usr/bin/env python3
"""Sweep short-anchor signal-contrast windows without promoting field inversion."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_gssi_field_short_anchor_signal_contrast_audit import (  # noqa: E402
    DEFAULT_ALIGNMENT_RUN,
    DEFAULT_MIN_EVENT_TO_NOISE_RMS,
    DEFAULT_MIN_PEAK_TO_NOISE_P95,
    build_signal_contrast_rows,
    load_processed_profiles,
    read_csv_rows,
)
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SIGNAL_CONTRAST_RUN = "131_gssi51600s_field_short_anchor_signal_contrast_audit"
DEFAULT_APERTURE_SWEEP_M = "0.010,0.020,0.030"
DEFAULT_EVENT_WINDOWS = "tight:0.05:0.12,default:0.08:0.18,broad:0.10:0.25"
DEFAULT_NOISE_WINDOWS = "near:0.35:0.12,default:0.50:0.20,far:0.65:0.35"


def parse_float_list(value: str) -> list[float]:
    out = []
    for item in str(value or "").split(","):
        item = item.strip()
        if item:
            out.append(float(item))
    if not out:
        raise ValueError("expected at least one float")
    return out


def parse_window_specs(value: str) -> list[dict]:
    specs = []
    for item in str(value or "").split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":")
        if len(parts) != 3:
            raise ValueError(f"expected label:start:end window spec, got {item!r}")
        specs.append({"label": parts[0], "start": float(parts[1]), "end": float(parts[2])})
    if not specs:
        raise ValueError("expected at least one window spec")
    return specs


def build_sensitivity_rows(
    alignment_rows: list[dict],
    processed_by_file: dict,
    axes_by_file: dict,
    aperture_values_m: list[float],
    event_windows: list[dict],
    noise_windows: list[dict],
    *,
    min_event_to_noise_rms: float = DEFAULT_MIN_EVENT_TO_NOISE_RMS,
    min_peak_to_noise_p95: float = DEFAULT_MIN_PEAK_TO_NOISE_P95,
) -> tuple[list[dict], list[dict]]:
    combo_rows: list[dict] = []
    window_rows: list[dict] = []
    for aperture in aperture_values_m:
        for event in event_windows:
            for noise in noise_windows:
                detail = build_signal_contrast_rows(
                    alignment_rows,
                    processed_by_file,
                    axes_by_file,
                    aperture_half_width_m=aperture,
                    event_pre_ns=event["start"],
                    event_post_ns=event["end"],
                    noise_pre_start_ns=noise["start"],
                    noise_pre_end_ns=noise["end"],
                    min_event_to_noise_rms=min_event_to_noise_rms,
                    min_peak_to_noise_p95=min_peak_to_noise_p95,
                )
                combo_key = f"a{aperture * 1000.0:g}mm_{event['label']}_{noise['label']}"
                for row in detail:
                    window_rows.append(
                        {
                            "combo_key": combo_key,
                            "aperture_label": f"{aperture * 1000.0:g}mm",
                            "event_window_label": event["label"],
                            "noise_window_label": noise["label"],
                            **row,
                        }
                    )
                rms_values = [safe_float(row.get("event_to_noise_rms")) for row in detail]
                peak_values = [safe_float(row.get("peak_to_noise_p95")) for row in detail]
                supported = [row for row in detail if row["signal_contrast_supported"]]
                combo_rows.append(
                    {
                        "combo_key": combo_key,
                        "aperture_half_width_m": aperture,
                        "event_window_label": event["label"],
                        "event_pre_ns": event["start"],
                        "event_post_ns": event["end"],
                        "noise_window_label": noise["label"],
                        "noise_pre_start_ns": noise["start"],
                        "noise_pre_end_ns": noise["end"],
                        "side_window_count": len(detail),
                        "supported_side_window_count": len(supported),
                        "all_side_windows_supported": len(detail) > 0 and len(supported) == len(detail),
                        "min_event_to_noise_rms": min(rms_values) if rms_values else math.nan,
                        "min_peak_to_noise_p95": min(peak_values) if peak_values else math.nan,
                        "ready_for_signal_contrast_qc": len(detail) > 0 and len(supported) == len(detail),
                    }
                )
    return combo_rows, window_rows


def summarize_sensitivity(combo_rows: list[dict], baseline_summary: dict) -> dict:
    all_supported = [row for row in combo_rows if row["all_side_windows_supported"]]
    default_combo = [
        row
        for row in combo_rows
        if math.isclose(safe_float(row.get("aperture_half_width_m")), 0.020)
        and row.get("event_window_label") == "default"
        and row.get("noise_window_label") == "default"
    ]
    min_rms_row = min(combo_rows, key=lambda row: safe_float(row.get("min_event_to_noise_rms"), math.inf))
    min_peak_row = min(combo_rows, key=lambda row: safe_float(row.get("min_peak_to_noise_p95"), math.inf))
    return {
        "policy_label": "gssi51600s_field_short_anchor_signal_contrast_sensitivity_qc_only",
        "source_signal_contrast_policy_label": baseline_summary.get("policy_label", ""),
        "sensitivity_combo_count": len(combo_rows),
        "all_supported_combo_count": len(all_supported),
        "all_supported_combo_fraction": len(all_supported) / len(combo_rows) if combo_rows else 0.0,
        "default_combo_all_supported": bool(default_combo and default_combo[0]["all_side_windows_supported"]),
        "default_combo_min_event_to_noise_rms": (
            safe_float(default_combo[0].get("min_event_to_noise_rms")) if default_combo else math.nan
        ),
        "default_combo_min_peak_to_noise_p95": (
            safe_float(default_combo[0].get("min_peak_to_noise_p95")) if default_combo else math.nan
        ),
        "worst_rms_combo_key": min_rms_row["combo_key"],
        "worst_rms_supported_side_window_count": min_rms_row["supported_side_window_count"],
        "worst_rms_min_event_to_noise_rms": safe_float(min_rms_row.get("min_event_to_noise_rms")),
        "worst_peak_combo_key": min_peak_row["combo_key"],
        "worst_peak_supported_side_window_count": min_peak_row["supported_side_window_count"],
        "worst_peak_min_peak_to_noise_p95": safe_float(min_peak_row.get("min_peak_to_noise_p95")),
        "ready_for_default_signal_contrast_qc": bool(default_combo and default_combo[0]["all_side_windows_supported"]),
        "ready_for_window_invariant_signal_contrast_claim": len(all_supported) == len(combo_rows) and len(combo_rows) > 0,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "The default signal-contrast gate remains supported, but the result is "
            "not invariant across all tested aperture/event/noise windows. Use it "
            "as a default-window field morphology QC guardrail, not as a strict "
            "window-invariant contrast claim or amplitude-calibrated inversion cue."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "default_signal_contrast_qc",
            "ready": summary["ready_for_default_signal_contrast_qc"],
            "allowed_use": "default-window short-anchor signal-contrast QC",
            "blocked_use": "amplitude calibration",
            "evidence": (
                f"default min rms={summary['default_combo_min_event_to_noise_rms']:.3f}; "
                f"default min peak={summary['default_combo_min_peak_to_noise_p95']:.3f}"
            ),
        },
        {
            "gate_key": "window_invariant_signal_contrast_claim",
            "ready": summary["ready_for_window_invariant_signal_contrast_claim"],
            "allowed_use": "none",
            "blocked_use": "strict window-invariant contrast claim",
            "evidence": (
                f"all-supported combos={summary['all_supported_combo_count']}/"
                f"{summary['sensitivity_combo_count']}"
            ),
        },
        {
            "gate_key": "absolute_amplitude_calibration",
            "ready": summary["ready_for_absolute_amplitude_calibration"],
            "allowed_use": "none",
            "blocked_use": "amplitude-calibrated field inversion",
            "evidence": "sensitivity uses local relative contrast only",
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI / 3D HPC",
            "evidence": "no geometry/radius/depth/absolute-amplitude calibration",
        },
    ]


def plot_sensitivity(combo_rows: list[dict], summary: dict, save_path: Path) -> str:
    apertures = sorted({safe_float(row.get("aperture_half_width_m")) for row in combo_rows})
    event_labels = []
    noise_labels = []
    for row in combo_rows:
        if row["event_window_label"] not in event_labels:
            event_labels.append(row["event_window_label"])
        if row["noise_window_label"] not in noise_labels:
            noise_labels.append(row["noise_window_label"])
    fig, axes = plt.subplots(
        1,
        len(apertures) + 1,
        figsize=(15.2, 4.8),
        constrained_layout=True,
        gridspec_kw={"width_ratios": [1.0] * len(apertures) + [1.2]},
    )
    heatmap_axes = axes[: len(apertures)]
    gate_ax = axes[-1]
    image = None
    for ax, aperture in zip(heatmap_axes, apertures):
        matrix = np.full((len(event_labels), len(noise_labels)), np.nan, dtype=float)
        for row in combo_rows:
            if not math.isclose(safe_float(row.get("aperture_half_width_m")), aperture):
                continue
            row_idx = event_labels.index(row["event_window_label"])
            col_idx = noise_labels.index(row["noise_window_label"])
            matrix[row_idx, col_idx] = safe_float(row.get("supported_side_window_count"))
        image = ax.imshow(matrix, vmin=0, vmax=4, cmap="RdYlGn", aspect="auto")
        for row_idx, event_label in enumerate(event_labels):
            for col_idx, noise_label in enumerate(noise_labels):
                value = matrix[row_idx, col_idx]
                if math.isfinite(value):
                    ax.text(col_idx, row_idx, f"{int(value)}/4", ha="center", va="center", fontsize=9)
        ax.set_title(f"aperture {aperture * 1000.0:g} mm")
        ax.set_xticks(np.arange(len(noise_labels)), noise_labels)
        ax.set_yticks(np.arange(len(event_labels)), event_labels)
        ax.set_xlabel("pre-event baseline")
        if ax is heatmap_axes[0]:
            ax.set_ylabel("event window")
    if image is not None:
        fig.colorbar(image, ax=list(heatmap_axes), shrink=0.82, label="supported side windows")

    gate_labels = ["default\nQC", "window\ninvariant", "amplitude\ncal.", "field\nFWI"]
    gate_values = [
        summary["ready_for_default_signal_contrast_qc"],
        summary["ready_for_window_invariant_signal_contrast_claim"],
        summary["ready_for_absolute_amplitude_calibration"],
        summary["ready_for_field_fwi"],
    ]
    gate_ax.bar(
        gate_labels,
        [1 if value else 0 for value in gate_values],
        color=["#59a14f" if value else "#bab0ac" for value in gate_values],
    )
    gate_ax.set_yticks([0, 1], ["blocked", "ready"])
    gate_ax.set_ylim(0, 1.15)
    gate_ax.set_title("Scope gates")
    gate_ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    gate_ax.text(
        0.04,
        0.08,
        f"all-supported: {summary['all_supported_combo_count']}/{summary['sensitivity_combo_count']}\n"
        f"worst RMS combo: {summary['worst_rms_combo_key']}\n"
        f"worst min RMS: {summary['worst_rms_min_event_to_noise_rms']:.2f}x\n"
        f"gpu={summary['gpu_priority']}",
        transform=gate_ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short-anchor signal-contrast sensitivity", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_signal_contrast_sensitivity.png`",
                "",
                "This CPU-only figure sweeps local aperture, event window, and pre-event",
                "baseline choices for the short-anchor signal-contrast gate.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"All-supported combinations: `{summary['all_supported_combo_count']}` / `{summary['sensitivity_combo_count']}`.",
                f"Default combination supported: `{summary['default_combo_all_supported']}`.",
                f"Worst RMS combination: `{summary['worst_rms_combo_key']}`.",
                f"Worst minimum RMS ratio: `{summary['worst_rms_min_event_to_noise_rms']}`.",
                f"Window-invariant contrast claim ready: `{summary['ready_for_window_invariant_signal_contrast_claim']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This is a sensitivity guardrail for field morphology QC. It is not",
                "absolute amplitude calibration, radius/geometry/depth recovery,",
                "field FWI, 3D/HPC, or neural-network evidence.",
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
    parser.add_argument("--signal-contrast-run", default=DEFAULT_SIGNAL_CONTRAST_RUN)
    parser.add_argument("--aperture-sweep-m", default=DEFAULT_APERTURE_SWEEP_M)
    parser.add_argument("--event-windows", default=DEFAULT_EVENT_WINDOWS)
    parser.add_argument("--noise-windows", default=DEFAULT_NOISE_WINDOWS)
    parser.add_argument("--min-event-to-noise-rms", type=float, default=DEFAULT_MIN_EVENT_TO_NOISE_RMS)
    parser.add_argument("--min-peak-to-noise-p95", type=float, default=DEFAULT_MIN_PEAK_TO_NOISE_P95)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_signal_contrast_sensitivity")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    alignment_dir = dataset_root / args.alignment_run
    baseline_dir = dataset_root / args.signal_contrast_run
    alignment_rows = read_csv_rows(alignment_dir / "data/content_anchor_trace_alignment_rows.csv")
    baseline_summary = read_json(baseline_dir / "data/field_short_anchor_signal_contrast_summary.json")
    file_names = {
        row.get("reference_file", "")
        for row in alignment_rows
        if str(row.get("anchor_content_backed", "")).lower() == "true"
    } | {
        row.get("comparison_file", "")
        for row in alignment_rows
        if str(row.get("anchor_content_backed", "")).lower() == "true"
    }
    processed_by_file, axes_by_file = load_processed_profiles(Path(args.input_dir), file_names)
    combo_rows, window_rows = build_sensitivity_rows(
        alignment_rows,
        processed_by_file,
        axes_by_file,
        parse_float_list(args.aperture_sweep_m),
        parse_window_specs(args.event_windows),
        parse_window_specs(args.noise_windows),
        min_event_to_noise_rms=args.min_event_to_noise_rms,
        min_peak_to_noise_p95=args.min_peak_to_noise_p95,
    )
    summary = summarize_sensitivity(combo_rows, baseline_summary)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    combo_csv = data_dir / "field_short_anchor_signal_contrast_sensitivity_combos.csv"
    windows_csv = data_dir / "field_short_anchor_signal_contrast_sensitivity_windows.csv"
    gates_csv = data_dir / "field_short_anchor_signal_contrast_sensitivity_gates.csv"
    summary_json = data_dir / "field_short_anchor_signal_contrast_sensitivity_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_signal_contrast_sensitivity.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(combo_csv, [json_safe(row) for row in combo_rows])
    write_csv(windows_csv, [json_safe(row) for row in window_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_sensitivity(combo_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    output_summary = {
        **summary,
        "paths": {
            "combo_rows_csv": str(combo_csv),
            "window_rows_csv": str(windows_csv),
            "gates_csv": str(gates_csv),
            "summary_json": str(summary_json),
            "source_signal_contrast_summary_json": str(
                baseline_dir / "data/field_short_anchor_signal_contrast_summary.json"
            ),
            "source_alignment_rows_csv": str(alignment_dir / "data/content_anchor_trace_alignment_rows.csv"),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_signal_contrast_sensitivity",
        {
            "summary_json": str(summary_json),
            "combo_rows_csv": str(combo_csv),
            "window_rows_csv": str(windows_csv),
            "gates_csv": str(gates_csv),
            "figure_validation_csv": str(validation_csv),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
