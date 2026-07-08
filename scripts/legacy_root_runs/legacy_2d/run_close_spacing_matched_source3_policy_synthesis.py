#!/usr/bin/env python3
"""Synthesize the completed close14/close50 matched source3 probe results."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter
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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_detector_rank_budget_diagnostic import safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CLOSE14_AGGREGATE = (
    "outputs/experiments/1351_coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates/"
    "data/coordinate_confidence_aggregate.json"
)
DEFAULT_CLOSE50_AGGREGATE = (
    "outputs/experiments/1355_coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates/"
    "data/coordinate_confidence_aggregate.json"
)
DEFAULT_QUEUE_SUMMARY = (
    "outputs/summary_tables/120_close_spacing_matched_source3_probe_queue/"
    "data/close_spacing_matched_source3_probe_queue_summary.json"
)
DEFAULT_CONFOUND_SUMMARY = (
    "outputs/summary_tables/111_close_spacing_source_density_confound_audit/"
    "data/close_spacing_source_density_confound_summary.json"
)

FAMILY_LABELS = {
    "close14_source3_txrx40": "close14 source3 Tx/Rx40",
    "close50_source3_txrx45": "close50 source3 Tx/Rx45",
}


def read_json(path: Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _truth_fraction(row_count: int, truth_count: int) -> float:
    return 0.0 if row_count <= 0 else truth_count / row_count


def _confidence_counts_text(counts: dict) -> str:
    return ",".join(f"{key}={value}" for key, value in sorted(counts.items())) if counts else ""


def _selected_branch_counter(rows: list[dict]) -> Counter:
    counter = Counter()
    for row in rows:
        x = safe_float(row.get("best_x_mm"), math.nan)
        z = safe_float(row.get("best_z_mm"), math.nan)
        radius = safe_float(row.get("best_radius_mm"), math.nan)
        if all(math.isfinite(value) for value in (x, z, radius)):
            counter[(x, z, radius)] += 1
    return counter


def _branch_label(branch: tuple[float, float, float] | None) -> str:
    if branch is None:
        return ""
    x, z, radius = branch
    return f"x={x:g} mm, z={z:g} mm, r={radius:g} mm"


def _first_input_summary(aggregate_json: dict) -> dict:
    paths = aggregate_json.get("input_summary_json", [])
    if not paths:
        return {}
    path = Path(paths[0])
    if not path.exists():
        return {}
    return read_json(path)


def family_row(family_key: str, aggregate_json: dict, input_summary: dict | None = None) -> dict:
    """Summarize one matched source3 aggregate."""
    aggregate = aggregate_json.get("aggregate", {})
    rows = list(aggregate_json.get("rows", []))
    input_summary = input_summary if input_summary is not None else _first_input_summary(aggregate_json)
    true_x = [safe_float(value, math.nan) for value in input_summary.get("true_x_values_mm", [])]
    true_z = [safe_float(value, math.nan) for value in input_summary.get("true_z_values_mm", [])]
    true_r = [safe_float(value, math.nan) for value in input_summary.get("truth_radius_values_mm", [])]
    row_count = safe_int(aggregate.get("row_count"), len(rows))
    truth_count = safe_int(aggregate.get("truth_geometry_count"), 0)
    selected = _selected_branch_counter(rows)
    selected_branch, selected_count = selected.most_common(1)[0] if selected else (None, 0)
    truth_target2 = (
        true_x[2] if len(true_x) > 2 else safe_float(rows[0].get("truth_x_mm"), math.nan) if rows else math.nan,
        true_z[2] if len(true_z) > 2 else safe_float(rows[0].get("truth_z_mm"), math.nan) if rows else math.nan,
        true_r[2] if len(true_r) > 2 else safe_float(rows[0].get("truth_radius_mm"), math.nan) if rows else math.nan,
    )
    target1_target2_gap = (
        abs(true_x[2] - true_x[1]) if len(true_x) > 2 and math.isfinite(true_x[2]) and math.isfinite(true_x[1]) else math.nan
    )
    confidence_counts = aggregate.get("confidence_label_counts", {})
    return {
        "family_key": family_key,
        "family_label": FAMILY_LABELS.get(family_key, family_key),
        "source_count": safe_int(rows[0].get("sources"), safe_int(input_summary.get("sources"), 3)) if rows else 3,
        "tx_rx_offset_mm": safe_float(
            rows[0].get("tx_rx_offset_mm") if rows else input_summary.get("tx_rx_offset_mm"),
            math.nan,
        ),
        "target1_target2_gap_mm": target1_target2_gap,
        "target2_x_mm": truth_target2[0],
        "target2_truth_branch": _branch_label(truth_target2),
        "row_count": row_count,
        "truth_geometry_count": truth_count,
        "truth_geometry_fraction": _truth_fraction(row_count, truth_count),
        "confidence_label_counts": _confidence_counts_text(confidence_counts),
        "strong_row_count": safe_int(confidence_counts.get("strong"), 0),
        "moderate_row_count": safe_int(confidence_counts.get("moderate"), 0),
        "weak_row_count": safe_int(confidence_counts.get("weak"), 0),
        "fallback_warning_count": safe_int(aggregate.get("fallback_warning_count"), 0),
        "radius_margin_abs_min": safe_float(aggregate.get("radius_margin_abs_min"), math.nan),
        "radius_margin_abs_mean": safe_float(aggregate.get("radius_margin_abs_mean"), math.nan),
        "radius_margin_abs_max": safe_float(aggregate.get("radius_margin_abs_max"), math.nan),
        "ambiguity_x_width_max_mm": safe_float(aggregate.get("ambiguity_x_width_max_mm"), math.nan),
        "ambiguity_radius_width_max_mm": safe_float(aggregate.get("ambiguity_radius_width_max_mm"), math.nan),
        "x_ambiguity_row_count": safe_int(aggregate.get("x_ambiguity_row_count"), 0),
        "selected_branch_unique_count": len(selected),
        "dominant_selected_branch": _branch_label(selected_branch),
        "dominant_selected_branch_count": selected_count,
        "dominant_selected_branch_fraction": _truth_fraction(row_count, selected_count),
        "all_rows_same_selected_branch": bool(row_count and len(selected) == 1 and selected_count == row_count),
        "all_rows_truth": bool(row_count and truth_count == row_count),
        "all_rows_nontruth": bool(row_count and truth_count == 0),
        "input_aggregate_json": aggregate_json.get("paths", {}).get("json", ""),
    }


def build_family_rows(close14_aggregate: dict, close50_aggregate: dict) -> list[dict]:
    return [
        family_row("close14_source3_txrx40", close14_aggregate),
        family_row("close50_source3_txrx45", close50_aggregate),
    ]


def build_claim_rows(family_rows: list[dict], queue_summary: dict, confound_summary: dict) -> list[dict]:
    by_key = {row["family_key"]: row for row in family_rows}
    close14 = by_key["close14_source3_txrx40"]
    close50 = by_key["close50_source3_txrx45"]
    queue_complete = safe_int(queue_summary.get("missing_seed_probe_count"), 1) == 0
    close14_truth = close14["all_rows_truth"] and close14["strong_row_count"] == close14["row_count"]
    close50_wrong = close50["all_rows_nontruth"] and close50["all_rows_same_selected_branch"]
    guarded_contrast = queue_complete and close14_truth and close50_wrong
    old_confound_count = (
        safe_int(confound_summary.get("acquisition_confound_count"), 0)
        + safe_int(confound_summary.get("geometry_confound_count"), 0)
        + safe_int(confound_summary.get("metadata_gap_count"), 0)
    )
    return [
        {
            "claim_key": "matched_source3_queue_complete",
            "ready": queue_complete,
            "allowed_wording": "the two matched source3 probe families are complete",
            "blocked_wording": "more queued matched source3 seeds remain",
            "evidence": f"missing_seed_probe_count={safe_int(queue_summary.get('missing_seed_probe_count'), -1)}",
        },
        {
            "claim_key": "close14_matched_txrx40_truth_result",
            "ready": close14_truth,
            "allowed_wording": "close14 source3 Tx/Rx40 selects the exact target2 geometry in all six rows",
            "blocked_wording": "close14 source3 fails when Tx/Rx is moved to 40 mm",
            "evidence": f"truth_rows={close14['truth_geometry_count']}/{close14['row_count']}; labels={close14['confidence_label_counts']}",
        },
        {
            "claim_key": "close50_reciprocal_txrx45_wrong_branch",
            "ready": close50_wrong,
            "allowed_wording": "close50 source3 Tx/Rx45 repeatedly selects the same near-truth wrong branch",
            "blocked_wording": "Tx/Rx45 rescues close50 source3 to exact recovery",
            "evidence": f"truth_rows={close50['truth_geometry_count']}/{close50['row_count']}; selected={close50['dominant_selected_branch']}",
        },
        {
            "claim_key": "guarded_acquisition_geometry_contrast",
            "ready": guarded_contrast,
            "allowed_wording": "matched source3 controls show a replicated close14/close50 contrast with explicit geometry caveats",
            "blocked_wording": "target spacing alone controls source3 success/failure",
            "evidence": f"old_confound_count={old_confound_count}; close14_truth={close14_truth}; close50_wrong={close50_wrong}",
        },
        {
            "claim_key": "spacing_only_causal_generalization",
            "ready": False,
            "allowed_wording": "none from the completed matched-source3 controls",
            "blocked_wording": "target1-target2 spacing alone explains the source3 outcome",
            "evidence": "absolute target2 x-position changes with spacing, and close50 produces a stable wrong branch rather than an ambiguity interval around truth",
        },
        {
            "claim_key": "broad_gpu_queue",
            "ready": False,
            "allowed_wording": "none",
            "blocked_wording": "launch broad close-spacing GPU sweeps",
            "evidence": "the narrow matched queue is complete; the next step is CPU/manuscript synthesis",
        },
        {
            "claim_key": "field_fwi_or_3d_hpc_from_local_field_archive",
            "ready": False,
            "allowed_wording": "field archive remains scoped 2D QC and collection-planning evidence",
            "blocked_wording": "launch field FWI, heavy field GPU work, or field 3D/HPC from this archive",
            "evidence": "field evidence chain still lacks absolute time-zero, amplitude calibration, target truth, and surveyed profile geometry",
        },
    ]


def synthesize_policy(family_rows: list[dict], claim_rows: list[dict]) -> dict:
    by_key = {row["family_key"]: row for row in family_rows}
    claim_ready = {row["claim_key"]: bool(row["ready"]) for row in claim_rows}
    close14 = by_key["close14_source3_txrx40"]
    close50 = by_key["close50_source3_txrx45"]
    return {
        "policy_label": "close_spacing_matched_source3_policy_synthesis",
        "family_count": len(family_rows),
        "claim_count": len(claim_rows),
        "queue_complete": claim_ready["matched_source3_queue_complete"],
        "close14_truth_geometry_fraction": close14["truth_geometry_fraction"],
        "close50_truth_geometry_fraction": close50["truth_geometry_fraction"],
        "close14_all_truth_strong": claim_ready["close14_matched_txrx40_truth_result"],
        "close50_replicated_wrong_branch": claim_ready["close50_reciprocal_txrx45_wrong_branch"],
        "guarded_acquisition_geometry_contrast_ready": claim_ready["guarded_acquisition_geometry_contrast"],
        "spacing_only_causal_generalization_ready": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc_handoff": False,
        "ready_for_neural_network_training": False,
        "gpu_priority": "none",
        "recommended_next_local_mode": "cpu_manuscript_policy_or_field_collection_packet",
        "decision": (
            "The completed matched-source3 queue supports a guarded acquisition/geometry-aware "
            "contrast: close14 source3 Tx/Rx40 is exact and strong across all six rows, while "
            "close50 source3 Tx/Rx45 repeatedly selects x=299 mm, z=90 mm, r=7.5 mm instead "
            "of the truth x=300 mm, z=90 mm, r=8 mm. Do not launch a broad GPU queue from "
            "this result; write it as a controlled identifiability contrast with explicit caveats."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "paper_guarded_matched_source3_contrast",
            "ready": summary["guarded_acquisition_geometry_contrast_ready"],
            "allowed_use": "paper-facing matched-control table with caveats",
            "blocked_use": "spacing-only causal proof",
            "evidence": "close14 all truth; close50 repeated wrong branch",
        },
        {
            "gate_key": "spacing_only_causal_claim",
            "ready": summary["spacing_only_causal_generalization_ready"],
            "allowed_use": "none",
            "blocked_use": "claim spacing alone controls source3 outcome",
            "evidence": "absolute x-position and branch-lock behavior remain part of the geometry",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad local GPU close-spacing sweep",
            "evidence": "matched queue is complete; no broad GPU hypothesis is defined",
        },
        {
            "gate_key": "field_or_3d_handoff",
            "ready": summary["ready_for_field_fwi"] or summary["ready_for_3d_hpc_handoff"],
            "allowed_use": "none from this synthetic matched-control result",
            "blocked_use": "field FWI, heavy field GPU, or field 3D/HPC",
            "evidence": "field controls remain separate from synthetic trackers",
        },
    ]


def plot_synthesis(family_rows: list[dict], claim_rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["family_label"].replace(" ", "\n") for row in family_rows]
    truth_fraction = [safe_float(row["truth_geometry_fraction"], 0.0) for row in family_rows]
    mean_margin = [safe_float(row["radius_margin_abs_mean"], 0.0) for row in family_rows]
    claim_labels = [row["claim_key"] for row in claim_rows]
    claim_ready = [1 if row["ready"] else 0 for row in claim_rows]

    fig, axes = plt.subplots(1, 3, figsize=(16.0, 5.2), constrained_layout=True)
    x = np.arange(len(family_rows))
    axes[0].bar(x, truth_fraction, color=["#59a14f", "#e15759"], edgecolor="#333333", linewidth=0.5)
    axes[0].set_xticks(x, labels, fontsize=8)
    axes[0].set_ylim(0.0, 1.08)
    axes[0].set_ylabel("truth geometry fraction")
    axes[0].set_title("Matched source3 exactness")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(x, mean_margin, color=["#4e79a7", "#f28e2b"], edgecolor="#333333", linewidth=0.5)
    axes[1].set_xticks(x, labels, fontsize=8)
    axes[1].set_ylabel("mean radius margin abs")
    axes[1].set_title("Radius-confidence separation")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.03,
        0.95,
        f"close14 truth: {summary['close14_truth_geometry_fraction']:.3g}\n"
        f"close50 truth: {summary['close50_truth_geometry_fraction']:.3g}\n"
        f"GPU priority: {summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )

    axes[2].bar(
        range(len(claim_labels)),
        claim_ready,
        color=["#59a14f" if ready else "#e15759" for ready in claim_ready],
    )
    axes[2].set_xticks(range(len(claim_labels)), [label.replace("_", "\n") for label in claim_labels], fontsize=6.5)
    axes[2].set_yticks([0, 1], ["blocked", "ready"])
    axes[2].set_ylim(0.0, 1.2)
    axes[2].set_title("Claim gates")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle("Close-Spacing Matched Source3 Policy Synthesis", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close_spacing_matched_source3_policy_synthesis.png`",
                "",
                "This CPU-only figure synthesizes the completed close14 Tx/Rx40 and",
                "close50 Tx/Rx45 matched source3 probe aggregates.",
                "",
                f"Queue complete: `{summary['queue_complete']}`.",
                f"Close14 truth-geometry fraction: `{summary['close14_truth_geometry_fraction']}`.",
                f"Close50 truth-geometry fraction: `{summary['close50_truth_geometry_fraction']}`.",
                f"Guarded acquisition/geometry contrast ready: `{summary['guarded_acquisition_geometry_contrast_ready']}`.",
                f"Spacing-only causal generalization ready: `{summary['spacing_only_causal_generalization_ready']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This synthesis reads saved synthetic 2D summaries. It does not launch",
                "FDTD/FWI, GPU kernels, detector-seeded FWI, field FWI, 3D/HPC work,",
                "or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--close14-aggregate", default=DEFAULT_CLOSE14_AGGREGATE)
    parser.add_argument("--close50-aggregate", default=DEFAULT_CLOSE50_AGGREGATE)
    parser.add_argument("--queue-summary", default=DEFAULT_QUEUE_SUMMARY)
    parser.add_argument("--confound-summary", default=DEFAULT_CONFOUND_SUMMARY)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close_spacing_matched_source3_policy_synthesis")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    close14_aggregate = read_json(Path(args.close14_aggregate))
    close50_aggregate = read_json(Path(args.close50_aggregate))
    queue_summary = read_json(Path(args.queue_summary))
    confound_summary = read_json(Path(args.confound_summary))

    family_rows = build_family_rows(close14_aggregate, close50_aggregate)
    claim_rows = build_claim_rows(family_rows, queue_summary, confound_summary)
    summary = synthesize_policy(family_rows, claim_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    family_csv = data_dir / "close_spacing_matched_source3_family_rows.csv"
    claims_csv = data_dir / "close_spacing_matched_source3_claim_rows.csv"
    gates_csv = data_dir / "close_spacing_matched_source3_gate_rows.csv"
    summary_json = data_dir / "close_spacing_matched_source3_policy_summary.json"
    figure_path = figures_dir / "close_spacing_matched_source3_policy_synthesis.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(family_csv, [json_safe(row) for row in family_rows])
    write_csv(claims_csv, [json_safe(row) for row in claim_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_synthesis(family_rows, claim_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    summary["paths"] = {
        "family_csv": str(family_csv),
        "claims_csv": str(claims_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
        "figure_notes": str(figure_notes),
        "close14_aggregate": args.close14_aggregate,
        "close50_aggregate": args.close50_aggregate,
        "queue_summary": args.queue_summary,
        "confound_summary": args.confound_summary,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close_spacing_matched_source3_policy_synthesis",
        {
            "summary_json": str(summary_json),
            "family_csv": str(family_csv),
            "claims_csv": str(claims_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
