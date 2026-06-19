import numpy as np

from run_local_2d_detector_image_objective_gate import (
    hyperbola_mask,
    image_objective_score,
    select_best_rows,
    summarize_selected,
)


def _row(case, score, hits, label="row_background_sigma60"):
    return {
        "branch_key": case[0],
        "seed": str(case[1]),
        "case_variant": case[2],
        "run_name": f"{case[0]}_{case[1]}_{case[2]}",
        "objective_label": label,
        "image_objective_score": score,
        "assignment_status": "assigned",
        "assigned_detection_ranks": "1,2,3",
        "candidate_budget": "20",
        "config_key": "cfg",
        "assignment_policy_key": "policy",
        "unique_truth_hit_count_numeric": sum(hits),
        "unique_all_truths_bool": all(hits),
        "unique_target0_bool": hits[0],
        "unique_target1_bool": hits[1],
        "unique_target2_bool": hits[2],
        "failure_label": "all_truth" if all(hits) else "missed",
    }


def test_image_objective_score_prefers_matching_hyperbola_geometry():
    scan_x = np.linspace(0.05, 0.45, 7)
    time_values = np.linspace(0.0, 8.0e-9, 512)
    true_mask = hyperbola_mask(
        scan_x,
        time_values,
        [190.0, 250.0, 264.0],
        [90.0, 90.0, 90.0],
        tx_rx_offset_m=0.045,
        time_offset_s=667.0e-12,
        sigma_ps=60.0,
    )

    matching = image_objective_score(
        true_mask,
        scan_x,
        time_values,
        [190.0, 250.0, 264.0],
        [90.0, 90.0, 90.0],
        tx_rx_offset_m=0.045,
        offsets_s=[667.0e-12],
        sigma_ps=60.0,
    )
    shifted = image_objective_score(
        true_mask,
        scan_x,
        time_values,
        [210.0, 270.0, 290.0],
        [90.0, 90.0, 90.0],
        tx_rx_offset_m=0.045,
        offsets_s=[667.0e-12],
        sigma_ps=60.0,
    )

    assert matching["image_objective_score"] > shifted["image_objective_score"]
    assert matching["best_time_offset_ps"] == 667.0


def test_select_best_rows_uses_objective_score_without_truth():
    rows = [
        _row(("close14", 13, "nominal"), 0.7, (False, True, False)),
        _row(("close14", 13, "nominal"), 0.9, (True, True, True)),
        _row(("close14", 21, "nominal"), 0.8, (False, True, True)),
    ]

    selected = select_best_rows(rows, "row_background_sigma60")
    summary = summarize_selected("row_background_sigma60", selected)

    assert len(selected) == 2
    assert selected[0]["image_objective_score"] == 0.9
    assert summary["all_truth_case_count"] == 1
    assert summary["target1_hit_count"] == 2
