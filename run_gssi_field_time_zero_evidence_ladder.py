#!/usr/bin/env python3
"""Consolidate local GSSI field time-zero evidence into one decision ladder."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_BUDGET_RUN = "075_gssi51600s_field_time_zero_uncertainty_budget"
DEFAULT_PERTURBATION_RUN = "078_gssi51600s_field_time_zero_perturbation_sensitivity"
DEFAULT_CONFLICT_RUN = "097_gssi51600s_field_timing_anchor_conflict_synthesis"
DEFAULT_DISCRIMINANT_RUN = "105_gssi51600s_field_timing_discriminant_scorecard"
DEFAULT_ENVELOPE_RUN = "115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog"
DEFAULT_SPATIAL_TRANSFER_RUN = "116_gssi51600s_field_spatial_transfer_audit_post_timing_envelope"
DEFAULT_ANCHOR_INTERVAL_RUN = "117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer"
DEFAULT_DIMENSIONALITY_RUN = "118_gssi51600s_field_hpc_dimensionality_decision_card_post_anchor_interval"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def boolish(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def ladder_row(
    *,
    gate_key: str,
    status: str,
    readiness_score: float,
    evidence: str,
    allowed_use: str,
    blocked_use: str,
) -> dict:
    return {
        "gate_key": gate_key,
        "status": status,
        "readiness_score": float(readiness_score),
        "evidence": evidence,
        "allowed_use": allowed_use,
        "blocked_use": blocked_use,
    }


def build_ladder_rows(
    *,
    budget: dict,
    perturbation: dict,
    conflict: dict,
    discriminant: dict,
    envelope: dict,
    spatial_transfer: dict,
    anchor_interval: dict,
    dimensionality: dict,
) -> list[dict]:
    short_supported = (
        boolish(budget.get("ready_for_manuscript_time_zero_budget"))
        and boolish(perturbation.get("ready_for_manuscript_uncertainty_sensitivity"))
        and boolish(envelope.get("ready_for_short_relative_timing_qc"))
        and boolish(anchor_interval.get("ready_for_short_relative_timing_qc"))
    )
    absolute_blocked = (
        not boolish(conflict.get("absolute_time_zero_ready"))
        and not boolish(discriminant.get("absolute_time_zero_ready"))
        and not boolish(envelope.get("ready_for_absolute_time_zero"))
        and not boolish(anchor_interval.get("ready_for_absolute_time_zero"))
    )
    long_transfer_blocked = (
        not boolish(envelope.get("ready_for_long_short_transfer"))
        and not boolish(spatial_transfer.get("ready_for_short_to_long_timing_transfer"))
        and not boolish(dimensionality.get("ready_for_long_short_transfer"))
    )
    field_fwi_blocked = (
        not boolish(budget.get("field_fwi_ready"))
        and not boolish(perturbation.get("field_fwi_ready"))
        and not boolish(conflict.get("field_fwi_ready"))
        and not boolish(discriminant.get("field_fwi_ready"))
        and not boolish(dimensionality.get("ready_for_field_fwi"))
    )
    rows = [
        ladder_row(
            gate_key="short_relative_timing_budget",
            status="supported" if short_supported else "review",
            readiness_score=0.95 if short_supported else 0.35,
            evidence=(
                f"offset={safe_float(budget.get('relative_anchor_offset_ns')):.6f} ns; "
                f"half_width={safe_float(budget.get('conservative_half_width_ns')):.6f} ns; "
                f"bootstrap_ci_width={safe_float(budget.get('bootstrap_ci_width_ns')):.6f} ns; "
                f"content_residual={safe_float(budget.get('max_abs_content_anchor_residual_ns')):.6f} ns"
            ),
            allowed_use="short 014/016 relative time-zero QC with conservative uncertainty bounds",
            blocked_use="absolute time-zero, cover-depth, radius, field FWI",
        ),
        ladder_row(
            gate_key="perturbation_robustness",
            status="supported" if boolish(perturbation.get("ready_for_manuscript_uncertainty_sensitivity")) else "review",
            readiness_score=0.85 if boolish(perturbation.get("ready_for_manuscript_uncertainty_sensitivity")) else 0.35,
            evidence=(
                f"supported={safe_float(perturbation.get('supported_row_count')):.0f}/"
                f"{safe_float(perturbation.get('row_count')):.0f}; "
                f"min_improvement={safe_float(perturbation.get('min_nonraw_matrix_improvement')):.6f}; "
                f"min_corr={safe_float(perturbation.get('min_nonraw_corrected_abs_correlation')):.6f}"
            ),
            allowed_use="bootstrap/conservative offset sensitivity for short-pair QC",
            blocked_use="absolute timing or inversion calibration",
        ),
        ladder_row(
            gate_key="timing_family_discriminant",
            status="separates_short_from_controls" if boolish(conflict.get("ready_for_manuscript_field_timing_boundary")) else "review",
            readiness_score=0.8 if boolish(conflict.get("ready_for_manuscript_field_timing_boundary")) else 0.35,
            evidence=(
                f"early_vs_short={safe_float(conflict.get('early_vs_short_delta_half_widths')):.3f} half-widths; "
                f"long_vs_short={safe_float(conflict.get('long_vs_short_delta_half_widths')):.3f} half-widths; "
                f"short_nonraw_supported={safe_float(discriminant.get('short_nonraw_supported_count')):.0f}/"
                f"{safe_float(discriminant.get('short_nonraw_row_count')):.0f}"
            ),
            allowed_use="timing-boundary wording separating short content, early common-mode, and long pattern timing",
            blocked_use="collapsing all timing families into one absolute time-zero",
        ),
        ladder_row(
            gate_key="anchor_interval_support",
            status="supported" if boolish(anchor_interval.get("ready_for_short_relative_timing_qc")) else "review",
            readiness_score=0.9 if boolish(anchor_interval.get("ready_for_short_relative_timing_qc")) else 0.35,
            evidence=(
                f"short_inside={safe_float(anchor_interval.get('short_anchor_inside_supported_interval_count')):.0f}/"
                f"{safe_float(anchor_interval.get('short_anchor_count')):.0f}; "
                f"content_inside={safe_float(anchor_interval.get('short_content_anchor_inside_supported_interval_count')):.0f}/"
                f"{safe_float(anchor_interval.get('short_content_anchor_count')):.0f}; "
                f"min_margin={safe_float(anchor_interval.get('min_margin_to_supported_interval_edge_mm')):.3f} mm"
            ),
            allowed_use="supported-interval visual QC for short-profile anchors",
            blocked_use="full-profile field inversion or unsupported intervals",
        ),
        ladder_row(
            gate_key="long_short_transfer",
            status="blocked" if long_transfer_blocked else "review",
            readiness_score=0.0 if long_transfer_blocked else 0.45,
            evidence=(
                f"long_reject={safe_float(envelope.get('long_pattern_reject_short_transfer_count')):.0f}; "
                f"long_covered={safe_float(spatial_transfer.get('long_pattern_with_nearest_short_content_within_threshold_count')):.0f}/"
                f"{safe_float(spatial_transfer.get('long_pattern_anchor_count')):.0f}; "
                f"median_long_to_short={safe_float(spatial_transfer.get('median_long_to_short_distance_mm')):.3f} mm"
            ),
            allowed_use="long profiles as pattern-only context",
            blocked_use="transferring short-pair timing to long profiles",
        ),
        ladder_row(
            gate_key="absolute_time_zero",
            status="blocked" if absolute_blocked else "review",
            readiness_score=0.0 if absolute_blocked else 0.45,
            evidence=(
                f"conflict_abs_ready={boolish(conflict.get('absolute_time_zero_ready'))}; "
                f"discriminant_abs_ready={boolish(discriminant.get('absolute_time_zero_ready'))}; "
                f"early_low_margin={boolish(discriminant.get('early_has_low_uniqueness_margin'))}"
            ),
            allowed_use="explicit not-absolute timing claim boundary",
            blocked_use="absolute time-zero, calibrated depth, radius, field FWI",
        ),
        ladder_row(
            gate_key="field_fwi_hpc",
            status="blocked" if field_fwi_blocked else "review",
            readiness_score=0.0 if field_fwi_blocked else 0.45,
            evidence=(
                f"field_fwi={boolish(dimensionality.get('ready_for_field_fwi'))}; "
                f"3d_hpc={boolish(dimensionality.get('ready_for_3d_hpc'))}; "
                f"is_3d={boolish(dimensionality.get('is_3d_survey'))}"
            ),
            allowed_use="local CPU-side 2D field QC and manuscript supplement evidence",
            blocked_use="field FWI, 3D/HPC, cover-depth/radius recovery",
        ),
    ]
    return rows


def summarize_ladder(rows: list[dict], budget: dict, envelope: dict, anchor_interval: dict, spatial_transfer: dict, dimensionality: dict) -> dict:
    by_key = {row["gate_key"]: row for row in rows}
    ready_short = by_key["short_relative_timing_budget"]["status"] == "supported"
    long_blocked = by_key["long_short_transfer"]["status"] == "blocked"
    abs_blocked = by_key["absolute_time_zero"]["status"] == "blocked"
    fwi_blocked = by_key["field_fwi_hpc"]["status"] == "blocked"
    return {
        "policy_label": "gssi51600s_field_time_zero_evidence_ladder_short_qc_only",
        "ladder_row_count": len(rows),
        "ready_for_short_relative_timing_qc": bool(ready_short),
        "ready_for_long_short_transfer": not bool(long_blocked),
        "ready_for_absolute_time_zero": not bool(abs_blocked),
        "ready_for_field_fwi": not bool(fwi_blocked),
        "ready_for_3d_hpc": boolish(dimensionality.get("ready_for_3d_hpc")),
        "short_relative_offset_ns": safe_float(budget.get("relative_anchor_offset_ns")),
        "short_conservative_half_width_ns": safe_float(budget.get("conservative_half_width_ns")),
        "short_anchor_inside_envelope_count": safe_float(envelope.get("short_anchor_inside_envelope_count"), 0.0),
        "short_anchor_inside_supported_interval_count": safe_float(
            anchor_interval.get("short_anchor_inside_supported_interval_count"), 0.0
        ),
        "anchor_interval_min_margin_mm": safe_float(anchor_interval.get("min_margin_to_supported_interval_edge_mm"), 0.0),
        "long_pattern_reject_short_transfer_count": safe_float(
            envelope.get("long_pattern_reject_short_transfer_count"), 0.0
        ),
        "long_pattern_with_nearest_short_content_count": safe_float(
            spatial_transfer.get("long_pattern_with_nearest_short_content_within_threshold_count"), 0.0
        ),
        "median_long_to_short_distance_mm": safe_float(spatial_transfer.get("median_long_to_short_distance_mm"), 0.0),
        "gpu_priority": "none",
        "decision": (
            "Use this ladder as the current measured-field time-zero claim boundary: "
            "short 014/016 relative timing QC is supported with conservative uncertainty and interval evidence, "
            "while long-profile transfer, absolute time-zero, field FWI, and 3D/HPC remain blocked."
        ),
    }


def plot_ladder(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["gate_key"].replace("_", "\n") for row in rows]
    scores = [safe_float(row["readiness_score"], 0.0) for row in rows]
    colors = ["#2f9d55" if score >= 0.75 else "#d99a19" if score >= 0.35 else "#c7302b" for score in scores]
    fig, axes = plt.subplots(1, 2, figsize=(14.8, 5.2), constrained_layout=True)
    x = np.arange(len(rows))
    axes[0].bar(x, scores, color=colors, edgecolor="#333333", linewidth=0.6)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_ylabel("readiness score")
    axes[0].set_title("Field time-zero evidence ladder")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    decision_labels = ["short\nrelative", "long\ntransfer", "absolute\nt0", "field\nFWI", "3D\nHPC"]
    decision_values = [
        summary["ready_for_short_relative_timing_qc"],
        summary["ready_for_long_short_transfer"],
        summary["ready_for_absolute_time_zero"],
        summary["ready_for_field_fwi"],
        summary["ready_for_3d_hpc"],
    ]
    axes[1].bar(
        np.arange(len(decision_labels)),
        [1 if value else 0 for value in decision_values],
        color=["#2f9d55" if value else "#c7302b" for value in decision_values],
    )
    axes[1].set_xticks(np.arange(len(decision_labels)), decision_labels, fontsize=9)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Claim gates")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"offset={summary['short_relative_offset_ns']:.6f} ns\n"
        f"half-width={summary['short_conservative_half_width_ns']:.6f} ns\n"
        f"short anchors inside={summary['short_anchor_inside_supported_interval_count']:.0f}/3\n"
        f"long transfer ready={summary['ready_for_long_short_transfer']}",
        transform=axes[1].transAxes,
        va="top",
        ha="left",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Local GSSI field time-zero evidence ladder", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `field_time_zero_evidence_ladder.png`",
                "",
                "This CPU-only figure consolidates existing local GSSI field timing evidence.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Ready for short relative timing QC: `{summary['ready_for_short_relative_timing_qc']}`.",
                f"Ready for long-short transfer: `{summary['ready_for_long_short_transfer']}`.",
                f"Ready for absolute time-zero: `{summary['ready_for_absolute_time_zero']}`.",
                f"Ready for field FWI: `{summary['ready_for_field_fwi']}`.",
                f"Ready for 3D/HPC: `{summary['ready_for_3d_hpc']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "Outputs:",
                "",
                f"- Ladder rows: `{rows_csv.name}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads existing field summaries only. It does not run FDTD, FWI,",
                "GPU kernels, 3D/HPC jobs, or neural-network training.",
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
    parser.add_argument("--budget-run", default=DEFAULT_BUDGET_RUN)
    parser.add_argument("--perturbation-run", default=DEFAULT_PERTURBATION_RUN)
    parser.add_argument("--conflict-run", default=DEFAULT_CONFLICT_RUN)
    parser.add_argument("--discriminant-run", default=DEFAULT_DISCRIMINANT_RUN)
    parser.add_argument("--envelope-run", default=DEFAULT_ENVELOPE_RUN)
    parser.add_argument("--spatial-transfer-run", default=DEFAULT_SPATIAL_TRANSFER_RUN)
    parser.add_argument("--anchor-interval-run", default=DEFAULT_ANCHOR_INTERVAL_RUN)
    parser.add_argument("--dimensionality-run", default=DEFAULT_DIMENSIONALITY_RUN)
    parser.add_argument("--run-name", default="gssi51600s_field_time_zero_evidence_ladder")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_root = field_dataset_output_root(args.field_root, args.dataset_id)
    budget = read_json(dataset_root / args.budget_run / "data/field_time_zero_uncertainty_budget_summary.json")
    perturbation = read_json(
        dataset_root / args.perturbation_run / "data/field_time_zero_perturbation_sensitivity_summary.json"
    )
    conflict = read_json(dataset_root / args.conflict_run / "data/field_timing_anchor_conflict_summary.json")
    discriminant = read_json(
        dataset_root / args.discriminant_run / "data/field_timing_discriminant_scorecard_summary.json"
    )
    envelope = read_json(dataset_root / args.envelope_run / "data/field_cue_timing_envelope_summary.json")
    spatial_transfer = read_json(
        dataset_root / args.spatial_transfer_run / "data/field_spatial_transfer_audit_summary.json"
    )
    anchor_interval = read_json(
        dataset_root / args.anchor_interval_run / "data/field_anchor_interval_reconciliation_summary.json"
    )
    dimensionality = read_json(
        dataset_root / args.dimensionality_run / "data/field_hpc_dimensionality_decision_summary.json"
    )

    rows = build_ladder_rows(
        budget=budget,
        perturbation=perturbation,
        conflict=conflict,
        discriminant=discriminant,
        envelope=envelope,
        spatial_transfer=spatial_transfer,
        anchor_interval=anchor_interval,
        dimensionality=dimensionality,
    )
    summary = summarize_ladder(rows, budget, envelope, anchor_interval, spatial_transfer, dimensionality)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(dataset_root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "field_time_zero_evidence_ladder_rows.csv"
    summary_json = data_dir / "field_time_zero_evidence_ladder_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "field_time_zero_evidence_ladder.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    plot_ladder(rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    summary["paths"] = {
        "rows_csv": str(rows_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_figure_notes(figure_notes, summary, rows_csv)
    write_run_manifest(
        str(outdir),
        "gssi_field_time_zero_evidence_ladder",
        {
            "budget_run": args.budget_run,
            "perturbation_run": args.perturbation_run,
            "conflict_run": args.conflict_run,
            "discriminant_run": args.discriminant_run,
            "envelope_run": args.envelope_run,
            "spatial_transfer_run": args.spatial_transfer_run,
            "anchor_interval_run": args.anchor_interval_run,
            "dimensionality_run": args.dimensionality_run,
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
