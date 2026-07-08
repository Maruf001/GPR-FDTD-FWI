from run_close_spacing_matched_source3_policy_synthesis import (
    build_claim_rows,
    build_family_rows,
    gate_rows,
    synthesize_policy,
)


def _aggregate(run_name, *, txrx, target2_x, truth_count, confidence_counts, selected_x, selected_r):
    row_count = 6
    rows = []
    for seed in (13, 21, 34):
        for case_label in (f"noise10_seed{seed}", f"source_mismatch_noise10_seed{seed}"):
            rows.append(
                {
                    "run_name": run_name,
                    "case_label": case_label,
                    "sources": 3,
                    "tx_rx_offset_mm": txrx,
                    "truth_x_mm": target2_x,
                    "truth_z_mm": 90.0,
                    "truth_radius_mm": 8.0,
                    "best_x_mm": selected_x,
                    "best_z_mm": 90.0,
                    "best_radius_mm": selected_r,
                    "is_truth_geometry": selected_x == target2_x and selected_r == 8.0,
                    "confidence_label": "strong",
                    "radius_margin_abs": 0.003 if selected_x == target2_x else 0.001,
                }
            )
    return {
        "run_name": run_name,
        "input_summary_json": [],
        "aggregate": {
            "row_count": row_count,
            "truth_geometry_count": truth_count,
            "confidence_label_counts": confidence_counts,
            "fallback_warning_count": 0,
            "radius_margin_abs_min": 0.003 if truth_count else 0.0007,
            "radius_margin_abs_mean": 0.0035 if truth_count else 0.0009,
            "radius_margin_abs_max": 0.004 if truth_count else 0.0011,
            "ambiguity_x_width_max_mm": 2.0 if truth_count else 0.0,
            "ambiguity_radius_width_max_mm": 0.0,
            "x_ambiguity_row_count": 6 if truth_count else 0,
        },
        "rows": rows,
    }


def test_matched_source3_synthesis_blocks_spacing_only_and_gpu_queue():
    close14 = _aggregate(
        "close14",
        txrx=40,
        target2_x=264,
        truth_count=6,
        confidence_counts={"strong": 6},
        selected_x=264,
        selected_r=8.0,
    )
    close50 = _aggregate(
        "close50",
        txrx=45,
        target2_x=300,
        truth_count=0,
        confidence_counts={"moderate": 4, "strong": 2},
        selected_x=299,
        selected_r=7.5,
    )
    family_rows = build_family_rows(close14, close50)
    claims = build_claim_rows(
        family_rows,
        {"missing_seed_probe_count": 0},
        {"acquisition_confound_count": 1, "geometry_confound_count": 1, "metadata_gap_count": 1},
    )
    summary = synthesize_policy(family_rows, claims)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["queue_complete"] is True
    assert summary["close14_all_truth_strong"] is True
    assert summary["close50_replicated_wrong_branch"] is True
    assert summary["guarded_acquisition_geometry_contrast_ready"] is True
    assert summary["spacing_only_causal_generalization_ready"] is False
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["gpu_priority"] == "none"
    assert gates["paper_guarded_matched_source3_contrast"]["ready"] is True
    assert gates["spacing_only_causal_claim"]["ready"] is False
    assert gates["broad_gpu_queue"]["ready"] is False


def test_matched_source3_family_rows_capture_repeated_wrong_branch():
    close14 = _aggregate(
        "close14",
        txrx=40,
        target2_x=264,
        truth_count=6,
        confidence_counts={"strong": 6},
        selected_x=264,
        selected_r=8.0,
    )
    close50 = _aggregate(
        "close50",
        txrx=45,
        target2_x=300,
        truth_count=0,
        confidence_counts={"moderate": 4, "strong": 2},
        selected_x=299,
        selected_r=7.5,
    )

    rows = {row["family_key"]: row for row in build_family_rows(close14, close50)}

    assert rows["close14_source3_txrx40"]["all_rows_truth"] is True
    assert rows["close50_source3_txrx45"]["all_rows_nontruth"] is True
    assert rows["close50_source3_txrx45"]["all_rows_same_selected_branch"] is True
    assert rows["close50_source3_txrx45"]["dominant_selected_branch"] == "x=299 mm, z=90 mm, r=7.5 mm"
