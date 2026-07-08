#!/usr/bin/env python3
"""Audit signed short-anchor field morphology from saved alignment evidence."""

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


DEFAULT_ALIGNMENT_RUN = "039_gssi51600s_content_anchor_trace_alignment"
DEFAULT_WAVEFORM_COHERENCE_RUN = "124_gssi51600s_field_short_anchor_waveform_coherence_audit"
DEFAULT_RADIUS_DEGENERACY_RUN = "125_gssi51600s_field_short_anchor_radius_degeneracy_audit"
DEFAULT_MIN_CORRECTED_SIGNED_CORRELATION = 0.90
DEFAULT_MIN_EVENT_LOCAL_CORRELATION = 0.95
DEFAULT_MIN_CORRELATION_IMPROVEMENT = 0.30
DEFAULT_MAX_TIMING_RESIDUAL_NS = 0.05


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "supported"}


def signed_correlation(abs_correlation: object, polarity: object) -> float:
    corr = safe_float(abs_correlation)
    if not math.isfinite(corr):
        return math.nan
    label = str(polarity).strip().lower()
    if label == "same":
        return corr
    if label == "opposite":
        return -corr
    return math.nan


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def _radius_pairs(radius_summary: dict) -> dict:
    return {
        "weak_radius_side_count": safe_float(radius_summary.get("weak_radius_side_count"), 0.0),
        "selected_radius_mismatch_pair_count": safe_float(
            radius_summary.get("selected_radius_mismatch_pair_count"), 0.0
        ),
        "common_radius_near_tie_pair_count": safe_float(
            radius_summary.get("common_radius_near_tie_pair_count"), 0.0
        ),
        "ready_for_radius_seed": bool(radius_summary.get("ready_for_radius_seed", False)),
        "ready_for_radius_recovery": bool(radius_summary.get("ready_for_radius_recovery", False)),
        "ready_for_geometry_seed": bool(radius_summary.get("ready_for_geometry_seed", False)),
        "ready_for_field_fwi": bool(radius_summary.get("ready_for_field_fwi", False)),
    }


def build_signed_morphology_rows(
    alignment_rows: list[dict],
    radius_summary: dict,
    *,
    min_corrected_signed_correlation: float = DEFAULT_MIN_CORRECTED_SIGNED_CORRELATION,
    min_event_local_correlation: float = DEFAULT_MIN_EVENT_LOCAL_CORRELATION,
    min_correlation_improvement: float = DEFAULT_MIN_CORRELATION_IMPROVEMENT,
    max_timing_residual_ns: float = DEFAULT_MAX_TIMING_RESIDUAL_NS,
) -> list[dict]:
    radius = _radius_pairs(radius_summary)
    rows: list[dict] = []
    for row in alignment_rows:
        if not boolish(row.get("anchor_content_backed")):
            continue
        raw_signed = signed_correlation(row.get("raw_field_trace_abs_correlation"), row.get("raw_field_trace_polarity"))
        corrected_signed = signed_correlation(
            row.get("corrected_field_trace_abs_correlation"),
            row.get("corrected_field_trace_polarity"),
        )
        event_abs = safe_float(row.get("event_local_field_trace_abs_correlation"))
        improvement = safe_float(row.get("field_trace_abs_correlation_improvement"))
        timing_residual = abs(safe_float(row.get("corrected_comparison_minus_reference_phase_time_ns")))
        corrected_residual_rms = safe_float(row.get("corrected_field_trace_residual_rms"))
        supported = (
            corrected_signed >= min_corrected_signed_correlation
            and event_abs >= min_event_local_correlation
            and improvement >= min_correlation_improvement
            and timing_residual <= max_timing_residual_ns
        )
        rows.append(
            {
                "pair_index": int(safe_float(row.get("pair_index"), -1)),
                "reference_file": row.get("reference_file", ""),
                "comparison_file": row.get("comparison_file", ""),
                "reference_apex_group": row.get("reference_apex_group", ""),
                "comparison_apex_group": row.get("comparison_apex_group", ""),
                "anchor_reference_x_mm": safe_float(row.get("anchor_reference_x_mm")),
                "anchor_comparison_aligned_x_mm": safe_float(row.get("anchor_comparison_aligned_x_mm")),
                "anchor_aligned_x_residual_mm": safe_float(row.get("anchor_aligned_x_residual_mm")),
                "reference_best_radius_mm": safe_float(row.get("reference_best_radius_mm")),
                "comparison_best_radius_mm": safe_float(row.get("comparison_best_radius_mm")),
                "radius_match": boolish(row.get("radius_match")),
                "raw_field_trace_polarity": row.get("raw_field_trace_polarity", ""),
                "corrected_field_trace_polarity": row.get("corrected_field_trace_polarity", ""),
                "raw_signed_correlation": raw_signed,
                "corrected_signed_correlation": corrected_signed,
                "raw_field_trace_abs_correlation": safe_float(row.get("raw_field_trace_abs_correlation")),
                "corrected_field_trace_abs_correlation": safe_float(row.get("corrected_field_trace_abs_correlation")),
                "event_local_field_trace_abs_correlation": event_abs,
                "field_trace_abs_correlation_improvement": improvement,
                "corrected_abs_timing_residual_ns": timing_residual,
                "corrected_field_trace_residual_rms": corrected_residual_rms,
                "signed_morphology_supported": supported,
                "amplitude_calibration_ready": False,
                "radius_seed_ready": radius["ready_for_radius_seed"],
                "geometry_seed_ready": radius["ready_for_geometry_seed"],
                "field_fwi_ready": radius["ready_for_field_fwi"],
                "allowed_use": "signed short-profile waveform morphology QC",
                "blocked_use": "amplitude calibration, radius/geometry/cover-depth recovery, field FWI, 3D/HPC",
            }
        )
    return sorted(rows, key=lambda item: item["pair_index"])


def summarize_signed_morphology(
    rows: list[dict],
    alignment_summary: dict,
    waveform_summary: dict,
    radius_summary: dict,
) -> dict:
    corrected_signed = _finite([safe_float(row.get("corrected_signed_correlation")) for row in rows])
    raw_signed = _finite([safe_float(row.get("raw_signed_correlation")) for row in rows])
    event_abs = _finite([safe_float(row.get("event_local_field_trace_abs_correlation")) for row in rows])
    improvements = _finite([safe_float(row.get("field_trace_abs_correlation_improvement")) for row in rows])
    timing_residuals = _finite([safe_float(row.get("corrected_abs_timing_residual_ns")) for row in rows])
    residual_rms = _finite([safe_float(row.get("corrected_field_trace_residual_rms")) for row in rows])
    supported = [row for row in rows if boolish(row.get("signed_morphology_supported"))]
    corrected_same = [row for row in rows if str(row.get("corrected_field_trace_polarity", "")).lower() == "same"]
    raw_same = [row for row in rows if str(row.get("raw_field_trace_polarity", "")).lower() == "same"]
    radius = _radius_pairs(radius_summary)
    signed_ready = len(rows) > 0 and len(supported) == len(rows)
    return {
        "policy_label": "gssi51600s_field_short_anchor_signed_morphology_qc_only",
        "source_alignment_policy_label": alignment_summary.get("policy_label", ""),
        "source_waveform_coherence_policy_label": waveform_summary.get("policy_label", ""),
        "source_radius_degeneracy_policy_label": radius_summary.get("policy_label", ""),
        "content_pair_count": len(rows),
        "signed_morphology_supported_pair_count": len(supported),
        "corrected_same_polarity_pair_count": len(corrected_same),
        "raw_same_polarity_pair_count": len(raw_same),
        "min_corrected_signed_correlation": min(corrected_signed) if corrected_signed else math.nan,
        "mean_corrected_signed_correlation": float(np.mean(corrected_signed)) if corrected_signed else math.nan,
        "min_raw_signed_correlation": min(raw_signed) if raw_signed else math.nan,
        "mean_raw_signed_correlation": float(np.mean(raw_signed)) if raw_signed else math.nan,
        "min_event_local_abs_correlation": min(event_abs) if event_abs else math.nan,
        "min_abs_correlation_improvement": min(improvements) if improvements else math.nan,
        "mean_abs_correlation_improvement": float(np.mean(improvements)) if improvements else math.nan,
        "max_corrected_abs_timing_residual_ns": max(timing_residuals) if timing_residuals else math.nan,
        "max_corrected_trace_residual_rms": max(residual_rms) if residual_rms else math.nan,
        "weak_radius_side_count": radius["weak_radius_side_count"],
        "selected_radius_mismatch_pair_count": radius["selected_radius_mismatch_pair_count"],
        "common_radius_near_tie_pair_count": radius["common_radius_near_tie_pair_count"],
        "ready_for_signed_waveform_morphology_qc": signed_ready,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_radius_seed": radius["ready_for_radius_seed"],
        "ready_for_radius_recovery": radius["ready_for_radius_recovery"],
        "ready_for_geometry_seed": radius["ready_for_geometry_seed"],
        "ready_for_cover_depth_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
        "decision": (
            "The content-backed short anchors keep same-polarity, high-correlation waveform morphology "
            "after the relative time correction. This supports signed waveform-morphology QC only. "
            "The traces are robust-normalized, radius remains weak/near-tied, and spatial/depth controls "
            "remain unavailable, so do not use this as amplitude calibration, radius/geometry seeding, "
            "field FWI, 3D/HPC, or heavy field-work evidence."
        ),
    }


def build_gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "signed_waveform_morphology_qc",
            "ready": summary["ready_for_signed_waveform_morphology_qc"],
            "allowed_use": "field supplement signed waveform-morphology QC",
            "blocked_use": "none within morphology-QC scope",
            "evidence": (
                f"same-polarity corrected pairs={summary['corrected_same_polarity_pair_count']}/"
                f"{summary['content_pair_count']}; min signed corr="
                f"{summary['min_corrected_signed_correlation']:.6f}"
            ),
        },
        {
            "gate_key": "absolute_amplitude_calibration",
            "ready": summary["ready_for_absolute_amplitude_calibration"],
            "allowed_use": "none",
            "blocked_use": "amplitude-calibrated field inversion or material inference",
            "evidence": "trace comparison uses robust-normalized waveform windows",
        },
        {
            "gate_key": "radius_seed",
            "ready": summary["ready_for_radius_seed"],
            "allowed_use": "none",
            "blocked_use": "field radius seed",
            "evidence": (
                f"weak radius sides={summary['weak_radius_side_count']}; "
                f"mismatch pairs={summary['selected_radius_mismatch_pair_count']}; "
                f"common-radius near ties={summary['common_radius_near_tie_pair_count']}"
            ),
        },
        {
            "gate_key": "geometry_seed",
            "ready": summary["ready_for_geometry_seed"],
            "allowed_use": "none",
            "blocked_use": "field geometry seed",
            "evidence": "profile spatial calibration and repeatable radius/depth controls remain unavailable",
        },
        {
            "gate_key": "field_fwi",
            "ready": summary["ready_for_field_fwi"],
            "allowed_use": "none",
            "blocked_use": "field FWI, 3D/HPC, or heavy field work",
            "evidence": "signed morphology alone is not an inversion launch contract",
        },
    ]


def plot_signed_morphology(rows: list[dict], summary: dict, save_path: Path) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.8), constrained_layout=True)
    pair_labels = [f"pair {int(row['pair_index'])}" for row in rows]
    x = np.arange(len(rows), dtype=float)
    width = 0.24
    axes[0].bar(
        x - width,
        [safe_float(row.get("raw_signed_correlation")) for row in rows],
        width=width,
        color="#c44e52",
        label="raw signed",
    )
    axes[0].bar(
        x,
        [safe_float(row.get("corrected_signed_correlation")) for row in rows],
        width=width,
        color="#4c72b0",
        label="corrected signed",
    )
    axes[0].bar(
        x + width,
        [safe_float(row.get("event_local_field_trace_abs_correlation")) for row in rows],
        width=width,
        color="#55a868",
        label="event-local |corr|",
    )
    axes[0].axhline(DEFAULT_MIN_CORRECTED_SIGNED_CORRELATION, color="#333333", linestyle="--", linewidth=0.8)
    axes[0].set_xticks(x, pair_labels)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("correlation")
    axes[0].set_title("Signed field-trace morphology after timing correction")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    gate_labels = ["signed\nmorph.", "amplitude\ncal.", "radius\nseed", "geometry\nseed", "field\nFWI"]
    gate_values = [
        summary["ready_for_signed_waveform_morphology_qc"],
        summary["ready_for_absolute_amplitude_calibration"],
        summary["ready_for_radius_seed"],
        summary["ready_for_geometry_seed"],
        summary["ready_for_field_fwi"],
    ]
    colors = ["#59a14f" if value else "#bab0ac" for value in gate_values]
    axes[1].bar(np.arange(len(gate_labels)), [1 if value else 0 for value in gate_values], color=colors)
    axes[1].set_xticks(np.arange(len(gate_labels)), gate_labels)
    axes[1].set_ylim(0, 1.15)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_title("Field claim gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.06,
        f"same-polarity corrected pairs: {summary['corrected_same_polarity_pair_count']}/"
        f"{summary['content_pair_count']}\n"
        f"min corrected signed corr: {summary['min_corrected_signed_correlation']:.3f}\n"
        f"weak radius sides: {summary['weak_radius_side_count']:.0f}\n"
        f"common-radius near ties: {summary['common_radius_near_tie_pair_count']:.0f}",
        transform=axes[1].transAxes,
        va="bottom",
        ha="left",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("GSSI 51600S short-anchor signed morphology audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, gates_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_short_anchor_signed_morphology_audit.png`",
                "",
                "This CPU-only figure audits whether the content-backed short anchors",
                "support signed field waveform-morphology QC after relative timing correction.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Content pairs: `{summary['content_pair_count']}`.",
                f"Corrected same-polarity pairs: `{summary['corrected_same_polarity_pair_count']}`.",
                f"Min corrected signed correlation: `{summary['min_corrected_signed_correlation']}`.",
                f"Ready for signed morphology QC: `{summary['ready_for_signed_waveform_morphology_qc']}`.",
                f"Ready for amplitude calibration: `{summary['ready_for_absolute_amplitude_calibration']}`.",
                f"Ready for radius seed: `{summary['ready_for_radius_seed']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Pair rows: `{rows_csv.name}`.",
                f"- Gate rows: `{gates_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved alignment, waveform-coherence, and radius-degeneracy artifacts only. It does not",
                "run DZT preprocessing, FDTD, FWI, GPU kernels, field inversion, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--alignment-run", default=DEFAULT_ALIGNMENT_RUN)
    parser.add_argument("--waveform-coherence-run", default=DEFAULT_WAVEFORM_COHERENCE_RUN)
    parser.add_argument("--radius-degeneracy-run", default=DEFAULT_RADIUS_DEGENERACY_RUN)
    parser.add_argument("--min-corrected-signed-correlation", type=float, default=DEFAULT_MIN_CORRECTED_SIGNED_CORRELATION)
    parser.add_argument("--min-event-local-correlation", type=float, default=DEFAULT_MIN_EVENT_LOCAL_CORRELATION)
    parser.add_argument("--min-correlation-improvement", type=float, default=DEFAULT_MIN_CORRELATION_IMPROVEMENT)
    parser.add_argument("--max-timing-residual-ns", type=float, default=DEFAULT_MAX_TIMING_RESIDUAL_NS)
    parser.add_argument("--run-name", default="gssi51600s_field_short_anchor_signed_morphology_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    alignment_dir = field_root / args.alignment_run
    waveform_dir = field_root / args.waveform_coherence_run
    radius_dir = field_root / args.radius_degeneracy_run

    alignment_rows = read_csv_rows(alignment_dir / "data/content_anchor_trace_alignment_rows.csv")
    alignment_summary = read_json(alignment_dir / "data/content_anchor_trace_alignment_summary.json")
    waveform_summary = read_json(waveform_dir / "data/field_short_anchor_waveform_coherence_summary.json")
    radius_summary = read_json(radius_dir / "data/field_short_anchor_radius_degeneracy_summary.json")

    rows = build_signed_morphology_rows(
        alignment_rows,
        radius_summary,
        min_corrected_signed_correlation=args.min_corrected_signed_correlation,
        min_event_local_correlation=args.min_event_local_correlation,
        min_correlation_improvement=args.min_correlation_improvement,
        max_timing_residual_ns=args.max_timing_residual_ns,
    )
    summary = summarize_signed_morphology(rows, alignment_summary, waveform_summary, radius_summary)
    gates = build_gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=field_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_short_anchor_signed_morphology_rows.csv"
    gates_csv = data_dir / "field_short_anchor_signed_morphology_gates.csv"
    summary_json = data_dir / "field_short_anchor_signed_morphology_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_short_anchor_signed_morphology_audit.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_signed_morphology(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv, gates_csv)

    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "source_alignment_rows_csv": str(alignment_dir / "data/content_anchor_trace_alignment_rows.csv"),
        "source_alignment_summary_json": str(alignment_dir / "data/content_anchor_trace_alignment_summary.json"),
        "source_waveform_coherence_summary_json": str(
            waveform_dir / "data/field_short_anchor_waveform_coherence_summary.json"
        ),
        "source_radius_degeneracy_summary_json": str(
            radius_dir / "data/field_short_anchor_radius_degeneracy_summary.json"
        ),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "gssi_field_short_anchor_signed_morphology_audit",
        {
            "alignment_run": args.alignment_run,
            "waveform_coherence_run": args.waveform_coherence_run,
            "radius_degeneracy_run": args.radius_degeneracy_run,
            "min_corrected_signed_correlation": args.min_corrected_signed_correlation,
            "min_event_local_correlation": args.min_event_local_correlation,
            "min_correlation_improvement": args.min_correlation_improvement,
            "max_timing_residual_ns": args.max_timing_residual_ns,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
