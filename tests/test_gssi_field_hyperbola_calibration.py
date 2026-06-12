import numpy as np

from run_gssi_field_hyperbola_calibration import (
    cluster_apex_cues,
    depth_from_apex_m,
    epsr_from_velocity,
    fit_profile_grid,
    hyperbola_time_ns,
)
from run_gssi_field_common_offset_sweep import common_offset_hyperbola_time_ns


def _paint_curve(image, x_m, time_ns, curve_ns, amplitude=10.0):
    for col, t_val in enumerate(curve_ns):
        row = int(np.argmin(np.abs(time_ns - t_val)))
        image[max(0, row - 1): row + 2, col] += amplitude


def test_hyperbola_time_returns_apex_at_center():
    x_m = np.array([0.1, 0.2, 0.3])
    curve = hyperbola_time_ns(
        x_m,
        x0_m=0.2,
        apex_time_ns=0.7,
        velocity_m_per_ns=0.15,
        time_zero_ns=0.05,
    )

    assert curve[1] == 0.7
    assert curve[0] > curve[1]
    assert curve[2] > curve[1]


def test_depth_and_epsr_from_velocity_are_two_way_quantities():
    assert depth_from_apex_m(1.0, 0.12, 0.0) == 0.06
    assert round(epsr_from_velocity(0.149896229), 2) == 4.00


def test_cluster_apex_cues_keeps_earliest_pick_per_x_cluster():
    candidates = [
        {"x_m": 0.10, "time_ns": 0.95, "relative_strength": 9.0},
        {"x_m": 0.11, "time_ns": 0.72, "relative_strength": 8.0},
        {"x_m": 0.40, "time_ns": 0.80, "relative_strength": 7.0},
    ]

    apexes = cluster_apex_cues(candidates, x_cluster_m=0.04)

    assert len(apexes) == 2
    assert apexes[0]["time_ns"] == 0.72
    assert apexes[0]["group_size"] == 2
    assert apexes[1]["x_m"] == 0.40


def test_fit_profile_grid_recovers_synthetic_velocity_and_time_zero():
    x_m = np.linspace(0.0, 0.9, 181)
    time_ns = np.linspace(0.0, 3.0, 301)
    true_velocity = 0.14
    true_time_zero = 0.04
    apexes = []
    image = np.zeros((time_ns.size, x_m.size), dtype=np.float64)
    for idx, x0 in enumerate([0.15, 0.45, 0.72], start=1):
        apex_time = 0.75 + 0.03 * idx
        curve = hyperbola_time_ns(x_m, x0, apex_time, true_velocity, true_time_zero)
        _paint_curve(image, x_m, time_ns, curve)
        apexes.append(
            {
                "file": "synthetic.DZT",
                "channel": 0,
                "apex_group": idx,
                "group_size": 1,
                "x_m": x0,
                "trace_index": int(np.argmin(np.abs(x_m - x0))),
                "time_ns": apex_time,
                "sample_index": int(np.argmin(np.abs(time_ns - apex_time))),
                "relative_strength": 10.0,
            }
        )

    best, per_cue_rows, _surface_rows = fit_profile_grid(
        image,
        x_m,
        time_ns,
        apexes,
        velocity_values=np.array([0.10, 0.12, 0.14, 0.16]),
        time_zero_values=np.array([-0.02, 0.04, 0.10]),
        half_width_m=0.18,
    )

    assert best["velocity_m_per_ns"] == true_velocity
    assert best["time_zero_ns"] == true_time_zero
    assert len(per_cue_rows) == 3
    assert all(row["fitted_depth_m"] > 0.0 for row in per_cue_rows)


def test_common_offset_hyperbola_reduces_to_apex_time_at_center():
    x_m = np.array([0.1, 0.2, 0.3])
    curve, depth = common_offset_hyperbola_time_ns(
        x_m,
        x0_m=0.2,
        apex_time_ns=1.0,
        velocity_m_per_ns=0.12,
        time_zero_ns=0.0,
        tx_rx_offset_m=0.04,
    )

    assert np.isfinite(depth)
    assert np.isclose(curve[1], 1.0)
    assert curve[0] > curve[1]
    assert curve[2] > curve[1]
