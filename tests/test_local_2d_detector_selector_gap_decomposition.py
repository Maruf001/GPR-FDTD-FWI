import pytest

from run_local_2d_detector_geometry_family_selector import enrich_row
from run_local_2d_detector_selector_gap_decomposition import (
    build_gap_rows,
    dominant_loss_feature,
    feature_contributions,
    summarize_features,
    summarize_gap_decomposition,
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
    component_balanced=1.0,
    hybrid=1.0,
    component_min=0.2,
):
    return {
        "branch_key": branch_key,
        "seed": seed,
        "case_variant": case_variant,
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


def component_selector(label="component_fixture"):
    return {
        "selector_label": label,
        "component_balanced_weight": 1.0,
        "hybrid_span_component_weight": 0.0,
        "component_min_weight": 0.0,
        "span_prior_weight": 0.0,
        "signed_gap_prior_weight": 0.0,
        "center_prior_weight": 0.0,
        "rank_sum_weight": 0.0,
        "max_rank_weight": 0.0,
    }


def test_feature_contributions_use_selector_weights():
    row = enrich_row(detector_row(component_balanced=2.0, hybrid=5.0))
    selector = component_selector()
    selector["hybrid_span_component_weight"] = 0.5

    contributions = feature_contributions(row, selector)

    assert contributions["score_component_balanced"] == 2.0
    assert contributions["score_hybrid_span_component"] == 2.5
    assert contributions["score_component_min"] == 0.0


def test_gap_rows_identify_component_score_loss_against_truth():
    rows = [
        enrich_row(
            detector_row(
                xs="188,250,264",
                ranks="9,3,2",
                all_truth=True,
                component_balanced=1.0,
            )
        ),
        enrich_row(
            detector_row(
                xs="186,221,265",
                ranks="4,2,1",
                all_truth=False,
                truth_hits=2,
                target1=False,
                component_balanced=1.4,
            )
        ),
    ]

    gap_rows = build_gap_rows(rows, component_selector())

    assert len(gap_rows) == 1
    assert gap_rows[0]["selected_all_truth"] is False
    assert gap_rows[0]["required_selector_gain_to_choose_truth"] == pytest.approx(0.4)
    assert gap_rows[0]["dominant_loss_feature"] == "score_component_balanced"
    assert gap_rows[0]["delta_truth_minus_selected_score_component_balanced"] == pytest.approx(-0.4)


def test_summary_keeps_detector_fwi_blocked_after_gap_decomposition():
    rows = [
        enrich_row(detector_row(seed=13, all_truth=True, component_balanced=2.0)),
        enrich_row(detector_row(seed=13, all_truth=False, truth_hits=2, target1=False, component_balanced=1.0)),
        enrich_row(detector_row(seed=21, run_name="run_b", all_truth=True, component_balanced=1.0)),
        enrich_row(detector_row(seed=21, run_name="run_b", all_truth=False, truth_hits=2, target1=False, component_balanced=1.5)),
    ]
    selector = component_selector()

    gap_rows = build_gap_rows(rows, selector)
    feature_rows = summarize_features(gap_rows)
    summary = summarize_gap_decomposition(gap_rows, feature_rows, selector)

    assert summary["selected_all_truth_case_count"] == 1
    assert summary["failed_selector_case_count"] == 1
    assert summary["dominant_loss_feature"] == "score_component_balanced"
    assert summary["ready_for_detector_seeded_fwi"] is False
    assert summary["gpu_priority"] == "none"


def test_dominant_loss_feature_marks_selected_truth_without_deficit():
    assert dominant_loss_feature({"score_component_balanced": -1.0}, selected_all_truth=True) == "selected_truth"
