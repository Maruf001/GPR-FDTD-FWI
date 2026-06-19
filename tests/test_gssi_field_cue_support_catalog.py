from pathlib import Path

from run_gssi_field_cue_support_catalog import (
    build_catalogs,
    find_nearest_cue,
    summarize_catalogs,
    write_figure_notes,
)


def _cue_rows():
    return [
        {
            "file": "PROJECT001C__014.DZT",
            "x_m": "0.100000",
            "time_ns": "0.50",
            "approx_depth_m": "0.05",
            "relative_strength": "10",
        },
        {
            "file": "PROJECT001C__016.DZT",
            "x_m": "0.110000",
            "time_ns": "0.70",
            "approx_depth_m": "0.07",
            "relative_strength": "9",
        },
        {
            "file": "PROJECT001C__015.DZT",
            "x_m": "1.000000",
            "time_ns": "2.70",
            "approx_depth_m": "0.27",
            "relative_strength": "8",
        },
    ]


def _short_event_rows():
    return [
        {
            "file": "PROJECT001C__014.DZT",
            "apex_group": "1",
            "x_m": "0.100000",
            "current_cue_time_ns": "0.50",
        },
        {
            "file": "PROJECT001C__016.DZT",
            "apex_group": "1",
            "x_m": "0.110000",
            "current_cue_time_ns": "0.70",
        },
    ]


def _short_pair_rows():
    return [
        {
            "pair_index": "1",
            "reference_file": "PROJECT001C__014.DZT",
            "comparison_file": "PROJECT001C__016.DZT",
            "reference_apex_group": "1",
            "comparison_apex_group": "1",
            "reference_x_m": "0.100000",
            "comparison_aligned_x_m": "0.110000",
            "aligned_x_residual_mm": "10",
            "comparison_minus_reference_phase_time_ns": "0.12",
        }
    ]


def _short_anchor_rows():
    return [
        {
            "pair_index": "1",
            "content_backed": "True",
            "anchor_policy_label": "content_time_zero_anchor_supported",
            "reference_x_mm": "100",
            "comparison_aligned_x_mm": "110",
            "aligned_x_residual_mm": "10",
            "comparison_minus_reference_phase_time_ns": "0.12",
            "pair_min_absolute_correlation": "0.9",
        }
    ]


def _long_rows():
    return [
        {
            "anchor_index": "2",
            "center_x_mm": "1000",
            "stability_label": "stable_stack_anchor",
            "pattern_shift_abs_correlation_gain": "0.2",
            "support_label": "supported",
            "is_supported": "True",
        }
    ]


def test_find_nearest_cue_prefers_same_file_and_time():
    idx, residual_x_mm, residual_time_ns = find_nearest_cue(
        _cue_rows(),
        "PROJECT001C__016.DZT",
        0.1095,
        0.71,
    )

    assert idx == 1
    assert round(residual_x_mm, 3) == 0.5
    assert round(residual_time_ns, 3) == 0.01


def test_build_catalogs_separates_raw_cues_and_support_anchors():
    cue_catalog, support_catalog = build_catalogs(
        cue_rows=_cue_rows(),
        short_event_rows=_short_event_rows(),
        short_pair_rows=_short_pair_rows(),
        short_anchor_rows=_short_anchor_rows(),
        long_holdout_rows=_long_rows(),
    )
    cue_by_file = {row["file"]: row for row in cue_catalog}
    support_by_id = {row["support_anchor_id"]: row for row in support_catalog}

    assert len(cue_catalog) == 3
    assert len(support_catalog) == 2
    assert cue_by_file["PROJECT001C__014.DZT"]["support_category"] == "short_content_backed_time_zero_anchor"
    assert cue_by_file["PROJECT001C__016.DZT"]["support_pair_index"] == 1
    assert cue_by_file["PROJECT001C__015.DZT"]["support_category"] == "long_profile_context_cue_only"
    assert support_by_id["short_pair_1"]["is_claim_supporting"] is True
    assert support_by_id["long_anchor_2"]["support_category"] == "long_stable_pattern_only_anchor"


def test_summary_keeps_field_inversion_flags_false():
    cue_catalog, support_catalog = build_catalogs(
        cue_rows=_cue_rows(),
        short_event_rows=_short_event_rows(),
        short_pair_rows=_short_pair_rows(),
        short_anchor_rows=_short_anchor_rows(),
        long_holdout_rows=_long_rows(),
    )
    summary = summarize_catalogs(
        cue_catalog,
        support_catalog,
        timing_rows=[{"timing_discriminant": "short"}],
        event_support_summary={
            "tier_row_count": 11,
            "short_content_anchor_support_fraction": 2 / 3,
            "long_pattern_total_supported_anchor_count": 8,
            "hpc_dimensionality_field_geometry_type": "independent_2d_line_profiles",
        },
        policy_summary={"publication_claim_bundle_ready": True},
    )

    assert summary["policy_label"] == "gssi51600s_field_cue_support_catalog_2d_qc_not_inversion"
    assert summary["raw_cue_count"] == 3
    assert summary["support_anchor_count"] == 2
    assert summary["short_content_backed_anchor_count"] == 1
    assert summary["ready_for_2d_qc"] is True
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
    assert summary["gpu_priority"] == "none"


def test_write_figure_notes_documents_scope(tmp_path):
    notes_path = tmp_path / "FIGURE_NOTES.md"
    summary = {
        "policy_label": "field_catalog",
        "raw_cue_count": 19,
        "support_anchor_count": 11,
        "short_content_backed_anchor_count": 2,
        "short_timing_only_cue_count": 1,
        "long_pattern_total_supported_anchor_count": 8,
        "gpu_priority": "none",
    }

    write_figure_notes(
        notes_path,
        summary,
        Path("cue.csv"),
        Path("support.csv"),
        Path("summary.json"),
        Path("validation.csv"),
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "field_cue_support_catalog.png" in text
    assert "does not run" in text
    assert "known-truth field rebar labels" in text
