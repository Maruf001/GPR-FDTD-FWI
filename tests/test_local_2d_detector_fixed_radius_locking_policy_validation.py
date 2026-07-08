from run_local_2d_detector_fixed_radius_locking_policy_validation import (
    build_validation_rows,
    final_linf_error,
    gate_rows,
    summarize_validation,
)


def _validation_summary():
    return {
        "run_name": "validation_probe",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "final_state": {
            "x_values_mm": [190.0, 250.0, 264.0],
            "z_values_mm": [90.0, 90.0, 90.0],
            "radii_mm": [5.0, 6.0, 8.0],
        },
        "confidence_rows": [
            {
                "target_rebar_index": 2,
                "candidate_count": 25,
                "best_x_mm": 264.0,
                "best_z_mm": 90.0,
                "best_radius_mm": 8.0,
                "best_misfit": 0.05850212279737268,
                "competing_geometry_x_mm": 265.0,
                "competing_geometry_z_mm": 90.0,
                "competing_geometry_radius_mm": 8.0,
                "competing_geometry_misfit": 0.05919824673075413,
                "ambiguity_candidate_count": 2,
            }
        ],
    }


def test_validation_rows_preserve_exact_but_ambiguous_target2_result():
    rows = build_validation_rows(_validation_summary())

    assert len(rows) == 1
    assert rows[0]["target_index"] == 2
    assert rows[0]["truth_selected"] is True
    assert rows[0]["truth_selected_but_ambiguous"] is True
    assert round(rows[0]["competing_minus_best_abs"], 6) == 0.000696


def test_validation_summary_allows_only_single_branch_mechanism_claim():
    validation_summary = _validation_summary()
    rows = build_validation_rows(validation_summary)
    summary = summarize_validation(
        {"policy_label": "design"},
        validation_summary,
        {
            "aborted": False,
            "max_gpu_util_percent": 88.0,
            "max_ram_used_percent": 14.7,
        },
        rows,
    )
    gates = {row["gate_key"]: row for row in gate_rows(summary)}
    _, _, linf = final_linf_error(validation_summary)

    assert linf == 0.0
    assert summary["exact_geometry_recovered"] is True
    assert summary["guard_within_caps"] is True
    assert summary["ready_for_locking_mechanism_claim"] is True
    assert summary["ready_for_general_detector_policy_claim"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert gates["locking_mechanism_claim"]["ready"] is True
    assert gates["general_detector_policy_claim"]["ready"] is False
