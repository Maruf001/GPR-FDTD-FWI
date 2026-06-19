import math

from run_gssi_field_acquisition_readiness_audit import (
    acquisition_sampling_metrics,
    build_audit,
    medium_velocity_m_per_ns,
    two_way_depth_equivalent_mm,
)


def _minimal_data():
    return {
        "dzt": {
            "dzt_file_count": 4,
            "profile_channel_count": 4,
            "records": [
                {
                    "scan_spacing_m": 0.003333,
                    "antenna_frequency_mhz": 1600.0,
                    "dielectric": 2.25,
                    "time_range_ns": 5.0,
                    "profile_length_m": 0.909909,
                    "traces": 274,
                    "samples": 510,
                },
                {
                    "scan_spacing_m": 0.003333,
                    "antenna_frequency_mhz": 1600.0,
                    "dielectric": 2.25,
                    "time_range_ns": 5.0,
                    "profile_length_m": 2.709729,
                    "traces": 814,
                    "samples": 510,
                },
            ],
        },
        "survey": {"classification": "independent_2d_line_profiles"},
        "network": {"pair_label_counts": {"repeat_candidate": 2, "embedded_segment_candidate": 0}},
        "short_stack": {
            "summary": {
                "alignment_label": "strong_reversed_scan_preferred",
                "best_normalized_correlation": 0.931186,
            }
        },
        "long_stack": {
            "summary": {
                "alignment_label": "moderate_direct_scan_preferred",
                "comparison_profile_missing_phase_anchor_picks": True,
            }
        },
        "spatial_support": {
            "policy_label": "corrected_stack_spatial_support_sparse",
            "all_window_supported_column_fraction": 0.281124,
            "all_window_supported_column_count": 70,
            "finite_column_count": 249,
        },
        "supported_interval": {
            "policy_label": "supported_interval_visual_qc_ready",
            "selected_interval_count": 3,
            "supported_interval_count": 3,
            "total_selected_interval_length_m": 0.16665,
        },
        "time_zero_budget": {
            "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
            "conservative_half_width_ns": 0.058939096267190516,
            "absolute_time_zero_ready": False,
        },
        "time_zero_perturbation": {
            "policy_label": "field_time_zero_ci_perturbation_stack_robust",
            "bootstrap_ci_supported_count": 9,
            "bootstrap_ci_row_count": 9,
        },
        "field_policy": {"policy_label": "field_2d_qc_not_3d_or_fwi"},
    }


def _event_rows():
    return [
        {
            "tier_key": "short_content_time_zero_anchors",
            "support_fraction": "0.6666666666666666",
            "claim_allowed": "short-pair content-backed relative time-zero visual QC",
            "claim_blocked": "absolute time-zero, radius, cover depth, 3D, or field FWI",
        },
        {
            "tier_key": "long_stable_pattern_anchors",
            "support_fraction": "1.0",
            "claim_allowed": "long-pair stable-anchor pattern-only visual QC",
            "claim_blocked": "phase anchor or transferable time-zero correction",
        },
        {
            "tier_key": "field_fwi_readiness_blocked",
            "support_tier": "blocked_not_ready",
        },
    ]


def test_medium_velocity_and_depth_equivalent_are_two_way():
    velocity = medium_velocity_m_per_ns(2.25)
    depth_mm = two_way_depth_equivalent_mm(0.058939096267190516, 2.25)

    assert math.isclose(velocity, 0.19986163866666667)
    assert math.isclose(depth_mm, 5.889832180746556)


def test_acquisition_sampling_metrics_quantify_dense_alongline_sampling():
    metrics = acquisition_sampling_metrics(_minimal_data()["dzt"])

    assert metrics["profile_count"] == 2
    assert math.isclose(metrics["scan_spacing_mm"], 3.333)
    assert math.isclose(metrics["center_wavelength_mm"], 124.91352416666666)
    assert metrics["samples_per_wavelength"] > 37.0
    assert math.isclose(metrics["nominal_depth_window_mm"], 499.65409666666666)


def test_build_audit_blocks_3d_hpc_and_field_fwi():
    rows, summary = build_audit(_minimal_data(), _event_rows())
    rows_by_key = {row["audit_key"]: row for row in rows}

    assert summary["policy_label"] == "field_acquisition_readiness_2d_qc_not_hpc_fwi"
    assert summary["ready_for_2d_qc"] is True
    assert summary["ready_for_3d_hpc"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["field_hpc_priority"] == "none"
    assert rows_by_key["survey_dimensionality"]["status"] == "blocks_3d_hpc"
    assert rows_by_key["field_fwi_readiness"]["status"] == "blocked"
    assert rows_by_key["hpc_priority"]["status"] == "do_not_submit_field_hpc_job"
    assert math.isclose(summary["spatial_all_window_supported_fraction"], 0.281124)
    assert "3D or field-FWI workload" in summary["decision"]
