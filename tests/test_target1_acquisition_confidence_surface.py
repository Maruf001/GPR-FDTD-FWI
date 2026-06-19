import math

from run_target1_acquisition_confidence_surface import (
    build_source_series_policy_rows,
    build_surface_rows,
    canonical_target1_rows,
    summarize,
)


def _coordinate_rows():
    return [
        {
            "run_id": "10",
            "target": "1",
            "base_margin_is_canonical": "True",
            "base_margin": "0.00055",
            "sources": "5",
            "tx_rx_offset_mm": "60",
            "exact_geometry": "True",
        },
        {
            "run_id": "11",
            "target": "1",
            "base_margin_is_canonical": "True",
            "base_margin": "0.00045",
            "sources": "9",
            "tx_rx_offset_mm": "60",
            "exact_geometry": "True",
        },
        {
            "run_id": "12",
            "target": "1",
            "base_margin_is_canonical": "True",
            "base_margin": "0.00040",
            "sources": "9",
            "tx_rx_offset_mm": "55",
            "exact_geometry": "True",
        },
        {
            "run_id": "13",
            "target": "2",
            "base_margin_is_canonical": "True",
            "base_margin": "0.00040",
            "sources": "9",
            "tx_rx_offset_mm": "55",
            "exact_geometry": "True",
        },
        {
            "run_id": "14",
            "target": "1",
            "base_margin_is_canonical": "False",
            "base_margin": "0.00090",
            "sources": "11",
            "tx_rx_offset_mm": "60",
            "exact_geometry": "True",
        },
    ]


def _objective_rows():
    rows = []
    for run_id, margin, truth in [
        ("10", "0.00080", True),
        ("11", "0.00070", True),
        ("12", "0.00042", True),
    ]:
        rows.append({
            "run_id": run_id,
            "objective_label": "late_high",
            "objective_margin": margin,
            "best_x_mm": "250" if truth else "251",
            "best_z_mm": "100",
            "best_radius_mm": "6",
        })
    return rows


def _source_series_rows():
    return [
        {
            "series_id": "seed_a",
            "seed": "a",
            "run_ids": "10,11",
            "first_run": "10",
            "last_run": "11",
            "n_runs": "2",
            "n_accepted": "1",
            "n_weak": "1",
            "first_setting": "5",
            "last_setting": "9",
            "best_setting": "9",
            "worst_setting": "5",
            "first_margin": "0.00045",
            "last_margin": "0.00055",
            "best_margin": "0.00055",
            "worst_margin": "0.00045",
            "best_minus_first_margin": "0.00010",
            "all_exact_geometry": "True",
            "outcome_category": "mixed: accepted setting exists",
        },
        {
            "series_id": "seed_b",
            "seed": "b",
            "run_ids": "12,13",
            "first_run": "12",
            "last_run": "13",
            "n_runs": "2",
            "n_accepted": "0",
            "n_weak": "2",
            "first_setting": "5",
            "last_setting": "11",
            "best_setting": "5",
            "worst_setting": "11",
            "first_margin": "0.00044",
            "last_margin": "0.00036",
            "best_margin": "0.00044",
            "worst_margin": "0.00036",
            "best_minus_first_margin": "0.0",
            "all_exact_geometry": "True",
            "outcome_category": "all weak",
        },
    ]


def test_canonical_target1_rows_filter_scope():
    rows = canonical_target1_rows(_coordinate_rows())

    assert [row["run_id"] for row in rows] == ["10", "11", "12"]


def test_build_surface_rows_tracks_base_and_secondary_confirmation():
    rows = build_surface_rows(_coordinate_rows(), _objective_rows(), "sources", "source_count")
    by_setting = {row["setting"]: row for row in rows}

    assert by_setting[5.0]["accepted_count"] == 1
    assert by_setting[5.0]["late_high_accepted_count"] == 1
    assert by_setting[9.0]["row_count"] == 2
    assert by_setting[9.0]["weak_exact_count"] == 2
    assert by_setting[9.0]["late_high_accepted_count"] == 1
    assert by_setting[9.0]["status"] == "secondary_exception_present"


def test_source_series_policy_marks_nonmonotonic_branches():
    rows = build_source_series_policy_rows(_source_series_rows())
    by_seed = {row["seed"]: row for row in rows}

    assert by_seed["a"]["status"] == "source_escalation_helped_one_branch"
    assert by_seed["b"]["status"] == "all_base_weak"
    assert by_seed["b"]["last_worse_than_first"] is True
    assert math.isclose(by_seed["b"]["last_minus_first_margin"], -0.00008)


def test_summary_keeps_gpu_priority_none_and_counts_branch_behaviour():
    surface_rows = (
        build_surface_rows(_coordinate_rows(), _objective_rows(), "sources", "source_count")
        + build_surface_rows(_coordinate_rows(), _objective_rows(), "tx_rx_offset_mm", "txrx_offset")
    )
    policy_rows = build_source_series_policy_rows(_source_series_rows())
    summary = summarize(surface_rows, policy_rows, _coordinate_rows(), _objective_rows())

    assert summary["policy_label"] == "target1_acquisition_confidence_surface_exact_but_nonmonotonic_cpu_no_gpu"
    assert summary["target1_canonical_row_count"] == 3
    assert summary["target1_exact_geometry_count"] == 3
    assert summary["target1_base_accepted_count"] == 1
    assert summary["target1_base_weak_exact_count"] == 2
    assert summary["target1_late_high_accepted_count"] == 2
    assert summary["source_density_escalation_helped_count"] == 1
    assert summary["source_density_terminal_11_worse_count"] == 1
    assert summary["gpu_priority"] == "none_now"
