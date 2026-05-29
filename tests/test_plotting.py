"""Tests for robust plotting helpers and figure generation."""
import os
import sys

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg  # noqa: E402
from visualization.plot_bscan import plot_bscan  # noqa: E402
from visualization.plot_inversion import plot_convergence, plot_inversion_comparison  # noqa: E402
from visualization.plot_style import safe_symmetric_limits, scan_extent_mm_ns  # noqa: E402


def _dynamic_range(path):
    with Image.open(path) as image:
        gray = np.asarray(image.convert("L"))
    return int(gray.max()) - int(gray.min())


def test_scan_extent_pads_single_scan_position():
    extent = scan_extent_mm_ns(np.array([0.05]), np.array([0.0, 1e-9]))

    assert extent == [47.5, 52.5, 1.0, 0.0]


def test_safe_symmetric_limits_handles_zero_data():
    vmin, vmax = safe_symmetric_limits(np.zeros((4, 3)))

    assert vmin < 0.0
    assert vmax > 0.0
    assert abs(vmin) == vmax


def test_plot_bscan_single_column_is_not_blank(tmp_path):
    bscan = np.zeros((80, 1), dtype=np.float64)
    bscan[30:35, 0] = np.array([0.0, 0.4, -1.0, 0.6, 0.0])
    path = tmp_path / "single_column_bscan.png"

    plot_bscan(
        bscan,
        scan_x=np.array([0.05]),
        time=np.linspace(0.0, 8e-9, bscan.shape[0]),
        save_path=str(path),
        show=False,
        title="single column",
    )

    assert path.exists()
    assert _dynamic_range(path) > 10


def test_plot_convergence_handles_single_zero_value(tmp_path):
    path = tmp_path / "convergence.png"

    plot_convergence(np.array([0.0]), save_path=str(path), show=False)

    assert path.exists()
    assert _dynamic_range(path) > 10


def test_plot_inversion_comparison_uses_valid_colorbar_layout(tmp_path):
    n = cfg.NPML
    shape = (2 * n + 30, 2 * n + 40)
    initial = np.ones(shape, dtype=np.float64)
    inverted = initial.copy()
    truth = initial.copy()
    initial[n + 5:, n:-n] = 6.0
    inverted[n + 5:, n:-n] = 6.0
    truth[n + 5:, n:-n] = 6.0
    truth[n + 12:n + 15, n + 18:n + 21] = 1.0
    path = tmp_path / "model_comparison.png"

    plot_inversion_comparison(
        initial,
        inverted,
        truth,
        save_path=str(path),
        show=False,
        rebar_params=[(0.09, 0.25, 0.006)],
    )

    assert path.exists()
    assert _dynamic_range(path) > 10
