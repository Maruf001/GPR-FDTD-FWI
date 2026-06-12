from run_cross_condition_fitted_ringdown_summary import (
    compare_condition_pair,
    condition_target_rows,
    parse_condition_arg,
    summarize_cross_condition,
)


def _condition(label, target_rows):
    return {
        "label": label,
        "path": f"{label}.json",
        "target_rows": target_rows,
    }


def _target(target_index, margin, confidence, best_objective):
    return {
        "target_index": target_index,
        "truth_x_mm": 10.0 + target_index,
        "truth_z_mm": 20.0 + target_index,
        "truth_radius_mm": 5.0 + target_index,
        "base_best_x_mm": 10.0 + target_index,
        "base_best_z_mm": 20.0 + target_index,
        "base_best_radius_mm": 5.0 + target_index,
        "base_is_truth_geometry": True,
        "base_confidence_label": confidence,
        "base_radius_margin_abs": margin,
        "base_radius_margin_rel": 0.02,
        "best_truth_preserving_objective": best_objective,
        "best_truth_preserving_margin_abs": margin * 1.25,
        "best_truth_preserving_ratio_to_base": 1.25,
    }


def test_parse_condition_arg_splits_label_and_path():
    label, path = parse_condition_arg("ringdown035=outputs/summary.json")

    assert label == "ringdown035"
    assert str(path) == "outputs/summary.json"


def test_compare_condition_pair_tracks_margin_and_confidence_change():
    rows = condition_target_rows([
        _condition("ringdown025", [_target(2, 9.0e-4, "moderate", "late_high")]),
        _condition("ringdown035", [_target(2, 1.2e-3, "strong", "late_high")]),
    ])

    comparisons = compare_condition_pair(rows, "ringdown025", "ringdown035")

    assert comparisons[0]["comparison_direction"] == "stronger"
    assert comparisons[0]["confidence_label_change"] == "moderate->strong"
    assert comparisons[0]["best_objective_same"] is True
    assert abs(comparisons[0]["comparison_to_baseline_margin_ratio"] - (1.2 / 0.9)) < 1e-12


def test_summarize_cross_condition_counts_transitions_and_objectives():
    rows = condition_target_rows([
        _condition("ringdown025", [
            _target(0, 5.0e-4, "moderate", "veryhigh"),
            _target(1, 6.0e-4, "moderate", "late_high"),
        ]),
        _condition("ringdown035", [
            _target(0, 5.5e-4, "moderate", "veryhigh"),
            _target(1, 7.0e-4, "strong", "late_high"),
        ]),
    ])
    comparisons = compare_condition_pair(rows, "ringdown025", "ringdown035")

    summary = summarize_cross_condition(rows, comparisons)

    assert summary["condition_count"] == 2
    assert summary["target_count"] == 2
    assert summary["base_truth_rows"] == 4
    assert summary["comparison_direction_counts"] == {"stronger": 2}
    assert summary["confidence_label_change_counts"] == {
        "moderate->moderate": 1,
        "moderate->strong": 1,
    }
    assert summary["best_objective_same_count"] == 2
