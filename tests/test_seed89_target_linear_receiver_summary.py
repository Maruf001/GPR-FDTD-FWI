import pytest

from run_seed89_target_linear_receiver_summary import (
    attach_target_baselines,
    summarize_rows,
)


def _row(label, target, sampling, txrx, offset, margin, confidence):
    return {
        "label": label,
        "target_index": target,
        "run_index": None,
        "receiver_sampling": sampling,
        "tx_rx_offset_mm": txrx,
        "mean_effective_receiver_offset_cells": offset,
        "base_radius_margin_abs": margin,
        "base_confidence_label": confidence,
        "best_truth_preserving_objective": "late_high",
    }


def test_attach_target_baselines_normalizes_per_target():
    rows = attach_target_baselines([
        _row("target0_nearest50", 0, "nearest", 50.0, 50.0, 5.8e-4, "moderate"),
        _row("target0_linear50p3125", 0, "linear", 50.3125, 50.3125, 5.8e-4, "moderate"),
        _row("target2_nearest50", 2, "nearest", 50.0, 50.0, 9.9e-4, "moderate"),
        _row("target2_linear50p3125", 2, "linear", 50.3125, 50.3125, 4.8e-4, "weak"),
    ])

    target0_linear = next(row for row in rows if row["label"] == "target0_linear50p3125")
    target2_linear = next(row for row in rows if row["label"] == "target2_linear50p3125")

    assert target0_linear["base_margin_ratio_to_target_baseline"] == pytest.approx(1.0)
    assert target2_linear["base_margin_ratio_to_target_baseline"] == pytest.approx(0.484848, rel=1e-5)
    assert target0_linear["effective_offset_delta_from_target_baseline_cells"] == pytest.approx(0.3125)
    assert target2_linear["effective_offset_delta_from_target_baseline_cells"] == pytest.approx(0.3125)


def test_summarize_rows_identifies_target2_as_only_weak_linear_target():
    rows = attach_target_baselines([
        _row("target0_nearest50", 0, "nearest", 50.0, 50.0, 5.8e-4, "moderate"),
        _row("target0_linear50p3125", 0, "linear", 50.3125, 50.3125, 5.8e-4, "moderate"),
        _row("target1_nearest50", 1, "nearest", 50.0, 50.0, 6.0e-4, "moderate"),
        _row("target1_linear50p3125", 1, "linear", 50.3125, 50.3125, 6.0e-4, "moderate"),
        _row("target2_nearest50", 2, "nearest", 50.0, 50.0, 9.9e-4, "moderate"),
        _row("target2_linear50p3125", 2, "linear", 50.3125, 50.3125, 4.8e-4, "weak"),
    ])

    summary = summarize_rows(rows)

    assert summary["target_count"] == 3
    assert summary["weak_linear_targets"] == [2]
    assert summary["moderate_linear_targets"] == [0, 1]
    assert summary["linear_confidence_label_counts"] == {"moderate": 2, "weak": 1}
