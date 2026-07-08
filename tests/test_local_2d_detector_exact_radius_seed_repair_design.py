from run_local_2d_detector_exact_radius_seed_repair_design import (
    build_repair_rows,
    find_repair_candidate,
    gate_rows,
    summarize_repairs,
)


def test_find_repair_candidate_makes_overlap_nonoverlapping():
    repair = find_repair_candidate(
        [190.0, 254.0, 266.0],
        [90.0, 90.0, 90.0],
        [5.0, 6.0, 8.0],
        [-2.0, 0.0, 2.0],
    )

    assert repair
    assert repair["min_pair_clearance_after_repair_mm"] >= 0.0
    assert repair["max_component_shift_mm"] == 2.0
    assert repair["shifted_component_count"] == 1


def test_repair_summary_keeps_gpu_and_fwi_blocked():
    case_rows = [
        {
            "case_label": "overlap",
            "branch_key": "target2_close14",
            "seed": 21,
            "case_variant": "nominal",
            "x_seed_values_mm": "190,254,266",
            "z_seed_values_mm": "90,90,90",
            "exact_radius_values_mm": "5,6,8",
            "min_pair_clearance_mm": -2.0,
            "overlapping_pair_count": 1,
            "overlapping_pair_keys": "1-2",
            "repair_required_mm": 2.0,
        }
    ]

    repair_rows = build_repair_rows(case_rows, [-2.0, 0.0, 2.0])
    summary = summarize_repairs(repair_rows, {"policy_label": "preflight"})
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert repair_rows[0]["repair_found"] is True
    assert repair_rows[0]["ready_for_repaired_fixed_radius_pilot"] is True
    assert summary["repair_found_count"] == 1
    assert summary["all_overlap_blocked_cases_repairable"] is True
    assert summary["ready_for_repaired_fixed_radius_pilot_subset"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gates["broad_gpu_queue"]["ready"] is False
