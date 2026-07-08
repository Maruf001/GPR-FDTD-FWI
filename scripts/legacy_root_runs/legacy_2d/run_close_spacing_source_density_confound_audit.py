#!/usr/bin/env python3
"""Audit acquisition confounds in close14/close50 source-density comparisons."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
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
from run_local_2d_detector_rank_budget_diagnostic import read_json, safe_float, safe_int  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_CROSS_SPACING_SOURCE_ROWS = (
    "outputs/summary_tables/110_close_spacing_source_density_cross_spacing_synthesis/"
    "data/close_spacing_source_density_cross_spacing_source_rows.csv"
)
DEFAULT_CROSS_SPACING_SUMMARY = (
    "outputs/summary_tables/110_close_spacing_source_density_cross_spacing_synthesis/"
    "data/close_spacing_source_density_cross_spacing_summary.json"
)
DEFAULT_CLOSE50_SOURCE3_RUNS = (
    "274_coordinate_optimizer_close50_seed34_sources3_txrx40_objectives,"
    "1344_coordinate_optimizer_close50_seed13_sources3_txrx40_objectives,"
    "1345_coordinate_optimizer_close50_seed21_sources3_txrx40_objectives"
)
DEFAULT_CLOSE14_SOURCE3_RUNS = (
    "336_coordinate_optimizer_close14_seed34_sources3_txrx45_objectives,"
    "1346_coordinate_optimizer_close14_seed13_sources3_txrx45_objectives,"
    "1347_coordinate_optimizer_close14_seed21_sources3_txrx45_objectives"
)


def read_csv_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def boolish(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def seed_from_text(text: object) -> int:
    match = re.search(r"seed(\d+)", str(text))
    return int(match.group(1)) if match else -1


def fmt_values(values: list[object]) -> str:
    unique = []
    for value in values:
        if isinstance(value, float) and math.isfinite(value):
            text = f"{value:g}"
        else:
            text = str(value)
        if text not in unique:
            unique.append(text)
    return ",".join(unique)


def replication_signature(summary: dict) -> str:
    parts = []
    for case in summary.get("replication_cases", []):
        parts.append(
            "|".join(
                [
                    str(case.get("label", "")),
                    f"freq={safe_float(case.get('frequency_scale'), math.nan):g}",
                    f"shift_ps={safe_float(case.get('time_shift_ps'), math.nan):g}",
                    f"amp={safe_float(case.get('amplitude_scale'), math.nan):g}",
                    f"noise={safe_float(case.get('noise_fraction'), math.nan):g}",
                ]
            )
        )
    return ";".join(parts)


def run_descriptor(experiment_root: Path, run_name: str, family: str) -> dict:
    summary = read_json(experiment_root / run_name / "data/multi_rebar_coordinate_optimizer_summary.json")
    true_x = [safe_float(value) for value in summary.get("true_x_values_mm", [])]
    true_z = [safe_float(value) for value in summary.get("true_z_values_mm", [])]
    truth_r = [safe_float(value) for value in summary.get("truth_radius_values_mm", [])]
    return {
        "family": family,
        "run_name": run_name,
        "seed": seed_from_text(run_name),
        "source_count": safe_int(summary.get("sources")),
        "tx_rx_offset_mm": safe_float(summary.get("tx_rx_offset_mm")),
        "receiver_sampling": summary.get("receiver_sampling", ""),
        "backend": summary.get("backend", ""),
        "target0_x_mm": true_x[0] if len(true_x) > 0 else math.nan,
        "target1_x_mm": true_x[1] if len(true_x) > 1 else math.nan,
        "target2_x_mm": true_x[2] if len(true_x) > 2 else math.nan,
        "target0_target1_gap_mm": abs(true_x[1] - true_x[0]) if len(true_x) > 1 else math.nan,
        "target1_target2_gap_mm": abs(true_x[2] - true_x[1]) if len(true_x) > 2 else math.nan,
        "true_z_values_mm": ",".join(f"{value:g}" for value in true_z),
        "truth_radius_values_mm": ",".join(f"{value:g}" for value in truth_r),
        "replication_signature": replication_signature(summary),
    }


def load_run_descriptors(experiment_root: Path, close50_runs: list[str], close14_runs: list[str]) -> list[dict]:
    rows = []
    for run_name in close50_runs:
        rows.append(run_descriptor(experiment_root, run_name, "close50"))
    for run_name in close14_runs:
        rows.append(run_descriptor(experiment_root, run_name, "close14"))
    return rows


def family_summary(run_rows: list[dict], source_rows: list[dict], family: str) -> dict:
    runs = [row for row in run_rows if row["family"] == family]
    source_by_count = {
        safe_int(row.get("source_count")): row for row in source_rows if row.get("family") == family
    }
    return {
        "family": family,
        "source3_seed_values": fmt_values(sorted(row["seed"] for row in runs)),
        "source3_source_count": fmt_values([row["source_count"] for row in runs]),
        "source3_tx_rx_offset_mm": fmt_values([row["tx_rx_offset_mm"] for row in runs]),
        "source3_receiver_sampling": fmt_values([row["receiver_sampling"] or "missing" for row in runs]),
        "source3_backend": fmt_values([row["backend"] for row in runs]),
        "target0_target1_gap_mm": fmt_values([row["target0_target1_gap_mm"] for row in runs]),
        "target1_target2_gap_mm": fmt_values([row["target1_target2_gap_mm"] for row in runs]),
        "target2_x_mm": fmt_values([row["target2_x_mm"] for row in runs]),
        "true_z_values_mm": fmt_values([row["true_z_values_mm"] for row in runs]),
        "truth_radius_values_mm": fmt_values([row["truth_radius_values_mm"] for row in runs]),
        "source3_replication_signature": fmt_values([row["replication_signature"] for row in runs]),
        "source3_truth_fraction": safe_float(source_by_count.get(3, {}).get("truth_geometry_fraction")),
        "source3_strong_fraction": safe_float(source_by_count.get(3, {}).get("strong_fraction")),
        "source3_weak_fraction": safe_float(source_by_count.get(3, {}).get("weak_fraction")),
        "source3_evidence_role": source_by_count.get(3, {}).get("archive_evidence_role", ""),
        "source4_evidence_role": source_by_count.get(4, {}).get("archive_evidence_role", ""),
        "source5_evidence_scope": source_by_count.get(5, {}).get("archive_evidence_scope", ""),
        "source5_evidence_role": source_by_count.get(5, {}).get("archive_evidence_role", ""),
    }


def factor_row(
    factor_key: str,
    factor_type: str,
    close50_value: object,
    close14_value: object,
    matched: bool,
    impact: str,
    action: str,
) -> dict:
    return {
        "factor_key": factor_key,
        "factor_type": factor_type,
        "close50_value": close50_value,
        "close14_value": close14_value,
        "matched_or_intended": matched,
        "manuscript_impact": impact,
        "recommended_action": action,
    }


def build_factor_rows(close50: dict, close14: dict) -> list[dict]:
    return [
        factor_row(
            "source3_seed_values",
            "matched_control",
            close50["source3_seed_values"],
            close14["source3_seed_values"],
            close50["source3_seed_values"] == close14["source3_seed_values"],
            "supports three-seed comparison for the source3 contrast",
            "use as matched control",
        ),
        factor_row(
            "source3_replication_cases",
            "matched_control",
            close50["source3_replication_signature"],
            close14["source3_replication_signature"],
            close50["source3_replication_signature"] == close14["source3_replication_signature"],
            "supports nominal/source-mismatch pairing across families",
            "use as matched control",
        ),
        factor_row(
            "source3_source_count",
            "matched_control",
            close50["source3_source_count"],
            close14["source3_source_count"],
            close50["source3_source_count"] == close14["source3_source_count"],
            "source count is matched for the cross-spacing source3 contrast",
            "use as matched control",
        ),
        factor_row(
            "target_depths_and_radii",
            "matched_control",
            f"z={close50['true_z_values_mm']}; r={close50['truth_radius_values_mm']}",
            f"z={close14['true_z_values_mm']}; r={close14['truth_radius_values_mm']}",
            close50["true_z_values_mm"] == close14["true_z_values_mm"]
            and close50["truth_radius_values_mm"] == close14["truth_radius_values_mm"],
            "depth and radius are not the reason for the source3 contrast",
            "use as matched control",
        ),
        factor_row(
            "target0_target1_gap_mm",
            "matched_control",
            close50["target0_target1_gap_mm"],
            close14["target0_target1_gap_mm"],
            close50["target0_target1_gap_mm"] == close14["target0_target1_gap_mm"],
            "left-pair geometry is matched while target2 spacing changes",
            "use as matched context",
        ),
        factor_row(
            "target1_target2_gap_mm",
            "intended_spacing_axis",
            close50["target1_target2_gap_mm"],
            close14["target1_target2_gap_mm"],
            close50["target1_target2_gap_mm"] != close14["target1_target2_gap_mm"],
            "this is the intended close-spacing contrast axis, not an accidental confound",
            "state explicitly in manuscript",
        ),
        factor_row(
            "tx_rx_offset_mm",
            "acquisition_confound",
            close50["source3_tx_rx_offset_mm"],
            close14["source3_tx_rx_offset_mm"],
            close50["source3_tx_rx_offset_mm"] == close14["source3_tx_rx_offset_mm"],
            "prevents a spacing-only causal claim from the cross-family source3 contrast",
            "only run a matched Tx/Rx probe if the paper needs spacing-only causality",
        ),
        factor_row(
            "target2_absolute_x_mm",
            "geometry_confound",
            close50["target2_x_mm"],
            close14["target2_x_mm"],
            close50["target2_x_mm"] == close14["target2_x_mm"],
            "absolute target2 position differs along with the intended target1-target2 gap",
            "avoid claiming isolated spacing causality",
        ),
        factor_row(
            "receiver_sampling_metadata",
            "metadata_gap",
            close50["source3_receiver_sampling"],
            close14["source3_receiver_sampling"],
            close50["source3_receiver_sampling"] == close14["source3_receiver_sampling"],
            "older seed34 summaries lack explicit receiver_sampling even though newer runs record nearest",
            "treat as metadata caveat, not a launch trigger",
        ),
        factor_row(
            "source5_context_scope",
            "context_only",
            close50["source5_evidence_scope"],
            close14["source5_evidence_scope"],
            close50["source5_evidence_scope"] == close14["source5_evidence_scope"],
            "source5 cross-family comparison mixes nominal close50 context with close14 noise-boundary context",
            "use source5 only as within-family/context evidence",
        ),
    ]


def build_claim_rows(factor_rows: list[dict], cross_summary: dict) -> list[dict]:
    confounds = [row["factor_key"] for row in factor_rows if row["factor_type"].endswith("confound")]
    context_only = [row["factor_key"] for row in factor_rows if row["factor_type"] == "context_only"]
    metadata_gaps = [row["factor_key"] for row in factor_rows if row["factor_type"] == "metadata_gap"]
    return [
        {
            "claim_key": "close50_within_family_source_density_transition",
            "ready": boolish(cross_summary.get("close50_source3_replicated_failure"))
            and boolish(cross_summary.get("close50_source4_5_exact_recovery")),
            "allowed_wording": "close50 Tx/Rx40 shows a three-seed source-density transition from source3 failure to source4/5 exact recovery",
            "blocked_wording": "all close-spacing source3 acquisitions fail",
            "limiting_factors": "",
        },
        {
            "claim_key": "close14_source3_near_exact_context",
            "ready": boolish(cross_summary.get("close14_source3_near_exact_context")),
            "allowed_wording": "close14 Tx/Rx45 source3 is a strong near-exact three-seed context",
            "blocked_wording": "close14 reproduces the close50 source3 failure",
            "limiting_factors": "",
        },
        {
            "claim_key": "guarded_cross_spacing_source3_contrast",
            "ready": boolish(cross_summary.get("source3_spacing_dependent_contrast")),
            "allowed_wording": "saved evidence contrasts close50 Tx/Rx40 source3 failure with close14 Tx/Rx45 source3 near-exact recovery",
            "blocked_wording": "spacing alone explains the source3 outcome",
            "limiting_factors": ",".join(confounds + metadata_gaps),
        },
        {
            "claim_key": "spacing_only_causal_generalization",
            "ready": False,
            "allowed_wording": "none from current saved evidence",
            "blocked_wording": "target spacing alone controls source3 success/failure across close14 and close50",
            "limiting_factors": ",".join(confounds + metadata_gaps),
        },
        {
            "claim_key": "source5_cross_family_comparison",
            "ready": False,
            "allowed_wording": "source5 remains within-family/context evidence",
            "blocked_wording": "close14 and close50 source5 are a matched cross-family comparison",
            "limiting_factors": ",".join(context_only),
        },
        {
            "claim_key": "broad_gpu_queue",
            "ready": False,
            "allowed_wording": "none",
            "blocked_wording": "launch broad close-spacing source-density sweep",
            "limiting_factors": "current evidence is sufficient for guarded claim boundary; causal generalization needs a deliberately matched narrow probe, not a queue",
        },
        {
            "claim_key": "matched_narrow_probe_design",
            "ready": True,
            "allowed_wording": "if manuscript requires spacing-only causality, design one skip-existing matched Tx/Rx source3 probe set",
            "blocked_wording": "start broad GPU experiments",
            "limiting_factors": "candidate sets: close14 source3 Tx/Rx40 seeds 13/21/34 or close50 source3 Tx/Rx45 seeds 13/21/34",
        },
    ]


def synthesize_policy(factor_rows: list[dict], claim_rows: list[dict]) -> dict:
    counts = Counter(row["factor_type"] for row in factor_rows)
    ready_claims = [row["claim_key"] for row in claim_rows if boolish(row["ready"])]
    return {
        "policy_label": "close_spacing_source_density_confound_audit",
        "factor_count": len(factor_rows),
        "claim_count": len(claim_rows),
        "matched_control_factor_count": counts.get("matched_control", 0),
        "intended_spacing_axis_count": counts.get("intended_spacing_axis", 0),
        "acquisition_confound_count": counts.get("acquisition_confound", 0),
        "geometry_confound_count": counts.get("geometry_confound", 0),
        "metadata_gap_count": counts.get("metadata_gap", 0),
        "context_only_factor_count": counts.get("context_only", 0),
        "ready_claim_keys": ",".join(ready_claims),
        "close50_within_family_transition_ready": any(
            row["claim_key"] == "close50_within_family_source_density_transition" and boolish(row["ready"])
            for row in claim_rows
        ),
        "guarded_cross_spacing_contrast_ready": any(
            row["claim_key"] == "guarded_cross_spacing_source3_contrast" and boolish(row["ready"])
            for row in claim_rows
        ),
        "spacing_only_causal_generalization_ready": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc_handoff": False,
        "gpu_priority": "none",
        "recommended_next_local_mode": "field_controls_or_cpu_matched_probe_design",
        "decision": (
            "The saved source-density evidence is strong for the close50 within-family transition "
            "and useful as a guarded close50/close14 source3 contrast. It is not a spacing-only "
            "causal proof because Tx/Rx offset and target2 absolute position also differ, and "
            "source5 cross-family evidence is context-only. Do not launch a broad GPU queue."
        ),
    }


def gate_rows(summary: dict) -> list[dict]:
    return [
        {
            "gate_key": "within_close50_source_density_claim",
            "ready": summary["close50_within_family_transition_ready"],
            "allowed_use": "manuscript source-density transition claim for close50 Tx/Rx40",
            "blocked_use": "generalize to all close spacings",
            "evidence": "source3 fails, source4/5 exact in matched close50 three-seed evidence",
        },
        {
            "gate_key": "guarded_cross_spacing_contrast",
            "ready": summary["guarded_cross_spacing_contrast_ready"],
            "allowed_use": "guarded contrast table with explicit confounds",
            "blocked_use": "spacing-only causal wording",
            "evidence": "close14 source3 near-exact but Tx/Rx and target2 absolute x differ",
        },
        {
            "gate_key": "spacing_only_causal_generalization",
            "ready": summary["spacing_only_causal_generalization_ready"],
            "allowed_use": "none",
            "blocked_use": "claim target spacing alone controls source3 outcome",
            "evidence": "requires matched Tx/Rx/absolute-geometry probe not present in archive",
        },
        {
            "gate_key": "broad_gpu_queue",
            "ready": summary["ready_for_broad_gpu_queue"],
            "allowed_use": "none",
            "blocked_use": "broad source-density sweep",
            "evidence": "current need is claim-boundary discipline, not broad compute",
        },
    ]


def plot_audit(factor_rows: list[dict], claim_rows: list[dict], summary: dict, save_path: Path) -> str:
    factor_counts = Counter(row["factor_type"] for row in factor_rows)
    factor_labels = list(factor_counts)
    factor_values = [factor_counts[label] for label in factor_labels]
    claim_labels = [row["claim_key"] for row in claim_rows]
    claim_ready = [1 if boolish(row["ready"]) else 0 for row in claim_rows]

    fig, axes = plt.subplots(1, 2, figsize=(15.0, 5.2), constrained_layout=True)
    axes[0].bar(range(len(factor_labels)), factor_values, color="#4e79a7")
    axes[0].set_xticks(range(len(factor_labels)), [label.replace("_", "\n") for label in factor_labels], fontsize=8)
    axes[0].set_ylabel("factor count")
    axes[0].set_title("Matched controls vs confounds")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)

    axes[1].bar(
        range(len(claim_labels)),
        claim_ready,
        color=["#59a14f" if ready else "#e15759" for ready in claim_ready],
    )
    axes[1].set_xticks(range(len(claim_labels)), [label.replace("_", "\n") for label in claim_labels], fontsize=7)
    axes[1].set_yticks([0, 1], ["blocked", "ready"])
    axes[1].set_ylim(0, 1.2)
    axes[1].set_title("Claim readiness")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].text(
        0.02,
        0.95,
        f"spacing-only causal: {summary['spacing_only_causal_generalization_ready']}\n"
        f"broad GPU queue: {summary['ready_for_broad_gpu_queue']}\n"
        f"GPU priority: {summary['gpu_priority']}",
        transform=axes[1].transAxes,
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "boxstyle": "round,pad=0.35"},
    )
    fig.suptitle("Close-Spacing Source-Density Confound Audit", fontweight="bold")
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict) -> None:
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `close_spacing_source_density_confound_audit.png`",
                "",
                "This CPU-only figure audits matched controls and confounds in the",
                "close50/close14 source-density comparison.",
                "",
                f"Matched control factors: `{summary['matched_control_factor_count']}`.",
                f"Acquisition confounds: `{summary['acquisition_confound_count']}`.",
                f"Geometry confounds: `{summary['geometry_confound_count']}`.",
                f"Context-only factors: `{summary['context_only_factor_count']}`.",
                f"Spacing-only causal generalization ready: `{summary['spacing_only_causal_generalization_ready']}`.",
                f"Broad GPU queue ready: `{summary['ready_for_broad_gpu_queue']}`.",
                "",
                "Scope boundary:",
                "",
                "This audit reads saved synthetic 2D summaries. It does not run FDTD/FWI,",
                "GPU kernels, detector-seeded FWI, field FWI, 3D/HPC, or neural-network training.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default="outputs/experiments")
    parser.add_argument("--cross-spacing-source-rows", default=DEFAULT_CROSS_SPACING_SOURCE_ROWS)
    parser.add_argument("--cross-spacing-summary", default=DEFAULT_CROSS_SPACING_SUMMARY)
    parser.add_argument("--close50-source3-runs", default=DEFAULT_CLOSE50_SOURCE3_RUNS)
    parser.add_argument("--close14-source3-runs", default=DEFAULT_CLOSE14_SOURCE3_RUNS)
    parser.add_argument("--summary-root", default="outputs/summary_tables")
    parser.add_argument("--run-name", default="close_spacing_source_density_confound_audit")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    close50_runs = [part.strip() for part in args.close50_source3_runs.split(",") if part.strip()]
    close14_runs = [part.strip() for part in args.close14_source3_runs.split(",") if part.strip()]
    source_rows = read_csv_rows(Path(args.cross_spacing_source_rows))
    run_rows = load_run_descriptors(experiment_root, close50_runs, close14_runs)
    close50 = family_summary(run_rows, source_rows, "close50")
    close14 = family_summary(run_rows, source_rows, "close14")
    factor_rows = build_factor_rows(close50, close14)
    cross_summary = read_json(Path(args.cross_spacing_summary))
    claim_rows = build_claim_rows(factor_rows, cross_summary)
    summary = synthesize_policy(factor_rows, claim_rows)
    gates = gate_rows(summary)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=args.summary_root))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    family_csv = data_dir / "close_spacing_source_density_confound_family_summary.csv"
    factors_csv = data_dir / "close_spacing_source_density_confound_factors.csv"
    claims_csv = data_dir / "close_spacing_source_density_confound_claims.csv"
    gates_csv = data_dir / "close_spacing_source_density_confound_gates.csv"
    summary_json = data_dir / "close_spacing_source_density_confound_summary.json"
    figure_path = figures_dir / "close_spacing_source_density_confound_audit.png"
    validation_csv = data_dir / "figure_validation.csv"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(family_csv, [json_safe(close50), json_safe(close14)])
    write_csv(factors_csv, [json_safe(row) for row in factor_rows])
    write_csv(claims_csv, [json_safe(row) for row in claim_rows])
    write_csv(gates_csv, [json_safe(row) for row in gates])
    plot_audit(factor_rows, claim_rows, summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary)

    summary["paths"] = {
        "family_summary_csv": str(family_csv),
        "factor_csv": str(factors_csv),
        "claim_csv": str(claims_csv),
        "gates_csv": str(gates_csv),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_validation_csv": str(validation_csv),
        "figure_notes": str(figure_notes),
        "cross_spacing_source_rows": args.cross_spacing_source_rows,
        "cross_spacing_summary": args.cross_spacing_summary,
        "close50_source3_runs": close50_runs,
        "close14_source3_runs": close14_runs,
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "close_spacing_source_density_confound_audit",
        {
            "summary_json": str(summary_json),
            "factor_csv": str(factors_csv),
            "claim_csv": str(claims_csv),
            "figure": str(figure_path),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
