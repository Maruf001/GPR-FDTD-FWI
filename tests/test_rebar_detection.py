import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.rebar_detection import (  # noqa: E402
    RebarDetectionCandidate,
    assign_rebar_candidates,
    background_removed_bscan,
    candidate_window,
    detect_rebar_candidates,
    hyperbola_times,
)
from run_rebar_detection_pipeline import (  # noqa: E402
    parse_mm_range,
    truth_match_metrics,
    write_detection_figure_notes,
)
from run_rebar_detection_benchmark import summarize_rows  # noqa: E402


def _synthetic_hyperbola_bscan(scan_x, time, x_m, z_m, amplitude=1.0, width_s=45e-12):
    bscan = np.zeros((time.size, scan_x.size), dtype=np.float64)
    curve = hyperbola_times(scan_x, x_m, z_m)
    for col, t0 in enumerate(curve):
        bscan[:, col] += amplitude * np.exp(-0.5 * ((time - t0) / width_s) ** 2)
    return bscan


def test_background_removed_bscan_removes_horizontal_event():
    bscan = np.tile(np.linspace(0.0, 1.0, 12)[:, None], (1, 5))
    bscan[4, 2] += 3.0

    cleaned = background_removed_bscan(bscan)

    assert np.allclose(np.median(cleaned, axis=1), 0.0)
    assert cleaned[4, 2] > 0.0


def test_detect_rebar_candidates_finds_synthetic_hyperbola():
    scan_x = np.linspace(0.05, 0.45, 101)
    time = np.linspace(0.0, 4.0e-9, 900)
    truth_x_m = 0.250
    truth_z_m = 0.090
    bscan = _synthetic_hyperbola_bscan(scan_x, time, truth_x_m, truth_z_m)
    bscan += 0.25 * np.exp(-0.5 * ((time[:, None] - 0.25e-9) / 30e-12) ** 2)

    candidates = detect_rebar_candidates(
        bscan,
        scan_x,
        time,
        x_values_mm=np.arange(220.0, 281.0, 4.0),
        z_values_mm=np.arange(70.0, 111.0, 4.0),
        top_k=3,
        x_min_separation_mm=12.0,
        z_min_separation_mm=8.0,
    )

    assert candidates
    best = candidates[0]
    assert abs(best.x_m - truth_x_m) <= 0.006
    assert abs(best.z_m - truth_z_m) <= 0.006
    assert best.normalized_score > 0.0


def test_candidate_window_reports_mm_bounds():
    scan_x = np.linspace(0.05, 0.45, 11)
    time = np.linspace(0.0, 4.0e-9, 100)
    candidate = detect_rebar_candidates(
        _synthetic_hyperbola_bscan(scan_x, time, 0.250, 0.090),
        scan_x,
        time,
        x_values_mm=[250.0],
        z_values_mm=[90.0],
        top_k=1,
    )[0]

    window = candidate_window(candidate, x_half_window_mm=10.0, z_half_window_mm=5.0)

    assert window == {
        "x_min_mm": 240.0,
        "x_max_mm": 260.0,
        "z_min_mm": 85.0,
        "z_max_mm": 95.0,
    }


def test_parse_mm_range_accepts_inclusive_range_and_lists():
    assert parse_mm_range("10:14:2") == [10.0, 12.0, 14.0]
    assert parse_mm_range("10,12") == [10.0, 12.0]


def test_truth_match_metrics_reports_tolerance():
    candidates = detect_rebar_candidates(
        _synthetic_hyperbola_bscan(
            np.linspace(0.05, 0.45, 21),
            np.linspace(0.0, 4.0e-9, 200),
            0.250,
            0.090,
        ),
        np.linspace(0.05, 0.45, 21),
        np.linspace(0.0, 4.0e-9, 200),
        x_values_mm=[250.0],
        z_values_mm=[90.0],
        top_k=1,
    )

    metrics = truth_match_metrics(candidates, [252.0], [92.0], 5.0, 5.0)

    assert metrics[0]["matched_rank"] == 1
    assert metrics[0]["within_tolerance"]


def test_write_detection_figure_notes_explains_overlay(tmp_path):
    summary = {
        "truth_x_values_mm": [150.0, 250.0],
        "truth_z_values_mm": [90.0, 110.0],
        "truth_radius_values_mm": [5.0, 8.0],
        "candidates": [
            {"rank": 1, "x_mm": 148.0, "z_mm": 90.0},
            {"rank": 2, "x_mm": 252.0, "z_mm": 110.0},
        ],
        "all_truths_within_tolerance": True,
    }
    notes_path = tmp_path / "FIGURE_NOTES.md"

    write_detection_figure_notes(notes_path, summary)

    text = notes_path.read_text(encoding="utf-8")
    assert "detection_overlay.png" in text
    assert "B-scan" in text
    assert "Full-waveform inversion" in text
    assert "truth radii: 5, 8 mm" in text


def test_assign_rebar_candidates_rejects_same_x_duplicate():
    candidates = [
        RebarDetectionCandidate(0.148, 0.085, 10.0, 1.0, 1.0),
        RebarDetectionCandidate(0.252, 0.105, 9.0, 0.9, 1.0),
        RebarDetectionCandidate(0.252, 0.065, 8.5, 0.85, 1.0),
        RebarDetectionCandidate(0.352, 0.120, 7.0, 0.7, 1.0),
    ]

    assigned = assign_rebar_candidates(candidates, 3, min_x_separation_mm=45.0)

    assert [(round(c.x_m * 1000), round(c.z_m * 1000)) for c in assigned] == [
        (148, 85),
        (252, 105),
        (352, 120),
    ]


def test_assign_rebar_candidates_reports_no_feasible_set():
    candidates = [
        RebarDetectionCandidate(0.250, 0.090, 10.0, 1.0, 1.0),
        RebarDetectionCandidate(0.252, 0.120, 9.0, 0.9, 1.0),
    ]

    with np.testing.assert_raises(ValueError):
        assign_rebar_candidates(candidates, 2, min_x_separation_mm=45.0)


def test_summarize_rows_reports_hit_rate_and_error_stats():
    summary = summarize_rows([
        {
            "detected": True,
            "within_tolerance": True,
            "x_error_mm": 2.0,
            "z_error_mm": 5.0,
        },
        {
            "detected": True,
            "within_tolerance": False,
            "x_error_mm": 4.0,
            "z_error_mm": 15.0,
        },
    ])

    assert summary["scenario_count"] == 2
    assert summary["detected_count"] == 2
    assert summary["hit_count"] == 1
    assert summary["hit_rate"] == 0.5
    assert summary["median_x_error_mm"] == 3.0
    assert summary["max_z_error_mm"] == 15.0
