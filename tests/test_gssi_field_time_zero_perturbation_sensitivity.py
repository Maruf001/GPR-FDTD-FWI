import math

from run_gssi_field_time_zero_perturbation_sensitivity import (
    is_supported_row,
    summarize_perturbations,
    unique_offset_configs,
)


def test_unique_offset_configs_builds_ordered_budget_envelope():
    budget = {
        "relative_anchor_offset_ns": 0.12,
        "conservative_half_width_ns": 0.05,
        "bootstrap_ci_lower_ns": 0.10,
        "bootstrap_observed_median_offset_ns": 0.115,
        "bootstrap_ci_upper_ns": 0.14,
    }

    configs = unique_offset_configs(budget)

    labels = [row["offset_label"] for row in configs]
    assert labels == [
        "no_correction",
        "conservative_lower",
        "bootstrap_ci_lower",
        "bootstrap_median",
        "nominal_relative_anchor",
        "bootstrap_ci_upper",
        "conservative_upper",
    ]
    assert configs[0]["offset_ns"] == 0.0
    assert math.isclose(configs[1]["offset_delta_from_nominal_ns"], -0.05)
    assert math.isclose(configs[-1]["offset_delta_from_nominal_ns"], 0.05)


def test_is_supported_row_requires_all_stack_thresholds():
    assert is_supported_row({
        "matrix_abs_correlation_improvement": 0.051,
        "corrected_matrix_abs_correlation": 0.65,
        "improved_column_fraction": 0.55,
    })
    assert not is_supported_row({
        "matrix_abs_correlation_improvement": 0.049,
        "corrected_matrix_abs_correlation": 0.80,
        "improved_column_fraction": 0.75,
    })


def test_summarize_perturbations_marks_ci_robust_conservative_mixed():
    rows = []
    for label, family in [
        ("bootstrap_ci_lower", "bootstrap_ci"),
        ("bootstrap_median", "bootstrap_ci"),
        ("bootstrap_ci_upper", "bootstrap_ci"),
        ("nominal_relative_anchor", "nominal"),
    ]:
        for window in ("0.35_1.1ns", "0.45_1.25ns"):
            rows.append({
                "offset_label": label,
                "offset_family": family,
                "window_label": window,
                "offset_window_supported": True,
                "matrix_abs_correlation_improvement": 0.12,
                "corrected_matrix_abs_correlation": 0.82,
                "improved_column_fraction": 0.63,
            })
    rows.append({
        "offset_label": "conservative_lower",
        "offset_family": "conservative_envelope",
        "window_label": "0.35_1.1ns",
        "offset_window_supported": False,
        "matrix_abs_correlation_improvement": 0.01,
        "corrected_matrix_abs_correlation": 0.70,
        "improved_column_fraction": 0.60,
    })
    rows.append({
        "offset_label": "conservative_upper",
        "offset_family": "conservative_envelope",
        "window_label": "0.35_1.1ns",
        "offset_window_supported": True,
        "matrix_abs_correlation_improvement": 0.08,
        "corrected_matrix_abs_correlation": 0.73,
        "improved_column_fraction": 0.58,
    })

    summary = summarize_perturbations(rows)

    assert summary["policy_label"] == "field_time_zero_ci_perturbation_stack_robust_conservative_mixed"
    assert summary["bootstrap_ci_supported_count"] == 6
    assert summary["bootstrap_ci_row_count"] == 6
    assert summary["nominal_supported_count"] == 2
    assert summary["conservative_supported_count"] == 1
    assert summary["ready_for_manuscript_uncertainty_sensitivity"] is True


def test_summarize_perturbations_marks_ci_mixed_when_bootstrap_endpoint_fails():
    rows = [
        {
            "offset_label": "nominal_relative_anchor",
            "offset_family": "nominal",
            "window_label": "0.45_1.25ns",
            "offset_window_supported": True,
            "matrix_abs_correlation_improvement": 0.12,
            "corrected_matrix_abs_correlation": 0.82,
            "improved_column_fraction": 0.63,
        },
        {
            "offset_label": "bootstrap_ci_lower",
            "offset_family": "bootstrap_ci",
            "window_label": "0.45_1.25ns",
            "offset_window_supported": False,
            "matrix_abs_correlation_improvement": 0.01,
            "corrected_matrix_abs_correlation": 0.82,
            "improved_column_fraction": 0.63,
        },
        {
            "offset_label": "bootstrap_median",
            "offset_family": "bootstrap_ci",
            "window_label": "0.45_1.25ns",
            "offset_window_supported": True,
            "matrix_abs_correlation_improvement": 0.09,
            "corrected_matrix_abs_correlation": 0.82,
            "improved_column_fraction": 0.63,
        },
    ]

    summary = summarize_perturbations(rows)

    assert summary["policy_label"] == "field_time_zero_perturbation_stack_nominal_supported_ci_mixed"
    assert summary["ready_for_manuscript_uncertainty_sensitivity"] is False
