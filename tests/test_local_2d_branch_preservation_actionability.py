import csv
import json

from run_local_2d_branch_preservation_actionability import (
    build_actionability_rows,
    gate_rows,
    summarize_actionability,
)


def _write_candidate_csv(path):
    fieldnames = [
        "case_label",
        "misfit",
        "target_index",
        "x_mm",
        "z_mm",
        "radius_mm",
        "x_values_mm",
        "z_values_mm",
    ]
    rows = [
        {
            "case_label": "nominal",
            "misfit": 0.066,
            "target_index": 1,
            "x_mm": 252.0,
            "z_mm": 89.0,
            "radius_mm": 6.0,
            "x_values_mm": "[190.0, 252.0, 266.0]",
            "z_values_mm": "[90.0, 89.0, 91.0]",
        },
        {
            "case_label": "nominal",
            "misfit": 0.072,
            "target_index": 1,
            "x_mm": 250.0,
            "z_mm": 89.0,
            "radius_mm": 6.0,
            "x_values_mm": "[190.0, 250.0, 264.0]",
            "z_values_mm": "[90.0, 89.0, 91.0]",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_actionability_rows_compare_full_coordinate_error(tmp_path):
    run_dir = tmp_path / "001_case"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    candidate_csv = data_dir / "coordinate_step_01_target_1_candidates.csv"
    summary_json = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    _write_candidate_csv(candidate_csv)
    summary_json.write_text(
        json.dumps(
            {
                "run_name": "case",
                "true_x_values_mm": [190.0, 250.0, 264.0],
                "true_z_values_mm": [90.0, 90.0, 90.0],
                "steps": [
                    {"target_index": 1, "candidate_csv": str(candidate_csv)},
                    {"target_index": 2, "candidate_csv": "later.csv"},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    audit_rows = [
        {
            "source_summary_json": str(summary_json),
            "run_dir": "001_case",
            "run_name": "case",
            "target_index": "1",
            "case_label": "nominal",
            "candidate_csv": str(candidate_csv),
            "truth_x_mm": "250.0",
            "truth_lateral_retained_but_not_selected": "True",
        }
    ]

    rows = build_actionability_rows(audit_rows)

    assert len(rows) == 1
    assert rows[0]["best_candidate_linf_error_mm"] == 2.0
    assert rows[0]["truth_lateral_candidate_linf_error_mm"] == 1.0
    assert rows[0]["candidate_linf_improvement_mm"] == 1.0
    assert rows[0]["actionability_label"] == "candidate_for_narrow_coupled_probe"


def test_actionability_summary_keeps_gpu_blocked_without_specific_design(tmp_path):
    run_dir = tmp_path / "001_case"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    candidate_csv = data_dir / "coordinate_step_01_target_1_candidates.csv"
    summary_json = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    _write_candidate_csv(candidate_csv)
    summary_json.write_text(
        json.dumps(
            {
                "run_name": "case",
                "true_x_values_mm": [190.0, 250.0, 264.0],
                "true_z_values_mm": [90.0, 90.0, 90.0],
                "steps": [{"target_index": 1, "candidate_csv": str(candidate_csv)}],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    rows = build_actionability_rows(
        [
            {
                "source_summary_json": str(summary_json),
                "run_dir": "001_case",
                "run_name": "case",
                "target_index": "1",
                "case_label": "nominal",
                "candidate_csv": str(candidate_csv),
                "truth_x_mm": "250.0",
                "truth_lateral_retained_but_not_selected": "True",
            }
        ]
    )
    _, summary = summarize_actionability(rows)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["truth_lateral_improves_linf_count"] == 1
    assert summary["ready_for_branch_preservation_actionability_claim"] is True
    assert summary["ready_for_narrow_gpu_probe"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert gates["narrow_gpu_probe"]["ready"] is False
