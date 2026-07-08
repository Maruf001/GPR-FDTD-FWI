#!/usr/bin/env python3
"""Rank candidate next synthetic 2D research questions without running GPU work."""

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
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_EXPERIMENT_ROOT = "outputs/experiments"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_optional_json(path: Path) -> dict:
    if not Path(path).exists():
        return {}
    return read_json(path)


def read_latest_publication_bundle(root: Path) -> tuple[dict, str]:
    candidates = (
        (
            "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation",
            root
            / "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation/data/"
            "synthetic_2d_publication_figure_bundle_summary.json",
        ),
        (
            "1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh",
            root
            / "1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh/data/"
            "synthetic_2d_publication_figure_bundle_summary.json",
        ),
        (
            "1318_synthetic_2d_publication_figure_bundle_post_28p75_replicated_midpoint_refresh",
            root
            / "1318_synthetic_2d_publication_figure_bundle_post_28p75_replicated_midpoint_refresh/data/"
            "synthetic_2d_publication_figure_bundle_summary.json",
        ),
        (
            "1309_synthetic_2d_publication_figure_bundle_post_resolution_map_refresh",
            root
            / "1309_synthetic_2d_publication_figure_bundle_post_resolution_map_refresh/data/"
            "synthetic_2d_publication_figure_bundle_summary.json",
        ),
        (
            "1278_synthetic_2d_publication_figure_bundle",
            root
            / "1278_synthetic_2d_publication_figure_bundle/data/"
            "synthetic_2d_publication_figure_bundle_summary.json",
        ),
    )
    for run_name, path in candidates:
        payload = read_optional_json(path)
        if payload:
            return payload, run_name
    return {}, ""


def read_latest_target1_acquisition_surface(root: Path) -> tuple[dict, str]:
    candidates = (
        (
            "1312_target1_acquisition_confidence_surface",
            root
            / "1312_target1_acquisition_confidence_surface/data/"
            "target1_acquisition_confidence_surface_summary.json",
        ),
    )
    for run_name, path in candidates:
        payload = read_optional_json(path)
        if payload:
            return payload, run_name
    return {}, ""


def read_latest_target1_source_density_exception_map(root: Path) -> tuple[dict, str]:
    candidates = (
        (
            "1314_target1_source_density_exception_map",
            root
            / "1314_target1_source_density_exception_map/data/"
            "target1_source_density_exception_map_summary.json",
        ),
    )
    for run_name, path in candidates:
        payload = read_optional_json(path)
        if payload:
            return payload, run_name
    return {}, ""


def summary_table_root(root: Path) -> Path:
    if root.name == "experiments":
        return root.parent / "summary_tables"
    return root / "summary_tables"


def read_latest_matched_source3_policy(root: Path) -> tuple[dict, str]:
    candidates = (
        (
            "121_close_spacing_matched_source3_policy_synthesis",
            summary_table_root(root)
            / "121_close_spacing_matched_source3_policy_synthesis/data/"
            "close_spacing_matched_source3_policy_summary.json",
        ),
    )
    for run_name, path in candidates:
        payload = read_optional_json(path)
        if payload:
            return payload, run_name
    return {}, ""


def candidate_rows(root: Path) -> list[dict]:
    bundle, bundle_run = read_latest_publication_bundle(root)
    target1_surface, target1_surface_run = read_latest_target1_acquisition_surface(root)
    target1_exception, target1_exception_run = read_latest_target1_source_density_exception_map(root)
    matched_source3, matched_source3_run = read_latest_matched_source3_policy(root)
    close50 = read_json(root / "1275_close50_linear_sub30_bracket_policy/data/close50_linear_sub30_bracket_summary.json")
    target0 = read_json(root / "1276_target0_exception_closure_policy/data/target0_exception_closure_summary.json")
    modern = read_json(root / "1277_modern_ringdown050_exception_status/data/modern_ringdown050_exception_status_summary.json")
    acquisition_gap = read_json(
        root
        / "1289_synthetic_objective_uniqueness_acquisition_gap_map/data/"
        "synthetic_objective_uniqueness_acquisition_gap_summary.json"
    )
    family_gap = read_json(
        root
        / "1290_synthetic_objective_uniqueness_family_gap_context/data/"
        "synthetic_objective_uniqueness_family_gap_summary.json"
    )
    threshold = read_json(
        root
        / "1291_synthetic_objective_threshold_sensitivity/data/"
        "synthetic_objective_threshold_sensitivity_summary.json"
    )
    completed_close14_probe = read_optional_json(
        root
        / "1297_synthetic_target2_close14_three_seed_probe_synthesis/data/"
        "target2_close14_three_seed_probe_summary.json"
    )
    completed_close14_claim_refresh = read_optional_json(
        root
        / "1299_synthetic_2d_publication_claim_boundary_refresh_post_close14_probe/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json"
    )
    completed_close50_policy = read_optional_json(
        root
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json"
    )
    completed_close50_claim_refresh = read_optional_json(
        root
        / "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json"
    )

    if completed_close50_claim_refresh:
        close14_rows = []
        if bundle_run.startswith(("1309_", "1318_", "1320_", "1322_")):
            close14_rows.append({
                "question_key": "synthetic_publication_bundle_current",
                "category": "completed_reporting",
                "motivation": (
                    "The synthetic paper-facing figure bundle has been refreshed "
                    "after the current resolution map and close50 270/280 legacy "
                    "midpoint audit."
                ),
                "current_evidence": (
                    f"run={bundle_run}; "
                    f"policy={bundle.get('policy_label', '')}; "
                    f"figures={bundle.get('figure_count', 0)}; "
                    f"validated={bundle.get('validated_figure_count', 0)}; "
                    f"claims={bundle.get('claim_boundary_count', 0)}; "
                    f"gpu={bundle.get('gpu_priority', '')}"
                ),
                "gpu_readiness": "no_gpu_required",
                "gpu_priority": "none",
                "research_value": 0.76,
                "evidence_gap": 0.34,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Use the refreshed synthetic paper bundle and its "
                    "claim-boundary CSV. No GPU work follows from this "
                    "completed reporting endpoint."
                ),
            })
        if target1_surface_run.startswith("1312_"):
            close14_rows.append({
                "question_key": "target1_acquisition_confidence_surface_current",
                "category": "completed_policy_synthesis",
                "motivation": (
                    "Target1 remains active as a confidence-policy result: "
                    "exact geometry is stable, but canonical base confidence "
                    "and source-density behavior are acquisition-sensitive."
                ),
                "current_evidence": (
                    f"run={target1_surface_run}; "
                    f"policy={target1_surface.get('policy_label', '')}; "
                    f"rows={target1_surface.get('target1_canonical_row_count', 0)}; "
                    f"exact={target1_surface.get('target1_exact_geometry_count', 0)}; "
                    f"weak_exact={target1_surface.get('target1_base_weak_exact_count', 0)}; "
                    f"late_high={target1_surface.get('target1_late_high_accepted_count', 0)}/"
                    f"{target1_surface.get('target1_late_high_truth_count', 0)}; "
                    f"escalation_helped={target1_surface.get('source_density_escalation_helped_count', 0)}; "
                    f"lower_best={target1_surface.get('source_density_lower_count_best_count', 0)}"
                ),
                "gpu_readiness": "no_gpu_required",
                "gpu_priority": "none",
                "research_value": 0.78,
                "evidence_gap": 0.31,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Use run 1312 as the current target1 acquisition-confidence "
                    "table. Do not launch a target1 GPU sweep unless a new "
                    "objective or geometry hypothesis is defined."
                ),
            })
        if target1_exception_run.startswith("1314_"):
            close14_rows.append({
                "question_key": "target1_source_density_exception_map_current",
                "category": "completed_policy_synthesis",
                "motivation": (
                    "The target1 source-density branch question now has an "
                    "action map: modern branches are secondary-confirmed and "
                    "terminal 11-source branches should not be extended."
                ),
                "current_evidence": (
                    f"run={target1_exception_run}; "
                    f"policy={target1_exception.get('policy_label', '')}; "
                    f"series={target1_exception.get('source_density_series_count', 0)}; "
                    f"modern_exceptions={target1_exception.get('modern_exception_series_count', 0)}; "
                    f"legacy_exceptions={target1_exception.get('legacy_exception_series_count', 0)}; "
                    f"terminal11_worse={target1_exception.get('terminal_11_worse_count', 0)}/"
                    f"{target1_exception.get('terminal_11_series_count', 0)}; "
                    f"gpu_action={target1_exception.get('recommended_gpu_action', '')}"
                ),
                "gpu_readiness": "closed",
                "gpu_priority": "none",
                "research_value": 0.74,
                "evidence_gap": 0.24,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Use run 1314 as the target1 source-density closure. Do "
                    "not launch a target1 source-count GPU rerun under the "
                    "current hypothesis."
                ),
            })
        if matched_source3_run.startswith("121_"):
            close14_rows.append({
                "question_key": "matched_source3_acquisition_geometry_contrast_closed",
                "category": "completed_policy_synthesis",
                "motivation": (
                    "The reciprocal matched source3 queue is complete and now "
                    "answers the guarded close14/close50 acquisition-geometry "
                    "contrast without exposing a new broad GPU queue."
                ),
                "current_evidence": (
                    f"run={matched_source3_run}; "
                    f"close14_truth_fraction={matched_source3.get('close14_truth_geometry_fraction', '')}; "
                    f"close50_truth_fraction={matched_source3.get('close50_truth_geometry_fraction', '')}; "
                    f"close50_wrong_branch={matched_source3.get('close50_replicated_wrong_branch', '')}; "
                    f"spacing_only={matched_source3.get('spacing_only_causal_generalization_ready', '')}; "
                    f"gpu={matched_source3.get('gpu_priority', '')}"
                ),
                "gpu_readiness": "closed",
                "gpu_priority": "none",
                "research_value": 0.80,
                "evidence_gap": 0.24,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Use the matched-source3 result as a guarded "
                    "acquisition/geometry contrast in the manuscript. Do not "
                    "claim spacing-only causality and do not launch a broad "
                    "source-density GPU queue."
                ),
            })
        close14_rows.extend([
            {
                "question_key": "synthetic_claim_boundaries_current",
                "category": "completed_reporting",
                "motivation": (
                    "The close14 objective-limit result and close50 linear "
                    "29.5 mm seed-frequency caveat have both been moved into "
                    "the manuscript claim-boundary table."
                ),
                "current_evidence": (
                    f"policy={completed_close50_claim_refresh['policy_label']}; "
                    f"claims={completed_close50_claim_refresh['claim_boundary_count']}; "
                    f"close50_included={completed_close50_claim_refresh['close50_seed_frequency_included']}; "
                    f"ambiguous_seeds={completed_close50_claim_refresh['close50_ambiguous_seed_values']}"
                ),
                "gpu_readiness": "no_gpu_required",
                "gpu_priority": "none",
                "research_value": 0.72,
                "evidence_gap": 0.30,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Use the refreshed claim table. Do not launch more GPU "
                    "work unless a genuinely new objective, geometry, or "
                    "acquisition question is introduced."
                ),
            },
            {
                "question_key": "close50_linear29p5_seed_frequency_closed",
                "category": "completed_probe",
                "motivation": (
                    "The seed34 probe closed the two-seed ambiguity-frequency "
                    "uncertainty for close50 linear Tx/Rx=29.5 mm."
                ),
                "current_evidence": (
                    f"policy={completed_close50_policy.get('policy_label', '')}; "
                    f"seed_count={completed_close50_policy.get('seed_count', 0)}; "
                    f"ambiguous_seeds={completed_close50_policy.get('ambiguous_seed_values', '')}; "
                    f"strict_clean_seeds={completed_close50_policy.get('strict_clean_seed_values', '')}"
                ),
                "gpu_readiness": "closed",
                "gpu_priority": "none",
                "research_value": 0.62,
                "evidence_gap": 0.05,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Report exact/strong but not clean-replicated at 29.5 mm; "
                    "keep 30 mm as the paper-safe clean threshold."
                ),
            },
        ])
    elif completed_close50_policy:
        close14_rows = [
            {
                "question_key": "post_close50_claim_boundary_refresh",
                "category": "reporting",
                "motivation": (
                    "The close50 linear 29.5 mm seed-frequency branch is "
                    "complete and changes manuscript wording from pending "
                    "contract to one-seed x-ambiguity caveat."
                ),
                "current_evidence": (
                    f"policy={completed_close50_policy['policy_label']}; "
                    f"seeds={completed_close50_policy['seed_values']}; "
                    f"ambiguous_seeds={completed_close50_policy['ambiguous_seed_values']}; "
                    f"strict_clean_seeds={completed_close50_policy['strict_clean_seed_values']}"
                ),
                "gpu_readiness": "cpu_first",
                "gpu_priority": "none_now",
                "research_value": 0.86,
                "evidence_gap": 0.52,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Refresh the synthetic manuscript claim boundaries using "
                    "the completed close50 seed-frequency policy; no GPU "
                    "launch is needed."
                ),
            },
            {
                "question_key": "close50_linear29p5_seed_frequency_closed",
                "category": "completed_probe",
                "motivation": (
                    "The seed34 probe made the close50 linear 29.5 mm "
                    "ambiguity-frequency statement three-seed rather than "
                    "two-seed."
                ),
                "current_evidence": (
                    f"truth_rows={completed_close50_policy['truth_geometry_row_count']}; "
                    f"strong_rows={completed_close50_policy['strong_confidence_row_count']}; "
                    f"strict_clean_rows={completed_close50_policy['strict_clean_row_count']}; "
                    f"x_ambiguity_rows={completed_close50_policy['x_ambiguity_row_count']}"
                ),
                "gpu_readiness": "closed",
                "gpu_priority": "none",
                "research_value": 0.70,
                "evidence_gap": 0.08,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Keep the result as exact/strong but not clean-replicated; "
                    "do not promote a clean sub-30 threshold."
                ),
            },
        ]
    elif completed_close14_claim_refresh:
        close14_rows = [
            {
                "question_key": "close50_sub30_seed_frequency_contract",
                "category": "replication_design",
                "motivation": (
                    "The close14 objective-limit probe and claim refresh are "
                    "complete. The remaining local synthetic question with a "
                    "bounded experimental path is whether the close50 linear "
                    "29.5 mm x-ambiguity is seed-specific or frequent."
                ),
                "current_evidence": (
                    f"close14_claim_policy={completed_close14_claim_refresh['policy_label']}; "
                    f"sub30_rows={close50['sub30_confidence_row_count']}; "
                    f"x_ambiguous_rows={close50['x_ambiguity_row_count']}; "
                    f"seed13_ambiguous_offsets={close50['seed13_x_ambiguous_offsets_mm']}"
                ),
                "gpu_readiness": "cpu_first",
                "gpu_priority": "none_now",
                "research_value": 0.74,
                "evidence_gap": 0.45,
                "estimated_gpu_cost": 0.05,
                "recommended_action": (
                    "Write a fixed skip-existing contract for one close50 "
                    "target2 linear 29.5 mm seed34 run. Only launch it if the "
                    "contract keeps the decision rule to ambiguity-frequency "
                    "estimation, not clean-threshold promotion."
                ),
            },
            {
                "question_key": "close50_linear29p5_seed34_frequency_probe",
                "category": "conditional_gpu_probe",
                "motivation": (
                    "Existing linear 29.5 mm evidence has seed21 clean and "
                    "seed13 x-ambiguous. Seed34 would make the frequency "
                    "statement three-seed rather than two-seed."
                ),
                "current_evidence": (
                    f"tested_offsets={close50['tested_offsets_mm']}; "
                    f"strict_clean_rows={close50['strict_clean_row_count']}; "
                    f"seed13_ambiguous_offsets={close50['seed13_x_ambiguous_offsets_mm']}"
                ),
                "gpu_readiness": "conditional_after_probe_contract",
                "gpu_priority": "low_conditional",
                "research_value": 0.62,
                "evidence_gap": 0.30,
                "estimated_gpu_cost": 0.35,
                "recommended_action": (
                    "At most one GPU job: seed34, target2, close50, sources4, "
                    "Tx/Rx=29.5 mm, receiver_sampling=linear. Do not run a "
                    "sub-30 sweep."
                ),
            },
            {
                "question_key": "target2_close14_source5_claim_refreshed",
                "category": "completed_probe",
                "motivation": (
                    "The close14 source5/TxRx45 three-seed result has already "
                    "been moved into the manuscript claim-boundary table."
                ),
                "current_evidence": (
                    f"policy={completed_close14_claim_refresh['policy_label']}; "
                    f"close14_probe_included={completed_close14_claim_refresh['close14_probe_included']}; "
                    f"near_ties_0p5={completed_close14_claim_refresh['close14_probe_near_tie_count_at_scale_0p5']}"
                ),
                "gpu_readiness": "closed",
                "gpu_priority": "none",
                "research_value": 0.65,
                "evidence_gap": 0.05,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Keep as a robust objective-uniqueness limit; no further "
                    "GPU work for this exact close14 branch."
                ),
            },
        ]
    elif completed_close14_probe:
        close14_rows = [
            {
                "question_key": "post_close14_claim_boundary_refresh",
                "category": "reporting",
                "motivation": (
                    "The fixed close14 source5/TxRx45 probe is complete and "
                    "now changes the manuscript wording from candidate probe "
                    "to robust objective-uniqueness limitation."
                ),
                "current_evidence": (
                    f"probe_rows={completed_close14_probe['row_count']}; "
                    f"truth={completed_close14_probe['truth_geometry_count']}; "
                    f"strong={completed_close14_probe['strong_confidence_count']}; "
                    f"near_ties_0p5={completed_close14_probe['near_tie_count_at_scale_0p5']}; "
                    f"gpu={completed_close14_probe['gpu_priority']}"
                ),
                "gpu_readiness": "cpu_first",
                "gpu_priority": "none_now",
                "research_value": 0.90,
                "evidence_gap": 0.55,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Refresh the synthetic manuscript claim boundaries using "
                    "the completed close14 objective-uniqueness limit; do not "
                    "launch more GPU work for this exact probe."
                ),
            },
            {
                "question_key": "target2_close14_source5_completed_probe",
                "category": "completed_probe",
                "motivation": (
                    "The source5/TxRx45 close14 target2 branch no longer needs "
                    "a launch decision; the fixed three-seed probe has answered it."
                ),
                "current_evidence": (
                    f"policy={completed_close14_probe['policy_label']}; "
                    f"seeds={completed_close14_probe['seed_values']}; "
                    f"x_ambiguity={completed_close14_probe['x_ambiguity_row_count']}; "
                    f"competitor_x={completed_close14_probe['competing_geometry_x_values_mm']}"
                ),
                "gpu_readiness": "closed",
                "gpu_priority": "none",
                "research_value": 0.75,
                "evidence_gap": 0.10,
                "estimated_gpu_cost": 0.0,
                "recommended_action": (
                    "Use this as a robust objective-uniqueness limit in the "
                    "synthetic 2D claim table, not as clean lateral resolution."
                ),
            },
        ]
    else:
        close14_rows = [
            {
                "question_key": "target2_close14_source5_threshold_gate",
                "category": "objective_gate",
                "motivation": (
                    "Known-acquisition objective caveats are target2-only and the "
                    "persistent close14 x caveat is source5/TxRx45, not close50."
                ),
                "current_evidence": (
                    f"known_target2_near_ties={acquisition_gap['target2_known_acquisition_near_tie_row_count']}; "
                    f"close14_x={family_gap['known_close14_target2_x_near_tie_count']}; "
                    f"source5_txrx45_0p5={threshold['source5_txrx45_near_tie_count_at_scale_0p5']}; "
                    f"source4_50_default={threshold['source4_txrx50_default_near_tie_count']}"
                ),
                "gpu_readiness": "cpu_first",
                "gpu_priority": "none_now",
                "research_value": 0.92,
                "evidence_gap": 0.70,
                "estimated_gpu_cost": 0.15,
                "recommended_action": (
                    "Define the exact narrow target2 close14 source5/TxRx45 probe "
                    "contract and manuscript decision rule before any GPU run."
                ),
            },
            {
                "question_key": "target2_close14_source5_narrow_probe",
                "category": "conditional_gpu_probe",
                "motivation": (
                    "If the paper needs one new synthetic 2D experiment, the CPU "
                    "gate now identifies source5/TxRx45 close14 target2 x-resolution."
                ),
                "current_evidence": (
                    f"default_near_ties={threshold['near_tie_count_at_scale_1p0']}; "
                    f"tight_0p5_near_ties={threshold['near_tie_count_at_scale_0p5']}; "
                    f"source5_txrx45_default={threshold['source5_txrx45_near_tie_count_at_scale_1p0']}"
                ),
                "gpu_readiness": "conditional_after_probe_contract",
                "gpu_priority": "low_conditional",
                "research_value": 0.78,
                "evidence_gap": 0.45,
                "estimated_gpu_cost": 0.35,
                "recommended_action": (
                    "Only run this after writing a fixed probe contract: target2, "
                    "close14, source5, Tx/Rx45, fixed threshold decision, skip-existing."
                ),
            },
        ]

    rows = [
        *close14_rows,
        {
            "question_key": "legacy_close50_x_ambiguity",
            "category": "claim_boundary",
            "motivation": (
                "Earlier close50 sub-30 linear receiver rows remain a claim caveat, "
                "but current family context points away from close50 as the next probe."
            ),
            "current_evidence": (
                f"x_ambiguity_rows={close50['x_ambiguity_row_count']}; "
                f"tested_offsets_mm={close50['tested_offsets_mm']}; "
                f"close50_known_near_ties={family_gap['target2_close50_known_near_tie_count']}"
            ),
            "gpu_readiness": "superseded_by_current_gate",
            "gpu_priority": "none",
            "research_value": 0.55,
            "evidence_gap": 0.20,
            "estimated_gpu_cost": 0.20,
            "recommended_action": (
                "Keep as a claim caveat; current actionability evidence points "
                "to close14 target2, not broad close50 reruns."
            ),
        },
        {
            "question_key": "sub30_seed_frequency_estimate",
            "category": "replication_design",
            "motivation": (
                "If the paper needs a frequency estimate for sub-30 linear "
                "receiver ambiguity, existing seed21/seed13 evidence is too small."
            ),
            "current_evidence": (
                f"strict_clean_rows={close50['strict_clean_row_count']}; "
                f"sub30_rows={close50['sub30_confidence_row_count']}; "
                f"seed13_ambiguous_offsets={close50['seed13_x_ambiguous_offsets_mm']}"
            ),
            "gpu_readiness": "conditional_after_objective_scope",
            "gpu_priority": "low_conditional",
            "research_value": 0.45,
            "evidence_gap": 0.25,
            "estimated_gpu_cost": 0.55,
            "recommended_action": (
                "Defer; the current actionability map points away from close50 "
                "as the next probe family."
            ),
        },
        {
            "question_key": "target1_archive_caveat_closure",
            "category": "claim_boundary",
            "motivation": "Target1 objective near ties are archive rows without source/TxRx metadata.",
            "current_evidence": (
                f"target1_known_near_ties={acquisition_gap['target1_known_acquisition_near_tie_row_count']}; "
                f"target1_archive_near_ties={family_gap['target1_legacy_archive_near_tie_count']}"
            ),
            "gpu_readiness": "archive_claim_caveat",
            "gpu_priority": "none",
            "research_value": 0.40,
            "evidence_gap": 0.15,
            "estimated_gpu_cost": 0.30,
            "recommended_action": "Do not rerun target1 for this caveat; keep the manuscript wording conservative.",
        },
        {
            "question_key": "modern_ringdown050_exception_probe",
            "category": "exception_closure",
            "motivation": "Previously open modern target0 weak-exact exception.",
            "current_evidence": (
                f"modern_open={modern['modern_ringdown050_open_count']}; "
                f"modern_closed={modern['modern_ringdown050_closed_count']}; "
                f"gpu={modern['gpu_priority']}"
            ),
            "gpu_readiness": "closed",
            "gpu_priority": "none",
            "research_value": 0.20,
            "evidence_gap": 0.05,
            "estimated_gpu_cost": 0.35,
            "recommended_action": "No GPU action; cite the existing source-density closure.",
        },
        {
            "question_key": "target0_source_density_extension",
            "category": "acquisition_extension",
            "motivation": "Target0 source-density rescue crossed the base cutoff at 9 sources.",
            "current_evidence": (
                f"baseline={target0['baseline_base_margin']:.6g}; "
                f"best_spacing={target0['best_spacing_base_margin']:.6g}; "
                f"source_density={target0['best_overall_base_margin']:.6g}; "
                f"gpu={target0['gpu_priority']}"
            ),
            "gpu_readiness": "closed",
            "gpu_priority": "none",
            "research_value": 0.25,
            "evidence_gap": 0.10,
            "estimated_gpu_cost": 0.45,
            "recommended_action": "No extension unless a new acquisition-design hypothesis is stated.",
        },
        {
            "question_key": "publication_claim_boundary_audit",
            "category": "reporting",
            "motivation": "The synthetic publication bundle is ready but needs claim discipline.",
            "current_evidence": (
                f"run={bundle_run}; "
                f"figures={bundle['figure_count']}; "
                f"validated={bundle['validated_figure_count']}; "
                f"gpu={bundle['gpu_priority']}"
            ),
            "gpu_readiness": "no_gpu_required",
            "gpu_priority": "none",
            "research_value": 0.70,
            "evidence_gap": 0.20,
            "estimated_gpu_cost": 0.0,
            "recommended_action": "Use the claim-boundary CSV before drafting manuscript text.",
        },
    ]
    if completed_close14_claim_refresh or completed_close50_claim_refresh:
        rows = [
            row for row in rows
            if row["question_key"] != "sub30_seed_frequency_estimate"
        ]
    for row in rows:
        row["priority_score"] = (
            float(row["research_value"])
            * float(row["evidence_gap"])
            * (1.0 - 0.5 * float(row["estimated_gpu_cost"]))
        )
    return sorted(rows, key=lambda row: row["priority_score"], reverse=True)


def summarize_matrix(rows: list[dict]) -> dict:
    immediate_gpu = [row for row in rows if row["gpu_priority"] == "high_now"]
    cpu_first = [row for row in rows if row["gpu_readiness"] == "cpu_first"]
    top = rows[0] if rows else {}
    target1_surface_included = any(
        row.get("question_key") == "target1_acquisition_confidence_surface_current"
        for row in rows
    )
    target1_exception_map_included = any(
        row.get("question_key") == "target1_source_density_exception_map_current"
        for row in rows
    )
    matched_source3_policy_included = any(
        row.get("question_key") == "matched_source3_acquisition_geometry_contrast_closed"
        for row in rows
    )
    if top.get("question_key") == "synthetic_publication_bundle_current":
        decision = (
            "The current synthetic paper-facing bundle includes the resolution "
            "claim map, target1 policy figures, close50 legacy midpoint "
            "refresh, and detailed close14/close50 claim-boundary rows. No "
            "immediate or broad GPU run is justified; further work requires a "
            "new objective, geometry, or acquisition question."
        )
    elif top.get("question_key") == "post_close14_claim_boundary_refresh":
        decision = (
            "The fixed close14 target2 probe is complete and shows a persistent "
            "+1 mm objective near-tie across all seed/case rows. The next "
            "synthetic work is CPU-side claim-boundary refresh, not another "
            "GPU launch for that probe."
        )
    elif top.get("question_key") == "close50_sub30_seed_frequency_contract":
        decision = (
            "The close14 probe and claim refresh are complete. The next "
            "synthetic work is a CPU-side contract for a single close50 target2 "
            "linear 29.5 mm seed-frequency probe. Any GPU launch should be "
            "one seed34 run only and should estimate ambiguity frequency, not "
            "promote a clean sub-30 threshold."
        )
    elif top.get("question_key") == "post_close50_claim_boundary_refresh":
        decision = (
            "The close50 linear 29.5 mm seed-frequency branch is complete: "
            "truth is exact/strong across three seeds, but seed13 remains an "
            "x-ambiguity caveat. The next work is CPU-side claim-boundary "
            "refresh, not another GPU launch."
        )
    elif top.get("question_key") == "synthetic_claim_boundaries_current":
        decision = (
            "The close14 objective-limit result and close50 linear 29.5 mm "
            "seed-frequency caveat are now both reflected in the synthetic "
            "claim-boundary table. No immediate or broad GPU run is justified."
        )
    else:
        decision = (
            "The highest-value next synthetic work is CPU-first target2 close14 "
            "probe-contract design around the source5/TxRx45 threshold gate. No "
            "candidate currently justifies immediate or broad GPU execution."
        )
    if target1_surface_included:
        decision += (
            " The target1 acquisition-confidence surface is also current: exact "
            "geometry is stable, but source-density behavior is nonmonotonic and "
            "does not justify a broad target1 GPU sweep."
        )
    if target1_exception_map_included:
        decision += (
            " The target1 source-density exception map closes the branch under "
            "the current hypothesis: zero modern exceptions, one legacy "
            "ringdown025 exception, and no target1 source-count GPU rerun."
        )
    if matched_source3_policy_included:
        decision += (
            " The matched-source3 queue is complete: it supports a guarded "
            "acquisition/geometry contrast, not a spacing-only causal claim or "
            "a broad source-density GPU queue."
        )
    return {
        "policy_label": "synthetic_2d_next_question_matrix_cpu_first_no_gpu",
        "candidate_count": len(rows),
        "cpu_first_count": len(cpu_first),
        "immediate_gpu_priority_count": 0,
        "conditional_gpu_candidate_count": sum(1 for row in rows if "conditional" in row["gpu_priority"]),
        "target1_acquisition_surface_included": target1_surface_included,
        "target1_exception_map_included": target1_exception_map_included,
        "matched_source3_policy_included": matched_source3_policy_included,
        "top_question_key": top.get("question_key", ""),
        "top_question_gpu_readiness": top.get("gpu_readiness", ""),
        "top_question_recommended_action": top.get("recommended_action", ""),
        "gpu_priority": "none_now",
        "decision": decision,
        "open_immediate_gpu_rows": len(immediate_gpu),
    }


def plot_matrix(rows: list[dict], summary: dict, save_path: Path) -> str:
    labels = [row["question_key"].replace("_", "\n") for row in rows]
    x = np.arange(len(rows))
    value = np.asarray([float(row["research_value"]) for row in rows], dtype=np.float64)
    gap = np.asarray([float(row["evidence_gap"]) for row in rows], dtype=np.float64)
    cost = np.asarray([float(row["estimated_gpu_cost"]) for row in rows], dtype=np.float64)
    priority = np.asarray([float(row["priority_score"]) for row in rows], dtype=np.float64)

    fig, axes = plt.subplots(1, 2, figsize=(14.6, 5.2), constrained_layout=True)
    axes[0].bar(x - 0.25, value, width=0.25, color="#2f9d55", label="research value")
    axes[0].bar(x, gap, width=0.25, color="#4c78a8", label="evidence gap")
    axes[0].bar(x + 0.25, cost, width=0.25, color="#c7302b", label="GPU cost")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(0.0, 1.05)
    axes[0].set_title("Candidate question components")
    axes[0].grid(axis="y", color="#dddddd", linewidth=0.6)
    axes[0].legend(frameon=False, fontsize=8)

    colors = ["#4c78a8" if row["gpu_readiness"] == "cpu_first" else "#6b6b6b" for row in rows]
    axes[1].bar(x, priority, width=0.55, color=colors)
    axes[1].set_xticks(x, labels)
    axes[1].set_ylim(0.0, max(0.7, float(np.max(priority)) + 0.1 if priority.size else 0.7))
    axes[1].set_title("Priority score, blue = CPU-first")
    axes[1].grid(axis="y", color="#dddddd", linewidth=0.6)

    fig.suptitle(
        f"Synthetic 2D next-question matrix: {summary['policy_label']}",
        fontweight="bold",
    )
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def write_figure_notes(path: Path, summary: dict, rows_csv: Path, validation_csv: Path) -> None:
    """Write notes for the synthetic 2D next-question matrix figure."""
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `synthetic_2d_next_question_matrix.png`",
                "",
                "This figure ranks current synthetic 2D follow-up questions from the",
                "existing archive. The bars show research value, evidence gap, estimated",
                "GPU cost, and the resulting priority score for each candidate question.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Top question: `{summary['top_question_key']}`.",
                f"Immediate GPU candidates: `{summary['immediate_gpu_priority_count']}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "This is a planning matrix, not a simulation result. Candidate rows and",
                f"recommended actions are stored in `{rows_csv.name}`. Image-validation",
                f"metrics for this matrix figure are stored in `{validation_csv.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--run-name", default="synthetic_2d_next_question_matrix")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    root = Path(args.experiment_root)
    rows = candidate_rows(root)
    summary = summarize_matrix(rows)

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root=str(root)))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    rows_csv = data_dir / "synthetic_2d_next_question_matrix_rows.csv"
    summary_json = data_dir / "synthetic_2d_next_question_matrix_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = Path(plot_matrix(rows, summary, figures_dir / "synthetic_2d_next_question_matrix.png"))
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(rows_csv, [json_safe(row) for row in rows])
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, rows_csv, validation_csv)
    output_summary = {
        **summary,
        "paths": {
            "rows_csv": str(rows_csv),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
            "figure_validation_csv": str(validation_csv),
        },
    }
    summary_json.write_text(json.dumps(json_safe(output_summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "synthetic_2d_next_question_matrix",
        {
            "summary_json": str(summary_json),
            "rows_csv": str(rows_csv),
            "figure_validation_csv": str(validation_csv),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(output_summary), indent=2))


if __name__ == "__main__":
    main()
