from run_local_2d_detector_component_selector_audit import (
    cross_validate,
    enrich_row,
    select_rows_for_selector,
    selector_score,
    summarize_audit,
    summarize_selected,
)


def _row(case, xs, ranks, hits, balanced="1.0", minimum="0.2"):
    return enrich_row(
        {
            "branch_key": case[0],
            "seed": str(case[1]),
            "case_variant": case[2],
            "run_name": f"{case[0]}_{case[1]}_{case[2]}",
            "candidate_x_values_mm": ",".join(str(x) for x in xs),
            "candidate_z_values_mm": "90,90,90",
            "candidate_ranks": ",".join(str(rank) for rank in ranks),
            "x_span_mm": str(max(xs) - min(xs)),
            "gap_balance_mm": "0",
            "score_component_balanced": balanced,
            "score_component_min": minimum,
            "score_hybrid_span_component": balanced,
            "score_span_bonus": balanced,
            "unique_truth_hit_count": str(sum(hits)),
            "unique_all_truths_within_tolerance": str(all(hits)),
            "unique_target0_hit": str(hits[0]),
            "unique_target1_hit": str(hits[1]),
            "unique_target2_hit": str(hits[2]),
        }
    )


def _selector(label="selector", span_target=80.0):
    return {
        "selector_label": label,
        "component_balanced_weight": 1.0,
        "component_min_weight": 0.0,
        "hybrid_span_component_weight": 0.0,
        "span_bonus_weight": 0.0,
        "span_width_weight": 0.0,
        "span_target_mm": span_target,
        "span_target_weight": 1.0,
        "gap_balance_weight": 0.0,
        "rank_sum_weight": 0.0,
        "max_rank_weight": 0.0,
        "center_weight": 0.0,
    }


def test_selector_score_prefers_matching_span_when_component_scores_tie():
    selector = _selector(span_target=80.0)
    matching = _row(("branch", 13, "nominal"), [190, 250, 270], [3, 4, 5], (True, True, True))
    narrow = _row(("branch", 13, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False))

    assert selector_score(matching, selector) > selector_score(narrow, selector)


def test_select_rows_and_summary_count_top1_truth():
    selector = _selector(span_target=80.0)
    rows = [
        _row(("branch", 13, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False)),
        _row(("branch", 13, "nominal"), [190, 250, 270], [3, 4, 5], (True, True, True)),
        _row(("branch", 21, "nominal"), [190, 250, 270], [3, 4, 5], (False, True, True)),
    ]

    selected = select_rows_for_selector(rows, selector)
    summary = summarize_selected(selector, selected)

    assert len(selected) == 2
    assert selected[0]["unique_all_truths_bool"] is True
    assert summary["all_truth_case_count"] == 1
    assert summary["target1_hit_count"] == 2


def test_cross_validate_and_audit_summary_keep_fwi_blocked():
    selectors = [_selector("wide", span_target=80.0), _selector("narrow", span_target=20.0)]
    rows = [
        _row(("branch", 13, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False)),
        _row(("branch", 13, "nominal"), [190, 250, 270], [3, 4, 5], (True, True, True)),
        _row(("branch", 21, "nominal"), [240, 250, 260], [1, 2, 3], (False, True, False)),
        _row(("branch", 21, "nominal"), [190, 250, 270], [3, 4, 5], (True, True, True)),
    ]
    selectors_by_label = {selector["selector_label"]: selector for selector in selectors}
    selected_by_selector = {
        selector["selector_label"]: select_rows_for_selector(rows, selector)
        for selector in selectors
    }
    selector_rows = [
        summarize_selected(selector, selected_by_selector[selector["selector_label"]])
        for selector in selectors
    ]
    selector_rows = sorted(selector_rows, key=lambda row: row["selector_label"], reverse=True)
    cv_summary, cv_rows = cross_validate(selectors_by_label, selected_by_selector, "leave_one_case")

    summary = summarize_audit(
        rows,
        selector_rows,
        selected_by_selector["wide"],
        [cv_summary, {"cv_strategy": "leave_one_seed", "all_truth_case_count": 2}, {"cv_strategy": "leave_one_branch", "all_truth_case_count": 2}],
        {"best_top1_all_truth_case_count": 0, "best_top50_case_count": 10},
    )

    assert cv_summary["all_truth_case_count"] == 2
    assert {row["trained_selector_label"] for row in cv_rows} == {"wide"}
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
