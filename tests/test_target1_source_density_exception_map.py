from run_target1_source_density_exception_map import (
    build_branch_rows,
    build_per_run_rows,
    parse_run_ids,
    summarize_exception_map,
)


def _source_rows():
    return [
        {
            "series_id": "accepted_helped",
            "seed": "1",
            "run_ids": "1, 2",
            "first_run": "1",
            "last_run": "2",
            "n_runs": "2",
            "n_accepted": "1",
            "n_weak": "1",
            "first_setting": "5",
            "last_setting": "9",
            "best_setting": "9",
            "worst_setting": "5",
            "first_margin": "0.00045",
            "last_margin": "0.00056",
            "best_margin": "0.00056",
            "worst_margin": "0.00045",
            "best_minus_first_margin": "0.00011",
            "last_minus_first_margin": "0.00011",
            "last_worse_than_first": "False",
            "status": "source_escalation_helped_one_branch",
        },
        {
            "series_id": "terminal_11",
            "seed": "2",
            "run_ids": "3, 4",
            "first_run": "3",
            "last_run": "4",
            "n_runs": "2",
            "n_accepted": "0",
            "n_weak": "2",
            "first_setting": "5",
            "last_setting": "11",
            "best_setting": "5",
            "worst_setting": "11",
            "first_margin": "0.00048",
            "last_margin": "0.00037",
            "best_margin": "0.00048",
            "worst_margin": "0.00037",
            "best_minus_first_margin": "0.0",
            "last_minus_first_margin": "-0.00011",
            "last_worse_than_first": "True",
            "status": "all_base_weak",
        },
        {
            "series_id": "legacy_exception",
            "seed": "3",
            "run_ids": "5",
            "first_run": "5",
            "last_run": "5",
            "n_runs": "1",
            "n_accepted": "0",
            "n_weak": "1",
            "first_setting": "7",
            "last_setting": "7",
            "best_setting": "7",
            "worst_setting": "7",
            "first_margin": "0.00035",
            "last_margin": "0.00035",
            "best_margin": "0.00035",
            "worst_margin": "0.00035",
            "best_minus_first_margin": "0.0",
            "last_minus_first_margin": "0.0",
            "last_worse_than_first": "False",
            "status": "all_base_weak",
        },
        {
            "series_id": "modern_exception",
            "seed": "4",
            "run_ids": "6",
            "first_run": "6",
            "last_run": "6",
            "n_runs": "1",
            "n_accepted": "0",
            "n_weak": "1",
            "first_setting": "9",
            "last_setting": "9",
            "best_setting": "9",
            "worst_setting": "9",
            "first_margin": "0.00044",
            "last_margin": "0.00044",
            "best_margin": "0.00044",
            "worst_margin": "0.00044",
            "best_minus_first_margin": "0.0",
            "last_minus_first_margin": "0.0",
            "last_worse_than_first": "False",
            "status": "all_base_weak",
        },
    ]


def _coordinate_rows():
    rows = []
    for run_id, source, ringdown, margin in [
        (1, 5, 0.5, 0.00045),
        (2, 9, 0.5, 0.00056),
        (3, 5, 0.5, 0.00048),
        (4, 11, 0.5, 0.00037),
        (5, 7, 0.25, 0.00035),
        (6, 9, 0.5, 0.00044),
    ]:
        rows.append({
            "run_id": str(run_id),
            "seed": str(run_id),
            "sources": str(source),
            "tx_rx_offset_mm": "60",
            "ringdown_value": str(ringdown),
            "base_margin": str(margin),
            "exact_geometry": "True",
            "run_name": f"run_{run_id}",
        })
    return rows


def _objective_rows():
    rows = []
    for run_id, margin in [
        (1, 0.00070),
        (2, 0.00080),
        (3, 0.00060),
        (4, 0.00055),
        (5, 0.00042),
        (6, 0.00043),
    ]:
        rows.append({
            "run_id": str(run_id),
            "objective_label": "late_high",
            "objective_margin": str(margin),
            "best_x_mm": "250",
            "best_z_mm": "100",
            "best_radius_mm": "6",
        })
    return rows


def test_parse_run_ids_accepts_comma_and_semicolon_lists():
    assert parse_run_ids("1, 2; 3") == [1, 2, 3]


def test_branch_rows_classify_source_density_actions():
    rows = build_branch_rows(_source_rows(), _coordinate_rows(), _objective_rows())
    by_series = {row["series_id"]: row for row in rows}

    assert by_series["accepted_helped"]["recommended_action"] == "accepted_branch_no_rerun"
    assert by_series["terminal_11"]["recommended_action"] == "do_not_extend_source_density"
    assert by_series["terminal_11"]["terminal_11_worse"] is True
    assert by_series["legacy_exception"]["recommended_action"] == "legacy_exception_no_gpu"
    assert by_series["legacy_exception"]["late_high_exception_run_ids"] == "5"
    assert by_series["modern_exception"]["recommended_action"] == "modern_exception_review_before_gpu"
    assert by_series["modern_exception"]["gpu_priority"] == "review_first"


def test_per_run_rows_preserve_late_high_and_base_flags():
    rows = build_per_run_rows(_source_rows(), _coordinate_rows(), _objective_rows())
    by_run = {row["run_id"]: row for row in rows}

    assert by_run[2]["base_accepted"] is True
    assert by_run[2]["late_high_accepted"] is True
    assert by_run[5]["base_accepted"] is False
    assert by_run[5]["late_high_accepted"] is False
    assert by_run[5]["ringdown_value"] == 0.25


def test_summary_requests_review_only_for_modern_exception():
    branch_rows = build_branch_rows(_source_rows(), _coordinate_rows(), _objective_rows())
    per_run_rows = build_per_run_rows(_source_rows(), _coordinate_rows(), _objective_rows())
    summary = summarize_exception_map(branch_rows, per_run_rows)

    assert summary["policy_label"] == "target1_source_density_exception_map_review_before_gpu"
    assert summary["source_density_series_count"] == 4
    assert summary["terminal_11_worse_count"] == 1
    assert summary["source_escalation_helped_count"] == 1
    assert summary["lower_source_count_best_count"] == 3
    assert summary["legacy_exception_series_count"] == 1
    assert summary["modern_exception_series_count"] == 1
    assert summary["gpu_priority"] == "review_first"
    assert summary["legacy_exception_run_ids"] == "5"
