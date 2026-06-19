from run_local_2d_field_manuscript_table_pack import (
    claim_tier,
    combine_claim_rows,
    combine_figure_rows,
    figure_role,
    metric_rows,
    summarize_table_pack,
    write_figure_notes,
)


def test_claim_tier_keeps_main_results_and_guardrails_separate():
    assert claim_tier("synthetic_2d", "resolution_limit") == "main_result"
    assert claim_tier("synthetic_2d", "gpu_next_step") == "guardrail"
    assert claim_tier("field_2d", "field_cue_spacing_context") == "field_supplement_result"
    assert claim_tier("field_2d", "field_timing_anchor_conflict") == "field_supplement_result"
    assert claim_tier("field_2d", "field_timing_window_family_classification") == "field_supplement_result"
    assert claim_tier("field_2d", "field_acquisition_readiness") == "guardrail"


def test_figure_role_identifies_field_cue_spacing_as_primary_supplement():
    assert figure_role("synthetic_2d", "synthetic_2d_resolution_claim_map") == "main_synthetic_result"
    assert (
        figure_role("field_2d", "field_cue_spacing_threshold_sensitivity")
        == "field_primary_supplement"
    )
    assert figure_role("field_2d", "field_timing_anchor_conflict") == "field_primary_supplement"
    assert figure_role("field_2d", "field_timing_window_family_classification") == "field_primary_supplement"
    assert figure_role("field_2d", "field_hyperbola_timezero_degeneracy") == "field_guardrail_supplement"


def test_combined_claim_and_figure_rows_are_domain_tagged():
    synthetic_claims = [
        {"claim_area": "resolution_limit", "allowed_claim": "allowed", "not_allowed": "blocked"},
    ]
    field_claims = [
        {"claim_area": "field_cue_spacing_context", "allowed_claim": "allowed", "not_allowed": "blocked"},
    ]
    synthetic_figures = [
        {
            "figure_key": "synthetic_2d_resolution_claim_map",
            "source_run": "run_a",
            "status_label": "ready",
            "support_metric": "metric",
            "paper_use": "use",
            "figure_path": "synthetic.png",
        },
    ]
    field_figures = [
        {
            "figure_key": "field_cue_spacing_threshold_sensitivity",
            "source_run": "run_b",
            "policy_label": "ready",
            "metric_label": "min_spacing",
            "metric_value": "96.657",
            "allowed_use": "use",
            "figure_path": "field.png",
        },
    ]

    claim_rows = combine_claim_rows(synthetic_claims, field_claims)
    figure_rows = combine_figure_rows(synthetic_figures, field_figures)

    assert [row["domain"] for row in claim_rows] == ["synthetic_2d", "field_2d"]
    assert claim_rows[0]["paper_use_tier"] == "main_result"
    assert claim_rows[1]["paper_use_tier"] == "field_supplement_result"
    assert figure_rows[0]["paper_role"] == "main_synthetic_result"
    assert figure_rows[1]["metric_summary"] == "min_spacing=96.657"


def test_summarize_table_pack_ready_no_gpu():
    claim_rows = [
        {"domain": "synthetic_2d"},
        {"domain": "field_2d"},
    ]
    figure_rows = [
        {"domain": "synthetic_2d"},
        {"domain": "field_2d"},
    ]
    synthetic_summary = {
        "ready_for_manuscript_draft": True,
        "gpu_priority": "none",
        "figure_count": 2,
    }
    synthetic_next = {"gpu_priority": "none_now"}
    field_summary = {
        "ready_for_manuscript_field_supplement": True,
        "gpu_priority": "none",
        "figure_row_count": 2,
        "cue_spacing_sensitivity_included": True,
        "cue_spacing_resolution_benchmark_ready": False,
        "cue_spacing_field_fwi_ready": False,
        "timing_anchor_conflict_included": True,
        "timing_anchor_early_vs_short_delta_half_widths": 2.166667,
        "timing_anchor_long_vs_short_delta_half_widths": 1.148667,
        "timing_anchor_absolute_time_zero_ready": False,
        "timing_anchor_field_fwi_ready": False,
        "timing_window_family_included": True,
        "timing_window_early_strict_near_zero_lag_count": 6,
        "timing_window_short_nonraw_supported_count": 18,
        "timing_window_short_nonraw_row_count": 18,
        "timing_window_long_reject_short_transfer_count": 3,
        "timing_window_long_row_count": 3,
        "timing_window_absolute_time_zero_ready": False,
        "timing_window_field_fwi_ready": False,
    }
    field_policy = {"publication_claim_bundle_gpu_priority": "none"}
    audit_summary = {
        "ready_for_manuscript_planning": True,
        "gpu_priority": "none",
        "claim_boundary_row_count": 2,
        "figure_audit_row_count": 2,
    }
    field_source_notes = {
        "ready_for_manuscript_handoff": True,
        "source_figure_count": 2,
        "notes_present_after_count": 2,
        "gpu_priority": "none",
    }
    synthetic_source_notes = {
        "ready_for_manuscript_handoff": True,
        "source_figure_count": 2,
        "notes_present_after_count": 2,
        "gpu_priority": "none",
    }
    target1_probe_summary = {
        "triggered_gate_count": 0,
        "gpu_action_count": 0,
        "ready_for_target1_gpu_probe": False,
        "target1_base_weak_exact_count": 43,
        "target1_late_high_accepted_count": 132,
        "gpu_priority": "none",
    }
    detector_handoff_summary = {
        "cheapest_full_candidate_triples_per_case": 1140,
        "best_deployable_all_truth_case_count": 2,
        "oracle_all_truth_case_count": 7,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_alltriples_summary = {
        "combo_row_count": 12180,
        "best_top1_all_truth_case_count": 0,
        "best_top10_case_count": 2,
        "best_top50_case_count": 8,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    field_cue_catalog_summary = {
        "raw_cue_count": 19,
        "support_anchor_count": 11,
        "short_content_backed_anchor_count": 2,
        "ready_for_2d_qc": True,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }
    detector_rank_budget_summary = {
        "minimal_all_case_candidate_triple_budget": 200,
        "best_top50_case_count": 8,
        "max_top1_all_truth_case_count": 0,
        "sparse_all_truth_case_count": 6,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_component_gate_summary = {
        "component_candidate_count": 230,
        "best_top10_case_count": 3,
        "best_top50_case_count": 10,
        "top50_improvement_over_source": 2,
        "best_top1_all_truth_case_count": 0,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_component_selector_summary = {
        "selector_candidate_count": 975,
        "best_in_sample_all_truth_case_count": 1,
        "leave_one_case_all_truth_case_count": 0,
        "leave_one_seed_all_truth_case_count": 0,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_geometry_selector_summary = {
        "selector_candidate_count": 2160,
        "best_in_sample_all_truth_case_count": 3,
        "leave_one_case_all_truth_case_count": 2,
        "leave_one_case_improvement_over_component_selector": 2,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_selector_gap_summary = {
        "selected_all_truth_case_count": 3,
        "failed_selector_case_count": 9,
        "best_truth_available_case_count": 12,
        "median_required_selector_gain_to_choose_truth": 0.18097749906867877,
        "max_required_selector_gain_to_choose_truth": 0.5505405776977454,
        "dominant_loss_feature": "signed_gap_prior_score",
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_selector_counterfactual_summary = {
        "counterfactual_variant_count": 44,
        "best_all_truth_case_count": 3,
        "best_improvement_over_base_all_truth_cases": 0,
        "signed_gap_zero_all_truth_case_count": 1,
        "best_median_required_selector_gain": 0.1541958996372459,
        "best_counterfactual_label": "signed_gap_sweep_w2",
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_image_objective_rank_summary = {
        "best_top50_all_truth_case_count": 0,
        "best_top200_all_truth_case_count": 1,
        "best_top1000_all_truth_case_count": 6,
        "best_median_first_all_truth_rank": 639,
        "previous_oracle_all_truth_case_count": 7,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_target_failure_summary = {
        "failed_selector_case_count": 9,
        "missing_target0_case_count": 5,
        "missing_target1_case_count": 7,
        "missing_target2_case_count": 3,
        "multi_target_missing_case_count": 5,
        "dominant_missing_target": "target1",
        "target1_missing_median_required_selector_gain": 0.28614967362496546,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_depth_slot_prior_summary = {
        "variant_count": 72,
        "base_all_truth_case_count": 3,
        "best_all_truth_case_count": 5,
        "best_improvement_over_base_all_truth_cases": 2,
        "best_depth_weight": 12.0,
        "best_slot_weight": 1.0,
        "best_missing_target1_case_count": 4,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_slot_component_assembly_summary = {
        "variant_count": 120,
        "current_triple_selector_all_truth_case_count": 3,
        "depth_slot_prior_best_all_truth_case_count": 5,
        "best_all_target_slot_case_count": 12,
        "best_failed_case_count": 0,
        "min_component_candidate_count": 16,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_blind_envelope_summary = {
        "variant_count": 288,
        "best_all_target_slot_case_count": 12,
        "leave_one_case_all_target_slot_case_count": 12,
        "known_slot_component_upper_bound_case_count": 12,
        "truth_free_selection_at_inference": True,
        "uses_branch_slots_for_selection": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_blind_envelope_robustness_summary = {
        "full_success_variant_count": 117,
        "near_success_variant_count": 288,
        "leave_one_seed_all_target_slot_case_count": 12,
        "leave_one_branch_all_target_slot_case_count": 11,
        "leave_one_condition_all_target_slot_case_count": 12,
        "best_variant_min_truth_vs_wrong_score_margin": 0.08362755681394554,
        "best_variant_low_margin_case_count": 1,
        "robustness_boundary": "seed_and_condition_robust_but_not_branch_independent",
        "heldout_branch_robust": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_blind_envelope_stability_summary = {
        "all_variant_success_case_count": 10,
        "partial_success_case_count": 2,
        "tuning_sensitive_case_count": 2,
        "min_success_fraction": 0.53125,
        "consensus_single_selection_case_count": 2,
        "close50_partial_success_case_count": 2,
        "max_unique_success_selection_count": 6,
        "tuning_sensitive_case_labels": (
            "target2_close50_linear29p5|seed13|nominal;"
            "target2_close50_linear29p5|seed34|nominal"
        ),
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_blind_envelope_tuning_summary = {
        "tuning_sensitive_case_count": 2,
        "max_knob_success_fraction_effect": 1.0,
        "structural_weight_direction_conflict": True,
        "support_weight_direction_conflict": True,
        "span_threshold_max_effect": 0.0,
        "ready_for_global_policy_tuning_fix": False,
        "ready_for_detector_seeded_fwi": False,
        "top_effect_knob": "structural_weight",
        "gpu_priority": "none",
    }
    detector_blind_envelope_reliability_summary = {
        "stable_assignment_case_count": 10,
        "review_assignment_case_count": 2,
        "tuning_sensitive_detected_by_gate_count": 2,
        "tuning_sensitive_missed_by_gate_count": 0,
        "stable_assignment_min_success_fraction_truth_eval": 1.0,
        "review_case_labels": (
            "target2_close50_linear29p5|seed13|nominal;"
            "target2_close50_linear29p5|seed34|nominal"
        ),
        "ready_for_reliability_claim": True,
        "ready_for_global_policy_tuning_fix": False,
        "truth_free_gate_uses_truth": False,
        "truth_evaluation_used_for_audit": True,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_blind_envelope_reliability_threshold_summary = {
        "clean_threshold_count": 5,
        "clean_threshold_min_mm": 5.0,
        "clean_threshold_max_mm": 19.0,
        "default_threshold_clean": True,
        "default_threshold_tuning_missed": 0,
        "default_threshold_false_review": 0,
        "ready_for_reliability_claim": True,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_physics_ambiguity_link_summary = {
        "detector_review_case_count": 2,
        "detector_stable_case_count": 10,
        "review_near_boundary_nominal_count": 2,
        "detector_reviews_all_near_boundary_nominal": True,
        "close50_linear29p5_nominal_review_fraction": 2 / 3,
        "review_cases_with_synthetic_x_ambiguity_count": 1,
        "review_cases_with_synthetic_strict_clean_count": 1,
        "linear29p5_offset_below_first_clean_mm": 0.5,
        "ready_for_branch_localization_claim": True,
        "ready_for_per_seed_physics_equivalence_claim": False,
        "ready_for_global_detector_tuning": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_refinement_launch_contract_summary = {
        "case_count": 12,
        "branch_count": 2,
        "candidate_component_seed_ready_count": 10,
        "review_case_count": 2,
        "active_blocker_count": 6,
        "max_component_seed_error_mm": 10.0,
        "radius_seed_available": False,
        "material_seed_available": False,
        "ready_for_component_seed_table": True,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_component_seed_export_summary = {
        "source_case_count": 12,
        "exported_seed_case_count": 10,
        "exported_component_row_count": 30,
        "excluded_review_case_count": 2,
        "max_exported_case_seed_error_mm": 10.0,
        "ready_for_coordinate_seed_table": True,
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_refinement_neighborhood_budget_summary = {
        "stable_seed_case_count": 10,
        "review_case_count": 2,
        "min_lateral_x_half_width_all_stable_seed_cases_mm": 10.0,
        "stable_lateral_x_coverage_at_5mm": 7,
        "stable_lateral_x_coverage_at_8mm": 9,
        "stable_lateral_x_coverage_at_10mm": 10,
        "per_case_lateral_x_grid_points_h10_step2": 1331,
        "hypothetical_per_case_xz_tensor_points_h10_step2": 1771561,
        "ready_for_lateral_x_slot_neighborhood_design": True,
        "z_coverage_validated": False,
        "ready_for_xz_neighborhood_design": False,
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_naive_full_tensor_refinement": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_seed_geometry_error_audit_summary = {
        "stable_seed_case_count": 10,
        "review_case_count": 2,
        "max_stable_x_error_mm": 10.0,
        "max_stable_z_error_mm": 12.0,
        "max_stable_linf_error_mm": 12.0,
        "stable_cases_z_exceeds_lateral_slot_error_count": 7,
        "min_xz_half_width_all_stable_seed_cases_mm": 12.0,
        "source_lateral_min_half_width_all_stable_seed_cases_mm": 10.0,
        "stable_xz_coverage_at_10mm": 8,
        "stable_xz_coverage_at_12mm": 10,
        "per_case_xz_grid_points_h12_step2": 4826809,
        "ready_for_xz_seed_neighborhood_design": True,
        "ready_for_radius_material_contract": False,
        "ready_for_narrow_refinement_contract": False,
        "ready_for_naive_full_tensor_refinement": False,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    detector_radius_material_prior_scope_summary = {
        "source_case_count": 12,
        "stable_controlled_prior_case_count": 10,
        "review_case_excluded_count": 2,
        "radius_prior_case_count": 12,
        "detector_radius_seed_available_count": 0,
        "detector_material_seed_available_count": 0,
        "ready_for_controlled_synthetic_prior_contract": True,
        "ready_for_detector_inferred_radius_material_contract": False,
        "ready_for_field_transfer": False,
        "ready_for_narrow_refinement_launch": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_work": False,
        "gpu_priority": "none",
    }
    detector_controlled_prior_refinement_budget_summary = {
        "fixed_slot_radii_stable_total_points_fine": 29_936_602,
        "fixed_slot_radii_stable_total_points_coarse": 156_250,
        "known_radius_permutations_stable_total_points_fine": 179_619_612,
        "independent_known_radius_choices_stable_total_points_fine": 808_288_254,
        "permutation_vs_fixed_multiplier": 6.0,
        "independent_vs_fixed_multiplier": 27.0,
        "ready_for_controlled_fixed_radius_budget": True,
        "ready_for_known_radius_permutation_budget": True,
        "ready_for_independent_radius_search": False,
        "ready_for_refinement_launch": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_work": False,
        "gpu_priority": "none",
    }
    detector_fixed_radius_locking_validation_summary = {
        "final_linf_error_mm": 0.0,
        "exact_geometry_recovered": True,
        "truth_selected_count": 1,
        "truth_selected_but_ambiguous_count": 1,
        "guard_aborted": False,
        "guard_within_caps": True,
        "guard_max_gpu_util_percent": 88.0,
        "guard_max_ram_used_percent": 14.687683727827094,
        "ready_for_locking_mechanism_claim": True,
        "ready_for_general_detector_policy_claim": False,
        "ready_for_broad_gpu_queue": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_field_transfer": False,
        "gpu_priority": "none",
    }
    detector_sampling_boundary_integration_summary = {
        "detector_review_case_count": 2,
        "review_below_clean_case_count": 2,
        "close50_nominal_review_case_count": 2,
        "close50_source_mismatch_review_case_count": 0,
        "ready_for_detector_sampling_boundary_claim": True,
        "per_seed_physics_equivalence_ready": False,
        "ready_for_detector_seeded_fwi": False,
        "ready_for_gpu_probe": False,
        "gpu_priority": "none",
    }
    detector_upper_bound_summary = {
        "minimal_all_case_rank_gated_triples_per_case": 200,
        "best_rank_gated_upper_bound_all_truth_case_count": 12,
        "ready_for_rank_gated_upper_bound_claim": True,
        "ready_for_detector_seeded_fwi": False,
        "gpu_priority": "none",
    }
    field_cue_timing_envelope_summary = {
        "short_anchor_inside_envelope_count": 3,
        "short_content_anchor_inside_envelope_count": 2,
        "long_pattern_reject_short_transfer_count": 8,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_long_short_transfer": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }
    field_spatial_transfer_summary = {
        "short_content_with_nearest_long_within_threshold_count": 1,
        "long_pattern_with_nearest_short_content_within_threshold_count": 1,
        "median_long_to_short_distance_mm": 701.5965,
        "ready_for_short_to_long_timing_transfer": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }
    field_anchor_interval_summary = {
        "short_anchor_inside_supported_interval_count": 3,
        "short_content_anchor_inside_supported_interval_count": 2,
        "min_margin_to_supported_interval_edge_mm": 13.332,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }
    field_dimensionality_summary = {
        "is_3d_survey": False,
        "ready_for_2d_qc": True,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_long_short_transfer": False,
        "ready_for_3d_hpc": False,
        "ready_for_field_fwi": False,
        "decision_gate_count": 8,
        "field_hpc_priority": "none",
    }
    field_time_zero_ladder_summary = {
        "ladder_row_count": 8,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_content_only_short_qc": True,
        "ready_for_leave_one_content_anchor_claim": False,
        "ready_for_long_short_transfer": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "short_conservative_half_width_ns": 0.058939096267190516,
        "content_only_offset_half_range_ns": 0.00982318271119842,
        "gpu_priority": "none",
    }
    field_short_anchor_leave_one_summary = {
        "content_only_supported": True,
        "content_only_offset_half_range_ns": 0.00982318271119842,
        "leave_one_supported_count": 1,
        "leave_one_degraded_single_content_count": 2,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }
    field_short_anchor_spatial_consistency_summary = {
        "content_residual_range_mm": 29.99699999999994,
        "content_residual_half_range_mm": 14.99849999999997,
        "content_min_supported_interval_margin_mm": 13.331999999999994,
        "content_single_translation_supported": False,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_profile_spatial_calibration": False,
        "ready_for_absolute_time_zero": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "gpu_priority": "none",
    }
    field_inversion_readiness_summary = {
        "gate_count": 8,
        "supported_gate_count": 2,
        "blocked_gate_count": 6,
        "ready_for_short_relative_timing_qc": True,
        "ready_for_apparent_depth_scale_qc": True,
        "ready_for_long_profile_transfer": False,
        "ready_for_profile_spatial_calibration": False,
        "ready_for_cover_depth_recovery": False,
        "ready_for_radius_recovery": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "apparent_depth_max_span_mm": 149.9159238899803,
        "gpu_priority": "none",
    }
    field_short_anchor_radius_degeneracy_summary = {
        "weak_radius_side_count": 4,
        "selected_radius_mismatch_pair_count": 2,
        "common_radius_near_tie_pair_count": 2,
        "ready_for_waveform_morphology_qc": True,
        "ready_for_radius_seed": False,
        "ready_for_radius_recovery": False,
        "ready_for_geometry_seed": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
    }
    field_short_anchor_signed_morphology_summary = {
        "signed_morphology_supported_pair_count": 2,
        "corrected_same_polarity_pair_count": 2,
        "min_corrected_signed_correlation": 0.9394685644349674,
        "ready_for_signed_waveform_morphology_qc": True,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_radius_seed": False,
        "ready_for_geometry_seed": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
    }
    field_short_anchor_signed_morphology_sensitivity_summary = {
        "threshold_combo_count": 320,
        "all_pairs_supported_threshold_combo_count": 36,
        "support_limit_corrected_signed_correlation": 0.9394685644349674,
        "ready_for_default_signed_morphology_qc": True,
        "ready_for_moderate_threshold_morphology_qc": True,
        "ready_for_strict_morphology_claim": False,
        "ready_for_absolute_amplitude_calibration": False,
        "ready_for_radius_seed": False,
        "ready_for_geometry_seed": False,
        "ready_for_field_fwi": False,
        "ready_for_3d_hpc": False,
        "ready_for_heavy_field_work": False,
        "gpu_priority": "none",
    }
    metrics = metric_rows(
        synthetic_summary,
        synthetic_next,
        field_summary,
        field_policy,
        audit_summary,
        synthetic_source_notes,
        field_source_notes,
        target1_probe_summary,
        detector_handoff_summary,
        detector_alltriples_summary,
        field_cue_catalog_summary,
        detector_rank_budget_summary,
        detector_component_gate_summary,
        detector_component_selector_summary,
        detector_geometry_selector_summary,
        detector_selector_gap_summary,
        detector_selector_counterfactual_summary,
        detector_image_objective_rank_summary,
        detector_target_failure_summary,
        detector_depth_slot_prior_summary,
        detector_slot_component_assembly_summary,
        detector_blind_envelope_summary,
        detector_blind_envelope_robustness_summary,
        detector_blind_envelope_stability_summary,
        detector_blind_envelope_tuning_summary,
        detector_blind_envelope_reliability_summary,
        detector_blind_envelope_reliability_threshold_summary,
        detector_physics_ambiguity_link_summary,
        detector_refinement_launch_contract_summary,
        detector_component_seed_export_summary,
        detector_refinement_neighborhood_budget_summary,
        detector_seed_geometry_error_audit_summary,
        detector_upper_bound_summary,
        field_cue_timing_envelope_summary,
        field_spatial_transfer_summary,
        field_anchor_interval_summary,
        field_dimensionality_summary,
        field_time_zero_ladder_summary,
        field_short_anchor_leave_one_summary,
        field_short_anchor_spatial_consistency_summary,
        field_inversion_readiness_summary,
        detector_sampling_boundary_integration_summary,
        field_short_anchor_radius_degeneracy_summary,
        field_short_anchor_signed_morphology_summary,
        field_short_anchor_signed_morphology_sensitivity_summary,
        detector_radius_material_prior_scope_summary=detector_radius_material_prior_scope_summary,
        detector_controlled_prior_refinement_budget_summary=(
            detector_controlled_prior_refinement_budget_summary
        ),
        detector_fixed_radius_locking_policy_validation_summary=(
            detector_fixed_radius_locking_validation_summary
        ),
    )

    summary = summarize_table_pack(
        claim_rows,
        figure_rows,
        metrics,
        synthetic_summary,
        synthetic_next,
        field_summary,
        field_policy,
        audit_summary,
        synthetic_source_notes,
        field_source_notes,
        target1_probe_summary,
        detector_handoff_summary,
        detector_alltriples_summary,
        field_cue_catalog_summary,
        detector_rank_budget_summary,
        detector_component_gate_summary,
        detector_component_selector_summary,
        detector_geometry_selector_summary,
        detector_selector_gap_summary,
        detector_selector_counterfactual_summary,
        detector_image_objective_rank_summary,
        detector_target_failure_summary,
        detector_depth_slot_prior_summary,
        detector_slot_component_assembly_summary,
        detector_blind_envelope_summary,
        detector_blind_envelope_robustness_summary,
        detector_blind_envelope_stability_summary,
        detector_blind_envelope_tuning_summary,
        detector_blind_envelope_reliability_summary,
        detector_blind_envelope_reliability_threshold_summary,
        detector_physics_ambiguity_link_summary,
        detector_refinement_launch_contract_summary,
        detector_component_seed_export_summary,
        detector_refinement_neighborhood_budget_summary,
        detector_seed_geometry_error_audit_summary,
        detector_upper_bound_summary,
        field_cue_timing_envelope_summary,
        field_spatial_transfer_summary,
        field_anchor_interval_summary,
        field_dimensionality_summary,
        field_time_zero_ladder_summary,
        field_short_anchor_leave_one_summary,
        field_short_anchor_spatial_consistency_summary,
        field_inversion_readiness_summary,
        detector_sampling_boundary_integration_summary,
        field_short_anchor_radius_degeneracy_summary,
        field_short_anchor_signed_morphology_summary,
        field_short_anchor_signed_morphology_sensitivity_summary,
        detector_radius_material_prior_scope_summary=detector_radius_material_prior_scope_summary,
        detector_controlled_prior_refinement_budget_summary=(
            detector_controlled_prior_refinement_budget_summary
        ),
        detector_fixed_radius_locking_policy_validation_summary=(
            detector_fixed_radius_locking_validation_summary
        ),
    )

    assert summary["policy_label"] == "local_2d_field_manuscript_table_pack_ready_no_gpu"
    assert summary["ready_for_manuscript_table_use"] is True
    assert summary["synthetic_source_figure_notes_included"] is True
    assert summary["synthetic_source_figure_notes_ready"] is True
    assert summary["synthetic_source_figure_notes_present_after_count"] == 2
    assert summary["field_cue_spacing_included"] is True
    assert summary["field_cue_spacing_resolution_ready"] is False
    assert summary["field_cue_spacing_fwi_ready"] is False
    assert summary["field_timing_anchor_conflict_included"] is True
    assert summary["field_timing_anchor_absolute_ready"] is False
    assert summary["field_timing_anchor_fwi_ready"] is False
    assert summary["field_timing_window_family_included"] is True
    assert summary["field_timing_window_short_supported_count"] == 18
    assert summary["field_timing_window_short_row_count"] == 18
    assert summary["field_timing_window_long_reject_count"] == 3
    assert summary["field_timing_window_long_row_count"] == 3
    assert summary["field_timing_window_absolute_ready"] is False
    assert summary["field_timing_window_fwi_ready"] is False
    assert summary["field_source_figure_notes_included"] is True
    assert summary["field_source_figure_notes_ready"] is True
    assert summary["field_source_figure_notes_present_after_count"] == 2
    assert summary["target1_probe_scorecard_included"] is True
    assert summary["target1_ready_for_gpu_probe"] is False
    assert summary["target1_probe_triggered_gate_count"] == 0
    assert summary["detector_handoff_budget_included"] is True
    assert summary["detector_handoff_ready_for_fwi"] is False
    assert summary["detector_handoff_cheapest_full_triples_per_case"] == 1140
    assert summary["detector_alltriples_gate_included"] is True
    assert summary["detector_alltriples_ready_for_fwi"] is False
    assert summary["detector_alltriples_best_top1_all_truth_cases"] == 0
    assert summary["detector_alltriples_best_top50_all_truth_cases"] == 8
    assert summary["field_cue_support_catalog_included"] is True
    assert summary["field_cue_catalog_ready_for_2d_qc"] is True
    assert summary["field_cue_catalog_ready_for_field_fwi"] is False
    assert summary["field_cue_catalog_support_anchor_count"] == 11
    assert summary["detector_rank_budget_included"] is True
    assert summary["detector_rank_budget_ready_for_fwi"] is False
    assert summary["detector_rank_budget_minimal_all_case_triples"] == 200
    assert summary["detector_component_gate_included"] is True
    assert summary["detector_component_gate_ready_for_fwi"] is False
    assert summary["detector_component_gate_best_top50_cases"] == 10
    assert summary["detector_component_gate_top50_improvement"] == 2
    assert summary["detector_component_selector_included"] is True
    assert summary["detector_component_selector_ready_for_fwi"] is False
    assert summary["detector_component_selector_candidate_count"] == 975
    assert summary["detector_component_selector_best_in_sample_cases"] == 1
    assert summary["detector_component_selector_leave_one_case_cases"] == 0
    assert summary["detector_geometry_selector_included"] is True
    assert summary["detector_geometry_selector_ready_for_fwi"] is False
    assert summary["detector_geometry_selector_candidate_count"] == 2160
    assert summary["detector_geometry_selector_best_in_sample_cases"] == 3
    assert summary["detector_geometry_selector_leave_one_case_cases"] == 2
    assert summary["detector_geometry_selector_leave_one_case_improvement"] == 2
    assert summary["detector_selector_gap_included"] is True
    assert summary["detector_selector_gap_ready_for_fwi"] is False
    assert summary["detector_selector_gap_selected_all_truth_cases"] == 3
    assert summary["detector_selector_gap_failed_cases"] == 9
    assert summary["detector_selector_gap_best_truth_available_cases"] == 12
    assert summary["detector_selector_gap_dominant_loss_feature"] == "signed_gap_prior_score"
    assert summary["detector_selector_counterfactual_included"] is True
    assert summary["detector_selector_counterfactual_ready_for_fwi"] is False
    assert summary["detector_selector_counterfactual_variant_count"] == 44
    assert summary["detector_selector_counterfactual_best_all_truth_cases"] == 3
    assert summary["detector_selector_counterfactual_improvement_over_base"] == 0
    assert summary["detector_selector_counterfactual_signed_gap_zero_cases"] == 1
    assert summary["detector_selector_counterfactual_best_label"] == "signed_gap_sweep_w2"
    assert summary["detector_image_objective_rank_included"] is True
    assert summary["detector_image_objective_rank_ready_for_fwi"] is False
    assert summary["detector_image_objective_rank_best_top50_cases"] == 0
    assert summary["detector_image_objective_rank_best_top200_cases"] == 1
    assert summary["detector_image_objective_rank_best_top1000_cases"] == 6
    assert summary["detector_image_objective_rank_best_median_rank"] == 639
    assert summary["detector_target_failure_taxonomy_included"] is True
    assert summary["detector_target_failure_ready_for_fwi"] is False
    assert summary["detector_target_failure_failed_cases"] == 9
    assert summary["detector_target_failure_missing_target0_cases"] == 5
    assert summary["detector_target_failure_missing_target1_cases"] == 7
    assert summary["detector_target_failure_missing_target2_cases"] == 3
    assert summary["detector_target_failure_multi_target_cases"] == 5
    assert summary["detector_target_failure_dominant_missing_target"] == "target1"
    assert summary["detector_target_failure_target1_median_gain"] == 0.28614967362496546
    assert summary["detector_depth_slot_prior_probe_included"] is True
    assert summary["detector_depth_slot_prior_ready_for_fwi"] is False
    assert summary["detector_depth_slot_prior_variant_count"] == 72
    assert summary["detector_depth_slot_prior_base_all_truth_cases"] == 3
    assert summary["detector_depth_slot_prior_best_all_truth_cases"] == 5
    assert summary["detector_depth_slot_prior_improvement_cases"] == 2
    assert summary["detector_depth_slot_prior_best_depth_weight"] == 12.0
    assert summary["detector_depth_slot_prior_best_slot_weight"] == 1.0
    assert summary["detector_depth_slot_prior_best_missing_target1_cases"] == 4
    assert summary["detector_slot_component_assembly_included"] is True
    assert summary["detector_slot_component_ready_for_fwi"] is False
    assert summary["detector_slot_component_variant_count"] == 120
    assert summary["detector_slot_component_current_triple_cases"] == 3
    assert summary["detector_slot_component_depth_prior_cases"] == 5
    assert summary["detector_slot_component_best_slot_cases"] == 12
    assert summary["detector_slot_component_best_failed_cases"] == 0
    assert summary["detector_slot_component_min_component_candidates"] == 16
    assert summary["detector_blind_envelope_included"] is True
    assert summary["detector_blind_envelope_ready_for_fwi"] is False
    assert summary["detector_blind_envelope_variant_count"] == 288
    assert summary["detector_blind_envelope_best_slot_cases"] == 12
    assert summary["detector_blind_envelope_leave_one_cases"] == 12
    assert summary["detector_blind_envelope_known_slot_upper_bound_cases"] == 12
    assert summary["detector_blind_envelope_uses_branch_slots"] is False
    assert summary["detector_blind_envelope_truth_free_inference"] is True
    assert summary["detector_blind_envelope_robustness_included"] is True
    assert summary["detector_blind_envelope_robustness_ready_for_fwi"] is False
    assert summary["detector_blind_envelope_robustness_full_success_variants"] == 117
    assert summary["detector_blind_envelope_robustness_near_success_variants"] == 288
    assert summary["detector_blind_envelope_robustness_leave_one_seed_cases"] == 12
    assert summary["detector_blind_envelope_robustness_leave_one_branch_cases"] == 11
    assert summary["detector_blind_envelope_robustness_leave_one_condition_cases"] == 12
    assert summary["detector_blind_envelope_robustness_min_margin"] == 0.08362755681394554
    assert summary["detector_blind_envelope_robustness_low_margin_cases"] == 1
    assert (
        summary["detector_blind_envelope_robustness_boundary"]
        == "seed_and_condition_robust_but_not_branch_independent"
    )
    assert summary["detector_blind_envelope_robustness_branch_robust"] is False
    assert summary["detector_blind_envelope_stability_included"] is True
    assert summary["detector_blind_envelope_stability_ready_for_fwi"] is False
    assert summary["detector_blind_envelope_stability_all_variant_cases"] == 10
    assert summary["detector_blind_envelope_stability_partial_cases"] == 2
    assert summary["detector_blind_envelope_stability_tuning_sensitive_cases"] == 2
    assert summary["detector_blind_envelope_stability_min_success_fraction"] == 0.53125
    assert summary["detector_blind_envelope_stability_consensus_cases"] == 2
    assert summary["detector_blind_envelope_stability_close50_partial_cases"] == 2
    assert summary["detector_blind_envelope_stability_max_unique_success_selections"] == 6
    assert (
        summary["detector_blind_envelope_stability_sensitive_labels"]
        == "target2_close50_linear29p5|seed13|nominal;target2_close50_linear29p5|seed34|nominal"
    )
    assert summary["detector_blind_envelope_tuning_included"] is True
    assert summary["detector_blind_envelope_tuning_ready_for_fwi"] is False
    assert summary["detector_blind_envelope_tuning_sensitive_cases"] == 2
    assert summary["detector_blind_envelope_tuning_max_knob_effect"] == 1.0
    assert summary["detector_blind_envelope_tuning_structural_conflict"] is True
    assert summary["detector_blind_envelope_tuning_support_conflict"] is True
    assert summary["detector_blind_envelope_tuning_span_effect"] == 0.0
    assert summary["detector_blind_envelope_tuning_global_fix_ready"] is False
    assert summary["detector_blind_envelope_tuning_top_knob"] == "structural_weight"
    assert summary["detector_blind_envelope_reliability_included"] is True
    assert summary["detector_blind_envelope_reliability_ready_for_claim"] is True
    assert summary["detector_blind_envelope_reliability_ready_for_fwi"] is False
    assert summary["detector_blind_envelope_reliability_stable_cases"] == 10
    assert summary["detector_blind_envelope_reliability_review_cases"] == 2
    assert summary["detector_blind_envelope_reliability_tuning_detected"] == 2
    assert summary["detector_blind_envelope_reliability_tuning_missed"] == 0
    assert summary["detector_blind_envelope_reliability_stable_min_success_fraction"] == 1.0
    assert (
        summary["detector_blind_envelope_reliability_review_labels"]
        == "target2_close50_linear29p5|seed13|nominal;target2_close50_linear29p5|seed34|nominal"
    )
    assert summary["detector_blind_envelope_reliability_threshold_included"] is True
    assert summary["detector_blind_envelope_reliability_threshold_ready_for_claim"] is True
    assert summary["detector_blind_envelope_reliability_threshold_ready_for_fwi"] is False
    assert summary["detector_blind_envelope_reliability_threshold_clean_count"] == 5
    assert summary["detector_blind_envelope_reliability_threshold_clean_min_mm"] == 5.0
    assert summary["detector_blind_envelope_reliability_threshold_clean_max_mm"] == 19.0
    assert summary["detector_blind_envelope_reliability_threshold_default_clean"] is True
    assert summary["detector_blind_envelope_reliability_threshold_default_tuning_missed"] == 0
    assert summary["detector_blind_envelope_reliability_threshold_default_false_review"] == 0
    assert summary["detector_physics_link_included"] is True
    assert summary["detector_physics_link_ready_for_branch_claim"] is True
    assert summary["detector_physics_link_ready_for_per_seed_equivalence"] is False
    assert summary["detector_physics_link_ready_for_fwi"] is False
    assert summary["detector_physics_link_review_cases"] == 2
    assert summary["detector_physics_link_near_boundary_nominal_reviews"] == 2
    assert summary["detector_physics_link_close50_nominal_review_fraction"] == 2 / 3
    assert summary["detector_physics_link_review_x_ambiguous_cases"] == 1
    assert summary["detector_physics_link_review_strict_clean_cases"] == 1
    assert summary["detector_physics_link_linear29p5_offset_below_clean_mm"] == 0.5
    assert summary["detector_refinement_contract_included"] is True
    assert summary["detector_refinement_contract_ready_seed_table"] is True
    assert summary["detector_refinement_contract_ready_narrow_refinement"] is False
    assert summary["detector_refinement_contract_ready_for_fwi"] is False
    assert summary["detector_refinement_contract_component_seed_ready_cases"] == 10
    assert summary["detector_refinement_contract_review_cases"] == 2
    assert summary["detector_refinement_contract_active_blockers"] == 6
    assert summary["detector_refinement_contract_radius_seed_available"] is False
    assert summary["detector_refinement_contract_material_seed_available"] is False
    assert summary["detector_refinement_contract_max_seed_error_mm"] == 10.0
    assert summary["detector_component_seed_export_included"] is True
    assert summary["detector_component_seed_exported_cases"] == 10
    assert summary["detector_component_seed_exported_components"] == 30
    assert summary["detector_component_seed_excluded_review_cases"] == 2
    assert summary["detector_component_seed_ready_coordinate_table"] is True
    assert summary["detector_component_seed_ready_for_fwi"] is False
    assert summary["detector_lateral_slot_budget_included"] is True
    assert summary["detector_lateral_slot_budget_min_half_width_mm"] == 10.0
    assert summary["detector_lateral_slot_budget_stable_coverage_5mm"] == 7
    assert summary["detector_lateral_slot_budget_stable_coverage_8mm"] == 9
    assert summary["detector_lateral_slot_budget_stable_coverage_10mm"] == 10
    assert summary["detector_lateral_slot_budget_h10_step2_per_case_points"] == 1331
    assert summary["detector_lateral_slot_budget_hypothetical_xz_h10_step2_points"] == 1771561
    assert summary["detector_lateral_slot_budget_z_coverage_validated"] is False
    assert summary["detector_lateral_slot_budget_ready_for_xz"] is False
    assert summary["detector_lateral_slot_budget_ready_for_fwi"] is False
    assert summary["detector_seed_geometry_audit_included"] is True
    assert summary["detector_seed_geometry_xz_min_half_width_mm"] == 12.0
    assert summary["detector_seed_geometry_source_lateral_half_width_mm"] == 10.0
    assert summary["detector_seed_geometry_max_stable_x_error_mm"] == 10.0
    assert summary["detector_seed_geometry_max_stable_z_error_mm"] == 12.0
    assert summary["detector_seed_geometry_z_exceeds_lateral_count"] == 7
    assert summary["detector_seed_geometry_stable_xz_coverage_10mm"] == 8
    assert summary["detector_seed_geometry_stable_xz_coverage_12mm"] == 10
    assert summary["detector_seed_geometry_h12_step2_per_case_points"] == 4826809
    assert summary["detector_seed_geometry_ready_xz_seed_neighborhood"] is True
    assert summary["detector_seed_geometry_ready_for_fwi"] is False
    assert summary["detector_radius_material_prior_included"] is True
    assert summary["detector_radius_material_prior_controlled_ready"] is True
    assert summary["detector_radius_material_prior_detector_inferred_ready"] is False
    assert summary["detector_radius_material_prior_ready_for_fwi"] is False
    assert summary["detector_radius_material_prior_stable_cases"] == 10
    assert summary["detector_radius_material_prior_review_cases"] == 2
    assert summary["detector_radius_material_prior_detector_radius_seeds"] == 0
    assert summary["detector_radius_material_prior_detector_material_seeds"] == 0
    assert summary["detector_controlled_prior_refinement_budget_included"] is True
    assert summary["detector_controlled_prior_refinement_fixed_budget_ready"] is True
    assert summary["detector_controlled_prior_refinement_independent_search_ready"] is False
    assert summary["detector_controlled_prior_refinement_launch_ready"] is False
    assert summary["detector_controlled_prior_refinement_ready_for_fwi"] is False
    assert summary["detector_controlled_prior_refinement_fixed_fine_points"] == 29_936_602
    assert summary["detector_controlled_prior_refinement_fixed_coarse_points"] == 156_250
    assert summary["detector_controlled_prior_refinement_permutation_multiplier"] == 6.0
    assert summary["detector_controlled_prior_refinement_independent_multiplier"] == 27.0
    assert summary["detector_fixed_radius_locking_validation_included"] is True
    assert summary["detector_fixed_radius_locking_validation_exact"] is True
    assert summary["detector_fixed_radius_locking_validation_mechanism_ready"] is True
    assert summary["detector_fixed_radius_locking_validation_general_policy_ready"] is False
    assert summary["detector_fixed_radius_locking_validation_broad_gpu_ready"] is False
    assert summary["detector_fixed_radius_locking_validation_ready_for_fwi"] is False
    assert summary["detector_fixed_radius_locking_validation_final_linf_mm"] == 0.0
    assert summary["detector_fixed_radius_locking_validation_truth_ambiguous_count"] == 1
    assert summary["detector_fixed_radius_locking_validation_guard_max_gpu_util_percent"] == 88.0
    assert summary["detector_sampling_boundary_integration_included"] is True
    assert summary["detector_sampling_boundary_claim_ready"] is True
    assert summary["detector_sampling_boundary_per_seed_equivalence_ready"] is False
    assert summary["detector_sampling_boundary_ready_for_fwi"] is False
    assert summary["detector_sampling_boundary_review_cases"] == 2
    assert summary["detector_sampling_boundary_review_below_clean_cases"] == 2
    assert summary["detector_sampling_boundary_close50_nominal_reviews"] == 2
    assert summary["detector_sampling_boundary_close50_source_mismatch_reviews"] == 0
    assert summary["detector_upper_bound_policy_included"] is True
    assert summary["detector_upper_bound_ready_for_claim"] is True
    assert summary["detector_upper_bound_ready_for_fwi"] is False
    assert summary["detector_upper_bound_minimal_all_case_triples"] == 200
    assert summary["detector_upper_bound_all_truth_cases"] == 12
    assert summary["field_cue_timing_envelope_included"] is True
    assert summary["field_cue_timing_ready_for_short_qc"] is True
    assert summary["field_cue_timing_ready_for_field_fwi"] is False
    assert summary["field_cue_timing_short_inside_envelope_count"] == 3
    assert summary["field_cue_timing_long_reject_short_transfer_count"] == 8
    assert summary["field_spatial_transfer_included"] is True
    assert summary["field_spatial_transfer_ready_for_transfer"] is False
    assert summary["field_spatial_transfer_ready_for_field_fwi"] is False
    assert summary["field_spatial_transfer_short_covered_count"] == 1
    assert summary["field_spatial_transfer_long_covered_count"] == 1
    assert summary["field_spatial_transfer_median_long_distance_mm"] == 701.5965
    assert summary["field_anchor_interval_included"] is True
    assert summary["field_anchor_interval_ready_for_short_qc"] is True
    assert summary["field_anchor_interval_ready_for_field_fwi"] is False
    assert summary["field_anchor_interval_short_inside_count"] == 3
    assert summary["field_anchor_interval_content_inside_count"] == 2
    assert summary["field_anchor_interval_min_margin_mm"] == 13.332
    assert summary["field_dimensionality_included"] is True
    assert summary["field_dimensionality_is_3d_survey"] is False
    assert summary["field_dimensionality_ready_for_short_qc"] is True
    assert summary["field_dimensionality_ready_for_long_transfer"] is False
    assert summary["field_dimensionality_ready_for_3d_hpc"] is False
    assert summary["field_dimensionality_ready_for_field_fwi"] is False
    assert summary["field_dimensionality_decision_gate_count"] == 8
    assert summary["field_time_zero_ladder_included"] is True
    assert summary["field_time_zero_ladder_ready_for_short_qc"] is True
    assert summary["field_time_zero_ladder_ready_for_content_only_short_qc"] is True
    assert summary["field_time_zero_ladder_ready_for_leave_one_content_anchor"] is False
    assert summary["field_time_zero_ladder_ready_for_long_transfer"] is False
    assert summary["field_time_zero_ladder_ready_for_absolute_t0"] is False
    assert summary["field_time_zero_ladder_ready_for_field_fwi"] is False
    assert summary["field_time_zero_ladder_ready_for_3d_hpc"] is False
    assert summary["field_time_zero_ladder_short_half_width_ns"] == 0.058939096267190516
    assert summary["field_time_zero_ladder_content_half_range_ns"] == 0.00982318271119842
    assert summary["field_time_zero_ladder_ladder_row_count"] == 8
    assert summary["field_short_anchor_leave_one_included"] is True
    assert summary["field_short_anchor_leave_one_content_only_supported"] is True
    assert summary["field_short_anchor_leave_one_ready_for_short_qc"] is True
    assert summary["field_short_anchor_leave_one_ready_for_field_fwi"] is False
    assert summary["field_short_anchor_leave_one_supported_cases"] == 1
    assert summary["field_short_anchor_leave_one_degraded_cases"] == 2
    assert summary["field_short_anchor_leave_one_content_half_range_ns"] == 0.00982318271119842
    assert summary["field_short_anchor_spatial_consistency_included"] is True
    assert summary["field_short_anchor_spatial_ready_for_short_qc"] is True
    assert summary["field_short_anchor_spatial_ready_for_spatial_calibration"] is False
    assert summary["field_short_anchor_spatial_ready_for_field_fwi"] is False
    assert summary["field_short_anchor_spatial_single_translation_supported"] is False
    assert summary["field_short_anchor_spatial_content_residual_range_mm"] == 29.99699999999994
    assert summary["field_short_anchor_spatial_content_residual_half_range_mm"] == 14.99849999999997
    assert summary["field_short_anchor_spatial_content_min_margin_mm"] == 13.331999999999994
    assert summary["field_inversion_readiness_included"] is True
    assert summary["field_inversion_readiness_ready_short_qc"] is True
    assert summary["field_inversion_readiness_ready_depth_scale_qc"] is True
    assert summary["field_inversion_readiness_ready_long_transfer"] is False
    assert summary["field_inversion_readiness_ready_spatial_calibration"] is False
    assert summary["field_inversion_readiness_ready_cover_depth"] is False
    assert summary["field_inversion_readiness_ready_radius"] is False
    assert summary["field_inversion_readiness_ready_field_fwi"] is False
    assert summary["field_inversion_readiness_ready_3d_hpc"] is False
    assert summary["field_inversion_readiness_gate_count"] == 8
    assert summary["field_inversion_readiness_supported_gates"] == 2
    assert summary["field_inversion_readiness_blocked_gates"] == 6
    assert summary["field_inversion_readiness_apparent_depth_span_mm"] == 149.9159238899803
    assert summary["field_short_anchor_radius_degeneracy_included"] is True
    assert summary["field_short_anchor_radius_degeneracy_ready_morphology_qc"] is True
    assert summary["field_short_anchor_radius_degeneracy_ready_radius_seed"] is False
    assert summary["field_short_anchor_radius_degeneracy_ready_field_fwi"] is False
    assert summary["field_short_anchor_radius_degeneracy_weak_sides"] == 4
    assert summary["field_short_anchor_radius_degeneracy_mismatch_pairs"] == 2
    assert summary["field_short_anchor_radius_degeneracy_common_near_ties"] == 2
    assert summary["field_short_anchor_signed_morphology_included"] is True
    assert summary["field_short_anchor_signed_morphology_ready_qc"] is True
    assert summary["field_short_anchor_signed_morphology_ready_amplitude_calibration"] is False
    assert summary["field_short_anchor_signed_morphology_ready_field_fwi"] is False
    assert summary["field_short_anchor_signed_morphology_supported_pairs"] == 2
    assert summary["field_short_anchor_signed_morphology_min_signed_corr"] == 0.9394685644349674
    assert summary["field_short_anchor_signed_sensitivity_included"] is True
    assert summary["field_short_anchor_signed_sensitivity_supported_combos"] == 36
    assert summary["field_short_anchor_signed_sensitivity_threshold_combos"] == 320
    assert summary["field_short_anchor_signed_sensitivity_moderate_ready"] is True
    assert summary["field_short_anchor_signed_sensitivity_strict_ready"] is False
    assert summary["field_short_anchor_signed_sensitivity_ready_field_fwi"] is False
    assert summary["auxiliary_evidence_metric_count"] == 272
    assert sum(row["metric"] == "source_figure_notes_present_after_count" for row in metrics) == 2
    assert any(
        row["metric"] == "timing_window_short_nonraw_supported_count" and row["value"] == 18
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_alltriples_combo_row_count" and row["value"] == 12180
        for row in metrics
    )
    assert any(
        row["metric"] == "field_cue_catalog_ready_for_field_fwi" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_component_gate_best_top50_cases" and row["value"] == 10
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_component_selector_leave_one_case_cases" and row["value"] == 0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_radius_material_prior_controlled_ready" and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_controlled_prior_refinement_fixed_fine_points"
        and row["value"] == 29_936_602
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_fixed_radius_locking_validation_exact"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_fixed_radius_locking_validation_broad_gpu_ready"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_geometry_selector_leave_one_case_cases" and row["value"] == 2
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_selector_gap_failed_cases" and row["value"] == 9
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_selector_counterfactual_improvement_over_base" and row["value"] == 0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_image_rank_best_top50_cases" and row["value"] == 0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_target_failure_missing_target1_cases" and row["value"] == 7
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_target_failure_ready_for_fwi" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_depth_slot_prior_best_all_truth_cases" and row["value"] == 5
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_depth_slot_prior_ready_for_fwi" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_slot_component_best_slot_cases" and row["value"] == 12
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_slot_component_ready_for_fwi" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_best_slot_cases" and row["value"] == 12
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_uses_branch_slots" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_ready_for_fwi" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_robustness_leave_one_branch_cases"
        and row["value"] == 11
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_robustness_min_margin"
        and row["value"] == 0.08362755681394554
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_robustness_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_stability_all_variant_cases"
        and row["value"] == 10
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_stability_tuning_sensitive_cases"
        and row["value"] == 2
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_stability_min_success_fraction"
        and row["value"] == 0.53125
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_stability_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_tuning_max_knob_effect"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_tuning_global_fix_ready"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_reliability_stable_cases"
        and row["value"] == 10
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_reliability_tuning_missed"
        and row["value"] == 0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_reliability_ready_for_claim"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_reliability_threshold_clean_count"
        and row["value"] == 5
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_reliability_threshold_default_clean"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_blind_envelope_reliability_threshold_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_physics_link_reviews_all_near_boundary_nominal"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_physics_link_review_x_ambiguous_cases"
        and row["value"] == 1
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_physics_link_per_seed_equivalence_ready"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_physics_link_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_refinement_contract_seed_table_cases"
        and row["value"] == 10
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_refinement_contract_active_blockers"
        and row["value"] == 6
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_refinement_contract_ready_narrow_refinement"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_refinement_contract_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_component_seed_exported_cases" and row["value"] == 10
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_component_seed_ready_for_fwi" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_lateral_slot_budget_min_half_width_mm"
        and row["value"] == 10.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_lateral_slot_budget_h10_step2_per_case_points"
        and row["value"] == 1331
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_lateral_slot_budget_hypothetical_xz_h10_step2_points"
        and row["value"] == 1771561
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_lateral_slot_budget_ready_for_xz"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_lateral_slot_budget_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_seed_geometry_xz_min_half_width_mm"
        and row["value"] == 12.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_seed_geometry_max_stable_z_error_mm"
        and row["value"] == 12.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_seed_geometry_h12_step2_per_case_points"
        and row["value"] == 4826809
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_seed_geometry_ready_xz_seed_neighborhood"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_seed_geometry_ready_for_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_sampling_boundary_claim_ready"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_sampling_boundary_per_seed_equivalence_ready"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "detector_upper_bound_minimal_all_case_triples" and row["value"] == 200
        for row in metrics
    )
    assert any(
        row["metric"] == "field_cue_timing_long_reject_short_transfer_count" and row["value"] == 8
        for row in metrics
    )
    assert any(
        row["metric"] == "field_spatial_transfer_long_covered_count" and row["value"] == 1
        for row in metrics
    )
    assert any(
        row["metric"] == "field_anchor_interval_short_inside_count" and row["value"] == 3
        for row in metrics
    )
    assert any(
        row["metric"] == "field_dimensionality_ready_for_short_qc" and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_time_zero_ladder_ready_absolute_t0" and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_time_zero_ladder_ladder_row_count" and row["value"] == 8
        for row in metrics
    )
    assert any(
        row["metric"] == "field_time_zero_ladder_ready_content_only_short_qc"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_spatial_content_residual_range_mm"
        and row["value"] == 29.99699999999994
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_spatial_single_translation_supported"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_spatial_ready_spatial_calibration"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_inversion_readiness_supported_gates"
        and row["value"] == 2
        for row in metrics
    )
    assert any(
        row["metric"] == "field_inversion_readiness_ready_depth_scale_qc"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_inversion_readiness_ready_field_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_inversion_readiness_apparent_depth_span_mm"
        and row["value"] == 149.9159238899803
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_radius_degeneracy_ready_radius_seed"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_radius_degeneracy_common_near_tie_pairs"
        and row["value"] == 2
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_signed_morphology_min_signed_corr"
        and row["value"] == 0.9394685644349674
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_signed_morphology_ready_field_fwi"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_signed_sensitivity_supported_combos"
        and row["value"] == 36
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_signed_sensitivity_strict_ready"
        and row["value"] == 0.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_leave_one_content_only_supported"
        and row["value"] == 1.0
        for row in metrics
    )
    assert any(
        row["metric"] == "field_short_anchor_leave_one_degraded_cases" and row["value"] == 2
        for row in metrics
    )


def test_field_collection_handoff_is_table_pack_guardrail():
    claim_rows = [
        {"domain": "synthetic_2d"},
        {"domain": "field_2d"},
    ]
    figure_rows = [
        {"domain": "synthetic_2d"},
        {"domain": "field_2d"},
    ]
    synthetic_summary = {
        "ready_for_manuscript_draft": True,
        "gpu_priority": "none",
        "figure_count": 1,
    }
    synthetic_next = {"gpu_priority": "none_now"}
    field_summary = {
        "ready_for_manuscript_field_supplement": True,
        "gpu_priority": "none",
        "figure_row_count": 1,
    }
    field_policy = {"publication_claim_bundle_gpu_priority": "none"}
    audit_summary = {
        "ready_for_manuscript_planning": True,
        "gpu_priority": "none",
        "claim_boundary_row_count": 2,
        "figure_audit_row_count": 2,
    }
    field_handoff = {
        "handoff_action_count": 7,
        "critical_new_data_action_count": 5,
        "packet_rows_needing_entry": 12,
        "failed_acceptance_gate_count": 7,
        "reference_uncertainty_gate_ns": 0.02,
        "ready_for_collection_day": True,
        "ready_for_packet_acceptance": False,
        "ready_for_current_archive_field_qc_supplement": True,
        "ready_for_current_archive_field_fwi": False,
        "ready_for_current_archive_heavy_field_work": False,
        "ready_for_field_3d_hpc": False,
        "gpu_priority": "none",
    }

    metrics = metric_rows(
        synthetic_summary,
        synthetic_next,
        field_summary,
        field_policy,
        audit_summary,
        field_collection_handoff_summary=field_handoff,
    )
    summary = summarize_table_pack(
        claim_rows,
        figure_rows,
        metrics,
        synthetic_summary,
        synthetic_next,
        field_summary,
        field_policy,
        audit_summary,
        field_collection_handoff_summary=field_handoff,
    )

    assert summary["policy_label"] == "local_2d_field_manuscript_table_pack_ready_no_gpu"
    assert summary["field_collection_handoff_included"] is True
    assert summary["field_collection_handoff_ready_collection_day"] is True
    assert summary["field_collection_handoff_ready_packet_acceptance"] is False
    assert summary["field_collection_handoff_ready_field_fwi"] is False
    assert summary["field_collection_handoff_ready_3d_hpc"] is False
    assert summary["field_collection_handoff_critical_new_data_actions"] == 5
    assert summary["field_collection_handoff_packet_rows_needing_entry"] == 12
    assert any(
        row["metric"] == "field_collection_handoff_failed_acceptance_gates"
        and row["value"] == 7
        for row in metrics
    )


def test_write_figure_notes_documents_table_pack(tmp_path):
    summary = {
        "policy_label": "table_policy",
        "synthetic_figure_count": 9,
        "field_figure_count": 19,
        "synthetic_claim_count": 11,
        "field_claim_count": 18,
        "gpu_priority": "none",
    }
    notes_path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(
        notes_path,
        summary,
        tmp_path / "claims.csv",
        tmp_path / "figures.csv",
        tmp_path / "metrics.csv",
        tmp_path / "figure_validation.csv",
    )

    text = notes_path.read_text(encoding="utf-8")
    assert "local_2d_field_manuscript_table_pack.png" in text
    assert "table_policy" in text
    assert "not a new experiment" in text
