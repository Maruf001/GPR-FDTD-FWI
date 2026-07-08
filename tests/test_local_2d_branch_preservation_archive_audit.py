import csv

from run_local_2d_branch_preservation_archive_audit import (
    audit_candidate_step,
    gate_rows,
    summarize_archive,
    summarize_by_target,
)


def _write_candidates(path):
    fieldnames = ["case_label", "misfit", "target_index", "x_mm", "z_mm", "radius_mm"]
    rows = [
        {"case_label": "nominal", "misfit": 0.066, "target_index": 1, "x_mm": 252.0, "z_mm": 89.0, "radius_mm": 6.0},
        {"case_label": "nominal", "misfit": 0.072, "target_index": 1, "x_mm": 250.0, "z_mm": 89.0, "radius_mm": 6.0},
        {"case_label": "nominal", "misfit": 0.090, "target_index": 1, "x_mm": 248.0, "z_mm": 91.0, "radius_mm": 6.0},
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_audit_candidate_step_flags_retained_truth_lateral_not_selected(tmp_path):
    run_dir = tmp_path / "001_case"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    candidate_csv = data_dir / "candidates.csv"
    summary_path = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    _write_candidates(candidate_csv)

    summary = {
        "run_name": "case",
        "update_case_label": "nominal",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
    }
    step = {"target_index": 1, "candidate_csv": str(candidate_csv)}

    row = audit_candidate_step(
        summary_path,
        summary,
        step,
        abs_gap_cutoff=0.01,
        rel_gap_cutoff=0.10,
    )

    assert row["audited"] is True
    assert row["selected_truth_lateral"] is False
    assert row["truth_lateral_available"] is True
    assert row["truth_lateral_retained_by_rule"] is True
    assert row["truth_lateral_retained_but_not_selected"] is True
    assert round(row["truth_lateral_gap_abs"], 6) == 0.006


def test_summarize_archive_keeps_gpu_and_fwi_blocked(tmp_path):
    run_dir = tmp_path / "001_case"
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True)
    candidate_csv = data_dir / "candidates.csv"
    summary_path = data_dir / "multi_rebar_coordinate_optimizer_summary.json"
    _write_candidates(candidate_csv)
    summary = {
        "run_name": "case",
        "update_case_label": "nominal",
        "true_x_values_mm": [190.0, 250.0, 264.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
    }
    step = {"target_index": 1, "candidate_csv": str(candidate_csv)}
    rows = [
        audit_candidate_step(
            summary_path,
            summary,
            step,
            abs_gap_cutoff=0.01,
            rel_gap_cutoff=0.10,
        )
    ]

    target_rows = summarize_by_target(rows)
    archive_summary = summarize_archive(rows, target_rows, abs_gap_cutoff=0.01, rel_gap_cutoff=0.10)
    gates = {row["gate_key"]: row for row in gate_rows(archive_summary)}

    assert archive_summary["retained_but_not_selected_count"] == 1
    assert archive_summary["ready_for_branch_preservation_policy_claim"] is True
    assert archive_summary["ready_for_broad_gpu_queue"] is False
    assert archive_summary["ready_for_detector_seeded_fwi"] is False
    assert gates["broad_gpu_queue"]["ready"] is False
    assert gates["detector_seeded_fwi"]["ready"] is False
