import json

from run_coordinate_objective_policy_matrix import policy_rows, summarize_report


def test_summarize_report_counts_cutoff_acceptance(tmp_path):
    report = {
        "aggregate": {
            "by_objective": {
                "highband": {
                    "margin_ratio_mean": 1.5,
                    "geometry_change_count": 0,
                }
            }
        },
        "objective_confidence_rows": [
            {
                "objective_label": "base",
                "is_truth_geometry": True,
                "confidence_label": "weak",
                "radius_margin_abs": 4.0e-4,
            },
            {
                "objective_label": "highband",
                "is_truth_geometry": True,
                "confidence_label": "moderate",
                "radius_margin_abs": 6.0e-4,
            },
        ],
    }
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    rows = summarize_report("targetX", path, cutoff=5.0e-4)

    base = next(row for row in rows if row["objective_label"] == "base")
    highband = next(row for row in rows if row["objective_label"] == "highband")
    assert base["accepted_count"] == 0
    assert base["margin_ratio_mean"] == 1.0
    assert highband["accepted_count"] == 1
    assert highband["accepted_fraction"] == 1.0
    assert highband["margin_ratio_mean"] == 1.5


def test_policy_rows_prefers_full_acceptance_then_margin_ratio():
    matrix_rows = [
        {
            "target_label": "targetX",
            "objective_label": "base",
            "accepted_fraction": 0.0,
            "margin_ratio_mean": 1.0,
            "radius_margin_abs_mean": 4.0e-4,
            "geometry_change_count": 0,
        },
        {
            "target_label": "targetX",
            "objective_label": "highband",
            "accepted_fraction": 1.0,
            "margin_ratio_mean": 1.4,
            "radius_margin_abs_mean": 6.0e-4,
            "geometry_change_count": 0,
        },
        {
            "target_label": "targetX",
            "objective_label": "late_high",
            "accepted_fraction": 1.0,
            "margin_ratio_mean": 1.7,
            "radius_margin_abs_mean": 7.0e-4,
            "geometry_change_count": 0,
        },
        {
            "target_label": "targetX",
            "objective_label": "veryhigh",
            "accepted_fraction": 1.0,
            "margin_ratio_mean": 1.8,
            "radius_margin_abs_mean": 8.0e-4,
            "geometry_change_count": 1,
        },
    ]

    rows = policy_rows(matrix_rows)

    assert rows[0]["full_acceptance_objectives"] == "highband, late_high"
    assert rows[0]["strongest_secondary_objective"] == "late_high"
