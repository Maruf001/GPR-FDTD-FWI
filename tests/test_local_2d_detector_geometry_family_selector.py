from run_local_2d_detector_geometry_family_selector import (
    enrich_row,
    geometry_features,
    precompute_selected_indices,
    selected_rows_for_selector_index,
    selector_grid,
    summarize_audit,
    summarize_selected,
)


def detector_row(
    *,
    branch_key="target2_close14",
    seed=13,
    case_variant="nominal",
    run_name="run_a",
    xs="188,250,264",
    ranks="9,3,2",
    all_truth=True,
    truth_hits=3,
    target0=True,
    target1=True,
    target2=True,
    component_balanced=1.4,
    hybrid=3.2,
    component_min=0.23,
):
    return {
        "branch_key": branch_key,
        "seed": seed,
        "case_variant": case_variant,
        "run_name": run_name,
        "candidate_x_values_mm": xs,
        "candidate_ranks": ranks,
        "unique_all_truths_within_tolerance": str(all_truth),
        "unique_truth_hit_count": truth_hits,
        "unique_target0_hit": str(target0),
        "unique_target1_hit": str(target1),
        "unique_target2_hit": str(target2),
        "score_component_balanced": component_balanced,
        "score_hybrid_span_component": hybrid,
        "score_component_min": component_min,
    }


def test_geometry_features_encode_right_close_pair_signed_gap():
    features = geometry_features(detector_row(xs="190,250,264"))

    assert features["geometry_family_label"] == "right_close_pair"
    assert features["x_span_mm_numeric"] == 74.0
    assert features["signed_gap_mm"] == -46.0
    assert features["span_prior_score"] == 0.0
    assert features["signed_gap_prior_score"] == -0.01


def test_selector_grid_contains_geometry_family_weights():
    selectors = selector_grid()

    assert len(selectors) == 2160
    assert any(selector["signed_gap_prior_weight"] == 4.0 for selector in selectors)
    assert any("sgap4" in selector["selector_label"] for selector in selectors)


def test_geometry_family_selector_can_prefer_imbalanced_close_pair():
    rows = [
        enrich_row(
            detector_row(
                xs="185,221,265",
                ranks="13,7,1",
                all_truth=False,
                truth_hits=2,
                target1=False,
                component_balanced=1.7,
                hybrid=3.5,
            )
        ),
        enrich_row(
            detector_row(
                xs="188,250,264",
                ranks="9,3,2",
                all_truth=True,
                truth_hits=3,
                component_balanced=1.4,
                hybrid=3.1,
            )
        ),
    ]
    selector = {
        "selector_label": "fixture_geometry_prior",
        "component_balanced_weight": 0.5,
        "hybrid_span_component_weight": 0.2,
        "component_min_weight": 0.0,
        "span_prior_weight": 0.5,
        "signed_gap_prior_weight": 4.0,
        "center_prior_weight": 0.2,
        "rank_sum_weight": 0.1,
        "max_rank_weight": 0.05,
    }

    _, selected_indices = precompute_selected_indices(rows, [selector])
    selected = selected_rows_for_selector_index([selector], rows, selected_indices, 0)
    summary = summarize_selected(selector, selected)

    assert selected[0]["candidate_x_values_mm"] == "188,250,264"
    assert summary["all_truth_case_count"] == 1
    assert summary["target1_hit_count"] == 1


def test_summary_reports_improvement_over_component_selector():
    selector_row = {
        "selector_label": "fixture_geometry_prior",
        "all_truth_case_count": 2,
        "mean_unique_truth_hit_count": 2.0,
        "target0_hit_count": 2,
        "target1_hit_count": 2,
        "target2_hit_count": 2,
    }
    selected_rows = [
        enrich_row(detector_row(seed=13, all_truth=True)),
        enrich_row(detector_row(seed=21, run_name="run_b", all_truth=False, truth_hits=1, target1=False)),
    ]
    cv_summaries = [
        {"cv_strategy": "leave_one_case", "all_truth_case_count": 1, "mean_unique_truth_hit_count": 1.5},
        {"cv_strategy": "leave_one_seed", "all_truth_case_count": 1, "mean_unique_truth_hit_count": 1.5},
        {"cv_strategy": "leave_one_branch", "all_truth_case_count": 0, "mean_unique_truth_hit_count": 1.0},
    ]
    previous = {
        "best_in_sample_all_truth_case_count": 1,
        "leave_one_case_all_truth_case_count": 0,
    }

    summary = summarize_audit(selected_rows, [selector_row], selected_rows, cv_summaries, previous)

    assert summary["best_in_sample_all_truth_case_count"] == 2
    assert summary["in_sample_improvement_over_component_selector"] == 1
    assert summary["leave_one_case_improvement_over_component_selector"] == 1
    assert summary["ready_for_detector_seeded_fwi"] is False
