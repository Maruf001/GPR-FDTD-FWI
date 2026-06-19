from run_gssi_field_profile_repeatability_policy import (
    build_repeatability_summary,
    pair_profiles,
    summarize_profiles,
)


def _event(file_name, group, x_m, time_ns, radius=5.0, corr=0.8):
    return {
        "file": file_name,
        "profile_stem": file_name.replace(".DZT", ""),
        "apex_group": group,
        "x_m": x_m,
        "accepted_phase_time_ns": time_ns,
        "fitted_depth_mm": 25.0 + group,
        "best_abs_correlation": corr,
        "best_radius_mm": radius,
        "radius_margin_abs": 0.01,
    }


def test_summarize_profiles_reports_spacing_and_radius_consensus():
    rows = [
        _event("a.DZT", 1, 0.10, 0.5, radius=5.0),
        _event("a.DZT", 2, 0.40, 0.6, radius=5.0),
        _event("a.DZT", 3, 0.70, 0.7, radius=6.0),
    ]

    summary = summarize_profiles(rows)

    assert len(summary) == 1
    assert summary[0]["event_count"] == 3
    assert round(summary[0]["mean_spacing_mm"], 3) == 300.0
    assert summary[0]["radius_mode_mm"] == 5.0
    assert summary[0]["radius_mode_count"] == 2


def test_pair_profiles_aligns_by_median_lateral_shift():
    rows = [
        _event("a.DZT", 1, 0.10, 0.50, radius=5.0),
        _event("a.DZT", 2, 0.40, 0.55, radius=5.0),
        _event("a.DZT", 3, 0.70, 0.60, radius=5.0),
        _event("b.DZT", 1, 0.12, 0.65, radius=6.0),
        _event("b.DZT", 2, 0.42, 0.70, radius=6.0),
        _event("b.DZT", 3, 0.72, 0.75, radius=6.0),
    ]

    pair_rows, spacing_rows, summary = pair_profiles(rows)

    assert len(pair_rows) == 3
    assert len(spacing_rows) == 2
    assert round(summary["median_lateral_shift_mm"], 3) == 20.0
    assert round(summary["max_abs_aligned_x_residual_mm"], 3) == 0.0
    assert summary["radius_match_count"] == 0
    assert summary["repeatability_label"] == "spacing_repeatable_radius_not_repeatable"


def test_build_repeatability_summary_marks_weak_large_spacing_error():
    pair_rows = [
        {"aligned_x_residual_mm": 60.0, "phase_time_delta_ns": 0.1, "radius_match": True, "reference_best_abs_correlation": 0.8, "comparison_best_abs_correlation": 0.81},
        {"aligned_x_residual_mm": -55.0, "phase_time_delta_ns": 0.2, "radius_match": True, "reference_best_abs_correlation": 0.82, "comparison_best_abs_correlation": 0.83},
    ]
    spacing_rows = [{"abs_spacing_delta_mm": 80.0}]

    summary = build_repeatability_summary(pair_rows, spacing_rows, "a.DZT", "b.DZT", 0.0)

    assert summary["repeatability_label"] == "weak_profile_repeatability"
    assert summary["radius_match_count"] == 2
