import math

from run_coordinate_weak_exact_secondary_confirmation_audit import (
    canonical_weak_exact_rows,
    objective_summary_rows,
    per_run_confirmation_rows,
    select_objective_row,
    target_policy_rows,
    build_rows_by_run_objective,
)


def _coordinate_rows():
    return [
        {
            "run_id": "1",
            "target": "0",
            "exact_geometry": "True",
            "base_margin_is_canonical": "True",
            "confidence_label": "weak",
            "seed": "89",
            "sources": "15",
            "tx_rx_offset_mm": "60",
            "ringdown_value": "0.35",
            "base_margin": "0.000452",
            "run_name": "all target duplicate row case",
        },
        {
            "run_id": "2",
            "target": "1",
            "exact_geometry": "True",
            "base_margin_is_canonical": "True",
            "confidence_label": "weak",
            "seed": "610",
            "sources": "5",
            "tx_rx_offset_mm": "60",
            "ringdown_value": "0.5",
            "base_margin": "0.000468",
            "run_name": "target1 weak exact",
        },
        {
            "run_id": "3",
            "target": "2",
            "exact_geometry": "True",
            "base_margin_is_canonical": "False",
            "confidence_label": "weak",
            "seed": "610",
            "base_margin": "0.0008",
        },
    ]


def _objective_rows():
    return [
        {
            "run_id": "1",
            "objective_label": "highband",
            "objective_margin": "0.000522",
            "best_x_mm": "150",
            "best_z_mm": "80",
            "best_radius_mm": "5",
        },
        {
            "run_id": "1",
            "objective_label": "highband",
            "objective_margin": "0.000675",
            "best_x_mm": "250",
            "best_z_mm": "100",
            "best_radius_mm": "6",
        },
        {
            "run_id": "1",
            "objective_label": "base",
            "objective_margin": "0.000452",
            "best_x_mm": "150",
            "best_z_mm": "80",
            "best_radius_mm": "5",
        },
        {
            "run_id": "2",
            "objective_label": "base",
            "objective_margin": "0.000468",
            "best_x_mm": "250",
            "best_z_mm": "100",
            "best_radius_mm": "6",
        },
        {
            "run_id": "2",
            "objective_label": "late_high",
            "objective_margin": "0.000767",
            "best_x_mm": "250",
            "best_z_mm": "100",
            "best_radius_mm": "6",
        },
    ]


def test_canonical_weak_exact_rows_excludes_noncanonical_rows():
    rows = canonical_weak_exact_rows(_coordinate_rows())

    assert [(row["target"], row["run_id"]) for row in rows] == [("0", "1"), ("1", "2")]


def test_select_objective_row_uses_matching_target_truth_when_run_has_multiple_targets():
    rows_by_key = build_rows_by_run_objective(_objective_rows())

    selected = select_objective_row(rows_by_key, 1, "highband", 0)

    assert math.isclose(float(selected["objective_margin"]), 0.000522)
    assert selected["best_radius_mm"] == "5"


def test_per_run_confirmation_rows_preserve_target_specific_margins():
    rows = per_run_confirmation_rows(
        canonical_weak_exact_rows(_coordinate_rows()),
        _objective_rows(),
        cutoff=5.0e-4,
    )
    by_target = {row["target"]: row for row in rows}

    assert math.isclose(by_target[0]["highband_margin"], 0.000522)
    assert by_target[0]["highband_truth_geometry"] is True
    assert by_target[0]["highband_accepted"] is True
    assert by_target[1]["late_high_accepted"] is True


def test_target_policy_rows_classify_full_secondary_confirmation():
    per_run = per_run_confirmation_rows(
        canonical_weak_exact_rows(_coordinate_rows()),
        _objective_rows(),
        cutoff=5.0e-4,
    )
    summary = objective_summary_rows(per_run, cutoff=5.0e-4)
    policies = target_policy_rows(per_run, summary)
    by_target = {row["target"]: row for row in policies}

    assert by_target[0]["strongest_secondary_objective"] == "highband"
    assert by_target[0]["policy_label"] == "full_secondary_confirmation"
    assert by_target[1]["strongest_secondary_objective"] == "late_high"
