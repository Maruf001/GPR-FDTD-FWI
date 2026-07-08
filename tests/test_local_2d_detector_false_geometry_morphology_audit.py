import pytest

from run_local_2d_detector_false_geometry_morphology_audit import (
    assignment_errors,
    build_morphology_rows,
    false_geometry_mode,
    representative_truth_x_by_case,
    summarize_audit,
    summarize_by_branch,
)


def component_row(case="case_a", xs="150,250,264", all_truth=True):
    return {
        "case_label": case,
        "branch_key": "target2_close14",
        "seed": "13",
        "case_variant": "nominal",
        "candidate_x_values_mm": xs,
        "unique_all_truths_within_tolerance": str(all_truth),
    }


def gap_row(
    case="case_a",
    selected_xs="221,261,273",
    missing="target0,target1",
    rank=50,
):
    return {
        "case_label": case,
        "branch_key": "target2_close14",
        "seed": "13",
        "case_variant": "nominal",
        "run_name": f"{case}_run",
        "selected_first_all_truth_rank": str(rank),
        "selected_rank_gate_label": "top50",
        "selected_best_false_minus_truth_score_gap": "0.07",
        "selected_positive_false_truth_gap": "True",
        "selected_top_unique_truth_hit_count": "1",
        "selected_top_missing_targets": missing,
        "selected_top_candidate_x_values_mm": selected_xs,
    }


def test_representative_truth_x_uses_median_all_truth_candidates():
    rows = [
        component_row(xs="150,250,264"),
        component_row(xs="152,250,266"),
        component_row(xs="221,250,264", all_truth=False),
    ]

    truth = representative_truth_x_by_case(rows)

    assert truth["case_a"] == [151.0, 250.0, 265.0]


def test_assignment_errors_match_selected_to_truth_by_minimum_sum():
    errors = assignment_errors([261.0, 221.0, 273.0], [151.0, 250.0, 265.0])

    assert errors == pytest.approx([70.0, 11.0, 8.0])


def test_false_geometry_mode_names_target_subset():
    assert false_geometry_mode(["target0", "target1"]) == "single_truth_only_target2"
    assert false_geometry_mode(["target2"]) == "two_truth_partial_missing_target2"
    assert false_geometry_mode(["target0", "target1", "target2"]) == "all_targets_missed"
    assert false_geometry_mode([]) == "all_truth_or_duplicate"


def test_build_morphology_rows_quantifies_compressed_top_false_geometry():
    rows = build_morphology_rows([gap_row()], [component_row(xs="150,250,264"), component_row(xs="152,250,266")])

    assert len(rows) == 1
    assert rows[0]["representative_truth_x_values_mm"] == "151,250,265"
    assert rows[0]["selected_top_x_span_mm"] == pytest.approx(52.0)
    assert rows[0]["representative_truth_x_span_mm"] == pytest.approx(114.0)
    assert rows[0]["selected_to_truth_x_span_ratio"] == pytest.approx(52.0 / 114.0)
    assert rows[0]["compressed_span_under_75pct_truth"] is True
    assert rows[0]["false_geometry_mode"] == "single_truth_only_target2"


def test_summary_keeps_detector_seeded_fwi_blocked():
    morphology = build_morphology_rows(
        [gap_row(), gap_row(case="case_b", selected_xs="150,250,270", missing="target2", rank=12)],
        [component_row(), component_row(case="case_b", xs="150,250,300")],
    )
    branches = summarize_by_branch(morphology)
    summary = summarize_audit(morphology, branches, {"policy_label": "gap", "selected_top200_case_count": 2})

    assert summary["case_count"] == 2
    assert summary["top200_all_truth_case_count"] == 2
    assert summary["positive_false_truth_gap_case_count"] == 2
    assert summary["compressed_span_case_count"] >= 1
    assert summary["ready_for_rank_gated_selector_claim"] is True
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
