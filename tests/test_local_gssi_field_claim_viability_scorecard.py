from pathlib import Path

from run_local_gssi_field_claim_viability_scorecard import (
    build_claim_rows,
    summarize_claim_rows,
    write_figure_notes,
)


def _event_rows():
    return [
        {
            "tier_key": "short_supported_stack_intervals",
            "support_fraction": "1.0",
            "quality_metric_value": "0.909",
        },
        {
            "tier_key": "short_content_time_zero_anchors",
            "support_fraction": "0.6666666667",
            "quality_metric_value": "0.819",
        },
        {
            "tier_key": "long_stable_pattern_anchors",
            "support_fraction": "1.0",
            "quality_metric_value": "0.889",
        },
    ]


def _timing_rows():
    return [
        {
            "timing_discriminant": "short_content_relative",
            "support_fraction": "1.0",
            "representative_offset_ns": "0.127701",
            "strength_metric": "0.125151",
        },
        {
            "timing_discriminant": "raw_no_correction",
            "support_fraction": "0.0",
            "representative_offset_ns": "0.0",
            "strength_metric": "0.0",
        },
        {
            "timing_discriminant": "long_pattern_only",
            "support_fraction": "1.0",
            "representative_offset_ns": "0.06",
            "strength_metric": "0.150304",
        },
        {
            "timing_discriminant": "early_common_mode",
            "support_fraction": "1.0",
            "representative_offset_ns": "0.0",
            "strength_metric": "0.00003017",
        },
    ]


def _summaries():
    acquisition = {
        "ready_for_2d_qc": True,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "spatial_all_window_supported_fraction": 0.281124,
    }
    apparent_depth = {
        "ready_for_cover_depth_recovery": False,
        "max_corrected_depth_residual_mm": 4.908193,
        "time_zero_depth_equivalent_mm": 5.889832,
    }
    depth_sensitivity = {
        "cover_depth_claim_ready": False,
        "max_apparent_depth_span_mm": 149.915924,
    }
    degeneracy = {
        "radius_claim_ready": False,
        "max_near_top_time_zero_span_ns": 0.3,
    }
    cue_spacing = {
        "ready_for_field_context": True,
        "min_dataset_same_time_lateral_spacing_mm": 269.973,
        "synthetic_close_spacing_context_max_mm": 50.0,
    }
    dataset_card = {"profile_count": 4}
    publication_bundle = {
        "ready_for_manuscript_field_supplement": True,
        "figure_row_count": 20,
    }
    timing_summary = {
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
    }
    return (
        acquisition,
        apparent_depth,
        depth_sensitivity,
        degeneracy,
        cue_spacing,
        dataset_card,
        publication_bundle,
        timing_summary,
    )


def test_build_claim_rows_separates_supported_limited_and_blocked_claims():
    (
        acquisition,
        apparent_depth,
        depth_sensitivity,
        degeneracy,
        cue_spacing,
        dataset_card,
        publication_bundle,
        _timing_summary,
    ) = _summaries()

    rows = build_claim_rows(
        event_rows=_event_rows(),
        timing_rows=_timing_rows(),
        acquisition=acquisition,
        apparent_depth=apparent_depth,
        depth_sensitivity=depth_sensitivity,
        degeneracy=degeneracy,
        cue_spacing=cue_spacing,
        dataset_card=dataset_card,
        publication_bundle=publication_bundle,
    )
    by_key = {row["claim_key"]: row for row in rows}

    assert len(rows) == 13
    assert by_key["field_dataset_methods_2d_line_profiles"]["status"] == "supported"
    assert by_key["short_pair_relative_time_zero"]["support_score"] == 1.0
    assert by_key["raw_no_correction_control"]["status"] == "rejected_control"
    assert by_key["raw_no_correction_control"]["support_score"] == 1.0
    assert by_key["corrected_stack_supported_intervals"]["support_score"] == 0.281124
    assert by_key["field_cue_spacing_context"]["primary_metric_value"] == 269.973 / 50.0
    assert by_key["cover_depth_recovery"]["status"] == "blocked"
    assert by_key["radius_or_parametric_field_inversion"]["status"] == "blocked"
    assert by_key["field_publication_bundle_current"]["support_score"] == 1.0


def test_summarize_claim_rows_keeps_field_fwi_and_3d_blocked():
    (
        acquisition,
        apparent_depth,
        depth_sensitivity,
        degeneracy,
        cue_spacing,
        dataset_card,
        publication_bundle,
        timing_summary,
    ) = _summaries()
    rows = build_claim_rows(
        event_rows=_event_rows(),
        timing_rows=_timing_rows(),
        acquisition=acquisition,
        apparent_depth=apparent_depth,
        depth_sensitivity=depth_sensitivity,
        degeneracy=degeneracy,
        cue_spacing=cue_spacing,
        dataset_card=dataset_card,
        publication_bundle=publication_bundle,
    )
    summary = summarize_claim_rows(
        rows,
        acquisition=acquisition,
        timing_summary=timing_summary,
        cue_spacing=cue_spacing,
        apparent_depth=apparent_depth,
        depth_sensitivity=depth_sensitivity,
        degeneracy=degeneracy,
    )

    assert summary["policy_label"] == "local_gssi_field_claim_viability_scorecard_ready_no_field_fwi"
    assert summary["claim_row_count"] == 13
    assert summary["supported_count"] == 3
    assert summary["blocked_count"] == 3
    assert summary["ready_for_2d_field_qc"] is True
    assert summary["ready_for_absolute_time_zero"] is False
    assert summary["ready_for_cover_depth_recovery"] is False
    assert summary["ready_for_radius_recovery"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["scorecard_promoted_to_publication_bundle"] is False


def test_write_figure_notes_documents_scope_boundary(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "claim_viability",
        "claim_row_count": 13,
        "supported_count": 3,
        "scope_limited_count": 5,
        "blocked_count": 3,
        "ready_for_2d_field_qc": True,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("rows.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_gssi_field_claim_viability_scorecard.png" in text
    assert "absolute time-zero" in text
    assert "field FWI" in text
    assert "3D" in text
