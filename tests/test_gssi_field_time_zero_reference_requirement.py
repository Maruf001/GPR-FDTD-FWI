import math

from run_gssi_field_time_zero_reference_requirement import (
    REFERENCE_UNCERTAINTY_GATE_NS,
    gate_rows,
    requirement_rows,
    summarize,
    timing_error_for_depth_mm,
    two_way_depth_error_mm,
    velocity_m_per_ns,
)


def test_two_way_depth_error_round_trips_for_epsr_2p25():
    epsr = 2.25
    velocity = velocity_m_per_ns(epsr)
    dt_ns = timing_error_for_depth_mm(2.0, epsr)

    assert math.isclose(velocity, 0.19986163866666667)
    assert math.isclose(dt_ns, REFERENCE_UNCERTAINTY_GATE_NS, rel_tol=1.0e-3)
    assert math.isclose(two_way_depth_error_mm(dt_ns, epsr), 2.0, rel_tol=1.0e-9)


def test_requirement_rows_include_reference_gate_and_negative_control():
    uncertainty = {
        "max_abs_content_anchor_residual_ns": 0.00982318271119842,
        "bootstrap_ci_width_ns": 0.03929273084479362,
        "conservative_half_width_ns": 0.058939096267190516,
    }
    control_gap = {
        "short_vs_early_delta_ns": 0.12770137524557956,
    }
    rows = requirement_rows(uncertainty, control_gap, 2.25)
    by_key = {row["requirement_key"]: row for row in rows}

    assert by_key["content_anchor_residual"]["ready"] is True
    assert by_key["short_vs_early_conflict"]["ready"] is False
    assert by_key["packet_reference_uncertainty_gate"]["dt_ns"] == REFERENCE_UNCERTAINTY_GATE_NS
    assert by_key["packet_reference_uncertainty_gate"]["depth_error_mm"] < by_key["conservative_half_width"]["depth_error_mm"]
    assert by_key["depth_error_5mm_equivalent"]["dt_ns"] > REFERENCE_UNCERTAINTY_GATE_NS


def test_gate_summary_blocks_current_archive_without_reference_rows():
    rows = requirement_rows(
        {
            "max_abs_content_anchor_residual_ns": 0.01,
            "bootstrap_ci_width_ns": 0.04,
            "conservative_half_width_ns": 0.06,
        },
        {"short_vs_early_delta_ns": 0.12},
        2.25,
    )
    acceptance_rows = [
        {
            "gate_key": "absolute_time_zero_references",
            "ready": False,
            "evidence": "time_zero_reference_count=0",
        }
    ]
    gates = gate_rows(rows, acceptance_rows)
    summary = summarize(rows, gates, 2.25, {"blocking_finding_count": 67})
    by_gate = {row["gate_key"]: row for row in gates}

    assert by_gate["external_reference_requirement_defined"]["ready"] is True
    assert by_gate["current_archive_absolute_time_zero"]["ready"] is False
    assert summary["ready_for_reference_collection"] is True
    assert summary["ready_for_current_archive_absolute_time_zero"] is False
    assert summary["ready_for_current_archive_field_fwi"] is False
    assert summary["gpu_priority"] == "none"
