#!/usr/bin/env python3
"""Audit short-anchor waveform coherence without promoting field inversion claims."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_PANEL_RUN = "035_gssi51600s_content_backed_waveform_panels"
DEFAULT_ALIGNMENT_RUN = "039_gssi51600s_content_anchor_trace_alignment"
DEFAULT_LEAVE_ONE_RUN = "120_gssi51600s_field_short_anchor_leave_one_audit"
DEFAULT_SPATIAL_CONSISTENCY_RUN = "122_gssi51600s_field_short_anchor_spatial_consistency_audit"
DEFAULT_INVERSION_READINESS_RUN = "123_gssi51600s_field_inversion_readiness_synthesis_post_spatial_consistency"
DEFAULT_MIN_CORRECTED_CORRELATION = 0.90
DEFAULT_MIN_EVENT_CORRELATION = 0.95
DEFAULT_MIN_CORRELATION_IMPROVEMENT = 0.30
DEFAULT_MAX_TIMING_RESIDUAL_NS = 0.05
DEFAULT_MIN_PANEL_CORRELATION = 0.80


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def _panel_stats_by_pair(panel_rows: list[dict]) -> dict[int, dict]:
    grouped: dict[int, list[dict]] = {}
    for row in panel_rows:
        pair_index = int(safe_float(row.get("pair_index"), -1))
        if pair_index < 0:
            continue
        grouped.setdefault(pair_index, []).append(row)
    stats = {}
    for pair_index, rows in grouped.items():
        panel_corr = _finite([safe_float(row.get("absolute_correlation")) for row in rows])
        panel_residuals = _finite([safe_float(row.get("normalized_residual_rms")) for row in rows])
        radii = _finite([safe_float(row.get("radius_mm")) for row in rows])
        stats[pair_index] = {
            "panel_count": len(rows),
            "valid_panel_count": sum(parse_bool(row.get("available", True)) for row in rows),
            "panel_min_absolute_correlation": min(panel_corr) if panel_corr else math.nan,
            "panel_mean_absolute_correlation": float(np.mean(panel_corr)) if panel_corr else math.nan,
            "panel_max_normalized_residual_rms": max(panel_residuals) if panel_residuals else math.nan,
            "panel_mean_normalized_residual_rms": float(np.mean(panel_residuals)) if panel_residuals else math.nan,
            "panel_radius_min_mm": min(radii) if radii else math.nan,
            "panel_radius_max_mm": max(radii) if radii else math.nan,
            "panel_radius_span_mm": max(radii) - min(radii) if len(radii) >= 2 else 0.0,
        }
    return stats


def build_waveform_coherence_rows(
    alignment_rows: list[dict],
    panel_rows: list[dict],
    *,
    min_corrected_correlation: float = DEFAULT_MIN_CORRECTED_CORRELATION,
    min_event_correlation: float = DEFAULT_MIN_EVENT_CORRELATION,
    min_correlation_improvement: float = DEFAULT_MIN_CORRELATION_IMPROVEMENT,
    max_timing_residual_ns: float = DEFAULT_MAX_TIMING_RESIDUAL_NS,
    min_panel_correlation: float = DEFAULT_MIN_PANEL_CORRELATION,
) -> list[dict]:
    panel_by_pair = _panel_stats_by_pair(panel_rows)
    outputs = []
    for row in alignment_rows:
        pair_index = int(safe_float(row.get("pair_index"), -1))
        if pair_index < 0 or not parse_bool(row.get("anchor_content_backed", False)):
            continue
        panel = panel_by_pair.get(pair_index, {})
        corrected_corr = safe_float(row.get("corrected_field_trace_abs_correlation"))
        event_corr = safe_float(row.get("event_local_field_trace_abs_correlation"))
        improvement = safe_float(row.get("field_trace_abs_correlation_improvement"))
        corrected_residual_ns = abs(safe_float(row.get("corrected_comparison_minus_reference_phase_time_ns")))
        panel_min_corr = safe_float(panel.get("panel_min_absolute_correlation"))
        radius_match = parse_bool(row.get("radius_match"))
        morphology_supported = (
            corrected_corr >= min_corrected_correlation
            and event_corr >= min_event_correlation
            and improvement >= min_correlation_improvement
            and corrected_residual_ns <= max_timing_residual_ns
            and panel_min_corr >= min_panel_correlation
        )
        outputs.append(
            {
                "pair_index": pair_index,
                "reference_file": row.get("reference_file", ""),
                "comparison_file": row.get("comparison_file", ""),
                "reference_apex_group": row.get("reference_apex_group", ""),
                "comparison_apex_group": row.get("comparison_apex_group", ""),
                "anchor_reference_x_mm": safe_float(row.get("anchor_reference_x_mm")),
                "anchor_comparison_aligned_x_mm": safe_float(row.get("anchor_comparison_aligned_x_mm")),
                "anchor_aligned_x_residual_mm": safe_float(row.get("anchor_aligned_x_residual_mm")),
                "reference_best_radius_mm": safe_float(row.get("reference_best_radius_mm")),
                "comparison_best_radius_mm": safe_float(row.get("comparison_best_radius_mm")),
                "radius_match": radius_match,
                "raw_field_trace_abs_correlation": safe_float(row.get("raw_field_trace_abs_correlation")),
                "corrected_field_trace_abs_correlation": corrected_corr,
                "event_local_field_trace_abs_correlation": event_corr,
                "field_trace_abs_correlation_improvement": improvement,
                "corrected_field_trace_residual_rms": safe_float(row.get("corrected_field_trace_residual_rms")),
                "corrected_abs_timing_residual_ns": corrected_residual_ns,
                "panel_count": int(safe_float(panel.get("panel_count"), 0)),
                "valid_panel_count": int(safe_float(panel.get("valid_panel_count"), 0)),
                "panel_min_absolute_correlation": panel_min_corr,
                "panel_mean_absolute_correlation": safe_float(panel.get("panel_mean_absolute_correlation")),
                "panel_max_normalized_residual_rms": safe_float(panel.get("panel_max_normalized_residual_rms")),
                "panel_radius_span_mm": safe_float(panel.get("panel_radius_span_mm")),
                "morphology_supported": morphology_supported,
                "geometry_seed_ready": False,
                "radius_seed_ready": False,
                "allowed_use": "short-profile relative timing and waveform-morphology QC",
                "blocked_use": "absolute time-zero, geometry/radius/cover-depth recovery, field FWI, 3D/HPC",
            }
        )
    return sorted(outputs, key=lambda row: row["pair_index"])


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "waveform_morphology_qc",
            "ready": summary["ready_for_waveform_morphology_qc"],
            "supported_use": "short-profile waveform-morphology QC",
            "blocked_use": "geometry/radius/cover-depth recovery",
            "evidence": (
                f"coherent pairs={summary['waveform_coherent_pair_count']}/"
                f"{summary['content_pair_count']}; min corrected corr="
                f"{summary['min_corrected_field_trace_abs_correlation']:.3f}"
            ),
        },
        {
            "gate_key": "relative_timing_qc",
            "ready": summary["ready_for_relative_timing_qc"],
            "supported_use": "short-profile relative timing QC",
            "blocked_use": "absolute time-zero",
            "evidence": f"max corrected timing residual={summary['max_corrected_abs_timing_residual_ns']:.6f} ns",
        },
        {
            "gate_key": "geometry_seed",
            "ready": summary["ready_for_geometry_seed"],
            "supported_use": "none",
            "blocked_use": "geometry seed for inversion",
            "evidence": (
                f"radius matches={summary['radius_match_pair_count']}/"
                f"{summary['content_pair_count']}; single spatial translation="
                f"{summary['content_single_translation_supported']}"
            ),
        },
        {
            "gate_key": "radius_recovery",
            "ready": summary["ready_for_radius_recovery"],
            "supported_use": "none",
            "blocked_use": "radius recovery",
            "evidence": f"radius matches={summary['radius_match_pair_count']}/{summary['content_pair_count']}",
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "supported_use": "none",
            "blocked_use": "field FWI",
            "evidence": "field FWI remains blocked by missing geometry, radius, cover-depth, and absolute controls",
        },
    ]


def summarize_waveform_coherence(
    rows: list[dict],
    panel_summary: dict,
    alignment_summary: dict,
    leave_one_summary: dict,
    spatial_summary: dict,
    inversion_summary: dict,
) -> dict:
    corrected = _finite([safe_float(row.get("corrected_field_trace_abs_correlation")) for row in rows])
    event = _finite([safe_float(row.get("event_local_field_trace_abs_correlation")) for row in rows])
    improvements = _finite([safe_float(row.get("field_trace_abs_correlation_improvement")) for row in rows])
    corrected_rms = _finite([safe_float(row.get("corrected_field_trace_residual_rms")) for row in rows])
    timing_residuals = _finite([safe_float(row.get("corrected_abs_timing_residual_ns")) for row in rows])
    panel_min = _finite([safe_float(row.get("panel_min_absolute_correlation")) for row in rows])
    coherent = [row for row in rows if row["morphology_supported"]]
    radius_matches = [row for row in rows if row["radius_match"]]
    waveform_ready = len(rows) > 0 and len(coherent) == len(rows)
    relative_ready = waveform_ready and bool(leave_one_summary.get("ready_for_short_relative_timing_qc", False))
    return {
        "policy_label": "gssi51600s_field_short_anchor_waveform_coherence_qc_only",
        "source_panel_policy_label": panel_summary.get("policy_label", ""),
        "source_alignment_policy_label": alignment_summary.get("policy_label", ""),
        "content_pair_count": len(rows),
        "waveform_coherent_pair_count": len(coherent),
        "waveform_coherent_pair_fraction": len(coherent) / len(rows) if rows else 0.0,
        "min_corrected_field_trace_abs_correlation": min(corrected) if corrected else math.nan,
        "mean_corrected_field_trace_abs_correlation": float(np.mean(corrected)) if corrected else math.nan,
        "min_event_local_field_trace_abs_correlation": min(event) if event else math.nan,
        "min_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "mean_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "max_corrected_field_trace_residual_rms": max(corrected_rms) if corrected_rms else math.nan,
        "max_corrected_abs_timing_residual_ns": max(timing_residuals) if timing_residuals else math.nan,
        "min_panel_absolute_correlation": min(panel_min) if panel_min else math.nan,
        "radius_match_pair_count": len(radius_matches),
        "content_spatial_residual_range_mm": safe_float(spatial_summary.get("content_residual_range_mm"), 0.0),
        "content_single_translation_supported": bool(
            spatial_summary.get("content_single_translation_supported", False)
        ),
        "leave_one_content_anchor_claim_ready": bool(
            leave_one_summary.get("ready_for_leave_one_content_anchor_claim", False)
        ),
        "ready_for_waveform_morphology_qc": waveform_ready,
        "ready_for_relative_timing_qc": relative_ready,
        "ready_for_absolute_time_zero": False,
        "ready_for_geometry_seed": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "source_inversion_ready_for_field_fwi": bool(inversion_summary.get("ready_for_field_fwi", False)),
        "gpu_priority": "none",
        "decision": (
            "The two content-backed short anchors are waveform-coherent after the relative timing correction, "
            "so they support morphology QC. They still do not support geometry, radius, cover-depth, field FWI, "
            "3D/HPC, or absolute time-zero claims because radius choices disagree, spatial residuals do not "
            "support one profile translation, and leave-one-content redundancy is absent."
        ),
    }


def plot_waveform_coherence(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [f"pair {row['pair_index']}" for row in rows]
    x = np.arange(len(rows))
    raw = [safe_float(row.get("raw_field_trace_abs_correlation"), 0.0) for row in rows]
    corrected = [safe_float(row.get("corrected_field_trace_abs_correlation"), 0.0) for row in rows]
    event = [safe_float(row.get("event_local_field_trace_abs_correlation"), 0.0) for row in rows]
    panel = [safe_float(row.get("panel_min_absolute_correlation"), 0.0) for row in rows]
    residual = [safe_float(row.get("corrected_field_trace_residual_rms"), 0.0) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    width = 0.20
    axes[0].bar(x - 1.5 * width, raw, width=width, label="raw field", color="#e15759")
    axes[0].bar(x - 0.5 * width, corrected, width=width, label="corrected field", color="#59a14f")
    axes[0].bar(x + 0.5 * width, event, width=width, label="event-local field", color="#4e79a7")
    axes[0].bar(x + 1.5 * width, panel, width=width, label="panel min", color="#f28e2b")
    axes[0].axhline(DEFAULT_MIN_CORRECTED_CORRELATION, color="#333333", linestyle="--", linewidth=0.8)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.08)
    axes[0].set_ylabel("absolute correlation")
    axes[0].set_title("Short-anchor waveform coherence")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(fontsize=8)

    axes[1].bar(x, residual, width=0.45, color="#9c755f", label="corrected residual RMS")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylabel("normalized residual RMS")
    axes[1].set_title("Residuals and launch gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"coherent pairs: {summary['waveform_coherent_pair_count']}/{summary['content_pair_count']}\n"
        f"min corrected corr: {summary['min_corrected_field_trace_abs_correlation']:.3f}\n"
        f"min improvement: {summary['min_abs_correlation_improvement']:.3f}\n"
        f"radius matches: {summary['radius_match_pair_count']}/{summary['content_pair_count']}\n"
        f"spatial translation: {summary['content_single_translation_supported']}\n"
        f"field FWI: {summary['ready_for_field_fwi']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short-anchor waveform coherence audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, gates_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_waveform_coherence_audit.png`",
                "",
                "This CPU-only figure audits whether the content-backed short anchors",
                "support waveform-morphology QC after relative timing correction.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Content pairs: `{summary['content_pair_count']}`.",
                f"Waveform-coherent pairs: `{summary['waveform_coherent_pair_count']}`.",
                f"Minimum corrected field-trace absolute correlation: `{summary['min_corrected_field_trace_abs_correlation']}`.",
                f"Minimum event-local field-trace absolute correlation: `{summary['min_event_local_field_trace_abs_correlation']}`.",
                f"Minimum correlation improvement: `{summary['min_abs_correlation_improvement']}`.",
                f"Radius-match pairs: `{summary['radius_match_pair_count']}`.",
                f"Content single translation supported: `{summary['content_single_translation_supported']}`.",
                f"Ready for waveform morphology QC: `{summary['ready_for_waveform_morphology_qc']}`.",
                f"Ready for geometry seed: `{summary['ready_for_geometry_seed']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Waveform coherence rows: `{rows_csv.name}`.",
                f"- Gate rows: `{gates_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved field waveform/alignment tables only. It does",
                "not run FDTD, FWI, GPU kernels, 3D/HPC jobs, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--panel-run", default=DEFAULT_PANEL_RUN)
    parser.add_argument("--alignment-run", default=DEFAULT_ALIGNMENT_RUN)
    parser.add_argument("--leave-one-run", default=DEFAULT_LEAVE_ONE_RUN)
    parser.add_argument("--spatial-consistency-run", default=DEFAULT_SPATIAL_CONSISTENCY_RUN)
    parser.add_argument("--inversion-readiness-run", default=DEFAULT_INVERSION_READINESS_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_waveform_coherence_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    panel_dir = field_root / args.panel_run
    alignment_dir = field_root / args.alignment_run
    leave_one_dir = field_root / args.leave_one_run
    spatial_dir = field_root / args.spatial_consistency_run
    inversion_dir = field_root / args.inversion_readiness_run

    panel_rows = read_csv_rows(panel_dir / "data/content_backed_waveform_panel_rows.csv")
    alignment_rows = read_csv_rows(alignment_dir / "data/content_anchor_trace_alignment_rows.csv")
    panel_summary = read_json(panel_dir / "data/content_backed_waveform_panel_summary.json")
    alignment_summary = read_json(alignment_dir / "data/content_anchor_trace_alignment_summary.json")
    leave_one_summary = read_json(leave_one_dir / "data/field_short_anchor_leave_one_summary.json")
    spatial_summary = read_json(spatial_dir / "data/field_short_anchor_spatial_consistency_summary.json")
    inversion_summary = read_json(inversion_dir / "data/field_inversion_readiness_synthesis_summary.json")

    rows = build_waveform_coherence_rows(alignment_rows, panel_rows)
    summary = summarize_waveform_coherence(
        rows,
        panel_summary,
        alignment_summary,
        leave_one_summary,
        spatial_summary,
        inversion_summary,
    )
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=field_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_short_anchor_waveform_coherence_rows.csv"
    gates_csv = data_dir / "field_short_anchor_waveform_coherence_gates.csv"
    summary_json = data_dir / "field_short_anchor_waveform_coherence_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_waveform_coherence_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_waveform_coherence(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv, gates_csv)

    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_panel_summary_json": str(panel_dir / "data/content_backed_waveform_panel_summary.json"),
        "source_panel_rows_csv": str(panel_dir / "data/content_backed_waveform_panel_rows.csv"),
        "source_alignment_summary_json": str(alignment_dir / "data/content_anchor_trace_alignment_summary.json"),
        "source_alignment_rows_csv": str(alignment_dir / "data/content_anchor_trace_alignment_rows.csv"),
        "source_leave_one_summary_json": str(leave_one_dir / "data/field_short_anchor_leave_one_summary.json"),
        "source_spatial_consistency_summary_json": str(
            spatial_dir / "data/field_short_anchor_spatial_consistency_summary.json"
        ),
        "source_inversion_readiness_summary_json": str(
            inversion_dir / "data/field_inversion_readiness_synthesis_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_waveform_coherence_audit",
        {
            "panel_run": args.panel_run,
            "alignment_run": args.alignment_run,
            "leave_one_run": args.leave_one_run,
            "spatial_consistency_run": args.spatial_consistency_run,
            "inversion_readiness_run": args.inversion_readiness_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
