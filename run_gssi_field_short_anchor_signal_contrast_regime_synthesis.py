#!/usr/bin/env python3
"""Summarize field short-anchor signal-contrast regimes from sensitivity rows."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_SENSITIVITY_RUN = "132_gssi51600s_field_short_anchor_signal_contrast_sensitivity"


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def group_rows(rows: list[dict], key: str) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key, ""))].append(row)
    return dict(grouped)


def summarize_group(group_key: str, rows: list[dict], group_label: str) -> dict:
    supported = [row for row in rows if boolish(row.get("all_side_windows_supported"))]
    min_rms = min((safe_float(row.get("min_event_to_noise_rms"), math.inf) for row in rows), default=math.nan)
    min_peak = min((safe_float(row.get("min_peak_to_noise_p95"), math.inf) for row in rows), default=math.nan)
    worst = min(rows, key=lambda row: safe_float(row.get("min_event_to_noise_rms"), math.inf)) if rows else {}
    return {
        "group_label": group_label,
        "group_key": group_key,
        "combo_count": len(rows),
        "all_supported_combo_count": len(supported),
        "all_supported_fraction": len(supported) / len(rows) if rows else 0.0,
        "all_combos_supported": len(rows) > 0 and len(supported) == len(rows),
        "min_event_to_noise_rms": min_rms,
        "min_peak_to_noise_p95": min_peak,
        "worst_combo_key": worst.get("combo_key", ""),
        "ready_for_regime_claim": len(rows) > 0 and len(supported) == len(rows),
    }


def build_regime_rows(combo_rows: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    event_rows = [
        summarize_group(label, rows, "event_window")
        for label, rows in sorted(group_rows(combo_rows, "event_window_label").items())
    ]
    aperture_rows = [
        summarize_group(f"{safe_float(label) * 1000.0:g}mm", rows, "aperture")
        for label, rows in sorted(group_rows(combo_rows, "aperture_half_width_m").items(), key=lambda item: safe_float(item[0]))
    ]
    noise_rows = [
        summarize_group(label, rows, "noise_window")
        for label, rows in sorted(group_rows(combo_rows, "noise_window_label").items())
    ]
    return event_rows, aperture_rows, noise_rows


def summarize_regimes(combo_rows: list[dict], sensitivity_summary: dict, event_rows: list[dict]) -> dict:
    supported_rows = [row for row in combo_rows if boolish(row.get("all_side_windows_supported"))]
    broad = next((row for row in event_rows if row["group_key"] == "broad"), {})
    default_event = next((row for row in event_rows if row["group_key"] == "default"), {})
    tight = next((row for row in event_rows if row["group_key"] == "tight"), {})
    return {
        "policy_label": "gssi51600s_field_short_anchor_signal_contrast_regime_synthesis_qc_only",
        "source_sensitivity_policy_label": sensitivity_summary.get("policy_label", ""),
        "sensitivity_combo_count": len(combo_rows),
        "all_supported_combo_count": len(supported_rows),
        "all_supported_combo_fraction": len(supported_rows) / len(combo_rows) if combo_rows else 0.0,
        "broad_event_all_supported": bool(broad.get("all_combos_supported", False)),
        "broad_event_combo_count": int(broad.get("combo_count", 0)),
        "broad_event_min_event_to_noise_rms": safe_float(broad.get("min_event_to_noise_rms"), math.nan),
        "broad_event_min_peak_to_noise_p95": safe_float(broad.get("min_peak_to_noise_p95"), math.nan),
        "default_event_all_supported_fraction": safe_float(default_event.get("all_supported_fraction"), 0.0),
        "tight_event_all_supported_fraction": safe_float(tight.get("all_supported_fraction"), 0.0),
        "ready_for_broad_event_signal_contrast_regime": bool(broad.get("all_combos_supported", False)),
        "ready_for_default_signal_contrast_qc": bool(sensitivity_summary.get("ready_for_default_signal_contrast_qc", False)),
        "ready_for_strict_window_invariant_signal_contrast_claim": False,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "The broad event window is robust across the tested aperture/noise "
            "settings, but the full tight/default/broad sweep is not window "
            "invariant. Treat this as a broad-window field morphology contrast "
            "regime only; do not promote it to amplitude calibration, field FWI, "
            "or 3D/HPC."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "broad_event_signal_contrast_regime",
            "ready": summary["ready_for_broad_event_signal_contrast_regime"],
            "allowed_use": "broad-event-window short-anchor signal-contrast morphology QC",
            "blocked_use": "absolute amplitude calibration",
            "evidence": (
                f"broad event combos={summary['broad_event_combo_count']}; "
                f"min rms={summary['broad_event_min_event_to_noise_rms']:.3f}"
            ),
        },
        {
            "gate_key": "strict_window_invariant_signal_contrast_claim",
            "ready": summary["ready_for_strict_window_invariant_signal_contrast_claim"],
            "allowed_use": "none",
            "blocked_use": "claim contrast is invariant across tight/default/broad event windows",
            "evidence": (
                f"all-supported combos={summary['all_supported_combo_count']}/"
                f"{summary['sensitivity_combo_count']}"
            ),
        },
        {
            "gate_key": "absolute_amplitude_calibration",
            "ready": summary["ready_for_absolute_amplitude_calibration"],
            "allowed_use": "none",
            "blocked_use": "amplitude-calibrated inversion",
            "evidence": "contrast is local relative morphology QC only",
        },
        {
            "gate_key": "field_fwi_or_3d_hpc",
            "ready": summary["ready_for_field_fwi"] or summary["ready_for_3d_hpc"],
            "allowed_use": "none",
            "blocked_use": "field FWI / 3D HPC",
            "evidence": "no geometry/radius/depth/absolute-amplitude calibration",
        },
    ]


def plot_regimes(event_rows: list[dict], aperture_rows: list[dict], noise_rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.7), constrained_layout=True)
    panels = [
        ("Event Window", event_rows),
        ("Aperture", aperture_rows),
        ("Pre-Event Baseline", noise_rows),
    ]
    for ax, (title, rows) in zip(axes, panels):
        labels = [row["group_key"] for row in rows]
        fractions = [safe_float(row.get("all_supported_fraction"), 0.0) for row in rows]
        colors = ["#2f9d55" if row.get("all_combos_supported") else "#d8a03d" for row in rows]
        ax.bar(labels, fractions, color=colors)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("all-supported combo fraction")
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        for idx, row in enumerate(rows):
            ax.text(
                idx,
                min(1.0, fractions[idx] + 0.04),
                f"{row['all_supported_combo_count']}/{row['combo_count']}",
                ha="center",
                va="bottom",
                fontsize=9,
            )
    axes[0].text(
        0.02,
        0.06,
        f"broad min RMS={summary['broad_event_min_event_to_noise_rms']:.2f}x\n"
        f"strict invariant={summary['ready_for_strict_window_invariant_signal_contrast_claim']}\n"
        f"gpu={summary['gpu_priority']}",
        transform=axes[0].transAxes,
        ha="left",
        va="bottom",
        fontsize=8.8,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S Signal-Contrast Regime Synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_signal_contrast_regime_synthesis.png`",
                "",
                "This figure summarizes which signal-contrast sensitivity regimes from",
                "run `132` are robust across all tested combinations.",
                "",
                f"Broad event window all-supported: `{summary['broad_event_all_supported']}`.",
                f"Broad event minimum RMS ratio: `{summary['broad_event_min_event_to_noise_rms']:.3f}`.",
                f"Strict window-invariant contrast ready: `{summary['ready_for_strict_window_invariant_signal_contrast_claim']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Scope boundary:",
                "",
                "This is field morphology QC only. It does not provide absolute",
                "amplitude calibration, cover-depth/radius recovery, field FWI, or",
                "3D/HPC readiness.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--sensitivity-run", default=DEFAULT_SENSITIVITY_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_signal_contrast_regime_synthesis")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    dataset_root = Path(field_dataset_output_root(args.field_root, args.dataset_id))
    sensitivity_dir = dataset_root / args.sensitivity_run
    combo_csv = sensitivity_dir / "data/field_short_anchor_signal_contrast_sensitivity_combos.csv"
    sensitivity_json = sensitivity_dir / "data/field_short_anchor_signal_contrast_sensitivity_summary.json"
    combo_rows = read_csv_rows(combo_csv)
    sensitivity_summary = read_json(sensitivity_json)
    event_rows, aperture_rows, noise_rows = build_regime_rows(combo_rows)
    summary = summarize_regimes(combo_rows, sensitivity_summary, event_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    event_csv = data_dir / "field_short_anchor_signal_contrast_regime_event_rows.csv"
    aperture_csv = data_dir / "field_short_anchor_signal_contrast_regime_aperture_rows.csv"
    noise_csv = data_dir / "field_short_anchor_signal_contrast_regime_noise_rows.csv"
    gates_csv = data_dir / "field_short_anchor_signal_contrast_regime_gates.csv"
    summary_json = data_dir / "field_short_anchor_signal_contrast_regime_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_signal_contrast_regime_synthesis.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    plot_regimes(event_rows, aperture_rows, noise_rows, summary, figure_path)
    write_csv(event_csv, [json_safe(row) for row in event_rows])
    write_csv(aperture_csv, [json_safe(row) for row in aperture_rows])
    write_csv(noise_csv, [json_safe(row) for row in noise_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "event_rows_csv": str(event_csv),
        "aperture_rows_csv": str(aperture_csv),
        "noise_rows_csv": str(noise_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
        "source_combo_csv": str(combo_csv),
        "source_sensitivity_summary_json": str(sensitivity_json),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary)
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_signal_contrast_regime_synthesis",
        {
            "dataset_id": args.dataset_id,
            "sensitivity_run": args.sensitivity_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
