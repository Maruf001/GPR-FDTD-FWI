from run_local_2d_detector_branch_lock_counterfactual_synthesis import (
    build_synthesis,
    candidate_at_x_nearest_z,
)


def test_candidate_at_x_nearest_z_prefers_nearest_depth_then_misfit():
    rows = [
        {"x_mm": 250.0, "z_mm": 87.0, "misfit": 0.04},
        {"x_mm": 250.0, "z_mm": 89.0, "misfit": 0.07},
        {"x_mm": 250.0, "z_mm": 91.0, "misfit": 0.08},
        {"x_mm": 252.0, "z_mm": 89.0, "misfit": 0.06},
    ]

    selected = candidate_at_x_nearest_z(rows, 250.0, 90.0)

    assert selected["x_mm"] == 250.0
    assert selected["z_mm"] == 89.0


def test_branch_lock_synthesis_keeps_broad_gpu_and_fwi_blocked():
    greedy_summary = {
        "run_name": "greedy",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "final_state": {
            "x_values_mm": [191.0, 252.0, 266.0],
            "z_values_mm": [90.0, 89.0, 91.0],
        },
        "steps": [
            {
                "target_index": 1,
                "best_candidate": {
                    "misfit": 0.066,
                    "params": {"x_mm": 252.0, "z_mm": 89.0},
                },
            },
            {
                "target_index": 2,
                "best_candidate": {
                    "misfit": 0.066,
                    "params": {"x_mm": 266.0, "z_mm": 91.0},
                },
            },
        ],
    }
    counterfactual_summary = {
        "run_name": "counterfactual",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "final_state": {
            "x_values_mm": [191.0, 250.0, 264.0],
            "z_values_mm": [90.0, 89.0, 91.0],
        },
        "steps": [
            {
                "target_index": 2,
                "best_candidate": {
                    "misfit": 0.070,
                    "params": {"x_mm": 264.0, "z_mm": 91.0},
                },
            }
        ],
    }
    target1_rows = [
        {"x_mm": 252.0, "z_mm": 89.0, "misfit": 0.066},
        {"x_mm": 250.0, "z_mm": 89.0, "misfit": 0.072},
        {"x_mm": 250.0, "z_mm": 91.0, "misfit": 0.073},
    ]
    target2_rows = [
        {"x_mm": 266.0, "z_mm": 91.0, "misfit": 0.066},
        {"x_mm": 268.0, "z_mm": 91.0, "misfit": 0.075},
    ]

    rows, gates, summary = build_synthesis(
        greedy_summary,
        target1_rows,
        target2_rows,
        counterfactual_summary,
        abs_gap_cutoff=0.01,
        rel_gap_cutoff=0.10,
    )
    gate_lookup = {row["gate_key"]: row for row in gates}

    assert len(rows) == 4
    assert summary["target1_near_tie_retained_by_rule"] is True
    assert summary["target2_true_lateral_candidate_available_after_greedy_middle"] is False
    assert summary["target2_counterfactual_unlocked_true_lateral"] is True
    assert summary["counterfactual_linf_improvement_mm"] == 1.0
    assert summary["ready_for_branch_preserving_selector_design"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gate_lookup["broad_gpu_queue"]["ready"] is False
    assert gate_lookup["detector_seeded_fwi"]["ready"] is False
