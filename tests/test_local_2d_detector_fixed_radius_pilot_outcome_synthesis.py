from run_local_2d_detector_fixed_radius_pilot_outcome_synthesis import (
    build_candidate_coverage_rows,
    build_pilot_rows,
    build_selector_rows,
    gate_rows,
    guarded_command_text,
    summarize,
)


def _preflight_rows():
    return [
        {
            "case_label": "target2_close14|seed21|source_mismatch",
            "branch_key": "target2_close14",
            "seed": "21",
            "case_variant": "source_mismatch",
            "x_seed_values_mm": "190,248,263",
            "z_seed_values_mm": "95,86,81",
            "min_pair_clearance_mm": "1.8",
            "direct_fixed_radius_pilot_ready": "True",
        },
        {
            "case_label": "target2_close14|seed21|nominal",
            "branch_key": "target2_close14",
            "seed": "21",
            "case_variant": "nominal",
            "x_seed_values_mm": "191,254,266",
            "z_seed_values_mm": "86,91,91",
            "min_pair_clearance_mm": "-2.0",
            "direct_fixed_radius_pilot_ready": "False",
        },
        {
            "case_label": "target2_close14|seed13|nominal",
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "x_seed_values_mm": "185,250,265",
            "z_seed_values_mm": "97,81,85",
            "min_pair_clearance_mm": "1.5",
            "direct_fixed_radius_pilot_ready": "True",
        },
    ]


def _repair_rows():
    return [
        {
            "case_label": "target2_close14|seed21|nominal",
            "branch_key": "target2_close14",
            "seed": "21",
            "case_variant": "nominal",
            "repaired_x_values_mm": "191,252,266",
            "repaired_z_values_mm": "86,91,91",
            "min_pair_clearance_after_repair_mm": "0.0",
            "ready_for_repaired_fixed_radius_pilot": "True",
        }
    ]


def _summary(run_name, update_label, initial_x, initial_z, final_x, final_z):
    return {
        "run_name": run_name,
        "backend": "gpu-cpml",
        "sources": 5,
        "tx_rx_offset_mm": 45.0,
        "receiver_sampling": "nearest",
        "frequency_ghz": 1.5,
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "initial_state": {
            "x_values_mm": initial_x,
            "z_values_mm": initial_z,
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "final_state": {
            "x_values_mm": final_x,
            "z_values_mm": final_z,
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "update_case_label": update_label,
        "replication_cases": [
            {
                "label": update_label,
                "noise_seed": 21,
            }
        ],
        "confidence_rows": [
            {"candidate_count": 25, "confidence_label": "missing"},
            {"candidate_count": 15, "confidence_label": "missing"},
            {"candidate_count": 15, "confidence_label": "missing"},
        ],
        "elapsed_time_s": 321.0,
    }


def _pilot_summaries():
    return [
        _summary(
            "local2d_controlled_fixed_radius_seed_refine_target2_close14_seed21_source_mismatch_gpu",
            "source_mismatch",
            [190.0, 248.0, 263.0],
            [95.0, 86.0, 81.0],
            [190.0, 250.0, 265.0],
            [91.0, 90.0, 85.0],
        ),
        _summary(
            "local2d_repaired_exact_radius_seed_refine_target2_close14_seed21_nominal_gpu",
            "nominal",
            [191.0, 252.0, 266.0],
            [86.0, 91.0, 91.0],
            [191.0, 252.0, 266.0],
            [90.0, 89.0, 91.0],
        ),
    ]


def _pilot_summaries_post_second_pass():
    rows = list(_pilot_summaries())
    rows.append(
        _summary(
            "local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu",
            "nominal",
            [191.0, 252.0, 266.0],
            [90.0, 89.0, 91.0],
            [190.0, 251.0, 265.0],
            [90.0, 89.0, 91.0],
        )
    )
    return rows


def test_pilot_rows_match_direct_and_repaired_seed_sources_and_compute_residuals():
    rows = build_pilot_rows(_pilot_summaries(), _preflight_rows(), _repair_rows())
    by_case = {row["case_label"]: row for row in rows}

    direct = by_case["target2_close14|seed21|source_mismatch"]
    assert direct["seed_source_kind"] == "direct_preflight_seed"
    assert direct["initial_linf_mm"] == 9.0
    assert direct["final_linf_mm"] == 5.0
    assert direct["outcome_label"] == "improved_not_close"

    repaired = by_case["target2_close14|seed21|nominal"]
    assert repaired["seed_source_kind"] == "repaired_seed"
    assert repaired["initial_linf_mm"] == 4.0
    assert repaired["final_linf_mm"] == 2.0
    assert repaired["final_x_linf_mm"] == 2.0
    assert repaired["final_z_linf_mm"] == 1.0
    assert repaired["recommended_followup"] == "single_guarded_second_pass_probe"
    assert repaired["radius_confidence_missing_count"] == 3


def test_candidate_coverage_keeps_untested_cases_as_backlog_not_queue():
    pilot_rows = build_pilot_rows(_pilot_summaries(), _preflight_rows(), _repair_rows())
    coverage = build_candidate_coverage_rows(_preflight_rows(), _repair_rows(), pilot_rows)
    by_case = {row["case_label"]: row for row in coverage}

    assert by_case["target2_close14|seed21|source_mismatch"]["coverage_status"] == "tested"
    assert by_case["target2_close14|seed21|nominal"]["coverage_status"] == "tested"
    assert by_case["target2_close14|seed13|nominal"]["coverage_status"] == "untested_direct_ready"
    assert by_case["target2_close14|seed13|nominal"]["eligible_for_one_case_backlog"] is True
    assert by_case["target2_close14|seed13|nominal"]["ready_for_broad_gpu_queue"] is False


def test_summary_selects_one_guarded_second_pass_and_blocks_fwi_and_broad_gpu():
    pilot_rows = build_pilot_rows(_pilot_summaries(), _preflight_rows(), _repair_rows())
    coverage = build_candidate_coverage_rows(_preflight_rows(), _repair_rows(), pilot_rows)
    selector = build_selector_rows(pilot_rows, coverage)
    summary = summarize(
        {"policy_label": "preflight", "stable_seed_case_count": 3, "direct_fixed_radius_pilot_ready_count": 2},
        {"policy_label": "repair", "repair_found_count": 1},
        pilot_rows,
        coverage,
        selector,
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}
    ready = [row for row in selector if row["ready_now"]]

    assert len(ready) == 1
    assert ready[0]["action_key"] == "single_guarded_second_pass_probe"
    assert ready[0]["case_label"] == "target2_close14|seed21|nominal"
    assert ready[0]["initial_x_values_mm"] == "191,252,266"
    assert ready[0]["initial_z_values_mm"] == "90,89,91"
    assert summary["ready_for_single_guarded_second_pass_probe"] is True
    assert summary["ready_for_fresh_one_case_probe_now"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gates["single_guarded_second_pass_probe"]["ready"] is True
    assert gates["broad_gpu_queue"]["ready"] is False


def test_within_one_mm_second_pass_result_stops_immediate_gpu_iteration():
    pilot_rows = build_pilot_rows(_pilot_summaries_post_second_pass(), _preflight_rows(), _repair_rows())
    coverage = build_candidate_coverage_rows(_preflight_rows(), _repair_rows(), pilot_rows)
    selector = build_selector_rows(pilot_rows, coverage)
    summary = summarize(
        {"policy_label": "preflight", "stable_seed_case_count": 3, "direct_fixed_radius_pilot_ready_count": 2},
        {"policy_label": "repair", "repair_found_count": 1},
        pilot_rows,
        coverage,
        selector,
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["within_one_mm_residual_pilot_count"] == 1
    assert summary["best_pilot_run_name"] == "local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu"
    assert summary["best_final_linf_mm"] == 1.0
    assert summary["ready_for_single_guarded_second_pass_probe"] is False
    assert summary["gpu_priority"] == "none"
    assert not [row for row in selector if row["ready_now"]]
    assert gates["single_guarded_second_pass_probe"]["ready"] is False


def test_guarded_command_preserves_resource_caps():
    selector = build_selector_rows(
        build_pilot_rows(_pilot_summaries(), _preflight_rows(), _repair_rows()),
        build_candidate_coverage_rows(
            _preflight_rows(),
            _repair_rows(),
            build_pilot_rows(_pilot_summaries(), _preflight_rows(), _repair_rows()),
        ),
    )
    command = guarded_command_text(next(row for row in selector if row["ready_now"]))

    assert "--max-ram-percent 80" in command
    assert "--max-gpu-util-percent 90" in command
    assert "--initial-x-values-mm 191,252,266" in command
    assert "--initial-z-values-mm 90,89,91" in command
    assert "--x-offsets-mm=-2,-1,0,1,2" in command
