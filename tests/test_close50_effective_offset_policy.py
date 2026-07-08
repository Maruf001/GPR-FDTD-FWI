import pytest

from run_close50_effective_offset_policy import (
    effective_offsets_from_positions,
    summarize_effective_offset_policy,
)


def test_effective_offsets_from_nearest_positions_detects_duplicate_signature():
    layout = effective_offsets_from_positions(
        [
            (0, 80, 0, 109),
            (0, 208, 0, 237),
            (0, 344, 0, 373),
            (0, 480, 0, 509),
        ],
        1.0,
    )

    assert layout["effective_receiver_offsets_mm"] == [29.0, 29.0, 29.0, 29.0]
    assert layout["mean_effective_receiver_offset_mm"] == pytest.approx(29.0)
    assert layout["unique_effective_receiver_offset_count"] == 1
    assert layout["receiver_signature"] == "109|237|373|509"


def test_effective_offsets_from_linear_positions_preserves_subcell_offset():
    layout = effective_offsets_from_positions(
        [
            (0, 80, 0, 109, 110, 0.375),
            (0, 208, 0, 237, 238, 0.375),
        ],
        1.0,
    )

    assert layout["effective_receiver_offsets_mm"] == pytest.approx([29.375, 29.375])
    assert layout["receiver_signature"] == "109:110:0.375000000|237:238:0.375000000"


def test_summarize_effective_offset_policy_stops_nearest_bisection():
    rows = [
        {
            "requested_tx_rx_offset_mm": 28.75,
            "mean_effective_receiver_offset_mm": 29.0,
            "branch_policy_label": "single_seed_exact_but_nonclean",
            "duplicate_effective_layout": False,
        },
        {
            "requested_tx_rx_offset_mm": 29.375,
            "mean_effective_receiver_offset_mm": 29.0,
            "branch_policy_label": "duplicate_effective_geometry_check",
            "duplicate_effective_layout": True,
        },
        {
            "requested_tx_rx_offset_mm": 30.0,
            "mean_effective_receiver_offset_mm": 30.0,
            "branch_policy_label": "clean_replicated",
            "duplicate_effective_layout": False,
        },
    ]

    summary = summarize_effective_offset_policy(rows)

    assert summary["policy_label"] == "close50_nearest_receiver_bisection_quantized_stop"
    assert summary["duplicate_effective_layout_count"] == 1
    assert summary["duplicate_requested_tx_rx_offsets_mm"] == "29.375"
    assert summary["first_clean_mean_effective_offset_mm"] == 30.0
    assert "Stop nearest-sampled sub-millimeter bisection" in summary["next_action"]
