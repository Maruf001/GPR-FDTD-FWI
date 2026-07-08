#!/usr/bin/env python3
"""Create a publication-facing synthetic 2D figure and claim-boundary bundle."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EXPERIMENT_ROOT = "outputs/experiments"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_first_csv_row(path: Path) -> dict:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return rows[0] if rows else {}


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def figure_status(validation: dict) -> str:
    nonwhite = safe_float(validation.get("nonwhite_fraction"))
    dynamic = safe_float(validation.get("dynamic_range"))
    if math.isfinite(nonwhite) and nonwhite > 0.02 and math.isfinite(dynamic) and dynamic > 10:
        return "figure_validated"
    return "figure_needs_review"


def _metric_string(parts: list[str]) -> str:
    return "; ".join(part for part in parts if part)


def build_figure_rows(root: Path) -> list[dict]:
    resolution = read_json(root / "1239_coordinate_resolution_policy_synthesis/data/coordinate_resolution_policy_summary.json")
    weak = read_json(
        root
        / "1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259/data/weak_exact_secondary_confirmation_audit_summary.json"
    )
    close50 = read_json(root / "1275_close50_linear_sub30_bracket_policy/data/close50_linear_sub30_bracket_summary.json")
    target0 = read_json(root / "1276_target0_exception_closure_policy/data/target0_exception_closure_summary.json")
    modern = read_json(root / "1277_modern_ringdown050_exception_status/data/modern_ringdown050_exception_status_summary.json")
    resolution_map = read_json(
        root / "1307_synthetic_2d_resolution_claim_map_current/data/synthetic_2d_resolution_claim_map_summary.json"
    )
    legacy_close50 = read_json(
        root
        / "1317_close50_legacy_270_280_policy_audit_post_28p75_seed13_replicate/data/close50_legacy_policy_audit_summary.json"
    )
    target1_surface = read_json(
        root
        / "1312_target1_acquisition_confidence_surface/data/target1_acquisition_confidence_surface_summary.json"
    )
    target1_exception = read_json(
        root
        / "1314_target1_source_density_exception_map/data/target1_source_density_exception_map_summary.json"
    )

    specs = [
        {
            "figure_key": "current_resolution_claim_map",
            "source_run": "1307_synthetic_2d_resolution_claim_map_current",
            "figure_path": resolution_map["paths"]["figure"],
            "validation_csv": resolution_map["paths"]["figure_validation_csv"],
            "paper_use": "Current manuscript-facing synthetic 2D resolution claim map.",
            "allowed_claim": (
                "Use the current map to separate physical non-overlap guardrails, "
                "overlap stress tests, objective-uniqueness limits, and seed-frequency caveats."
            ),
            "prohibited_claim": (
                "Do not present the synthetic map as a universal rebar resolution law "
                "or as a reason for a broad GPU sweep."
            ),
            "status_label": "paper_ready_current_policy_figure",
            "support_metric": _metric_string([
                f"rows={resolution_map['row_count']}",
                f"nonoverlap={resolution_map['physical_nonoverlap_guardrail_mm']} mm",
                f"close14_near_ties={resolution_map['target2_close14_near_tie_rows_at_0p5']}",
                f"close50_clean_seeds={resolution_map['target2_close50_strict_clean_seed_count']}/"
                f"{resolution_map['target2_close50_seed_count']}",
                f"gpu={resolution_map['gpu_priority']}",
            ]),
            "strength_score": 0.88,
            "risk_score": 0.35,
        },
        {
            "figure_key": "resolution_envelope",
            "source_run": "1239_coordinate_resolution_policy_synthesis",
            "figure_path": resolution["paths"]["figure"],
            "validation_csv": resolution["paths"]["figure_validation_csv"],
            "paper_use": "Acquisition-aware close-spacing resolution envelope.",
            "allowed_claim": (
                "Clean replicated spacing depends on Tx/Rx offset; 35 mm is clean "
                "to close30, 45 mm is clean through close14 in the tested branch."
            ),
            "prohibited_claim": (
                "Do not claim a universal rebar resolution limit independent of "
                "acquisition geometry or objective policy."
            ),
            "status_label": "paper_ready_policy_figure",
            "support_metric": _metric_string([
                f"groups={resolution['group_count']}",
                f"clean={resolution['clean_group_count']}",
                f"35mm_clean_limit={resolution['standard_35mm_closest_clean_spacing_mm']} mm",
                f"45mm_clean_limit={resolution['extended_45mm_closest_clean_spacing_mm']} mm",
            ]),
            "strength_score": float(resolution["clean_group_count"]) / max(1.0, float(resolution["group_count"])),
            "risk_score": 0.30,
        },
        {
            "figure_key": "weak_exact_secondary_confirmation",
            "source_run": "1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259",
            "figure_path": weak["paths"]["figure"],
            "validation_csv": weak["paths"]["figure_validation_csv"],
            "paper_use": "Separate point recovery from base-margin confidence.",
            "allowed_claim": (
                "Diagnostic objectives confirm many base-weak exact recoveries "
                "without replacing the canonical base gate."
            ),
            "prohibited_claim": "Do not replace the production base confidence gate with diagnostic objectives.",
            "status_label": "paper_ready_policy_figure",
            "support_metric": _metric_string([
                f"weak_exact={weak['weak_exact_row_count']}",
                f"target2_full={weak['full_confirmation_targets']}",
                f"near={weak['near_confirmation_targets']}",
            ]),
            "strength_score": 0.80,
            "risk_score": 0.45,
        },
        {
            "figure_key": "target1_acquisition_confidence_surface",
            "source_run": "1312_target1_acquisition_confidence_surface",
            "figure_path": target1_surface["paths"]["figure"],
            "validation_csv": target1_surface["paths"]["figure_validation_csv"],
            "paper_use": "Target1 acquisition-confidence and source-count behavior.",
            "allowed_claim": (
                "Target1 exact geometry is stable in the canonical archive, while "
                "base confidence is acquisition-sensitive and source-density "
                "escalation is nonmonotonic."
            ),
            "prohibited_claim": (
                "Do not present source-count escalation as a monotonic target1 "
                "rescue rule or launch a broad target1 GPU sweep from this table."
            ),
            "status_label": "paper_ready_target1_policy_figure",
            "support_metric": _metric_string([
                f"rows={target1_surface['target1_canonical_row_count']}",
                f"exact={target1_surface['target1_exact_geometry_count']}",
                f"weak_exact={target1_surface['target1_base_weak_exact_count']}",
                f"late_high={target1_surface['target1_late_high_accepted_count']}/"
                f"{target1_surface['target1_late_high_truth_count']}",
                f"lower_best={target1_surface['source_density_lower_count_best_count']}",
                f"terminal11_worse={target1_surface['source_density_terminal_11_worse_count']}/"
                f"{target1_surface['source_density_terminal_11_count']}",
                f"gpu={target1_surface['gpu_priority']}",
            ]),
            "strength_score": float(target1_surface["target1_exact_geometry_count"]) / max(
                1.0, float(target1_surface["target1_canonical_row_count"])
            ),
            "risk_score": 0.42,
        },
        {
            "figure_key": "target1_source_density_exception_map",
            "source_run": "1314_target1_source_density_exception_map",
            "figure_path": target1_exception["paths"]["figure"],
            "validation_csv": target1_exception["paths"]["figure_validation_csv"],
            "paper_use": "Target1 source-density exception closure and no-GPU queue.",
            "allowed_claim": (
                "Use this as the current target1 source-density closure: zero "
                "modern exceptions, one legacy ringdown025 caveat, and no target1 "
                "source-count GPU rerun under the current hypothesis."
            ),
            "prohibited_claim": (
                "Do not reopen target1 source-density GPU work without a new "
                "objective definition, geometry, or acquisition hypothesis."
            ),
            "status_label": "paper_ready_target1_queue_figure",
            "support_metric": _metric_string([
                f"series={target1_exception['source_density_series_count']}",
                f"modern_exceptions={target1_exception['modern_exception_series_count']}",
                f"legacy_exceptions={target1_exception['legacy_exception_series_count']}",
                f"terminal11_worse={target1_exception['terminal_11_worse_count']}/"
                f"{target1_exception['terminal_11_series_count']}",
                f"gpu={target1_exception['gpu_priority']}",
            ]),
            "strength_score": 1.0
            if int(target1_exception["modern_exception_series_count"]) == 0
            and target1_exception["gpu_priority"] == "none"
            else 0.2,
            "risk_score": 0.25,
        },
        {
            "figure_key": "close50_sub30_boundary",
            "source_run": "1275_close50_linear_sub30_bracket_policy",
            "figure_path": close50["paths"]["figure"],
            "validation_csv": close50["paths"]["figure_validation_csv"],
            "paper_use": "Close50 sub-30 receiver-geometry boundary caveat.",
            "allowed_claim": (
                "Sub-30 linear samples are exact and strong but not strict-clean "
                "because seed13 remains x-ambiguous; keep nearest-sampled 30 mm."
            ),
            "prohibited_claim": "Do not report sub-30 linear receiver rows as clean replicated thresholds.",
            "status_label": "paper_ready_caveat_figure",
            "support_metric": _metric_string([
                f"tested_offsets={close50['tested_offsets_mm']} mm",
                f"strong_rows={close50['strong_confidence_row_count']}",
                f"x_ambiguous={close50['x_ambiguity_row_count']}",
            ]),
            "strength_score": 1.0 - float(close50["x_ambiguity_row_count"]) / max(
                1.0, float(close50["sub30_confidence_row_count"])
            ),
            "risk_score": 0.55,
        },
        {
            "figure_key": "close50_legacy_midpoint_refresh",
            "source_run": "1317_close50_legacy_270_280_policy_audit_post_28p75_seed13_replicate",
            "figure_path": legacy_close50["paths"]["figure"],
            "validation_csv": legacy_close50["paths"]["figure_validation_csv"],
            "paper_use": "Replicated-midpoint refresh of the old close50 270/280 branch.",
            "allowed_claim": (
                "The old close50 270/280 Tx/Rx 40 branch is target2-only and clean there; "
                "the current branch-specific threshold is replicated non-clean at 28.75 mm "
                "and clean at 30 mm and above under the tested evidence."
            ),
            "prohibited_claim": (
                "Do not repeat the old Tx/Rx 40 branch or treat it as an all-target "
                "resolution result."
            ),
            "status_label": "paper_ready_legacy_refresh_figure",
            "support_metric": _metric_string([
                f"first_clean={legacy_close50['first_clean_tx_rx_offset_mm']} mm",
                f"nonclean={legacy_close50['non_clean_tx_rx_offsets_mm']} mm",
                f"clean={legacy_close50['clean_tx_rx_offsets_mm']} mm",
                f"replicated_midpoint={legacy_close50.get('replicated_nonclean_midpoint_tx_rx_offsets_mm', '')} mm",
                f"midpoint_rows={legacy_close50['single_seed_midpoint_rows']}",
                "gpu=none",
            ]),
            "strength_score": 0.78,
            "risk_score": 0.40,
        },
        {
            "figure_key": "target0_exception_closure",
            "source_run": "1276_target0_exception_closure_policy",
            "figure_path": target0["paths"]["figure"],
            "validation_csv": target0["paths"]["figure_validation_csv"],
            "paper_use": "Target0 weak-exact exception closure mechanism.",
            "allowed_claim": (
                "Existing source-density follow-up closes the modern target0 "
                "exception; spacing-only probes improved but remained weak."
            ),
            "prohibited_claim": "Do not launch or imply a remaining target0 GPU exception branch.",
            "status_label": "paper_ready_policy_figure",
            "support_metric": _metric_string([
                f"baseline={target0['baseline_base_margin']:.6g}",
                f"best_spacing={target0['best_spacing_base_margin']:.6g}",
                f"source_density={target0['best_overall_base_margin']:.6g}",
                f"gpu={target0['gpu_priority']}",
            ]),
            "strength_score": min(1.0, float(target0["best_overall_base_margin"]) / float(target0["cutoff"])),
            "risk_score": 0.25,
        },
        {
            "figure_key": "modern_ringdown050_gpu_queue",
            "source_run": "1277_modern_ringdown050_exception_status",
            "figure_path": modern["paths"]["figure"],
            "validation_csv": modern["paths"]["figure_validation_csv"],
            "paper_use": "Current synthetic GPU-priority queue status.",
            "allowed_claim": "No modern ringdown050 weak-exact exception remains open.",
            "prohibited_claim": "Do not use the legacy ringdown025 caveat as a modern ringdown050 GPU priority.",
            "status_label": "paper_ready_queue_figure",
            "support_metric": _metric_string([
                f"modern_open={modern['modern_ringdown050_open_count']}",
                f"modern_closed={modern['modern_ringdown050_closed_count']}",
                f"legacy={modern['legacy_exception_count']}",
                f"gpu={modern['gpu_priority']}",
            ]),
            "strength_score": 1.0 if int(modern["modern_ringdown050_open_count"]) == 0 else 0.0,
            "risk_score": 0.20,
        },
    ]

    rows: list[dict] = []
    for spec in specs:
        validation = read_first_csv_row(spec["validation_csv"])
        rows.append({
            **spec,
            "figure_validation_status": figure_status(validation),
            "figure_nonwhite_fraction": safe_float(validation.get("nonwhite_fraction")),
            "figure_dynamic_range": safe_float(validation.get("dynamic_range")),
            "figure_width": safe_float(validation.get("width")),
            "figure_height": safe_float(validation.get("height")),
        })
    return rows


def build_claim_boundary_rows() -> list[dict]:
    return [
        {
            "claim_area": "resolution_limit",
            "allowed_claim": (
                "Report acquisition- and objective-specific clean/interval/mixed "
                "resolution regions, using the current resolution-claim map."
            ),
            "not_allowed": (
                "Do not present a universal physical rebar spacing limit from "
                "these synthetic sweeps."
            ),
        },
        {
            "claim_area": "close50_legacy_branch",
            "allowed_claim": (
                "Use the refreshed 270/280 audit to say the old close50 Tx/Rx 40 "
                "target2 branch is resolved by later midpoint, replicated 28.75 mm "
                "non-clean, and replicated 30 mm clean-threshold evidence."
            ),
            "not_allowed": (
                "Do not repeat the old Tx/Rx 40 branch or present it as an all-target "
                "resolution result."
            ),
        },
        {
            "claim_area": "confidence_policy",
            "allowed_claim": "Separate truth selection, strict base-margin confidence, and secondary diagnostic confirmation.",
            "not_allowed": "Do not call weak-exact rows fully accepted under the canonical base policy.",
        },
        {
            "claim_area": "reporting_tiers",
            "allowed_claim": (
                "Report exact-strong, strict location-clean, zero-width objective "
                "near-tie, and geometry-ambiguous near-tie as separate tiers."
            ),
            "not_allowed": (
                "Do not collapse exact-strong rows into paper-clean location "
                "claims without checking geometry ambiguity widths."
            ),
        },
        {
            "claim_area": "objective_uniqueness",
            "allowed_claim": (
                "Zero-width objective near-ties occur for targets 1 and 2; "
                "they limit objective-uniqueness wording but not "
                "location-clean geometry wording."
            ),
            "not_allowed": (
                "Do not describe zero-width near-tie rows as uniquely isolated "
                "objective basins."
            ),
        },
        {
            "claim_area": "target_specificity",
            "allowed_claim": (
                "Geometry ambiguity in exact-strong archive rows is "
                "target-specific to target2; target2 strict location-clean "
                "fraction is 0.921348 in the current claim-tier table."
            ),
            "not_allowed": (
                "Do not imply target0, target1, and target2 share the same "
                "ambiguity profile."
            ),
        },
        {
            "claim_area": "target1_acquisition_confidence",
            "allowed_claim": (
                "Use target1 as an example of stable exact geometry with "
                "acquisition-sensitive confidence and nonmonotonic source-density "
                "behavior."
            ),
            "not_allowed": (
                "Do not claim source-count escalation is a general target1 rescue "
                "rule or launch target1 reruns without a new hypothesis."
            ),
        },
        {
            "claim_area": "target2_close14_objective_limit",
            "allowed_claim": (
                "For target2 close14 source5 / Tx/Rx=45 mm, the three-seed "
                "probe selected truth with strong radius confidence in 6 / 6 "
                "rows, but the +1 mm x competitor remained inside the 0.5x "
                "ambiguity gate in 6 / 6 rows."
            ),
            "not_allowed": (
                "Do not describe this branch as clean lateral resolution or "
                "as an objective-unique inversion result."
            ),
        },
        {
            "claim_area": "target2_close50_linear29p5_seed_frequency",
            "allowed_claim": (
                "For target2 close50 linear receiver Tx/Rx=29.5 mm, the "
                "three-seed policy selected the true geometry with strong "
                "radius confidence in 6 / 6 rows. Strict-clean support is "
                "2 / 3 seeds; seed13 remains an x-ambiguity caveat."
            ),
            "not_allowed": (
                "Do not promote 29.5 mm to a clean replicated sub-30 mm "
                "threshold; keep the nearest-sampled 30 mm result as the "
                "paper-safe clean threshold."
            ),
        },
        {
            "claim_area": "gpu_next_step",
            "allowed_claim": (
                "Current synthetic policy has no open modern ringdown050, "
                "close14 objective-limit, close50 seed-frequency, or target1 "
                "source-density GPU-priority exception."
            ),
            "not_allowed": "Do not launch broad GPU sweeps without a new objective, geometry, or acquisition question.",
        },
        {
            "claim_area": "field_separation",
            "allowed_claim": "Keep synthetic policy claims separate from local GSSI field QC claims.",
            "not_allowed": "Do not use field QC to change known-truth synthetic confidence labels.",
        },
    ]


def summarize_bundle(rows: list[dict], claim_rows: list[dict]) -> dict:
    valid_figures = sum(1 for row in rows if row["figure_validation_status"] == "figure_validated")
    open_gpu_priority = any("gpu=none" not in str(row.get("support_metric", "")) for row in rows if "gpu" in str(row.get("support_metric", "")))
    target1_current = {
        "target1_acquisition_confidence_surface",
        "target1_source_density_exception_map",
    }.issubset({str(row.get("figure_key", "")) for row in rows})
    detailed_claims = {
        "reporting_tiers",
        "objective_uniqueness",
        "target_specificity",
        "target2_close14_objective_limit",
        "target2_close50_linear29p5_seed_frequency",
    }.issubset({str(row.get("claim_area", "")) for row in claim_rows})
    label = "synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none"
    if target1_current:
        label = "synthetic_2d_publication_bundle_current_resolution_target1_ready_gpu_priority_none"
    if target1_current and detailed_claims:
        label = "synthetic_2d_publication_bundle_current_resolution_target1_claims_ready_gpu_priority_none"
    return {
        "policy_label": label,
        "figure_count": len(rows),
        "validated_figure_count": valid_figures,
        "claim_boundary_count": len(claim_rows),
        "target1_current_policy_figures_included": target1_current,
        "detailed_claim_boundaries_included": detailed_claims,
        "gpu_priority": "none",
        "open_gpu_priority_detected": bool(open_gpu_priority),
        "ready_for_manuscript_draft": bool(valid_figures == len(rows) and not open_gpu_priority),
        "decision": (
            "Use the listed synthetic 2D figures as publication-facing policy "
            "figures with the claim boundaries in the CSV. Do not launch a GPU "
            "run from this bundle; define a new objective, geometry, or "
            "acquisition question first."
        ),
    }


def plot_bundle(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["figure_key"].replace("_", "\n") for row in rows]
    x = np.arange(len(rows))
    strength = np.asarray([safe_float(row["strength_score"], 0.0) for row in rows], dtype=np.float64)
    risk = np.asarray([safe_float(row["risk_score"], 0.0) for row in rows], dtype=np.float64)
    nonwhite = np.asarray([safe_float(row["figure_nonwhite_fraction"], 0.0) for row in rows], dtype=np.float64)
    dynamic = np.asarray([safe_float(row["figure_dynamic_range"], 0.0) / 255.0 for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 3, figsize=(16.0, 5.2), constrained_layout=True)
    axes[0].bar(x - 0.18, strength, width=0.36, color="#2f9d55", label="support")
    axes[0].bar(x + 0.18, risk, width=0.36, color="#c7302b", label="claim risk")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_title("Synthetic 2D figure claim posture")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].bar(x - 0.18, nonwhite, width=0.36, color="#4c78a8", label="nonwhite fraction")
    axes[1].bar(x + 0.18, dynamic, width=0.36, color="#f58518", label="dynamic range / 255")
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0.0, 1.05)
    axes[1].set_title("Existing figure validation")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[1].legend(frameon=False, fontsize=8)

    ready = [1.0 if row["figure_validation_status"] == "figure_validated" else 0.0 for row in rows]
    axes[2].bar(x, ready, color="#6b6b6b", width=0.55)
    axes[2].set_xticks(x, labels)
    axes[2].set_ylim(0.0, 1.05)
    axes[2].set_title("Bundle readiness")
    axes[2].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Synthetic 2D publication bundle: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(
    path: Path,
    summary: dict,
    rows_csv: Path,
    claims_csv: Path,
    validation_csv: Path,
) -> None:
    """Write notes for the synthetic 2D publication bundle figure."""
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `synthetic_2d_publication_figure_bundle.png`",
                "",
                "This summary figure audits the current synthetic 2D publication-facing",
                "figures. It combines claim-support score, claim-risk score, image",
                "validation status, and readiness for manuscript planning.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Validated figures: `{summary['validated_figure_count']}` of `{summary['figure_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "The plotted bars are an index over existing evidence, not a new FDTD",
                "or FWI result. Claim boundaries and source figure paths are stored in",
                f"`{rows_csv.name}` and `{claims_csv.name}`. Image-validation metrics",
                f"for this bundle figure are stored in `{validation_csv.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--run-name", default="synthetic_2d_publication_figure_bundle")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    root = Path(args.experiment_root)
    rows = build_figure_rows(root)
    claim_rows = build_claim_boundary_rows()
    summary = summarize_bundle(rows, claim_rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_2d_publication_figure_rows.csv"
    claims_csv = data_dir / "synthetic_2d_publication_claim_boundaries.csv"
    summary_json = data_dir / "synthetic_2d_publication_figure_bundle_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_bundle(rows, summary, figures_dir / "synthetic_2d_publication_figure_bundle.png"))
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(claims_csv, [json_safe(row) for row in claim_rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv, claims_csv, validation_csv)
    output_summary = {
        **summary,
        "paths": {
            "figure_rows_csv": str(rows_csv),
            "claim_boundaries_csv": str(claims_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_2d_publication_figure_bundle",
        {
            "summary_json": str(summary_json),
            "figure_rows_csv": str(rows_csv),
            "claim_boundaries_csv": str(claims_csv),
            "figure_validation_csv": str(validation_csv),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
