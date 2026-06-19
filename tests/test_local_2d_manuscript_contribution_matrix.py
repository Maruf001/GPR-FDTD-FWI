from pathlib import Path

from run_local_2d_manuscript_contribution_matrix import (
    DEFAULT_SYNTHETIC_NEXT_RUN,
    build_contribution_rows,
    summarize_contributions,
    write_figure_notes,
)


def _synthetic_claims():
    return [
        {
            "claim_area": "resolution_limit",
            "allowed_claim": "Use the current resolution-claim map.",
            "not_allowed": "Do not present a universal spacing limit.",
        },
        {
            "claim_area": "reporting_tiers",
            "allowed_claim": "Report exact-strong, geometry-clean, and objective-unique tiers.",
            "not_allowed": "Do not collapse exact-strong into paper-clean claims.",
        },
        {
            "claim_area": "target2_close14_objective_limit",
            "allowed_claim": "Truth is selected strongly in 6 / 6 rows.",
            "not_allowed": "Do not describe this branch as objective-unique.",
        },
        {
            "claim_area": "target2_close50_linear29p5_seed_frequency",
            "allowed_claim": "Exact and strong in 6 / 6 rows, clean in 2 / 3 seeds.",
            "not_allowed": "Do not promote 29.5 mm to a clean replicated threshold.",
        },
        {
            "claim_area": "target1_acquisition_confidence",
            "allowed_claim": "Use target1 as acquisition-sensitive confidence evidence.",
            "not_allowed": "Do not claim source escalation is generally monotonic.",
        },
    ]


def _synthetic_next_rows():
    return [
        {
            "question_key": "synthetic_publication_bundle_current",
            "gpu_readiness": "no_gpu_required",
            "gpu_priority": "none",
        },
        {
            "question_key": "target1_acquisition_confidence_surface_current",
            "gpu_readiness": "no_gpu_required",
            "gpu_priority": "none",
        },
    ]


def _cross_domain_rows():
    return [
        {
            "scope_key": "field_timing_window_family_boundary",
            "allowed_joint_claim": "Field timing windows support scoped timing/repeatability.",
        },
        {
            "scope_key": "current_no_gpu_queue",
            "allowed_joint_claim": "Current manuscript tables are ready without a local GPU run.",
        },
    ]


def _field_rows():
    return [
        {
            "claim_key": "field_dataset_methods_2d_line_profiles",
            "status": "supported",
            "support_score": "1.0",
        },
        {
            "claim_key": "short_pair_relative_time_zero",
            "status": "supported",
            "support_score": "1.0",
        },
    ]


def _matched_source3_summary():
    return {
        "guarded_acquisition_geometry_contrast_ready": True,
        "close14_truth_geometry_fraction": 1.0,
        "close50_truth_geometry_fraction": 0.0,
        "close50_replicated_wrong_branch": True,
        "spacing_only_causal_generalization_ready": False,
    }


def test_default_synthetic_next_matrix_uses_matched_source3_refresh():
    assert DEFAULT_SYNTHETIC_NEXT_RUN == "1356_synthetic_2d_next_question_matrix_post_matched_source3_policy"


def test_build_contribution_rows_marks_ready_and_deferred_paths():
    rows = build_contribution_rows(
        synthetic_claims=_synthetic_claims(),
        synthetic_next_rows=_synthetic_next_rows(),
        cross_domain_rows=_cross_domain_rows(),
        field_viability_rows=_field_rows(),
        field_viability_summary={
            "claim_row_count": 13,
            "ready_for_manuscript_field_claim_viability": True,
        },
        synthetic_bundle_summary={"figure_count": 9, "claim_boundary_count": 11},
        synthetic_corpus_summary={"archive_run_count": 1325},
        matched_source3_summary=_matched_source3_summary(),
        literature_matrix_exists=True,
        neural_triage_exists=True,
    )
    by_key = {row["contribution_key"]: row for row in rows}

    assert len(rows) == 11
    assert by_key["controlled_close_spacing_resolution_map"]["readiness"] == "ready"
    assert by_key["matched_source3_acquisition_geometry_contrast"]["readiness"] == "ready"
    assert "close50 truth fraction=0.0" in by_key["matched_source3_acquisition_geometry_contrast"]["current_evidence"]
    assert by_key["field_2d_qc_supplement"]["readiness"] == "ready"
    assert "2D QC status=supported" in by_key["field_2d_qc_supplement"]["current_evidence"]
    assert by_key["neural_network_baseline_not_current_path"]["readiness"] == "deferred"
    assert by_key["current_no_gpu_queue"]["gpu_priority"] == "none"


def test_summarize_contributions_keeps_no_gpu_policy():
    rows = build_contribution_rows(
        synthetic_claims=_synthetic_claims(),
        synthetic_next_rows=_synthetic_next_rows(),
        cross_domain_rows=_cross_domain_rows(),
        field_viability_rows=_field_rows(),
        field_viability_summary={
            "claim_row_count": 13,
            "ready_for_manuscript_field_claim_viability": True,
        },
        synthetic_bundle_summary={"figure_count": 9, "claim_boundary_count": 11},
        synthetic_corpus_summary={"archive_run_count": 1325},
        matched_source3_summary=_matched_source3_summary(),
        literature_matrix_exists=True,
        neural_triage_exists=True,
    )
    summary = summarize_contributions(
        rows,
        field_summary={
            "ready_for_manuscript_field_claim_viability": True,
            "ready_for_2d_field_qc": True,
            "ready_for_field_fwi": False,
            "ready_for_3d_hpc": False,
        },
        synthetic_next_rows=_synthetic_next_rows(),
    )

    assert summary["policy_label"] == "local_2d_manuscript_contribution_matrix_ready_no_gpu"
    assert summary["contribution_row_count"] == 11
    assert summary["ready_count"] == 10
    assert summary["deferred_count"] == 1
    assert summary["synthetic_immediate_gpu_priority_count"] == 0
    assert summary["synthetic_conditional_gpu_candidate_count"] == 0
    assert summary["field_ready_for_fwi"] is False
    assert summary["field_ready_for_3d_hpc"] is False


def test_write_figure_notes_records_no_training_or_hpc_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "contribution_matrix_ready",
        "contribution_row_count": 10,
        "ready_count": 9,
        "deferred_count": 1,
        "synthetic_immediate_gpu_priority_count": 0,
        "synthetic_conditional_gpu_candidate_count": 0,
        "field_ready_for_fwi": False,
        "field_ready_for_3d_hpc": False,
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_2d_manuscript_contribution_matrix.png" in text
    assert "neural-network training" in text
    assert "3D/HPC" in text
