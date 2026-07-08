from run_gssi_field_publication_claim_bundle import (
    claim_boundary_rows,
    figure_rows,
    relaxed_phase_anchor_policy,
    summarize_bundle,
    write_figure_notes,
)


def _summaries():
    return {
        "geometry": {
            "classification": "independent_2d_line_profiles",
            "profile_count": 4,
            "paths": {"plot": "geometry.png"},
        },
        "short_waveform": {
            "policy_label": "content_backed_waveform_visual_qc",
            "min_absolute_correlation": 0.82,
            "paths": {"figure": "short_waveform.png"},
        },
        "short_stack": {
            "policy_label": "supported_interval_visual_qc_ready",
            "min_corrected_interval_abs_correlation": 0.91,
            "paths": {"figure": "short_stack.png"},
        },
        "long_visual": {
            "policy_label": "long_profile_pattern_visual_qc_ready",
            "min_pattern_shift_abs_correlation": 0.89,
            "paths": {"figure": "long_visual.png"},
        },
        "long_holdout": {
            "policy_label": "long_profile_pattern_holdout_qc_all_candidate_anchors_supported",
            "repeat_limited_supported_anchor_count": 2,
            "paths": {"figure": "long_holdout.png"},
        },
        "long_window_sensitivity": {
            "policy_label": "long_profile_pattern_holdout_sensitivity_all_candidate_anchors_all_windows_supported",
            "candidate_anchor_count": 8,
            "all_window_supported_anchor_count": 8,
            "paths": {"figure": "long_window_sensitivity.png"},
        },
        "long_width_sensitivity": {
            "policy_label": "long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported",
            "candidate_anchor_count": 8,
            "all_width_supported_anchor_count": 8,
            "paths": {"figure": "long_width_sensitivity.png"},
        },
        "bandlimited_repeatability": {
            "policy_label": "field_bandlimited_repeatability_short_pair_supported_long_pattern_only",
            "short_supported_band_count": 4,
            "long_pattern_supported_band_count": 4,
            "paths": {"figure": "bandlimited.png"},
        },
    }


def test_figure_rows_include_field_claim_sources():
    rows = figure_rows(_summaries())
    keys = [row["figure_key"] for row in rows]

    assert keys == [
        "survey_geometry_boundary",
        "short_content_waveform_qc",
        "short_supported_stack_intervals",
        "long_pattern_visual_qc",
        "long_pattern_holdout_qc",
        "long_pattern_window_sensitivity",
        "long_pattern_width_sensitivity",
        "field_bandlimited_repeatability_qc",
    ]
    assert rows[0]["metric_value"] == 4
    assert rows[4]["metric_value"] == 2
    assert rows[-3]["metric_value"] == 8
    assert rows[-2]["metric_value"] == 8
    assert rows[-1]["metric_value"] == 4
    assert rows[-1]["figure_path"] == "bandlimited.png"


def test_write_figure_notes_documents_field_bundle(tmp_path):
    summary = {
        "policy_label": "field_policy",
        "figure_row_count": 19,
        "claim_boundary_count": 18,
        "geometry_classification": "independent_2d_line_profiles",
        "gpu_priority": "none",
    }
    notes_path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(
        notes_path,
        summary,
        tmp_path / "field_publication_figure_rows.csv",
        tmp_path / "field_publication_claim_boundaries.csv",
        tmp_path / "figure_validation.csv",
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "field_publication_claim_bundle.png" in text
    assert "field_policy" in text
    assert "does not establish a 3D survey" in text


def test_claim_boundary_rows_preserve_not_fwi_boundary():
    claims = claim_boundary_rows(bandlimited_repeatability_summary={"policy_label": "band"})
    text = " ".join(row["not_allowed"] for row in claims)

    assert len(claims) == 7
    assert "field FWI/3D" in text
    assert "synthetic optimizer" in text
    assert "absolute phase-anchor" in text
    assert "band-limited repeatability" in text


def test_relaxed_phase_anchor_adds_negative_qc_bundle_row():
    relaxed_summary = {
        "phase_anchor_pick_count": 10,
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {"boundary_solution_count": 1},
        "figures": {"convention_summary": "relaxed_summary.png"},
    }
    summaries = {**_summaries(), "long_relaxed_phase_anchor": relaxed_summary}

    rows = figure_rows(summaries)
    claims = claim_boundary_rows(relaxed_summary)
    by_key = {row["figure_key"]: row for row in rows}

    assert relaxed_phase_anchor_policy(relaxed_summary) == "long_profile_relaxed_phase_anchor_low_snr_not_time_zero"
    assert by_key["long_relaxed_phase_anchor_negative_qc"]["metric_value"] == 10
    assert by_key["long_relaxed_phase_anchor_negative_qc"]["figure_path"] == "relaxed_summary.png"
    assert claims[-1]["claim_area"] == "long_relaxed_phase_anchor"
    assert "absolute time-zero" in claims[-1]["not_allowed"]


def test_summarize_bundle_marks_ready_for_2d_qc_not_fwi():
    figures = figure_rows(_summaries())
    claims = claim_boundary_rows(bandlimited_repeatability_summary=_summaries()["bandlimited_repeatability"])
    summary = summarize_bundle(figures, claims, _summaries())

    assert summary["policy_label"] == "field_publication_claim_bundle_2d_qc_bandlimited_ready_not_fwi"
    assert summary["figure_row_count"] == 8
    assert summary["claim_boundary_count"] == 7
    assert summary["geometry_classification"] == "independent_2d_line_profiles"
    assert summary["long_window_sensitivity_ready"] is True
    assert summary["long_width_sensitivity_ready"] is True
    assert summary["bandlimited_repeatability_included"] is True
    assert summary["bandlimited_short_supported_band_count"] == 4
    assert summary["gpu_priority"] == "none"
    assert summary["ready_for_manuscript_field_supplement"] is True


def test_summarize_bundle_records_relaxed_phase_anchor_negative_qc():
    relaxed_summary = {
        "phase_anchor_pick_count": 10,
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {"boundary_solution_count": 1},
        "figures": {"convention_summary": "relaxed_summary.png"},
    }
    summaries = {**_summaries(), "long_relaxed_phase_anchor": relaxed_summary}
    summary = summarize_bundle(
        figure_rows(summaries),
        claim_boundary_rows(relaxed_summary, summaries["bandlimited_repeatability"]),
        summaries,
    )

    assert summary["policy_label"] == "field_publication_claim_bundle_2d_qc_bandlimited_relaxed_anchor_ready_not_fwi"
    assert summary["figure_row_count"] == 9
    assert summary["claim_boundary_count"] == 8
    assert summary["long_relaxed_phase_anchor_included"] is True
    assert summary["long_relaxed_phase_anchor_low_snr_pick_count"] == 10
    assert summary["bandlimited_repeatability_included"] is True
    assert summary["gpu_priority"] == "none"


def test_event_support_tiers_are_added_to_publication_bundle():
    event_support = {
        "policy_label": "field_event_support_tiers_2d_qc_ready_not_fwi",
        "tier_row_count": 9,
        "short_content_anchor_supported_count": 2,
        "long_pattern_total_supported_anchor_count": 8,
        "paths": {"figure": "event_support.png"},
    }
    summaries = {**_summaries(), "event_support_tiers": event_support}
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        event_support_tiers_summary=event_support,
    )
    summary = summarize_bundle(figures, claims, summaries)

    assert figures[-1]["figure_key"] == "field_event_support_tiers"
    assert figures[-1]["metric_value"] == 9
    assert figures[-1]["figure_path"] == "event_support.png"
    assert claims[-1]["claim_area"] == "field_event_support_tiers"
    assert summary["policy_label"] == "field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_ready_not_fwi"
    assert summary["figure_row_count"] == 9
    assert summary["claim_boundary_count"] == 8
    assert summary["event_support_tiers_included"] is True
    assert summary["event_support_tier_row_count"] == 9
    assert summary["event_support_short_content_anchor_supported_count"] == 2
    assert summary["event_support_long_pattern_total_supported_anchor_count"] == 8
    assert summary["gpu_priority"] == "none"


def test_time_zero_uncertainty_budget_is_added_to_publication_bundle():
    time_zero = {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "relative_anchor_offset_ns": 0.127701,
        "bootstrap_ci_lower_ns": 0.108055,
        "bootstrap_ci_upper_ns": 0.147348,
        "conservative_half_width_ns": 0.058939,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "time_zero_budget.png"},
    }
    summaries = {**_summaries(), "time_zero_uncertainty": time_zero}
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        time_zero_uncertainty_summary=time_zero,
    )
    summary = summarize_bundle(figures, claims, summaries)

    assert figures[-1]["figure_key"] == "field_time_zero_uncertainty_budget"
    assert figures[-1]["metric_value"] == 0.058939
    assert figures[-1]["figure_path"] == "time_zero_budget.png"
    assert claims[-1]["claim_area"] == "field_time_zero_uncertainty_budget"
    assert "absolute time-zero" in claims[-1]["not_allowed"]
    assert summary["policy_label"] == "field_publication_claim_bundle_2d_qc_time_zero_bandlimited_ready_not_fwi"
    assert summary["figure_row_count"] == 9
    assert summary["claim_boundary_count"] == 8
    assert summary["time_zero_uncertainty_included"] is True
    assert summary["time_zero_uncertainty_policy"] == time_zero["policy_label"]
    assert summary["time_zero_relative_anchor_offset_ns"] == 0.127701
    assert summary["time_zero_bootstrap_ci_lower_ns"] == 0.108055
    assert summary["time_zero_bootstrap_ci_upper_ns"] == 0.147348
    assert summary["time_zero_conservative_half_width_ns"] == 0.058939
    assert summary["time_zero_absolute_ready"] is False
    assert summary["gpu_priority"] == "none"


def test_time_zero_perturbation_sensitivity_is_added_to_publication_bundle():
    time_zero = {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "relative_anchor_offset_ns": 0.127701,
        "bootstrap_ci_lower_ns": 0.108055,
        "bootstrap_ci_upper_ns": 0.147348,
        "conservative_half_width_ns": 0.058939,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "time_zero_budget.png"},
    }
    perturbation = {
        "policy_label": "field_time_zero_ci_perturbation_stack_robust",
        "bootstrap_ci_supported_count": 9,
        "bootstrap_ci_row_count": 9,
        "conservative_supported_count": 6,
        "conservative_row_count": 6,
        "min_nonraw_matrix_improvement": 0.125152,
        "min_nonraw_corrected_abs_correlation": 0.661316,
        "min_nonraw_improved_column_fraction": 0.570281,
        "paths": {"figure": "perturbation.png"},
    }
    summaries = {
        **_summaries(),
        "time_zero_uncertainty": time_zero,
        "time_zero_perturbation": perturbation,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        time_zero_uncertainty_summary=time_zero,
        time_zero_perturbation_summary=perturbation,
    )
    summary = summarize_bundle(figures, claims, summaries)

    assert figures[-1]["figure_key"] == "field_time_zero_perturbation_sensitivity"
    assert figures[-1]["metric_value"] == 9
    assert figures[-1]["figure_path"] == "perturbation.png"
    assert claims[-1]["claim_area"] == "field_time_zero_perturbation_sensitivity"
    assert "field FWI" in claims[-1]["not_allowed"]
    assert summary["policy_label"] == "field_publication_claim_bundle_2d_qc_time_zero_perturbation_bandlimited_ready_not_fwi"
    assert summary["figure_row_count"] == 10
    assert summary["claim_boundary_count"] == 9
    assert summary["time_zero_perturbation_included"] is True
    assert summary["time_zero_perturbation_policy"] == perturbation["policy_label"]
    assert summary["time_zero_perturbation_bootstrap_supported_count"] == 9
    assert summary["time_zero_perturbation_bootstrap_row_count"] == 9
    assert summary["time_zero_perturbation_conservative_supported_count"] == 6
    assert summary["time_zero_perturbation_conservative_row_count"] == 6
    assert summary["time_zero_perturbation_min_matrix_improvement"] == 0.125152
    assert summary["time_zero_perturbation_min_corrected_abs_correlation"] == 0.661316
    assert summary["time_zero_perturbation_min_improved_column_fraction"] == 0.570281


def test_timing_window_family_classification_is_added_to_publication_bundle():
    timing_anchor = {
        "policy_label": "field_timing_anchor_conflict_short_relative_not_absolute",
        "early_vs_short_delta_half_widths": 2.166667,
        "long_vs_short_delta_half_widths": 1.148667,
        "ready_for_manuscript_field_timing_boundary": True,
        "paths": {"figure": "timing_anchor.png"},
    }
    timing_window = {
        "policy_label": "field_timing_window_family_classification_ready_not_absolute",
        "early_strict_near_zero_lag_row_count": 6,
        "early_strict_row_count": 6,
        "short_nonraw_supported_count": 18,
        "short_nonraw_row_count": 18,
        "long_reject_short_transfer_row_count": 3,
        "long_row_count": 3,
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "ready_for_manuscript_field_timing_boundary": True,
        "paths": {"figure": "timing_window.png"},
    }
    summaries = {
        **_summaries(),
        "timing_anchor_conflict": timing_anchor,
        "timing_window_family": timing_window,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        timing_anchor_conflict_summary=timing_anchor,
        timing_window_family_summary=timing_window,
    )
    summary = summarize_bundle(figures, claims, summaries)

    assert figures[-1]["figure_key"] == "field_timing_window_family_classification"
    assert figures[-1]["metric_value"] == 18
    assert figures[-1]["figure_path"] == "timing_window.png"
    assert claims[-1]["claim_area"] == "field_timing_window_family_classification"
    assert "absolute time-zero" in claims[-1]["not_allowed"]
    assert "timing_window" in summary["policy_label"]
    assert summary["timing_window_family_included"] is True
    assert summary["timing_window_early_strict_near_zero_lag_count"] == 6
    assert summary["timing_window_short_nonraw_supported_count"] == 18
    assert summary["timing_window_long_reject_short_transfer_count"] == 3
    assert summary["timing_window_absolute_time_zero_ready"] is False
    assert summary["timing_window_field_fwi_ready"] is False
    assert summary["gpu_priority"] == "none"


def test_timing_discriminant_and_hpc_dimensionality_are_added_to_publication_bundle():
    timing_discriminant = {
        "policy_label": "field_timing_discriminant_scorecard_ready_not_absolute",
        "score_row_count": 4,
        "early_has_low_uniqueness_margin": True,
        "short_nonraw_supported_count": 18,
        "long_reject_short_transfer_count": 3,
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "ready_for_manuscript_timing_scorecard": True,
        "paths": {"figure": "timing_discriminant.png"},
    }
    hpc_dimensionality = {
        "policy_label": "gssi51600s_field_hpc_dimensionality_decision_2d_only_no_hpc",
        "field_geometry_type": "independent_2d_line_profiles",
        "is_3d_survey": False,
        "ready_for_2d_qc": True,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "field_hpc_priority": "none",
        "profile_count": 4,
        "paths": {"figure": "hpc_dimensionality.png"},
    }
    summaries = {
        **_summaries(),
        "timing_discriminant": timing_discriminant,
        "hpc_dimensionality": hpc_dimensionality,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        timing_discriminant_summary=timing_discriminant,
        hpc_dimensionality_summary=hpc_dimensionality,
    )
    summary = summarize_bundle(figures, claims, summaries)

    assert figures[-2]["figure_key"] == "field_timing_discriminant_scorecard"
    assert figures[-2]["metric_value"] == 4
    assert figures[-2]["figure_path"] == "timing_discriminant.png"
    assert figures[-1]["figure_key"] == "field_hpc_dimensionality_decision_card"
    assert figures[-1]["metric_value"] == 4
    assert claims[-2]["claim_area"] == "field_timing_discriminant_scorecard"
    assert claims[-1]["claim_area"] == "field_hpc_dimensionality"
    assert "timing_discriminant" in summary["policy_label"]
    assert "hpc_dimensionality" in summary["policy_label"]
    assert summary["figure_row_count"] == 10
    assert summary["claim_boundary_count"] == 9
    assert summary["timing_discriminant_included"] is True
    assert summary["timing_discriminant_short_nonraw_supported_count"] == 18
    assert summary["timing_discriminant_long_reject_short_transfer_count"] == 3
    assert summary["timing_discriminant_absolute_time_zero_ready"] is False
    assert summary["timing_discriminant_field_fwi_ready"] is False
    assert summary["hpc_dimensionality_included"] is True
    assert summary["hpc_dimensionality_field_geometry_type"] == "independent_2d_line_profiles"
    assert summary["hpc_dimensionality_ready_for_3d_hpc"] is False
    assert summary["hpc_dimensionality_ready_for_field_fwi"] is False
    assert summary["hpc_dimensionality_field_hpc_priority"] == "none"


def test_acquisition_readiness_is_added_to_publication_bundle():
    time_zero = {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "relative_anchor_offset_ns": 0.127701,
        "bootstrap_ci_lower_ns": 0.108055,
        "bootstrap_ci_upper_ns": 0.147348,
        "conservative_half_width_ns": 0.058939,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "time_zero_budget.png"},
    }
    perturbation = {
        "policy_label": "field_time_zero_ci_perturbation_stack_robust",
        "bootstrap_ci_supported_count": 9,
        "bootstrap_ci_row_count": 9,
        "conservative_supported_count": 6,
        "conservative_row_count": 6,
        "min_nonraw_matrix_improvement": 0.125152,
        "min_nonraw_corrected_abs_correlation": 0.661316,
        "min_nonraw_improved_column_fraction": 0.570281,
        "paths": {"figure": "perturbation.png"},
    }
    acquisition = {
        "policy_label": "field_acquisition_readiness_2d_qc_not_hpc_fwi",
        "readiness_row_count": 11,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "field_hpc_priority": "none",
        "samples_per_wavelength": 37.4778,
        "time_zero_two_way_depth_equivalent_mm": 5.8898,
        "paths": {"figure": "acquisition.png"},
    }
    relaxed = {
        "phase_anchor_pick_count": 10,
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {"boundary_solution_count": 1},
        "figures": {"convention_summary": "relaxed_summary.png"},
    }
    event_support = {
        "policy_label": "field_event_support_tiers_2d_qc_ready_not_fwi",
        "tier_row_count": 9,
        "short_content_anchor_supported_count": 2,
        "long_pattern_total_supported_anchor_count": 8,
        "paths": {"figure": "event_support.png"},
    }
    summaries = {
        **_summaries(),
        "long_relaxed_phase_anchor": relaxed,
        "event_support_tiers": event_support,
        "time_zero_uncertainty": time_zero,
        "time_zero_perturbation": perturbation,
        "acquisition_readiness": acquisition,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        relaxed_phase_anchor_summary=relaxed,
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        event_support_tiers_summary=event_support,
        time_zero_uncertainty_summary=time_zero,
        time_zero_perturbation_summary=perturbation,
        acquisition_readiness_summary=acquisition,
    )
    summary = summarize_bundle(figures, claims, summaries)

    assert figures[-1]["figure_key"] == "field_acquisition_readiness_audit"
    assert figures[-1]["metric_value"] == 11
    assert figures[-1]["figure_path"] == "acquisition.png"
    assert claims[-1]["claim_area"] == "field_acquisition_readiness"
    assert "field FWI/3D HPC" in claims[-1]["not_allowed"]
    assert summary["policy_label"] == (
        "field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_"
        "event_tiers_bandlimited_relaxed_ready_not_fwi"
    )
    assert summary["figure_row_count"] == 13
    assert summary["claim_boundary_count"] == 12
    assert summary["acquisition_readiness_included"] is True
    assert summary["acquisition_readiness_policy"] == acquisition["policy_label"]
    assert summary["acquisition_readiness_ready_for_3d_hpc"] is False
    assert summary["acquisition_readiness_ready_for_field_fwi"] is False
    assert summary["acquisition_readiness_field_hpc_priority"] == "none"
    assert summary["acquisition_readiness_samples_per_wavelength"] == 37.4778
    assert summary["acquisition_readiness_time_zero_depth_equivalent_mm"] == 5.8898


def test_depth_degeneracy_guardrails_are_added_to_publication_bundle():
    time_zero = {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "relative_anchor_offset_ns": 0.127701,
        "bootstrap_ci_lower_ns": 0.108055,
        "bootstrap_ci_upper_ns": 0.147348,
        "conservative_half_width_ns": 0.058939,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "time_zero_budget.png"},
    }
    perturbation = {
        "policy_label": "field_time_zero_ci_perturbation_stack_robust",
        "bootstrap_ci_supported_count": 9,
        "bootstrap_ci_row_count": 9,
        "conservative_supported_count": 6,
        "conservative_row_count": 6,
        "min_nonraw_matrix_improvement": 0.125152,
        "min_nonraw_corrected_abs_correlation": 0.661316,
        "min_nonraw_improved_column_fraction": 0.570281,
        "paths": {"figure": "perturbation.png"},
    }
    acquisition = {
        "policy_label": "field_acquisition_readiness_2d_qc_not_hpc_fwi",
        "readiness_row_count": 11,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "field_hpc_priority": "none",
        "samples_per_wavelength": 37.4778,
        "time_zero_two_way_depth_equivalent_mm": 5.8898,
        "paths": {"figure": "acquisition.png"},
    }
    relaxed = {
        "phase_anchor_pick_count": 10,
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {"boundary_solution_count": 1},
        "figures": {"convention_summary": "relaxed_summary.png"},
    }
    event_support = {
        "policy_label": "field_event_support_tiers_2d_qc_ready_not_fwi",
        "tier_row_count": 9,
        "short_content_anchor_supported_count": 2,
        "long_pattern_total_supported_anchor_count": 8,
        "paths": {"figure": "event_support.png"},
    }
    apparent_depth = {
        "policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth",
        "cue_count": 19,
        "max_corrected_depth_residual_mm": 4.908193,
        "time_zero_depth_equivalent_mm": 5.889832,
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_cover_depth_recovery": False,
        "paths": {"figure": "apparent_depth.png"},
    }
    apparent_sensitivity = {
        "policy_label": "field_apparent_depth_sensitivity_not_calibrated_cover_depth",
        "scenario_count": 5,
        "max_apparent_depth_sensitivity_factor": 2.181313,
        "max_apparent_depth_span_mm": 149.915924,
        "cover_depth_claim_ready": False,
        "paths": {"figure": "apparent_sensitivity.png"},
    }
    hyperbola_degeneracy = {
        "policy_label": "field_hyperbola_timezero_degeneracy_not_calibrated_inversion",
        "boundary_best_surface_count": 3,
        "surface_summary_row_count": 4,
        "max_near_top_epsr_span": 4.084544,
        "max_near_top_time_zero_span_ns": 0.3,
        "cover_depth_claim_ready": False,
        "radius_claim_ready": False,
        "field_fwi_ready": False,
        "paths": {"figure": "hyperbola_degen.png"},
    }
    summaries = {
        **_summaries(),
        "long_relaxed_phase_anchor": relaxed,
        "event_support_tiers": event_support,
        "time_zero_uncertainty": time_zero,
        "time_zero_perturbation": perturbation,
        "acquisition_readiness": acquisition,
        "apparent_depth_qc": apparent_depth,
        "apparent_depth_sensitivity": apparent_sensitivity,
        "hyperbola_timezero_degeneracy": hyperbola_degeneracy,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        relaxed_phase_anchor_summary=relaxed,
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        event_support_tiers_summary=event_support,
        time_zero_uncertainty_summary=time_zero,
        time_zero_perturbation_summary=perturbation,
        acquisition_readiness_summary=acquisition,
        apparent_depth_qc_summary=apparent_depth,
        apparent_depth_sensitivity_summary=apparent_sensitivity,
        hyperbola_timezero_degeneracy_summary=hyperbola_degeneracy,
    )
    summary = summarize_bundle(figures, claims, summaries)
    by_key = {row["figure_key"]: row for row in figures}
    claim_text = " ".join(row["not_allowed"] for row in claims)

    assert by_key["field_apparent_depth_scale_qc"]["metric_value"] == 4.908193
    assert by_key["field_apparent_depth_scale_qc"]["figure_path"] == "apparent_depth.png"
    assert by_key["field_apparent_depth_sensitivity_qc"]["metric_value"] == 2.181313
    assert by_key["field_hyperbola_timezero_degeneracy"]["metric_value"] == 3
    assert "calibrated cover-depth recovery" in claim_text
    assert "measured-data FWI recovery" in claim_text
    assert summary["policy_label"] == (
        "field_publication_claim_bundle_2d_qc_depth_degen_acquisition_time_zero_"
        "perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    )
    assert summary["figure_row_count"] == 16
    assert summary["claim_boundary_count"] == 15
    assert summary["apparent_depth_qc_included"] is True
    assert summary["apparent_depth_qc_ready_for_apparent_depth_scale_qc"] is True
    assert summary["apparent_depth_qc_ready_for_cover_depth_recovery"] is False
    assert summary["apparent_depth_sensitivity_factor"] == 2.181313
    assert summary["apparent_depth_sensitivity_cover_depth_ready"] is False
    assert summary["hyperbola_timezero_degeneracy_included"] is True
    assert summary["hyperbola_timezero_boundary_best_surface_count"] == 3
    assert summary["hyperbola_timezero_surface_count"] == 4
    assert summary["hyperbola_timezero_cover_depth_ready"] is False
    assert summary["hyperbola_timezero_radius_ready"] is False
    assert summary["hyperbola_timezero_field_fwi_ready"] is False
    assert summary["gpu_priority"] == "none"


def test_early_time_anchor_negative_qc_is_added_to_current_bundle():
    time_zero = {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "relative_anchor_offset_ns": 0.127701,
        "bootstrap_ci_lower_ns": 0.108055,
        "bootstrap_ci_upper_ns": 0.147348,
        "conservative_half_width_ns": 0.058939,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "time_zero_budget.png"},
    }
    perturbation = {
        "policy_label": "field_time_zero_ci_perturbation_stack_robust",
        "bootstrap_ci_supported_count": 9,
        "bootstrap_ci_row_count": 9,
        "conservative_supported_count": 6,
        "conservative_row_count": 6,
        "min_nonraw_matrix_improvement": 0.125152,
        "min_nonraw_corrected_abs_correlation": 0.661316,
        "min_nonraw_improved_column_fraction": 0.570281,
        "paths": {"figure": "perturbation.png"},
    }
    early_time = {
        "policy_label": "field_early_time_common_mode_not_content_time_zero",
        "short_pair_early_shift_ns": 0.0,
        "short_pair_early_vs_content_delta_ns": 0.127701,
        "short_pair_early_agrees_with_content_budget": False,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "early_time.png"},
    }
    acquisition = {
        "policy_label": "field_acquisition_readiness_2d_qc_not_hpc_fwi",
        "readiness_row_count": 11,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "field_hpc_priority": "none",
        "samples_per_wavelength": 37.4778,
        "time_zero_two_way_depth_equivalent_mm": 5.8898,
        "paths": {"figure": "acquisition.png"},
    }
    relaxed = {
        "phase_anchor_pick_count": 10,
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {"boundary_solution_count": 1},
        "figures": {"convention_summary": "relaxed_summary.png"},
    }
    event_support = {
        "policy_label": "field_event_support_tiers_2d_qc_ready_not_fwi",
        "tier_row_count": 9,
        "short_content_anchor_supported_count": 2,
        "long_pattern_total_supported_anchor_count": 8,
        "paths": {"figure": "event_support.png"},
    }
    apparent_depth = {
        "policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth",
        "cue_count": 19,
        "max_corrected_depth_residual_mm": 4.908193,
        "time_zero_depth_equivalent_mm": 5.889832,
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_cover_depth_recovery": False,
        "paths": {"figure": "apparent_depth.png"},
    }
    apparent_sensitivity = {
        "policy_label": "field_apparent_depth_sensitivity_not_calibrated_cover_depth",
        "scenario_count": 5,
        "max_apparent_depth_sensitivity_factor": 2.181313,
        "max_apparent_depth_span_mm": 149.915924,
        "cover_depth_claim_ready": False,
        "paths": {"figure": "apparent_sensitivity.png"},
    }
    hyperbola_degeneracy = {
        "policy_label": "field_hyperbola_timezero_degeneracy_not_calibrated_inversion",
        "boundary_best_surface_count": 3,
        "surface_summary_row_count": 4,
        "max_near_top_epsr_span": 4.084544,
        "max_near_top_time_zero_span_ns": 0.3,
        "cover_depth_claim_ready": False,
        "radius_claim_ready": False,
        "field_fwi_ready": False,
        "paths": {"figure": "hyperbola_degen.png"},
    }
    summaries = {
        **_summaries(),
        "long_relaxed_phase_anchor": relaxed,
        "event_support_tiers": event_support,
        "time_zero_uncertainty": time_zero,
        "time_zero_perturbation": perturbation,
        "early_time_anchor": early_time,
        "acquisition_readiness": acquisition,
        "apparent_depth_qc": apparent_depth,
        "apparent_depth_sensitivity": apparent_sensitivity,
        "hyperbola_timezero_degeneracy": hyperbola_degeneracy,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        relaxed_phase_anchor_summary=relaxed,
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        event_support_tiers_summary=event_support,
        time_zero_uncertainty_summary=time_zero,
        time_zero_perturbation_summary=perturbation,
        early_time_anchor_summary=early_time,
        acquisition_readiness_summary=acquisition,
        apparent_depth_qc_summary=apparent_depth,
        apparent_depth_sensitivity_summary=apparent_sensitivity,
        hyperbola_timezero_degeneracy_summary=hyperbola_degeneracy,
    )
    summary = summarize_bundle(figures, claims, summaries)
    by_key = {row["figure_key"]: row for row in figures}
    claim_text = " ".join(row["not_allowed"] for row in claims)

    assert by_key["field_early_time_anchor_negative_qc"]["metric_value"] == 0.127701
    assert by_key["field_early_time_anchor_negative_qc"]["figure_path"] == "early_time.png"
    assert "early direct/ringdown component" in claim_text
    assert summary["policy_label"] == (
        "field_publication_claim_bundle_2d_qc_early_time_depth_degen_acquisition_time_zero_"
        "perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    )
    assert summary["figure_row_count"] == 17
    assert summary["claim_boundary_count"] == 16
    assert summary["early_time_anchor_included"] is True
    assert summary["early_time_anchor_policy"] == early_time["policy_label"]
    assert summary["early_time_short_pair_shift_ns"] == 0.0
    assert summary["early_time_short_vs_content_delta_ns"] == 0.127701
    assert summary["early_time_short_agrees_with_content_budget"] is False
    assert summary["early_time_absolute_ready"] is False
    assert summary["gpu_priority"] == "none"


def test_timing_anchor_conflict_and_cue_spacing_are_added_to_current_bundle():
    time_zero = {
        "policy_label": "field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute",
        "relative_anchor_offset_ns": 0.127701,
        "bootstrap_ci_lower_ns": 0.108055,
        "bootstrap_ci_upper_ns": 0.147348,
        "conservative_half_width_ns": 0.058939,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "time_zero_budget.png"},
    }
    perturbation = {
        "policy_label": "field_time_zero_ci_perturbation_stack_robust",
        "bootstrap_ci_supported_count": 9,
        "bootstrap_ci_row_count": 9,
        "conservative_supported_count": 6,
        "conservative_row_count": 6,
        "min_nonraw_matrix_improvement": 0.125152,
        "min_nonraw_corrected_abs_correlation": 0.661316,
        "min_nonraw_improved_column_fraction": 0.570281,
        "paths": {"figure": "perturbation.png"},
    }
    early_time = {
        "policy_label": "field_early_time_common_mode_not_content_time_zero",
        "short_pair_early_shift_ns": 0.0,
        "short_pair_early_vs_content_delta_ns": 0.127701,
        "short_pair_early_agrees_with_content_budget": False,
        "absolute_time_zero_ready": False,
        "paths": {"figure": "early_time.png"},
    }
    acquisition = {
        "policy_label": "field_acquisition_readiness_2d_qc_not_hpc_fwi",
        "readiness_row_count": 11,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "field_hpc_priority": "none",
        "samples_per_wavelength": 37.4778,
        "time_zero_two_way_depth_equivalent_mm": 5.8898,
        "paths": {"figure": "acquisition.png"},
    }
    relaxed = {
        "phase_anchor_pick_count": 10,
        "low_snr_phase_anchor_pick_count": 10,
        "best_phase_hypothesis": {"boundary_solution_count": 1},
        "figures": {"convention_summary": "relaxed_summary.png"},
    }
    event_support = {
        "policy_label": "field_event_support_tiers_2d_qc_ready_not_fwi",
        "tier_row_count": 9,
        "short_content_anchor_supported_count": 2,
        "long_pattern_total_supported_anchor_count": 8,
        "paths": {"figure": "event_support.png"},
    }
    apparent_depth = {
        "policy_label": "field_apparent_depth_qc_relative_scale_not_cover_depth",
        "cue_count": 19,
        "max_corrected_depth_residual_mm": 4.908193,
        "time_zero_depth_equivalent_mm": 5.889832,
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_cover_depth_recovery": False,
        "paths": {"figure": "apparent_depth.png"},
    }
    apparent_sensitivity = {
        "policy_label": "field_apparent_depth_sensitivity_not_calibrated_cover_depth",
        "scenario_count": 5,
        "max_apparent_depth_sensitivity_factor": 2.181313,
        "max_apparent_depth_span_mm": 149.915924,
        "cover_depth_claim_ready": False,
        "paths": {"figure": "apparent_sensitivity.png"},
    }
    hyperbola_degeneracy = {
        "policy_label": "field_hyperbola_timezero_degeneracy_not_calibrated_inversion",
        "boundary_best_surface_count": 3,
        "surface_summary_row_count": 4,
        "max_near_top_epsr_span": 4.084544,
        "max_near_top_time_zero_span_ns": 0.3,
        "cover_depth_claim_ready": False,
        "radius_claim_ready": False,
        "field_fwi_ready": False,
        "paths": {"figure": "hyperbola_degen.png"},
    }
    cue_spacing = {
        "policy_label": "field_cue_spacing_context_threshold_robust_not_resolution_benchmark",
        "threshold_count": 7,
        "min_same_time_lateral_spacing_mm_across_thresholds": 96.657,
        "max_same_time_lateral_pair_count": 32,
        "all_thresholds_wider_than_close_scale": True,
        "ready_for_resolution_benchmark": False,
        "ready_for_field_fwi": False,
        "paths": {"figure": "cue_spacing.png"},
    }
    timing_anchor = {
        "policy_label": "field_timing_anchor_conflict_short_relative_not_absolute",
        "early_vs_short_delta_half_widths": 2.166667,
        "long_vs_short_delta_half_widths": 1.148667,
        "absolute_time_zero_ready": False,
        "field_fwi_ready": False,
        "ready_for_manuscript_field_timing_boundary": True,
        "paths": {"figure": "timing_conflict.png"},
    }
    summaries = {
        **_summaries(),
        "long_relaxed_phase_anchor": relaxed,
        "event_support_tiers": event_support,
        "time_zero_uncertainty": time_zero,
        "time_zero_perturbation": perturbation,
        "early_time_anchor": early_time,
        "timing_anchor_conflict": timing_anchor,
        "cue_spacing_sensitivity": cue_spacing,
        "acquisition_readiness": acquisition,
        "apparent_depth_qc": apparent_depth,
        "apparent_depth_sensitivity": apparent_sensitivity,
        "hyperbola_timezero_degeneracy": hyperbola_degeneracy,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        relaxed_phase_anchor_summary=relaxed,
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        event_support_tiers_summary=event_support,
        time_zero_uncertainty_summary=time_zero,
        time_zero_perturbation_summary=perturbation,
        early_time_anchor_summary=early_time,
        acquisition_readiness_summary=acquisition,
        apparent_depth_qc_summary=apparent_depth,
        apparent_depth_sensitivity_summary=apparent_sensitivity,
        hyperbola_timezero_degeneracy_summary=hyperbola_degeneracy,
        cue_spacing_sensitivity_summary=cue_spacing,
        timing_anchor_conflict_summary=timing_anchor,
    )
    summary = summarize_bundle(figures, claims, summaries)
    by_key = {row["figure_key"]: row for row in figures}
    claims_by_area = {row["claim_area"]: row for row in claims}

    assert by_key["field_cue_spacing_threshold_sensitivity"]["metric_value"] == 96.657
    assert by_key["field_cue_spacing_threshold_sensitivity"]["figure_path"] == "cue_spacing.png"
    assert by_key["field_timing_anchor_conflict"]["metric_value"] == 2.166667
    assert by_key["field_timing_anchor_conflict"]["figure_path"] == "timing_conflict.png"
    assert claims_by_area["field_cue_spacing_context"]["claim_area"] == "field_cue_spacing_context"
    assert "known-truth rebar separation" in claims_by_area["field_cue_spacing_context"]["not_allowed"]
    assert claims_by_area["field_timing_anchor_conflict"]["claim_area"] == "field_timing_anchor_conflict"
    assert "absolute time-zero" in claims_by_area["field_timing_anchor_conflict"]["not_allowed"]
    assert summary["policy_label"] == (
        "field_publication_claim_bundle_2d_qc_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_"
        "time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi"
    )
    assert summary["figure_row_count"] == 19
    assert summary["claim_boundary_count"] == 18
    assert summary["cue_spacing_sensitivity_included"] is True
    assert summary["cue_spacing_sensitivity_policy"] == cue_spacing["policy_label"]
    assert summary["cue_spacing_threshold_count"] == 7
    assert summary["cue_spacing_min_same_time_spacing_mm"] == 96.657
    assert summary["cue_spacing_max_same_time_pair_count"] == 32
    assert summary["cue_spacing_ready_for_field_context"] is True
    assert summary["cue_spacing_resolution_benchmark_ready"] is False
    assert summary["cue_spacing_field_fwi_ready"] is False
    assert summary["timing_anchor_conflict_included"] is True
    assert summary["timing_anchor_conflict_policy"] == timing_anchor["policy_label"]
    assert summary["timing_anchor_early_vs_short_delta_half_widths"] == 2.166667
    assert summary["timing_anchor_long_vs_short_delta_half_widths"] == 1.148667
    assert summary["timing_anchor_absolute_time_zero_ready"] is False
    assert summary["timing_anchor_field_fwi_ready"] is False
    assert summary["timing_anchor_ready_for_manuscript_boundary"] is True
    assert summary["gpu_priority"] == "none"


def test_short_anchor_signed_morphology_chain_is_added_to_current_bundle():
    waveform_coherence = {
        "policy_label": "gssi51600s_field_short_anchor_waveform_coherence_qc_only",
        "min_corrected_field_trace_abs_correlation": 0.939469,
        "ready_for_waveform_morphology_qc": True,
        "ready_for_field_fwi": False,
        "paths": {"figure": "waveform_coherence.png"},
    }
    radius_degeneracy = {
        "policy_label": "gssi51600s_field_short_anchor_radius_degeneracy_audit_qc_only",
        "weak_radius_side_count": 4,
        "ready_for_radius_seed": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "paths": {"figure": "radius_degeneracy.png"},
    }
    signed_morphology = {
        "policy_label": "gssi51600s_field_short_anchor_signed_morphology_qc_only",
        "signed_morphology_supported_pair_count": 2,
        "min_corrected_signed_correlation": 0.939469,
        "ready_for_signed_waveform_morphology_qc": True,
        "ready_for_field_fwi": False,
        "paths": {"figure": "signed_morphology.png"},
    }
    sensitivity = {
        "policy_label": "gssi51600s_field_short_anchor_signed_morphology_threshold_sensitivity_qc_only",
        "all_pairs_supported_threshold_combo_count": 36,
        "ready_for_moderate_threshold_morphology_qc": True,
        "ready_for_field_fwi": False,
        "paths": {"figure": "signed_sensitivity.png"},
    }
    timing_margin = {
        "policy_label": "gssi51600s_field_short_anchor_signed_morphology_timing_margin_qc_only",
        "max_corrected_abs_timing_residual_ns": 0.019646,
        "min_default_timing_slack_ns": 0.030354,
        "content_only_offset_half_range_ns": 0.009823,
        "short_conservative_half_width_ns": 0.058939,
        "default_slack_content_covered_pair_count": 2,
        "ready_for_content_only_morphology_timing_qc": True,
        "ready_for_conservative_timing_morphology_claim": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "paths": {"figure": "timing_margin.png"},
    }
    summaries = {
        **_summaries(),
        "short_waveform_coherence": waveform_coherence,
        "short_radius_degeneracy": radius_degeneracy,
        "short_signed_morphology": signed_morphology,
        "short_signed_morphology_sensitivity": sensitivity,
        "short_signed_morphology_timing_margin": timing_margin,
    }
    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        short_waveform_coherence_summary=waveform_coherence,
        short_radius_degeneracy_summary=radius_degeneracy,
        short_signed_morphology_summary=signed_morphology,
        short_signed_morphology_sensitivity_summary=sensitivity,
        short_signed_morphology_timing_margin_summary=timing_margin,
    )
    summary = summarize_bundle(figures, claims, summaries)
    by_key = {row["figure_key"]: row for row in figures}
    claims_by_area = {row["claim_area"]: row for row in claims}

    assert by_key["field_short_anchor_waveform_coherence_qc"]["metric_value"] == 0.939469
    assert by_key["field_short_anchor_radius_degeneracy_guardrail"]["metric_value"] == 4
    assert by_key["field_short_anchor_signed_morphology_qc"]["metric_value"] == 0.939469
    assert by_key["field_short_anchor_signed_morphology_threshold_sensitivity"]["metric_value"] == 36
    assert by_key["field_short_anchor_signed_morphology_timing_margin"]["metric_value"] == 0.030354
    assert "absolute amplitude calibration" in claims_by_area[
        "field_short_anchor_signed_morphology_qc"
    ]["not_allowed"]
    assert "field radius seeds" in claims_by_area[
        "field_short_anchor_radius_degeneracy"
    ]["not_allowed"]
    assert "conservative timing" in claims_by_area[
        "field_short_anchor_signed_morphology_timing_margin"
    ]["not_allowed"]
    assert "short_morphology" in summary["policy_label"]
    assert "short_timing_margin" in summary["policy_label"]
    assert summary["figure_row_count"] == 13
    assert summary["claim_boundary_count"] == 10
    assert summary["short_waveform_coherence_included"] is True
    assert summary["short_waveform_coherence_ready_for_morphology_qc"] is True
    assert summary["short_waveform_coherence_field_fwi_ready"] is False
    assert summary["short_radius_degeneracy_weak_side_count"] == 4
    assert summary["short_radius_degeneracy_ready_for_radius_seed"] is False
    assert summary["short_signed_morphology_supported_pair_count"] == 2
    assert summary["short_signed_morphology_ready_for_qc"] is True
    assert summary["short_signed_morphology_sensitivity_supported_threshold_combo_count"] == 36
    assert summary["short_signed_morphology_sensitivity_ready_for_moderate_qc"] is True
    assert summary["short_signed_morphology_timing_margin_min_default_slack_ns"] == 0.030354
    assert summary["short_signed_morphology_timing_margin_content_half_range_ns"] == 0.009823
    assert summary["short_signed_morphology_timing_margin_conservative_half_width_ns"] == 0.058939
    assert summary["short_signed_morphology_timing_margin_ready_for_content_qc"] is True
    assert summary["short_signed_morphology_timing_margin_ready_for_conservative_claim"] is False
    assert summary["short_signed_morphology_timing_margin_absolute_time_zero_ready"] is False
    assert summary["short_signed_morphology_timing_margin_field_fwi_ready"] is False
    assert summary["short_signed_morphology_timing_margin_3d_hpc_ready"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False


def test_short_anchor_signal_contrast_chain_is_added_to_current_bundle():
    signal_contrast = {
        "policy_label": "gssi51600s_field_short_anchor_signal_contrast_qc_only",
        "side_window_count": 4,
        "signal_contrast_supported_count": 4,
        "min_event_to_noise_rms": 4.129473,
        "min_peak_to_noise_p95": 12.398729,
        "ready_for_signal_contrast_qc": True,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_field_fwi": False,
        "paths": {"figure": "signal_contrast.png"},
    }
    sensitivity = {
        "policy_label": "gssi51600s_field_short_anchor_signal_contrast_sensitivity_qc_only",
        "sensitivity_combo_count": 27,
        "all_supported_combo_count": 13,
        "default_combo_all_supported": True,
        "ready_for_window_invariant_signal_contrast_claim": False,
        "ready_for_field_fwi": False,
        "paths": {"figure": "signal_sensitivity.png"},
    }
    summaries = {
        **_summaries(),
        "short_signal_contrast": signal_contrast,
        "short_signal_contrast_sensitivity": sensitivity,
    }

    figures = figure_rows(summaries)
    claims = claim_boundary_rows(
        bandlimited_repeatability_summary=summaries["bandlimited_repeatability"],
        short_signal_contrast_summary=signal_contrast,
        short_signal_contrast_sensitivity_summary=sensitivity,
    )
    summary = summarize_bundle(figures, claims, summaries)
    by_key = {row["figure_key"]: row for row in figures}
    claims_by_area = {row["claim_area"]: row for row in claims}

    assert by_key["field_short_anchor_signal_contrast_qc"]["metric_value"] == 4.129473
    assert by_key["field_short_anchor_signal_contrast_qc"]["figure_path"] == "signal_contrast.png"
    assert by_key["field_short_anchor_signal_contrast_sensitivity"]["metric_value"] == 13
    assert by_key["field_short_anchor_signal_contrast_sensitivity"]["figure_path"] == "signal_sensitivity.png"
    assert "strict window-invariant contrast" in claims_by_area[
        "field_short_anchor_signal_contrast_qc"
    ]["not_allowed"]
    assert "short_signal_contrast" in summary["policy_label"]
    assert summary["figure_row_count"] == 10
    assert summary["claim_boundary_count"] == 8
    assert summary["short_signal_contrast_included"] is True
    assert summary["short_signal_contrast_supported_window_count"] == 4
    assert summary["short_signal_contrast_side_window_count"] == 4
    assert summary["short_signal_contrast_min_event_to_noise_rms"] == 4.129473
    assert summary["short_signal_contrast_min_peak_to_noise_p95"] == 12.398729
    assert summary["short_signal_contrast_ready_for_qc"] is True
    assert summary["short_signal_contrast_amplitude_calibration_ready"] is False
    assert summary["short_signal_contrast_field_fwi_ready"] is False
    assert summary["short_signal_contrast_sensitivity_included"] is True
    assert summary["short_signal_contrast_sensitivity_combo_count"] == 27
    assert summary["short_signal_contrast_sensitivity_all_supported_combo_count"] == 13
    assert summary["short_signal_contrast_sensitivity_default_supported"] is True
    assert summary["short_signal_contrast_sensitivity_window_invariant_ready"] is False
    assert summary["short_signal_contrast_sensitivity_field_fwi_ready"] is False
    assert summary["ready_for_field_fwi"] is False
    assert summary["ready_for_3d_hpc"] is False
