from run_cross_seed_fitted_ringdown_summary import (
    compare_seed_pair,
    package_target_rows,
    parse_package_arg,
    summarize_cross_seed,
)


def _package(label, target_rows):
    return {
        "label": label,
        "path": f"{label}.json",
        "target_rows": target_rows,
    }


def _target(target_index, margin, best_objective):
    return {
        "target_index": target_index,
        "truth_x_mm": 10.0 + target_index,
        "truth_z_mm": 20.0 + target_index,
        "truth_radius_mm": 5.0 + target_index,
        "base_best_x_mm": 10.0 + target_index,
        "base_best_z_mm": 20.0 + target_index,
        "base_best_radius_mm": 5.0 + target_index,
        "base_is_truth_geometry": True,
        "base_confidence_label": "moderate",
        "base_radius_margin_abs": margin,
        "base_radius_margin_rel": 0.02,
        "best_truth_preserving_objective": best_objective,
        "best_truth_preserving_margin_abs": margin * 1.25,
        "best_truth_preserving_ratio_to_base": 1.25,
    }


def test_parse_package_arg_splits_label_and_path():
    label, path = parse_package_arg("seed89=outputs/summary.json")

    assert label == "seed89"
    assert str(path) == "outputs/summary.json"


def test_compare_seed_pair_marks_weaker_and_same_objective():
    rows = package_target_rows([
        _package("seed21", [_target(1, 8.0e-4, "late_high")]),
        _package("seed89", [_target(1, 6.0e-4, "late_high")]),
    ])

    comparisons = compare_seed_pair(rows, "seed21", "seed89")

    assert comparisons[0]["comparison_direction"] == "weaker"
    assert comparisons[0]["best_objective_same"] is True
    assert abs(comparisons[0]["comparison_to_baseline_margin_ratio"] - 0.75) < 1e-12


def test_summarize_cross_seed_counts_direction_and_objectives():
    rows = package_target_rows([
        _package("seed21", [_target(0, 5.0e-4, "veryhigh"), _target(1, 8.0e-4, "late_high")]),
        _package("seed89", [_target(0, 6.0e-4, "veryhigh"), _target(1, 6.0e-4, "late_high")]),
    ])
    comparisons = compare_seed_pair(rows, "seed21", "seed89")

    summary = summarize_cross_seed(rows, comparisons)

    assert summary["seed_count"] == 2
    assert summary["target_count"] == 2
    assert summary["base_truth_rows"] == 4
    assert summary["comparison_direction_counts"] == {"stronger": 1, "weaker": 1}
    assert summary["best_objective_same_count"] == 2
