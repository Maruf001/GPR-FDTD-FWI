#!/usr/bin/env python3
"""Build compact manuscript tables from current local 2D and field endpoints."""

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
from run_gssi_dzt_qc import DEFAULT_DATASET_ID, DEFAULT_FIELD_ROOT, field_dataset_output_root, readgssi_version  # noqa: E402
from run_gssi_field_content_anchor_trace_alignment import figure_stats  # noqa: E402
from run_gssi_field_preprocess_feature_qc import json_safe, write_csv  # noqa: E402
from run_local_2d_field_manuscript_evidence_audit import (  # noqa: E402
    DEFAULT_FIELD_BUNDLE_RUN,
    DEFAULT_FIELD_POLICY_RUN,
    DEFAULT_SYNTHETIC_BUNDLE_RUN,
    DEFAULT_SYNTHETIC_NEXT_MATRIX_RUN,
)
from run_synthetic_2d_publication_figure_bundle import DEFAULT_EXPERIMENT_ROOT  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


DEFAULT_AUDIT_RUN = "032_local_2d_field_manuscript_evidence_audit_post_event_support_timing_discriminant_hpc"
DEFAULT_SYNTHETIC_SOURCE_NOTES_RUN = "1325_synthetic_publication_source_figure_notes_backfill_report"
DEFAULT_FIELD_SOURCE_NOTES_RUN = "114_gssi51600s_field_publication_source_figure_notes_backfill_post_event_support_timing_discriminant_hpc"
DEFAULT_TARGET1_PROBE_SCORECARD_RUN = "028_local_2d_target1_probe_readiness_scorecard"
DEFAULT_DETECTOR_HANDOFF_BUDGET_RUN = "029_local_2d_detector_handoff_budget"
DEFAULT_DETECTOR_ALLTRIPLES_GATE_RUN = "030_local_2d_detector_alltriples_gate_pilot"
DEFAULT_FIELD_CUE_SUPPORT_CATALOG_RUN = "113_gssi51600s_field_cue_support_catalog"
DEFAULT_DETECTOR_RANK_BUDGET_RUN = "034_local_2d_detector_rank_budget_diagnostic_post_alltriples_gate"
DEFAULT_DETECTOR_COMPONENT_GATE_RUN = "035_local_2d_detector_component_waveform_gate_post_rank_budget"
DEFAULT_DETECTOR_COMPONENT_SELECTOR_RUN = "037_local_2d_detector_component_selector_audit_post_component_gate"
DEFAULT_DETECTOR_GEOMETRY_SELECTOR_RUN = "041_local_2d_detector_geometry_family_selector_post_upper_bound_policy"
DEFAULT_DETECTOR_SELECTOR_GAP_RUN = "045_local_2d_detector_selector_gap_decomposition"
DEFAULT_DETECTOR_SELECTOR_COUNTERFACTUAL_RUN = "048_local_2d_detector_selector_counterfactual_sensitivity"
DEFAULT_DETECTOR_IMAGE_OBJECTIVE_RANK_RUN = "050_local_2d_detector_image_objective_rank_diagnostic"
DEFAULT_DETECTOR_TARGET_FAILURE_TAXONOMY_RUN = "053_local_2d_detector_target_failure_taxonomy"
DEFAULT_DETECTOR_DEPTH_SLOT_PRIOR_RUN = "055_local_2d_detector_depth_slot_prior_probe"
DEFAULT_DETECTOR_SLOT_COMPONENT_ASSEMBLY_RUN = "057_local_2d_detector_slot_component_assembly_probe"
DEFAULT_DETECTOR_BLIND_ENVELOPE_RUN = "059_local_2d_detector_blind_component_envelope_assembly"
DEFAULT_DETECTOR_BLIND_ENVELOPE_ROBUSTNESS_RUN = "061_local_2d_detector_blind_envelope_robustness_audit"
DEFAULT_DETECTOR_BLIND_ENVELOPE_STABILITY_RUN = "063_local_2d_detector_blind_envelope_policy_stability"
DEFAULT_DETECTOR_BLIND_ENVELOPE_TUNING_RUN = "066_local_2d_detector_blind_envelope_tuning_sensitivity"
DEFAULT_DETECTOR_BLIND_ENVELOPE_RELIABILITY_RUN = "069_local_2d_detector_blind_envelope_reliability_gate"
DEFAULT_DETECTOR_BLIND_ENVELOPE_RELIABILITY_THRESHOLD_RUN = (
    "071_local_2d_detector_blind_envelope_reliability_threshold_sensitivity"
)
DEFAULT_DETECTOR_PHYSICS_AMBIGUITY_LINK_RUN = "074_local_2d_detector_physics_ambiguity_link"
DEFAULT_DETECTOR_REFINEMENT_LAUNCH_CONTRACT_RUN = "077_local_2d_detector_refinement_launch_contract_audit"
DEFAULT_DETECTOR_SAMPLING_BOUNDARY_INTEGRATION_RUN = "079_local_2d_detector_sampling_boundary_integration"
DEFAULT_DETECTOR_COMPONENT_SEED_EXPORT_RUN = "081_local_2d_detector_component_seed_export"
DEFAULT_DETECTOR_REFINEMENT_NEIGHBORHOOD_BUDGET_RUN = "084_local_2d_detector_lateral_slot_neighborhood_budget"
DEFAULT_DETECTOR_SEED_GEOMETRY_ERROR_AUDIT_RUN = "086_local_2d_detector_seed_geometry_error_audit"
DEFAULT_DETECTOR_RADIUS_MATERIAL_PRIOR_SCOPE_RUN = "089_local_2d_detector_radius_material_prior_scope_audit"
DEFAULT_DETECTOR_CONTROLLED_PRIOR_REFINEMENT_BUDGET_RUN = (
    "090_local_2d_detector_controlled_prior_refinement_budget"
)
DEFAULT_DETECTOR_FIXED_RADIUS_PILOT_OUTCOME_SYNTHESIS_RUN = (
    "127_local_2d_detector_fixed_radius_pilot_outcome_synthesis_post_second_pass"
)
DEFAULT_DETECTOR_FIXED_RADIUS_RESIDUAL_AMBIGUITY_AUDIT_RUN = (
    "128_local_2d_detector_fixed_radius_residual_ambiguity_audit_post_second_pass"
)
DEFAULT_DETECTOR_FIXED_RADIUS_LOCKING_POLICY_VALIDATION_RUN = (
    "131_local_2d_detector_fixed_radius_locking_policy_validation_post_unlock_probe"
)
DEFAULT_DETECTOR_UPPER_BOUND_POLICY_RUN = "039_local_2d_detector_upper_bound_policy_post_selector_audit"
DEFAULT_FIELD_CUE_TIMING_ENVELOPE_RUN = "115_gssi51600s_field_cue_timing_envelope_post_cue_support_catalog"
DEFAULT_FIELD_SPATIAL_TRANSFER_RUN = "116_gssi51600s_field_spatial_transfer_audit_post_timing_envelope"
DEFAULT_FIELD_ANCHOR_INTERVAL_RUN = "117_gssi51600s_field_anchor_interval_reconciliation_post_spatial_transfer"
DEFAULT_FIELD_DIMENSIONALITY_DECISION_RUN = (
    "118_gssi51600s_field_hpc_dimensionality_decision_card_post_anchor_interval"
)
DEFAULT_FIELD_TIME_ZERO_LADDER_RUN = "121_gssi51600s_field_time_zero_ladder_post_leave_one"
DEFAULT_FIELD_SHORT_ANCHOR_LEAVE_ONE_RUN = "120_gssi51600s_field_short_anchor_leave_one_audit"
DEFAULT_FIELD_SHORT_ANCHOR_SPATIAL_CONSISTENCY_RUN = (
    "122_gssi51600s_field_short_anchor_spatial_consistency_audit"
)
DEFAULT_FIELD_INVERSION_READINESS_RUN = (
    "123_gssi51600s_field_inversion_readiness_synthesis_post_spatial_consistency"
)
DEFAULT_FIELD_SHORT_ANCHOR_RADIUS_DEGENERACY_RUN = "125_gssi51600s_field_short_anchor_radius_degeneracy_audit"
DEFAULT_FIELD_SHORT_ANCHOR_SIGNED_MORPHOLOGY_RUN = "126_gssi51600s_field_short_anchor_signed_morphology_audit"
DEFAULT_FIELD_SHORT_ANCHOR_SIGNED_MORPHOLOGY_SENSITIVITY_RUN = (
    "127_gssi51600s_field_short_anchor_signed_morphology_sensitivity"
)
DEFAULT_FIELD_COLLECTION_HANDOFF_RUN = "155_gssi51600s_controlled_collection_handoff"


def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def safe_float(value, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def no_gpu_value(value) -> bool:
    return str(value).strip().lower() in {"", "none", "none_now", "no_gpu_required"}


def claim_tier(domain: str, claim_area: str) -> str:
    if domain == "synthetic_2d":
        if claim_area in {"resolution_limit", "target2_close14_objective_limit", "target2_close50_linear29p5_seed_frequency"}:
            return "main_result"
        if claim_area in {"gpu_next_step", "field_separation"}:
            return "guardrail"
        return "supporting_policy"
    if claim_area in {
        "short_profile_timing",
        "long_profile_pattern",
        "field_time_zero_uncertainty_budget",
        "field_timing_anchor_conflict",
        "field_timing_window_family_classification",
        "field_cue_spacing_context",
    }:
        return "field_supplement_result"
    if claim_area in {"gpu_next_step", "synthetic_separation", "field_acquisition_readiness"}:
        return "guardrail"
    return "field_supplement_guardrail"


def figure_role(domain: str, figure_key: str) -> str:
    if domain == "synthetic_2d":
        if "resolution" in figure_key or "target1" in figure_key:
            return "main_synthetic_result"
        return "synthetic_supporting_policy"
    if figure_key in {
        "short_content_waveform_qc",
        "short_supported_stack_intervals",
        "field_time_zero_uncertainty_budget",
        "field_time_zero_perturbation_sensitivity",
        "field_timing_anchor_conflict",
        "field_timing_window_family_classification",
        "field_cue_spacing_threshold_sensitivity",
    }:
        return "field_primary_supplement"
    return "field_guardrail_supplement"


def combine_claim_rows(synthetic_claims: list[dict], field_claims: list[dict]) -> list[dict]:
    rows = []
    for domain, claims in (("synthetic_2d", synthetic_claims), ("field_2d", field_claims)):
        for idx, row in enumerate(claims, start=1):
            claim_area = row.get("claim_area", "")
            rows.append(
                {
                    "domain": domain,
                    "claim_order": idx,
                    "claim_area": claim_area,
                    "paper_use_tier": claim_tier(domain, claim_area),
                    "allowed_claim": row.get("allowed_claim", ""),
                    "not_allowed": row.get("not_allowed", ""),
                }
            )
    return rows


def combine_figure_rows(synthetic_figures: list[dict], field_figures: list[dict]) -> list[dict]:
    rows = []
    for domain, figures in (("synthetic_2d", synthetic_figures), ("field_2d", field_figures)):
        for idx, row in enumerate(figures, start=1):
            figure_key = row.get("figure_key", "")
            metric_label = row.get("support_metric") or row.get("metric_label", "")
            metric_value = row.get("metric_value", "")
            metric_summary = row.get("support_metric") or (
                f"{metric_label}={metric_value}".strip("=")
            )
            rows.append(
                {
                    "domain": domain,
                    "figure_order": idx,
                    "figure_key": figure_key,
                    "paper_role": figure_role(domain, figure_key),
                    "source_run": row.get("source_run", ""),
                    "policy_or_status": row.get("status_label") or row.get("policy_label", ""),
                    "metric_summary": metric_summary,
                    "use_summary": row.get("paper_use") or row.get("allowed_use", ""),
                    "figure_path": row.get("figure_path", ""),
                }
            )
    return rows


def metric_rows(
    synthetic_summary: dict,
    synthetic_next: dict,
    field_summary: dict,
    field_policy: dict,
    audit_summary: dict,
    synthetic_source_notes: dict | None = None,
    field_source_notes: dict | None = None,
    target1_probe_summary: dict | None = None,
    detector_handoff_summary: dict | None = None,
    detector_alltriples_summary: dict | None = None,
    field_cue_catalog_summary: dict | None = None,
    detector_rank_budget_summary: dict | None = None,
    detector_component_gate_summary: dict | None = None,
    detector_component_selector_summary: dict | None = None,
    detector_geometry_selector_summary: dict | None = None,
    detector_selector_gap_summary: dict | None = None,
    detector_selector_counterfactual_summary: dict | None = None,
    detector_image_objective_rank_summary: dict | None = None,
    detector_target_failure_summary: dict | None = None,
    detector_depth_slot_prior_summary: dict | None = None,
    detector_slot_component_assembly_summary: dict | None = None,
    detector_blind_envelope_summary: dict | None = None,
    detector_blind_envelope_robustness_summary: dict | None = None,
    detector_blind_envelope_stability_summary: dict | None = None,
    detector_blind_envelope_tuning_summary: dict | None = None,
    detector_blind_envelope_reliability_summary: dict | None = None,
    detector_blind_envelope_reliability_threshold_summary: dict | None = None,
    detector_physics_ambiguity_link_summary: dict | None = None,
    detector_refinement_launch_contract_summary: dict | None = None,
    detector_component_seed_export_summary: dict | None = None,
    detector_refinement_neighborhood_budget_summary: dict | None = None,
    detector_seed_geometry_error_audit_summary: dict | None = None,
    detector_upper_bound_summary: dict | None = None,
    field_cue_timing_envelope_summary: dict | None = None,
    field_spatial_transfer_summary: dict | None = None,
    field_anchor_interval_summary: dict | None = None,
    field_dimensionality_summary: dict | None = None,
    field_time_zero_ladder_summary: dict | None = None,
    field_short_anchor_leave_one_summary: dict | None = None,
    field_short_anchor_spatial_consistency_summary: dict | None = None,
    field_inversion_readiness_summary: dict | None = None,
    detector_sampling_boundary_integration_summary: dict | None = None,
    field_short_anchor_radius_degeneracy_summary: dict | None = None,
    field_short_anchor_signed_morphology_summary: dict | None = None,
    field_short_anchor_signed_morphology_sensitivity_summary: dict | None = None,
    field_collection_handoff_summary: dict | None = None,
    detector_radius_material_prior_scope_summary: dict | None = None,
    detector_controlled_prior_refinement_budget_summary: dict | None = None,
    detector_fixed_radius_pilot_outcome_synthesis_summary: dict | None = None,
    detector_fixed_radius_residual_ambiguity_audit_summary: dict | None = None,
    detector_fixed_radius_locking_policy_validation_summary: dict | None = None,
) -> list[dict]:
    synthetic_notes = synthetic_source_notes or {}
    source_notes = field_source_notes or {}
    target1_probe = target1_probe_summary or {}
    detector_handoff = detector_handoff_summary or {}
    detector_alltriples = detector_alltriples_summary or {}
    field_cue_catalog = field_cue_catalog_summary or {}
    detector_rank_budget = detector_rank_budget_summary or {}
    detector_component_gate = detector_component_gate_summary or {}
    detector_component_selector = detector_component_selector_summary or {}
    detector_geometry_selector = detector_geometry_selector_summary or {}
    detector_selector_gap = detector_selector_gap_summary or {}
    detector_selector_counterfactual = detector_selector_counterfactual_summary or {}
    detector_image_objective_rank = detector_image_objective_rank_summary or {}
    detector_target_failure = detector_target_failure_summary or {}
    detector_depth_slot_prior = detector_depth_slot_prior_summary or {}
    detector_slot_component_assembly = detector_slot_component_assembly_summary or {}
    detector_blind_envelope = detector_blind_envelope_summary or {}
    detector_blind_envelope_robustness = detector_blind_envelope_robustness_summary or {}
    detector_blind_envelope_stability = detector_blind_envelope_stability_summary or {}
    detector_blind_envelope_tuning = detector_blind_envelope_tuning_summary or {}
    detector_blind_envelope_reliability = detector_blind_envelope_reliability_summary or {}
    detector_blind_envelope_reliability_threshold = detector_blind_envelope_reliability_threshold_summary or {}
    detector_physics_ambiguity_link = detector_physics_ambiguity_link_summary or {}
    detector_refinement_launch_contract = detector_refinement_launch_contract_summary or {}
    detector_component_seed_export = detector_component_seed_export_summary or {}
    detector_refinement_neighborhood_budget = detector_refinement_neighborhood_budget_summary or {}
    detector_seed_geometry_error_audit = detector_seed_geometry_error_audit_summary or {}
    detector_upper_bound = detector_upper_bound_summary or {}
    field_cue_timing_envelope = field_cue_timing_envelope_summary or {}
    field_spatial_transfer = field_spatial_transfer_summary or {}
    field_anchor_interval = field_anchor_interval_summary or {}
    field_dimensionality = field_dimensionality_summary or {}
    field_time_zero_ladder = field_time_zero_ladder_summary or {}
    field_short_anchor_leave_one = field_short_anchor_leave_one_summary or {}
    field_short_anchor_spatial_consistency = field_short_anchor_spatial_consistency_summary or {}
    field_inversion_readiness = field_inversion_readiness_summary or {}
    detector_sampling_boundary_integration = detector_sampling_boundary_integration_summary or {}
    field_short_anchor_radius_degeneracy = field_short_anchor_radius_degeneracy_summary or {}
    field_short_anchor_signed_morphology = field_short_anchor_signed_morphology_summary or {}
    field_short_anchor_signed_morphology_sensitivity = (
        field_short_anchor_signed_morphology_sensitivity_summary or {}
    )
    field_collection_handoff = field_collection_handoff_summary or {}
    detector_radius_material_prior_scope = detector_radius_material_prior_scope_summary or {}
    detector_controlled_prior_refinement_budget = detector_controlled_prior_refinement_budget_summary or {}
    detector_fixed_radius_pilot_outcome = detector_fixed_radius_pilot_outcome_synthesis_summary or {}
    detector_fixed_radius_residual_ambiguity = detector_fixed_radius_residual_ambiguity_audit_summary or {}
    detector_fixed_radius_locking_validation = detector_fixed_radius_locking_policy_validation_summary or {}
    rows = [
        {
            "domain": "synthetic_2d",
            "metric": "publication_figure_count",
            "value": safe_float(synthetic_summary.get("figure_count")),
            "interpretation": "current synthetic publication figures",
        },
        {
            "domain": "synthetic_2d",
            "metric": "publication_claim_boundary_count",
            "value": safe_float(synthetic_summary.get("claim_boundary_count")),
            "interpretation": "current synthetic claim boundaries",
        },
        {
            "domain": "synthetic_2d",
            "metric": "next_matrix_immediate_gpu_candidates",
            "value": safe_float(synthetic_next.get("immediate_gpu_priority_count", 0.0)),
            "interpretation": "no current synthetic immediate GPU queue",
        },
        {
            "domain": "synthetic_2d",
            "metric": "source_figure_notes_present_after_count",
            "value": safe_float(synthetic_notes.get("notes_present_after_count"), 0.0),
            "interpretation": "paper-facing synthetic source figures with FIGURE_NOTES.md",
        },
        {
            "domain": "field_2d",
            "metric": "publication_figure_count",
            "value": safe_float(field_summary.get("figure_row_count")),
            "interpretation": "current field publication figures",
        },
        {
            "domain": "field_2d",
            "metric": "publication_claim_boundary_count",
            "value": safe_float(field_summary.get("claim_boundary_count")),
            "interpretation": "current field claim boundaries",
        },
        {
            "domain": "field_2d",
            "metric": "cue_spacing_min_same_time_spacing_mm",
            "value": safe_float(field_summary.get("cue_spacing_min_same_time_spacing_mm")),
            "interpretation": "field context only, not known-truth resolution validation",
        },
        {
            "domain": "field_2d",
            "metric": "timing_anchor_early_vs_short_delta_half_widths",
            "value": safe_float(field_summary.get("timing_anchor_early_vs_short_delta_half_widths")),
            "interpretation": "timing-anchor scope boundary, not absolute time-zero",
        },
        {
            "domain": "field_2d",
            "metric": "timing_anchor_long_vs_short_delta_half_widths",
            "value": safe_float(field_summary.get("timing_anchor_long_vs_short_delta_half_widths")),
            "interpretation": "long timing remains pattern-only relative to short content timing",
        },
        {
            "domain": "field_2d",
            "metric": "timing_window_early_strict_near_zero_lag_count",
            "value": safe_float(field_summary.get("timing_window_early_strict_near_zero_lag_count")),
            "interpretation": "early/ringdown windows remain common-mode, not content time-zero",
        },
        {
            "domain": "field_2d",
            "metric": "timing_window_short_nonraw_supported_count",
            "value": safe_float(field_summary.get("timing_window_short_nonraw_supported_count")),
            "interpretation": "non-raw short content windows support the relative correction",
        },
        {
            "domain": "field_2d",
            "metric": "timing_window_long_reject_short_transfer_count",
            "value": safe_float(field_summary.get("timing_window_long_reject_short_transfer_count")),
            "interpretation": "long windows reject transferring the short-pair correction",
        },
        {
            "domain": "field_2d",
            "metric": "field_policy_ready_for_field_fwi",
            "value": 1.0 if field_policy.get("publication_cue_spacing_field_fwi_ready", False) else 0.0,
            "interpretation": "0 means field FWI remains blocked",
        },
        {
            "domain": "field_2d",
            "metric": "source_figure_notes_present_after_count",
            "value": safe_float(source_notes.get("notes_present_after_count"), 0.0),
            "interpretation": "paper-facing field source figures with FIGURE_NOTES.md",
        },
        {
            "domain": "cross_bundle",
            "metric": "validated_figure_file_count",
            "value": safe_float(audit_summary.get("validated_figure_file_count")),
            "interpretation": "validated synthetic plus field figure files",
        },
        {
            "domain": "cross_bundle",
            "metric": "claim_boundary_row_count",
            "value": safe_float(audit_summary.get("claim_boundary_row_count")),
            "interpretation": "complete synthetic plus field claim-boundary rows",
        },
    ]
    if target1_probe:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "target1_probe_triggered_gate_count",
                    "value": safe_float(target1_probe.get("triggered_gate_count"), 0.0),
                    "interpretation": "0 means target1 has no CPU-side gate justifying a GPU probe",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "target1_probe_gpu_action_count",
                    "value": safe_float(target1_probe.get("gpu_action_count"), 0.0),
                    "interpretation": "0 keeps target1 on CPU-side policy synthesis",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "target1_probe_ready_for_gpu",
                    "value": 1.0 if target1_probe.get("ready_for_target1_gpu_probe", False) else 0.0,
                    "interpretation": "0 means a new target1 hypothesis is required before GPU work",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "target1_base_weak_exact_count",
                    "value": safe_float(target1_probe.get("target1_base_weak_exact_count"), 0.0),
                    "interpretation": "target1 weak-but-exact base rows represented in the scorecard",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "target1_late_high_accepted_count",
                    "value": safe_float(target1_probe.get("target1_late_high_accepted_count"), 0.0),
                    "interpretation": "late_high rows accepted by the current target1 policy",
                },
            ]
        )
    if detector_handoff:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_handoff_cheapest_full_triples_per_case",
                    "value": safe_float(detector_handoff.get("cheapest_full_candidate_triples_per_case"), 0.0),
                    "interpretation": "candidate-list FWI cost before a waveform gate",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_handoff_best_deployable_all_truth_cases",
                    "value": safe_float(detector_handoff.get("best_deployable_all_truth_case_count"), 0.0),
                    "interpretation": "truth-free detector handoff recovery count across cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_handoff_oracle_all_truth_cases",
                    "value": safe_float(detector_handoff.get("oracle_all_truth_case_count"), 0.0),
                    "interpretation": "oracle upper bound for detector handoff recovery",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_handoff_ready_for_fwi",
                    "value": 1.0 if detector_handoff.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means detector-seeded FWI is not yet a narrow run",
                },
            ]
        )
    if detector_alltriples:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_alltriples_combo_row_count",
                    "value": safe_float(detector_alltriples.get("combo_row_count"), 0.0),
                    "interpretation": "CPU-scored detector triple combinations",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_alltriples_best_top1_all_truth_cases",
                    "value": safe_float(detector_alltriples.get("best_top1_all_truth_case_count"), 0.0),
                    "interpretation": "top-1 all-truth recovery after objective scoring",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_alltriples_best_top10_all_truth_cases",
                    "value": safe_float(detector_alltriples.get("best_top10_case_count"), 0.0),
                    "interpretation": "top-10 all-truth recovery after objective scoring",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_alltriples_best_top50_all_truth_cases",
                    "value": safe_float(detector_alltriples.get("best_top50_case_count"), 0.0),
                    "interpretation": "top-50 all-truth recovery after objective scoring",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_alltriples_ready_for_fwi",
                    "value": 1.0 if detector_alltriples.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means all-triples gating still does not justify FWI",
                },
            ]
        )
    if field_cue_catalog:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_cue_catalog_raw_cue_count",
                    "value": safe_float(field_cue_catalog.get("raw_cue_count"), 0.0),
                    "interpretation": "raw measured-field cue count before support filtering",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_catalog_support_anchor_count",
                    "value": safe_float(field_cue_catalog.get("support_anchor_count"), 0.0),
                    "interpretation": "field cues that have explicit support-tier anchoring",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_catalog_short_content_backed_anchor_count",
                    "value": safe_float(field_cue_catalog.get("short_content_backed_anchor_count"), 0.0),
                    "interpretation": "short-profile content-backed timing anchors",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_catalog_ready_for_field_fwi",
                    "value": 1.0 if field_cue_catalog.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means measured-field cues remain QC only, not inversion-ready",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_catalog_ready_for_3d_hpc",
                    "value": 1.0 if field_cue_catalog.get("ready_for_3d_hpc", False) else 0.0,
                    "interpretation": "0 means the local GSSI dataset does not justify 3D/HPC escalation",
                },
            ]
        )
    if detector_rank_budget:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_rank_budget_minimal_all_case_triples",
                    "value": safe_float(detector_rank_budget.get("minimal_all_case_candidate_triple_budget"), 0.0),
                    "interpretation": "candidate-triple budget needed for all-case detector upper-bound coverage",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_rank_budget_best_top50_cases",
                    "value": safe_float(detector_rank_budget.get("best_top50_case_count"), 0.0),
                    "interpretation": "best simple all-triples objective coverage within top-50",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_rank_budget_max_top1_all_truth_cases",
                    "value": safe_float(detector_rank_budget.get("max_top1_all_truth_case_count"), 0.0),
                    "interpretation": "0 means rank-budget diagnostic is not a deployable selector",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_rank_budget_sparse_all_truth_cases",
                    "value": safe_float(detector_rank_budget.get("sparse_all_truth_case_count"), 0.0),
                    "interpretation": "cases with only one or two all-truth triples in the candidate space",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_rank_budget_ready_for_fwi",
                    "value": 1.0 if detector_rank_budget.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means rank-budget result is an upper-bound study, not FWI-ready",
                },
            ]
        )
    if detector_component_gate:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_gate_component_candidate_count",
                    "value": safe_float(detector_component_gate.get("component_candidate_count"), 0.0),
                    "interpretation": "unique component candidates scored by CPU waveform masks",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_gate_best_top10_cases",
                    "value": safe_float(detector_component_gate.get("best_top10_case_count"), 0.0),
                    "interpretation": "component-gate coverage within top-10",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_gate_best_top50_cases",
                    "value": safe_float(detector_component_gate.get("best_top50_case_count"), 0.0),
                    "interpretation": "component-gate coverage within top-50",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_gate_top50_improvement",
                    "value": safe_float(detector_component_gate.get("top50_improvement_over_source"), 0.0),
                    "interpretation": "top-50 gain over the prior all-triples gate",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_gate_best_top1_cases",
                    "value": safe_float(detector_component_gate.get("best_top1_all_truth_case_count"), 0.0),
                    "interpretation": "0 means component waveform gate is still not deployable top-1",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_gate_ready_for_fwi",
                    "value": 1.0 if detector_component_gate.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means component gate does not justify detector-seeded FWI",
                },
            ]
        )
    if detector_component_selector:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_selector_candidate_count",
                    "value": safe_float(detector_component_selector.get("selector_candidate_count"), 0.0),
                    "interpretation": "truth-free component selector candidates tested",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_selector_best_in_sample_cases",
                    "value": safe_float(detector_component_selector.get("best_in_sample_all_truth_case_count"), 0.0),
                    "interpretation": "best top-1 in-sample all-truth recovery after selector tuning",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_selector_leave_one_case_cases",
                    "value": safe_float(detector_component_selector.get("leave_one_case_all_truth_case_count"), 0.0),
                    "interpretation": "leave-one-case validated top-1 all-truth recovery",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_selector_leave_one_seed_cases",
                    "value": safe_float(detector_component_selector.get("leave_one_seed_all_truth_case_count"), 0.0),
                    "interpretation": "leave-one-seed validated top-1 all-truth recovery",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_selector_ready_for_fwi",
                    "value": 1.0 if detector_component_selector.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means selector audit does not justify detector-seeded FWI",
                },
            ]
        )
    if detector_geometry_selector:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_geometry_selector_candidate_count",
                    "value": safe_float(detector_geometry_selector.get("selector_candidate_count"), 0.0),
                    "interpretation": "branch-family geometry-prior selector candidates tested",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_geometry_selector_best_in_sample_cases",
                    "value": safe_float(detector_geometry_selector.get("best_in_sample_all_truth_case_count"), 0.0),
                    "interpretation": "best in-sample top-1 all-truth recovery with geometry-family priors",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_geometry_selector_leave_one_case_cases",
                    "value": safe_float(detector_geometry_selector.get("leave_one_case_all_truth_case_count"), 0.0),
                    "interpretation": "leave-one-case top-1 all-truth recovery with geometry-family priors",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_geometry_selector_leave_one_case_improvement",
                    "value": safe_float(detector_geometry_selector.get("leave_one_case_improvement_over_component_selector"), 0.0),
                    "interpretation": "validated improvement over the previous component selector",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_geometry_selector_ready_for_fwi",
                    "value": 1.0 if detector_geometry_selector.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means geometry-family selector still does not justify detector-seeded FWI",
                },
            ]
        )
    if detector_selector_gap:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_gap_selected_all_truth_cases",
                    "value": safe_float(detector_selector_gap.get("selected_all_truth_case_count"), 0.0),
                    "interpretation": "top-1 all-truth recovery for the selector being decomposed",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_gap_failed_cases",
                    "value": safe_float(detector_selector_gap.get("failed_selector_case_count"), 0.0),
                    "interpretation": "cases where the truth-free selector still chooses a wrong triple",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_gap_best_truth_available_cases",
                    "value": safe_float(detector_selector_gap.get("best_truth_available_case_count"), 0.0),
                    "interpretation": "cases with an all-truth triple available in the saved candidate space",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_gap_median_required_gain",
                    "value": safe_float(detector_selector_gap.get("median_required_selector_gain_to_choose_truth"), 0.0),
                    "interpretation": "median selector-score gain needed for truth to beat the selected wrong triple",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_gap_max_required_gain",
                    "value": safe_float(detector_selector_gap.get("max_required_selector_gain_to_choose_truth"), 0.0),
                    "interpretation": "largest selector-score gain needed for truth to beat the selected wrong triple",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_gap_ready_for_fwi",
                    "value": 1.0 if detector_selector_gap.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means gap decomposition supports a guardrail, not detector-seeded FWI",
                },
            ]
        )
    if detector_selector_counterfactual:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_counterfactual_variant_count",
                    "value": safe_float(detector_selector_counterfactual.get("counterfactual_variant_count"), 0.0),
                    "interpretation": "simple counterfactual selector reweightings tested",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_counterfactual_best_all_truth_cases",
                    "value": safe_float(detector_selector_counterfactual.get("best_all_truth_case_count"), 0.0),
                    "interpretation": "best top-1 all-truth recovery across counterfactual reweightings",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_counterfactual_improvement_over_base",
                    "value": safe_float(
                        detector_selector_counterfactual.get("best_improvement_over_base_all_truth_cases"), 0.0
                    ),
                    "interpretation": "0 means simple reweighting does not beat the current selector",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_counterfactual_signed_gap_zero_cases",
                    "value": safe_float(
                        detector_selector_counterfactual.get("signed_gap_zero_all_truth_case_count"), 0.0
                    ),
                    "interpretation": "top-1 all-truth cases after removing the signed-gap prior",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_counterfactual_best_median_gain",
                    "value": safe_float(detector_selector_counterfactual.get("best_median_required_selector_gain"), 0.0),
                    "interpretation": "best median selector gain still needed for failed cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_selector_counterfactual_ready_for_fwi",
                    "value": 1.0 if detector_selector_counterfactual.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means counterfactual sensitivity remains a guardrail, not an FWI trigger",
                },
            ]
        )
    if detector_image_objective_rank:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_image_rank_best_top50_cases",
                    "value": safe_float(detector_image_objective_rank.get("best_top50_all_truth_case_count"), 0.0),
                    "interpretation": "cases where image objective ranks first all-truth inside top-50",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_image_rank_best_top200_cases",
                    "value": safe_float(detector_image_objective_rank.get("best_top200_all_truth_case_count"), 0.0),
                    "interpretation": "cases where image objective ranks first all-truth inside top-200",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_image_rank_best_top1000_cases",
                    "value": safe_float(detector_image_objective_rank.get("best_top1000_all_truth_case_count"), 0.0),
                    "interpretation": "cases where image objective ranks first all-truth inside top-1000",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_image_rank_best_median_first_truth_rank",
                    "value": safe_float(detector_image_objective_rank.get("best_median_first_all_truth_rank"), 0.0),
                    "interpretation": "rank depth of first all-truth row under the best image objective",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_image_rank_previous_oracle_cases",
                    "value": safe_float(detector_image_objective_rank.get("previous_oracle_all_truth_case_count"), 0.0),
                    "interpretation": "per-case policy-oracle all-truth cases from the source image-objective context",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_image_rank_ready_for_fwi",
                    "value": 1.0 if detector_image_objective_rank.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means saved image objective does not justify detector-seeded FWI",
                },
            ]
        )
    if detector_target_failure:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_failed_cases",
                    "value": safe_float(detector_target_failure.get("failed_selector_case_count"), 0.0),
                    "interpretation": "cases where the truth-free selector drops at least one target",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_missing_target0_cases",
                    "value": safe_float(detector_target_failure.get("missing_target0_case_count"), 0.0),
                    "interpretation": "selector failures that drop target0",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_missing_target1_cases",
                    "value": safe_float(detector_target_failure.get("missing_target1_case_count"), 0.0),
                    "interpretation": "selector failures that drop target1",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_missing_target2_cases",
                    "value": safe_float(detector_target_failure.get("missing_target2_case_count"), 0.0),
                    "interpretation": "selector failures that drop target2",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_multi_target_cases",
                    "value": safe_float(detector_target_failure.get("multi_target_missing_case_count"), 0.0),
                    "interpretation": "selector failures that drop more than one target",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_target1_median_gain",
                    "value": safe_float(detector_target_failure.get("target1_missing_median_required_selector_gain"), 0.0),
                    "interpretation": "median selector-score gain needed when target1 is dropped",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_target_failure_ready_for_fwi",
                    "value": 1.0 if detector_target_failure.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means target-failure taxonomy remains analysis, not detector-seeded FWI",
                },
            ]
        )
    if detector_depth_slot_prior:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_depth_slot_prior_variant_count",
                    "value": safe_float(detector_depth_slot_prior.get("variant_count"), 0.0),
                    "interpretation": "depth/slot prior variants tested on saved detector rows",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_depth_slot_prior_base_all_truth_cases",
                    "value": safe_float(detector_depth_slot_prior.get("base_all_truth_case_count"), 0.0),
                    "interpretation": "baseline selector all-truth cases before depth/slot priors",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_depth_slot_prior_best_all_truth_cases",
                    "value": safe_float(detector_depth_slot_prior.get("best_all_truth_case_count"), 0.0),
                    "interpretation": "best all-truth cases after broad depth/slot prior probe",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_depth_slot_prior_improvement_cases",
                    "value": safe_float(detector_depth_slot_prior.get("best_improvement_over_base_all_truth_cases"), 0.0),
                    "interpretation": "all-truth case gain from the best depth/slot prior variant",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_depth_slot_prior_best_missing_target1_cases",
                    "value": safe_float(detector_depth_slot_prior.get("best_missing_target1_case_count"), 0.0),
                    "interpretation": "remaining target1 misses under the best depth/slot prior variant",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_depth_slot_prior_ready_for_fwi",
                    "value": 1.0 if detector_depth_slot_prior.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means the prior probe remains feature analysis, not detector-seeded FWI",
                },
            ]
        )
    if detector_slot_component_assembly:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_slot_component_variant_count",
                    "value": safe_float(detector_slot_component_assembly.get("variant_count"), 0.0),
                    "interpretation": "branch-slot component assembly variants tested on saved detector rows",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_slot_component_current_triple_cases",
                    "value": safe_float(
                        detector_slot_component_assembly.get("current_triple_selector_all_truth_case_count"), 0.0
                    ),
                    "interpretation": "current triple selector all-truth cases before slot assembly",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_slot_component_depth_prior_cases",
                    "value": safe_float(
                        detector_slot_component_assembly.get("depth_slot_prior_best_all_truth_case_count"), 0.0
                    ),
                    "interpretation": "best all-truth cases from the prior depth/slot probe",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_slot_component_best_slot_cases",
                    "value": safe_float(detector_slot_component_assembly.get("best_all_target_slot_case_count"), 0.0),
                    "interpretation": "branch-slot upper-bound cases with all target slots hit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_slot_component_min_component_candidates",
                    "value": safe_float(detector_slot_component_assembly.get("min_component_candidate_count"), 0.0),
                    "interpretation": "minimum unique detector components available per case",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_slot_component_ready_for_fwi",
                    "value": 1.0
                    if detector_slot_component_assembly.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means slot assembly is an upper-bound contract, not detector-seeded FWI",
                },
            ]
        )
    if detector_blind_envelope:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_variant_count",
                    "value": safe_float(detector_blind_envelope.get("variant_count"), 0.0),
                    "interpretation": "blind component-envelope variants tested on saved detector rows",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_best_slot_cases",
                    "value": safe_float(detector_blind_envelope.get("best_all_target_slot_case_count"), 0.0),
                    "interpretation": "best truth-free inference cases with all target slots hit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_leave_one_cases",
                    "value": safe_float(
                        detector_blind_envelope.get("leave_one_case_all_target_slot_case_count"), 0.0
                    ),
                    "interpretation": "leave-one-case selected variants with all target slots hit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_known_slot_upper_bound_cases",
                    "value": safe_float(
                        detector_blind_envelope.get("known_slot_component_upper_bound_case_count"), 0.0
                    ),
                    "interpretation": "known-slot component upper-bound cases used as comparison",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_uses_branch_slots",
                    "value": 1.0 if detector_blind_envelope.get("uses_branch_slots_for_selection", False) else 0.0,
                    "interpretation": "0 means inference did not use branch slot coordinates",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_ready_for_fwi",
                    "value": 1.0 if detector_blind_envelope.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means blind envelope assembly remains saved-evidence policy analysis",
                },
            ]
        )
    if detector_blind_envelope_robustness:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_full_success_variants",
                    "value": safe_float(detector_blind_envelope_robustness.get("full_success_variant_count"), 0.0),
                    "interpretation": "blind-envelope variants that recover all saved target slots",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_near_success_variants",
                    "value": safe_float(detector_blind_envelope_robustness.get("near_success_variant_count"), 0.0),
                    "interpretation": "blind-envelope variants within one failed case of full recovery",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_leave_one_seed_cases",
                    "value": safe_float(
                        detector_blind_envelope_robustness.get("leave_one_seed_all_target_slot_case_count"), 0.0
                    ),
                    "interpretation": "held-out seed split cases with all target slots hit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_leave_one_branch_cases",
                    "value": safe_float(
                        detector_blind_envelope_robustness.get("leave_one_branch_all_target_slot_case_count"), 0.0
                    ),
                    "interpretation": "held-out branch split cases with all target slots hit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_leave_one_condition_cases",
                    "value": safe_float(
                        detector_blind_envelope_robustness.get("leave_one_condition_all_target_slot_case_count"), 0.0
                    ),
                    "interpretation": "held-out nominal/source-condition split cases with all target slots hit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_min_margin",
                    "value": safe_float(
                        detector_blind_envelope_robustness.get("best_variant_min_truth_vs_wrong_score_margin"), 0.0
                    ),
                    "interpretation": "minimum selected-truth score margin over the best wrong triple",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_low_margin_cases",
                    "value": safe_float(detector_blind_envelope_robustness.get("best_variant_low_margin_case_count"), 0.0),
                    "interpretation": "cases below the blind-envelope margin review threshold",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_robustness_ready_for_fwi",
                    "value": 1.0
                    if detector_blind_envelope_robustness.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means robustness audit remains saved-evidence detector analysis",
                },
            ]
        )
    if detector_blind_envelope_stability:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_all_variant_cases",
                    "value": safe_float(detector_blind_envelope_stability.get("all_variant_success_case_count"), 0.0),
                    "interpretation": "cases recovered by every saved blind-envelope policy variant",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_partial_cases",
                    "value": safe_float(detector_blind_envelope_stability.get("partial_success_case_count"), 0.0),
                    "interpretation": "cases that depend on policy tuning for target-slot recovery",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_tuning_sensitive_cases",
                    "value": safe_float(detector_blind_envelope_stability.get("tuning_sensitive_case_count"), 0.0),
                    "interpretation": "cases below the saved-grid success-fraction stability threshold",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_min_success_fraction",
                    "value": safe_float(detector_blind_envelope_stability.get("min_success_fraction"), 0.0),
                    "interpretation": "minimum case-level success fraction across blind-envelope variants",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_consensus_cases",
                    "value": safe_float(
                        detector_blind_envelope_stability.get("consensus_single_selection_case_count"), 0.0
                    ),
                    "interpretation": "cases with one successful selected component triple across all successful variants",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_close50_partial_cases",
                    "value": safe_float(detector_blind_envelope_stability.get("close50_partial_success_case_count"), 0.0),
                    "interpretation": "close50 cases that are not stable under all blind-envelope variants",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_max_unique_success_selections",
                    "value": safe_float(detector_blind_envelope_stability.get("max_unique_success_selection_count"), 0.0),
                    "interpretation": "maximum number of distinct successful selected triples for a case",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_stability_ready_for_fwi",
                    "value": 1.0
                    if detector_blind_envelope_stability.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means stability audit remains saved-evidence detector analysis",
                },
            ]
        )
    if detector_blind_envelope_tuning:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_sensitive_cases",
                    "value": safe_float(detector_blind_envelope_tuning.get("tuning_sensitive_case_count"), 0.0),
                    "interpretation": "close50 blind-envelope cases decomposed for policy tuning sensitivity",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_max_knob_effect",
                    "value": safe_float(detector_blind_envelope_tuning.get("max_knob_success_fraction_effect"), 0.0),
                    "interpretation": "largest success-fraction swing across a single policy knob",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_structural_conflict",
                    "value": 1.0
                    if detector_blind_envelope_tuning.get("structural_weight_direction_conflict", False)
                    else 0.0,
                    "interpretation": "1 means best structural-weight direction conflicts across sensitive seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_support_conflict",
                    "value": 1.0
                    if detector_blind_envelope_tuning.get("support_weight_direction_conflict", False)
                    else 0.0,
                    "interpretation": "1 means best support-weight direction conflicts across sensitive seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_span_effect",
                    "value": safe_float(detector_blind_envelope_tuning.get("span_threshold_max_effect"), 0.0),
                    "interpretation": "0 means span threshold does not explain the close50 instability",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_global_fix_ready",
                    "value": 1.0
                    if detector_blind_envelope_tuning.get("ready_for_global_policy_tuning_fix", False)
                    else 0.0,
                    "interpretation": "0 means close50 tuning sensitivity is not resolved by a global knob choice",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_tuning_ready_for_fwi",
                    "value": 1.0
                    if detector_blind_envelope_tuning.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means tuning sensitivity remains CPU-side ambiguity evidence",
                },
            ]
        )
    if detector_blind_envelope_reliability:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_stable_cases",
                    "value": safe_float(
                        detector_blind_envelope_reliability.get("stable_assignment_case_count"), 0.0
                    ),
                    "interpretation": "cases accepted by the truth-free x-slot drift reliability gate",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_review_cases",
                    "value": safe_float(
                        detector_blind_envelope_reliability.get("review_assignment_case_count"), 0.0
                    ),
                    "interpretation": "cases flagged for ambiguity review by the truth-free gate",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_tuning_detected",
                    "value": safe_float(
                        detector_blind_envelope_reliability.get("tuning_sensitive_detected_by_gate_count"), 0.0
                    ),
                    "interpretation": "tuning-sensitive cases caught by the reliability gate",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_tuning_missed",
                    "value": safe_float(
                        detector_blind_envelope_reliability.get("tuning_sensitive_missed_by_gate_count"), 0.0
                    ),
                    "interpretation": "0 means the gate does not miss known tuning-sensitive cases in this corpus",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_stable_min_success_fraction",
                    "value": safe_float(
                        detector_blind_envelope_reliability.get(
                            "stable_assignment_min_success_fraction_truth_eval"
                        ),
                        0.0,
                    ),
                    "interpretation": "post-hoc truth evaluation for cases accepted by the truth-free gate",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_ready_for_claim",
                    "value": 1.0
                    if detector_blind_envelope_reliability.get("ready_for_reliability_claim", False)
                    else 0.0,
                    "interpretation": "1 means the gate is usable as reliability/ambiguity-boundary evidence",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_ready_for_fwi",
                    "value": 1.0
                    if detector_blind_envelope_reliability.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means reliability gate is not a detector-seeded FWI trigger",
                },
            ]
        )
    if detector_blind_envelope_reliability_threshold:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_clean_count",
                    "value": safe_float(
                        detector_blind_envelope_reliability_threshold.get("clean_threshold_count"), 0.0
                    ),
                    "interpretation": "threshold values that separate stable cases from tuning-sensitive cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_clean_min_mm",
                    "value": safe_float(
                        detector_blind_envelope_reliability_threshold.get("clean_threshold_min_mm"), 0.0
                    ),
                    "interpretation": "lower edge of the clean x-slot drift threshold interval",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_clean_max_mm",
                    "value": safe_float(
                        detector_blind_envelope_reliability_threshold.get("clean_threshold_max_mm"), 0.0
                    ),
                    "interpretation": "upper edge of the clean x-slot drift threshold interval",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_default_clean",
                    "value": 1.0
                    if detector_blind_envelope_reliability_threshold.get("default_threshold_clean", False)
                    else 0.0,
                    "interpretation": "1 means the default reliability gate threshold is in the clean interval",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_default_tuning_missed",
                    "value": safe_float(
                        detector_blind_envelope_reliability_threshold.get("default_threshold_tuning_missed"), 0.0
                    ),
                    "interpretation": "known tuning-sensitive cases accepted by the default threshold",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_default_false_review",
                    "value": safe_float(
                        detector_blind_envelope_reliability_threshold.get("default_threshold_false_review"), 0.0
                    ),
                    "interpretation": "stable cases over-reviewed by the default threshold",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_blind_envelope_reliability_threshold_ready_for_fwi",
                    "value": 1.0
                    if detector_blind_envelope_reliability_threshold.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means threshold sensitivity remains CPU-side confidence evidence",
                },
            ]
        )
    if detector_physics_ambiguity_link:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_review_cases",
                    "value": safe_float(detector_physics_ambiguity_link.get("detector_review_case_count"), 0.0),
                    "interpretation": "truth-free detector review cases entering the physics-link audit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_near_boundary_nominal_reviews",
                    "value": safe_float(
                        detector_physics_ambiguity_link.get("review_near_boundary_nominal_count"), 0.0
                    ),
                    "interpretation": "review cases localized to close50 29.5 mm nominal near-boundary rows",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_reviews_all_near_boundary_nominal",
                    "value": 1.0
                    if detector_physics_ambiguity_link.get("detector_reviews_all_near_boundary_nominal", False)
                    else 0.0,
                    "interpretation": "1 means every detector review case is a close50 near-boundary nominal case",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_close50_nominal_review_fraction",
                    "value": safe_float(
                        detector_physics_ambiguity_link.get("close50_linear29p5_nominal_review_fraction"), 0.0
                    ),
                    "interpretation": "fraction of close50 29.5 mm nominal cases flagged for review",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_review_x_ambiguous_cases",
                    "value": safe_float(
                        detector_physics_ambiguity_link.get("review_cases_with_synthetic_x_ambiguity_count"), 0.0
                    ),
                    "interpretation": "review cases also x-ambiguous in the saved coordinate-confidence rows",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_branch_claim_ready",
                    "value": 1.0
                    if detector_physics_ambiguity_link.get("ready_for_branch_localization_claim", False)
                    else 0.0,
                    "interpretation": "1 means the detector review cases can be localized to a branch/variant boundary",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_per_seed_equivalence_ready",
                    "value": 1.0
                    if detector_physics_ambiguity_link.get("ready_for_per_seed_physics_equivalence_claim", False)
                    else 0.0,
                    "interpretation": "0 means per-seed coordinate ambiguity does not explain every detector review",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_physics_link_ready_for_fwi",
                    "value": 1.0
                    if detector_physics_ambiguity_link.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means this is explanatory evidence, not a detector-seeded FWI trigger",
                },
            ]
        )
    if detector_refinement_launch_contract:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_case_count",
                    "value": safe_float(detector_refinement_launch_contract.get("case_count"), 0.0),
                    "interpretation": "saved detector cases entering the refinement launch-contract audit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_seed_table_cases",
                    "value": safe_float(
                        detector_refinement_launch_contract.get("candidate_component_seed_ready_count"), 0.0
                    ),
                    "interpretation": "stable saved-corpus cases exportable as x/z component seed rows",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_review_cases",
                    "value": safe_float(detector_refinement_launch_contract.get("review_case_count"), 0.0),
                    "interpretation": "cases still requiring detector-policy review before any launch contract",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_active_blockers",
                    "value": safe_float(detector_refinement_launch_contract.get("active_blocker_count"), 0.0),
                    "interpretation": "active blockers preventing detector-seeded refinement/FWI",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_radius_seed_available",
                    "value": 1.0
                    if detector_refinement_launch_contract.get("radius_seed_available", False)
                    else 0.0,
                    "interpretation": "0 means detector rows do not yet provide radius seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_material_seed_available",
                    "value": 1.0
                    if detector_refinement_launch_contract.get("material_seed_available", False)
                    else 0.0,
                    "interpretation": "0 means detector rows do not yet provide material seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_ready_seed_table",
                    "value": 1.0
                    if detector_refinement_launch_contract.get("ready_for_component_seed_table", False)
                    else 0.0,
                    "interpretation": "1 means the stable x/z component rows are usable as a saved seed table",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_ready_narrow_refinement",
                    "value": 1.0
                    if detector_refinement_launch_contract.get("ready_for_narrow_refinement_contract", False)
                    else 0.0,
                    "interpretation": "0 means the saved seed table is not yet a narrow refinement contract",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_refinement_contract_ready_for_fwi",
                    "value": 1.0
                    if detector_refinement_launch_contract.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means no detector-seeded FWI is justified by this audit",
                },
            ]
        )
    if detector_component_seed_export:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_seed_exported_cases",
                    "value": safe_float(detector_component_seed_export.get("exported_seed_case_count"), 0.0),
                    "interpretation": "stable detector cases exported as coordinate-only x/z seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_seed_exported_components",
                    "value": safe_float(detector_component_seed_export.get("exported_component_row_count"), 0.0),
                    "interpretation": "component-level x/z seed rows exported for later design",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_seed_excluded_review_cases",
                    "value": safe_float(detector_component_seed_export.get("excluded_review_case_count"), 0.0),
                    "interpretation": "review cases intentionally excluded from the coordinate seed table",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_seed_max_error_mm",
                    "value": safe_float(detector_component_seed_export.get("max_exported_case_seed_error_mm"), 0.0),
                    "interpretation": "maximum saved truth-evaluated x/z seed error among exported cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_seed_ready_coordinate_table",
                    "value": 1.0
                    if detector_component_seed_export.get("ready_for_coordinate_seed_table", False)
                    else 0.0,
                    "interpretation": "1 means the coordinate-only seed table is usable for design",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_component_seed_ready_for_fwi",
                    "value": 1.0
                    if detector_component_seed_export.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means the seed export is not a detector-seeded FWI trigger",
                },
            ]
        )
    if detector_refinement_neighborhood_budget:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_min_half_width_mm",
                    "value": safe_float(
                        detector_refinement_neighborhood_budget.get(
                            "min_lateral_x_half_width_all_stable_seed_cases_mm"
                        ),
                        0.0,
                    ),
                    "interpretation": "lateral x-slot half-width needed to cover all stable exported seed cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_stable_coverage_5mm",
                    "value": safe_float(
                        detector_refinement_neighborhood_budget.get("stable_lateral_x_coverage_at_5mm"), 0.0
                    ),
                    "interpretation": "stable exported cases covered by a 5 mm lateral x-slot half-width",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_stable_coverage_8mm",
                    "value": safe_float(
                        detector_refinement_neighborhood_budget.get("stable_lateral_x_coverage_at_8mm"), 0.0
                    ),
                    "interpretation": "stable exported cases covered by an 8 mm lateral x-slot half-width",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_stable_coverage_10mm",
                    "value": safe_float(
                        detector_refinement_neighborhood_budget.get("stable_lateral_x_coverage_at_10mm"), 0.0
                    ),
                    "interpretation": "stable exported cases covered by a 10 mm lateral x-slot half-width",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_h10_step2_per_case_points",
                    "value": safe_float(
                        detector_refinement_neighborhood_budget.get("per_case_lateral_x_grid_points_h10_step2"), 0.0
                    ),
                    "interpretation": "per-case 3D lateral x-slot tensor points at 10 mm half-width and 2 mm step",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_hypothetical_xz_h10_step2_points",
                    "value": safe_float(
                        detector_refinement_neighborhood_budget.get(
                            "hypothetical_per_case_xz_tensor_points_h10_step2"
                        ),
                        0.0,
                    ),
                    "interpretation": "hypothetical per-case 6D x/z tensor points; z coverage is not validated",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_z_coverage_validated",
                    "value": 1.0
                    if detector_refinement_neighborhood_budget.get("z_coverage_validated", False)
                    else 0.0,
                    "interpretation": "0 means detector z-neighborhood coverage remains unvalidated",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_ready_for_xz",
                    "value": 1.0
                    if detector_refinement_neighborhood_budget.get("ready_for_xz_neighborhood_design", False)
                    else 0.0,
                    "interpretation": "0 means x/z neighborhood design remains blocked",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_lateral_slot_budget_ready_for_fwi",
                    "value": 1.0
                    if detector_refinement_neighborhood_budget.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means the lateral-slot budget does not open detector-seeded FWI",
                },
            ]
        )
    if detector_seed_geometry_error_audit:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_xz_min_half_width_mm",
                    "value": safe_float(
                        detector_seed_geometry_error_audit.get("min_xz_half_width_all_stable_seed_cases_mm"), 0.0
                    ),
                    "interpretation": "matched x/z L-infinity half-width needed to cover stable exported seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_source_lateral_half_width_mm",
                    "value": safe_float(
                        detector_seed_geometry_error_audit.get(
                            "source_lateral_min_half_width_all_stable_seed_cases_mm"
                        ),
                        0.0,
                    ),
                    "interpretation": "earlier lateral x-slot-only half-width for comparison",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_max_stable_x_error_mm",
                    "value": safe_float(detector_seed_geometry_error_audit.get("max_stable_x_error_mm"), 0.0),
                    "interpretation": "maximum matched x error among stable exported detector seed cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_max_stable_z_error_mm",
                    "value": safe_float(detector_seed_geometry_error_audit.get("max_stable_z_error_mm"), 0.0),
                    "interpretation": "maximum matched z error among stable exported detector seed cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_z_exceeds_lateral_count",
                    "value": safe_float(
                        detector_seed_geometry_error_audit.get("stable_cases_z_exceeds_lateral_slot_error_count"), 0.0
                    ),
                    "interpretation": "stable cases where matched z error exceeds lateral slot error",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_stable_xz_coverage_10mm",
                    "value": safe_float(detector_seed_geometry_error_audit.get("stable_xz_coverage_at_10mm"), 0.0),
                    "interpretation": "stable exported cases covered by a 10 mm matched x/z half-width",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_stable_xz_coverage_12mm",
                    "value": safe_float(detector_seed_geometry_error_audit.get("stable_xz_coverage_at_12mm"), 0.0),
                    "interpretation": "stable exported cases covered by a 12 mm matched x/z half-width",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_h12_step2_per_case_points",
                    "value": safe_float(detector_seed_geometry_error_audit.get("per_case_xz_grid_points_h12_step2"), 0.0),
                    "interpretation": "per-case 6D x/z tensor points at 12 mm half-width and 2 mm step",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_ready_xz_seed_neighborhood",
                    "value": 1.0
                    if detector_seed_geometry_error_audit.get("ready_for_xz_seed_neighborhood_design", False)
                    else 0.0,
                    "interpretation": "1 means matched x/z seed-neighborhood sizing is supported",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_seed_geometry_ready_for_fwi",
                    "value": 1.0
                    if detector_seed_geometry_error_audit.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means matched x/z seed sizing does not open detector-seeded FWI",
                },
            ]
        )
    if detector_radius_material_prior_scope:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_source_cases",
                    "value": safe_float(detector_radius_material_prior_scope.get("source_case_count"), 0.0),
                    "interpretation": "saved detector cases audited for controlled synthetic radius/material priors",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_stable_cases",
                    "value": safe_float(
                        detector_radius_material_prior_scope.get("stable_controlled_prior_case_count"), 0.0
                    ),
                    "interpretation": "stable saved cases with controlled synthetic radius/material prior scope",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_review_cases",
                    "value": safe_float(
                        detector_radius_material_prior_scope.get("review_case_excluded_count"), 0.0
                    ),
                    "interpretation": "review cases excluded from controlled-prior use",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_radius_cases",
                    "value": safe_float(detector_radius_material_prior_scope.get("radius_prior_case_count"), 0.0),
                    "interpretation": "cases with known synthetic truth-radius pattern available",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_detector_radius_seeds",
                    "value": safe_float(
                        detector_radius_material_prior_scope.get("detector_radius_seed_available_count"), 0.0
                    ),
                    "interpretation": "0 means the detector itself still does not infer radius seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_detector_material_seeds",
                    "value": safe_float(
                        detector_radius_material_prior_scope.get("detector_material_seed_available_count"), 0.0
                    ),
                    "interpretation": "0 means the detector itself still does not infer material seeds",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_controlled_ready",
                    "value": 1.0
                    if detector_radius_material_prior_scope.get(
                        "ready_for_controlled_synthetic_prior_contract", False
                    )
                    else 0.0,
                    "interpretation": "1 means controlled synthetic radius/material priors are scoped for design",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_detector_inferred_ready",
                    "value": 1.0
                    if detector_radius_material_prior_scope.get(
                        "ready_for_detector_inferred_radius_material_contract", False
                    )
                    else 0.0,
                    "interpretation": "0 means no detector-inferred radius/material claim is supported",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_radius_material_prior_ready_for_fwi",
                    "value": 1.0
                    if detector_radius_material_prior_scope.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means the prior-scope audit is not a detector-seeded FWI trigger",
                },
            ]
        )
    if detector_controlled_prior_refinement_budget:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_fixed_fine_points",
                    "value": safe_float(
                        detector_controlled_prior_refinement_budget.get(
                            "fixed_slot_radii_stable_total_points_fine"
                        ),
                        0.0,
                    ),
                    "interpretation": "stable-case fine x/z coordinate-radius points with fixed slot radii",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_fixed_coarse_points",
                    "value": safe_float(
                        detector_controlled_prior_refinement_budget.get(
                            "fixed_slot_radii_stable_total_points_coarse"
                        ),
                        0.0,
                    ),
                    "interpretation": "stable-case coarse x/z coordinate-radius points with fixed slot radii",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_permutation_fine_points",
                    "value": safe_float(
                        detector_controlled_prior_refinement_budget.get(
                            "known_radius_permutations_stable_total_points_fine"
                        ),
                        0.0,
                    ),
                    "interpretation": "stable-case fine points if known radii are permuted across slots",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_independent_fine_points",
                    "value": safe_float(
                        detector_controlled_prior_refinement_budget.get(
                            "independent_known_radius_choices_stable_total_points_fine"
                        ),
                        0.0,
                    ),
                    "interpretation": "stable-case fine points for independent per-slot known-radius choices",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_permutation_multiplier",
                    "value": safe_float(
                        detector_controlled_prior_refinement_budget.get("permutation_vs_fixed_multiplier"), 0.0
                    ),
                    "interpretation": "radius-permutation cost multiplier over fixed slot radii",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_independent_multiplier",
                    "value": safe_float(
                        detector_controlled_prior_refinement_budget.get("independent_vs_fixed_multiplier"), 0.0
                    ),
                    "interpretation": "independent known-radius choice cost multiplier over fixed slot radii",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_fixed_budget_ready",
                    "value": 1.0
                    if detector_controlled_prior_refinement_budget.get(
                        "ready_for_controlled_fixed_radius_budget", False
                    )
                    else 0.0,
                    "interpretation": "1 means fixed-radius controlled-prior budget sizing is usable",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_permutation_budget_ready",
                    "value": 1.0
                    if detector_controlled_prior_refinement_budget.get(
                        "ready_for_known_radius_permutation_budget", False
                    )
                    else 0.0,
                    "interpretation": "1 means radius permutations are usable for cost comparison only",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_independent_search_ready",
                    "value": 1.0
                    if detector_controlled_prior_refinement_budget.get("ready_for_independent_radius_search", False)
                    else 0.0,
                    "interpretation": "0 means independent per-slot radius tensor search remains blocked",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_launch_ready",
                    "value": 1.0
                    if detector_controlled_prior_refinement_budget.get("ready_for_refinement_launch", False)
                    else 0.0,
                    "interpretation": "0 means the budget is not a refinement launch contract",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_controlled_prior_refinement_ready_for_fwi",
                    "value": 1.0
                    if detector_controlled_prior_refinement_budget.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means controlled-prior budgeting does not open detector-seeded FWI",
                },
            ]
        )
    if detector_fixed_radius_pilot_outcome:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_pilot_outcome_run_count",
                    "value": safe_float(detector_fixed_radius_pilot_outcome.get("pilot_run_count"), 0.0),
                    "interpretation": "completed controlled fixed-radius detector refinement pilots",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_pilot_best_final_linf_mm",
                    "value": safe_float(detector_fixed_radius_pilot_outcome.get("best_final_linf_mm"), 0.0),
                    "interpretation": "best final x/z L-infinity residual across fixed-radius pilots",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_pilot_within_one_mm_count",
                    "value": safe_float(
                        detector_fixed_radius_pilot_outcome.get("within_one_mm_residual_pilot_count"),
                        0.0,
                    ),
                    "interpretation": "pilots ending within 1 mm but not exact",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_pilot_second_pass_ready",
                    "value": 1.0
                    if detector_fixed_radius_pilot_outcome.get(
                        "ready_for_single_guarded_second_pass_probe", False
                    )
                    else 0.0,
                    "interpretation": "0 means the completed second pass closed the immediate GPU action",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_pilot_broad_gpu_ready",
                    "value": 1.0
                    if detector_fixed_radius_pilot_outcome.get("ready_for_broad_gpu_queue", False)
                    else 0.0,
                    "interpretation": "0 means no broad fixed-radius detector queue is open",
                },
            ]
        )
    if detector_fixed_radius_residual_ambiguity:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_residual_final_linf_mm",
                    "value": safe_float(detector_fixed_radius_residual_ambiguity.get("final_linf_error_mm"), 0.0),
                    "interpretation": "post-second-pass fixed-radius residual after candidate audit",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_residual_truth_selected_ambiguous",
                    "value": safe_float(
                        detector_fixed_radius_residual_ambiguity.get("truth_selected_but_ambiguous_count"),
                        0.0,
                    ),
                    "interpretation": "targets where truth wins but has a near competitor",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_residual_objective_neighbor",
                    "value": safe_float(
                        detector_fixed_radius_residual_ambiguity.get(
                            "truth_present_but_objective_prefers_neighbor_count"
                        ),
                        0.0,
                    ),
                    "interpretation": "targets where truth is present but a neighbor has lower objective",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_residual_nonoverlap_absent",
                    "value": safe_float(
                        detector_fixed_radius_residual_ambiguity.get(
                            "truth_absent_after_nonoverlap_filter_count"
                        ),
                        0.0,
                    ),
                    "interpretation": "targets where exact truth is absent after sequential non-overlap filtering",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_residual_immediate_gpu_ready",
                    "value": 1.0
                    if detector_fixed_radius_residual_ambiguity.get(
                        "ready_for_immediate_gpu_iteration", False
                    )
                    else 0.0,
                    "interpretation": "0 means residual cause requires CPU policy design before more GPU",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_residual_guard_max_gpu_util_percent",
                    "value": safe_float(
                        detector_fixed_radius_residual_ambiguity.get("guard_max_gpu_util_percent"), 0.0
                    ),
                    "interpretation": "guard-observed GPU utilization for the second-pass pilot",
                },
            ]
        )
    if detector_fixed_radius_locking_validation:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_final_linf_mm",
                    "value": safe_float(
                        detector_fixed_radius_locking_validation.get("final_linf_error_mm"),
                        0.0,
                    ),
                    "interpretation": "post-locking guarded target2 unlock probe final x/z residual",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_exact",
                    "value": 1.0
                    if detector_fixed_radius_locking_validation.get("exact_geometry_recovered", False)
                    else 0.0,
                    "interpretation": "1 means the single locked-branch validation recovered exact geometry",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_mechanism_ready",
                    "value": 1.0
                    if detector_fixed_radius_locking_validation.get(
                        "ready_for_locking_mechanism_claim", False
                    )
                    else 0.0,
                    "interpretation": "1 means the result supports only the fixed-radius locking mechanism claim",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_general_policy_ready",
                    "value": 1.0
                    if detector_fixed_radius_locking_validation.get(
                        "ready_for_general_detector_policy_claim", False
                    )
                    else 0.0,
                    "interpretation": "0 means this is not a deployable general detector-policy claim",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_broad_gpu_ready",
                    "value": 1.0
                    if detector_fixed_radius_locking_validation.get("ready_for_broad_gpu_queue", False)
                    else 0.0,
                    "interpretation": "0 means the validation closes the guarded GPU action instead of opening a queue",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_guard_max_gpu_util_percent",
                    "value": safe_float(
                        detector_fixed_radius_locking_validation.get("guard_max_gpu_util_percent"),
                        0.0,
                    ),
                    "interpretation": "guard-observed GPU utilization for the single unlock validation",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_fixed_radius_locking_validation_guard_max_ram_percent",
                    "value": safe_float(
                        detector_fixed_radius_locking_validation.get("guard_max_ram_used_percent"),
                        0.0,
                    ),
                    "interpretation": "guard-observed RAM utilization for the single unlock validation",
                },
            ]
        )
    if detector_sampling_boundary_integration:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_review_cases",
                    "value": safe_float(detector_sampling_boundary_integration.get("detector_review_case_count"), 0.0),
                    "interpretation": "detector reliability review cases after linking to close50 sampling boundary",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_review_below_clean_cases",
                    "value": safe_float(
                        detector_sampling_boundary_integration.get("review_below_clean_case_count"), 0.0
                    ),
                    "interpretation": "review cases below the 30 mm clean threshold",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_close50_nominal_review_cases",
                    "value": safe_float(
                        detector_sampling_boundary_integration.get("close50_nominal_review_case_count"), 0.0
                    ),
                    "interpretation": "close50 linear 29.5 mm nominal rows flagged for detector review",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_close50_source_mismatch_review_cases",
                    "value": safe_float(
                        detector_sampling_boundary_integration.get("close50_source_mismatch_review_case_count"), 0.0
                    ),
                    "interpretation": "source-mismatch rows at the same offset flagged for detector review",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_claim_ready",
                    "value": 1.0
                    if detector_sampling_boundary_integration.get(
                        "ready_for_detector_sampling_boundary_claim", False
                    )
                    else 0.0,
                    "interpretation": "1 means detector reviews are localized to the branch sampling boundary",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_per_seed_equivalence_ready",
                    "value": 1.0
                    if detector_sampling_boundary_integration.get("per_seed_physics_equivalence_ready", False)
                    else 0.0,
                    "interpretation": "0 means the detector caveat is branch-local rather than per-seed equivalent",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_sampling_boundary_ready_for_fwi",
                    "value": 1.0
                    if detector_sampling_boundary_integration.get("ready_for_detector_seeded_fwi", False)
                    else 0.0,
                    "interpretation": "0 means no detector-seeded FWI or GPU probe is opened",
                },
            ]
        )
    if detector_upper_bound:
        rows.extend(
            [
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_upper_bound_minimal_all_case_triples",
                    "value": safe_float(detector_upper_bound.get("minimal_all_case_rank_gated_triples_per_case"), 0.0),
                    "interpretation": "minimal rank-gated detector budget that covers all saved cases",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_upper_bound_all_truth_cases",
                    "value": safe_float(detector_upper_bound.get("best_rank_gated_upper_bound_all_truth_case_count"), 0.0),
                    "interpretation": "all-truth cases covered by the best rank-gated upper-bound strategy",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_upper_bound_ready_for_claim",
                    "value": 1.0 if detector_upper_bound.get("ready_for_rank_gated_upper_bound_claim", False) else 0.0,
                    "interpretation": "1 means detector evidence has a paper-safe upper-bound role",
                },
                {
                    "domain": "synthetic_2d",
                    "metric": "detector_upper_bound_ready_for_fwi",
                    "value": 1.0 if detector_upper_bound.get("ready_for_detector_seeded_fwi", False) else 0.0,
                    "interpretation": "0 means upper-bound policy does not justify detector-seeded FWI",
                },
            ]
        )
    if field_cue_timing_envelope:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_cue_timing_short_inside_envelope_count",
                    "value": safe_float(field_cue_timing_envelope.get("short_anchor_inside_envelope_count"), 0.0),
                    "interpretation": "short relative-timing anchors inside the conservative envelope",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_timing_short_content_inside_envelope_count",
                    "value": safe_float(field_cue_timing_envelope.get("short_content_anchor_inside_envelope_count"), 0.0),
                    "interpretation": "content-backed short anchors inside the conservative envelope",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_timing_long_reject_short_transfer_count",
                    "value": safe_float(field_cue_timing_envelope.get("long_pattern_reject_short_transfer_count"), 0.0),
                    "interpretation": "long pattern anchors outside the short-transfer timing envelope",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_timing_ready_for_short_qc",
                    "value": 1.0 if field_cue_timing_envelope.get("ready_for_short_relative_timing_qc", False) else 0.0,
                    "interpretation": "1 means short-pair relative timing QC remains supported",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_cue_timing_ready_for_field_fwi",
                    "value": 1.0 if field_cue_timing_envelope.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means timing envelope remains field QC only",
                },
            ]
        )
    if field_spatial_transfer:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_spatial_transfer_short_covered_count",
                    "value": safe_float(
                        field_spatial_transfer.get("short_content_with_nearest_long_within_threshold_count"), 0.0
                    ),
                    "interpretation": "short content anchors spatially covered by a long pattern anchor",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_spatial_transfer_long_covered_count",
                    "value": safe_float(
                        field_spatial_transfer.get("long_pattern_with_nearest_short_content_within_threshold_count"), 0.0
                    ),
                    "interpretation": "long pattern anchors spatially covered by a short content anchor",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_spatial_transfer_median_long_distance_mm",
                    "value": safe_float(field_spatial_transfer.get("median_long_to_short_distance_mm"), 0.0),
                    "interpretation": "median nearest short-content distance for long pattern anchors",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_spatial_transfer_ready_for_transfer",
                    "value": 1.0 if field_spatial_transfer.get("ready_for_short_to_long_timing_transfer", False) else 0.0,
                    "interpretation": "0 means short timing cannot be transferred to long profiles",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_spatial_transfer_ready_for_field_fwi",
                    "value": 1.0 if field_spatial_transfer.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means spatial-transfer audit does not justify field FWI",
                },
            ]
        )
    if field_anchor_interval:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_anchor_interval_short_inside_count",
                    "value": safe_float(field_anchor_interval.get("short_anchor_inside_supported_interval_count"), 0.0),
                    "interpretation": "short timing anchors inside all-window supported intervals",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_anchor_interval_content_inside_count",
                    "value": safe_float(
                        field_anchor_interval.get("short_content_anchor_inside_supported_interval_count"), 0.0
                    ),
                    "interpretation": "content-backed short anchors inside all-window supported intervals",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_anchor_interval_min_margin_mm",
                    "value": safe_float(field_anchor_interval.get("min_margin_to_supported_interval_edge_mm"), 0.0),
                    "interpretation": "minimum anchor margin to supported interval edge",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_anchor_interval_ready_for_short_qc",
                    "value": 1.0 if field_anchor_interval.get("ready_for_short_relative_timing_qc", False) else 0.0,
                    "interpretation": "1 means short relative timing anchors coincide with supported intervals",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_anchor_interval_ready_for_field_fwi",
                    "value": 1.0 if field_anchor_interval.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means interval reconciliation does not justify field FWI",
                },
            ]
        )
    if field_dimensionality:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_dimensionality_is_3d_survey",
                    "value": 1.0 if field_dimensionality.get("is_3d_survey", False) else 0.0,
                    "interpretation": "0 means the local GSSI dataset remains independent 2D line profiles",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_dimensionality_ready_for_short_qc",
                    "value": 1.0 if field_dimensionality.get("ready_for_short_relative_timing_qc", False) else 0.0,
                    "interpretation": "1 means short-profile relative timing QC is supported",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_dimensionality_ready_for_long_transfer",
                    "value": 1.0 if field_dimensionality.get("ready_for_long_short_transfer", False) else 0.0,
                    "interpretation": "0 means short timing should not be transferred to long profiles",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_dimensionality_ready_for_3d_hpc",
                    "value": 1.0 if field_dimensionality.get("ready_for_3d_hpc", False) else 0.0,
                    "interpretation": "0 means no field-data 3D/HPC job should be submitted",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_dimensionality_ready_for_field_fwi",
                    "value": 1.0 if field_dimensionality.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means measured-field FWI remains blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_dimensionality_decision_gate_count",
                    "value": safe_float(field_dimensionality.get("decision_gate_count"), 0.0),
                    "interpretation": "decision gates represented in the field dimensionality card",
                },
            ]
        )
    if field_time_zero_ladder:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ready_short_qc",
                    "value": 1.0 if field_time_zero_ladder.get("ready_for_short_relative_timing_qc", False) else 0.0,
                    "interpretation": "1 means the consolidated field ladder supports short-profile relative timing QC",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ready_long_transfer",
                    "value": 1.0 if field_time_zero_ladder.get("ready_for_long_short_transfer", False) else 0.0,
                    "interpretation": "0 means short timing should not be transferred to long profiles",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ready_content_only_short_qc",
                    "value": 1.0 if field_time_zero_ladder.get("ready_for_content_only_short_qc", False) else 0.0,
                    "interpretation": "1 means content-backed short anchors support the relative timing QC claim",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ready_leave_one_content_anchor",
                    "value": 1.0
                    if field_time_zero_ladder.get("ready_for_leave_one_content_anchor_claim", False)
                    else 0.0,
                    "interpretation": "0 means the field short-timing claim is not leave-one-content redundant",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ready_absolute_t0",
                    "value": 1.0 if field_time_zero_ladder.get("ready_for_absolute_time_zero", False) else 0.0,
                    "interpretation": "0 means the field data do not support absolute time-zero calibration",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ready_field_fwi",
                    "value": 1.0 if field_time_zero_ladder.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means the field ladder remains QC-only, not FWI-ready",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_short_half_width_ns",
                    "value": safe_float(field_time_zero_ladder.get("short_conservative_half_width_ns"), 0.0),
                    "interpretation": "conservative half-width for short relative timing QC",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_content_half_range_ns",
                    "value": safe_float(field_time_zero_ladder.get("content_only_offset_half_range_ns"), 0.0),
                    "interpretation": "content-only short-anchor timing half-range after dropping the timing-only cue",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_time_zero_ladder_ladder_row_count",
                    "value": safe_float(field_time_zero_ladder.get("ladder_row_count"), 0.0),
                    "interpretation": "number of evidence gates represented in the consolidated ladder",
                },
            ]
        )
    if field_short_anchor_leave_one:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_leave_one_content_only_supported",
                    "value": 1.0 if field_short_anchor_leave_one.get("content_only_supported", False) else 0.0,
                    "interpretation": "1 means the two content-backed short anchors support relative timing without the timing-only cue",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_leave_one_supported_cases",
                    "value": safe_float(field_short_anchor_leave_one.get("leave_one_supported_count"), 0.0),
                    "interpretation": "leave-one subsets that preserve content-redundant short relative timing support",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_leave_one_degraded_cases",
                    "value": safe_float(
                        field_short_anchor_leave_one.get("leave_one_degraded_single_content_count"), 0.0
                    ),
                    "interpretation": "leave-one subsets degraded to a single content-backed short anchor",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_leave_one_content_half_range_ns",
                    "value": safe_float(field_short_anchor_leave_one.get("content_only_offset_half_range_ns"), 0.0),
                    "interpretation": "content-only short-anchor relative timing half-range",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_leave_one_ready_field_fwi",
                    "value": 1.0 if field_short_anchor_leave_one.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means the leave-one audit remains field-QC evidence, not field FWI readiness",
                },
            ]
        )
    if field_short_anchor_spatial_consistency:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_content_residual_range_mm",
                    "value": safe_float(
                        field_short_anchor_spatial_consistency.get("content_residual_range_mm"), 0.0
                    ),
                    "interpretation": "signed x-residual span for content-backed short anchors",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_content_residual_half_range_mm",
                    "value": safe_float(
                        field_short_anchor_spatial_consistency.get("content_residual_half_range_mm"), 0.0
                    ),
                    "interpretation": "half-range of content-backed short-anchor spatial residuals",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_content_min_margin_mm",
                    "value": safe_float(
                        field_short_anchor_spatial_consistency.get("content_min_supported_interval_margin_mm"), 0.0
                    ),
                    "interpretation": "minimum supported-interval margin for content-backed anchors",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_single_translation_supported",
                    "value": 1.0
                    if field_short_anchor_spatial_consistency.get("content_single_translation_supported", False)
                    else 0.0,
                    "interpretation": "0 means short anchors do not support calibrated profile translation",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_ready_short_qc",
                    "value": 1.0
                    if field_short_anchor_spatial_consistency.get("ready_for_short_relative_timing_qc", False)
                    else 0.0,
                    "interpretation": "1 means short relative timing QC remains supported",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_ready_spatial_calibration",
                    "value": 1.0
                    if field_short_anchor_spatial_consistency.get(
                        "ready_for_profile_spatial_calibration", False
                    )
                    else 0.0,
                    "interpretation": "0 means do not use short anchors for profile spatial calibration",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_spatial_ready_field_fwi",
                    "value": 1.0
                    if field_short_anchor_spatial_consistency.get("ready_for_field_fwi", False)
                    else 0.0,
                    "interpretation": "0 means spatial audit does not justify field FWI",
                },
            ]
        )
    if field_inversion_readiness:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_gate_count",
                    "value": safe_float(field_inversion_readiness.get("gate_count"), 0.0),
                    "interpretation": "field readiness gates synthesized after spatial-consistency audit",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_supported_gates",
                    "value": safe_float(field_inversion_readiness.get("supported_gate_count"), 0.0),
                    "interpretation": "field gates still supported after current guardrails",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_blocked_gates",
                    "value": safe_float(field_inversion_readiness.get("blocked_gate_count"), 0.0),
                    "interpretation": "field heavy-work gates blocked after current guardrails",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_short_qc",
                    "value": 1.0
                    if field_inversion_readiness.get("ready_for_short_relative_timing_qc", False)
                    else 0.0,
                    "interpretation": "1 means short-profile relative timing QC is still allowed",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_depth_scale_qc",
                    "value": 1.0
                    if field_inversion_readiness.get("ready_for_apparent_depth_scale_qc", False)
                    else 0.0,
                    "interpretation": "1 means apparent-depth scale QC is still allowed",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_long_transfer",
                    "value": 1.0
                    if field_inversion_readiness.get("ready_for_long_profile_transfer", False)
                    else 0.0,
                    "interpretation": "0 means short-to-long profile timing transfer is blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_spatial_calibration",
                    "value": 1.0
                    if field_inversion_readiness.get("ready_for_profile_spatial_calibration", False)
                    else 0.0,
                    "interpretation": "0 means a single profile spatial calibration is blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_cover_depth",
                    "value": 1.0
                    if field_inversion_readiness.get("ready_for_cover_depth_recovery", False)
                    else 0.0,
                    "interpretation": "0 means calibrated cover-depth recovery is blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_radius",
                    "value": 1.0
                    if field_inversion_readiness.get("ready_for_radius_recovery", False)
                    else 0.0,
                    "interpretation": "0 means field radius recovery is blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_field_fwi",
                    "value": 1.0 if field_inversion_readiness.get("ready_for_field_fwi", False) else 0.0,
                    "interpretation": "0 means field FWI is blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_ready_3d_hpc",
                    "value": 1.0 if field_inversion_readiness.get("ready_for_3d_hpc", False) else 0.0,
                    "interpretation": "0 means field 3D/HPC is blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_inversion_readiness_apparent_depth_span_mm",
                    "value": safe_float(field_inversion_readiness.get("apparent_depth_max_span_mm"), 0.0),
                    "interpretation": "absolute apparent-depth span across field scale assumptions",
                },
            ]
        )
    if field_short_anchor_radius_degeneracy:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_radius_degeneracy_weak_sides",
                    "value": safe_float(field_short_anchor_radius_degeneracy.get("weak_radius_side_count"), 0.0),
                    "interpretation": "content-backed sides with weak radius separation in saved waveform grids",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_radius_degeneracy_mismatch_pairs",
                    "value": safe_float(
                        field_short_anchor_radius_degeneracy.get("selected_radius_mismatch_pair_count"), 0.0
                    ),
                    "interpretation": "content-backed pairs where selected repeat-profile radii disagree",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_radius_degeneracy_common_near_tie_pairs",
                    "value": safe_float(
                        field_short_anchor_radius_degeneracy.get("common_radius_near_tie_pair_count"), 0.0
                    ),
                    "interpretation": "pairs where forced common-radius alternatives are near-tied",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_radius_degeneracy_ready_morphology_qc",
                    "value": 1.0
                    if field_short_anchor_radius_degeneracy.get("ready_for_waveform_morphology_qc", False)
                    else 0.0,
                    "interpretation": "1 means field waveform morphology QC remains supported",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_radius_degeneracy_ready_radius_seed",
                    "value": 1.0
                    if field_short_anchor_radius_degeneracy.get("ready_for_radius_seed", False)
                    else 0.0,
                    "interpretation": "0 means field radius seeding remains blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_radius_degeneracy_ready_field_fwi",
                    "value": 1.0
                    if field_short_anchor_radius_degeneracy.get("ready_for_field_fwi", False)
                    else 0.0,
                    "interpretation": "0 means field FWI remains blocked",
                },
            ]
        )
    if field_short_anchor_signed_morphology:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_morphology_supported_pairs",
                    "value": safe_float(
                        field_short_anchor_signed_morphology.get("signed_morphology_supported_pair_count"),
                        0.0,
                    ),
                    "interpretation": "content-backed short-anchor pairs passing signed morphology QC",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_morphology_same_polarity_pairs",
                    "value": safe_float(
                        field_short_anchor_signed_morphology.get("corrected_same_polarity_pair_count"),
                        0.0,
                    ),
                    "interpretation": "corrected content-backed pairs with same signed polarity",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_morphology_min_signed_corr",
                    "value": safe_float(
                        field_short_anchor_signed_morphology.get("min_corrected_signed_correlation"), 0.0
                    ),
                    "interpretation": "minimum corrected signed field-trace correlation",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_morphology_ready_qc",
                    "value": 1.0
                    if field_short_anchor_signed_morphology.get(
                        "ready_for_signed_waveform_morphology_qc", False
                    )
                    else 0.0,
                    "interpretation": "1 means signed waveform morphology QC is supported",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_morphology_ready_amplitude_calibration",
                    "value": 1.0
                    if field_short_anchor_signed_morphology.get(
                        "ready_for_absolute_amplitude_calibration", False
                    )
                    else 0.0,
                    "interpretation": "0 means robust-normalized traces are not amplitude calibration",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_morphology_ready_field_fwi",
                    "value": 1.0
                    if field_short_anchor_signed_morphology.get("ready_for_field_fwi", False)
                    else 0.0,
                    "interpretation": "0 means signed morphology QC is not field FWI evidence",
                },
            ]
        )
    if field_short_anchor_signed_morphology_sensitivity:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_sensitivity_threshold_combos",
                    "value": safe_float(
                        field_short_anchor_signed_morphology_sensitivity.get("threshold_combo_count"), 0.0
                    ),
                    "interpretation": "signed-morphology threshold combinations swept",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_sensitivity_supported_combos",
                    "value": safe_float(
                        field_short_anchor_signed_morphology_sensitivity.get(
                            "all_pairs_supported_threshold_combo_count"
                        ),
                        0.0,
                    ),
                    "interpretation": "threshold combinations where all content-backed pairs pass",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_sensitivity_moderate_ready",
                    "value": 1.0
                    if field_short_anchor_signed_morphology_sensitivity.get(
                        "ready_for_moderate_threshold_morphology_qc", False
                    )
                    else 0.0,
                    "interpretation": "1 means the signed morphology result survives moderate threshold tightening",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_sensitivity_strict_ready",
                    "value": 1.0
                    if field_short_anchor_signed_morphology_sensitivity.get(
                        "ready_for_strict_morphology_claim", False
                    )
                    else 0.0,
                    "interpretation": "0 means strict signed morphology claims remain blocked",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_sensitivity_corr_limit",
                    "value": safe_float(
                        field_short_anchor_signed_morphology_sensitivity.get(
                            "support_limit_corrected_signed_correlation"
                        ),
                        0.0,
                    ),
                    "interpretation": "minimum corrected signed-correlation support limit",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_short_anchor_signed_sensitivity_ready_field_fwi",
                    "value": 1.0
                    if field_short_anchor_signed_morphology_sensitivity.get("ready_for_field_fwi", False)
                    else 0.0,
                    "interpretation": "0 means threshold sensitivity is not field FWI evidence",
                },
            ]
        )
    if field_collection_handoff:
        rows.extend(
            [
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_action_count",
                    "value": safe_float(field_collection_handoff.get("handoff_action_count"), 0.0),
                    "interpretation": "controlled-collection action groups in the current field handoff",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_critical_new_data_actions",
                    "value": safe_float(field_collection_handoff.get("critical_new_data_action_count"), 0.0),
                    "interpretation": "new controlled-data groups required before field inversion",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_packet_rows_needing_entry",
                    "value": safe_float(field_collection_handoff.get("packet_rows_needing_entry"), 0.0),
                    "interpretation": "planned packet rows that still need measured collection entries",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_failed_acceptance_gates",
                    "value": safe_float(field_collection_handoff.get("failed_acceptance_gate_count"), 0.0),
                    "interpretation": "acceptance gates still blocked before packet acceptance",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_reference_uncertainty_gate_ns",
                    "value": safe_float(field_collection_handoff.get("reference_uncertainty_gate_ns"), 0.0),
                    "interpretation": "time-zero reference uncertainty gate for the next controlled field pass",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_ready_collection_day",
                    "value": 1.0 if field_collection_handoff.get("ready_for_collection_day", False) else 0.0,
                    "interpretation": "1 means the run sheet is ready for collection, not packet acceptance",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_ready_packet_acceptance",
                    "value": 1.0 if field_collection_handoff.get("ready_for_packet_acceptance", False) else 0.0,
                    "interpretation": "0 means the packet still needs controlled measurements",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_ready_field_fwi",
                    "value": 1.0 if field_collection_handoff.get("ready_for_current_archive_field_fwi", False) else 0.0,
                    "interpretation": "0 means the current archive still does not support field FWI",
                },
                {
                    "domain": "field_2d",
                    "metric": "field_collection_handoff_ready_3d_hpc",
                    "value": 1.0 if field_collection_handoff.get("ready_for_field_3d_hpc", False) else 0.0,
                    "interpretation": "0 means the local field archive is not a 3D/HPC workload",
                },
            ]
        )
    return rows


def summarize_table_pack(
    claim_rows: list[dict],
    figure_rows: list[dict],
    metrics: list[dict],
    synthetic_summary: dict,
    synthetic_next: dict,
    field_summary: dict,
    field_policy: dict,
    audit_summary: dict,
    synthetic_source_notes: dict | None = None,
    field_source_notes: dict | None = None,
    target1_probe_summary: dict | None = None,
    detector_handoff_summary: dict | None = None,
    detector_alltriples_summary: dict | None = None,
    field_cue_catalog_summary: dict | None = None,
    detector_rank_budget_summary: dict | None = None,
    detector_component_gate_summary: dict | None = None,
    detector_component_selector_summary: dict | None = None,
    detector_geometry_selector_summary: dict | None = None,
    detector_selector_gap_summary: dict | None = None,
    detector_selector_counterfactual_summary: dict | None = None,
    detector_image_objective_rank_summary: dict | None = None,
    detector_target_failure_summary: dict | None = None,
    detector_depth_slot_prior_summary: dict | None = None,
    detector_slot_component_assembly_summary: dict | None = None,
    detector_blind_envelope_summary: dict | None = None,
    detector_blind_envelope_robustness_summary: dict | None = None,
    detector_blind_envelope_stability_summary: dict | None = None,
    detector_blind_envelope_tuning_summary: dict | None = None,
    detector_blind_envelope_reliability_summary: dict | None = None,
    detector_blind_envelope_reliability_threshold_summary: dict | None = None,
    detector_physics_ambiguity_link_summary: dict | None = None,
    detector_refinement_launch_contract_summary: dict | None = None,
    detector_component_seed_export_summary: dict | None = None,
    detector_refinement_neighborhood_budget_summary: dict | None = None,
    detector_seed_geometry_error_audit_summary: dict | None = None,
    detector_upper_bound_summary: dict | None = None,
    field_cue_timing_envelope_summary: dict | None = None,
    field_spatial_transfer_summary: dict | None = None,
    field_anchor_interval_summary: dict | None = None,
    field_dimensionality_summary: dict | None = None,
    field_time_zero_ladder_summary: dict | None = None,
    field_short_anchor_leave_one_summary: dict | None = None,
    field_short_anchor_spatial_consistency_summary: dict | None = None,
    field_inversion_readiness_summary: dict | None = None,
    detector_sampling_boundary_integration_summary: dict | None = None,
    field_short_anchor_radius_degeneracy_summary: dict | None = None,
    field_short_anchor_signed_morphology_summary: dict | None = None,
    field_short_anchor_signed_morphology_sensitivity_summary: dict | None = None,
    field_collection_handoff_summary: dict | None = None,
    detector_radius_material_prior_scope_summary: dict | None = None,
    detector_controlled_prior_refinement_budget_summary: dict | None = None,
    detector_fixed_radius_pilot_outcome_synthesis_summary: dict | None = None,
    detector_fixed_radius_residual_ambiguity_audit_summary: dict | None = None,
    detector_fixed_radius_locking_policy_validation_summary: dict | None = None,
) -> dict:
    synthetic_notes = synthetic_source_notes or {}
    synthetic_source_note_count = safe_float(synthetic_notes.get("source_figure_count"), 0.0)
    synthetic_source_notes_present = safe_float(synthetic_notes.get("notes_present_after_count"), 0.0)
    synthetic_source_notes_ready = (
        not synthetic_notes
        or (
            bool(synthetic_notes.get("ready_for_manuscript_handoff", False))
            and synthetic_source_note_count == safe_float(synthetic_summary.get("figure_count"))
            and synthetic_source_notes_present == synthetic_source_note_count
        )
    )
    source_notes = field_source_notes or {}
    source_note_count = safe_float(source_notes.get("source_figure_count"), 0.0)
    source_notes_present = safe_float(source_notes.get("notes_present_after_count"), 0.0)
    source_notes_ready = (
        not source_notes
        or (
            bool(source_notes.get("ready_for_manuscript_handoff", False))
            and source_note_count == safe_float(field_summary.get("figure_row_count"))
            and source_notes_present == source_note_count
        )
    )
    target1_probe = target1_probe_summary or {}
    detector_handoff = detector_handoff_summary or {}
    detector_alltriples = detector_alltriples_summary or {}
    field_cue_catalog = field_cue_catalog_summary or {}
    detector_rank_budget = detector_rank_budget_summary or {}
    detector_component_gate = detector_component_gate_summary or {}
    detector_component_selector = detector_component_selector_summary or {}
    detector_geometry_selector = detector_geometry_selector_summary or {}
    detector_selector_gap = detector_selector_gap_summary or {}
    detector_selector_counterfactual = detector_selector_counterfactual_summary or {}
    detector_image_objective_rank = detector_image_objective_rank_summary or {}
    detector_target_failure = detector_target_failure_summary or {}
    detector_depth_slot_prior = detector_depth_slot_prior_summary or {}
    detector_slot_component_assembly = detector_slot_component_assembly_summary or {}
    detector_blind_envelope = detector_blind_envelope_summary or {}
    detector_blind_envelope_robustness = detector_blind_envelope_robustness_summary or {}
    detector_blind_envelope_stability = detector_blind_envelope_stability_summary or {}
    detector_blind_envelope_tuning = detector_blind_envelope_tuning_summary or {}
    detector_blind_envelope_reliability = detector_blind_envelope_reliability_summary or {}
    detector_blind_envelope_reliability_threshold = detector_blind_envelope_reliability_threshold_summary or {}
    detector_physics_ambiguity_link = detector_physics_ambiguity_link_summary or {}
    detector_refinement_launch_contract = detector_refinement_launch_contract_summary or {}
    detector_component_seed_export = detector_component_seed_export_summary or {}
    detector_refinement_neighborhood_budget = detector_refinement_neighborhood_budget_summary or {}
    detector_seed_geometry_error_audit = detector_seed_geometry_error_audit_summary or {}
    detector_upper_bound = detector_upper_bound_summary or {}
    field_cue_timing_envelope = field_cue_timing_envelope_summary or {}
    field_spatial_transfer = field_spatial_transfer_summary or {}
    field_anchor_interval = field_anchor_interval_summary or {}
    field_dimensionality = field_dimensionality_summary or {}
    field_time_zero_ladder = field_time_zero_ladder_summary or {}
    field_short_anchor_leave_one = field_short_anchor_leave_one_summary or {}
    field_short_anchor_spatial_consistency = field_short_anchor_spatial_consistency_summary or {}
    field_inversion_readiness = field_inversion_readiness_summary or {}
    detector_sampling_boundary_integration = detector_sampling_boundary_integration_summary or {}
    field_short_anchor_radius_degeneracy = field_short_anchor_radius_degeneracy_summary or {}
    field_short_anchor_signed_morphology = field_short_anchor_signed_morphology_summary or {}
    field_short_anchor_signed_morphology_sensitivity = (
        field_short_anchor_signed_morphology_sensitivity_summary or {}
    )
    field_collection_handoff = field_collection_handoff_summary or {}
    detector_radius_material_prior_scope = detector_radius_material_prior_scope_summary or {}
    detector_controlled_prior_refinement_budget = detector_controlled_prior_refinement_budget_summary or {}
    detector_fixed_radius_pilot_outcome = detector_fixed_radius_pilot_outcome_synthesis_summary or {}
    detector_fixed_radius_residual_ambiguity = detector_fixed_radius_residual_ambiguity_audit_summary or {}
    detector_fixed_radius_locking_validation = detector_fixed_radius_locking_policy_validation_summary or {}
    target1_probe_guard_ready = (
        not target1_probe
        or (
            not bool(target1_probe.get("ready_for_target1_gpu_probe", False))
            and safe_float(target1_probe.get("gpu_action_count"), 0.0) == 0.0
        )
    )
    detector_handoff_guard_ready = (
        not detector_handoff or not bool(detector_handoff.get("ready_for_detector_seeded_fwi", False))
    )
    detector_alltriples_guard_ready = (
        not detector_alltriples or not bool(detector_alltriples.get("ready_for_detector_seeded_fwi", False))
    )
    field_cue_catalog_guard_ready = (
        not field_cue_catalog
        or (
            bool(field_cue_catalog.get("ready_for_2d_qc", False))
            and not bool(field_cue_catalog.get("ready_for_absolute_time_zero", False))
            and not bool(field_cue_catalog.get("ready_for_field_fwi", False))
            and not bool(field_cue_catalog.get("ready_for_3d_hpc", False))
        )
    )
    detector_rank_budget_guard_ready = (
        not detector_rank_budget or not bool(detector_rank_budget.get("ready_for_detector_seeded_fwi", False))
    )
    detector_component_gate_guard_ready = (
        not detector_component_gate or not bool(detector_component_gate.get("ready_for_detector_seeded_fwi", False))
    )
    detector_component_selector_guard_ready = (
        not detector_component_selector or not bool(detector_component_selector.get("ready_for_detector_seeded_fwi", False))
    )
    detector_geometry_selector_guard_ready = (
        not detector_geometry_selector or not bool(detector_geometry_selector.get("ready_for_detector_seeded_fwi", False))
    )
    detector_selector_gap_guard_ready = (
        not detector_selector_gap or not bool(detector_selector_gap.get("ready_for_detector_seeded_fwi", False))
    )
    detector_selector_counterfactual_guard_ready = (
        not detector_selector_counterfactual
        or not bool(detector_selector_counterfactual.get("ready_for_detector_seeded_fwi", False))
    )
    detector_image_objective_rank_guard_ready = (
        not detector_image_objective_rank
        or not bool(detector_image_objective_rank.get("ready_for_detector_seeded_fwi", False))
    )
    detector_target_failure_guard_ready = (
        not detector_target_failure
        or not bool(detector_target_failure.get("ready_for_detector_seeded_fwi", False))
    )
    detector_depth_slot_prior_guard_ready = (
        not detector_depth_slot_prior
        or not bool(detector_depth_slot_prior.get("ready_for_detector_seeded_fwi", False))
    )
    detector_slot_component_assembly_guard_ready = (
        not detector_slot_component_assembly
        or not bool(detector_slot_component_assembly.get("ready_for_detector_seeded_fwi", False))
    )
    detector_blind_envelope_guard_ready = (
        not detector_blind_envelope
        or (
            not bool(detector_blind_envelope.get("ready_for_detector_seeded_fwi", False))
            and not bool(detector_blind_envelope.get("uses_branch_slots_for_selection", False))
        )
    )
    detector_blind_envelope_robustness_guard_ready = (
        not detector_blind_envelope_robustness
        or not bool(detector_blind_envelope_robustness.get("ready_for_detector_seeded_fwi", False))
    )
    detector_blind_envelope_stability_guard_ready = (
        not detector_blind_envelope_stability
        or not bool(detector_blind_envelope_stability.get("ready_for_detector_seeded_fwi", False))
    )
    detector_blind_envelope_tuning_guard_ready = (
        not detector_blind_envelope_tuning
        or (
            not bool(detector_blind_envelope_tuning.get("ready_for_global_policy_tuning_fix", False))
            and not bool(detector_blind_envelope_tuning.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_blind_envelope_reliability_guard_ready = (
        not detector_blind_envelope_reliability
        or (
            bool(detector_blind_envelope_reliability.get("ready_for_reliability_claim", False))
            and not bool(detector_blind_envelope_reliability.get("truth_free_gate_uses_truth", True))
            and bool(detector_blind_envelope_reliability.get("truth_evaluation_used_for_audit", False))
            and safe_float(detector_blind_envelope_reliability.get("tuning_sensitive_missed_by_gate_count"), 0.0)
            == 0.0
            and not bool(detector_blind_envelope_reliability.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_blind_envelope_reliability_threshold_guard_ready = (
        not detector_blind_envelope_reliability_threshold
        or (
            bool(detector_blind_envelope_reliability_threshold.get("ready_for_reliability_claim", False))
            and bool(detector_blind_envelope_reliability_threshold.get("default_threshold_clean", False))
            and safe_float(
                detector_blind_envelope_reliability_threshold.get("default_threshold_tuning_missed"), 0.0
            )
            == 0.0
            and safe_float(
                detector_blind_envelope_reliability_threshold.get("default_threshold_false_review"), 0.0
            )
            == 0.0
            and not bool(
                detector_blind_envelope_reliability_threshold.get("ready_for_detector_seeded_fwi", False)
            )
        )
    )
    detector_physics_ambiguity_link_guard_ready = (
        not detector_physics_ambiguity_link
        or (
            bool(detector_physics_ambiguity_link.get("ready_for_branch_localization_claim", False))
            and bool(detector_physics_ambiguity_link.get("detector_reviews_all_near_boundary_nominal", False))
            and not bool(detector_physics_ambiguity_link.get("ready_for_global_detector_tuning", False))
            and not bool(detector_physics_ambiguity_link.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_refinement_launch_contract_guard_ready = (
        not detector_refinement_launch_contract
        or (
            bool(detector_refinement_launch_contract.get("ready_for_component_seed_table", False))
            and safe_float(detector_refinement_launch_contract.get("candidate_component_seed_ready_count"), 0.0)
            > 0.0
            and safe_float(detector_refinement_launch_contract.get("active_blocker_count"), 0.0) > 0.0
            and not bool(detector_refinement_launch_contract.get("radius_seed_available", False))
            and not bool(detector_refinement_launch_contract.get("material_seed_available", False))
            and not bool(detector_refinement_launch_contract.get("ready_for_narrow_refinement_contract", False))
            and not bool(detector_refinement_launch_contract.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_component_seed_export_guard_ready = (
        not detector_component_seed_export
        or (
            bool(detector_component_seed_export.get("ready_for_coordinate_seed_table", False))
            and safe_float(detector_component_seed_export.get("exported_seed_case_count"), 0.0) > 0.0
            and not bool(detector_component_seed_export.get("ready_for_radius_material_contract", False))
            and not bool(detector_component_seed_export.get("ready_for_narrow_refinement_contract", False))
            and not bool(detector_component_seed_export.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_refinement_neighborhood_budget_guard_ready = (
        not detector_refinement_neighborhood_budget
        or (
            bool(detector_refinement_neighborhood_budget.get("ready_for_lateral_x_slot_neighborhood_design", False))
            and safe_float(
                detector_refinement_neighborhood_budget.get(
                    "min_lateral_x_half_width_all_stable_seed_cases_mm"
                ),
                0.0,
            )
            > 0.0
            and not bool(detector_refinement_neighborhood_budget.get("z_coverage_validated", False))
            and not bool(detector_refinement_neighborhood_budget.get("ready_for_xz_neighborhood_design", False))
            and not bool(detector_refinement_neighborhood_budget.get("ready_for_radius_material_contract", False))
            and not bool(detector_refinement_neighborhood_budget.get("ready_for_narrow_refinement_contract", False))
            and not bool(
                detector_refinement_neighborhood_budget.get("ready_for_naive_full_tensor_refinement", False)
            )
            and not bool(detector_refinement_neighborhood_budget.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_seed_geometry_error_audit_guard_ready = (
        not detector_seed_geometry_error_audit
        or (
            bool(detector_seed_geometry_error_audit.get("ready_for_xz_seed_neighborhood_design", False))
            and safe_float(
                detector_seed_geometry_error_audit.get("min_xz_half_width_all_stable_seed_cases_mm"), 0.0
            )
            > safe_float(
                detector_seed_geometry_error_audit.get(
                    "source_lateral_min_half_width_all_stable_seed_cases_mm"
                ),
                0.0,
            )
            and not bool(detector_seed_geometry_error_audit.get("ready_for_radius_material_contract", False))
            and not bool(detector_seed_geometry_error_audit.get("ready_for_narrow_refinement_contract", False))
            and not bool(detector_seed_geometry_error_audit.get("ready_for_naive_full_tensor_refinement", False))
            and not bool(detector_seed_geometry_error_audit.get("ready_for_detector_seeded_fwi", False))
        )
    )
    detector_radius_material_prior_scope_guard_ready = (
        not detector_radius_material_prior_scope
        or (
            bool(
                detector_radius_material_prior_scope.get(
                    "ready_for_controlled_synthetic_prior_contract", False
                )
            )
            and safe_float(
                detector_radius_material_prior_scope.get("stable_controlled_prior_case_count"), 0.0
            )
            > 0.0
            and not bool(
                detector_radius_material_prior_scope.get(
                    "ready_for_detector_inferred_radius_material_contract", False
                )
            )
            and not bool(detector_radius_material_prior_scope.get("ready_for_field_transfer", False))
            and not bool(detector_radius_material_prior_scope.get("ready_for_narrow_refinement_launch", False))
            and not bool(detector_radius_material_prior_scope.get("ready_for_detector_seeded_fwi", False))
            and not bool(detector_radius_material_prior_scope.get("ready_for_gpu_work", False))
        )
    )
    detector_controlled_prior_refinement_budget_guard_ready = (
        not detector_controlled_prior_refinement_budget
        or (
            bool(
                detector_controlled_prior_refinement_budget.get(
                    "ready_for_controlled_fixed_radius_budget", False
                )
            )
            and bool(
                detector_controlled_prior_refinement_budget.get(
                    "ready_for_known_radius_permutation_budget", False
                )
            )
            and safe_float(
                detector_controlled_prior_refinement_budget.get(
                    "fixed_slot_radii_stable_total_points_fine"
                ),
                0.0,
            )
            > 0.0
            and not bool(
                detector_controlled_prior_refinement_budget.get(
                    "ready_for_independent_radius_search", False
                )
            )
            and not bool(detector_controlled_prior_refinement_budget.get("ready_for_refinement_launch", False))
            and not bool(detector_controlled_prior_refinement_budget.get("ready_for_detector_seeded_fwi", False))
            and not bool(detector_controlled_prior_refinement_budget.get("ready_for_gpu_work", False))
        )
    )
    detector_fixed_radius_pilot_outcome_guard_ready = (
        not detector_fixed_radius_pilot_outcome
        or (
            safe_float(detector_fixed_radius_pilot_outcome.get("pilot_run_count"), 0.0) >= 3.0
            and safe_float(detector_fixed_radius_pilot_outcome.get("best_final_linf_mm"), math.inf) <= 1.0
            and safe_float(
                detector_fixed_radius_pilot_outcome.get("within_one_mm_residual_pilot_count"),
                0.0,
            )
            >= 1.0
            and not bool(
                detector_fixed_radius_pilot_outcome.get(
                    "ready_for_single_guarded_second_pass_probe", False
                )
            )
            and not bool(detector_fixed_radius_pilot_outcome.get("ready_for_broad_gpu_queue", False))
            and not bool(detector_fixed_radius_pilot_outcome.get("ready_for_detector_seeded_fwi", False))
            and not bool(detector_fixed_radius_pilot_outcome.get("ready_for_field_transfer", False))
            and not bool(
                detector_fixed_radius_pilot_outcome.get(
                    "ready_for_detector_inferred_radius_material", False
                )
            )
        )
    )
    detector_fixed_radius_residual_ambiguity_guard_ready = (
        not detector_fixed_radius_residual_ambiguity
        or (
            safe_float(detector_fixed_radius_residual_ambiguity.get("final_linf_error_mm"), math.inf)
            <= 1.0
            and safe_float(
                detector_fixed_radius_residual_ambiguity.get(
                    "truth_present_but_objective_prefers_neighbor_count"
                ),
                0.0,
            )
            >= 1.0
            and safe_float(
                detector_fixed_radius_residual_ambiguity.get(
                    "truth_absent_after_nonoverlap_filter_count"
                ),
                0.0,
            )
            >= 1.0
            and not bool(
                detector_fixed_radius_residual_ambiguity.get("ready_for_immediate_gpu_iteration", False)
            )
            and not bool(detector_fixed_radius_residual_ambiguity.get("ready_for_broad_gpu_queue", False))
            and not bool(detector_fixed_radius_residual_ambiguity.get("ready_for_detector_seeded_fwi", False))
            and not bool(detector_fixed_radius_residual_ambiguity.get("ready_for_field_transfer", False))
            and not bool(detector_fixed_radius_residual_ambiguity.get("guard_aborted", False))
            and safe_float(
                detector_fixed_radius_residual_ambiguity.get("guard_max_gpu_util_percent"), 0.0
            )
            <= 90.0
            and safe_float(
                detector_fixed_radius_residual_ambiguity.get("guard_max_ram_used_percent"), 0.0
            )
            <= 80.0
        )
    )
    detector_fixed_radius_locking_validation_guard_ready = (
        not detector_fixed_radius_locking_validation
        or (
            bool(detector_fixed_radius_locking_validation.get("exact_geometry_recovered", False))
            and bool(detector_fixed_radius_locking_validation.get("guard_within_caps", False))
            and bool(
                detector_fixed_radius_locking_validation.get(
                    "ready_for_locking_mechanism_claim", False
                )
            )
            and not bool(
                detector_fixed_radius_locking_validation.get(
                    "ready_for_general_detector_policy_claim", False
                )
            )
            and not bool(detector_fixed_radius_locking_validation.get("ready_for_broad_gpu_queue", False))
            and not bool(
                detector_fixed_radius_locking_validation.get("ready_for_detector_seeded_fwi", False)
            )
            and not bool(detector_fixed_radius_locking_validation.get("ready_for_field_transfer", False))
            and not bool(detector_fixed_radius_locking_validation.get("guard_aborted", False))
            and safe_float(
                detector_fixed_radius_locking_validation.get("guard_max_gpu_util_percent"),
                0.0,
            )
            <= 90.0
            and safe_float(
                detector_fixed_radius_locking_validation.get("guard_max_ram_used_percent"),
                0.0,
            )
            <= 80.0
        )
    )
    detector_sampling_boundary_integration_guard_ready = (
        not detector_sampling_boundary_integration
        or (
            bool(detector_sampling_boundary_integration.get("ready_for_detector_sampling_boundary_claim", False))
            and not bool(detector_sampling_boundary_integration.get("per_seed_physics_equivalence_ready", False))
            and not bool(detector_sampling_boundary_integration.get("ready_for_detector_seeded_fwi", False))
            and not bool(detector_sampling_boundary_integration.get("ready_for_gpu_probe", False))
        )
    )
    detector_upper_bound_guard_ready = (
        not detector_upper_bound or not bool(detector_upper_bound.get("ready_for_detector_seeded_fwi", False))
    )
    field_cue_timing_guard_ready = (
        not field_cue_timing_envelope
        or (
            bool(field_cue_timing_envelope.get("ready_for_short_relative_timing_qc", False))
            and not bool(field_cue_timing_envelope.get("ready_for_long_short_transfer", False))
            and not bool(field_cue_timing_envelope.get("ready_for_absolute_time_zero", False))
            and not bool(field_cue_timing_envelope.get("ready_for_field_fwi", False))
            and not bool(field_cue_timing_envelope.get("ready_for_3d_hpc", False))
        )
    )
    field_spatial_transfer_guard_ready = (
        not field_spatial_transfer
        or (
            not bool(field_spatial_transfer.get("ready_for_short_to_long_timing_transfer", False))
            and not bool(field_spatial_transfer.get("ready_for_absolute_time_zero", False))
            and not bool(field_spatial_transfer.get("ready_for_field_fwi", False))
            and not bool(field_spatial_transfer.get("ready_for_3d_hpc", False))
        )
    )
    field_anchor_interval_guard_ready = (
        not field_anchor_interval
        or (
            bool(field_anchor_interval.get("ready_for_short_relative_timing_qc", False))
            and not bool(field_anchor_interval.get("ready_for_absolute_time_zero", False))
            and not bool(field_anchor_interval.get("ready_for_field_fwi", False))
            and not bool(field_anchor_interval.get("ready_for_3d_hpc", False))
        )
    )
    field_dimensionality_guard_ready = (
        not field_dimensionality
        or (
            bool(field_dimensionality.get("ready_for_2d_qc", False))
            and bool(field_dimensionality.get("ready_for_short_relative_timing_qc", False))
            and not bool(field_dimensionality.get("ready_for_long_short_transfer", False))
            and not bool(field_dimensionality.get("is_3d_survey", False))
            and not bool(field_dimensionality.get("ready_for_3d_hpc", False))
            and not bool(field_dimensionality.get("ready_for_field_fwi", False))
        )
    )
    field_time_zero_ladder_guard_ready = (
        not field_time_zero_ladder
        or (
            bool(field_time_zero_ladder.get("ready_for_short_relative_timing_qc", False))
            and (
                "ready_for_content_only_short_qc" not in field_time_zero_ladder
                or bool(field_time_zero_ladder.get("ready_for_content_only_short_qc", False))
            )
            and not bool(field_time_zero_ladder.get("ready_for_leave_one_content_anchor_claim", False))
            and not bool(field_time_zero_ladder.get("ready_for_long_short_transfer", False))
            and not bool(field_time_zero_ladder.get("ready_for_absolute_time_zero", False))
            and not bool(field_time_zero_ladder.get("ready_for_field_fwi", False))
            and not bool(field_time_zero_ladder.get("ready_for_3d_hpc", False))
        )
    )
    field_short_anchor_leave_one_guard_ready = (
        not field_short_anchor_leave_one
        or (
            bool(field_short_anchor_leave_one.get("ready_for_short_relative_timing_qc", False))
            and not bool(field_short_anchor_leave_one.get("ready_for_absolute_time_zero", False))
            and not bool(field_short_anchor_leave_one.get("ready_for_field_fwi", False))
            and not bool(field_short_anchor_leave_one.get("ready_for_3d_hpc", False))
        )
    )
    field_short_anchor_spatial_consistency_guard_ready = (
        not field_short_anchor_spatial_consistency
        or (
            bool(field_short_anchor_spatial_consistency.get("ready_for_short_relative_timing_qc", False))
            and not bool(field_short_anchor_spatial_consistency.get("content_single_translation_supported", False))
            and not bool(field_short_anchor_spatial_consistency.get("ready_for_profile_spatial_calibration", False))
            and not bool(field_short_anchor_spatial_consistency.get("ready_for_absolute_time_zero", False))
            and not bool(field_short_anchor_spatial_consistency.get("ready_for_field_fwi", False))
            and not bool(field_short_anchor_spatial_consistency.get("ready_for_3d_hpc", False))
        )
    )
    field_inversion_readiness_guard_ready = (
        not field_inversion_readiness
        or (
            bool(field_inversion_readiness.get("ready_for_short_relative_timing_qc", False))
            and bool(field_inversion_readiness.get("ready_for_apparent_depth_scale_qc", False))
            and not bool(field_inversion_readiness.get("ready_for_long_profile_transfer", False))
            and not bool(field_inversion_readiness.get("ready_for_profile_spatial_calibration", False))
            and not bool(field_inversion_readiness.get("ready_for_cover_depth_recovery", False))
            and not bool(field_inversion_readiness.get("ready_for_radius_recovery", False))
            and not bool(field_inversion_readiness.get("ready_for_field_fwi", False))
            and not bool(field_inversion_readiness.get("ready_for_3d_hpc", False))
            and not bool(field_inversion_readiness.get("ready_for_heavy_field_work", False))
        )
    )
    field_short_anchor_radius_degeneracy_guard_ready = (
        not field_short_anchor_radius_degeneracy
        or (
            bool(field_short_anchor_radius_degeneracy.get("ready_for_waveform_morphology_qc", False))
            and not bool(field_short_anchor_radius_degeneracy.get("ready_for_radius_seed", False))
            and not bool(field_short_anchor_radius_degeneracy.get("ready_for_radius_recovery", False))
            and not bool(field_short_anchor_radius_degeneracy.get("ready_for_geometry_seed", False))
            and not bool(field_short_anchor_radius_degeneracy.get("ready_for_field_fwi", False))
            and not bool(field_short_anchor_radius_degeneracy.get("ready_for_3d_hpc", False))
            and not bool(field_short_anchor_radius_degeneracy.get("ready_for_heavy_field_work", False))
        )
    )
    field_short_anchor_signed_morphology_guard_ready = (
        not field_short_anchor_signed_morphology
        or (
            bool(field_short_anchor_signed_morphology.get("ready_for_signed_waveform_morphology_qc", False))
            and not bool(
                field_short_anchor_signed_morphology.get("ready_for_absolute_amplitude_calibration", False)
            )
            and not bool(field_short_anchor_signed_morphology.get("ready_for_radius_seed", False))
            and not bool(field_short_anchor_signed_morphology.get("ready_for_geometry_seed", False))
            and not bool(field_short_anchor_signed_morphology.get("ready_for_field_fwi", False))
            and not bool(field_short_anchor_signed_morphology.get("ready_for_3d_hpc", False))
            and not bool(field_short_anchor_signed_morphology.get("ready_for_heavy_field_work", False))
        )
    )
    field_short_anchor_signed_morphology_sensitivity_guard_ready = (
        not field_short_anchor_signed_morphology_sensitivity
        or (
            bool(
                field_short_anchor_signed_morphology_sensitivity.get(
                    "ready_for_default_signed_morphology_qc", False
                )
            )
            and bool(
                field_short_anchor_signed_morphology_sensitivity.get(
                    "ready_for_moderate_threshold_morphology_qc", False
                )
            )
            and not bool(
                field_short_anchor_signed_morphology_sensitivity.get(
                    "ready_for_strict_morphology_claim", False
                )
            )
            and not bool(
                field_short_anchor_signed_morphology_sensitivity.get(
                    "ready_for_absolute_amplitude_calibration", False
                )
            )
            and not bool(field_short_anchor_signed_morphology_sensitivity.get("ready_for_radius_seed", False))
            and not bool(field_short_anchor_signed_morphology_sensitivity.get("ready_for_geometry_seed", False))
            and not bool(field_short_anchor_signed_morphology_sensitivity.get("ready_for_field_fwi", False))
            and not bool(field_short_anchor_signed_morphology_sensitivity.get("ready_for_3d_hpc", False))
            and not bool(field_short_anchor_signed_morphology_sensitivity.get("ready_for_heavy_field_work", False))
        )
    )
    field_collection_handoff_guard_ready = (
        not field_collection_handoff
        or (
            bool(field_collection_handoff.get("ready_for_collection_day", False))
            and bool(field_collection_handoff.get("ready_for_current_archive_field_qc_supplement", False))
            and not bool(field_collection_handoff.get("ready_for_packet_acceptance", False))
            and not bool(field_collection_handoff.get("ready_for_current_archive_field_fwi", False))
            and not bool(field_collection_handoff.get("ready_for_current_archive_heavy_field_work", False))
            and not bool(field_collection_handoff.get("ready_for_field_3d_hpc", False))
        )
    )
    no_gpu = (
        no_gpu_value(synthetic_summary.get("gpu_priority", ""))
        and no_gpu_value(synthetic_next.get("gpu_priority", ""))
        and no_gpu_value(field_summary.get("gpu_priority", ""))
        and no_gpu_value(field_policy.get("publication_claim_bundle_gpu_priority", ""))
        and no_gpu_value(audit_summary.get("gpu_priority", ""))
        and no_gpu_value(synthetic_notes.get("gpu_priority", ""))
        and no_gpu_value(source_notes.get("gpu_priority", ""))
        and no_gpu_value(target1_probe.get("gpu_priority", ""))
        and no_gpu_value(detector_handoff.get("gpu_priority", ""))
        and no_gpu_value(detector_alltriples.get("gpu_priority", ""))
        and no_gpu_value(field_cue_catalog.get("gpu_priority", ""))
        and no_gpu_value(detector_rank_budget.get("gpu_priority", ""))
        and no_gpu_value(detector_component_gate.get("gpu_priority", ""))
        and no_gpu_value(detector_component_selector.get("gpu_priority", ""))
        and no_gpu_value(detector_geometry_selector.get("gpu_priority", ""))
        and no_gpu_value(detector_selector_gap.get("gpu_priority", ""))
        and no_gpu_value(detector_selector_counterfactual.get("gpu_priority", ""))
        and no_gpu_value(detector_image_objective_rank.get("gpu_priority", ""))
        and no_gpu_value(detector_target_failure.get("gpu_priority", ""))
        and no_gpu_value(detector_depth_slot_prior.get("gpu_priority", ""))
        and no_gpu_value(detector_slot_component_assembly.get("gpu_priority", ""))
        and no_gpu_value(detector_blind_envelope.get("gpu_priority", ""))
        and no_gpu_value(detector_blind_envelope_robustness.get("gpu_priority", ""))
        and no_gpu_value(detector_blind_envelope_stability.get("gpu_priority", ""))
        and no_gpu_value(detector_blind_envelope_tuning.get("gpu_priority", ""))
        and no_gpu_value(detector_blind_envelope_reliability.get("gpu_priority", ""))
        and no_gpu_value(detector_blind_envelope_reliability_threshold.get("gpu_priority", ""))
        and no_gpu_value(detector_physics_ambiguity_link.get("gpu_priority", ""))
        and no_gpu_value(detector_refinement_launch_contract.get("gpu_priority", ""))
        and no_gpu_value(detector_component_seed_export.get("gpu_priority", ""))
        and no_gpu_value(detector_refinement_neighborhood_budget.get("gpu_priority", ""))
        and no_gpu_value(detector_seed_geometry_error_audit.get("gpu_priority", ""))
        and no_gpu_value(detector_radius_material_prior_scope.get("gpu_priority", ""))
        and no_gpu_value(detector_controlled_prior_refinement_budget.get("gpu_priority", ""))
        and no_gpu_value(detector_fixed_radius_pilot_outcome.get("gpu_priority", ""))
        and no_gpu_value(detector_fixed_radius_residual_ambiguity.get("gpu_priority", ""))
        and no_gpu_value(detector_fixed_radius_locking_validation.get("gpu_priority", ""))
        and no_gpu_value(detector_sampling_boundary_integration.get("gpu_priority", ""))
        and no_gpu_value(detector_upper_bound.get("gpu_priority", ""))
        and no_gpu_value(field_cue_timing_envelope.get("gpu_priority", ""))
        and no_gpu_value(field_spatial_transfer.get("gpu_priority", ""))
        and no_gpu_value(field_anchor_interval.get("gpu_priority", ""))
        and no_gpu_value(field_dimensionality.get("field_hpc_priority", ""))
        and no_gpu_value(field_time_zero_ladder.get("gpu_priority", ""))
        and no_gpu_value(field_short_anchor_leave_one.get("gpu_priority", ""))
        and no_gpu_value(field_short_anchor_spatial_consistency.get("gpu_priority", ""))
        and no_gpu_value(field_inversion_readiness.get("gpu_priority", ""))
        and no_gpu_value(field_short_anchor_radius_degeneracy.get("gpu_priority", ""))
        and no_gpu_value(field_short_anchor_signed_morphology.get("gpu_priority", ""))
        and no_gpu_value(field_short_anchor_signed_morphology_sensitivity.get("gpu_priority", ""))
        and no_gpu_value(field_collection_handoff.get("gpu_priority", ""))
    )
    ready = (
        bool(synthetic_summary.get("ready_for_manuscript_draft", False))
        and bool(field_summary.get("ready_for_manuscript_field_supplement", False))
        and bool(audit_summary.get("ready_for_manuscript_planning", False))
        and synthetic_source_notes_ready
        and source_notes_ready
        and target1_probe_guard_ready
        and detector_handoff_guard_ready
        and detector_alltriples_guard_ready
        and field_cue_catalog_guard_ready
        and detector_rank_budget_guard_ready
        and detector_component_gate_guard_ready
        and detector_component_selector_guard_ready
        and detector_geometry_selector_guard_ready
        and detector_selector_gap_guard_ready
        and detector_selector_counterfactual_guard_ready
        and detector_image_objective_rank_guard_ready
        and detector_target_failure_guard_ready
        and detector_depth_slot_prior_guard_ready
        and detector_slot_component_assembly_guard_ready
        and detector_blind_envelope_guard_ready
        and detector_blind_envelope_robustness_guard_ready
        and detector_blind_envelope_stability_guard_ready
        and detector_blind_envelope_tuning_guard_ready
        and detector_blind_envelope_reliability_guard_ready
        and detector_blind_envelope_reliability_threshold_guard_ready
        and detector_physics_ambiguity_link_guard_ready
        and detector_refinement_launch_contract_guard_ready
        and detector_component_seed_export_guard_ready
        and detector_refinement_neighborhood_budget_guard_ready
        and detector_seed_geometry_error_audit_guard_ready
        and detector_radius_material_prior_scope_guard_ready
        and detector_controlled_prior_refinement_budget_guard_ready
        and detector_fixed_radius_pilot_outcome_guard_ready
        and detector_fixed_radius_residual_ambiguity_guard_ready
        and detector_fixed_radius_locking_validation_guard_ready
        and detector_sampling_boundary_integration_guard_ready
        and detector_upper_bound_guard_ready
        and field_cue_timing_guard_ready
        and field_spatial_transfer_guard_ready
        and field_anchor_interval_guard_ready
        and field_dimensionality_guard_ready
        and field_time_zero_ladder_guard_ready
        and field_short_anchor_leave_one_guard_ready
        and field_short_anchor_spatial_consistency_guard_ready
        and field_inversion_readiness_guard_ready
        and field_short_anchor_radius_degeneracy_guard_ready
        and field_short_anchor_signed_morphology_guard_ready
        and field_short_anchor_signed_morphology_sensitivity_guard_ready
        and field_collection_handoff_guard_ready
        and no_gpu
        and len(claim_rows) == safe_float(audit_summary.get("claim_boundary_row_count"))
        and len(figure_rows) == safe_float(audit_summary.get("figure_audit_row_count"))
    )
    return {
        "policy_label": (
            "local_2d_field_manuscript_table_pack_ready_no_gpu"
            if ready
            else "local_2d_field_manuscript_table_pack_review_required"
        ),
        "claim_table_row_count": len(claim_rows),
        "figure_inventory_row_count": len(figure_rows),
        "metric_row_count": len(metrics),
        "synthetic_claim_count": sum(1 for row in claim_rows if row["domain"] == "synthetic_2d"),
        "field_claim_count": sum(1 for row in claim_rows if row["domain"] == "field_2d"),
        "synthetic_figure_count": sum(1 for row in figure_rows if row["domain"] == "synthetic_2d"),
        "field_figure_count": sum(1 for row in figure_rows if row["domain"] == "field_2d"),
        "synthetic_source_figure_notes_included": bool(synthetic_notes),
        "synthetic_source_figure_notes_ready": synthetic_source_notes_ready,
        "synthetic_source_figure_count": synthetic_source_note_count,
        "synthetic_source_figure_notes_present_after_count": synthetic_source_notes_present,
        "field_cue_spacing_included": bool(field_summary.get("cue_spacing_sensitivity_included", False)),
        "field_cue_spacing_resolution_ready": bool(
            field_summary.get("cue_spacing_resolution_benchmark_ready", False)
        ),
        "field_cue_spacing_fwi_ready": bool(field_summary.get("cue_spacing_field_fwi_ready", False)),
        "field_timing_anchor_conflict_included": bool(
            field_summary.get("timing_anchor_conflict_included", False)
        ),
        "field_timing_anchor_absolute_ready": bool(
            field_summary.get("timing_anchor_absolute_time_zero_ready", False)
        ),
        "field_timing_anchor_fwi_ready": bool(field_summary.get("timing_anchor_field_fwi_ready", False)),
        "field_timing_window_family_included": bool(
            field_summary.get("timing_window_family_included", False)
        ),
        "field_timing_window_short_supported_count": safe_float(
            field_summary.get("timing_window_short_nonraw_supported_count"), 0.0
        ),
        "field_timing_window_short_row_count": safe_float(
            field_summary.get("timing_window_short_nonraw_row_count"), 0.0
        ),
        "field_timing_window_long_reject_count": safe_float(
            field_summary.get("timing_window_long_reject_short_transfer_count"), 0.0
        ),
        "field_timing_window_long_row_count": safe_float(
            field_summary.get("timing_window_long_row_count"), 0.0
        ),
        "field_timing_window_absolute_ready": bool(
            field_summary.get("timing_window_absolute_time_zero_ready", False)
        ),
        "field_timing_window_fwi_ready": bool(field_summary.get("timing_window_field_fwi_ready", False)),
        "field_source_figure_notes_included": bool(source_notes),
        "field_source_figure_notes_ready": source_notes_ready,
        "field_source_figure_count": source_note_count,
        "field_source_figure_notes_present_after_count": source_notes_present,
        "target1_probe_scorecard_included": bool(target1_probe),
        "target1_ready_for_gpu_probe": bool(target1_probe.get("ready_for_target1_gpu_probe", False)),
        "target1_probe_triggered_gate_count": safe_float(target1_probe.get("triggered_gate_count"), 0.0),
        "target1_probe_gpu_action_count": safe_float(target1_probe.get("gpu_action_count"), 0.0),
        "detector_handoff_budget_included": bool(detector_handoff),
        "detector_handoff_ready_for_fwi": bool(
            detector_handoff.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_handoff_cheapest_full_triples_per_case": safe_float(
            detector_handoff.get("cheapest_full_candidate_triples_per_case"), 0.0
        ),
        "detector_handoff_best_deployable_all_truth_cases": safe_float(
            detector_handoff.get("best_deployable_all_truth_case_count"), 0.0
        ),
        "detector_alltriples_gate_included": bool(detector_alltriples),
        "detector_alltriples_ready_for_fwi": bool(
            detector_alltriples.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_alltriples_combo_row_count": safe_float(
            detector_alltriples.get("combo_row_count"), 0.0
        ),
        "detector_alltriples_best_top1_all_truth_cases": safe_float(
            detector_alltriples.get("best_top1_all_truth_case_count"), 0.0
        ),
        "detector_alltriples_best_top10_all_truth_cases": safe_float(
            detector_alltriples.get("best_top10_case_count"), 0.0
        ),
        "detector_alltriples_best_top50_all_truth_cases": safe_float(
            detector_alltriples.get("best_top50_case_count"), 0.0
        ),
        "field_cue_support_catalog_included": bool(field_cue_catalog),
        "field_cue_catalog_ready_for_2d_qc": bool(field_cue_catalog.get("ready_for_2d_qc", False)),
        "field_cue_catalog_ready_for_absolute_time_zero": bool(
            field_cue_catalog.get("ready_for_absolute_time_zero", False)
        ),
        "field_cue_catalog_ready_for_field_fwi": bool(
            field_cue_catalog.get("ready_for_field_fwi", False)
        ),
        "field_cue_catalog_ready_for_3d_hpc": bool(field_cue_catalog.get("ready_for_3d_hpc", False)),
        "field_cue_catalog_support_anchor_count": safe_float(
            field_cue_catalog.get("support_anchor_count"), 0.0
        ),
        "detector_rank_budget_included": bool(detector_rank_budget),
        "detector_rank_budget_ready_for_fwi": bool(
            detector_rank_budget.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_rank_budget_minimal_all_case_triples": safe_float(
            detector_rank_budget.get("minimal_all_case_candidate_triple_budget"), 0.0
        ),
        "detector_rank_budget_best_top50_cases": safe_float(
            detector_rank_budget.get("best_top50_case_count"), 0.0
        ),
        "detector_component_gate_included": bool(detector_component_gate),
        "detector_component_gate_ready_for_fwi": bool(
            detector_component_gate.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_component_gate_best_top50_cases": safe_float(
            detector_component_gate.get("best_top50_case_count"), 0.0
        ),
        "detector_component_gate_top50_improvement": safe_float(
            detector_component_gate.get("top50_improvement_over_source"), 0.0
        ),
        "detector_component_selector_included": bool(detector_component_selector),
        "detector_component_selector_ready_for_fwi": bool(
            detector_component_selector.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_component_selector_candidate_count": safe_float(
            detector_component_selector.get("selector_candidate_count"), 0.0
        ),
        "detector_component_selector_best_in_sample_cases": safe_float(
            detector_component_selector.get("best_in_sample_all_truth_case_count"), 0.0
        ),
        "detector_component_selector_leave_one_case_cases": safe_float(
            detector_component_selector.get("leave_one_case_all_truth_case_count"), 0.0
        ),
        "detector_geometry_selector_included": bool(detector_geometry_selector),
        "detector_geometry_selector_ready_for_fwi": bool(
            detector_geometry_selector.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_geometry_selector_candidate_count": safe_float(
            detector_geometry_selector.get("selector_candidate_count"), 0.0
        ),
        "detector_geometry_selector_best_in_sample_cases": safe_float(
            detector_geometry_selector.get("best_in_sample_all_truth_case_count"), 0.0
        ),
        "detector_geometry_selector_leave_one_case_cases": safe_float(
            detector_geometry_selector.get("leave_one_case_all_truth_case_count"), 0.0
        ),
        "detector_geometry_selector_leave_one_case_improvement": safe_float(
            detector_geometry_selector.get("leave_one_case_improvement_over_component_selector"), 0.0
        ),
        "detector_selector_gap_included": bool(detector_selector_gap),
        "detector_selector_gap_ready_for_fwi": bool(
            detector_selector_gap.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_selector_gap_selected_all_truth_cases": safe_float(
            detector_selector_gap.get("selected_all_truth_case_count"), 0.0
        ),
        "detector_selector_gap_failed_cases": safe_float(
            detector_selector_gap.get("failed_selector_case_count"), 0.0
        ),
        "detector_selector_gap_best_truth_available_cases": safe_float(
            detector_selector_gap.get("best_truth_available_case_count"), 0.0
        ),
        "detector_selector_gap_median_required_gain": safe_float(
            detector_selector_gap.get("median_required_selector_gain_to_choose_truth"), 0.0
        ),
        "detector_selector_gap_max_required_gain": safe_float(
            detector_selector_gap.get("max_required_selector_gain_to_choose_truth"), 0.0
        ),
        "detector_selector_gap_dominant_loss_feature": detector_selector_gap.get("dominant_loss_feature", ""),
        "detector_selector_counterfactual_included": bool(detector_selector_counterfactual),
        "detector_selector_counterfactual_ready_for_fwi": bool(
            detector_selector_counterfactual.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_selector_counterfactual_variant_count": safe_float(
            detector_selector_counterfactual.get("counterfactual_variant_count"), 0.0
        ),
        "detector_selector_counterfactual_best_all_truth_cases": safe_float(
            detector_selector_counterfactual.get("best_all_truth_case_count"), 0.0
        ),
        "detector_selector_counterfactual_improvement_over_base": safe_float(
            detector_selector_counterfactual.get("best_improvement_over_base_all_truth_cases"), 0.0
        ),
        "detector_selector_counterfactual_signed_gap_zero_cases": safe_float(
            detector_selector_counterfactual.get("signed_gap_zero_all_truth_case_count"), 0.0
        ),
        "detector_selector_counterfactual_best_median_gain": safe_float(
            detector_selector_counterfactual.get("best_median_required_selector_gain"), 0.0
        ),
        "detector_selector_counterfactual_best_label": detector_selector_counterfactual.get(
            "best_counterfactual_label", ""
        ),
        "detector_image_objective_rank_included": bool(detector_image_objective_rank),
        "detector_image_objective_rank_ready_for_fwi": bool(
            detector_image_objective_rank.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_image_objective_rank_best_top50_cases": safe_float(
            detector_image_objective_rank.get("best_top50_all_truth_case_count"), 0.0
        ),
        "detector_image_objective_rank_best_top200_cases": safe_float(
            detector_image_objective_rank.get("best_top200_all_truth_case_count"), 0.0
        ),
        "detector_image_objective_rank_best_top1000_cases": safe_float(
            detector_image_objective_rank.get("best_top1000_all_truth_case_count"), 0.0
        ),
        "detector_image_objective_rank_best_median_rank": safe_float(
            detector_image_objective_rank.get("best_median_first_all_truth_rank"), 0.0
        ),
        "detector_target_failure_taxonomy_included": bool(detector_target_failure),
        "detector_target_failure_ready_for_fwi": bool(
            detector_target_failure.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_target_failure_failed_cases": safe_float(
            detector_target_failure.get("failed_selector_case_count"), 0.0
        ),
        "detector_target_failure_missing_target0_cases": safe_float(
            detector_target_failure.get("missing_target0_case_count"), 0.0
        ),
        "detector_target_failure_missing_target1_cases": safe_float(
            detector_target_failure.get("missing_target1_case_count"), 0.0
        ),
        "detector_target_failure_missing_target2_cases": safe_float(
            detector_target_failure.get("missing_target2_case_count"), 0.0
        ),
        "detector_target_failure_multi_target_cases": safe_float(
            detector_target_failure.get("multi_target_missing_case_count"), 0.0
        ),
        "detector_target_failure_dominant_missing_target": detector_target_failure.get(
            "dominant_missing_target", ""
        ),
        "detector_target_failure_target1_median_gain": safe_float(
            detector_target_failure.get("target1_missing_median_required_selector_gain"), 0.0
        ),
        "detector_depth_slot_prior_probe_included": bool(detector_depth_slot_prior),
        "detector_depth_slot_prior_ready_for_fwi": bool(
            detector_depth_slot_prior.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_depth_slot_prior_variant_count": safe_float(
            detector_depth_slot_prior.get("variant_count"), 0.0
        ),
        "detector_depth_slot_prior_base_all_truth_cases": safe_float(
            detector_depth_slot_prior.get("base_all_truth_case_count"), 0.0
        ),
        "detector_depth_slot_prior_best_all_truth_cases": safe_float(
            detector_depth_slot_prior.get("best_all_truth_case_count"), 0.0
        ),
        "detector_depth_slot_prior_improvement_cases": safe_float(
            detector_depth_slot_prior.get("best_improvement_over_base_all_truth_cases"), 0.0
        ),
        "detector_depth_slot_prior_best_depth_weight": safe_float(
            detector_depth_slot_prior.get("best_depth_weight"), 0.0
        ),
        "detector_depth_slot_prior_best_slot_weight": safe_float(
            detector_depth_slot_prior.get("best_slot_weight"), 0.0
        ),
        "detector_depth_slot_prior_best_missing_target1_cases": safe_float(
            detector_depth_slot_prior.get("best_missing_target1_case_count"), 0.0
        ),
        "detector_slot_component_assembly_included": bool(detector_slot_component_assembly),
        "detector_slot_component_ready_for_fwi": bool(
            detector_slot_component_assembly.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_slot_component_variant_count": safe_float(
            detector_slot_component_assembly.get("variant_count"), 0.0
        ),
        "detector_slot_component_current_triple_cases": safe_float(
            detector_slot_component_assembly.get("current_triple_selector_all_truth_case_count"), 0.0
        ),
        "detector_slot_component_depth_prior_cases": safe_float(
            detector_slot_component_assembly.get("depth_slot_prior_best_all_truth_case_count"), 0.0
        ),
        "detector_slot_component_best_slot_cases": safe_float(
            detector_slot_component_assembly.get("best_all_target_slot_case_count"), 0.0
        ),
        "detector_slot_component_best_failed_cases": safe_float(
            detector_slot_component_assembly.get("best_failed_case_count"), 0.0
        ),
        "detector_slot_component_min_component_candidates": safe_float(
            detector_slot_component_assembly.get("min_component_candidate_count"), 0.0
        ),
        "detector_blind_envelope_included": bool(detector_blind_envelope),
        "detector_blind_envelope_ready_for_fwi": bool(
            detector_blind_envelope.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_blind_envelope_variant_count": safe_float(
            detector_blind_envelope.get("variant_count"), 0.0
        ),
        "detector_blind_envelope_best_slot_cases": safe_float(
            detector_blind_envelope.get("best_all_target_slot_case_count"), 0.0
        ),
        "detector_blind_envelope_leave_one_cases": safe_float(
            detector_blind_envelope.get("leave_one_case_all_target_slot_case_count"), 0.0
        ),
        "detector_blind_envelope_known_slot_upper_bound_cases": safe_float(
            detector_blind_envelope.get("known_slot_component_upper_bound_case_count"), 0.0
        ),
        "detector_blind_envelope_uses_branch_slots": bool(
            detector_blind_envelope.get("uses_branch_slots_for_selection", False)
        ),
        "detector_blind_envelope_truth_free_inference": bool(
            detector_blind_envelope.get("truth_free_selection_at_inference", False)
        ),
        "detector_blind_envelope_robustness_included": bool(detector_blind_envelope_robustness),
        "detector_blind_envelope_robustness_ready_for_fwi": bool(
            detector_blind_envelope_robustness.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_blind_envelope_robustness_full_success_variants": safe_float(
            detector_blind_envelope_robustness.get("full_success_variant_count"), 0.0
        ),
        "detector_blind_envelope_robustness_near_success_variants": safe_float(
            detector_blind_envelope_robustness.get("near_success_variant_count"), 0.0
        ),
        "detector_blind_envelope_robustness_leave_one_seed_cases": safe_float(
            detector_blind_envelope_robustness.get("leave_one_seed_all_target_slot_case_count"), 0.0
        ),
        "detector_blind_envelope_robustness_leave_one_branch_cases": safe_float(
            detector_blind_envelope_robustness.get("leave_one_branch_all_target_slot_case_count"), 0.0
        ),
        "detector_blind_envelope_robustness_leave_one_condition_cases": safe_float(
            detector_blind_envelope_robustness.get("leave_one_condition_all_target_slot_case_count"), 0.0
        ),
        "detector_blind_envelope_robustness_min_margin": safe_float(
            detector_blind_envelope_robustness.get("best_variant_min_truth_vs_wrong_score_margin"), 0.0
        ),
        "detector_blind_envelope_robustness_low_margin_cases": safe_float(
            detector_blind_envelope_robustness.get("best_variant_low_margin_case_count"), 0.0
        ),
        "detector_blind_envelope_robustness_boundary": detector_blind_envelope_robustness.get(
            "robustness_boundary", ""
        ),
        "detector_blind_envelope_robustness_branch_robust": bool(
            detector_blind_envelope_robustness.get("heldout_branch_robust", False)
        ),
        "detector_blind_envelope_stability_included": bool(detector_blind_envelope_stability),
        "detector_blind_envelope_stability_ready_for_fwi": bool(
            detector_blind_envelope_stability.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_blind_envelope_stability_all_variant_cases": safe_float(
            detector_blind_envelope_stability.get("all_variant_success_case_count"), 0.0
        ),
        "detector_blind_envelope_stability_partial_cases": safe_float(
            detector_blind_envelope_stability.get("partial_success_case_count"), 0.0
        ),
        "detector_blind_envelope_stability_tuning_sensitive_cases": safe_float(
            detector_blind_envelope_stability.get("tuning_sensitive_case_count"), 0.0
        ),
        "detector_blind_envelope_stability_min_success_fraction": safe_float(
            detector_blind_envelope_stability.get("min_success_fraction"), 0.0
        ),
        "detector_blind_envelope_stability_consensus_cases": safe_float(
            detector_blind_envelope_stability.get("consensus_single_selection_case_count"), 0.0
        ),
        "detector_blind_envelope_stability_close50_partial_cases": safe_float(
            detector_blind_envelope_stability.get("close50_partial_success_case_count"), 0.0
        ),
        "detector_blind_envelope_stability_max_unique_success_selections": safe_float(
            detector_blind_envelope_stability.get("max_unique_success_selection_count"), 0.0
        ),
        "detector_blind_envelope_stability_sensitive_labels": detector_blind_envelope_stability.get(
            "tuning_sensitive_case_labels", ""
        ),
        "detector_blind_envelope_tuning_included": bool(detector_blind_envelope_tuning),
        "detector_blind_envelope_tuning_ready_for_fwi": bool(
            detector_blind_envelope_tuning.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_blind_envelope_tuning_sensitive_cases": safe_float(
            detector_blind_envelope_tuning.get("tuning_sensitive_case_count"), 0.0
        ),
        "detector_blind_envelope_tuning_max_knob_effect": safe_float(
            detector_blind_envelope_tuning.get("max_knob_success_fraction_effect"), 0.0
        ),
        "detector_blind_envelope_tuning_structural_conflict": bool(
            detector_blind_envelope_tuning.get("structural_weight_direction_conflict", False)
        ),
        "detector_blind_envelope_tuning_support_conflict": bool(
            detector_blind_envelope_tuning.get("support_weight_direction_conflict", False)
        ),
        "detector_blind_envelope_tuning_span_effect": safe_float(
            detector_blind_envelope_tuning.get("span_threshold_max_effect"), 0.0
        ),
        "detector_blind_envelope_tuning_global_fix_ready": bool(
            detector_blind_envelope_tuning.get("ready_for_global_policy_tuning_fix", False)
        ),
        "detector_blind_envelope_tuning_top_knob": detector_blind_envelope_tuning.get("top_effect_knob", ""),
        "detector_blind_envelope_reliability_included": bool(detector_blind_envelope_reliability),
        "detector_blind_envelope_reliability_ready_for_claim": bool(
            detector_blind_envelope_reliability.get("ready_for_reliability_claim", False)
        ),
        "detector_blind_envelope_reliability_ready_for_fwi": bool(
            detector_blind_envelope_reliability.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_blind_envelope_reliability_stable_cases": safe_float(
            detector_blind_envelope_reliability.get("stable_assignment_case_count"), 0.0
        ),
        "detector_blind_envelope_reliability_review_cases": safe_float(
            detector_blind_envelope_reliability.get("review_assignment_case_count"), 0.0
        ),
        "detector_blind_envelope_reliability_tuning_detected": safe_float(
            detector_blind_envelope_reliability.get("tuning_sensitive_detected_by_gate_count"), 0.0
        ),
        "detector_blind_envelope_reliability_tuning_missed": safe_float(
            detector_blind_envelope_reliability.get("tuning_sensitive_missed_by_gate_count"), 0.0
        ),
        "detector_blind_envelope_reliability_stable_min_success_fraction": safe_float(
            detector_blind_envelope_reliability.get("stable_assignment_min_success_fraction_truth_eval"), 0.0
        ),
        "detector_blind_envelope_reliability_review_labels": detector_blind_envelope_reliability.get(
            "review_case_labels", ""
        ),
        "detector_blind_envelope_reliability_threshold_included": bool(
            detector_blind_envelope_reliability_threshold
        ),
        "detector_blind_envelope_reliability_threshold_ready_for_claim": bool(
            detector_blind_envelope_reliability_threshold.get("ready_for_reliability_claim", False)
        ),
        "detector_blind_envelope_reliability_threshold_ready_for_fwi": bool(
            detector_blind_envelope_reliability_threshold.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_blind_envelope_reliability_threshold_clean_count": safe_float(
            detector_blind_envelope_reliability_threshold.get("clean_threshold_count"), 0.0
        ),
        "detector_blind_envelope_reliability_threshold_clean_min_mm": safe_float(
            detector_blind_envelope_reliability_threshold.get("clean_threshold_min_mm"), 0.0
        ),
        "detector_blind_envelope_reliability_threshold_clean_max_mm": safe_float(
            detector_blind_envelope_reliability_threshold.get("clean_threshold_max_mm"), 0.0
        ),
        "detector_blind_envelope_reliability_threshold_default_clean": bool(
            detector_blind_envelope_reliability_threshold.get("default_threshold_clean", False)
        ),
        "detector_blind_envelope_reliability_threshold_default_tuning_missed": safe_float(
            detector_blind_envelope_reliability_threshold.get("default_threshold_tuning_missed"), 0.0
        ),
        "detector_blind_envelope_reliability_threshold_default_false_review": safe_float(
            detector_blind_envelope_reliability_threshold.get("default_threshold_false_review"), 0.0
        ),
        "detector_physics_link_included": bool(detector_physics_ambiguity_link),
        "detector_physics_link_ready_for_branch_claim": bool(
            detector_physics_ambiguity_link.get("ready_for_branch_localization_claim", False)
        ),
        "detector_physics_link_ready_for_per_seed_equivalence": bool(
            detector_physics_ambiguity_link.get("ready_for_per_seed_physics_equivalence_claim", False)
        ),
        "detector_physics_link_ready_for_fwi": bool(
            detector_physics_ambiguity_link.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_physics_link_review_cases": safe_float(
            detector_physics_ambiguity_link.get("detector_review_case_count"), 0.0
        ),
        "detector_physics_link_near_boundary_nominal_reviews": safe_float(
            detector_physics_ambiguity_link.get("review_near_boundary_nominal_count"), 0.0
        ),
        "detector_physics_link_close50_nominal_review_fraction": safe_float(
            detector_physics_ambiguity_link.get("close50_linear29p5_nominal_review_fraction"), 0.0
        ),
        "detector_physics_link_review_x_ambiguous_cases": safe_float(
            detector_physics_ambiguity_link.get("review_cases_with_synthetic_x_ambiguity_count"), 0.0
        ),
        "detector_physics_link_review_strict_clean_cases": safe_float(
            detector_physics_ambiguity_link.get("review_cases_with_synthetic_strict_clean_count"), 0.0
        ),
        "detector_physics_link_linear29p5_offset_below_clean_mm": safe_float(
            detector_physics_ambiguity_link.get("linear29p5_offset_below_first_clean_mm"), 0.0
        ),
        "detector_refinement_contract_included": bool(detector_refinement_launch_contract),
        "detector_refinement_contract_ready_seed_table": bool(
            detector_refinement_launch_contract.get("ready_for_component_seed_table", False)
        ),
        "detector_refinement_contract_ready_narrow_refinement": bool(
            detector_refinement_launch_contract.get("ready_for_narrow_refinement_contract", False)
        ),
        "detector_refinement_contract_ready_for_fwi": bool(
            detector_refinement_launch_contract.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_refinement_contract_component_seed_ready_cases": safe_float(
            detector_refinement_launch_contract.get("candidate_component_seed_ready_count"), 0.0
        ),
        "detector_refinement_contract_review_cases": safe_float(
            detector_refinement_launch_contract.get("review_case_count"), 0.0
        ),
        "detector_refinement_contract_active_blockers": safe_float(
            detector_refinement_launch_contract.get("active_blocker_count"), 0.0
        ),
        "detector_refinement_contract_radius_seed_available": bool(
            detector_refinement_launch_contract.get("radius_seed_available", False)
        ),
        "detector_refinement_contract_material_seed_available": bool(
            detector_refinement_launch_contract.get("material_seed_available", False)
        ),
        "detector_refinement_contract_max_seed_error_mm": safe_float(
            detector_refinement_launch_contract.get("max_component_seed_error_mm"), 0.0
        ),
        "detector_component_seed_export_included": bool(detector_component_seed_export),
        "detector_component_seed_exported_cases": safe_float(
            detector_component_seed_export.get("exported_seed_case_count"), 0.0
        ),
        "detector_component_seed_exported_components": safe_float(
            detector_component_seed_export.get("exported_component_row_count"), 0.0
        ),
        "detector_component_seed_excluded_review_cases": safe_float(
            detector_component_seed_export.get("excluded_review_case_count"), 0.0
        ),
        "detector_component_seed_ready_coordinate_table": bool(
            detector_component_seed_export.get("ready_for_coordinate_seed_table", False)
        ),
        "detector_component_seed_ready_for_fwi": bool(
            detector_component_seed_export.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_lateral_slot_budget_included": bool(detector_refinement_neighborhood_budget),
        "detector_lateral_slot_budget_min_half_width_mm": safe_float(
            detector_refinement_neighborhood_budget.get("min_lateral_x_half_width_all_stable_seed_cases_mm"), 0.0
        ),
        "detector_lateral_slot_budget_stable_coverage_5mm": safe_float(
            detector_refinement_neighborhood_budget.get("stable_lateral_x_coverage_at_5mm"), 0.0
        ),
        "detector_lateral_slot_budget_stable_coverage_8mm": safe_float(
            detector_refinement_neighborhood_budget.get("stable_lateral_x_coverage_at_8mm"), 0.0
        ),
        "detector_lateral_slot_budget_stable_coverage_10mm": safe_float(
            detector_refinement_neighborhood_budget.get("stable_lateral_x_coverage_at_10mm"), 0.0
        ),
        "detector_lateral_slot_budget_h10_step2_per_case_points": safe_float(
            detector_refinement_neighborhood_budget.get("per_case_lateral_x_grid_points_h10_step2"), 0.0
        ),
        "detector_lateral_slot_budget_hypothetical_xz_h10_step2_points": safe_float(
            detector_refinement_neighborhood_budget.get("hypothetical_per_case_xz_tensor_points_h10_step2"), 0.0
        ),
        "detector_lateral_slot_budget_z_coverage_validated": bool(
            detector_refinement_neighborhood_budget.get("z_coverage_validated", False)
        ),
        "detector_lateral_slot_budget_ready_for_xz": bool(
            detector_refinement_neighborhood_budget.get("ready_for_xz_neighborhood_design", False)
        ),
        "detector_lateral_slot_budget_ready_for_fwi": bool(
            detector_refinement_neighborhood_budget.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_seed_geometry_audit_included": bool(detector_seed_geometry_error_audit),
        "detector_seed_geometry_xz_min_half_width_mm": safe_float(
            detector_seed_geometry_error_audit.get("min_xz_half_width_all_stable_seed_cases_mm"), 0.0
        ),
        "detector_seed_geometry_source_lateral_half_width_mm": safe_float(
            detector_seed_geometry_error_audit.get("source_lateral_min_half_width_all_stable_seed_cases_mm"), 0.0
        ),
        "detector_seed_geometry_max_stable_x_error_mm": safe_float(
            detector_seed_geometry_error_audit.get("max_stable_x_error_mm"), 0.0
        ),
        "detector_seed_geometry_max_stable_z_error_mm": safe_float(
            detector_seed_geometry_error_audit.get("max_stable_z_error_mm"), 0.0
        ),
        "detector_seed_geometry_z_exceeds_lateral_count": safe_float(
            detector_seed_geometry_error_audit.get("stable_cases_z_exceeds_lateral_slot_error_count"), 0.0
        ),
        "detector_seed_geometry_stable_xz_coverage_10mm": safe_float(
            detector_seed_geometry_error_audit.get("stable_xz_coverage_at_10mm"), 0.0
        ),
        "detector_seed_geometry_stable_xz_coverage_12mm": safe_float(
            detector_seed_geometry_error_audit.get("stable_xz_coverage_at_12mm"), 0.0
        ),
        "detector_seed_geometry_h12_step2_per_case_points": safe_float(
            detector_seed_geometry_error_audit.get("per_case_xz_grid_points_h12_step2"), 0.0
        ),
        "detector_seed_geometry_ready_xz_seed_neighborhood": bool(
            detector_seed_geometry_error_audit.get("ready_for_xz_seed_neighborhood_design", False)
        ),
        "detector_seed_geometry_ready_for_fwi": bool(
            detector_seed_geometry_error_audit.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_radius_material_prior_included": bool(detector_radius_material_prior_scope),
        "detector_radius_material_prior_controlled_ready": bool(
            detector_radius_material_prior_scope.get("ready_for_controlled_synthetic_prior_contract", False)
        ),
        "detector_radius_material_prior_detector_inferred_ready": bool(
            detector_radius_material_prior_scope.get("ready_for_detector_inferred_radius_material_contract", False)
        ),
        "detector_radius_material_prior_ready_for_fwi": bool(
            detector_radius_material_prior_scope.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_radius_material_prior_stable_cases": safe_float(
            detector_radius_material_prior_scope.get("stable_controlled_prior_case_count"), 0.0
        ),
        "detector_radius_material_prior_review_cases": safe_float(
            detector_radius_material_prior_scope.get("review_case_excluded_count"), 0.0
        ),
        "detector_radius_material_prior_detector_radius_seeds": safe_float(
            detector_radius_material_prior_scope.get("detector_radius_seed_available_count"), 0.0
        ),
        "detector_radius_material_prior_detector_material_seeds": safe_float(
            detector_radius_material_prior_scope.get("detector_material_seed_available_count"), 0.0
        ),
        "detector_controlled_prior_refinement_budget_included": bool(
            detector_controlled_prior_refinement_budget
        ),
        "detector_controlled_prior_refinement_fixed_budget_ready": bool(
            detector_controlled_prior_refinement_budget.get(
                "ready_for_controlled_fixed_radius_budget", False
            )
        ),
        "detector_controlled_prior_refinement_independent_search_ready": bool(
            detector_controlled_prior_refinement_budget.get("ready_for_independent_radius_search", False)
        ),
        "detector_controlled_prior_refinement_launch_ready": bool(
            detector_controlled_prior_refinement_budget.get("ready_for_refinement_launch", False)
        ),
        "detector_controlled_prior_refinement_ready_for_fwi": bool(
            detector_controlled_prior_refinement_budget.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_controlled_prior_refinement_fixed_fine_points": safe_float(
            detector_controlled_prior_refinement_budget.get("fixed_slot_radii_stable_total_points_fine"), 0.0
        ),
        "detector_controlled_prior_refinement_fixed_coarse_points": safe_float(
            detector_controlled_prior_refinement_budget.get("fixed_slot_radii_stable_total_points_coarse"), 0.0
        ),
        "detector_controlled_prior_refinement_permutation_multiplier": safe_float(
            detector_controlled_prior_refinement_budget.get("permutation_vs_fixed_multiplier"), 0.0
        ),
        "detector_controlled_prior_refinement_independent_multiplier": safe_float(
            detector_controlled_prior_refinement_budget.get("independent_vs_fixed_multiplier"), 0.0
        ),
        "detector_fixed_radius_pilot_outcome_included": bool(detector_fixed_radius_pilot_outcome),
        "detector_fixed_radius_pilot_run_count": safe_float(
            detector_fixed_radius_pilot_outcome.get("pilot_run_count"), 0.0
        ),
        "detector_fixed_radius_pilot_best_final_linf_mm": safe_float(
            detector_fixed_radius_pilot_outcome.get("best_final_linf_mm"), 0.0
        ),
        "detector_fixed_radius_pilot_within_one_mm_count": safe_float(
            detector_fixed_radius_pilot_outcome.get("within_one_mm_residual_pilot_count"), 0.0
        ),
        "detector_fixed_radius_pilot_second_pass_ready": bool(
            detector_fixed_radius_pilot_outcome.get("ready_for_single_guarded_second_pass_probe", False)
        ),
        "detector_fixed_radius_pilot_broad_gpu_ready": bool(
            detector_fixed_radius_pilot_outcome.get("ready_for_broad_gpu_queue", False)
        ),
        "detector_fixed_radius_residual_ambiguity_included": bool(
            detector_fixed_radius_residual_ambiguity
        ),
        "detector_fixed_radius_residual_final_linf_mm": safe_float(
            detector_fixed_radius_residual_ambiguity.get("final_linf_error_mm"), 0.0
        ),
        "detector_fixed_radius_residual_truth_selected_ambiguous": safe_float(
            detector_fixed_radius_residual_ambiguity.get("truth_selected_but_ambiguous_count"), 0.0
        ),
        "detector_fixed_radius_residual_objective_neighbor": safe_float(
            detector_fixed_radius_residual_ambiguity.get(
                "truth_present_but_objective_prefers_neighbor_count"
            ),
            0.0,
        ),
        "detector_fixed_radius_residual_nonoverlap_absent": safe_float(
            detector_fixed_radius_residual_ambiguity.get(
                "truth_absent_after_nonoverlap_filter_count"
            ),
            0.0,
        ),
        "detector_fixed_radius_residual_immediate_gpu_ready": bool(
            detector_fixed_radius_residual_ambiguity.get("ready_for_immediate_gpu_iteration", False)
        ),
        "detector_fixed_radius_residual_guard_max_gpu_util_percent": safe_float(
            detector_fixed_radius_residual_ambiguity.get("guard_max_gpu_util_percent"), 0.0
        ),
        "detector_fixed_radius_residual_guard_max_ram_used_percent": safe_float(
            detector_fixed_radius_residual_ambiguity.get("guard_max_ram_used_percent"), 0.0
        ),
        "detector_fixed_radius_locking_validation_included": bool(
            detector_fixed_radius_locking_validation
        ),
        "detector_fixed_radius_locking_validation_exact": bool(
            detector_fixed_radius_locking_validation.get("exact_geometry_recovered", False)
        ),
        "detector_fixed_radius_locking_validation_mechanism_ready": bool(
            detector_fixed_radius_locking_validation.get("ready_for_locking_mechanism_claim", False)
        ),
        "detector_fixed_radius_locking_validation_general_policy_ready": bool(
            detector_fixed_radius_locking_validation.get(
                "ready_for_general_detector_policy_claim", False
            )
        ),
        "detector_fixed_radius_locking_validation_broad_gpu_ready": bool(
            detector_fixed_radius_locking_validation.get("ready_for_broad_gpu_queue", False)
        ),
        "detector_fixed_radius_locking_validation_ready_for_fwi": bool(
            detector_fixed_radius_locking_validation.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_fixed_radius_locking_validation_final_linf_mm": safe_float(
            detector_fixed_radius_locking_validation.get("final_linf_error_mm"), 0.0
        ),
        "detector_fixed_radius_locking_validation_truth_selected_count": safe_float(
            detector_fixed_radius_locking_validation.get("truth_selected_count"), 0.0
        ),
        "detector_fixed_radius_locking_validation_truth_ambiguous_count": safe_float(
            detector_fixed_radius_locking_validation.get("truth_selected_but_ambiguous_count"), 0.0
        ),
        "detector_fixed_radius_locking_validation_guard_max_gpu_util_percent": safe_float(
            detector_fixed_radius_locking_validation.get("guard_max_gpu_util_percent"), 0.0
        ),
        "detector_fixed_radius_locking_validation_guard_max_ram_used_percent": safe_float(
            detector_fixed_radius_locking_validation.get("guard_max_ram_used_percent"), 0.0
        ),
        "detector_sampling_boundary_integration_included": bool(detector_sampling_boundary_integration),
        "detector_sampling_boundary_claim_ready": bool(
            detector_sampling_boundary_integration.get("ready_for_detector_sampling_boundary_claim", False)
        ),
        "detector_sampling_boundary_per_seed_equivalence_ready": bool(
            detector_sampling_boundary_integration.get("per_seed_physics_equivalence_ready", False)
        ),
        "detector_sampling_boundary_ready_for_fwi": bool(
            detector_sampling_boundary_integration.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_sampling_boundary_review_cases": safe_float(
            detector_sampling_boundary_integration.get("detector_review_case_count"), 0.0
        ),
        "detector_sampling_boundary_review_below_clean_cases": safe_float(
            detector_sampling_boundary_integration.get("review_below_clean_case_count"), 0.0
        ),
        "detector_sampling_boundary_close50_nominal_reviews": safe_float(
            detector_sampling_boundary_integration.get("close50_nominal_review_case_count"), 0.0
        ),
        "detector_sampling_boundary_close50_source_mismatch_reviews": safe_float(
            detector_sampling_boundary_integration.get("close50_source_mismatch_review_case_count"), 0.0
        ),
        "detector_upper_bound_policy_included": bool(detector_upper_bound),
        "detector_upper_bound_ready_for_claim": bool(
            detector_upper_bound.get("ready_for_rank_gated_upper_bound_claim", False)
        ),
        "detector_upper_bound_ready_for_fwi": bool(
            detector_upper_bound.get("ready_for_detector_seeded_fwi", False)
        ),
        "detector_upper_bound_minimal_all_case_triples": safe_float(
            detector_upper_bound.get("minimal_all_case_rank_gated_triples_per_case"), 0.0
        ),
        "detector_upper_bound_all_truth_cases": safe_float(
            detector_upper_bound.get("best_rank_gated_upper_bound_all_truth_case_count"), 0.0
        ),
        "field_cue_timing_envelope_included": bool(field_cue_timing_envelope),
        "field_cue_timing_ready_for_short_qc": bool(
            field_cue_timing_envelope.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_cue_timing_ready_for_field_fwi": bool(
            field_cue_timing_envelope.get("ready_for_field_fwi", False)
        ),
        "field_cue_timing_short_inside_envelope_count": safe_float(
            field_cue_timing_envelope.get("short_anchor_inside_envelope_count"), 0.0
        ),
        "field_cue_timing_long_reject_short_transfer_count": safe_float(
            field_cue_timing_envelope.get("long_pattern_reject_short_transfer_count"), 0.0
        ),
        "field_spatial_transfer_included": bool(field_spatial_transfer),
        "field_spatial_transfer_ready_for_transfer": bool(
            field_spatial_transfer.get("ready_for_short_to_long_timing_transfer", False)
        ),
        "field_spatial_transfer_ready_for_field_fwi": bool(
            field_spatial_transfer.get("ready_for_field_fwi", False)
        ),
        "field_spatial_transfer_short_covered_count": safe_float(
            field_spatial_transfer.get("short_content_with_nearest_long_within_threshold_count"), 0.0
        ),
        "field_spatial_transfer_long_covered_count": safe_float(
            field_spatial_transfer.get("long_pattern_with_nearest_short_content_within_threshold_count"), 0.0
        ),
        "field_spatial_transfer_median_long_distance_mm": safe_float(
            field_spatial_transfer.get("median_long_to_short_distance_mm"), 0.0
        ),
        "field_anchor_interval_included": bool(field_anchor_interval),
        "field_anchor_interval_ready_for_short_qc": bool(
            field_anchor_interval.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_anchor_interval_ready_for_field_fwi": bool(
            field_anchor_interval.get("ready_for_field_fwi", False)
        ),
        "field_anchor_interval_short_inside_count": safe_float(
            field_anchor_interval.get("short_anchor_inside_supported_interval_count"), 0.0
        ),
        "field_anchor_interval_content_inside_count": safe_float(
            field_anchor_interval.get("short_content_anchor_inside_supported_interval_count"), 0.0
        ),
        "field_anchor_interval_min_margin_mm": safe_float(
            field_anchor_interval.get("min_margin_to_supported_interval_edge_mm"), 0.0
        ),
        "field_dimensionality_included": bool(field_dimensionality),
        "field_dimensionality_is_3d_survey": bool(field_dimensionality.get("is_3d_survey", False)),
        "field_dimensionality_ready_for_short_qc": bool(
            field_dimensionality.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_dimensionality_ready_for_long_transfer": bool(
            field_dimensionality.get("ready_for_long_short_transfer", False)
        ),
        "field_dimensionality_ready_for_3d_hpc": bool(field_dimensionality.get("ready_for_3d_hpc", False)),
        "field_dimensionality_ready_for_field_fwi": bool(
            field_dimensionality.get("ready_for_field_fwi", False)
        ),
        "field_dimensionality_decision_gate_count": safe_float(
            field_dimensionality.get("decision_gate_count"), 0.0
        ),
        "field_time_zero_ladder_included": bool(field_time_zero_ladder),
        "field_time_zero_ladder_ready_for_short_qc": bool(
            field_time_zero_ladder.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_time_zero_ladder_ready_for_long_transfer": bool(
            field_time_zero_ladder.get("ready_for_long_short_transfer", False)
        ),
        "field_time_zero_ladder_ready_for_content_only_short_qc": bool(
            field_time_zero_ladder.get("ready_for_content_only_short_qc", False)
        ),
        "field_time_zero_ladder_ready_for_leave_one_content_anchor": bool(
            field_time_zero_ladder.get("ready_for_leave_one_content_anchor_claim", False)
        ),
        "field_time_zero_ladder_ready_for_absolute_t0": bool(
            field_time_zero_ladder.get("ready_for_absolute_time_zero", False)
        ),
        "field_time_zero_ladder_ready_for_field_fwi": bool(
            field_time_zero_ladder.get("ready_for_field_fwi", False)
        ),
        "field_time_zero_ladder_ready_for_3d_hpc": bool(
            field_time_zero_ladder.get("ready_for_3d_hpc", False)
        ),
        "field_time_zero_ladder_short_half_width_ns": safe_float(
            field_time_zero_ladder.get("short_conservative_half_width_ns"), 0.0
        ),
        "field_time_zero_ladder_content_half_range_ns": safe_float(
            field_time_zero_ladder.get("content_only_offset_half_range_ns"), 0.0
        ),
        "field_time_zero_ladder_ladder_row_count": safe_float(
            field_time_zero_ladder.get("ladder_row_count"), 0.0
        ),
        "field_short_anchor_leave_one_included": bool(field_short_anchor_leave_one),
        "field_short_anchor_leave_one_content_only_supported": bool(
            field_short_anchor_leave_one.get("content_only_supported", False)
        ),
        "field_short_anchor_leave_one_ready_for_short_qc": bool(
            field_short_anchor_leave_one.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_short_anchor_leave_one_ready_for_field_fwi": bool(
            field_short_anchor_leave_one.get("ready_for_field_fwi", False)
        ),
        "field_short_anchor_leave_one_supported_cases": safe_float(
            field_short_anchor_leave_one.get("leave_one_supported_count"), 0.0
        ),
        "field_short_anchor_leave_one_degraded_cases": safe_float(
            field_short_anchor_leave_one.get("leave_one_degraded_single_content_count"), 0.0
        ),
        "field_short_anchor_leave_one_content_half_range_ns": safe_float(
            field_short_anchor_leave_one.get("content_only_offset_half_range_ns"), 0.0
        ),
        "field_short_anchor_spatial_consistency_included": bool(field_short_anchor_spatial_consistency),
        "field_short_anchor_spatial_ready_for_short_qc": bool(
            field_short_anchor_spatial_consistency.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_short_anchor_spatial_ready_for_spatial_calibration": bool(
            field_short_anchor_spatial_consistency.get("ready_for_profile_spatial_calibration", False)
        ),
        "field_short_anchor_spatial_ready_for_field_fwi": bool(
            field_short_anchor_spatial_consistency.get("ready_for_field_fwi", False)
        ),
        "field_short_anchor_spatial_single_translation_supported": bool(
            field_short_anchor_spatial_consistency.get("content_single_translation_supported", False)
        ),
        "field_short_anchor_spatial_content_residual_range_mm": safe_float(
            field_short_anchor_spatial_consistency.get("content_residual_range_mm"), 0.0
        ),
        "field_short_anchor_spatial_content_residual_half_range_mm": safe_float(
            field_short_anchor_spatial_consistency.get("content_residual_half_range_mm"), 0.0
        ),
        "field_short_anchor_spatial_content_min_margin_mm": safe_float(
            field_short_anchor_spatial_consistency.get("content_min_supported_interval_margin_mm"), 0.0
        ),
        "field_inversion_readiness_included": bool(field_inversion_readiness),
        "field_inversion_readiness_ready_short_qc": bool(
            field_inversion_readiness.get("ready_for_short_relative_timing_qc", False)
        ),
        "field_inversion_readiness_ready_depth_scale_qc": bool(
            field_inversion_readiness.get("ready_for_apparent_depth_scale_qc", False)
        ),
        "field_inversion_readiness_ready_long_transfer": bool(
            field_inversion_readiness.get("ready_for_long_profile_transfer", False)
        ),
        "field_inversion_readiness_ready_spatial_calibration": bool(
            field_inversion_readiness.get("ready_for_profile_spatial_calibration", False)
        ),
        "field_inversion_readiness_ready_cover_depth": bool(
            field_inversion_readiness.get("ready_for_cover_depth_recovery", False)
        ),
        "field_inversion_readiness_ready_radius": bool(
            field_inversion_readiness.get("ready_for_radius_recovery", False)
        ),
        "field_inversion_readiness_ready_field_fwi": bool(
            field_inversion_readiness.get("ready_for_field_fwi", False)
        ),
        "field_inversion_readiness_ready_3d_hpc": bool(field_inversion_readiness.get("ready_for_3d_hpc", False)),
        "field_inversion_readiness_gate_count": safe_float(field_inversion_readiness.get("gate_count"), 0.0),
        "field_inversion_readiness_supported_gates": safe_float(
            field_inversion_readiness.get("supported_gate_count"), 0.0
        ),
        "field_inversion_readiness_blocked_gates": safe_float(
            field_inversion_readiness.get("blocked_gate_count"), 0.0
        ),
        "field_inversion_readiness_apparent_depth_span_mm": safe_float(
            field_inversion_readiness.get("apparent_depth_max_span_mm"), 0.0
        ),
        "field_short_anchor_radius_degeneracy_included": bool(field_short_anchor_radius_degeneracy),
        "field_short_anchor_radius_degeneracy_ready_morphology_qc": bool(
            field_short_anchor_radius_degeneracy.get("ready_for_waveform_morphology_qc", False)
        ),
        "field_short_anchor_radius_degeneracy_ready_radius_seed": bool(
            field_short_anchor_radius_degeneracy.get("ready_for_radius_seed", False)
        ),
        "field_short_anchor_radius_degeneracy_ready_field_fwi": bool(
            field_short_anchor_radius_degeneracy.get("ready_for_field_fwi", False)
        ),
        "field_short_anchor_radius_degeneracy_weak_sides": safe_float(
            field_short_anchor_radius_degeneracy.get("weak_radius_side_count"), 0.0
        ),
        "field_short_anchor_radius_degeneracy_mismatch_pairs": safe_float(
            field_short_anchor_radius_degeneracy.get("selected_radius_mismatch_pair_count"), 0.0
        ),
        "field_short_anchor_radius_degeneracy_common_near_ties": safe_float(
            field_short_anchor_radius_degeneracy.get("common_radius_near_tie_pair_count"), 0.0
        ),
        "field_short_anchor_signed_morphology_included": bool(field_short_anchor_signed_morphology),
        "field_short_anchor_signed_morphology_ready_qc": bool(
            field_short_anchor_signed_morphology.get("ready_for_signed_waveform_morphology_qc", False)
        ),
        "field_short_anchor_signed_morphology_ready_amplitude_calibration": bool(
            field_short_anchor_signed_morphology.get("ready_for_absolute_amplitude_calibration", False)
        ),
        "field_short_anchor_signed_morphology_ready_field_fwi": bool(
            field_short_anchor_signed_morphology.get("ready_for_field_fwi", False)
        ),
        "field_short_anchor_signed_morphology_supported_pairs": safe_float(
            field_short_anchor_signed_morphology.get("signed_morphology_supported_pair_count"), 0.0
        ),
        "field_short_anchor_signed_morphology_min_signed_corr": safe_float(
            field_short_anchor_signed_morphology.get("min_corrected_signed_correlation"), 0.0
        ),
        "field_short_anchor_signed_sensitivity_included": bool(
            field_short_anchor_signed_morphology_sensitivity
        ),
        "field_short_anchor_signed_sensitivity_supported_combos": safe_float(
            field_short_anchor_signed_morphology_sensitivity.get("all_pairs_supported_threshold_combo_count"),
            0.0,
        ),
        "field_short_anchor_signed_sensitivity_threshold_combos": safe_float(
            field_short_anchor_signed_morphology_sensitivity.get("threshold_combo_count"), 0.0
        ),
        "field_short_anchor_signed_sensitivity_moderate_ready": bool(
            field_short_anchor_signed_morphology_sensitivity.get(
                "ready_for_moderate_threshold_morphology_qc", False
            )
        ),
        "field_short_anchor_signed_sensitivity_strict_ready": bool(
            field_short_anchor_signed_morphology_sensitivity.get("ready_for_strict_morphology_claim", False)
        ),
        "field_short_anchor_signed_sensitivity_ready_field_fwi": bool(
            field_short_anchor_signed_morphology_sensitivity.get("ready_for_field_fwi", False)
        ),
        "field_collection_handoff_included": bool(field_collection_handoff),
        "field_collection_handoff_ready_collection_day": bool(
            field_collection_handoff.get("ready_for_collection_day", False)
        ),
        "field_collection_handoff_ready_packet_acceptance": bool(
            field_collection_handoff.get("ready_for_packet_acceptance", False)
        ),
        "field_collection_handoff_ready_field_qc_supplement": bool(
            field_collection_handoff.get("ready_for_current_archive_field_qc_supplement", False)
        ),
        "field_collection_handoff_ready_field_fwi": bool(
            field_collection_handoff.get("ready_for_current_archive_field_fwi", False)
        ),
        "field_collection_handoff_ready_heavy_field_work": bool(
            field_collection_handoff.get("ready_for_current_archive_heavy_field_work", False)
        ),
        "field_collection_handoff_ready_3d_hpc": bool(
            field_collection_handoff.get("ready_for_field_3d_hpc", False)
        ),
        "field_collection_handoff_action_count": safe_float(
            field_collection_handoff.get("handoff_action_count"), 0.0
        ),
        "field_collection_handoff_critical_new_data_actions": safe_float(
            field_collection_handoff.get("critical_new_data_action_count"), 0.0
        ),
        "field_collection_handoff_packet_rows_needing_entry": safe_float(
            field_collection_handoff.get("packet_rows_needing_entry"), 0.0
        ),
        "field_collection_handoff_failed_acceptance_gates": safe_float(
            field_collection_handoff.get("failed_acceptance_gate_count"), 0.0
        ),
        "field_collection_handoff_reference_uncertainty_gate_ns": safe_float(
            field_collection_handoff.get("reference_uncertainty_gate_ns"), 0.0
        ),
        "auxiliary_evidence_metric_count": sum(
            1
            for row in metrics
            if row.get("metric", "").startswith(
                (
                    "target1_probe_",
                    "target1_base_",
                    "target1_late_",
                    "detector_handoff_",
                    "detector_alltriples_",
                    "field_cue_catalog_",
                    "detector_rank_budget_",
                    "detector_component_gate_",
                    "detector_component_selector_",
                    "detector_geometry_selector_",
                    "detector_selector_gap_",
                    "detector_selector_counterfactual_",
                    "detector_image_rank_",
                    "detector_image_objective_rank_",
                    "detector_target_failure_",
                    "detector_depth_slot_prior_",
                    "detector_slot_component_",
                    "detector_blind_envelope_",
                    "detector_blind_envelope_robustness_",
                    "detector_blind_envelope_stability_",
                    "detector_blind_envelope_tuning_",
                    "detector_blind_envelope_reliability_",
                    "detector_blind_envelope_reliability_threshold_",
                    "detector_physics_link_",
                    "detector_refinement_contract_",
                    "detector_component_seed_",
                    "detector_lateral_slot_budget_",
                    "detector_seed_geometry_",
                    "detector_radius_material_prior_",
                    "detector_controlled_prior_refinement_",
                    "detector_fixed_radius_pilot_",
                    "detector_fixed_radius_residual_",
                    "detector_fixed_radius_locking_",
                    "detector_sampling_boundary_",
                    "detector_upper_bound_",
                    "field_cue_timing_",
                    "field_spatial_transfer_",
                    "field_anchor_interval_",
                    "field_dimensionality_",
                    "field_time_zero_ladder_",
                    "field_short_anchor_leave_one_",
                    "field_short_anchor_spatial_",
                    "field_inversion_readiness_",
                    "field_short_anchor_radius_degeneracy_",
                    "field_short_anchor_signed_morphology_",
                    "field_short_anchor_signed_sensitivity_",
                    "field_collection_handoff_",
                )
            )
        ),
        "audit_policy_label": audit_summary.get("policy_label", ""),
        "gpu_priority": "none" if no_gpu else "review",
        "ready_for_manuscript_table_use": ready,
        "decision": (
            "Use these CSVs as compact manuscript planning tables. They summarize current "
            "synthetic 2D and measured-field evidence while preserving separate claim scopes; "
            "they do not justify a GPU run."
        ),
    }


def plot_table_pack(summary: dict, save_path: Path) -> str:
    labels = ["synthetic\nfigures", "field\nfigures", "synthetic\nclaims", "field\nclaims"]
    values = [
        summary["synthetic_figure_count"],
        summary["field_figure_count"],
        summary["synthetic_claim_count"],
        summary["field_claim_count"],
    ]
    fig, ax = plt.subplots(figsize=(8.8, 4.8), constrained_layout=True)
    ax.bar(np.arange(len(labels)), values, color=["#3b6ea8", "#4c9f70", "#7b5aa6", "#d08a2e"])
    ax.set_xticks(np.arange(len(labels)), labels)
    ax.set_ylabel("rows")
    ax.set_title("Local 2D and field manuscript table pack")
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    ax.text(
        0.02,
        0.95,
        f"policy={summary['policy_label']}\n"
        f"gpu={summary['gpu_priority']} | cue_fwi={summary['field_cue_timing_ready_for_field_fwi']}\n"
        f"upper_bound={summary['detector_upper_bound_minimal_all_case_triples']:.0f} | "
        f"geo_cv={summary['detector_geometry_selector_leave_one_case_cases']:.0f} | "
        f"gap_fail={summary['detector_selector_gap_failed_cases']:.0f} | "
        f"target1_miss={summary.get('detector_target_failure_missing_target1_cases', 0):.0f} | "
        f"depth_best={summary.get('detector_depth_slot_prior_best_all_truth_cases', 0):.0f} | "
        f"slot={summary.get('detector_slot_component_best_slot_cases', 0):.0f} | "
        f"blind={summary.get('detector_blind_envelope_best_slot_cases', 0):.0f} | "
        f"branch_cv={summary.get('detector_blind_envelope_robustness_leave_one_branch_cases', 0):.0f} | "
        f"stable={summary.get('detector_blind_envelope_stability_all_variant_cases', 0):.0f} | "
        f"rel={summary.get('detector_blind_envelope_reliability_stable_cases', 0):.0f}/"
        f"{summary.get('detector_blind_envelope_reliability_review_cases', 0):.0f}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    return save_validated_figure(fig, str(save_path))


def write_figure_notes(
    path: Path,
    summary: dict,
    claim_csv: Path,
    figure_csv: Path,
    metric_csv: Path,
    validation_csv: Path,
) -> None:
    """Write notes for the manuscript table-pack summary figure."""
    path.write_text(
        "\n".join(
            [
                "# Figure Notes",
                "",
                "## `local_2d_field_manuscript_table_pack.png`",
                "",
                "This figure summarizes the row counts in the compact manuscript planning",
                "tables for current synthetic 2D and measured-field 2D evidence.",
                "",
                f"Policy label: `{summary['policy_label']}`.",
                f"Synthetic figures: `{summary['synthetic_figure_count']}`.",
                f"Field figures: `{summary['field_figure_count']}`.",
                f"Synthetic claims: `{summary['synthetic_claim_count']}`.",
                f"Field claims: `{summary['field_claim_count']}`.",
                f"Auxiliary policy metrics: `{summary.get('auxiliary_evidence_metric_count', 0)}`.",
                f"Target1 ready for GPU probe: `{summary.get('target1_ready_for_gpu_probe', False)}`.",
                f"Detector all-triples top-1 all-truth cases: `{summary.get('detector_alltriples_best_top1_all_truth_cases', 0)}`.",
                f"Detector component-gate top-50 all-truth cases: `{summary.get('detector_component_gate_best_top50_cases', 0)}`.",
                f"Detector component-selector leave-one-case all-truth cases: `{summary.get('detector_component_selector_leave_one_case_cases', 0)}`.",
                f"Detector geometry-selector leave-one-case all-truth cases: `{summary.get('detector_geometry_selector_leave_one_case_cases', 0)}`.",
                f"Detector selector-gap failed cases: `{summary.get('detector_selector_gap_failed_cases', 0)}`.",
                f"Detector selector-gap dominant loss feature: `{summary.get('detector_selector_gap_dominant_loss_feature', '')}`.",
                f"Detector selector-counterfactual best all-truth cases: `{summary.get('detector_selector_counterfactual_best_all_truth_cases', 0)}`.",
                f"Detector selector-counterfactual improvement over base: `{summary.get('detector_selector_counterfactual_improvement_over_base', 0)}`.",
                f"Detector image-objective rank top-50 cases: `{summary.get('detector_image_objective_rank_best_top50_cases', 0)}`.",
                f"Detector image-objective rank top-1000 cases: `{summary.get('detector_image_objective_rank_best_top1000_cases', 0)}`.",
                f"Detector target-failure missing target1 cases: `{summary.get('detector_target_failure_missing_target1_cases', 0)}`.",
                f"Detector target-failure multi-target cases: `{summary.get('detector_target_failure_multi_target_cases', 0)}`.",
                f"Detector target-failure dominant missing target: `{summary.get('detector_target_failure_dominant_missing_target', '')}`.",
                f"Detector depth/slot prior best all-truth cases: `{summary.get('detector_depth_slot_prior_best_all_truth_cases', 0)}`.",
                f"Detector depth/slot prior improvement cases: `{summary.get('detector_depth_slot_prior_improvement_cases', 0)}`.",
                f"Detector depth/slot prior ready for FWI: `{summary.get('detector_depth_slot_prior_ready_for_fwi', False)}`.",
                f"Detector slot-component best slot cases: `{summary.get('detector_slot_component_best_slot_cases', 0)}`.",
                f"Detector slot-component ready for FWI: `{summary.get('detector_slot_component_ready_for_fwi', False)}`.",
                f"Detector blind-envelope best slot cases: `{summary.get('detector_blind_envelope_best_slot_cases', 0)}`.",
                f"Detector blind-envelope leave-one cases: `{summary.get('detector_blind_envelope_leave_one_cases', 0)}`.",
                f"Detector blind-envelope uses branch slots: `{summary.get('detector_blind_envelope_uses_branch_slots', False)}`.",
                f"Detector blind-envelope ready for FWI: `{summary.get('detector_blind_envelope_ready_for_fwi', False)}`.",
                f"Detector blind-envelope robustness full-success variants: `{summary.get('detector_blind_envelope_robustness_full_success_variants', 0)}`.",
                f"Detector blind-envelope robustness leave-one-seed cases: `{summary.get('detector_blind_envelope_robustness_leave_one_seed_cases', 0)}`.",
                f"Detector blind-envelope robustness leave-one-branch cases: `{summary.get('detector_blind_envelope_robustness_leave_one_branch_cases', 0)}`.",
                f"Detector blind-envelope robustness min margin: `{summary.get('detector_blind_envelope_robustness_min_margin', 0)}`.",
                f"Detector blind-envelope robustness boundary: `{summary.get('detector_blind_envelope_robustness_boundary', '')}`.",
                f"Detector blind-envelope robustness ready for FWI: `{summary.get('detector_blind_envelope_robustness_ready_for_fwi', False)}`.",
                f"Detector blind-envelope stability all-variant cases: `{summary.get('detector_blind_envelope_stability_all_variant_cases', 0)}`.",
                f"Detector blind-envelope stability partial cases: `{summary.get('detector_blind_envelope_stability_partial_cases', 0)}`.",
                f"Detector blind-envelope stability tuning-sensitive cases: `{summary.get('detector_blind_envelope_stability_tuning_sensitive_cases', 0)}`.",
                f"Detector blind-envelope stability min success fraction: `{summary.get('detector_blind_envelope_stability_min_success_fraction', 0)}`.",
                f"Detector blind-envelope stability sensitive labels: `{summary.get('detector_blind_envelope_stability_sensitive_labels', '')}`.",
                f"Detector blind-envelope stability ready for FWI: `{summary.get('detector_blind_envelope_stability_ready_for_fwi', False)}`.",
                f"Detector blind-envelope tuning max knob effect: `{summary.get('detector_blind_envelope_tuning_max_knob_effect', 0)}`.",
                f"Detector blind-envelope tuning structural conflict: `{summary.get('detector_blind_envelope_tuning_structural_conflict', False)}`.",
                f"Detector blind-envelope tuning support conflict: `{summary.get('detector_blind_envelope_tuning_support_conflict', False)}`.",
                f"Detector blind-envelope tuning ready for FWI: `{summary.get('detector_blind_envelope_tuning_ready_for_fwi', False)}`.",
                f"Detector blind-envelope reliability stable cases: `{summary.get('detector_blind_envelope_reliability_stable_cases', 0)}`.",
                f"Detector blind-envelope reliability review cases: `{summary.get('detector_blind_envelope_reliability_review_cases', 0)}`.",
                f"Detector blind-envelope reliability tuning missed: `{summary.get('detector_blind_envelope_reliability_tuning_missed', 0)}`.",
                f"Detector blind-envelope reliability ready for claim: `{summary.get('detector_blind_envelope_reliability_ready_for_claim', False)}`.",
                f"Detector blind-envelope reliability ready for FWI: `{summary.get('detector_blind_envelope_reliability_ready_for_fwi', False)}`.",
                f"Detector blind-envelope reliability clean threshold count: `{summary.get('detector_blind_envelope_reliability_threshold_clean_count', 0)}`.",
                f"Detector blind-envelope reliability clean threshold range mm: `{summary.get('detector_blind_envelope_reliability_threshold_clean_min_mm', 0)}`-`{summary.get('detector_blind_envelope_reliability_threshold_clean_max_mm', 0)}`.",
                f"Detector blind-envelope reliability default threshold clean: `{summary.get('detector_blind_envelope_reliability_threshold_default_clean', False)}`.",
                f"Detector blind-envelope reliability threshold ready for FWI: `{summary.get('detector_blind_envelope_reliability_threshold_ready_for_fwi', False)}`.",
                f"Detector physics-link review cases: `{summary.get('detector_physics_link_review_cases', 0)}`.",
                f"Detector physics-link near-boundary nominal reviews: `{summary.get('detector_physics_link_near_boundary_nominal_reviews', 0)}`.",
                f"Detector physics-link close50 nominal review fraction: `{summary.get('detector_physics_link_close50_nominal_review_fraction', 0)}`.",
                f"Detector physics-link review x-ambiguous cases: `{summary.get('detector_physics_link_review_x_ambiguous_cases', 0)}`.",
                f"Detector physics-link per-seed equivalence ready: `{summary.get('detector_physics_link_ready_for_per_seed_equivalence', False)}`.",
                f"Detector physics-link ready for FWI: `{summary.get('detector_physics_link_ready_for_fwi', False)}`.",
                f"Detector refinement-contract seed-table cases: `{summary.get('detector_refinement_contract_component_seed_ready_cases', 0)}`.",
                f"Detector refinement-contract review cases: `{summary.get('detector_refinement_contract_review_cases', 0)}`.",
                f"Detector refinement-contract active blockers: `{summary.get('detector_refinement_contract_active_blockers', 0)}`.",
                f"Detector refinement-contract radius seed available: `{summary.get('detector_refinement_contract_radius_seed_available', False)}`.",
                f"Detector refinement-contract material seed available: `{summary.get('detector_refinement_contract_material_seed_available', False)}`.",
                f"Detector refinement-contract ready for narrow refinement: `{summary.get('detector_refinement_contract_ready_narrow_refinement', False)}`.",
                f"Detector refinement-contract ready for FWI: `{summary.get('detector_refinement_contract_ready_for_fwi', False)}`.",
                f"Detector radius/material controlled prior ready: `{summary.get('detector_radius_material_prior_controlled_ready', False)}`.",
                f"Detector radius/material detector-inferred ready: `{summary.get('detector_radius_material_prior_detector_inferred_ready', False)}`.",
                f"Detector controlled-prior fixed fine points: `{summary.get('detector_controlled_prior_refinement_fixed_fine_points', 0)}`.",
                f"Detector controlled-prior permutation multiplier: `{summary.get('detector_controlled_prior_refinement_permutation_multiplier', 0)}`.",
                f"Detector controlled-prior refinement launch ready: `{summary.get('detector_controlled_prior_refinement_launch_ready', False)}`.",
                f"Detector fixed-radius pilot runs: `{summary.get('detector_fixed_radius_pilot_run_count', 0)}`.",
                f"Detector fixed-radius best final residual: `{summary.get('detector_fixed_radius_pilot_best_final_linf_mm', 0)}` mm.",
                f"Detector fixed-radius immediate second pass ready: `{summary.get('detector_fixed_radius_pilot_second_pass_ready', False)}`.",
                f"Detector fixed-radius residual objective-neighbor count: `{summary.get('detector_fixed_radius_residual_objective_neighbor', 0)}`.",
                f"Detector fixed-radius residual non-overlap-absent count: `{summary.get('detector_fixed_radius_residual_nonoverlap_absent', 0)}`.",
                f"Detector fixed-radius residual immediate GPU ready: `{summary.get('detector_fixed_radius_residual_immediate_gpu_ready', False)}`.",
                f"Detector fixed-radius locking validation exact: `{summary.get('detector_fixed_radius_locking_validation_exact', False)}`.",
                f"Detector fixed-radius locking validation broad GPU ready: `{summary.get('detector_fixed_radius_locking_validation_broad_gpu_ready', False)}`.",
                f"Detector upper-bound minimal all-case triples: `{summary.get('detector_upper_bound_minimal_all_case_triples', 0)}`.",
                f"Detector rank-budget all-case triples: `{summary.get('detector_rank_budget_minimal_all_case_triples', 0)}`.",
                f"Field cue catalog ready for field FWI: `{summary.get('field_cue_catalog_ready_for_field_fwi', False)}`.",
                f"Field cue timing long short-transfer rejections: `{summary.get('field_cue_timing_long_reject_short_transfer_count', 0)}`.",
                f"Field spatial transfer long anchors covered: `{summary.get('field_spatial_transfer_long_covered_count', 0)}`.",
                f"Field anchor interval short anchors inside: `{summary.get('field_anchor_interval_short_inside_count', 0)}`.",
                f"Field dimensionality is 3D survey: `{summary.get('field_dimensionality_is_3d_survey', False)}`.",
                f"Field dimensionality short QC ready: `{summary.get('field_dimensionality_ready_for_short_qc', False)}`.",
                f"Field dimensionality long-transfer ready: `{summary.get('field_dimensionality_ready_for_long_transfer', False)}`.",
                f"Field time-zero ladder short QC ready: `{summary.get('field_time_zero_ladder_ready_for_short_qc', False)}`.",
                f"Field time-zero ladder content-only short QC ready: `{summary.get('field_time_zero_ladder_ready_for_content_only_short_qc', False)}`.",
                f"Field time-zero ladder leave-one-content ready: `{summary.get('field_time_zero_ladder_ready_for_leave_one_content_anchor', False)}`.",
                f"Field time-zero ladder absolute t0 ready: `{summary.get('field_time_zero_ladder_ready_for_absolute_t0', False)}`.",
                f"Field time-zero ladder field FWI ready: `{summary.get('field_time_zero_ladder_ready_for_field_fwi', False)}`.",
                f"Field short-anchor content-only supported: `{summary.get('field_short_anchor_leave_one_content_only_supported', False)}`.",
                f"Field short-anchor leave-one supported cases: `{summary.get('field_short_anchor_leave_one_supported_cases', 0)}`.",
                f"Field short-anchor leave-one degraded cases: `{summary.get('field_short_anchor_leave_one_degraded_cases', 0)}`.",
                f"Field short-anchor spatial residual range mm: `{summary.get('field_short_anchor_spatial_content_residual_range_mm', 0)}`.",
                f"Field short-anchor spatial single translation supported: `{summary.get('field_short_anchor_spatial_single_translation_supported', False)}`.",
                f"Field short-anchor spatial calibration ready: `{summary.get('field_short_anchor_spatial_ready_for_spatial_calibration', False)}`.",
                f"Field short-anchor spatial field FWI ready: `{summary.get('field_short_anchor_spatial_ready_for_field_fwi', False)}`.",
                f"Field inversion readiness supported gates: `{summary.get('field_inversion_readiness_supported_gates', 0)}`.",
                f"Field inversion readiness blocked gates: `{summary.get('field_inversion_readiness_blocked_gates', 0)}`.",
                f"Field inversion readiness depth-scale QC: `{summary.get('field_inversion_readiness_ready_depth_scale_qc', False)}`.",
                f"Field inversion readiness cover-depth: `{summary.get('field_inversion_readiness_ready_cover_depth', False)}`.",
                f"Field inversion readiness field FWI: `{summary.get('field_inversion_readiness_ready_field_fwi', False)}`.",
                f"Field inversion readiness 3D/HPC: `{summary.get('field_inversion_readiness_ready_3d_hpc', False)}`.",
                f"Field collection handoff included: `{summary.get('field_collection_handoff_included', False)}`.",
                f"Field collection handoff ready for collection day: `{summary.get('field_collection_handoff_ready_collection_day', False)}`.",
                f"Field collection handoff ready for packet acceptance: `{summary.get('field_collection_handoff_ready_packet_acceptance', False)}`.",
                f"Field collection handoff critical new-data actions: `{summary.get('field_collection_handoff_critical_new_data_actions', 0)}`.",
                f"Field collection handoff packet rows needing entry: `{summary.get('field_collection_handoff_packet_rows_needing_entry', 0)}`.",
                f"Field collection handoff failed acceptance gates: `{summary.get('field_collection_handoff_failed_acceptance_gates', 0)}`.",
                f"Field collection handoff field FWI ready: `{summary.get('field_collection_handoff_ready_field_fwi', False)}`.",
                f"Field collection handoff 3D/HPC ready: `{summary.get('field_collection_handoff_ready_3d_hpc', False)}`.",
                f"GPU priority: `{summary['gpu_priority']}`.",
                "",
                "This is a manuscript-planning table index, not a new experiment.",
                f"The claim table, figure inventory, and result metrics are stored in",
                f"`{claim_csv.name}`, `{figure_csv.name}`, and `{metric_csv.name}`.",
                f"Image-validation metrics for this figure are stored in `{validation_csv.name}`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-root", default=DEFAULT_EXPERIMENT_ROOT)
    parser.add_argument("--field-root", default=DEFAULT_FIELD_ROOT)
    parser.add_argument("--dataset-id", default=DEFAULT_DATASET_ID)
    parser.add_argument("--synthetic-bundle-run", default=DEFAULT_SYNTHETIC_BUNDLE_RUN)
    parser.add_argument("--synthetic-next-matrix-run", default=DEFAULT_SYNTHETIC_NEXT_MATRIX_RUN)
    parser.add_argument("--synthetic-source-notes-run", default=DEFAULT_SYNTHETIC_SOURCE_NOTES_RUN)
    parser.add_argument("--field-bundle-run", default=DEFAULT_FIELD_BUNDLE_RUN)
    parser.add_argument("--field-policy-run", default=DEFAULT_FIELD_POLICY_RUN)
    parser.add_argument("--field-source-notes-run", default=DEFAULT_FIELD_SOURCE_NOTES_RUN)
    parser.add_argument("--target1-probe-scorecard-run", default=DEFAULT_TARGET1_PROBE_SCORECARD_RUN)
    parser.add_argument("--detector-handoff-budget-run", default=DEFAULT_DETECTOR_HANDOFF_BUDGET_RUN)
    parser.add_argument("--detector-alltriples-gate-run", default=DEFAULT_DETECTOR_ALLTRIPLES_GATE_RUN)
    parser.add_argument("--field-cue-support-catalog-run", default=DEFAULT_FIELD_CUE_SUPPORT_CATALOG_RUN)
    parser.add_argument("--detector-rank-budget-run", default=DEFAULT_DETECTOR_RANK_BUDGET_RUN)
    parser.add_argument("--detector-component-gate-run", default=DEFAULT_DETECTOR_COMPONENT_GATE_RUN)
    parser.add_argument("--detector-component-selector-run", default=DEFAULT_DETECTOR_COMPONENT_SELECTOR_RUN)
    parser.add_argument("--detector-geometry-selector-run", default=DEFAULT_DETECTOR_GEOMETRY_SELECTOR_RUN)
    parser.add_argument("--detector-selector-gap-run", default=DEFAULT_DETECTOR_SELECTOR_GAP_RUN)
    parser.add_argument("--detector-selector-counterfactual-run", default=DEFAULT_DETECTOR_SELECTOR_COUNTERFACTUAL_RUN)
    parser.add_argument("--detector-image-objective-rank-run", default=DEFAULT_DETECTOR_IMAGE_OBJECTIVE_RANK_RUN)
    parser.add_argument("--detector-target-failure-taxonomy-run", default=DEFAULT_DETECTOR_TARGET_FAILURE_TAXONOMY_RUN)
    parser.add_argument("--detector-depth-slot-prior-run", default=DEFAULT_DETECTOR_DEPTH_SLOT_PRIOR_RUN)
    parser.add_argument("--detector-slot-component-assembly-run", default=DEFAULT_DETECTOR_SLOT_COMPONENT_ASSEMBLY_RUN)
    parser.add_argument("--detector-blind-envelope-run", default=DEFAULT_DETECTOR_BLIND_ENVELOPE_RUN)
    parser.add_argument("--detector-blind-envelope-robustness-run", default=DEFAULT_DETECTOR_BLIND_ENVELOPE_ROBUSTNESS_RUN)
    parser.add_argument("--detector-blind-envelope-stability-run", default=DEFAULT_DETECTOR_BLIND_ENVELOPE_STABILITY_RUN)
    parser.add_argument("--detector-blind-envelope-tuning-run", default=DEFAULT_DETECTOR_BLIND_ENVELOPE_TUNING_RUN)
    parser.add_argument(
        "--detector-blind-envelope-reliability-run",
        default=DEFAULT_DETECTOR_BLIND_ENVELOPE_RELIABILITY_RUN,
    )
    parser.add_argument(
        "--detector-blind-envelope-reliability-threshold-run",
        default=DEFAULT_DETECTOR_BLIND_ENVELOPE_RELIABILITY_THRESHOLD_RUN,
    )
    parser.add_argument("--detector-physics-ambiguity-link-run", default=DEFAULT_DETECTOR_PHYSICS_AMBIGUITY_LINK_RUN)
    parser.add_argument(
        "--detector-refinement-launch-contract-run",
        default=DEFAULT_DETECTOR_REFINEMENT_LAUNCH_CONTRACT_RUN,
    )
    parser.add_argument("--detector-component-seed-export-run", default=DEFAULT_DETECTOR_COMPONENT_SEED_EXPORT_RUN)
    parser.add_argument(
        "--detector-refinement-neighborhood-budget-run",
        default=DEFAULT_DETECTOR_REFINEMENT_NEIGHBORHOOD_BUDGET_RUN,
    )
    parser.add_argument(
        "--detector-seed-geometry-error-audit-run",
        default=DEFAULT_DETECTOR_SEED_GEOMETRY_ERROR_AUDIT_RUN,
    )
    parser.add_argument(
        "--detector-radius-material-prior-scope-run",
        default=DEFAULT_DETECTOR_RADIUS_MATERIAL_PRIOR_SCOPE_RUN,
    )
    parser.add_argument(
        "--detector-controlled-prior-refinement-budget-run",
        default=DEFAULT_DETECTOR_CONTROLLED_PRIOR_REFINEMENT_BUDGET_RUN,
    )
    parser.add_argument(
        "--detector-fixed-radius-pilot-outcome-synthesis-run",
        default=DEFAULT_DETECTOR_FIXED_RADIUS_PILOT_OUTCOME_SYNTHESIS_RUN,
    )
    parser.add_argument(
        "--detector-fixed-radius-residual-ambiguity-audit-run",
        default=DEFAULT_DETECTOR_FIXED_RADIUS_RESIDUAL_AMBIGUITY_AUDIT_RUN,
    )
    parser.add_argument(
        "--detector-fixed-radius-locking-policy-validation-run",
        default=DEFAULT_DETECTOR_FIXED_RADIUS_LOCKING_POLICY_VALIDATION_RUN,
    )
    parser.add_argument(
        "--detector-sampling-boundary-integration-run",
        default=DEFAULT_DETECTOR_SAMPLING_BOUNDARY_INTEGRATION_RUN,
    )
    parser.add_argument("--detector-upper-bound-policy-run", default=DEFAULT_DETECTOR_UPPER_BOUND_POLICY_RUN)
    parser.add_argument("--field-cue-timing-envelope-run", default=DEFAULT_FIELD_CUE_TIMING_ENVELOPE_RUN)
    parser.add_argument("--field-spatial-transfer-run", default=DEFAULT_FIELD_SPATIAL_TRANSFER_RUN)
    parser.add_argument("--field-anchor-interval-run", default=DEFAULT_FIELD_ANCHOR_INTERVAL_RUN)
    parser.add_argument("--field-dimensionality-decision-run", default=DEFAULT_FIELD_DIMENSIONALITY_DECISION_RUN)
    parser.add_argument("--field-time-zero-ladder-run", default=DEFAULT_FIELD_TIME_ZERO_LADDER_RUN)
    parser.add_argument("--field-short-anchor-leave-one-run", default=DEFAULT_FIELD_SHORT_ANCHOR_LEAVE_ONE_RUN)
    parser.add_argument(
        "--field-short-anchor-spatial-consistency-run",
        default=DEFAULT_FIELD_SHORT_ANCHOR_SPATIAL_CONSISTENCY_RUN,
    )
    parser.add_argument("--field-inversion-readiness-run", default=DEFAULT_FIELD_INVERSION_READINESS_RUN)
    parser.add_argument(
        "--field-short-anchor-radius-degeneracy-run",
        default=DEFAULT_FIELD_SHORT_ANCHOR_RADIUS_DEGENERACY_RUN,
    )
    parser.add_argument(
        "--field-short-anchor-signed-morphology-run",
        default=DEFAULT_FIELD_SHORT_ANCHOR_SIGNED_MORPHOLOGY_RUN,
    )
    parser.add_argument(
        "--field-short-anchor-signed-morphology-sensitivity-run",
        default=DEFAULT_FIELD_SHORT_ANCHOR_SIGNED_MORPHOLOGY_SENSITIVITY_RUN,
    )
    parser.add_argument("--field-collection-handoff-run", default=DEFAULT_FIELD_COLLECTION_HANDOFF_RUN)
    parser.add_argument("--audit-run", default=DEFAULT_AUDIT_RUN)
    parser.add_argument("--run-name", default="local_2d_field_manuscript_table_pack")
    parser.add_argument("--outdir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    experiment_root = Path(args.experiment_root)
    field_root = field_dataset_output_root(args.field_root, args.dataset_id)
    audit_root = Path("outputs/summary_tables") / args.audit_run

    synthetic_bundle_dir = experiment_root / args.synthetic_bundle_run
    synthetic_next_dir = experiment_root / args.synthetic_next_matrix_run
    synthetic_source_notes_dir = experiment_root / args.synthetic_source_notes_run
    field_bundle_dir = field_root / args.field_bundle_run
    field_policy_dir = field_root / args.field_policy_run
    field_source_notes_dir = field_root / args.field_source_notes_run
    target1_probe_dir = Path("outputs/summary_tables") / args.target1_probe_scorecard_run
    detector_handoff_dir = Path("outputs/summary_tables") / args.detector_handoff_budget_run
    detector_alltriples_dir = Path("outputs/summary_tables") / args.detector_alltriples_gate_run
    field_cue_catalog_dir = field_root / args.field_cue_support_catalog_run
    detector_rank_budget_dir = Path("outputs/summary_tables") / args.detector_rank_budget_run
    detector_component_gate_dir = Path("outputs/summary_tables") / args.detector_component_gate_run
    detector_component_selector_dir = Path("outputs/summary_tables") / args.detector_component_selector_run
    detector_geometry_selector_dir = Path("outputs/summary_tables") / args.detector_geometry_selector_run
    detector_selector_gap_dir = Path("outputs/summary_tables") / args.detector_selector_gap_run
    detector_selector_counterfactual_dir = Path("outputs/summary_tables") / args.detector_selector_counterfactual_run
    detector_image_objective_rank_dir = Path("outputs/summary_tables") / args.detector_image_objective_rank_run
    detector_target_failure_dir = Path("outputs/summary_tables") / args.detector_target_failure_taxonomy_run
    detector_depth_slot_prior_dir = Path("outputs/summary_tables") / args.detector_depth_slot_prior_run
    detector_slot_component_assembly_dir = Path("outputs/summary_tables") / args.detector_slot_component_assembly_run
    detector_blind_envelope_dir = Path("outputs/summary_tables") / args.detector_blind_envelope_run
    detector_blind_envelope_robustness_dir = Path("outputs/summary_tables") / args.detector_blind_envelope_robustness_run
    detector_blind_envelope_stability_dir = Path("outputs/summary_tables") / args.detector_blind_envelope_stability_run
    detector_blind_envelope_tuning_dir = Path("outputs/summary_tables") / args.detector_blind_envelope_tuning_run
    detector_blind_envelope_reliability_dir = (
        Path("outputs/summary_tables") / args.detector_blind_envelope_reliability_run
    )
    detector_blind_envelope_reliability_threshold_dir = (
        Path("outputs/summary_tables") / args.detector_blind_envelope_reliability_threshold_run
    )
    detector_physics_ambiguity_link_dir = Path("outputs/summary_tables") / args.detector_physics_ambiguity_link_run
    detector_refinement_launch_contract_dir = (
        Path("outputs/summary_tables") / args.detector_refinement_launch_contract_run
    )
    detector_component_seed_export_dir = Path("outputs/summary_tables") / args.detector_component_seed_export_run
    detector_refinement_neighborhood_budget_dir = (
        Path("outputs/summary_tables") / args.detector_refinement_neighborhood_budget_run
    )
    detector_seed_geometry_error_audit_dir = (
        Path("outputs/summary_tables") / args.detector_seed_geometry_error_audit_run
    )
    detector_radius_material_prior_scope_dir = (
        Path("outputs/summary_tables") / args.detector_radius_material_prior_scope_run
    )
    detector_controlled_prior_refinement_budget_dir = (
        Path("outputs/summary_tables") / args.detector_controlled_prior_refinement_budget_run
    )
    detector_fixed_radius_pilot_outcome_synthesis_dir = (
        Path("outputs/summary_tables") / args.detector_fixed_radius_pilot_outcome_synthesis_run
    )
    detector_fixed_radius_residual_ambiguity_audit_dir = (
        Path("outputs/summary_tables") / args.detector_fixed_radius_residual_ambiguity_audit_run
    )
    detector_fixed_radius_locking_policy_validation_dir = (
        Path("outputs/summary_tables") / args.detector_fixed_radius_locking_policy_validation_run
    )
    detector_sampling_boundary_integration_dir = (
        Path("outputs/summary_tables") / args.detector_sampling_boundary_integration_run
    )
    detector_upper_bound_dir = Path("outputs/summary_tables") / args.detector_upper_bound_policy_run
    field_cue_timing_envelope_dir = field_root / args.field_cue_timing_envelope_run
    field_spatial_transfer_dir = field_root / args.field_spatial_transfer_run
    field_anchor_interval_dir = field_root / args.field_anchor_interval_run
    field_dimensionality_dir = field_root / args.field_dimensionality_decision_run
    field_time_zero_ladder_dir = field_root / args.field_time_zero_ladder_run
    field_short_anchor_leave_one_dir = field_root / args.field_short_anchor_leave_one_run
    field_short_anchor_spatial_consistency_dir = field_root / args.field_short_anchor_spatial_consistency_run
    field_inversion_readiness_dir = field_root / args.field_inversion_readiness_run
    field_short_anchor_radius_degeneracy_dir = field_root / args.field_short_anchor_radius_degeneracy_run
    field_short_anchor_signed_morphology_dir = field_root / args.field_short_anchor_signed_morphology_run
    field_short_anchor_signed_morphology_sensitivity_dir = (
        field_root / args.field_short_anchor_signed_morphology_sensitivity_run
    )
    field_collection_handoff_dir = field_root / args.field_collection_handoff_run

    synthetic_summary = read_json(
        synthetic_bundle_dir / "data/synthetic_2d_publication_figure_bundle_summary.json"
    )
    synthetic_next = read_json(
        synthetic_next_dir / "data/synthetic_2d_next_question_matrix_summary.json"
    )
    synthetic_source_notes = read_json(
        synthetic_source_notes_dir / "data/synthetic_publication_source_figure_notes_backfill_summary.json"
    )
    field_summary = read_json(field_bundle_dir / "data/field_publication_claim_bundle_summary.json")
    field_policy = read_json(field_policy_dir / "data/field_dataset_policy_summary.json")
    field_source_notes = read_json(
        field_source_notes_dir / "data/field_publication_source_figure_notes_backfill_summary.json"
    )
    target1_probe_summary = read_json(
        target1_probe_dir / "data/local_2d_target1_probe_readiness_summary.json"
    )
    detector_handoff_summary = read_json(
        detector_handoff_dir / "data/local_2d_detector_handoff_budget_summary.json"
    )
    detector_alltriples_summary = read_json(
        detector_alltriples_dir / "data/local_2d_detector_alltriples_gate_summary.json"
    )
    field_cue_catalog_summary = read_json(
        field_cue_catalog_dir / "data/field_cue_support_catalog_summary.json"
    )
    detector_rank_budget_summary = read_json(
        detector_rank_budget_dir / "data/local_2d_detector_rank_budget_diagnostic_summary.json"
    )
    detector_component_gate_summary = read_json(
        detector_component_gate_dir / "data/local_2d_detector_component_waveform_gate_summary.json"
    )
    detector_component_selector_summary = read_json(
        detector_component_selector_dir / "data/local_2d_detector_component_selector_audit_summary.json"
    )
    detector_geometry_selector_summary = read_json(
        detector_geometry_selector_dir / "data/local_2d_detector_geometry_family_selector_summary.json"
    )
    detector_selector_gap_summary = read_json(
        detector_selector_gap_dir / "data/local_2d_detector_selector_gap_decomposition_summary.json"
    )
    detector_selector_counterfactual_summary = read_json(
        detector_selector_counterfactual_dir
        / "data/local_2d_detector_selector_counterfactual_sensitivity_summary.json"
    )
    detector_image_objective_rank_summary = read_json(
        detector_image_objective_rank_dir
        / "data/local_2d_detector_image_objective_rank_diagnostic_summary.json"
    )
    detector_target_failure_summary = read_json(
        detector_target_failure_dir / "data/local_2d_detector_target_failure_taxonomy_summary.json"
    )
    detector_depth_slot_prior_summary = read_json(
        detector_depth_slot_prior_dir / "data/local_2d_detector_depth_slot_prior_probe_summary.json"
    )
    detector_slot_component_assembly_summary = read_json(
        detector_slot_component_assembly_dir / "data/local_2d_detector_slot_component_assembly_summary.json"
    )
    detector_blind_envelope_summary = read_json(
        detector_blind_envelope_dir
        / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
    )
    detector_blind_envelope_robustness_summary = read_json(
        detector_blind_envelope_robustness_dir
        / "data/local_2d_detector_blind_envelope_robustness_summary.json"
    )
    detector_blind_envelope_stability_summary = read_json(
        detector_blind_envelope_stability_dir
        / "data/local_2d_detector_blind_envelope_policy_stability_summary.json"
    )
    detector_blind_envelope_tuning_summary = read_json(
        detector_blind_envelope_tuning_dir
        / "data/local_2d_detector_blind_envelope_tuning_sensitivity_summary.json"
    )
    detector_blind_envelope_reliability_summary = read_json(
        detector_blind_envelope_reliability_dir
        / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
    )
    detector_blind_envelope_reliability_threshold_summary = read_json(
        detector_blind_envelope_reliability_threshold_dir
        / "data/local_2d_detector_blind_envelope_reliability_threshold_sensitivity_summary.json"
    )
    detector_physics_ambiguity_link_summary = read_json(
        detector_physics_ambiguity_link_dir / "data/local_2d_detector_physics_ambiguity_link_summary.json"
    )
    detector_refinement_launch_contract_summary = read_json(
        detector_refinement_launch_contract_dir
        / "data/local_2d_detector_refinement_launch_contract_summary.json"
    )
    detector_component_seed_export_summary = read_json(
        detector_component_seed_export_dir / "data/local_2d_detector_component_seed_export_summary.json"
    )
    detector_refinement_neighborhood_budget_summary = read_json(
        detector_refinement_neighborhood_budget_dir
        / "data/local_2d_detector_lateral_slot_neighborhood_budget_summary.json"
    )
    detector_seed_geometry_error_audit_summary = read_json(
        detector_seed_geometry_error_audit_dir
        / "data/local_2d_detector_seed_geometry_error_audit_summary.json"
    )
    detector_radius_material_prior_scope_summary = read_json(
        detector_radius_material_prior_scope_dir
        / "data/local_2d_detector_radius_material_prior_scope_summary.json"
    )
    detector_controlled_prior_refinement_budget_summary = read_json(
        detector_controlled_prior_refinement_budget_dir
        / "data/local_2d_detector_controlled_prior_refinement_budget_summary.json"
    )
    detector_fixed_radius_pilot_outcome_synthesis_summary = read_json(
        detector_fixed_radius_pilot_outcome_synthesis_dir
        / "data/local_2d_detector_fixed_radius_pilot_outcome_synthesis_summary.json"
    )
    detector_fixed_radius_residual_ambiguity_audit_summary = read_json(
        detector_fixed_radius_residual_ambiguity_audit_dir
        / "data/local_2d_detector_fixed_radius_residual_ambiguity_summary.json"
    )
    detector_fixed_radius_locking_policy_validation_summary = read_json(
        detector_fixed_radius_locking_policy_validation_dir
        / "data/local_2d_detector_fixed_radius_locking_policy_validation_summary.json"
    )
    detector_sampling_boundary_integration_summary = read_json(
        detector_sampling_boundary_integration_dir
        / "data/local_2d_detector_sampling_boundary_integration_summary.json"
    )
    detector_upper_bound_summary = read_json(
        detector_upper_bound_dir / "data/local_2d_detector_upper_bound_policy_summary.json"
    )
    field_cue_timing_envelope_summary = read_json(
        field_cue_timing_envelope_dir / "data/field_cue_timing_envelope_summary.json"
    )
    field_spatial_transfer_summary = read_json(
        field_spatial_transfer_dir / "data/field_spatial_transfer_audit_summary.json"
    )
    field_anchor_interval_summary = read_json(
        field_anchor_interval_dir / "data/field_anchor_interval_reconciliation_summary.json"
    )
    field_dimensionality_summary = read_json(
        field_dimensionality_dir / "data/field_hpc_dimensionality_decision_summary.json"
    )
    field_time_zero_ladder_summary = read_json(
        field_time_zero_ladder_dir / "data/field_time_zero_evidence_ladder_summary.json"
    )
    field_short_anchor_leave_one_summary = read_json(
        field_short_anchor_leave_one_dir / "data/field_short_anchor_leave_one_summary.json"
    )
    field_short_anchor_spatial_consistency_summary = read_json(
        field_short_anchor_spatial_consistency_dir
        / "data/field_short_anchor_spatial_consistency_summary.json"
    )
    field_inversion_readiness_summary = read_json(
        field_inversion_readiness_dir / "data/field_inversion_readiness_synthesis_summary.json"
    )
    field_short_anchor_radius_degeneracy_summary = read_json(
        field_short_anchor_radius_degeneracy_dir / "data/field_short_anchor_radius_degeneracy_summary.json"
    )
    field_short_anchor_signed_morphology_summary = read_json(
        field_short_anchor_signed_morphology_dir / "data/field_short_anchor_signed_morphology_summary.json"
    )
    field_short_anchor_signed_morphology_sensitivity_summary = read_json(
        field_short_anchor_signed_morphology_sensitivity_dir
        / "data/field_short_anchor_signed_morphology_sensitivity_summary.json"
    )
    field_collection_handoff_summary = read_json(
        field_collection_handoff_dir / "data/field_controlled_collection_handoff_summary.json"
    )
    audit_summary = read_json(audit_root / "data/local_2d_field_manuscript_evidence_audit_summary.json")

    synthetic_figures = read_csv_rows(
        synthetic_bundle_dir / "data/synthetic_2d_publication_figure_rows.csv"
    )
    synthetic_claims = read_csv_rows(
        synthetic_bundle_dir / "data/synthetic_2d_publication_claim_boundaries.csv"
    )
    field_figures = read_csv_rows(field_bundle_dir / "data/field_publication_figure_rows.csv")
    field_claims = read_csv_rows(field_bundle_dir / "data/field_publication_claim_boundaries.csv")

    claim_rows = combine_claim_rows(synthetic_claims, field_claims)
    figure_rows = combine_figure_rows(synthetic_figures, field_figures)
    metrics = metric_rows(
        synthetic_summary,
        synthetic_next,
        field_summary,
        field_policy,
        audit_summary,
        synthetic_source_notes,
        field_source_notes,
        target1_probe_summary,
        detector_handoff_summary,
        detector_alltriples_summary,
        field_cue_catalog_summary,
        detector_rank_budget_summary,
        detector_component_gate_summary,
        detector_component_selector_summary,
        detector_geometry_selector_summary,
        detector_selector_gap_summary,
        detector_selector_counterfactual_summary,
        detector_image_objective_rank_summary,
        detector_target_failure_summary,
        detector_depth_slot_prior_summary,
        detector_slot_component_assembly_summary,
        detector_blind_envelope_summary,
        detector_blind_envelope_robustness_summary,
        detector_blind_envelope_stability_summary,
        detector_blind_envelope_tuning_summary,
        detector_blind_envelope_reliability_summary,
        detector_blind_envelope_reliability_threshold_summary,
        detector_physics_ambiguity_link_summary,
        detector_refinement_launch_contract_summary,
        detector_component_seed_export_summary,
        detector_refinement_neighborhood_budget_summary,
        detector_seed_geometry_error_audit_summary,
        detector_upper_bound_summary,
        field_cue_timing_envelope_summary,
        field_spatial_transfer_summary,
        field_anchor_interval_summary,
        field_dimensionality_summary,
        field_time_zero_ladder_summary,
        field_short_anchor_leave_one_summary,
        field_short_anchor_spatial_consistency_summary,
        field_inversion_readiness_summary,
        detector_sampling_boundary_integration_summary,
        field_short_anchor_radius_degeneracy_summary,
        field_short_anchor_signed_morphology_summary,
        field_short_anchor_signed_morphology_sensitivity_summary,
        field_collection_handoff_summary,
        detector_radius_material_prior_scope_summary,
        detector_controlled_prior_refinement_budget_summary,
        detector_fixed_radius_pilot_outcome_synthesis_summary,
        detector_fixed_radius_residual_ambiguity_audit_summary,
        detector_fixed_radius_locking_policy_validation_summary,
    )
    summary = summarize_table_pack(
        claim_rows,
        figure_rows,
        metrics,
        synthetic_summary,
        synthetic_next,
        field_summary,
        field_policy,
        audit_summary,
        synthetic_source_notes,
        field_source_notes,
        target1_probe_summary,
        detector_handoff_summary,
        detector_alltriples_summary,
        field_cue_catalog_summary,
        detector_rank_budget_summary,
        detector_component_gate_summary,
        detector_component_selector_summary,
        detector_geometry_selector_summary,
        detector_selector_gap_summary,
        detector_selector_counterfactual_summary,
        detector_image_objective_rank_summary,
        detector_target_failure_summary,
        detector_depth_slot_prior_summary,
        detector_slot_component_assembly_summary,
        detector_blind_envelope_summary,
        detector_blind_envelope_robustness_summary,
        detector_blind_envelope_stability_summary,
        detector_blind_envelope_tuning_summary,
        detector_blind_envelope_reliability_summary,
        detector_blind_envelope_reliability_threshold_summary,
        detector_physics_ambiguity_link_summary,
        detector_refinement_launch_contract_summary,
        detector_component_seed_export_summary,
        detector_refinement_neighborhood_budget_summary,
        detector_seed_geometry_error_audit_summary,
        detector_upper_bound_summary,
        field_cue_timing_envelope_summary,
        field_spatial_transfer_summary,
        field_anchor_interval_summary,
        field_dimensionality_summary,
        field_time_zero_ladder_summary,
        field_short_anchor_leave_one_summary,
        field_short_anchor_spatial_consistency_summary,
        field_inversion_readiness_summary,
        detector_sampling_boundary_integration_summary,
        field_short_anchor_radius_degeneracy_summary,
        field_short_anchor_signed_morphology_summary,
        field_short_anchor_signed_morphology_sensitivity_summary,
        field_collection_handoff_summary,
        detector_radius_material_prior_scope_summary,
        detector_controlled_prior_refinement_budget_summary,
        detector_fixed_radius_pilot_outcome_synthesis_summary,
        detector_fixed_radius_residual_ambiguity_audit_summary,
        detector_fixed_radius_locking_policy_validation_summary,
    )

    outdir = Path(allocate_output_dir(args.outdir, args.run_name, root="outputs/summary_tables"))
    data_dir = outdir / "data"
    figures_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    claim_csv = data_dir / "local_2d_field_manuscript_claim_table.csv"
    figure_csv = data_dir / "local_2d_field_manuscript_figure_inventory.csv"
    metric_csv = data_dir / "local_2d_field_manuscript_result_metrics.csv"
    summary_json = data_dir / "local_2d_field_manuscript_table_pack_summary.json"
    validation_csv = data_dir / "figure_validation.csv"
    figure_path = figures_dir / "local_2d_field_manuscript_table_pack.png"
    figure_notes = figures_dir / "FIGURE_NOTES.md"

    write_csv(claim_csv, [json_safe(row) for row in claim_rows])
    write_csv(figure_csv, [json_safe(row) for row in figure_rows])
    write_csv(metric_csv, [json_safe(row) for row in metrics])
    plot_table_pack(summary, figure_path)
    write_csv(validation_csv, [json_safe(figure_stats(figure_path))])
    write_figure_notes(figure_notes, summary, claim_csv, figure_csv, metric_csv, validation_csv)

    summary["paths"] = {
        "claim_table_csv": str(claim_csv),
        "figure_inventory_csv": str(figure_csv),
        "result_metrics_csv": str(metric_csv),
        "synthetic_source_notes_summary_json": str(
            synthetic_source_notes_dir
            / "data/synthetic_publication_source_figure_notes_backfill_summary.json"
        ),
        "field_source_notes_summary_json": str(
            field_source_notes_dir / "data/field_publication_source_figure_notes_backfill_summary.json"
        ),
        "target1_probe_scorecard_summary_json": str(
            target1_probe_dir / "data/local_2d_target1_probe_readiness_summary.json"
        ),
        "detector_handoff_budget_summary_json": str(
            detector_handoff_dir / "data/local_2d_detector_handoff_budget_summary.json"
        ),
        "detector_alltriples_gate_summary_json": str(
            detector_alltriples_dir / "data/local_2d_detector_alltriples_gate_summary.json"
        ),
        "field_cue_support_catalog_summary_json": str(
            field_cue_catalog_dir / "data/field_cue_support_catalog_summary.json"
        ),
        "detector_rank_budget_summary_json": str(
            detector_rank_budget_dir / "data/local_2d_detector_rank_budget_diagnostic_summary.json"
        ),
        "detector_component_gate_summary_json": str(
            detector_component_gate_dir / "data/local_2d_detector_component_waveform_gate_summary.json"
        ),
        "detector_component_selector_summary_json": str(
            detector_component_selector_dir / "data/local_2d_detector_component_selector_audit_summary.json"
        ),
        "detector_geometry_selector_summary_json": str(
            detector_geometry_selector_dir / "data/local_2d_detector_geometry_family_selector_summary.json"
        ),
        "detector_selector_gap_summary_json": str(
            detector_selector_gap_dir / "data/local_2d_detector_selector_gap_decomposition_summary.json"
        ),
        "detector_selector_counterfactual_summary_json": str(
            detector_selector_counterfactual_dir
            / "data/local_2d_detector_selector_counterfactual_sensitivity_summary.json"
        ),
        "detector_image_objective_rank_summary_json": str(
            detector_image_objective_rank_dir
            / "data/local_2d_detector_image_objective_rank_diagnostic_summary.json"
        ),
        "detector_target_failure_taxonomy_summary_json": str(
            detector_target_failure_dir / "data/local_2d_detector_target_failure_taxonomy_summary.json"
        ),
        "detector_depth_slot_prior_probe_summary_json": str(
            detector_depth_slot_prior_dir / "data/local_2d_detector_depth_slot_prior_probe_summary.json"
        ),
        "detector_slot_component_assembly_summary_json": str(
            detector_slot_component_assembly_dir / "data/local_2d_detector_slot_component_assembly_summary.json"
        ),
        "detector_blind_envelope_summary_json": str(
            detector_blind_envelope_dir
            / "data/local_2d_detector_blind_component_envelope_assembly_summary.json"
        ),
        "detector_blind_envelope_robustness_summary_json": str(
            detector_blind_envelope_robustness_dir
            / "data/local_2d_detector_blind_envelope_robustness_summary.json"
        ),
        "detector_blind_envelope_stability_summary_json": str(
            detector_blind_envelope_stability_dir
            / "data/local_2d_detector_blind_envelope_policy_stability_summary.json"
        ),
        "detector_blind_envelope_tuning_summary_json": str(
            detector_blind_envelope_tuning_dir
            / "data/local_2d_detector_blind_envelope_tuning_sensitivity_summary.json"
        ),
        "detector_blind_envelope_reliability_summary_json": str(
            detector_blind_envelope_reliability_dir
            / "data/local_2d_detector_blind_envelope_reliability_gate_summary.json"
        ),
        "detector_blind_envelope_reliability_threshold_summary_json": str(
            detector_blind_envelope_reliability_threshold_dir
            / "data/local_2d_detector_blind_envelope_reliability_threshold_sensitivity_summary.json"
        ),
        "detector_physics_ambiguity_link_summary_json": str(
            detector_physics_ambiguity_link_dir / "data/local_2d_detector_physics_ambiguity_link_summary.json"
        ),
        "detector_refinement_launch_contract_summary_json": str(
            detector_refinement_launch_contract_dir
            / "data/local_2d_detector_refinement_launch_contract_summary.json"
        ),
        "detector_component_seed_export_summary_json": str(
            detector_component_seed_export_dir / "data/local_2d_detector_component_seed_export_summary.json"
        ),
        "detector_lateral_slot_neighborhood_budget_summary_json": str(
            detector_refinement_neighborhood_budget_dir
            / "data/local_2d_detector_lateral_slot_neighborhood_budget_summary.json"
        ),
        "detector_seed_geometry_error_audit_summary_json": str(
            detector_seed_geometry_error_audit_dir
            / "data/local_2d_detector_seed_geometry_error_audit_summary.json"
        ),
        "detector_radius_material_prior_scope_summary_json": str(
            detector_radius_material_prior_scope_dir
            / "data/local_2d_detector_radius_material_prior_scope_summary.json"
        ),
        "detector_controlled_prior_refinement_budget_summary_json": str(
            detector_controlled_prior_refinement_budget_dir
            / "data/local_2d_detector_controlled_prior_refinement_budget_summary.json"
        ),
        "detector_fixed_radius_pilot_outcome_synthesis_summary_json": str(
            detector_fixed_radius_pilot_outcome_synthesis_dir
            / "data/local_2d_detector_fixed_radius_pilot_outcome_synthesis_summary.json"
        ),
        "detector_fixed_radius_residual_ambiguity_audit_summary_json": str(
            detector_fixed_radius_residual_ambiguity_audit_dir
            / "data/local_2d_detector_fixed_radius_residual_ambiguity_summary.json"
        ),
        "detector_fixed_radius_locking_policy_validation_summary_json": str(
            detector_fixed_radius_locking_policy_validation_dir
            / "data/local_2d_detector_fixed_radius_locking_policy_validation_summary.json"
        ),
        "detector_sampling_boundary_integration_summary_json": str(
            detector_sampling_boundary_integration_dir
            / "data/local_2d_detector_sampling_boundary_integration_summary.json"
        ),
        "detector_upper_bound_policy_summary_json": str(
            detector_upper_bound_dir / "data/local_2d_detector_upper_bound_policy_summary.json"
        ),
        "field_cue_timing_envelope_summary_json": str(
            field_cue_timing_envelope_dir / "data/field_cue_timing_envelope_summary.json"
        ),
        "field_spatial_transfer_summary_json": str(
            field_spatial_transfer_dir / "data/field_spatial_transfer_audit_summary.json"
        ),
        "field_anchor_interval_summary_json": str(
            field_anchor_interval_dir / "data/field_anchor_interval_reconciliation_summary.json"
        ),
        "field_dimensionality_decision_summary_json": str(
            field_dimensionality_dir / "data/field_hpc_dimensionality_decision_summary.json"
        ),
        "field_time_zero_ladder_summary_json": str(
            field_time_zero_ladder_dir / "data/field_time_zero_evidence_ladder_summary.json"
        ),
        "field_short_anchor_leave_one_summary_json": str(
            field_short_anchor_leave_one_dir / "data/field_short_anchor_leave_one_summary.json"
        ),
        "field_short_anchor_spatial_consistency_summary_json": str(
            field_short_anchor_spatial_consistency_dir
            / "data/field_short_anchor_spatial_consistency_summary.json"
        ),
        "field_inversion_readiness_summary_json": str(
            field_inversion_readiness_dir / "data/field_inversion_readiness_synthesis_summary.json"
        ),
        "field_short_anchor_radius_degeneracy_summary_json": str(
            field_short_anchor_radius_degeneracy_dir / "data/field_short_anchor_radius_degeneracy_summary.json"
        ),
        "field_short_anchor_signed_morphology_summary_json": str(
            field_short_anchor_signed_morphology_dir / "data/field_short_anchor_signed_morphology_summary.json"
        ),
        "field_short_anchor_signed_morphology_sensitivity_summary_json": str(
            field_short_anchor_signed_morphology_sensitivity_dir
            / "data/field_short_anchor_signed_morphology_sensitivity_summary.json"
        ),
        "field_collection_handoff_summary_json": str(
            field_collection_handoff_dir / "data/field_controlled_collection_handoff_summary.json"
        ),
        "summary_json": str(summary_json),
        "figure": str(figure_path),
        "figure_notes": str(figure_notes),
        "figure_validation_csv": str(validation_csv),
    }
    summary_json.write_text(json.dumps(json_safe(summary), indent=2) + "\n", encoding="utf-8")
    write_run_manifest(
        str(outdir),
        "local_2d_field_manuscript_table_pack",
        {
            "synthetic_bundle_run": args.synthetic_bundle_run,
            "synthetic_next_matrix_run": args.synthetic_next_matrix_run,
            "synthetic_source_notes_run": args.synthetic_source_notes_run,
            "field_bundle_run": args.field_bundle_run,
            "field_policy_run": args.field_policy_run,
            "field_source_notes_run": args.field_source_notes_run,
            "target1_probe_scorecard_run": args.target1_probe_scorecard_run,
            "detector_handoff_budget_run": args.detector_handoff_budget_run,
            "detector_alltriples_gate_run": args.detector_alltriples_gate_run,
            "field_cue_support_catalog_run": args.field_cue_support_catalog_run,
            "detector_rank_budget_run": args.detector_rank_budget_run,
            "detector_component_gate_run": args.detector_component_gate_run,
            "detector_component_selector_run": args.detector_component_selector_run,
            "detector_geometry_selector_run": args.detector_geometry_selector_run,
            "detector_selector_gap_run": args.detector_selector_gap_run,
            "detector_selector_counterfactual_run": args.detector_selector_counterfactual_run,
            "detector_image_objective_rank_run": args.detector_image_objective_rank_run,
            "detector_target_failure_taxonomy_run": args.detector_target_failure_taxonomy_run,
            "detector_depth_slot_prior_run": args.detector_depth_slot_prior_run,
            "detector_slot_component_assembly_run": args.detector_slot_component_assembly_run,
            "detector_blind_envelope_run": args.detector_blind_envelope_run,
            "detector_blind_envelope_robustness_run": args.detector_blind_envelope_robustness_run,
            "detector_blind_envelope_stability_run": args.detector_blind_envelope_stability_run,
            "detector_blind_envelope_tuning_run": args.detector_blind_envelope_tuning_run,
            "detector_blind_envelope_reliability_run": args.detector_blind_envelope_reliability_run,
            "detector_blind_envelope_reliability_threshold_run": (
                args.detector_blind_envelope_reliability_threshold_run
            ),
            "detector_physics_ambiguity_link_run": args.detector_physics_ambiguity_link_run,
            "detector_refinement_launch_contract_run": args.detector_refinement_launch_contract_run,
            "detector_component_seed_export_run": args.detector_component_seed_export_run,
            "detector_refinement_neighborhood_budget_run": args.detector_refinement_neighborhood_budget_run,
            "detector_seed_geometry_error_audit_run": args.detector_seed_geometry_error_audit_run,
            "detector_radius_material_prior_scope_run": args.detector_radius_material_prior_scope_run,
            "detector_controlled_prior_refinement_budget_run": (
                args.detector_controlled_prior_refinement_budget_run
            ),
            "detector_fixed_radius_pilot_outcome_synthesis_run": (
                args.detector_fixed_radius_pilot_outcome_synthesis_run
            ),
            "detector_fixed_radius_residual_ambiguity_audit_run": (
                args.detector_fixed_radius_residual_ambiguity_audit_run
            ),
            "detector_fixed_radius_locking_policy_validation_run": (
                args.detector_fixed_radius_locking_policy_validation_run
            ),
            "detector_sampling_boundary_integration_run": args.detector_sampling_boundary_integration_run,
            "detector_upper_bound_policy_run": args.detector_upper_bound_policy_run,
            "field_cue_timing_envelope_run": args.field_cue_timing_envelope_run,
            "field_spatial_transfer_run": args.field_spatial_transfer_run,
            "field_anchor_interval_run": args.field_anchor_interval_run,
            "field_dimensionality_decision_run": args.field_dimensionality_decision_run,
            "field_time_zero_ladder_run": args.field_time_zero_ladder_run,
            "field_short_anchor_leave_one_run": args.field_short_anchor_leave_one_run,
            "field_short_anchor_spatial_consistency_run": args.field_short_anchor_spatial_consistency_run,
            "field_inversion_readiness_run": args.field_inversion_readiness_run,
            "field_short_anchor_radius_degeneracy_run": args.field_short_anchor_radius_degeneracy_run,
            "field_short_anchor_signed_morphology_run": args.field_short_anchor_signed_morphology_run,
            "field_short_anchor_signed_morphology_sensitivity_run": (
                args.field_short_anchor_signed_morphology_sensitivity_run
            ),
            "field_collection_handoff_run": args.field_collection_handoff_run,
            "audit_run": args.audit_run,
            "dataset_id": args.dataset_id,
            "readgssi_version": readgssi_version(),
            "summary_json": str(summary_json),
            "figure": str(figure_path),
            "figure_notes": str(figure_notes),
        },
    )
    print(json.dumps(json_safe(summary), indent=2))


if __name__ == "__main__":
    main()
