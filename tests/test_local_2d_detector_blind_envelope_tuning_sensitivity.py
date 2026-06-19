from run_local_2d_detector_blind_envelope_tuning_sensitivity import (
    feature_contrast_rows,
    knob_effect_rows,
    knob_value_rows,
    summarize_sensitivity,
    tuning_sensitive_case_labels,
)


def _selected_rows():
    rows = []
    for case_label, structural_results, support_results in [
        (
            "target2_close50_linear29p5|seed13|nominal",
            {0.0: [False, True], 0.4: [True, True]},
            {0.0: [True, True], 0.12: [False, True]},
        ),
        (
            "target2_close50_linear29p5|seed34|nominal",
            {0.0: [True, True], 0.4: [False, True]},
            {0.0: [False, True], 0.12: [True, True]},
        ),
    ]:
        seed = case_label.split("|")[1].replace("seed", "")
        for structural_weight, hits in structural_results.items():
            for idx, hit in enumerate(hits):
                rows.append(
                    {
                        "case_label": case_label,
                        "branch_key": "target2_close50_linear29p5",
                        "seed": seed,
                        "case_variant": "nominal",
                        "envelope_weight": "1.0",
                        "structural_weight": str(structural_weight),
                        "support_weight": "0.0",
                        "center_weight": "0.0",
                        "span_threshold_mm": "90.0",
                        "all_target_slots_hit": str(hit),
                        "selection_score": "0.2" if hit else "-0.2",
                        "support_score": "4.0" if hit else "1.0",
                        "active_structure_score": "1.0" if hit else "0.0",
                        "regular_structure_score": "1.0" if hit else "0.0",
                        "regular_center_score": "0.5" if hit else "0.0",
                        "selected_base_sum": "1.0" if hit else "0.5",
                        "edge_envelope_score": "0.0",
                        "pair_structure_score": "0.0",
                        "x_span_mm": "100",
                        "gap_left_mm": "50",
                        "gap_right_mm": "50",
                        "selected_x_values_mm": f"{idx},250,300",
                    }
                )
        for support_weight, hits in support_results.items():
            for idx, hit in enumerate(hits):
                rows.append(
                    {
                        "case_label": case_label,
                        "branch_key": "target2_close50_linear29p5",
                        "seed": seed,
                        "case_variant": "nominal",
                        "envelope_weight": "1.0",
                        "structural_weight": "0.0",
                        "support_weight": str(support_weight),
                        "center_weight": "0.0",
                        "span_threshold_mm": "90.0",
                        "all_target_slots_hit": str(hit),
                        "selection_score": "0.2" if hit else "-0.2",
                        "support_score": "4.0" if hit else "1.0",
                        "active_structure_score": "1.0" if hit else "0.0",
                        "regular_structure_score": "1.0" if hit else "0.0",
                        "regular_center_score": "0.5" if hit else "0.0",
                        "selected_base_sum": "1.0" if hit else "0.5",
                        "edge_envelope_score": "0.0",
                        "pair_structure_score": "0.0",
                        "x_span_mm": "100",
                        "gap_left_mm": "50",
                        "gap_right_mm": "50",
                        "selected_x_values_mm": f"{idx},250,300",
                    }
                )
    return rows


def test_tuning_sensitive_case_labels_use_success_fraction_threshold():
    cases = [
        {"case_label": "case_stable", "success_fraction": "1.0"},
        {"case_label": "case_sensitive", "success_fraction": "0.5"},
    ]

    assert tuning_sensitive_case_labels(cases) == ["case_sensitive"]


def test_knob_effect_rows_capture_best_weight_direction():
    selected = _selected_rows()
    case_labels = [
        "target2_close50_linear29p5|seed13|nominal",
        "target2_close50_linear29p5|seed34|nominal",
    ]
    value_rows = knob_value_rows(selected, case_labels)
    effect_rows = knob_effect_rows(value_rows)
    structural = {
        row["case_label"]: row
        for row in effect_rows
        if row["knob"] == "structural_weight"
    }
    support = {
        row["case_label"]: row
        for row in effect_rows
        if row["knob"] == "support_weight"
    }

    assert structural["target2_close50_linear29p5|seed13|nominal"]["best_value"] == 0.4
    assert structural["target2_close50_linear29p5|seed34|nominal"]["best_value"] == 0.0
    assert support["target2_close50_linear29p5|seed13|nominal"]["best_value"] == 0.0
    assert support["target2_close50_linear29p5|seed34|nominal"]["best_value"] == 0.12


def test_summary_marks_conflicting_tuning_boundary_no_fwi():
    selected = _selected_rows()
    case_rows = [
        {"case_label": "target2_close50_linear29p5|seed13|nominal"},
        {"case_label": "target2_close50_linear29p5|seed34|nominal"},
    ]
    case_labels = [row["case_label"] for row in case_rows]
    effect_rows = knob_effect_rows(knob_value_rows(selected, case_labels))
    feature_rows = feature_contrast_rows(selected, case_labels)
    failure_rows = [
        {"case_label": "target2_close50_linear29p5|seed13|nominal", "dominant_failure_count": 2},
        {"case_label": "target2_close50_linear29p5|seed34|nominal", "dominant_failure_count": 3},
    ]

    summary = summarize_sensitivity(
        case_rows,
        effect_rows,
        feature_rows,
        failure_rows,
        {"policy_label": "stability"},
    )

    assert summary["policy_label"] == "local_2d_detector_blind_envelope_tuning_sensitivity_cpu_no_fwi"
    assert summary["tuning_sensitive_case_count"] == 2
    assert summary["structural_weight_direction_conflict"] is True
    assert summary["support_weight_direction_conflict"] is True
    assert summary["ready_for_global_policy_tuning_fix"] is False
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
