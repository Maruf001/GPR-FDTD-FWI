from pathlib import Path

from run_gssi_field_publication_source_figure_notes_backfill import (
    DEFAULT_BUNDLE_RUN,
    backfill_source_notes,
    figure_notes_text,
    support_metric_text,
)


def _row(tmp_path: Path, figure_name: str = "field_source.png") -> dict:
    figure_path = tmp_path / "source_run" / "figures" / figure_name
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    figure_path.write_bytes(b"not-a-real-png")
    return {
        "figure_key": "field_source_qc",
        "source_run": "001_source",
        "figure_path": str(figure_path),
        "policy_label": "field_policy",
        "metric_label": "corr",
        "metric_value": "0.91",
        "allowed_use": "Use as field QC only.",
    }


def test_support_metric_text_uses_label_and_value():
    assert support_metric_text({"metric_label": "corr", "metric_value": "0.91"}) == "corr=0.91"
    assert support_metric_text({"support_metric": "gpu=none"}) == "gpu=none"


def test_default_bundle_run_tracks_current_signal_contrast_bundle():
    assert DEFAULT_BUNDLE_RUN == "133_gssi51600s_field_publication_claim_bundle_post_signal_contrast_sensitivity"


def test_figure_notes_text_records_scope_boundary(tmp_path):
    text = figure_notes_text(_row(tmp_path), dataset_id="dataset", bundle_run="098_bundle")

    assert "field_source.png" in text
    assert "098_bundle" in text
    assert "does not create calibrated cover-depth" in text


def test_backfill_source_notes_skip_existing(tmp_path):
    row = _row(tmp_path)
    notes_path = Path(row["figure_path"]).parent / "FIGURE_NOTES.md"
    notes_path.write_text("# Existing\n", encoding="utf-8")

    audit_rows, summary = backfill_source_notes(
        [row],
        dataset_id="dataset",
        bundle_run="098_bundle",
        refresh_existing=False,
    )

    assert audit_rows[0]["action"] == "skipped_existing"
    assert summary["skipped_existing_count"] == 1
    assert notes_path.read_text(encoding="utf-8") == "# Existing\n"


def test_backfill_source_notes_generates_missing_notes(tmp_path):
    row = _row(tmp_path)

    audit_rows, summary = backfill_source_notes(
        [row],
        dataset_id="dataset",
        bundle_run="098_bundle",
    )

    notes_path = Path(row["figure_path"]).parent / "FIGURE_NOTES.md"
    assert audit_rows[0]["action"] == "generated"
    assert summary["policy_label"] == "field_publication_source_figure_notes_backfill_complete_skip_existing"
    assert summary["ready_for_manuscript_handoff"] is True
    assert "field_source_qc" in notes_path.read_text(encoding="utf-8")


def test_backfill_source_notes_flags_missing_figure(tmp_path):
    row = _row(tmp_path)
    Path(row["figure_path"]).unlink()

    audit_rows, summary = backfill_source_notes(
        [row],
        dataset_id="dataset",
        bundle_run="098_bundle",
    )

    assert audit_rows[0]["action"] == "missing_figure"
    assert summary["policy_label"] == "field_publication_source_figure_notes_backfill_review_required"
    assert summary["ready_for_manuscript_handoff"] is False
