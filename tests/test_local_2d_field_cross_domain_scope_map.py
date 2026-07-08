from pathlib import Path

import pytest

from run_local_2d_field_cross_domain_scope_map import (
    build_scope_rows,
    summarize_scope,
    write_figure_notes,
)


def _inputs():
    resolution_summary = {
        "physical_nonoverlap_guardrail_mm": 14.0,
        "target2_close50_ambiguous_seed_values": "seed13",
    }
    resolution_rows = [
        {
            "map_key": "physical_nonoverlap_guardrail",
            "claim_status": "allowed_physical_spacing_guardrail",
            "support_count": "13",
            "total_count": "18",
        },
        {
            "map_key": "target2_close14_source5_txrx45_objective_limit",
            "primary_metric_value": "6",
            "support_count": "6",
            "total_count": "6",
        },
        {
            "map_key": "target2_close50_linear29p5_seed_frequency",
            "support_count": "2",
            "total_count": "3",
        },
        {"map_key": "current_synthetic_gpu_queue", "claim_status": "no_current_gpu_candidate"},
    ]
    synthetic_bundle = {"figure_count": 9, "claim_boundary_count": 11}
    synthetic_next = {
        "gpu_priority": "none_now",
        "immediate_gpu_priority_count": 0,
        "conditional_gpu_candidate_count": 0,
    }
    field_cue_spacing = {
        "min_same_time_lateral_spacing_mm_across_thresholds": 96.657,
        "synthetic_close_spacing_context_max_mm": 50.0,
        "ready_for_field_context": True,
        "ready_for_resolution_benchmark": False,
    }
    field_timing_window = {
        "early_strict_near_zero_lag_row_count": 6,
        "early_strict_row_count": 6,
        "short_nonraw_supported_count": 18,
        "short_nonraw_row_count": 18,
        "long_reject_short_transfer_row_count": 3,
        "long_row_count": 3,
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
    }
    field_bundle = {
        "gpu_priority": "none",
        "figure_row_count": 20,
        "claim_boundary_count": 19,
    }
    field_policy = {"publication_claim_bundle_gpu_priority": "none"}
    table_pack = {
        "gpu_priority": "none",
        "ready_for_manuscript_table_use": True,
        "detector_radius_material_prior_controlled_ready": True,
        "detector_radius_material_prior_detector_inferred_ready": False,
        "detector_controlled_prior_refinement_fixed_fine_points": 29_936_602,
        "detector_controlled_prior_refinement_permutation_multiplier": 6.0,
        "detector_controlled_prior_refinement_launch_ready": False,
        "detector_controlled_prior_refinement_ready_for_fwi": False,
        "field_collection_handoff_ready_field_fwi": False,
        "field_collection_handoff_ready_3d_hpc": False,
    }
    return {
        "resolution_summary": resolution_summary,
        "resolution_rows": resolution_rows,
        "synthetic_bundle": synthetic_bundle,
        "synthetic_next": synthetic_next,
        "field_cue_spacing": field_cue_spacing,
        "field_timing_window": field_timing_window,
        "field_bundle": field_bundle,
        "field_policy": field_policy,
        "table_pack": table_pack,
    }


def test_build_scope_rows_keeps_field_and_synthetic_claims_separate():
    rows = build_scope_rows(**_inputs())
    by_key = {row["scope_key"]: row for row in rows}

    assert len(rows) == 8
    assert by_key["synthetic_known_truth_resolution_only"]["decision"] == (
        "synthetic_result_field_context_only"
    )
    assert "validates the synthetic" in by_key["synthetic_known_truth_resolution_only"]["blocked_joint_claim"]
    assert by_key["field_spacing_outside_synthetic_stress_regime"]["primary_metric"] == pytest.approx(1.93314)
    assert by_key["field_timing_window_family_boundary"]["primary_metric"] == 1.0
    assert "absolute time-zero" in by_key["field_timing_window_family_boundary"]["blocked_joint_claim"]
    assert by_key["detector_controlled_prior_refinement_scope"]["decision"] == (
        "controlled_prior_budget_no_launch"
    )
    assert by_key["detector_controlled_prior_refinement_scope"]["primary_metric"] == 6.0
    assert "field transfer" in by_key["detector_controlled_prior_refinement_scope"]["blocked_joint_claim"]


def test_summarize_scope_ready_no_gpu_and_not_field_resolution():
    inputs = _inputs()
    rows = build_scope_rows(**inputs)
    summary = summarize_scope(
        rows,
        field_cue_spacing=inputs["field_cue_spacing"],
        field_timing_window=inputs["field_timing_window"],
        synthetic_next=inputs["synthetic_next"],
        field_bundle=inputs["field_bundle"],
        field_policy=inputs["field_policy"],
        table_pack=inputs["table_pack"],
    )

    assert summary["policy_label"] == "local_2d_field_cross_domain_scope_map_ready_no_gpu"
    assert summary["ready_for_manuscript_scope_table"] is True
    assert summary["field_ready_for_resolution_benchmark"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["field_to_synthetic_spacing_ratio"] == pytest.approx(1.93314)
    assert summary["field_timing_short_nonraw_supported_fraction"] == 1.0
    assert summary["detector_controlled_prior_ready"] is True
    assert summary["detector_inferred_radius_material_ready"] is False
    assert summary["detector_controlled_prior_fixed_fine_points"] == 29_936_602
    assert summary["detector_controlled_prior_permutation_multiplier"] == 6.0
    assert summary["detector_controlled_prior_launch_ready"] is False
    assert summary["detector_controlled_prior_fwi_ready"] is False
    assert summary["gpu_priority"] == "none"


def test_write_figure_notes_documents_scope_boundary(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "scope_ready",
        "scope_row_count": 7,
        "field_to_synthetic_spacing_ratio": 1.93314,
        "field_ready_for_resolution_benchmark": False,
        "field_fwi_ready": False,
        "detector_controlled_prior_ready": True,
        "detector_inferred_radius_material_ready": False,
        "detector_controlled_prior_fixed_fine_points": 29_936_602,
        "detector_controlled_prior_launch_ready": False,
        "detector_controlled_prior_fwi_ready": False,
        "gpu_priority": "none",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_2d_field_cross_domain_scope_map.png" in text
    assert "does not merge synthetic known-truth resolution claims" in text
    assert "FWI claims" in text
