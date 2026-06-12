import pytest

from run_cross_seed_linear_receiver_summary import (
    attach_seed_baselines,
    extract_seed_label,
    summarize_rows,
)


def _row(label, sampling, txrx, offset, margin, confidence):
    return {
        "label": label,
        "run_name": f"run_{label}",
        "run_path": f"outputs/experiments/{label}",
        "run_index": None,
        "receiver_sampling": sampling,
        "tx_rx_offset_mm": txrx,
        "mean_effective_receiver_offset_cells": offset,
        "base_radius_margin_abs": margin,
        "base_confidence_label": confidence,
        "best_truth_preserving_objective": "late_high",
    }


def test_extract_seed_label_from_label():
    assert extract_seed_label({"label": "seed89_linear50p3125"}) == "seed89"


def test_attach_seed_baselines_normalizes_each_seed_separately():
    rows = attach_seed_baselines([
        _row("seed21_nearest50", "nearest", 50.0, 50.0, 8.0e-4, "moderate"),
        _row("seed21_linear50p3125", "linear", 50.3125, 50.3125, 5.8e-4, "moderate"),
        _row("seed89_nearest50", "nearest", 50.0, 50.0, 9.9e-4, "moderate"),
        _row("seed89_linear50p3125", "linear", 50.3125, 50.3125, 4.8e-4, "weak"),
    ])

    seed21_linear = next(row for row in rows if row["label"] == "seed21_linear50p3125")
    seed89_linear = next(row for row in rows if row["label"] == "seed89_linear50p3125")

    assert seed21_linear["base_margin_ratio_to_seed_baseline"] == pytest.approx(0.725)
    assert seed89_linear["base_margin_ratio_to_seed_baseline"] == pytest.approx(0.484848, rel=1e-5)
    assert seed21_linear["effective_offset_delta_from_seed_baseline_cells"] == pytest.approx(0.3125)
    assert seed89_linear["effective_offset_delta_from_seed_baseline_cells"] == pytest.approx(0.3125)


def test_summarize_rows_reports_mixed_seed_classification():
    rows = attach_seed_baselines([
        _row("seed13_nearest50", "nearest", 50.0, 50.0, 8.1e-4, "moderate"),
        _row("seed13_linear50p3125", "linear", 50.3125, 50.3125, 6.0e-4, "moderate"),
        _row("seed21_nearest50", "nearest", 50.0, 50.0, 8.0e-4, "moderate"),
        _row("seed21_linear50p0390625", "linear", 50.0390625, 50.0390625, 5.8e-4, "moderate"),
        _row("seed89_nearest50", "nearest", 50.0, 50.0, 9.9e-4, "moderate"),
        _row("seed89_linear50p0390625", "linear", 50.0390625, 50.0390625, 4.8e-4, "weak"),
    ])

    summary = summarize_rows(rows)

    assert summary["seed_count"] == 3
    assert summary["all_seed13_nonzero_linear_moderate"] is True
    assert summary["all_seed21_nonzero_linear_moderate"] is True
    assert summary["all_seed89_nonzero_linear_weak"] is True
    assert summary["seed_summaries"]["seed13"]["nonzero_linear_confidence_label_counts"] == {"moderate": 1}
    assert summary["seed_summaries"]["seed21"]["nonzero_linear_confidence_label_counts"] == {"moderate": 1}
    assert summary["seed_summaries"]["seed89"]["nonzero_linear_confidence_label_counts"] == {"weak": 1}
