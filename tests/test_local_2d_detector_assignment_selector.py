from run_local_2d_detector_assignment_selector import (
    cross_validate,
    enrich_row,
    select_rows_for_selector,
    selector_score,
    summarize_selected,
)


def _row(case, label, xs, ranks, hits, policy="top20_minx8", config="cfg"):
    return enrich_row({
        "branch_key": case[0],
        "seed": str(case[1]),
        "case_variant": case[2],
        "run_name": f"{case[0]}_{case[1]}_{case[2]}",
        "config_key": config,
        "assignment_policy_key": policy,
        "assignment_status": "assigned",
        "assigned_candidate_count": "3",
        "assigned_x_values_mm": ",".join(str(x) for x in xs),
        "assigned_z_values_mm": "90,90,90",
        "assigned_detection_ranks": ",".join(str(rank) for rank in ranks),
        "candidate_budget": policy.split("_")[0].replace("top", ""),
        "top_k": "20",
        "unique_truth_hit_count": str(sum(hits)),
        "unique_all_truths_within_tolerance": all(hits),
        "unique_target0_hit": hits[0],
        "unique_target1_hit": hits[1],
        "unique_target2_hit": hits[2],
    })


def _selector(label, span_target=None, span_width_bonus=0.0):
    return {
        "selector_label": label,
        "rank_sum_weight": 0.2,
        "max_rank_weight": 0.4,
        "span_width_bonus": span_width_bonus,
        "span_target_mm": span_target,
        "span_target_weight": 2.0 if span_target is not None else 0.0,
        "center_target_mm": 250.0,
        "center_weight": 0.0,
        "gap_imbalance_weight": 0.0,
        "z_std_weight": 0.0,
        "budget_penalty": 0.0,
    }


def test_selector_score_can_prefer_target_span_over_lower_rank():
    target_selector = _selector("span80", span_target=80.0)
    low_rank_wrong_span = _row(("close14", 13, "nominal"), "a", [240, 250, 260], [1, 2, 3], (False, True, False))
    higher_rank_right_span = _row(("close14", 13, "nominal"), "b", [190, 250, 270], [4, 5, 6], (True, True, True))

    assert selector_score(higher_rank_right_span, target_selector) > selector_score(low_rank_wrong_span, target_selector)


def test_select_rows_and_summary_count_truth_hits():
    selector = _selector("wide", span_width_bonus=1.0)
    rows = [
        _row(("close14", 13, "nominal"), "narrow", [245, 250, 260], [1, 2, 3], (False, True, False)),
        _row(("close14", 13, "nominal"), "wide", [190, 250, 270], [4, 5, 6], (True, True, True)),
        _row(("close14", 21, "nominal"), "wide", [190, 250, 270], [4, 5, 6], (False, True, True)),
    ]

    selected = select_rows_for_selector(rows, selector)
    summary = summarize_selected(selector, selected)

    assert len(selected) == 2
    assert selected[0]["unique_all_truths_bool"] is True
    assert summary["all_truth_case_count"] == 1
    assert summary["target1_hit_count"] == 2


def test_cross_validation_trains_selector_on_non_holdout_cases():
    selectors = [_selector("narrow", span_target=10.0), _selector("wide", span_width_bonus=1.0)]
    rows = [
        _row(("close14", 13, "nominal"), "narrow", [245, 250, 260], [1, 2, 3], (False, True, False)),
        _row(("close14", 13, "nominal"), "wide", [190, 250, 270], [4, 5, 6], (True, True, True)),
        _row(("close14", 21, "nominal"), "narrow", [245, 250, 260], [1, 2, 3], (False, True, False)),
        _row(("close14", 21, "nominal"), "wide", [190, 250, 270], [4, 5, 6], (True, True, True)),
    ]
    selected_by_selector = {
        selector["selector_label"]: select_rows_for_selector(rows, selector)
        for selector in selectors
    }
    summaries = {
        selector["selector_label"]: summarize_selected(selector, selected_by_selector[selector["selector_label"]])
        for selector in selectors
    }

    summary, cv_rows = cross_validate(summaries, selected_by_selector, "leave_one_case")

    assert summary["case_count"] == 2
    assert summary["all_truth_case_count"] == 2
    assert {row["trained_selector_label"] for row in cv_rows} == {"wide"}
