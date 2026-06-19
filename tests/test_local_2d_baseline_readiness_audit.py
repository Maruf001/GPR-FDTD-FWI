from pathlib import Path

from run_local_2d_baseline_readiness_audit import (
    build_audit_rows,
    summarize_assignments,
    summarize_audit,
    summarize_single_detector,
    summarize_two_stage,
    write_figure_notes,
)


def test_summarize_single_detector_aggregates_hit_rate():
    summary = summarize_single_detector(
        [
            {"aggregate": {"scenario_count": 2, "detected_count": 2, "hit_count": 2, "max_x_error_mm": 4, "max_z_error_mm": 5}},
            {"aggregate": {"scenario_count": 2, "detected_count": 2, "hit_count": 1, "max_x_error_mm": 0, "max_z_error_mm": 10}},
        ]
    )

    assert summary["scenario_count"] == 4
    assert summary["detected_count"] == 4
    assert summary["hit_count"] == 3
    assert summary["hit_rate"] == 0.75
    assert summary["max_x_error_mm"] == 4
    assert summary["max_z_error_mm"] == 10


def test_summarize_two_stage_counts_exact_strong_and_weak_rows():
    rows = [
        {"x_error_mm": "0", "z_error_mm": "0", "radius_error_mm": "0", "confidence": "strong", "overall_wall_s": "10"},
        {"x_error_mm": "0", "z_error_mm": "0", "radius_error_mm": "0", "confidence": "weak", "overall_wall_s": "20"},
        {"x_error_mm": "1", "z_error_mm": "0", "radius_error_mm": "0", "confidence": "weak", "overall_wall_s": "30"},
    ]

    summary = summarize_two_stage(rows)

    assert summary["row_count"] == 3
    assert summary["exact_count"] == 2
    assert summary["exact_fraction"] == 2 / 3
    assert summary["strong_count"] == 1
    assert summary["weak_count"] == 2
    assert summary["max_wall_s"] == 30


def test_build_audit_rows_marks_contract_needed_without_gpu():
    single = {
        "scenario_count": 96,
        "detected_count": 96,
        "hit_count": 96,
        "hit_rate": 1.0,
        "detected_fraction": 1.0,
        "max_x_error_mm": 4,
        "max_z_error_mm": 10,
    }
    two_stage = {
        "row_count": 10,
        "exact_count": 10,
        "exact_fraction": 1.0,
        "strong_count": 3,
        "weak_count": 7,
        "weak_fraction": 0.7,
        "max_wall_s": 1514,
    }
    assignments = summarize_assignments(
        [
            {"count": 3, "assigned_rows": [{"normalized_score": 0.9}, {"normalized_score": 0.8}]},
            {"count": 3, "assigned_rows": [{"normalized_score": 0.7}]},
        ]
    )
    rows = build_audit_rows(
        single_detector=single,
        two_stage=two_stage,
        assignments=assignments,
        field_hyperbola={"apex_fit_count": 6},
        field_degeneracy={"surface_summary_row_count": 4, "max_near_top_time_zero_span_ns": 0.3},
        contribution_summary={
            "contribution_row_count": 10,
            "synthetic_immediate_gpu_priority_count": 0,
            "synthetic_conditional_gpu_candidate_count": 0,
        },
    )
    by_key = {row["baseline_key"]: row for row in rows}

    assert len(rows) == 6
    assert by_key["single_rebar_hyperbola_detector_location"]["status"] == "ready_location_baseline"
    assert by_key["single_rebar_hyperbola_detector_location"]["readiness_score"] == 1.0
    assert by_key["multi_rebar_detector_assignment_variable_depth_radius"]["primary_metric_value"] == 3.0
    assert by_key["field_hyperbola_timezero_degeneracy"]["status"] == "blocked_calibrated_field_baseline"
    assert by_key["current_synthetic_claim_baseline_gap"]["status"] == "contract_needed"
    assert by_key["current_synthetic_claim_baseline_gap"]["gpu_priority"] == "none"

    audit_summary = summarize_audit(rows, single, two_stage, assignments)
    assert audit_summary["policy_label"] == "local_2d_baseline_readiness_cpu_first_no_gpu"
    assert audit_summary["ready_baseline_count"] == 2
    assert audit_summary["partial_baseline_count"] == 1
    assert audit_summary["immediate_gpu_priority_count"] == 0
    assert audit_summary["conditional_gpu_candidate_count"] == 0


def test_write_figure_notes_documents_cpu_only_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "baseline_ready",
        "baseline_row_count": 6,
        "ready_baseline_count": 2,
        "single_detector_scenario_count": 96,
        "single_detector_hit_rate": 1.0,
        "two_stage_exact_fraction": 1.0,
        "immediate_gpu_priority_count": 0,
        "conditional_gpu_candidate_count": 0,
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_2d_baseline_readiness_audit.png" in text
    assert "does not run detector" in text
    assert "3D/HPC" in text
