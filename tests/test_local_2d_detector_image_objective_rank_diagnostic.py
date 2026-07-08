from run_local_2d_detector_image_objective_rank_diagnostic import (
    build_case_rank_rows,
    build_objective_rows,
    summarize_rank_diagnostic,
)


def scored_row(
    *,
    objective="obj_a",
    seed=13,
    run_name="run_a",
    score=1.0,
    all_truth=False,
    truth_hits=1,
):
    return {
        "objective_label": objective,
        "branch_key": "target2_close14",
        "seed": seed,
        "case_variant": "nominal",
        "run_name": run_name,
        "image_objective_score": score,
        "assigned_max_rank": 3,
        "assigned_rank_sum": 6,
        "unique_all_truths_within_tolerance": str(all_truth),
        "unique_truth_hit_count": truth_hits,
        "assigned_x_values_mm": "188,250,264",
        "assigned_detection_ranks": "1,2,3",
    }


def test_case_rank_rows_record_first_all_truth_rank_by_objective():
    rows = [
        scored_row(score=3.0, all_truth=False),
        scored_row(score=2.0, all_truth=True, truth_hits=3),
        scored_row(score=1.0, all_truth=False),
    ]

    case_rows = build_case_rank_rows(rows)

    assert len(case_rows) == 1
    assert case_rows[0]["first_all_truth_rank"] == 2.0
    assert case_rows[0]["first_truth_top1"] is False
    assert case_rows[0]["first_truth_top10"] is True


def test_objective_rows_select_best_rank_budget_coverage():
    rows = [
        scored_row(objective="obj_a", seed=13, run_name="run_a", score=3.0, all_truth=False),
        scored_row(objective="obj_a", seed=13, run_name="run_a", score=2.0, all_truth=True, truth_hits=3),
        scored_row(objective="obj_b", seed=13, run_name="run_a", score=3.0, all_truth=True, truth_hits=3),
        scored_row(objective="obj_b", seed=13, run_name="run_a", score=2.0, all_truth=False),
    ]
    case_rows = build_case_rank_rows(rows)

    objective_rows = build_objective_rows(case_rows)

    assert objective_rows[0]["objective_label"] == "obj_b"
    assert objective_rows[0]["top1_all_truth_case_count"] == 1
    assert objective_rows[0]["first_truth_top50_case_count"] == 1


def test_summary_keeps_image_objective_rank_diagnostic_no_fwi():
    objective_rows = [
        {
            "objective_label": "obj_a",
            "case_count": 2,
            "top1_all_truth_case_count": 0,
            "first_truth_top10_case_count": 0,
            "first_truth_top50_case_count": 0,
            "first_truth_top200_case_count": 1,
            "first_truth_top1000_case_count": 1,
            "median_first_all_truth_rank": 500.0,
            "max_first_all_truth_rank": 1200.0,
        }
    ]
    source_summary = {
        "policy_label": "source_policy",
        "scored_row_count": 42,
        "primary_objective_all_truth_case_count": 0,
        "oracle_all_truth_case_count": 1,
    }

    summary = summarize_rank_diagnostic([], objective_rows, source_summary)

    assert summary["policy_label"] == "local_2d_detector_image_objective_rank_diagnostic_cpu_no_fwi"
    assert summary["best_top50_all_truth_case_count"] == 0
    assert summary["best_top1000_all_truth_case_count"] == 1
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
