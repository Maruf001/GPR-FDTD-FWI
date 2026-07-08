from run_gssi_field_identifiability_policy import (
    filter_policy_rows,
    summarize_events,
    summarize_profiles,
)


def _row(file_name, group, radius, epsr_source, corr, shift=0.2, phase="top_envelope_35pct"):
    return {
        "candidate_id": f"{file_name}_g{group}_r{radius}_{epsr_source}",
        "file": file_name,
        "phase_convention": phase,
        "apex_group": str(group),
        "geometry_valid": "True",
        "synthetic_time_shift_ns": shift,
        "absolute_correlation": corr,
        "normalized_correlation": corr,
        "normalized_residual_rms": 1.0 - corr,
        "radius_mm": radius,
        "epsr_source": epsr_source,
        "concrete_epsr": 9.0,
        "fitted_depth_m": 0.03,
        "polarity": "same",
    }


def test_filter_policy_rows_keeps_only_accepted_phase_and_shift():
    rows = [
        _row("a.DZT", 1, 5.0, "fitted", 0.8),
        _row("a.DZT", 1, 5.0, "fitted", 0.7, shift=0.1),
        _row("a.DZT", 1, 5.0, "fitted", 0.6, phase="cue_time"),
        {**_row("a.DZT", 1, 5.0, "fitted", 0.9), "geometry_valid": "False"},
    ]

    accepted = filter_policy_rows(rows, "top_envelope_35pct", 0.2)

    assert len(accepted) == 1
    assert accepted[0]["absolute_correlation"] == 0.8


def test_summarize_events_reports_radius_and_epsr_margins():
    rows = [
        _row("a.DZT", 1, 5.0, "fitted", 0.82),
        _row("a.DZT", 1, 6.0, "fitted", 0.81),
        _row("a.DZT", 1, 5.0, "config", 0.78),
        _row("a.DZT", 1, 6.0, "config", 0.77),
    ]

    summary = summarize_events(rows, margin_threshold=0.02, correlation_floor=0.7)

    assert len(summary) == 1
    row = summary[0]
    assert row["best_radius_mm"] == 5.0
    assert round(row["radius_margin_abs"], 3) == 0.010
    assert row["radius_margin_clear"] is False
    assert row["best_epsr_source"] == "fitted"
    assert round(row["epsr_margin_abs"], 3) == 0.040
    assert row["epsr_margin_clear"] is True
    assert row["correlation_floor_pass"] is True


def test_summarize_profiles_counts_radius_consensus():
    event_rows = [
        {
            "file": "a.DZT",
            "best_abs_correlation": 0.8,
            "best_radius_mm": 5.0,
            "radius_margin_abs": 0.01,
            "best_epsr_source": "fitted",
            "epsr_margin_abs": 0.03,
            "best_fitted_depth_m": 0.03,
        },
        {
            "file": "a.DZT",
            "best_abs_correlation": 0.82,
            "best_radius_mm": 5.0,
            "radius_margin_abs": 0.02,
            "best_epsr_source": "fitted",
            "epsr_margin_abs": 0.04,
            "best_fitted_depth_m": 0.031,
        },
        {
            "file": "a.DZT",
            "best_abs_correlation": 0.79,
            "best_radius_mm": 6.0,
            "radius_margin_abs": 0.005,
            "best_epsr_source": "config",
            "epsr_margin_abs": 0.01,
            "best_fitted_depth_m": 0.032,
        },
    ]

    summary = summarize_profiles(event_rows)

    assert len(summary) == 1
    assert summary[0]["radius_mode_mm"] == 5.0
    assert summary[0]["radius_mode_count"] == 2
    assert round(summary[0]["radius_consensus_fraction"], 3) == 0.667
    assert summary[0]["epsr_mode"] == "fitted"
