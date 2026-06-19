from run_local_2d_detector_geometry_family_selector import enrich_row
from run_local_2d_detector_selector_counterfactual_sensitivity import (
    counterfactual_selector_grid,
    evaluate_counterfactuals,
    summarize_counterfactual_sensitivity,
    summarize_families,
)


def detector_row(
    *,
    seed=13,
    run_name="run_a",
    xs="188,250,264",
    ranks="9,3,2",
    all_truth=True,
    truth_hits=3,
    target0=True,
    target1=True,
    target2=True,
    component_balanced=1.0,
    hybrid=1.0,
    component_min=0.2,
):
    return {
        "branch_key": "target2_close14",
        "seed": seed,
        "case_variant": "nominal",
        "run_name": run_name,
        "candidate_x_values_mm": xs,
        "candidate_z_values_mm": "80,82,84",
        "candidate_ranks": ranks,
        "combo_index": ranks.replace(",", ""),
        "unique_all_truths_within_tolerance": str(all_truth),
        "unique_truth_hit_count": truth_hits,
        "unique_target0_hit": str(target0),
        "unique_target1_hit": str(target1),
        "unique_target2_hit": str(target2),
        "score_component_balanced": component_balanced,
        "score_hybrid_span_component": hybrid,
        "score_component_min": component_min,
    }


def base_selector():
    return {
        "selector_label": "fixture_base",
        "component_balanced_weight": 0.5,
        "hybrid_span_component_weight": 0.2,
        "component_min_weight": 0.0,
        "span_prior_weight": 0.5,
        "signed_gap_prior_weight": 4.0,
        "center_prior_weight": 0.2,
        "rank_sum_weight": 0.1,
        "max_rank_weight": 0.05,
    }


def test_counterfactual_selector_grid_contains_ablation_and_sweeps():
    selectors = counterfactual_selector_grid(base_selector())
    labels = {selector["counterfactual_label"] for selector in selectors}

    assert len(selectors) == 44
    assert "base_current" in labels
    assert "ablation_drop_signed_gap_prior" in labels
    assert "signed_gap_sweep_w0" in labels
    assert "signed_gap_sweep_w12" in labels
    assert "component_sweep_w2" in labels


def test_evaluate_counterfactuals_reports_failed_selector_case():
    rows = [
        enrich_row(detector_row(all_truth=True, component_balanced=1.0)),
        enrich_row(
            detector_row(
                xs="186,221,265",
                ranks="4,2,1",
                all_truth=False,
                truth_hits=2,
                target1=False,
                component_balanced=1.5,
            )
        ),
    ]
    selector = dict(base_selector())
    selector.update(
        {
            "component_balanced_weight": 1.0,
            "hybrid_span_component_weight": 0.0,
            "span_prior_weight": 0.0,
            "signed_gap_prior_weight": 0.0,
            "center_prior_weight": 0.0,
            "rank_sum_weight": 0.0,
            "max_rank_weight": 0.0,
        }
    )
    selector["counterfactual_label"] = "base_current"
    selector["counterfactual_family"] = "base"

    variant_rows, selected_rows = evaluate_counterfactuals(rows, [selector])

    assert len(selected_rows) == 1
    assert variant_rows[0]["counterfactual_label"] == "base_current"
    assert variant_rows[0]["all_truth_case_count"] == 0
    assert variant_rows[0]["failed_selector_case_count"] == 1
    assert variant_rows[0]["dominant_loss_feature"] == "score_component_balanced"


def test_summary_keeps_counterfactual_result_as_no_fwi_guardrail():
    variant_rows = [
        {
            "counterfactual_label": "base_current",
            "counterfactual_family": "base",
            "all_truth_case_count": 3,
            "failed_selector_case_count": 9,
            "mean_unique_truth_hit_count": 1.75,
            "median_required_selector_gain_to_choose_truth": 0.18,
            "max_required_selector_gain_to_choose_truth": 0.55,
            "dominant_loss_feature": "signed_gap_prior_score",
            "signed_gap_prior_weight": 4.0,
        },
        {
            "counterfactual_label": "signed_gap_sweep_w0",
            "counterfactual_family": "signed_gap_sweep",
            "all_truth_case_count": 1,
            "failed_selector_case_count": 11,
            "mean_unique_truth_hit_count": 1.25,
            "median_required_selector_gain_to_choose_truth": 0.06,
            "max_required_selector_gain_to_choose_truth": 0.24,
            "dominant_loss_feature": "score_hybrid_span_component",
            "signed_gap_prior_weight": 0.0,
        },
    ]
    family_rows = summarize_families(variant_rows)

    summary = summarize_counterfactual_sensitivity(variant_rows, family_rows, "fixture_base")

    assert summary["base_all_truth_case_count"] == 3
    assert summary["best_all_truth_case_count"] == 3
    assert summary["best_improvement_over_base_all_truth_cases"] == 0
    assert summary["signed_gap_zero_all_truth_case_count"] == 1
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"
