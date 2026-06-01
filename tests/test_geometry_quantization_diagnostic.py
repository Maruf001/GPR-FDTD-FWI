"""Tests for one-rebar geometry quantization diagnostics."""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.materials import MaterialModel  # noqa: E402
from run_single_rebar_geometry_quantization_diagnostic import (  # noqa: E402
    geometry_quantization_rows,
    material_contrast_metrics,
    material_distance,
)


def test_material_distance_is_zero_for_identical_models():
    model = MaterialModel(3, 3, eps_r_bg=6.0, sigma_bg=0.01)

    distance = material_distance(model, model.copy())

    assert distance == {"epsilon_l1": 0.0, "log_sigma_l1": 0.0}


def test_material_contrast_counts_changed_cells():
    baseline = MaterialModel(3, 3, eps_r_bg=6.0, sigma_bg=0.01)
    model = baseline.copy()
    model.epsilon_r[1, 1] = 1.0
    model.sigma[1, 1] = 1.0e7

    metrics = material_contrast_metrics(model, baseline)

    assert metrics["active_cell_count"] == 1
    assert metrics["epsilon_l1_contrast"] == 5.0
    assert metrics["log_sigma_l1_contrast"] == 9.0


def test_geometry_quantization_rows_report_adjacent_delta():
    rows = geometry_quantization_rows(
        radii_mm=[4.0, 4.1],
        x_mm=250.0,
        z_mm=70.0,
        geometry_modes=("hard",),
        subcell_samples=5,
    )

    assert len(rows) == 2
    assert np.isnan(rows[0]["adjacent_log_sigma_l1_delta"])
    assert rows[1]["adjacent_log_sigma_l1_delta"] >= 0.0
