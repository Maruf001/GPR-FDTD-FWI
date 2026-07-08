from run_gssi_field_apparent_depth_sensitivity import (
    scenario_depth_rows,
    summarize_sensitivity,
)


def test_scenario_depth_rows_show_higher_epsr_compresses_depth_scale():
    scenarios = [
        {
            "scenario_key": "low_epsr",
            "source": "test",
            "file": "all",
            "epsr": 2.25,
            "time_zero_ns": 0.0,
            "tx_rx_offset_mm": "",
            "calibration_status": "test_only",
        },
        {
            "scenario_key": "high_epsr",
            "source": "test",
            "file": "all",
            "epsr": 9.0,
            "time_zero_ns": 0.0,
            "tx_rx_offset_mm": "",
            "calibration_status": "test_only",
        },
    ]
    cues = [
        {"time_ns": "1.0"},
        {"time_ns": "2.0"},
    ]
    applied = [
        {"abs_corrected_phase_residual_ns": "0.02"},
        {"abs_corrected_phase_residual_ns": "0.04"},
    ]

    rows = scenario_depth_rows(scenarios, cues, applied, conservative_half_width_ns=0.05)
    by_key = {row["scenario_key"]: row for row in rows}

    assert by_key["high_epsr"]["cue_depth_max_mm"] < by_key["low_epsr"]["cue_depth_max_mm"]
    assert by_key["low_epsr"]["corrected_residual_support_count"] == 2
    assert by_key["high_epsr"]["cover_depth_claim_ready"] is False


def test_summarize_sensitivity_keeps_cover_depth_blocked():
    rows = [
        {
            "epsr": 2.25,
            "cue_depth_max_mm": 200.0,
            "corrected_residual_support_count": 3,
            "corrected_residual_row_count": 3,
        },
        {
            "epsr": 9.0,
            "cue_depth_max_mm": 100.0,
            "corrected_residual_support_count": 3,
            "corrected_residual_row_count": 3,
        },
    ]

    summary = summarize_sensitivity(rows)

    assert summary["policy_label"] == "field_apparent_depth_sensitivity_not_calibrated_cover_depth"
    assert summary["scenario_count"] == 2
    assert summary["max_apparent_depth_sensitivity_factor"] == 2.0
    assert summary["all_residuals_within_budget_all_scenarios"] is True
    assert summary["cover_depth_claim_ready"] is False
    assert summary["field_fwi_ready"] is False
    assert summary["gpu_priority"] == "none"
