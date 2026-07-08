from run_close14_source3_three_seed_policy_synthesis import (
    gate_rows,
    summarize_by_source,
    summarize_policy,
)


def _row(source_count, seed, truth_geometry, confidence_label, x_error=0.0, radius_error=0.0):
    return {
        "spacing_family": "close14",
        "spacing_mm": 14.0,
        "target_rebar_index": 2,
        "source_count": source_count,
        "source_family": "test",
        "source_path": "test.csv",
        "run_name": "test_run",
        "case_label": f"noise10_seed{seed}",
        "case_kind": "nominal",
        "seed": seed,
        "tx_rx_offset_mm": 45.0,
        "best_x_mm": 264.0 + x_error,
        "best_z_mm": 90.0,
        "best_radius_mm": 8.0 + radius_error,
        "truth_x_mm": 264.0,
        "truth_z_mm": 90.0,
        "truth_radius_mm": 8.0,
        "x_abs_error_mm": abs(x_error),
        "z_abs_error_mm": 0.0,
        "radius_abs_error_mm": abs(radius_error),
        "truth_geometry": truth_geometry,
        "confidence_label": confidence_label,
        "radius_margin_abs": 0.002 if confidence_label == "strong" else 0.0001,
        "best_misfit": 0.03,
        "competing_geometry_x_mm": 265.0,
        "competing_geometry_radius_mm": 8.0,
        "ambiguity_candidate_count": 2,
        "ambiguity_x_width_mm": abs(x_error),
        "ambiguity_radius_width_mm": abs(radius_error),
    }


def test_close14_source3_near_exact_context_is_not_replicated_failure():
    rows = []
    for seed in [13, 21]:
        rows.append(_row(3, seed, True, "strong"))
        rows.append(_row(3, seed, True, "strong"))
    rows.append(_row(3, 34, True, "strong"))
    rows.append(_row(3, 34, False, "strong", x_error=1.0))
    for source_count in [4, 5]:
        for seed in [13, 21, 34]:
            rows.append(_row(source_count, seed, True, "strong"))
            rows.append(_row(source_count, seed, True, "strong"))

    by_source = summarize_by_source(rows)
    summary = summarize_policy(rows, by_source)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["source3_seed_count"] == 3
    assert summary["source3_truth_geometry_fraction"] == 5 / 6
    assert summary["source3_strong_fraction"] == 1.0
    assert summary["source3_near_exact_three_seed_context"] is True
    assert summary["source3_replicated_failure"] is False
    assert summary["source4_three_seed_clean"] is True
    assert summary["source5_noise_boundary_three_seed_clean"] is True
    assert summary["close14_source3_additional_replicate_needed"] is False
    assert gates["additional_close14_source3_replicate"]["ready"] is False
    assert gates["broad_gpu_queue"]["ready"] is False


def test_all_wrong_weak_source3_would_be_separate_replicated_failure():
    rows = []
    for seed in [13, 21, 34]:
        rows.append(_row(3, seed, False, "weak", x_error=1.0, radius_error=-0.5))
        rows.append(_row(3, seed, False, "weak", x_error=1.0, radius_error=-0.5))

    summary = summarize_policy(rows, summarize_by_source(rows))

    assert summary["source3_near_exact_three_seed_context"] is False
    assert summary["source3_replicated_failure"] is True
    assert summary["ready_for_broad_gpu_queue"] is False
    assert summary["gpu_priority"] == "none"
