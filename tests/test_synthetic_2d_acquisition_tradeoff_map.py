from run_synthetic_2d_acquisition_tradeoff_map import (
    best_target_source_rows,
    best_target_txrx_rows,
    build_tradeoff_rows,
    summarize_tradeoffs,
)


def _by_txrx_rows():
    return [
        {
            "tx_rx_offset_mm": "35.0",
            "tested_spacing_count": "6",
            "clean_spacing_count": "5",
            "closest_clean_spacing_mm": "30.0",
        },
        {
            "tx_rx_offset_mm": "45.0",
            "tested_spacing_count": "5",
            "clean_spacing_count": "5",
            "closest_clean_spacing_mm": "14.0",
        },
    ]


def _by_spacing_rows():
    return [
        {
            "close_spacing_mm": "14.0",
            "minimum_clean_tx_rx_offset_mm": "45.0",
        }
    ]


def _txrx_target_rows():
    return [
        {"target": "0", "tx_rx_offset_mm": "50.0", "run_count": "7", "accepted_fraction": "0.85", "median_margin": "0.00051"},
        {"target": "0", "tx_rx_offset_mm": "52.5", "run_count": "14", "accepted_fraction": "0.57", "median_margin": "0.00050"},
        {"target": "1", "tx_rx_offset_mm": "52.5", "run_count": "14", "accepted_fraction": "0.64", "median_margin": "0.000506"},
        {"target": "1", "tx_rx_offset_mm": "60.0", "run_count": "105", "accepted_fraction": "0.71", "median_margin": "0.000525"},
        {"target": "2", "tx_rx_offset_mm": "50.0", "run_count": "12", "accepted_fraction": "0.92", "median_margin": "0.00159"},
        {"target": "2", "tx_rx_offset_mm": "60.0", "run_count": "142", "accepted_fraction": "0.53", "median_margin": "0.00050"},
    ]


def _source_rows():
    return [
        {"target": "0", "sources": "5", "run_count": "6", "accepted_fraction": "1.0", "median_margin": "0.00056"},
        {"target": "0", "sources": "9", "run_count": "15", "accepted_fraction": "0.47", "median_margin": "0.00050"},
        {"target": "1", "sources": "5", "run_count": "101", "accepted_fraction": "0.72", "median_margin": "0.00053"},
        {"target": "1", "sources": "9", "run_count": "25", "accepted_fraction": "0.68", "median_margin": "0.00051"},
        {"target": "1", "sources": "11", "run_count": "2", "accepted_fraction": "0.0", "median_margin": "0.00038"},
        {"target": "2", "sources": "4", "run_count": "9", "accepted_fraction": "0.89", "median_margin": "0.00163"},
        {"target": "2", "sources": "9", "run_count": "42", "accepted_fraction": "0.64", "median_margin": "0.00052"},
    ]


def test_best_target_txrx_rows_are_target_specific():
    best = best_target_txrx_rows(_txrx_target_rows())
    by_target = {row["target_label"]: row for row in best}

    assert by_target["target0"]["best_tx_rx_offset_mm"] == 50.0
    assert by_target["target1"]["best_tx_rx_offset_mm"] == 60.0
    assert by_target["target2"]["best_tx_rx_offset_mm"] == 50.0
    assert by_target["target2"]["accepted_fraction"] == 0.92


def test_best_target_source_rows_detect_nonmonotonic_source_density():
    best = best_target_source_rows(_source_rows())
    by_target = {row["target_label"]: row for row in best}

    assert by_target["target1"]["best_source_count"] == 5
    assert by_target["target1"]["is_nonmonotonic"] is True
    assert by_target["target2"]["best_source_count"] == 4
    assert by_target["target2"]["status"] == "source_density_nonmonotonic"


def test_tradeoff_summary_keeps_gpu_priority_none():
    next_matrix = {"candidate_count": 8, "conditional_gpu_candidate_count": 0}
    rows = build_tradeoff_rows(_by_txrx_rows(), _txrx_target_rows(), _source_rows(), next_matrix)
    summary = summarize_tradeoffs(rows, _by_spacing_rows(), next_matrix)
    row_keys = {row["tradeoff_key"] for row in rows}

    assert "resolution_txrx_45" in row_keys
    assert "target1_source_density" in row_keys
    assert summary["policy_label"] == "synthetic_2d_acquisition_tradeoff_cpu_no_gpu"
    assert summary["tight_spacing_reference_txrx_mm"] == 45.0
    assert summary["close14_minimum_clean_txrx_mm"] == 45.0
    assert summary["source_density_nonmonotonic_target_count"] == 3
    assert summary["conditional_gpu_candidate_count"] == 0
    assert summary["gpu_priority"] == "none_now"
