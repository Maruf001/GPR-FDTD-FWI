from pathlib import Path

from run_local_2d_target1_probe_readiness_scorecard import (
    build_probe_rows,
    find_surface_row,
    summarize_probe_rows,
    write_figure_notes,
)


def _acquisition_summary():
    return {
        "target1_canonical_row_count": 10,
        "target1_exact_geometry_count": 10,
        "target1_base_weak_exact_count": 3,
        "target1_late_high_accepted_count": 10,
        "source_density_escalation_helped_count": 4,
        "source_density_lower_count_best_count": 3,
    }


def _exception_summary(modern_exceptions=0):
    return {
        "source_density_series_count": 7,
        "modern_exception_series_count": modern_exceptions,
        "legacy_exception_series_count": 1,
        "terminal_11_series_count": 2,
        "terminal_11_worse_count": 2,
        "all_base_weak_series_count": 1,
    }


def _weak_subset_rows():
    return [
        {
            "subset": "ringdown050",
            "weak_exact_row_count": "3",
            "late_high_accepted_count": "3",
        }
    ]


def _surface_rows():
    return [
        {
            "group_type": "txrx_offset",
            "setting": "60",
            "row_count": "8",
            "accepted_fraction": "0.75",
            "late_high_accepted_count": "8",
        },
        {
            "group_type": "source_count",
            "setting": "5",
            "row_count": "9",
            "accepted_fraction": "0.8",
            "late_high_accepted_count": "9",
        },
    ]


def test_find_surface_row_matches_group_and_float_setting():
    row = find_surface_row(_surface_rows(), "txrx_offset", 60.0)

    assert row["accepted_fraction"] == "0.75"
    assert find_surface_row(_surface_rows(), "txrx_offset", 55.0) == {}


def test_probe_scorecard_marks_current_evidence_no_gpu():
    rows = build_probe_rows(
        acquisition_summary=_acquisition_summary(),
        exception_summary=_exception_summary(),
        next_matrix_summary={"candidate_count": 10, "immediate_gpu_priority_count": 0, "conditional_gpu_candidate_count": 0},
        weak_subset_rows=_weak_subset_rows(),
        surface_rows=_surface_rows(),
        source_branch_rows=[{"series_id": "a"}],
        exception_branch_rows=[{"series_id": "a"}],
    )
    by_key = {row["gate_key"]: row for row in rows}

    assert len(rows) == 10
    assert by_key["geometry_stability"]["triggered"] is False
    assert by_key["base_margin_weak_exact"]["status"] == "manuscript_confidence_policy"
    assert by_key["source_density_monotonic_rescue"]["status"] == "do_not_extend_source_density"
    assert by_key["global_next_question_matrix"]["gpu_action"] == "none"

    summary = summarize_probe_rows(rows, _acquisition_summary(), _exception_summary())
    assert summary["policy_label"] == "local_2d_target1_probe_readiness_requires_new_hypothesis"
    assert summary["ready_for_target1_gpu_probe"] is False
    assert summary["gpu_action_count"] == 0
    assert summary["gpu_priority"] == "none"


def test_modern_exception_or_geometry_failure_triggers_review():
    acquisition = _acquisition_summary()
    acquisition["target1_exact_geometry_count"] = 9
    exception = _exception_summary(modern_exceptions=1)
    rows = build_probe_rows(
        acquisition_summary=acquisition,
        exception_summary=exception,
        next_matrix_summary={"candidate_count": 10, "immediate_gpu_priority_count": 0, "conditional_gpu_candidate_count": 0},
        weak_subset_rows=_weak_subset_rows(),
        surface_rows=_surface_rows(),
        source_branch_rows=[{"series_id": "a"}],
        exception_branch_rows=[{"series_id": "a"}],
    )

    summary = summarize_probe_rows(rows, acquisition, exception)

    assert summary["ready_for_target1_gpu_probe"] is True
    assert summary["gpu_priority"] == "review_before_gpu"
    assert summary["triggered_gate_count"] >= 2


def test_write_figure_notes_documents_no_execution_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "probe_readiness",
        "scorecard_row_count": 10,
        "triggered_gate_count": 0,
        "gpu_action_count": 0,
        "ready_for_target1_gpu_probe": False,
        "modern_exception_series_count": 0,
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "target1 GPU-probe gates" in text
    assert "does not run" in text
    assert "3D/HPC" in text
