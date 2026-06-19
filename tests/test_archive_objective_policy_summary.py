from run_archive_objective_policy_summary import (
    assign_objective_rows,
    filter_noncanonical_primary_rows,
    policy_rows,
    run_is_canonical_primary,
    summarize_archive_policy,
    target_from_geometry,
)


def test_target_from_geometry_matches_known_three_rebar_truth():
    assert target_from_geometry((150.0, 80.0, 5.0)) == 0
    assert target_from_geometry((250.0, 100.0, 6.0)) == 1
    assert target_from_geometry((1.0, 2.0, 3.0)) is None


def test_assign_objective_rows_uses_run_summary_for_single_target_runs():
    run_rows = [{"run_id": "1", "target": "2"}]
    objective_rows = [
        {
            "run_id": "1",
            "objective_label": "base",
            "objective_margin": "0.1",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
        },
        {
            "run_id": "1",
            "objective_label": "highband",
            "objective_margin": "0.2",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
        },
    ]

    rows = assign_objective_rows(run_rows, objective_rows)

    assert {row["assigned_target"] for row in rows} == {2}
    assert rows[0]["assignment_method"] == "single_target_run_summary"
    assert rows[0]["is_truth_geometry_for_assigned_target"] is False


def test_assign_objective_rows_uses_geometry_for_multi_target_runs():
    run_rows = [{"run_id": "1", "target": "0"}]
    objective_rows = [
        {
            "run_id": "1",
            "objective_label": "base",
            "objective_margin": "0.1",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
        },
        {
            "run_id": "1",
            "objective_label": "base",
            "objective_margin": "0.2",
            "best_x_mm": "250.0",
            "best_z_mm": "100.0",
            "best_radius_mm": "6.0",
        },
        {
            "run_id": "1",
            "objective_label": "highband",
            "objective_margin": "0.3",
            "best_x_mm": "150.0",
            "best_z_mm": "80.0",
            "best_radius_mm": "5.0",
        },
        {
            "run_id": "1",
            "objective_label": "highband",
            "objective_margin": "0.4",
            "best_x_mm": "250.0",
            "best_z_mm": "100.0",
            "best_radius_mm": "6.0",
        },
    ]

    rows = assign_objective_rows(run_rows, objective_rows)

    assert [row["assigned_target"] for row in rows] == [0, 1, 0, 1]
    assert {row["assignment_method"] for row in rows} == {"multi_target_geometry"}


def test_summarize_archive_policy_computes_ratios_by_run_and_target():
    assigned_rows = [
        {
            "run_id": "1",
            "assigned_target": 0,
            "objective_label": "base",
            "objective_margin": "0.0004",
            "is_truth_geometry_for_assigned_target": True,
        },
        {
            "run_id": "1",
            "assigned_target": 0,
            "objective_label": "highband",
            "objective_margin": "0.0006",
            "is_truth_geometry_for_assigned_target": True,
        },
    ]

    rows = summarize_archive_policy(assigned_rows, cutoff=5.0e-4)

    highband = next(row for row in rows if row["objective_label"] == "highband")
    assert highband["accepted_count"] == 1
    assert highband["truth_geometry_count"] == 1
    assert round(highband["margin_ratio_mean"], 6) == 1.5


def test_policy_rows_uses_archive_scale_confirmation_threshold():
    summary_rows = [
        {
            "target_label": "target0",
            "objective_label": "base",
            "accepted_fraction": 0.2,
            "row_count": 10,
            "truth_geometry_count": 10,
            "margin_ratio_mean": 1.0,
            "radius_margin_abs_mean": 0.0004,
        },
        {
            "target_label": "target0",
            "objective_label": "highband",
            "accepted_fraction": 0.95,
            "row_count": 10,
            "truth_geometry_count": 10,
            "margin_ratio_mean": 1.3,
            "radius_margin_abs_mean": 0.0006,
        },
        {
            "target_label": "target0",
            "objective_label": "late",
            "accepted_fraction": 1.0,
            "row_count": 10,
            "truth_geometry_count": 9,
            "margin_ratio_mean": 1.5,
            "radius_margin_abs_mean": 0.0007,
        },
    ]

    rows = policy_rows(summary_rows)

    assert rows[0]["archive_scale_confirmation_objectives"] == "highband"
    assert rows[0]["strongest_archive_secondary_objective"] == "highband"


def test_filter_noncanonical_primary_rows_skips_update_rule_probe():
    run_rows = [
        {"run_id": "1", "base_margin_is_canonical": "True"},
        {"run_id": "2", "base_margin_is_canonical": "False"},
    ]
    objective_rows = [
        {"run_id": "1", "objective_label": "base"},
        {"run_id": "2", "objective_label": "base"},
        {"run_id": "2", "objective_label": "canonical_base"},
    ]

    filtered_runs, filtered_objectives, skipped_runs, skipped_objectives = (
        filter_noncanonical_primary_rows(run_rows, objective_rows)
    )

    assert [row["run_id"] for row in filtered_runs] == ["1"]
    assert [row["run_id"] for row in filtered_objectives] == ["1"]
    assert skipped_runs == 1
    assert skipped_objectives == 2


def test_missing_canonical_primary_flag_defaults_to_canonical_for_old_tables():
    assert run_is_canonical_primary({"run_id": "old"}) is True
