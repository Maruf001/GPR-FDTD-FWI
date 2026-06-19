from run_local_2d_detector_fixed_radius_residual_ambiguity_audit import (
    audit_step,
    gate_rows,
    summarize,
)


def _step(target_index):
    return {
        "target_index": target_index,
        "candidate_csv": f"step_{target_index}.csv",
    }


def _row(x_mm, z_mm, radius_mm, misfit, target_index):
    return {
        "case_label": "nominal",
        "misfit": misfit,
        "target_index": target_index,
        "x_mm": x_mm,
        "z_mm": z_mm,
        "radius_mm": radius_mm,
    }


def test_audit_step_flags_truth_selected_but_ambiguous():
    row = audit_step(
        step=_step(0),
        candidates=[
            _row(190.0, 90.0, 5.0, 0.10, 0),
            _row(191.0, 90.0, 5.0, 0.101, 0),
        ],
        confidence={"ambiguity_candidate_count": 2, "ambiguity_misfit_threshold": 0.1015},
        true_x=[190.0, 250.0, 264.0],
        true_z=[90.0, 90.0, 90.0],
        true_radii=[5.0, 6.0, 8.0],
        final_x=[190.0, 251.0, 265.0],
        final_z=[90.0, 89.0, 91.0],
    )

    assert row["selected_is_truth_coordinate"] is True
    assert row["truth_candidate_present"] is True
    assert row["residual_mode"] == "truth_selected_but_ambiguous"


def test_audit_step_flags_truth_present_but_neighbor_preferred():
    row = audit_step(
        step=_step(1),
        candidates=[
            _row(251.0, 89.0, 6.0, 0.062, 1),
            _row(250.0, 90.0, 6.0, 0.065, 1),
            _row(251.0, 90.0, 6.0, 0.066, 1),
        ],
        confidence={"ambiguity_candidate_count": 1, "ambiguity_misfit_threshold": 0.063},
        true_x=[190.0, 250.0, 264.0],
        true_z=[90.0, 90.0, 90.0],
        true_radii=[5.0, 6.0, 8.0],
        final_x=[190.0, 251.0, 265.0],
        final_z=[90.0, 89.0, 91.0],
    )

    assert row["selected_is_truth_coordinate"] is False
    assert row["truth_candidate_present"] is True
    assert row["truth_candidate_rank"] == 2
    assert round(row["truth_minus_best_misfit_abs"], 6) == 0.003
    assert row["residual_mode"] == "truth_present_but_objective_prefers_neighbor"


def test_audit_step_flags_truth_absent_after_nonoverlap_filter():
    row = audit_step(
        step=_step(2),
        candidates=[
            _row(265.0, 90.0, 8.0, 0.062, 2),
            _row(265.0, 91.0, 8.0, 0.061, 2),
            _row(266.0, 91.0, 8.0, 0.063, 2),
        ],
        confidence={"ambiguity_candidate_count": 1, "ambiguity_misfit_threshold": 0.062},
        true_x=[190.0, 250.0, 264.0],
        true_z=[90.0, 90.0, 90.0],
        true_radii=[5.0, 6.0, 8.0],
        final_x=[190.0, 251.0, 265.0],
        final_z=[90.0, 89.0, 91.0],
    )

    assert row["truth_candidate_present"] is False
    assert row["candidate_shortfall_from_25"] == 22
    assert row["residual_mode"] == "truth_candidate_absent_after_nonoverlap_filter"


def test_summary_blocks_more_gpu_after_residual_cause_audit():
    rows = [
        {
            "target_index": 0,
            "selected_is_truth_coordinate": True,
            "truth_candidate_present": True,
            "residual_mode": "truth_selected_but_ambiguous",
            "truth_minus_best_misfit_abs": 0.0,
        },
        {
            "target_index": 1,
            "selected_is_truth_coordinate": False,
            "truth_candidate_present": True,
            "residual_mode": "truth_present_but_objective_prefers_neighbor",
            "truth_minus_best_misfit_abs": 0.003,
        },
        {
            "target_index": 2,
            "selected_is_truth_coordinate": False,
            "truth_candidate_present": False,
            "residual_mode": "truth_candidate_absent_after_nonoverlap_filter",
            "truth_minus_best_misfit_abs": None,
        },
    ]
    summary = summarize(
        {
            "run_name": "pilot",
            "true_x_values_mm": [190.0, 250.0, 264.0],
            "true_z_values_mm": [90.0, 90.0, 90.0],
            "final_state": {
                "x_values_mm": [190.0, 251.0, 265.0],
                "z_values_mm": [90.0, 89.0, 91.0],
            },
        },
        {"policy_label": "selector"},
        rows,
        {"aborted": False, "max_gpu_util_percent": 88.0, "max_ram_used_percent": 15.0},
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["final_linf_error_mm"] == 1.0
    assert summary["truth_selected_but_ambiguous_count"] == 1
    assert summary["truth_present_but_objective_prefers_neighbor_count"] == 1
    assert summary["truth_absent_after_nonoverlap_filter_count"] == 1
    assert summary["ready_for_immediate_gpu_iteration"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert gates["residual_cause_identified"]["ready"] is True
    assert gates["immediate_gpu_iteration"]["ready"] is False
