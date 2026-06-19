import pytest

from run_close50_linear_receiver_policy import (
    confidence_detail_rows,
    row_matches_truth,
    summarize_policy,
)


def _confidence_row(case_label, *, x_width=0.0, confidence_label="strong"):
    return {
        "case_label": case_label,
        "target_rebar_index": 2,
        "step_target_index": 2,
        "best_x_mm": 300.0,
        "best_z_mm": 90.0,
        "best_radius_mm": 8.0,
        "radius_margin_abs": 0.0015,
        "confidence_label": confidence_label,
        "ambiguity_x_min_mm": 300.0,
        "ambiguity_x_max_mm": 300.0 + x_width,
        "ambiguity_radius_min_mm": 8.0,
        "ambiguity_radius_max_mm": 8.0,
    }


def _summary(seed, rows):
    return {
        "run_name": f"coordinate_optimizer_close50_{seed}_sources4_txrx29p5_linear_receiver_objectives",
        "receiver_sampling": "linear",
        "tx_rx_offset_mm": 29.5,
        "sources": 4,
        "true_x_values_mm": [190.0, 250.0, 300.0],
        "true_z_values_mm": [90.0, 90.0, 90.0],
        "truth_radius_values_mm": [5.0, 6.0, 8.0],
        "confidence_rows": rows,
    }


def _diagnostic_rows(seed, count=2):
    return [
        {
            "seed_label": seed,
            "objective_label": "highband",
            "truth_geometry_match": True,
            "radius_margin_abs": 0.0012,
        }
        for _ in range(count)
    ]


def test_row_matches_target_index_truth():
    summary = _summary("seed21", [_confidence_row("noise10_seed21")])

    assert row_matches_truth(summary["confidence_rows"][0], summary)

    wrong = dict(summary["confidence_rows"][0])
    wrong["best_x_mm"] = 301.0
    assert not row_matches_truth(wrong, summary)


def test_confidence_detail_rows_marks_x_ambiguity_as_not_strict_clean():
    summary = _summary("seed13", [_confidence_row("noise10_seed13", x_width=1.0)])

    rows = confidence_detail_rows(summary, "fake_summary.json")

    assert rows[0]["truth_geometry_match"]
    assert rows[0]["strong_confidence"]
    assert rows[0]["x_ambiguity_width_mm"] == pytest.approx(1.0)
    assert not rows[0]["strict_clean_row"]


def test_policy_exact_strong_with_one_x_ambiguity_is_not_clean():
    seed21_summary = _summary(
        "seed21",
        [
            _confidence_row("noise10_seed21"),
            _confidence_row("source_mismatch_noise10_seed21"),
        ],
    )
    seed13_summary = _summary(
        "seed13",
        [
            _confidence_row("noise10_seed13", x_width=1.0),
            _confidence_row("source_mismatch_noise10_seed13"),
        ],
    )
    confidence_rows = (
        confidence_detail_rows(seed21_summary, "seed21_summary.json")
        + confidence_detail_rows(seed13_summary, "seed13_summary.json")
    )
    diagnostic_rows = _diagnostic_rows("seed21") + _diagnostic_rows("seed13")
    run_rows = [
        {"seed_label": "seed21", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
        {"seed_label": "seed13", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
    ]

    summary = summarize_policy(run_rows, confidence_rows, diagnostic_rows)

    assert summary["policy_label"] == "close50_linear29p5_two_seed_exact_strong_not_clean_replicated"
    assert summary["seed_count"] == 2
    assert summary["ambiguous_seed_values"] == "seed13"
    assert summary["strict_clean_seed_values"] == "seed21"
    assert summary["confidence_row_count"] == 4
    assert summary["truth_geometry_row_count"] == 4
    assert summary["strong_confidence_row_count"] == 4
    assert summary["x_ambiguity_row_count"] == 1
    assert summary["strict_clean_row_count"] == 3


def test_policy_all_exact_strong_no_ambiguity_is_clean_candidate():
    seed21_summary = _summary(
        "seed21",
        [
            _confidence_row("noise10_seed21"),
            _confidence_row("source_mismatch_noise10_seed21"),
        ],
    )
    seed13_summary = _summary(
        "seed13",
        [
            _confidence_row("noise10_seed13"),
            _confidence_row("source_mismatch_noise10_seed13"),
        ],
    )
    confidence_rows = (
        confidence_detail_rows(seed21_summary, "seed21_summary.json")
        + confidence_detail_rows(seed13_summary, "seed13_summary.json")
    )
    diagnostic_rows = _diagnostic_rows("seed21") + _diagnostic_rows("seed13")
    run_rows = [
        {"seed_label": "seed21", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
        {"seed_label": "seed13", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
    ]

    summary = summarize_policy(run_rows, confidence_rows, diagnostic_rows)

    assert summary["policy_label"] == "close50_linear29p5_two_seed_clean_candidate"
    assert summary["x_ambiguity_row_count"] == 0


def test_policy_three_seed_frequency_counts_ambiguous_seed():
    seed21_summary = _summary(
        "seed21",
        [
            _confidence_row("noise10_seed21"),
            _confidence_row("source_mismatch_noise10_seed21"),
        ],
    )
    seed13_summary = _summary(
        "seed13",
        [
            _confidence_row("noise10_seed13", x_width=1.0),
            _confidence_row("source_mismatch_noise10_seed13"),
        ],
    )
    seed34_summary = _summary(
        "seed34",
        [
            _confidence_row("noise10_seed34"),
            _confidence_row("source_mismatch_noise10_seed34"),
        ],
    )
    confidence_rows = (
        confidence_detail_rows(seed21_summary, "seed21_summary.json")
        + confidence_detail_rows(seed13_summary, "seed13_summary.json")
        + confidence_detail_rows(seed34_summary, "seed34_summary.json")
    )
    diagnostic_rows = _diagnostic_rows("seed21") + _diagnostic_rows("seed13") + _diagnostic_rows("seed34")
    run_rows = [
        {"seed_label": "seed21", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
        {"seed_label": "seed13", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
        {"seed_label": "seed34", "receiver_sampling": "linear", "tx_rx_offset_mm": 29.5},
    ]

    summary = summarize_policy(run_rows, confidence_rows, diagnostic_rows)

    assert summary["policy_label"] == "close50_linear29p5_three_seed_exact_strong_not_clean_replicated"
    assert summary["seed_count"] == 3
    assert summary["strict_clean_seed_count"] == 2
    assert summary["strict_clean_seed_values"] == "seed21,seed34"
    assert summary["ambiguous_seed_count"] == 1
    assert summary["ambiguous_seed_values"] == "seed13"
    assert summary["x_ambiguity_row_count"] == 1
