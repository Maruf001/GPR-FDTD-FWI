import math

import numpy as np

from run_gssi_field_short_profile_timing_bootstrap_policy import (
    bootstrap_cell_medians,
    stable_offset_rows,
    stable_phase_conventions,
    summarize_bootstrap_policy,
)


def _summary_rows():
    return [
        {"phase_convention": "a", "stable_transfer_convention": "True"},
        {"phase_convention": "b", "stable_transfer_convention": "False"},
        {"phase_convention": "c", "stable_transfer_convention": "True"},
        {"phase_convention": "d", "stable_transfer_convention": "True"},
        {"phase_convention": "e", "stable_transfer_convention": "True"},
    ]


def _event_rows():
    rows = []
    values = {
        "a": [0.11, 0.12, 0.13],
        "b": [0.02, 0.03, 0.04],
        "c": [0.10, 0.12, 0.14],
        "d": [0.11, 0.12, 0.12],
        "e": [0.12, 0.13, 0.14],
    }
    for convention, deltas in values.items():
        for idx, delta in enumerate(deltas, start=1):
            rows.append({
                "pair_index": str(idx),
                "phase_convention": convention,
                "comparison_minus_reference_time_ns": str(delta),
            })
    return rows


def test_stable_offset_rows_keep_only_stable_conventions():
    stable = stable_phase_conventions(_summary_rows())
    rows = stable_offset_rows(_event_rows(), stable)

    assert stable == ["a", "c", "d", "e"]
    assert len(rows) == 12
    assert {row["phase_convention"] for row in rows} == {"a", "c", "d", "e"}


def test_bootstrap_cell_medians_is_deterministic_with_seed():
    values = np.asarray([0.11, 0.12, 0.13, 0.14], dtype=np.float64)

    row = bootstrap_cell_medians(
        values,
        iterations=200,
        alpha=0.10,
        rng=np.random.default_rng(7),
    )

    assert row["bootstrap_method"] == "cell"
    assert math.isclose(row["observed_median_ns"], 0.125)
    assert row["ci_lower_ns"] <= row["bootstrap_median_ns"] <= row["ci_upper_ns"]


def test_summarize_bootstrap_policy_accepts_positive_tight_intervals():
    stable = stable_phase_conventions(_summary_rows())
    rows = stable_offset_rows(_event_rows(), stable)
    bootstrap_rows = [
        {
            "bootstrap_method": "cell",
            "observed_median_ns": 0.12,
            "ci_lower_ns": 0.10,
            "ci_upper_ns": 0.14,
            "ci_width_ns": 0.04,
        },
        {
            "bootstrap_method": "phase_convention_cluster",
            "observed_median_ns": 0.12,
            "ci_lower_ns": 0.10,
            "ci_upper_ns": 0.13,
            "ci_width_ns": 0.03,
        },
    ]

    summary = summarize_bootstrap_policy(
        bootstrap_rows,
        rows,
        min_ci_lower_ns=0.09,
        max_ci_width_ns=0.05,
        min_stable_conventions=4,
    )

    assert summary["policy_label"] == "bootstrap_relative_time_zero_supported_qc"
    assert summary["stable_phase_convention_count"] == 4
    assert summary["all_stable_offsets_positive"] is True
