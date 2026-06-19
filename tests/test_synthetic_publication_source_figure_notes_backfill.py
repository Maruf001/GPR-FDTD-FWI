from pathlib import Path

from run_synthetic_publication_source_figure_notes_backfill import (
    backfill_source_notes,
    figure_notes_text,
    support_metric_text,
)


def _row(tmp_path: Path, figure_name: str = "synthetic_source.png") -> dict:
    figure_path = tmp_path / "source_run" / "figures" / figure_name
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    figure_path.write_bytes(b"not-a-real-png")
    return {
        "figure_key": "synthetic_source_qc",
        "source_run": "1320_source",
        "figure_path": str(figure_path),
        "status_label": "paper_ready",
        "support_metric": "gpu=none",
        "paper_use": "Use as synthetic policy support.",
        "allowed_claim": "Allowed synthetic claim.",
        "prohibited_claim": "Do not overclaim.",
    }


def test_support_metric_text_prefers_support_metric():
    assert support_metric_text({"support_metric": "gpu=none"}) == "gpu=none"
    assert support_metric_text({}) == "not recorded"


def test_figure_notes_text_records_synthetic_scope(tmp_path):
    text = figure_notes_text(_row(tmp_path), bundle_run="1322_bundle")

    assert "synthetic_source.png" in text
    assert "1322_bundle" in text
    assert "controlled known-truth synthetic 2D evidence" in text


def test_backfill_source_notes_skip_existing(tmp_path):
    row = _row(tmp_path)
    notes_path = Path(row["figure_path"]).parent / "FIGURE_NOTES.md"
    notes_path.write_text("# Existing\n", encoding="utf-8")

    audit_rows, summary = backfill_source_notes(
        [row],
        bundle_run="1322_bundle",
        refresh_existing=False,
    )

    assert audit_rows[0]["action"] == "skipped_existing"
    assert summary["skipped_existing_count"] == 1
    assert notes_path.read_text(encoding="utf-8") == "# Existing\n"


def test_backfill_source_notes_generates_missing_notes(tmp_path):
    row = _row(tmp_path)

    audit_rows, summary = backfill_source_notes([row], bundle_run="1322_bundle")

    notes_path = Path(row["figure_path"]).parent / "FIGURE_NOTES.md"
    assert audit_rows[0]["action"] == "generated"
    assert summary["policy_label"] == "synthetic_publication_source_figure_notes_backfill_complete_skip_existing"
    assert summary["ready_for_manuscript_handoff"] is True
    assert "synthetic_source_qc" in notes_path.read_text(encoding="utf-8")


def test_backfill_source_notes_flags_missing_figure(tmp_path):
    row = _row(tmp_path)
    Path(row["figure_path"]).unlink()

    audit_rows, summary = backfill_source_notes([row], bundle_run="1322_bundle")

    assert audit_rows[0]["action"] == "missing_figure"
    assert summary["policy_label"] == "synthetic_publication_source_figure_notes_backfill_review_required"
    assert summary["ready_for_manuscript_handoff"] is False
