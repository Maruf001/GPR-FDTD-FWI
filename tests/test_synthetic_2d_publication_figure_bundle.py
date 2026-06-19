from run_synthetic_2d_publication_figure_bundle import (
    build_claim_boundary_rows,
    figure_status,
    summarize_bundle,
    write_figure_notes,
)


def test_figure_status_requires_nonblank_dynamic_figure():
    assert figure_status({"nonwhite_fraction": "0.2", "dynamic_range": "255"}) == "figure_validated"
    assert figure_status({"nonwhite_fraction": "0.0", "dynamic_range": "255"}) == "figure_needs_review"
    assert figure_status({"nonwhite_fraction": "0.2", "dynamic_range": "5"}) == "figure_needs_review"


def test_claim_boundaries_keep_field_and_synthetic_separate():
    rows = build_claim_boundary_rows()
    by_area = {row["claim_area"]: row for row in rows}

    assert "field_separation" in by_area
    assert "close50_legacy_branch" in by_area
    assert "reporting_tiers" in by_area
    assert "objective_uniqueness" in by_area
    assert "target2_close14_objective_limit" in by_area
    assert "target2_close50_linear29p5_seed_frequency" in by_area
    assert "known-truth synthetic confidence labels" in by_area["field_separation"]["not_allowed"]
    assert "Tx/Rx 40 branch" in by_area["close50_legacy_branch"]["not_allowed"]
    assert "0.5x ambiguity gate" in by_area["target2_close14_objective_limit"]["allowed_claim"]
    assert "29.5 mm" in by_area["target2_close50_linear29p5_seed_frequency"]["allowed_claim"]
    assert "broad GPU sweeps" in by_area["gpu_next_step"]["not_allowed"]


def test_summarize_bundle_marks_ready_when_all_figures_valid_and_gpu_none():
    rows = [
        {
            "figure_validation_status": "figure_validated",
            "support_metric": "gpu=none",
        },
        {
            "figure_validation_status": "figure_validated",
            "support_metric": "groups=15",
        },
    ]

    summary = summarize_bundle(rows, build_claim_boundary_rows())

    assert summary["policy_label"] == "synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none"
    assert summary["ready_for_manuscript_draft"] is True
    assert summary["gpu_priority"] == "none"
    assert summary["target1_current_policy_figures_included"] is False


def test_summarize_bundle_marks_target1_current_when_policy_figures_present():
    rows = [
        {
            "figure_key": "target1_acquisition_confidence_surface",
            "figure_validation_status": "figure_validated",
            "support_metric": "gpu=none",
        },
        {
            "figure_key": "target1_source_density_exception_map",
            "figure_validation_status": "figure_validated",
            "support_metric": "gpu=none",
        },
    ]

    summary = summarize_bundle(rows, build_claim_boundary_rows())

    assert summary["policy_label"] == "synthetic_2d_publication_bundle_current_resolution_target1_claims_ready_gpu_priority_none"
    assert summary["target1_current_policy_figures_included"] is True
    assert summary["detailed_claim_boundaries_included"] is True
    assert summary["ready_for_manuscript_draft"] is True


def test_summarize_bundle_not_ready_when_a_figure_needs_review():
    rows = [
        {
            "figure_validation_status": "figure_validated",
            "support_metric": "gpu=none",
        },
        {
            "figure_validation_status": "figure_needs_review",
            "support_metric": "groups=15",
        },
    ]

    summary = summarize_bundle(rows, build_claim_boundary_rows())

    assert summary["ready_for_manuscript_draft"] is False
    assert summary["validated_figure_count"] == 1


def test_write_figure_notes_documents_publication_bundle(tmp_path):
    summary = {
        "policy_label": "synthetic_policy",
        "validated_figure_count": 9,
        "figure_count": 9,
        "gpu_priority": "none",
    }
    notes_path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(
        notes_path,
        summary,
        tmp_path / "synthetic_2d_publication_figure_rows.csv",
        tmp_path / "synthetic_2d_publication_claim_boundaries.csv",
        tmp_path / "figure_validation.csv",
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "synthetic_2d_publication_figure_bundle.png" in text
    assert "synthetic_policy" in text
    assert "not a new FDTD" in text
