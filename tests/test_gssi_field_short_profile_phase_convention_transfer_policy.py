import math

from run_gssi_field_short_profile_phase_convention_transfer_policy import (
    convention_event_offset_rows,
    convention_summary_rows,
    summarize_phase_convention_transfer,
)


def _event_pairs():
    return [
        {
            "pair_index": "1",
            "reference_file": "PROJECT001C__014.DZT",
            "comparison_file": "PROJECT001C__016.DZT",
            "reference_apex_group": "1",
            "comparison_apex_group": "3",
            "aligned_x_residual_mm": "-10.0",
        },
        {
            "pair_index": "2",
            "reference_file": "PROJECT001C__014.DZT",
            "comparison_file": "PROJECT001C__016.DZT",
            "reference_apex_group": "2",
            "comparison_apex_group": "2",
            "aligned_x_residual_mm": "-10.0",
        },
        {
            "pair_index": "3",
            "reference_file": "PROJECT001C__014.DZT",
            "comparison_file": "PROJECT001C__016.DZT",
            "reference_apex_group": "3",
            "comparison_apex_group": "1",
            "aligned_x_residual_mm": "20.0",
        },
    ]


def _phase_rows():
    rows = []
    values = {
        ("PROJECT001C__014.DZT", 1): (0.70, 0.48, 0.82, 0.96, 0.63, 0.78),
        ("PROJECT001C__014.DZT", 2): (0.71, 0.54, 0.95, 1.00, 0.66, 0.82),
        ("PROJECT001C__014.DZT", 3): (0.71, 0.51, 0.85, 0.97, 0.66, 0.80),
        ("PROJECT001C__016.DZT", 1): (0.73, 0.64, 0.99, 1.09, 0.78, 0.90),
        ("PROJECT001C__016.DZT", 2): (0.77, 0.65, 0.99, 1.11, 0.78, 0.91),
        ("PROJECT001C__016.DZT", 3): (0.83, 0.66, 0.99, 1.10, 0.79, 0.90),
    }
    for (file_name, group), times in values.items():
        rows.append({
            "file": file_name,
            "apex_group": str(group),
            "current_cue_time_ns": times[0],
            "top_envelope_35pct_time_ns": times[1],
            "envelope_max_time_ns": times[2],
            "signed_positive_peak_time_ns": times[3],
            "signed_negative_peak_time_ns": times[4],
            "nearest_zero_crossing_time_ns": times[5],
        })
    return rows


def test_convention_event_offset_rows_pair_reversed_events():
    rows = convention_event_offset_rows(_event_pairs(), _phase_rows())
    top = [
        row for row in rows
        if row["phase_convention"] == "top_envelope_35pct"
    ]

    assert len(top) == 3
    assert math.isclose(top[0]["comparison_minus_reference_time_ns"], 0.18)
    assert math.isclose(top[1]["comparison_minus_reference_time_ns"], 0.11)
    assert math.isclose(top[2]["comparison_minus_reference_time_ns"], 0.13)


def test_convention_summary_marks_low_spread_positive_conventions_stable():
    rows = convention_event_offset_rows(_event_pairs(), _phase_rows())
    summary = convention_summary_rows(rows, max_range_ns=0.10, max_robust_sigma_ns=0.04)
    by_convention = {row["phase_convention"]: row for row in summary}

    assert by_convention["top_envelope_35pct"]["stable_transfer_convention"] is True
    assert by_convention["signed_negative_peak"]["stable_transfer_convention"] is True
    assert by_convention["current_cue"]["stable_transfer_convention"] is False


def test_summarize_phase_convention_transfer_accepts_four_stable_conventions():
    rows = convention_event_offset_rows(_event_pairs(), _phase_rows())
    convention_rows = convention_summary_rows(rows, max_range_ns=0.10, max_robust_sigma_ns=0.04)

    summary = summarize_phase_convention_transfer(
        convention_rows,
        accepted_convention="top_envelope_35pct",
        min_stable_conventions=4,
        max_stable_median_spread_ns=0.05,
    )

    assert summary["policy_label"] == "multi_phase_relative_time_zero_supported_qc"
    assert summary["stable_phase_convention_count"] >= 4
    assert summary["accepted_phase_convention_stable"] is True
