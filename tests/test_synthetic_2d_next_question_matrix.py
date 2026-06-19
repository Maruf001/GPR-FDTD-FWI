import json

from run_synthetic_2d_next_question_matrix import (
    candidate_rows,
    read_latest_matched_source3_policy,
    read_latest_publication_bundle,
    read_latest_target1_acquisition_surface,
    read_latest_target1_source_density_exception_map,
    summarize_matrix,
    write_figure_notes,
)


def _write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_next_matrix_inputs(tmp_path):
    _write_json(
        tmp_path / "1278_synthetic_2d_publication_figure_bundle/data/synthetic_2d_publication_figure_bundle_summary.json",
        {"figure_count": 5, "validated_figure_count": 5, "gpu_priority": "none"},
    )
    _write_json(
        tmp_path / "1275_close50_linear_sub30_bracket_policy/data/close50_linear_sub30_bracket_summary.json",
        {
            "x_ambiguity_row_count": 2,
            "tested_offsets_mm": "29.5,29.75",
            "radius_margin_abs_min": 0.01,
            "strict_clean_row_count": 4,
            "sub30_confidence_row_count": 6,
            "seed13_x_ambiguous_offsets_mm": "29.5,29.75",
        },
    )
    _write_json(
        tmp_path / "1276_target0_exception_closure_policy/data/target0_exception_closure_summary.json",
        {
            "baseline_base_margin": 0.1,
            "best_spacing_base_margin": 0.2,
            "best_overall_base_margin": 0.3,
            "gpu_priority": "none",
        },
    )
    _write_json(
        tmp_path / "1277_modern_ringdown050_exception_status/data/modern_ringdown050_exception_status_summary.json",
        {"modern_ringdown050_open_count": 0, "modern_ringdown050_closed_count": 1, "gpu_priority": "none"},
    )
    _write_json(
        tmp_path / "1289_synthetic_objective_uniqueness_acquisition_gap_map/data/synthetic_objective_uniqueness_acquisition_gap_summary.json",
        {
            "target2_known_acquisition_near_tie_row_count": 6,
            "target1_known_acquisition_near_tie_row_count": 0,
        },
    )
    _write_json(
        tmp_path / "1290_synthetic_objective_uniqueness_family_gap_context/data/synthetic_objective_uniqueness_family_gap_summary.json",
        {
            "known_close14_target2_x_near_tie_count": 4,
            "target2_close50_known_near_tie_count": 0,
            "target1_legacy_archive_near_tie_count": 9,
        },
    )
    _write_json(
        tmp_path / "1291_synthetic_objective_threshold_sensitivity/data/synthetic_objective_threshold_sensitivity_summary.json",
        {
            "source5_txrx45_near_tie_count_at_scale_0p5": 2,
            "source4_txrx50_default_near_tie_count": 0,
            "near_tie_count_at_scale_1p0": 4,
            "near_tie_count_at_scale_0p5": 2,
            "source5_txrx45_near_tie_count_at_scale_1p0": 2,
        },
    )


def test_write_figure_notes_documents_next_question_matrix(tmp_path):
    summary = {
        "policy_label": "next_policy",
        "top_question_key": "synthetic_publication_bundle_current",
        "immediate_gpu_priority_count": 0,
        "gpu_priority": "none",
    }
    notes_path = tmp_path / "FIGURE_NOTES.md"

    write_figure_notes(notes_path, summary, tmp_path / "rows.csv", tmp_path / "figure_validation.csv")

    text = notes_path.read_text(encoding="utf-8")
    assert "synthetic_2d_next_question_matrix.png" in text
    assert "next_policy" in text
    assert "not a simulation result" in text


def test_candidate_rows_prefers_latest_target2_close14_gate(tmp_path):
    _write_next_matrix_inputs(tmp_path)

    rows = candidate_rows(tmp_path)

    assert rows[0]["question_key"] == "target2_close14_source5_threshold_gate"
    assert rows[0]["gpu_readiness"] == "cpu_first"
    assert rows[0]["gpu_priority"] == "none_now"
    assert "source5/TxRx45" in rows[0]["recommended_action"]
    assert any(row["question_key"] == "target1_archive_caveat_closure" for row in rows)


def test_candidate_rows_moves_to_claim_refresh_after_completed_close14_probe(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1297_synthetic_target2_close14_three_seed_probe_synthesis/data/"
        "target2_close14_three_seed_probe_summary.json",
        {
            "policy_label": "target2_close14_source5_txrx45_three_seed_persistent_x_near_tie",
            "seed_values": "13,21,34",
            "row_count": 6,
            "truth_geometry_count": 6,
            "strong_confidence_count": 6,
            "x_ambiguity_row_count": 6,
            "near_tie_count_at_scale_0p5": 6,
            "competing_geometry_x_values_mm": "265.0",
            "gpu_priority": "none_after_completed_probe",
        },
    )

    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]

    assert rows[0]["question_key"] == "post_close14_claim_boundary_refresh"
    assert rows[0]["gpu_readiness"] == "cpu_first"
    assert rows[0]["gpu_priority"] == "none_now"
    assert "do not launch more GPU work" in rows[0]["recommended_action"]
    assert "target2_close14_source5_completed_probe" in keys
    assert "target2_close14_source5_narrow_probe" not in keys

    summary = summarize_matrix(rows)

    assert summary["top_question_key"] == "post_close14_claim_boundary_refresh"
    assert "probe is complete" in summary["decision"]
    assert summary["immediate_gpu_priority_count"] == 0


def test_candidate_rows_moves_to_close50_contract_after_claim_refresh(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1297_synthetic_target2_close14_three_seed_probe_synthesis/data/"
        "target2_close14_three_seed_probe_summary.json",
        {
            "policy_label": "target2_close14_source5_txrx45_three_seed_persistent_x_near_tie",
            "seed_values": "13,21,34",
            "row_count": 6,
            "truth_geometry_count": 6,
            "strong_confidence_count": 6,
            "x_ambiguity_row_count": 6,
            "near_tie_count_at_scale_0p5": 6,
            "competing_geometry_x_values_mm": "265.0",
            "gpu_priority": "none_after_completed_probe",
        },
    )
    _write_json(
        tmp_path
        / "1299_synthetic_2d_publication_claim_boundary_refresh_post_close14_probe/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_limit_cpu_no_gpu",
            "close14_probe_included": True,
            "close14_probe_near_tie_count_at_scale_0p5": 6,
        },
    )

    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]

    assert rows[0]["question_key"] == "close50_sub30_seed_frequency_contract"
    assert rows[0]["gpu_readiness"] == "cpu_first"
    assert rows[0]["gpu_priority"] == "none_now"
    assert "seed34" in rows[0]["recommended_action"]
    assert "close50_linear29p5_seed34_frequency_probe" in keys
    assert "post_close14_claim_boundary_refresh" not in keys

    summary = summarize_matrix(rows)

    assert summary["top_question_key"] == "close50_sub30_seed_frequency_contract"
    assert "ambiguity frequency" in summary["decision"]
    assert summary["conditional_gpu_candidate_count"] == 1


def test_candidate_rows_moves_to_close50_claim_refresh_after_seed_frequency_policy(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1299_synthetic_2d_publication_claim_boundary_refresh_post_close14_probe/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_limit_cpu_no_gpu",
            "close14_probe_included": True,
            "close14_probe_near_tie_count_at_scale_0p5": 6,
        },
    )
    _write_json(
        tmp_path
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json",
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "seed_values": "seed13,seed21,seed34",
            "strict_clean_seed_count": 2,
            "strict_clean_seed_values": "seed21,seed34",
            "ambiguous_seed_count": 1,
            "ambiguous_seed_values": "seed13",
            "truth_geometry_row_count": 6,
            "strong_confidence_row_count": 6,
            "strict_clean_row_count": 5,
            "x_ambiguity_row_count": 1,
        },
    )

    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]

    assert rows[0]["question_key"] == "post_close50_claim_boundary_refresh"
    assert rows[0]["gpu_readiness"] == "cpu_first"
    assert rows[0]["gpu_priority"] == "none_now"
    assert "no GPU launch" in rows[0]["recommended_action"]
    assert "close50_linear29p5_seed_frequency_closed" in keys
    assert "close50_sub30_seed_frequency_contract" not in keys
    assert "close50_linear29p5_seed34_frequency_probe" not in keys

    summary = summarize_matrix(rows)

    assert summary["top_question_key"] == "post_close50_claim_boundary_refresh"
    assert "seed13 remains" in summary["decision"]
    assert summary["conditional_gpu_candidate_count"] == 0


def test_candidate_rows_closes_close50_after_claim_refresh(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json",
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "seed_values": "seed13,seed21,seed34",
            "strict_clean_seed_values": "seed21,seed34",
            "ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu",
            "claim_boundary_count": 9,
            "close50_seed_frequency_included": True,
            "close50_ambiguous_seed_values": "seed13",
        },
    )

    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]
    summary = summarize_matrix(rows)

    assert rows[0]["question_key"] == "synthetic_claim_boundaries_current"
    assert "close50_linear29p5_seed_frequency_closed" in keys
    assert "post_close50_claim_boundary_refresh" not in keys
    assert summary["top_question_key"] == "synthetic_claim_boundaries_current"
    assert summary["conditional_gpu_candidate_count"] == 0
    assert "No immediate or broad GPU" in summary["decision"]


def test_read_latest_publication_bundle_prefers_resolution_map_refresh(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "claim_reconciled_publication_bundle",
            "figure_count": 9,
            "validated_figure_count": 9,
            "claim_boundary_count": 11,
            "gpu_priority": "none",
        },
    )
    _write_json(
        tmp_path
        / "1320_synthetic_2d_publication_figure_bundle_post_target1_policy_refresh/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "target1_publication_bundle",
            "figure_count": 9,
            "validated_figure_count": 9,
            "claim_boundary_count": 6,
            "gpu_priority": "none",
        },
    )
    _write_json(
        tmp_path
        / "1318_synthetic_2d_publication_figure_bundle_post_28p75_replicated_midpoint_refresh/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "replicated_midpoint_publication_bundle",
            "figure_count": 7,
            "validated_figure_count": 7,
            "claim_boundary_count": 5,
            "gpu_priority": "none",
        },
    )
    _write_json(
        tmp_path
        / "1309_synthetic_2d_publication_figure_bundle_post_resolution_map_refresh/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "fresh_publication_bundle",
            "figure_count": 7,
            "validated_figure_count": 7,
            "claim_boundary_count": 5,
            "gpu_priority": "none",
        },
    )

    payload, run_name = read_latest_publication_bundle(tmp_path)

    assert run_name == "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation"
    assert payload["policy_label"] == "claim_reconciled_publication_bundle"


def test_candidate_rows_marks_current_publication_bundle_after_refresh(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json",
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "seed_values": "seed13,seed21,seed34",
            "strict_clean_seed_values": "seed21,seed34",
            "ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu",
            "claim_boundary_count": 9,
            "close50_seed_frequency_included": True,
            "close50_ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "synthetic_2d_publication_bundle_current_resolution_target1_claims_ready_gpu_priority_none",
            "figure_count": 9,
            "validated_figure_count": 9,
            "claim_boundary_count": 11,
            "gpu_priority": "none",
        },
    )

    rows = candidate_rows(tmp_path)
    summary = summarize_matrix(rows)

    assert rows[0]["question_key"] == "synthetic_publication_bundle_current"
    assert "1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation" in rows[0]["current_evidence"]
    assert summary["top_question_key"] == "synthetic_publication_bundle_current"
    assert summary["conditional_gpu_candidate_count"] == 0
    assert "paper-facing bundle" in summary["decision"]


def test_candidate_rows_includes_current_target1_acquisition_surface(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json",
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "seed_values": "seed13,seed21,seed34",
            "strict_clean_seed_values": "seed21,seed34",
            "ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu",
            "claim_boundary_count": 9,
            "close50_seed_frequency_included": True,
            "close50_ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1309_synthetic_2d_publication_figure_bundle_post_resolution_map_refresh/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none",
            "figure_count": 7,
            "validated_figure_count": 7,
            "claim_boundary_count": 5,
            "gpu_priority": "none",
        },
    )
    _write_json(
        tmp_path
        / "1312_target1_acquisition_confidence_surface/data/"
        "target1_acquisition_confidence_surface_summary.json",
        {
            "policy_label": "target1_acquisition_confidence_surface_exact_but_nonmonotonic_cpu_no_gpu",
            "target1_canonical_row_count": 133,
            "target1_exact_geometry_count": 133,
            "target1_base_weak_exact_count": 43,
            "target1_late_high_accepted_count": 132,
            "target1_late_high_truth_count": 133,
            "source_density_escalation_helped_count": 10,
            "source_density_lower_count_best_count": 7,
        },
    )

    payload, run_name = read_latest_target1_acquisition_surface(tmp_path)
    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]
    summary = summarize_matrix(rows)

    assert run_name == "1312_target1_acquisition_confidence_surface"
    assert payload["target1_base_weak_exact_count"] == 43
    assert "target1_acquisition_confidence_surface_current" in keys
    target1_row = next(row for row in rows if row["question_key"] == "target1_acquisition_confidence_surface_current")
    assert target1_row["gpu_readiness"] == "no_gpu_required"
    assert target1_row["gpu_priority"] == "none"
    assert "weak_exact=43" in target1_row["current_evidence"]
    assert summary["target1_acquisition_surface_included"] is True
    assert summary["conditional_gpu_candidate_count"] == 0
    assert "source-density behavior is nonmonotonic" in summary["decision"]


def test_candidate_rows_includes_target1_source_density_exception_map(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json",
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "seed_values": "seed13,seed21,seed34",
            "strict_clean_seed_values": "seed21,seed34",
            "ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu",
            "claim_boundary_count": 9,
            "close50_seed_frequency_included": True,
            "close50_ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1309_synthetic_2d_publication_figure_bundle_post_resolution_map_refresh/data/"
        "synthetic_2d_publication_figure_bundle_summary.json",
        {
            "policy_label": "synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none",
            "figure_count": 7,
            "validated_figure_count": 7,
            "claim_boundary_count": 5,
            "gpu_priority": "none",
        },
    )
    _write_json(
        tmp_path
        / "1314_target1_source_density_exception_map/data/"
        "target1_source_density_exception_map_summary.json",
        {
            "policy_label": "target1_source_density_exception_map_no_gpu",
            "source_density_series_count": 17,
            "modern_exception_series_count": 0,
            "legacy_exception_series_count": 1,
            "terminal_11_worse_count": 2,
            "terminal_11_series_count": 2,
            "recommended_gpu_action": "none_target1_source_density",
        },
    )

    payload, run_name = read_latest_target1_source_density_exception_map(tmp_path)
    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]
    summary = summarize_matrix(rows)

    assert run_name == "1314_target1_source_density_exception_map"
    assert payload["modern_exception_series_count"] == 0
    assert "target1_source_density_exception_map_current" in keys
    target1_row = next(row for row in rows if row["question_key"] == "target1_source_density_exception_map_current")
    assert target1_row["gpu_readiness"] == "closed"
    assert target1_row["gpu_priority"] == "none"
    assert "modern_exceptions=0" in target1_row["current_evidence"]
    assert "gpu_action=none_target1_source_density" in target1_row["current_evidence"]
    assert summary["target1_exception_map_included"] is True
    assert summary["conditional_gpu_candidate_count"] == 0
    assert "zero modern exceptions" in summary["decision"]


def test_candidate_rows_includes_completed_matched_source3_policy(tmp_path):
    _write_next_matrix_inputs(tmp_path)
    _write_json(
        tmp_path
        / "1303_close50_linear29p5_three_seed_frequency_policy/data/"
        "close50_linear_receiver_policy_summary.json",
        {
            "policy_label": "close50_linear29p5_three_seed_exact_strong_not_clean_replicated",
            "seed_count": 3,
            "seed_values": "seed13,seed21,seed34",
            "strict_clean_seed_values": "seed21,seed34",
            "ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "1305_synthetic_2d_publication_claim_boundary_refresh_post_close50_seed_frequency/data/"
        "synthetic_2d_publication_claim_boundary_refresh_summary.json",
        {
            "policy_label": "synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu",
            "claim_boundary_count": 9,
            "close50_seed_frequency_included": True,
            "close50_ambiguous_seed_values": "seed13",
        },
    )
    _write_json(
        tmp_path
        / "summary_tables/121_close_spacing_matched_source3_policy_synthesis/data/"
        "close_spacing_matched_source3_policy_summary.json",
        {
            "policy_label": "close_spacing_matched_source3_policy_synthesis",
            "close14_truth_geometry_fraction": 1.0,
            "close50_truth_geometry_fraction": 0.0,
            "close50_replicated_wrong_branch": True,
            "spacing_only_causal_generalization_ready": False,
            "gpu_priority": "none",
        },
    )

    payload, run_name = read_latest_matched_source3_policy(tmp_path)
    rows = candidate_rows(tmp_path)
    keys = [row["question_key"] for row in rows]
    summary = summarize_matrix(rows)

    assert run_name == "121_close_spacing_matched_source3_policy_synthesis"
    assert payload["close50_replicated_wrong_branch"] is True
    assert "matched_source3_acquisition_geometry_contrast_closed" in keys
    matched_row = next(row for row in rows if row["question_key"] == "matched_source3_acquisition_geometry_contrast_closed")
    assert matched_row["gpu_readiness"] == "closed"
    assert matched_row["gpu_priority"] == "none"
    assert "close50_truth_fraction=0.0" in matched_row["current_evidence"]
    assert summary["matched_source3_policy_included"] is True
    assert summary["conditional_gpu_candidate_count"] == 0
    assert "not a spacing-only causal claim" in summary["decision"]


def test_summarize_matrix_prefers_cpu_first_without_immediate_gpu():
    rows = [
        {
            "question_key": "x_ambiguity_objective_design",
            "gpu_readiness": "cpu_first",
            "gpu_priority": "none_now",
            "recommended_action": "Design objective first.",
            "priority_score": 0.6,
        },
        {
            "question_key": "conditional_probe",
            "gpu_readiness": "conditional_after_objective_scope",
            "gpu_priority": "low_conditional",
            "recommended_action": "Only if paper requires it.",
            "priority_score": 0.4,
        },
        {
            "question_key": "closed_exception",
            "gpu_readiness": "closed",
            "gpu_priority": "none",
            "recommended_action": "No action.",
            "priority_score": 0.1,
        },
    ]

    summary = summarize_matrix(rows)

    assert summary["policy_label"] == "synthetic_2d_next_question_matrix_cpu_first_no_gpu"
    assert summary["top_question_key"] == "x_ambiguity_objective_design"
    assert summary["top_question_gpu_readiness"] == "cpu_first"
    assert summary["immediate_gpu_priority_count"] == 0
    assert summary["open_immediate_gpu_rows"] == 0
    assert summary["conditional_gpu_candidate_count"] == 1
    assert summary["gpu_priority"] == "none_now"
    assert summary["target1_acquisition_surface_included"] is False


def test_summarize_matrix_counts_cpu_first_candidates():
    rows = [
        {
            "question_key": "a",
            "gpu_readiness": "cpu_first",
            "gpu_priority": "none_now",
            "recommended_action": "A",
            "priority_score": 0.2,
        },
        {
            "question_key": "b",
            "gpu_readiness": "cpu_first",
            "gpu_priority": "none_now",
            "recommended_action": "B",
            "priority_score": 0.1,
        },
    ]

    summary = summarize_matrix(rows)

    assert summary["candidate_count"] == 2
    assert summary["cpu_first_count"] == 2
