from run_local_2d_detector_depth_slot_prior_probe import (
    depth_prior_score,
    evaluate_prior_grid,
    slot_prior_score,
    summarize_prior_probe,
)
from run_local_2d_detector_geometry_family_selector import enrich_row


def _row(
    *,
    case="case_a",
    run_name="run_a",
    xs="190,250,264",
    zs="90,90,90",
    all_truth=True,
    truth_hits=3,
    component_score=1.0,
):
    return enrich_row(
        {
            "case_label": case,
            "branch_key": "target2_close14",
            "seed": "13",
            "case_variant": "nominal",
            "run_name": run_name,
            "combo_index": xs.replace(",", "_"),
            "candidate_ranks": "1,2,3",
            "candidate_x_values_mm": xs,
            "candidate_z_values_mm": zs,
            "unique_all_truths_within_tolerance": str(all_truth),
            "unique_truth_hit_count": truth_hits,
            "unique_target0_hit": str(truth_hits >= 1),
            "unique_target1_hit": str(truth_hits >= 2),
            "unique_target2_hit": str(truth_hits >= 3),
            "score_component_balanced": component_score,
            "score_hybrid_span_component": component_score,
            "score_component_min": component_score / 3.0,
        }
    )


def _selector():
    return {
        "selector_label": "fixture_selector",
        "component_balanced_weight": 1.0,
        "hybrid_span_component_weight": 0.0,
        "component_min_weight": 0.0,
        "span_prior_weight": 0.0,
        "signed_gap_prior_weight": 0.0,
        "center_prior_weight": 0.0,
        "rank_sum_weight": 0.0,
        "max_rank_weight": 0.0,
    }


def test_depth_prior_allows_broad_90mm_band_and_penalizes_deep_components():
    shallow = _row(zs="85,90,97")
    deep = _row(zs="90,115,125")

    assert depth_prior_score(shallow) == 0.0
    assert depth_prior_score(deep) < 0.0


def test_slot_prior_rewards_expected_branch_slots():
    aligned = _row(xs="190,250,264")
    shifted = _row(xs="210,250,290")

    assert slot_prior_score(aligned) == 0.0
    assert slot_prior_score(shifted) < slot_prior_score(aligned)


def test_prior_grid_can_promote_depth_consistent_truth_but_keeps_fwi_blocked():
    rows = [
        _row(case="case_a", run_name="run_a", xs="190,250,264", zs="90,90,90", all_truth=True, component_score=1.0),
        _row(
            case="case_a",
            run_name="run_a",
            xs="188,250,266",
            zs="115,116,118",
            all_truth=False,
            truth_hits=2,
            component_score=1.6,
        ),
        _row(
            case="case_b",
            run_name="run_b",
            xs="188,249,266",
            zs="88,92,94",
            all_truth=False,
            truth_hits=2,
            component_score=1.0,
        ),
    ]

    variant_rows, selected_rows = evaluate_prior_grid(
        rows,
        _selector(),
        depth_weights=(0.0, 4.0),
        slot_weights=(0.0,),
    )
    summary = summarize_prior_probe(variant_rows, selector_label="fixture_selector", candidate_row_count=len(rows))

    base = [row for row in variant_rows if row["variant_label"] == "depth0_slot0"][0]
    best = [row for row in variant_rows if row["variant_label"] == "depth4_slot0"][0]

    assert len(selected_rows) == 4
    assert base["all_truth_case_count"] == 0
    assert best["all_truth_case_count"] == 1
    assert summary["base_all_truth_case_count"] == 0
    assert summary["best_all_truth_case_count"] == 1
    assert summary["ready_for_detector_seeded_fwi"] is False
