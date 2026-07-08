import numpy as np

from run_gssi_field_profile_alignment_policy import (
    alignment_rows,
    best_alignment,
    classify_alignment,
    normalized_correlation,
    robust_normalize,
)


def test_robust_normalize_centers_constant_signal():
    out = robust_normalize(np.ones(8))

    assert np.allclose(out, np.zeros(8))


def test_normalized_correlation_finds_shifted_match():
    reference = np.array([0, 0, 1, 3, 1, 0, 0], dtype=float)
    comparison = np.array([0, 1, 3, 1, 0, 0, 0], dtype=float)

    best = best_alignment(alignment_rows(reference, comparison, dx_m=0.01, max_lag_m=0.03, orientation="direct"))

    assert best["lag_samples"] == -1
    assert best["normalized_correlation"] > 0.99
    assert normalized_correlation(reference, comparison, -1) > normalized_correlation(reference, comparison, 0)


def test_reversed_orientation_can_win():
    reference = np.array([0, 1, 3, 0, 0, 0], dtype=float)
    comparison = reference[::-1]
    direct_rows = alignment_rows(reference, comparison, dx_m=0.01, max_lag_m=0.0, orientation="direct")
    reversed_rows = alignment_rows(reference, comparison, dx_m=0.01, max_lag_m=0.0, orientation="reversed")
    direct_best = best_alignment(direct_rows)
    reversed_best = best_alignment(reversed_rows)
    best = best_alignment(direct_rows + reversed_rows)

    assert best["orientation"] == "reversed"
    assert reversed_best["normalized_correlation"] > direct_best["normalized_correlation"]
    assert classify_alignment(best, direct_best, reversed_best).endswith("reversed_scan_preferred")
