import math

import numpy as np

from run_gssi_field_corrected_profile_stack import (
    align_matrix_to_reference,
    compare_matrices,
    summarize_corrected_stack,
)


def test_align_matrix_to_reference_applies_orientation_and_lag():
    matrix = np.array([[1.0, 2.0, 3.0, 4.0], [10.0, 20.0, 30.0, 40.0]])

    direct = align_matrix_to_reference(matrix, "direct", 1)
    reversed_matrix = align_matrix_to_reference(matrix, "reversed", 0)
    reversed_lag = align_matrix_to_reference(matrix, "reversed", -1)

    np.testing.assert_allclose(direct[:, :3], np.array([[2.0, 3.0, 4.0], [20.0, 30.0, 40.0]]))
    assert np.isnan(direct[0, 3])
    np.testing.assert_allclose(reversed_matrix, np.array([[4.0, 3.0, 2.0, 1.0], [40.0, 30.0, 20.0, 10.0]]))
    assert np.isnan(reversed_lag[0, 0])
    np.testing.assert_allclose(reversed_lag[:, 1:], np.array([[4.0, 3.0, 2.0], [40.0, 30.0, 20.0]]))


def test_compare_matrices_reports_perfect_same_shape_match():
    reference = np.arange(20, dtype=float).reshape(4, 5)
    comparison = reference.copy()

    metrics = compare_matrices(reference, comparison)

    assert math.isclose(metrics["absolute_correlation"], 1.0)
    assert math.isclose(metrics["normalized_residual_rms"], 0.0)
    assert metrics["polarity"] == "same"


def test_summarize_corrected_stack_marks_supported_profile_correction():
    rows = [
        {"abs_correlation_improvement": 0.12, "corrected_abs_correlation": 0.78},
        {"abs_correlation_improvement": 0.08, "corrected_abs_correlation": 0.74},
        {"abs_correlation_improvement": -0.01, "corrected_abs_correlation": 0.67},
    ]
    raw_matrix = {"absolute_correlation": 0.62, "normalized_residual_rms": 0.9}
    corrected_matrix = {
        "absolute_correlation": 0.74,
        "normalized_residual_rms": 0.6,
        "valid_sample_count": 120,
    }

    summary = summarize_corrected_stack(
        rows,
        raw_matrix,
        corrected_matrix,
        transfer_offset_ns=0.12,
        orientation="reversed",
        lag_samples=25,
        lag_mm=83.3,
    )

    assert summary["policy_label"] == "corrected_profile_stack_time_zero_supported"
    assert summary["improved_column_count"] == 2
    assert math.isclose(summary["improved_column_fraction"], 2 / 3)
    assert math.isclose(summary["matrix_abs_correlation_improvement"], 0.12)
