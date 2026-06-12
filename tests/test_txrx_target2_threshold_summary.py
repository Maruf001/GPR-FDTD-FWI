from run_txrx_target2_threshold_summary import (
    attach_baseline_and_duplicate_fields,
    parse_run_arg,
    receiver_layout,
    summarize_threshold_rows,
)


SCAN_X_MM = [50.0, 146.0, 250.0, 346.0, 450.0]


def _row(label, txrx, layout_key, dominant_cells, margin, confidence):
    return {
        "label": label,
        "tx_rx_offset_mm": txrx,
        "receiver_layout_key": layout_key,
        "dominant_unclamped_receiver_offset_cells": dominant_cells,
        "base_radius_margin_abs": margin,
        "base_confidence_label": confidence,
        "best_truth_preserving_objective": "late_high",
        "target_index": 2,
        "base_is_truth_geometry": True,
    }


def test_parse_run_arg_splits_label_and_directory():
    label, path = parse_run_arg("txrx50=outputs/experiments/run")

    assert label == "txrx50"
    assert str(path) == "outputs/experiments/run"


def test_receiver_layout_quantizes_fractional_offsets_on_one_mm_grid():
    below_half = receiver_layout(
        SCAN_X_MM,
        50.3125,
        1.0,
        pml_thickness_mm=30.0,
        domain_x_mm=500.0,
    )
    first_plus_one = receiver_layout(
        SCAN_X_MM,
        50.625,
        1.0,
        pml_thickness_mm=30.0,
        domain_x_mm=500.0,
    )
    same_plus_one = receiver_layout(
        SCAN_X_MM,
        51.25,
        1.0,
        pml_thickness_mm=30.0,
        domain_x_mm=500.0,
    )

    assert below_half["receiver_offsets_cells"] == [50, 50, 50, 50, 49]
    assert below_half["dominant_unclamped_receiver_offset_cells"] == 50
    assert below_half["clamped_receiver_count"] == 1
    assert first_plus_one["receiver_offsets_cells"] == [51, 51, 51, 51, 49]
    assert first_plus_one["dominant_unclamped_receiver_offset_cells"] == 51
    assert first_plus_one["receiver_layout_key"] == same_plus_one["receiver_layout_key"]


def test_attach_baseline_marks_duplicate_receiver_layouts():
    rows = [
        _row("txrx50", 50.0, "50,50,50,50,49", 50, 1.0e-3, "moderate"),
        _row("txrx50p625", 50.625, "51,51,51,51,49", 51, 4.8e-4, "weak"),
        _row("txrx51p25", 51.25, "51,51,51,51,49", 51, 4.8e-4, "weak"),
    ]

    enriched = attach_baseline_and_duplicate_fields(rows, "txrx50")
    by_label = {row["label"]: row for row in enriched}

    assert by_label["txrx50"]["base_margin_ratio_to_baseline"] == 1.0
    assert by_label["txrx50"]["same_receiver_layout_as_baseline"] is True
    assert by_label["txrx50p625"]["same_receiver_layout_as_baseline"] is False
    assert by_label["txrx50p625"]["layout_duplicate_count"] == 2
    assert by_label["txrx50p625"]["layout_duplicate_tx_rx_offsets_mm"] == "50.625;51.25"


def test_summarize_threshold_rows_finds_cell_transition():
    rows = attach_baseline_and_duplicate_fields([
        _row("txrx50", 50.0, "50,50,50,50,49", 50, 1.0e-3, "moderate"),
        _row("txrx50p625", 50.625, "51,51,51,51,49", 51, 4.8e-4, "weak"),
        _row("txrx52p5", 52.5, "52,52,52,52,49", 52, 4.7e-4, "weak"),
    ], "txrx50")

    summary = summarize_threshold_rows(rows, "txrx50")

    assert summary["run_count"] == 3
    assert summary["all_base_truth_geometry"] is True
    assert summary["confidence_label_counts"] == {"moderate": 1, "weak": 2}
    assert summary["unique_receiver_layout_count"] == 3
    assert summary["moderate_to_weak_transition"]["from_effective_receiver_offset_cells"] == 50
    assert summary["moderate_to_weak_transition"]["to_effective_receiver_offset_cells"] == 51
