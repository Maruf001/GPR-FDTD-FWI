from run_close50_source_count_replicate_synthesis import (
    gate_rows,
    summarize_by_source,
    summarize_policy,
)


def _row(source_count, seed, truth_geometry, confidence_label, x_error):
    return {
        "source_count": source_count,
        "seed": seed,
        "case_label": f"noise10_seed{seed}",
        "case_kind": "nominal",
        "run_dir": "",
        "source_family": "test",
        "tx_rx_offset_mm": 40.0,
        "best_x_mm": 300.0 - x_error,
        "best_z_mm": 90.0,
        "best_radius_mm": 8.0 if truth_geometry else 7.5,
        "truth_x_mm": 300.0,
        "truth_z_mm": 90.0,
        "truth_radius_mm": 8.0,
        "x_abs_error_mm": x_error,
        "radius_abs_error_mm": 0.0 if truth_geometry else 0.5,
        "truth_geometry": truth_geometry,
        "confidence_label": confidence_label,
        "radius_margin_abs": 0.002 if confidence_label == "strong" else 0.0001,
        "best_misfit": 0.03,
    }


def test_synthesis_allows_one_final_source3_seed21_replicate():
    rows = []
    for seed in [13, 34]:
        rows.append(_row(3, seed, False, "weak", 1.0))
        rows.append(_row(3, seed, False, "weak", 1.0))
    for source_count in [4, 5]:
        for seed in [13, 21, 34]:
            rows.append(_row(source_count, seed, True, "strong", 0.0))
            rows.append(_row(source_count, seed, True, "strong", 0.0))

    by_source = summarize_by_source(rows)
    summary = summarize_policy(rows, by_source)
    gates = {row["gate_key"]: row for row in gate_rows(summary)}

    assert summary["source3_replicated_failure"] is True
    assert summary["source4_three_seed_clean"] is True
    assert summary["source5_three_seed_clean"] is True
    assert summary["missing_source3_seed_values"] == "21"
    assert summary["ready_for_final_source3_seed21_replicate"] is True
    assert gates["final_source3_seed21_replicate"]["ready"] is True
    assert gates["broad_gpu_queue"]["ready"] is False


def test_synthesis_blocks_final_seed_when_source3_already_has_three_seeds():
    rows = []
    for seed in [13, 21, 34]:
        rows.append(_row(3, seed, False, "weak", 1.0))
        rows.append(_row(3, seed, False, "weak", 1.0))
    for source_count in [4, 5]:
        for seed in [13, 21, 34]:
            rows.append(_row(source_count, seed, True, "strong", 0.0))
            rows.append(_row(source_count, seed, True, "strong", 0.0))

    summary = summarize_policy(rows, summarize_by_source(rows))

    assert summary["source3_replicated_failure"] is True
    assert summary["missing_source3_seed_values"] == ""
    assert summary["ready_for_final_source3_seed21_replicate"] is False
    assert summary["gpu_priority"] == "none"
