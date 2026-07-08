from run_gssi_field_time_zero_evidence_ladder import build_ladder_rows, summarize_ladder


def _inputs():
    budget = {
        "ready_for_manuscript_time_zero_budget": True,
        "field_fwi_ready": False,
        "relative_anchor_offset_ns": 0.12770137524557956,
        "conservative_half_width_ns": 0.058939096267190516,
        "bootstrap_ci_width_ns": 0.045,
        "max_abs_content_anchor_residual_ns": 0.012,
    }
    perturbation = {
        "ready_for_manuscript_uncertainty_sensitivity": True,
        "field_fwi_ready": False,
        "supported_row_count": 8,
        "row_count": 8,
        "min_nonraw_matrix_improvement": 0.25,
        "min_nonraw_corrected_abs_correlation": 0.91,
    }
    conflict = {
        "ready_for_manuscript_field_timing_boundary": True,
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "early_vs_short_delta_half_widths": 1.8,
        "long_vs_short_delta_half_widths": 2.4,
    }
    discriminant = {
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "short_nonraw_supported_count": 4,
        "short_nonraw_row_count": 4,
        "early_has_low_uniqueness_margin": True,
    }
    envelope = {
        "ready_for_short_relative_timing_qc": True,
        "ready_for_long_short_transfer": False,
        "ready_for_absolute_time_zero": False,
        "short_anchor_inside_envelope_count": 3,
        "long_pattern_reject_short_transfer_count": 8,
    }
    spatial_transfer = {
        "ready_for_short_to_long_timing_transfer": False,
        "long_pattern_anchor_count": 8,
        "long_pattern_with_nearest_short_content_within_threshold_count": 1,
        "median_long_to_short_distance_mm": 701.5965,
    }
    anchor_interval = {
        "ready_for_short_relative_timing_qc": True,
        "ready_for_absolute_time_zero": False,
        "short_anchor_count": 3,
        "short_anchor_inside_supported_interval_count": 3,
        "short_content_anchor_count": 2,
        "short_content_anchor_inside_supported_interval_count": 2,
        "min_margin_to_supported_interval_edge_mm": 13.332,
    }
    dimensionality = {
        "ready_for_long_short_transfer": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "is_3d_survey": False,
    }
    return budget, perturbation, conflict, discriminant, envelope, spatial_transfer, anchor_interval, dimensionality


def test_ladder_rows_support_short_qc_and_block_heavy_field_uses():
    budget, perturbation, conflict, discriminant, envelope, spatial_transfer, anchor_interval, dimensionality = _inputs()

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
    by_key = {row["gate_key"]: row for row in rows}

    assert by_key["short_relative_timing_budget"]["status"] == "supported"
    assert by_key["perturbation_robustness"]["status"] == "supported"
    assert by_key["anchor_interval_support"]["status"] == "supported"
    assert by_key["long_short_transfer"]["status"] == "blocked"
    assert by_key["absolute_time_zero"]["status"] == "blocked"
    assert by_key["field_fwi_hpc"]["status"] == "blocked"
    assert by_key["field_fwi_hpc"]["readiness_score"] == 0.0


def test_ladder_summary_keeps_field_policy_cpu_short_relative_only():
    budget, perturbation, conflict, discriminant, envelope, spatial_transfer, anchor_interval, dimensionality = _inputs()
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

    assert summary["policy_label"] == "gssi51600s_field_time_zero_evidence_ladder_short_qc_only"
    assert summary["ladder_row_count"] == 7
    assert summary["ready_for_short_relative_timing_qc"] is True
    assert summary["ready_for_long_short_transfer"] is False
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["short_anchor_inside_supported_interval_count"] == 3
    assert summary["long_pattern_reject_short_transfer_count"] == 8
    assert summary["gpu_priority"] == "none"
