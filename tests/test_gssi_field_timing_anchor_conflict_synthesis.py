from run_gssi_field_timing_anchor_conflict_synthesis import (
    anchor_rows,
    claim_boundary_rows,
    guardrail_rows,
    summarize_conflict,
)


def _summaries():
    return {
        "time_zero_budget": {
            "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
            "relative_anchor_offset_ns": 0.127701,
            "conservative_half_width_ns": 0.058939,
            "bootstrap_ci_lower_ns": 0.108055,
            "bootstrap_ci_upper_ns": 0.147348,
            "absolute_time_zero_ready": False,
            "field_fwi_ready": False,
        },
        "time_zero_perturbation": {
            "policy_label": "field_time_zero_ci_perturbation_stack_robust",
            "bootstrap_ci_supported_count": 9,
            "bootstrap_ci_row_count": 9,
            "conservative_supported_count": 6,
            "conservative_row_count": 6,
            "field_fwi_ready": False,
        },
        "early_time_anchor": {
            "policy_label": "field_early_time_common_mode_not_content_time_zero",
            "short_pair_early_shift_ns": 0.0,
            "short_pair_early_agrees_with_content_budget": False,
            "absolute_time_zero_ready": False,
            "field_fwi_ready": False,
        },
        "long_shift_sensitivity": {
            "policy_label": "long_profile_pattern_shift_window_robust_rejects_short_transfer",
            "best_offset_median_ns": 0.06,
            "reject_short_transfer_window_count": 3,
            "window_count": 3,
        },
        "acquisition_readiness": {
            "policy_label": "field_acquisition_readiness_2d_qc_not_hpc_fwi",
            "ready_for_2d_qc": True,
            "ready_for_field_fwi": False,
        },
        "apparent_depth_qc": {
            "policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth",
            "ready_for_cover_depth_recovery": False,
            "ready_for_field_fwi": False,
        },
        "hyperbola_timezero_degeneracy": {
            "policy_label": "field_hyperbola_timezero_degeneracy_not_calibrated_inversion",
            "radius_claim_ready": False,
            "field_fwi_ready": False,
        },
    }


def test_anchor_rows_quantify_timing_anchor_conflicts():
    rows = anchor_rows(_summaries())
    by_source = {row["anchor_source"]: row for row in rows}

    assert len(rows) == 7
    assert by_source["short_content_backed_relative_time_zero"]["offset_ns"] == 0.127701
    assert by_source["early_common_mode_direct_ringdown"]["offset_ns"] == 0.0
    assert by_source["early_common_mode_direct_ringdown"]["delta_to_short_content_ns"] == 0.127701
    assert by_source["early_common_mode_direct_ringdown"]["delta_to_short_content_half_widths"] > 2.0
    assert by_source["long_pattern_only_shift"]["offset_ns"] == 0.06
    assert by_source["long_pattern_only_shift"]["delta_to_short_content_half_widths"] > 1.0
    assert by_source["conservative_lower"]["support_status"] == "conservative_envelope_supported"


def test_guardrail_rows_preserve_no_fwi_no_cover_depth_boundaries():
    rows = guardrail_rows(_summaries())
    by_guardrail = {row["guardrail"]: row for row in rows}

    assert by_guardrail["acquisition_readiness"]["value"] == 0.0
    assert by_guardrail["apparent_depth_qc"]["value"] == 0.0
    assert by_guardrail["hyperbola_timezero_degeneracy"]["value"] == 0.0
    assert "blocks calibrated inversion" in by_guardrail["hyperbola_timezero_degeneracy"]["claim_boundary"]


def test_summarize_conflict_marks_short_relative_not_absolute_ready():
    summaries = _summaries()
    anchors = anchor_rows(summaries)
    guardrails = guardrail_rows(summaries)
    summary = summarize_conflict(anchors, guardrails, summaries)

    assert summary["policy_label"] == "field_timing_anchor_conflict_short_relative_not_absolute"
    assert summary["anchor_row_count"] == 7
    assert summary["guardrail_row_count"] == 7
    assert summary["claim_boundary_count"] == 4
    assert summary["early_agrees_with_content_budget"] is False
    assert summary["early_vs_short_delta_half_widths"] > 2.0
    assert summary["long_pattern_rejects_short_transfer_all_windows"] is True
    assert summary["perturbation_budget_supported"] is True
    assert summary["absolute_time_zero_ready"] is False
    assert summary["cover_depth_ready"] is False
    assert summary["radius_ready"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["ready_for_manuscript_field_timing_boundary"] is True
    assert summary["gpu_priority"] == "none"


def test_claim_boundary_rows_block_anchor_reconciliation_into_absolute_time_zero():
    rows = claim_boundary_rows()
    text = " ".join(row["not_allowed"] for row in rows)

    assert len(rows) == 4
    assert "absolute time-zero" in text
    assert "transfer it to the long pair" in text
    assert "inversion result" in text
