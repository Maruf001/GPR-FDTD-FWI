import pytest

from run_linear_receiver_threshold_summary import (
    attach_baseline_fields,
    parse_run_arg,
    receiver_sampling_layout,
    summarize_rows,
)


SCAN_X_MM = [50.0, 146.00000000000003, 250.0, 346.0, 450.0]


def _row(label, sampling, delta, margin, confidence):
    return {
        "label": label,
        "receiver_sampling": sampling,
        "mean_effective_receiver_offset_cells": 50.0 + delta,
        "base_radius_margin_abs": margin,
        "base_confidence_label": confidence,
        "best_truth_preserving_objective": "late_high",
    }


def test_parse_run_arg_splits_label_and_path():
    label, path = parse_run_arg("linear=outputs/experiments/run")

    assert label == "linear"
    assert str(path) == "outputs/experiments/run"


def test_receiver_sampling_layout_reduces_integer_linear_offset_to_baseline():
    layout = receiver_sampling_layout(
        SCAN_X_MM,
        50.0,
        1.0,
        "linear",
        pml_thickness_mm=30.0,
        domain_x_mm=500.0,
    )

    assert layout["clamped_receiver_count"] == 1
    assert layout["mean_effective_receiver_offset_cells"] == pytest.approx(50.0)


def test_receiver_sampling_layout_tracks_nonzero_linear_delta():
    layout = receiver_sampling_layout(
        SCAN_X_MM,
        50.078125,
        1.0,
        "linear",
        pml_thickness_mm=30.0,
        domain_x_mm=500.0,
    )

    assert layout["clamped_receiver_count"] == 1
    assert layout["mean_effective_receiver_offset_cells"] == pytest.approx(50.078125)
    assert layout["mean_receiver_weight_right"] == pytest.approx(0.078125)


def test_attach_baseline_and_summary_identify_nonzero_weak_rows():
    rows = attach_baseline_fields([
        _row("nearest50", "nearest", 0.0, 1.0e-3, "moderate"),
        _row("linear50p078125", "linear", 0.078125, 4.8e-4, "weak"),
        _row("linear50p15625", "linear", 0.15625, 4.8e-4, "weak"),
    ], "nearest50")

    summary = summarize_rows(rows)

    assert rows[0]["base_margin_ratio_to_baseline"] == 1.0
    assert rows[1]["effective_offset_delta_from_baseline_cells"] == pytest.approx(0.078125)
    assert summary["linear_nonzero_count"] == 2
    assert summary["all_nonzero_linear_weak"] is True
    assert summary["smallest_tested_nonzero_delta_cells"] == pytest.approx(0.078125)
