from run_local_2d_field_manuscript_evidence_audit import (
    audit_claim_rows,
    figure_validated,
    required_claims_present,
    summarize_audit,
    write_figure_notes,
)


def test_figure_validated_requires_content_and_dynamic_range():
    assert figure_validated({"nonwhite_fraction": 0.20, "dynamic_range": 255, "width": 900, "height": 400})
    assert not figure_validated({"nonwhite_fraction": 0.01, "dynamic_range": 255, "width": 900, "height": 400})
    assert not figure_validated({"nonwhite_fraction": 0.20, "dynamic_range": 5, "width": 900, "height": 400})
    assert not figure_validated({"nonwhite_fraction": 0.20, "dynamic_range": 255, "width": 20, "height": 400})


def test_required_claims_present_for_current_bundles():
    synthetic_rows = [
        {"claim_area": key, "allowed_claim": "allowed", "not_allowed": "blocked"}
        for key in [
            "resolution_limit",
            "close50_legacy_branch",
            "confidence_policy",
            "reporting_tiers",
            "objective_uniqueness",
            "target_specificity",
            "target1_acquisition_confidence",
            "target2_close14_objective_limit",
            "target2_close50_linear29p5_seed_frequency",
            "gpu_next_step",
            "field_separation",
        ]
    ]
    field_rows = [
        {"claim_area": key, "allowed_claim": "allowed", "not_allowed": "blocked"}
        for key in [
            "field_geometry",
            "short_profile_timing",
            "long_profile_pattern",
            "synthetic_separation",
            "gpu_next_step",
            "field_time_zero_uncertainty_budget",
            "field_early_time_anchor_negative_qc",
            "field_timing_anchor_conflict",
            "field_timing_window_family_classification",
            "field_cue_spacing_context",
            "field_acquisition_readiness",
            "field_hyperbola_timezero_degeneracy",
        ]
    ]

    assert required_claims_present("synthetic_2d", synthetic_rows)
    assert required_claims_present("field_2d", field_rows)


def test_audit_claim_rows_marks_complete_boundaries():
    rows = audit_claim_rows(
        "synthetic_2d",
        [
            {"claim_area": "resolution_limit", "allowed_claim": "allowed", "not_allowed": "blocked"},
            {"claim_area": "gpu_next_step", "allowed_claim": "allowed", "not_allowed": ""},
        ],
    )

    assert rows[0]["boundary_complete"] is True
    assert rows[0]["required_for_current_package"] is True
    assert rows[1]["boundary_complete"] is False


def test_summarize_audit_ready_when_domains_figures_claims_and_guards_are_ready():
    domain_rows = [
        {
            "domain": "synthetic_2d",
            "manuscript_ready": True,
            "gpu_priority": "none",
            "endpoint_gpu_priority": "none_now",
            "bundle_figure_validated": True,
        },
        {
            "domain": "field_2d",
            "manuscript_ready": True,
            "gpu_priority": "none",
            "endpoint_gpu_priority": "none",
            "bundle_figure_validated": True,
        },
    ]
    figure_rows = [
        {"domain": "synthetic_2d", "figure_validated": True},
        {"domain": "field_2d", "figure_validated": True},
    ]
    claim_rows = [
        {"domain": "synthetic_2d", "claim_area": "field_separation", "boundary_complete": True},
        {"domain": "field_2d", "claim_area": "synthetic_separation", "boundary_complete": True},
    ]

    summary = summarize_audit(domain_rows, figure_rows, claim_rows)

    assert summary["policy_label"] == "local_2d_field_manuscript_evidence_ready_no_gpu"
    assert summary["ready_for_manuscript_planning"] is True
    assert summary["gpu_priority"] == "none"


def test_write_figure_notes_documents_evidence_audit(tmp_path):
    summary = {
        "policy_label": "audit_policy",
        "validated_figure_file_count": 28,
        "figure_audit_row_count": 28,
        "claim_boundary_row_count": 29,
        "gpu_priority": "none",
    }
    notes_path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(
        notes_path,
        summary,
        tmp_path / "domain.csv",
        tmp_path / "figures.csv",
        tmp_path / "claims.csv",
        tmp_path / "figure_validation.csv",
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_2d_field_manuscript_evidence_audit.png" in text
    assert "audit_policy" in text
    assert "does not create new physics evidence" in text
