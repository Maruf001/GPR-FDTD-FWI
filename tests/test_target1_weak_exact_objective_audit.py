import math

from run_target1_weak_exact_objective_audit import (
    audit_decision,
    canonical_target1_weak_exact_rows,
    per_run_objective_rows,
    subset_policy_rows,
    summarize_objectives,
)


def _coordinate_rows():
    return [
        {
            "run_id": "10",
            "target": "1",
            "exact_geometry": "True",
            "base_margin_is_canonical": "True",
            "confidence_label": "weak",
            "seed": "610",
            "sources": "5",
            "tx_rx_offset_mm": "60",
            "ringdown_value": "0.5",
            "base_margin": "0.00045",
            "run_name": "weak modern",
        },
        {
            "run_id": "11",
            "target": "1",
            "exact_geometry": "True",
            "base_margin_is_canonical": "True",
            "confidence_label": "weak",
            "seed": "89",
            "sources": "7",
            "tx_rx_offset_mm": "60",
            "ringdown_value": "0.25",
            "base_margin": "0.00035",
            "run_name": "weak legacy",
        },
        {
            "run_id": "12",
            "target": "1",
            "exact_geometry": "True",
            "base_margin_is_canonical": "False",
            "confidence_label": "weak",
            "seed": "610",
            "sources": "5",
            "tx_rx_offset_mm": "55",
            "ringdown_value": "0.5",
            "base_margin": "0.00080",
            "run_name": "noncanonical",
        },
        {
            "run_id": "13",
            "target": "2",
            "exact_geometry": "True",
            "base_margin_is_canonical": "True",
            "confidence_label": "weak",
            "seed": "610",
            "base_margin": "0.00045",
        },
    ]


def _objective_rows():
    rows = []
    for run_id, base, late_high in [
        (10, 0.00045, 0.00075),
        (11, 0.00035, 0.00042),
    ]:
        rows.extend([
            {
                "run_id": str(run_id),
                "objective_label": "base",
                "objective_margin": str(base),
                "best_x_mm": "250",
                "best_z_mm": "100",
                "best_radius_mm": "6",
            },
            {
                "run_id": str(run_id),
                "objective_label": "late_high",
                "objective_margin": str(late_high),
                "best_x_mm": "250",
                "best_z_mm": "100",
                "best_radius_mm": "6",
            },
        ])
    return rows


def test_canonical_target1_weak_exact_rows_excludes_wrong_scope():
    rows = canonical_target1_weak_exact_rows(_coordinate_rows())

    assert [row["run_id"] for row in rows] == ["10", "11"]


def test_summarize_objectives_counts_truth_and_cutoff():
    weak = canonical_target1_weak_exact_rows(_coordinate_rows())
    rows = summarize_objectives(weak, _objective_rows(), cutoff=5.0e-4)
    by_objective = {row["objective_label"]: row for row in rows}

    assert by_objective["base"]["accepted_count"] == 0
    assert by_objective["late_high"]["truth_geometry_count"] == 2
    assert by_objective["late_high"]["accepted_count"] == 1
    assert math.isclose(by_objective["late_high"]["median_ratio_to_base"], (0.00075 / 0.00045 + 0.00042 / 0.00035) / 2)


def test_subset_policy_rows_separates_modern_from_archive_exception():
    weak = canonical_target1_weak_exact_rows(_coordinate_rows())
    per_run = per_run_objective_rows(weak, _objective_rows(), cutoff=5.0e-4)
    subsets = subset_policy_rows(per_run, cutoff=5.0e-4)
    by_subset = {row["subset"]: row for row in subsets}

    assert by_subset["all"]["weak_exact_row_count"] == 2
    assert by_subset["all"]["late_high_accepted_count"] == 1
    assert by_subset["all"]["late_high_nonaccepted_run_ids"] == "11"
    assert by_subset["ringdown050"]["late_high_accepted_count"] == 1
    assert by_subset["ringdown050"]["weak_exact_row_count"] == 1


def test_audit_decision_prefers_ringdown050_confirmation_with_archive_exception():
    weak = canonical_target1_weak_exact_rows(_coordinate_rows())
    per_run = per_run_objective_rows(weak, _objective_rows(), cutoff=5.0e-4)
    decision = audit_decision(subset_policy_rows(per_run, cutoff=5.0e-4))

    assert decision["policy_label"] == "target1_ringdown050_latehigh_secondary_confirmed"
    assert decision["archive_late_high_exception_run_ids"] == "11"
