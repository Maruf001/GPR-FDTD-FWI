from run_local_2d_detector_exact_radius_seed_nonoverlap_preflight import (
    build_preflight_rows,
    gate_rows,
    pair_clearance_rows,
    summarize_preflight,
)


def _seed_rows(case_label, x_values, z_values, branch="target2_close14"):
    rows = []
    for idx, (x_mm, z_mm) in enumerate(zip(x_values, z_values)):
        rows.append(
            {
                "case_label": case_label,
                "branch_key": branch,
                "seed": 21,
                "case_variant": "nominal",
                "component_index": idx,
                "x_seed_mm": x_mm,
                "z_seed_mm": z_mm,
                "coordinate_seed_ready": True,
            }
        )
    return rows


def _prior(case_label):
    return {
        "case_label": case_label,
        "truth_radius_pattern_key": "5,6,8",
    }


def test_pair_clearance_rows_flag_exact_radius_overlap():
    rows = pair_clearance_rows(
        "case",
        [190.0, 254.0, 266.0],
        [90.0, 90.0, 90.0],
        [5.0, 6.0, 8.0],
    )
    by_pair = {row["pair_key"]: row for row in rows}

    assert by_pair["1-2"]["clearance_mm"] == -2.0
    assert by_pair["1-2"]["overlaps_under_exact_radii"] is True
    assert by_pair["0-1"]["overlaps_under_exact_radii"] is False


def test_build_preflight_rows_separates_direct_and_repair_cases():
    seed_rows = (
        _seed_rows("ready", [190.0, 250.0, 264.0], [90.0, 90.0, 90.0])
        + _seed_rows("overlap", [190.0, 254.0, 266.0], [90.0, 90.0, 90.0])
    )
    prior_rows = [_prior("ready"), _prior("overlap")]

    case_rows, pair_rows = build_preflight_rows(seed_rows, prior_rows, repair_step_mm=2.0)
    by_case = {row["case_label"]: row for row in case_rows}
    summary = summarize_preflight(
        case_rows,
        pair_rows,
        {"policy_label": "seed_export"},
        {"policy_label": "prior"},
        repair_step_mm=2.0,
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert by_case["ready"]["direct_fixed_radius_pilot_ready"] is True
    assert by_case["ready"]["min_pair_clearance_mm"] == 0.0
    assert by_case["overlap"]["direct_fixed_radius_pilot_ready"] is False
    assert by_case["overlap"]["overlapping_pair_keys"] == "1-2"
    assert by_case["overlap"]["repair_required_mm"] == 2.0
    assert by_case["overlap"]["repair_within_default_step"] is True
    assert summary["direct_fixed_radius_pilot_ready_count"] == 1
    assert summary["overlap_blocked_case_count"] == 1
    assert summary["repair_within_default_step_count"] == 1
    assert summary["ready_for_direct_fixed_radius_pilot_subset"] is True
    assert summary["ready_for_seed_repair_audit"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert gates["seed_repair_audit"]["ready"] is True
