import math

from run_gssi_field_short_profile_time_zero_application_policy import (
    applied_transfer_rows,
    leave_one_out_transfer_rows,
    summarize_applied_transfer,
)


def _event_pairs():
    return [
        {
            "pair_index": "1",
            "comparison_minus_reference_phase_time_ns": "0.17681728880157166",
        },
        {
            "pair_index": "2",
            "comparison_minus_reference_phase_time_ns": "0.10805500982318272",
        },
        {
            "pair_index": "3",
            "comparison_minus_reference_phase_time_ns": "0.12770137524557956",
        },
    ]


def test_applied_transfer_rows_remove_median_offset():
    rows = applied_transfer_rows(_event_pairs(), 0.12770137524557956)

    assert math.isclose(rows[0]["corrected_comparison_minus_reference_phase_time_ns"], 0.0491159135559921)
    assert math.isclose(rows[1]["corrected_comparison_minus_reference_phase_time_ns"], -0.01964636542239684)
    assert math.isclose(rows[2]["corrected_comparison_minus_reference_phase_time_ns"], 0.0)


def test_leave_one_out_transfer_rows_hold_out_each_pair():
    rows = leave_one_out_transfer_rows(_event_pairs())

    by_pair = {int(row["holdout_pair_index"]): row for row in rows}
    assert math.isclose(by_pair[1]["loo_fitted_transfer_offset_ns"], 0.11787819253438114)
    assert math.isclose(by_pair[1]["holdout_corrected_phase_residual_ns"], 0.05893909626719052)
    assert by_pair[1]["training_pair_count"] == 2


def test_summarize_applied_transfer_accepts_consistent_application():
    summary = summarize_applied_transfer(
        _event_pairs(),
        {
            "policy_label": "relative_time_zero_transfer_limited_qc",
            "median_comparison_minus_reference_phase_time_ns": 0.12770137524557956,
        },
        max_corrected_abs_residual_ns=0.06,
        max_loo_abs_residual_ns=0.07,
        min_residual_reduction_factor=3.0,
    )

    assert summary["policy_label"] == "applied_relative_time_zero_transfer_qc"
    assert summary["application_consistent"] is True
    assert summary["event_pair_count"] == 3
    assert summary["corrected_max_abs_phase_residual_ns"] < 0.05
    assert summary["leave_one_out_max_abs_residual_ns"] < 0.06
    assert summary["mean_abs_residual_reduction_factor"] > 5.0


def test_summarize_applied_transfer_requires_prior_limited_qc_policy():
    summary = summarize_applied_transfer(
        _event_pairs(),
        {
            "policy_label": "relative_time_zero_transfer_pattern_only",
            "median_comparison_minus_reference_phase_time_ns": 0.12770137524557956,
        },
        max_corrected_abs_residual_ns=0.06,
        max_loo_abs_residual_ns=0.07,
        min_residual_reduction_factor=3.0,
    )

    assert summary["application_consistent"] is False
    assert summary["policy_label"] == "applied_relative_time_zero_transfer_limited"
