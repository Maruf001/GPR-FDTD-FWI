from pathlib import Path

from run_synthetic_2d_archive_corpus_card import (
    range_rows,
    summarize_corpus,
    write_figure_notes,
)


def _archive_summary():
    return {
        "summary": {
            "run_count": 4,
            "by_range": {
                "001-002": {
                    "run_count": 2,
                    "category_counts": {
                        "physics_or_diagnostic": 2,
                        "analysis_report": 0,
                        "reporting_audit_checkpoint": 0,
                        "unclear": 0,
                    },
                    "with_data_dir": 2,
                    "with_figures_dir": 2,
                    "with_images": 2,
                    "with_figure_notes": 1,
                    "issue_count": 1,
                    "warning_count": 0,
                },
                "003-004": {
                    "run_count": 2,
                    "category_counts": {
                        "physics_or_diagnostic": 1,
                        "analysis_report": 1,
                        "reporting_audit_checkpoint": 0,
                        "unclear": 0,
                    },
                    "with_data_dir": 2,
                    "with_figures_dir": 2,
                    "with_images": 2,
                    "with_figure_notes": 2,
                    "issue_count": 0,
                    "warning_count": 0,
                },
            },
            "category_counts": {
                "physics_or_diagnostic": 3,
                "analysis_report": 1,
                "reporting_audit_checkpoint": 0,
                "unclear": 0,
            },
            "issue_counts": {
                "figure_images_missing_figure_notes": 1,
                "missing_run_manifest": 0,
            },
            "warning_counts": {"unclear_run_type": 0},
        }
    }


def test_range_rows_compute_note_coverage_by_archive_range():
    rows = range_rows(_archive_summary())

    assert rows[0]["range"] == "001-002"
    assert rows[0]["figure_note_coverage_fraction"] == 0.5
    assert rows[1]["range"] == "003-004"
    assert rows[1]["figure_note_coverage_fraction"] == 1.0


def test_summarize_corpus_ready_with_legacy_hygiene_caveat():
    rows = range_rows(_archive_summary())
    summary = summarize_corpus(
        rows,
        archive_summary=_archive_summary(),
        publication_summary={
            "ready_for_manuscript_draft": True,
            "figure_count": 9,
            "validated_figure_count": 9,
            "claim_boundary_count": 11,
            "gpu_priority": "none",
        },
        next_matrix_summary={
            "immediate_gpu_priority_count": 0,
            "conditional_gpu_candidate_count": 0,
            "gpu_priority": "none_now",
        },
        source_notes_summary={
            "ready_for_manuscript_handoff": True,
            "source_figure_count": 9,
            "notes_present_after_count": 9,
            "gpu_priority": "none",
        },
    )

    assert summary["policy_label"] == (
        "synthetic_2d_archive_corpus_card_current_ready_legacy_hygiene_caveats"
    )
    assert summary["archive_run_count"] == 4
    assert summary["physics_or_diagnostic_count"] == 3
    assert summary["archive_figure_note_coverage_fraction"] == 0.75
    assert summary["legacy_issue_count"] == 1
    assert summary["current_source_figure_notes_present"] == 9
    assert summary["gpu_priority"] == "none"
    assert summary["ready_for_methods_corpus_card"] is True


def test_write_figure_notes_blocks_broad_regeneration(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "corpus_ready",
        "archive_run_count": 1325,
        "physics_or_diagnostic_count": 802,
        "current_publication_figure_count": 9,
        "current_source_figure_notes_present": 9,
        "legacy_issue_count": 130,
        "gpu_priority": "none",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("ranges.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "synthetic_2d_archive_corpus_card.png" in text
    assert "does not run FDTD" in text
    assert "reason to regenerate old runs" in text
