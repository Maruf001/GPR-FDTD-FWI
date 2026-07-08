import numpy as np

from run_gssi_field_profile_network_alignment import (
    aligned_vectors_for_lag,
    align_profile_pair,
    build_network,
    classify_pair,
    normalized_overlap_correlation,
)


def test_aligned_vectors_for_positive_lag_embeds_comparison():
    reference = np.arange(10, dtype=float)
    comparison = np.arange(4, dtype=float)

    ref, cmp = aligned_vectors_for_lag(reference, comparison, lag_samples=3)

    assert ref.tolist() == [3.0, 4.0, 5.0, 6.0]
    assert cmp.tolist() == [0.0, 1.0, 2.0, 3.0]


def test_normalized_overlap_correlation_respects_min_overlap():
    reference = np.array([0, 1, 2, 3, 0], dtype=float)
    comparison = np.array([1, 2, 3], dtype=float)

    assert normalized_overlap_correlation(reference, comparison, lag_samples=1, min_overlap=3) > 0.99
    assert np.isnan(normalized_overlap_correlation(reference, comparison, lag_samples=4, min_overlap=3))


def test_align_profile_pair_finds_reversed_embedded_segment():
    long_signature = np.array([0, 0, 1, 3, 6, 2, 0, 0, 0], dtype=float)
    short_signature = np.array([1, 3, 6, 2, 0], dtype=float)[::-1]
    first = {
        "stem": "long",
        "trace_count": long_signature.size,
        "dx_m": 0.01,
        "signature": long_signature,
    }
    second = {
        "stem": "short",
        "trace_count": short_signature.size,
        "dx_m": 0.01,
        "signature": short_signature,
    }

    pair, _rows = align_profile_pair(first, second, min_overlap_fraction=1.0)

    assert pair["best_orientation"] == "reversed"
    assert pair["pair_label"] == "embedded_segment_candidate"
    assert abs(pair["best_lag_mm"] - 20.0) < 1.0e-9


def test_classify_pair_marks_orientation_ambiguous_before_repeat():
    best = {"normalized_correlation": 0.90}
    direct = {"normalized_correlation": 0.90}
    reversed_best = {"normalized_correlation": 0.88}

    assert classify_pair(best, direct, reversed_best, length_ratio=1.0) == "orientation_or_lag_ambiguous"


def test_build_network_returns_all_pairs():
    entries = [
        {"stem": "a", "trace_count": 5, "dx_m": 0.01, "signature": np.array([0, 1, 2, 1, 0], dtype=float)},
        {"stem": "b", "trace_count": 5, "dx_m": 0.01, "signature": np.array([0, 1, 2, 1, 0], dtype=float)},
        {"stem": "c", "trace_count": 5, "dx_m": 0.01, "signature": np.array([0, 0, 1, 0, 0], dtype=float)},
    ]

    pair_rows, lag_rows = build_network(entries, min_overlap_fraction=0.8)

    assert len(pair_rows) == 3
    assert lag_rows
