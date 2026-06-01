"""Tests for coordinate candidate z/radius landscape reporting."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_coordinate_candidate_landscape_report import (  # noqa: E402
    axis_edges,
    best_candidate,
    build_report,
    filter_case_rows,
    landscape_matrix,
    landscape_rows,
    truth_rank,
)


def _rows():
    return [
        {
            "case_label": "noise",
            "x_mm": "309",
            "z_mm": "90",
            "radius_mm": "8",
            "misfit": "0.2",
        },
        {
            "case_label": "noise",
            "x_mm": "310",
            "z_mm": "90",
            "radius_mm": "8",
            "misfit": "0.1",
        },
        {
            "case_label": "noise",
            "x_mm": "310",
            "z_mm": "85",
            "radius_mm": "6",
            "misfit": "0.3",
        },
        {
            "case_label": "other",
            "x_mm": "310",
            "z_mm": "90",
            "radius_mm": "8",
            "misfit": "0.01",
        },
    ]


def test_filter_case_rows_selects_requested_case():
    rows = filter_case_rows(_rows(), "noise")

    assert len(rows) == 3


def test_landscape_rows_keeps_best_x_for_each_z_radius_pair():
    rows = landscape_rows(filter_case_rows(_rows(), "noise"))

    assert len(rows) == 2
    assert best_candidate(rows)["x_mm"] == "310"
    assert best_candidate(rows)["misfit"] == "0.1"


def test_landscape_matrix_places_misfit_by_z_and_radius():
    rows = landscape_rows(filter_case_rows(_rows(), "noise"))

    z_values, radius_values, matrix = landscape_matrix(rows)

    assert z_values == [85.0, 90.0]
    assert radius_values == [6.0, 8.0]
    assert matrix[0, 0] == 0.3
    assert matrix[1, 1] == 0.1
    assert np.isnan(matrix[0, 1])


def test_axis_edges_handles_single_value():
    edges = axis_edges([90.0], fallback_step=2.0)

    assert edges.tolist() == [89.0, 91.0]


def test_truth_rank_reports_exact_sampled_pair():
    rows = landscape_rows(filter_case_rows(_rows(), "noise"))

    rank = truth_rank(rows, truth_z_mm=90.0, truth_radius_mm=8.0)

    assert rank["rank"] == 1
    assert rank["row"]["misfit"] == "0.1"


def test_build_report_includes_best_and_truth_rank():
    rows = landscape_rows(filter_case_rows(_rows(), "noise"))

    report = build_report(rows, "noise", truth_z_mm=85.0, truth_radius_mm=6.0)

    assert report["best"]["z_mm"] == 90.0
    assert report["best"]["radius_mm"] == 8.0
    assert report["truth_rank"] == 2
