from run_competing_geometry_near_tie_audit import (
    geometry_delta_class,
    near_tie_tier,
    summarize_audit,
    target_summary_rows,
)


def test_geometry_delta_class_reports_changed_axes():
    assert geometry_delta_class({
        "competitor_delta_x_mm": -1,
        "competitor_delta_z_mm": 0,
        "competitor_delta_radius_mm": 0,
    }) == "x"
    assert geometry_delta_class({
        "competitor_delta_x_mm": 0,
        "competitor_delta_z_mm": -1,
        "competitor_delta_radius_mm": -0.4,
    }) == "z+radius"
    assert geometry_delta_class({
        "competitor_delta_x_mm": 0,
        "competitor_delta_z_mm": 0,
        "competitor_delta_radius_mm": 0,
    }) == "none"


def test_near_tie_tier_separates_reported_hidden_duplicate_and_separated():
    assert near_tie_tier({
        "competitor_within_ambiguity_threshold": False,
    }) == "competitor_separated"
    assert near_tie_tier({
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_width_nonzero": True,
        "competitor_delta_x_mm": 1,
    }) == "reported_width_near_tie"
    assert near_tie_tier({
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_width_nonzero": False,
        "competitor_delta_z_mm": -1,
        "competitor_delta_radius_mm": -0.4,
    }) == "zero_width_competing_geometry_near_tie"
    assert near_tie_tier({
        "competitor_within_ambiguity_threshold": True,
        "ambiguity_width_nonzero": False,
        "competitor_delta_x_mm": 0,
        "competitor_delta_z_mm": 0,
        "competitor_delta_radius_mm": 0,
    }) == "zero_width_duplicate_objective_near_tie"


def test_target_summary_rows_counts_hidden_near_ties():
    rows = [
        {
            "target_index": 1,
            "near_tie_tier": "zero_width_competing_geometry_near_tie",
            "geometry_delta_class": "z+radius",
        },
        {
            "target_index": 2,
            "near_tie_tier": "reported_width_near_tie",
            "geometry_delta_class": "x",
        },
        {
            "target_index": 2,
            "near_tie_tier": "competitor_separated",
            "geometry_delta_class": "none",
        },
    ]

    summary_rows = target_summary_rows(rows)

    assert summary_rows[0]["target_index"] == 1
    assert summary_rows[0]["zero_width_competing_geometry_near_tie_count"] == 1
    assert summary_rows[0]["geometry_delta_classes"] == "z+radius"
    assert summary_rows[1]["reported_width_near_tie_count"] == 1
    assert summary_rows[1]["competitor_separated_count"] == 1


def test_summarize_audit_recommends_competitor_threshold_metric():
    summary_rows = [
        {
            "target_index": 1,
            "reported_width_near_tie_count": 0,
            "zero_width_competing_geometry_near_tie_count": 1,
            "zero_width_duplicate_objective_near_tie_count": 0,
            "competitor_separated_count": 2,
        }
    ]

    summary = summarize_audit([{}, {}, {}], summary_rows)

    assert summary["policy_label"] == "competing_geometry_near_tie_zero_width_metric_gap_cpu_no_gpu"
    assert summary["zero_width_competing_geometry_near_tie_count"] == 1
    assert summary["hidden_near_tie_targets"] == "1"
    assert "not competitor_within_ambiguity_threshold" in summary["recommended_metric"]
    assert summary["gpu_priority"] == "none_now"
