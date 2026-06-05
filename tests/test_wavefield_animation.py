import os
import sys
from types import SimpleNamespace

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from run_wavefield_animation import (  # noqa: E402
    build_animation_model,
    source_receiver_indices,
    validate_animation,
)
from run_wavefield_comparison_animation import (  # noqa: E402
    comparison_frame_count,
    material_parameters_from_args,
    source_parameters_from_args,
    validate_same_length,
)
from run_residual_backprop_animation import residual_source  # noqa: E402


def test_source_receiver_indices_orders_surface_pair():
    src_iz, src_ix, rec_iz, rec_ix = source_receiver_indices(150.0)

    assert src_iz == rec_iz
    assert rec_ix > src_ix


def test_validate_animation_reports_nonblank_gif(tmp_path):
    frame1 = Image.fromarray(np.zeros((12, 16), dtype=np.uint8))
    frame2_array = np.zeros((12, 16), dtype=np.uint8)
    frame2_array[3:9, 5:11] = 255
    frame2 = Image.fromarray(frame2_array)
    path = tmp_path / "toy.gif"
    frame1.save(path, save_all=True, append_images=[frame2], duration=80, loop=0)

    metrics = validate_animation(path)

    assert metrics["frame_count"] == 2
    assert metrics["width_px"] == 16
    assert metrics["height_px"] == 12
    assert metrics["max_dynamic_range"] == 255
    assert metrics["mean_frame_std"] > 0.0


def test_build_animation_model_accepts_single_rebar_material_override():
    model = build_animation_model(
        [250.0],
        [90.0],
        [6.0],
        rebar_sigma=12345.0,
    )

    assert np.isclose(model.sigma.max(), 12345.0)


def test_build_animation_model_rejects_material_override_for_multi_rebar():
    with pytest.raises(ValueError, match="exactly one rebar"):
        build_animation_model(
            [150.0, 250.0],
            [90.0, 90.0],
            [6.0, 6.0],
            rebar_sigma=12345.0,
        )


def test_comparison_frame_count_uses_paired_frames():
    assert comparison_frame_count([(0, None), (1, None)], [(0, None)]) == 1


def test_source_parameters_from_args_falls_back_to_common_values():
    args = SimpleNamespace(
        frequency_scale=1.1,
        time_shift_ps=-50.0,
        amplitude_scale=0.9,
        truth_frequency_scale=None,
        truth_time_shift_ps=None,
        truth_amplitude_scale=None,
    )

    params = source_parameters_from_args(args, "truth")

    assert params == {
        "frequency_scale": 1.1,
        "time_shift_ps": -50.0,
        "amplitude_scale": 0.9,
    }


def test_source_parameters_from_args_prefers_prefixed_values():
    args = SimpleNamespace(
        frequency_scale=1.0,
        time_shift_ps=0.0,
        amplitude_scale=1.0,
        candidate_frequency_scale=0.9,
        candidate_time_shift_ps=25.0,
        candidate_amplitude_scale=1.2,
    )

    params = source_parameters_from_args(args, "candidate")

    assert params == {
        "frequency_scale": 0.9,
        "time_shift_ps": 25.0,
        "amplitude_scale": 1.2,
    }


def test_material_parameters_from_args_returns_prefixed_overrides():
    args = SimpleNamespace(
        truth_concrete_epsr=6.1,
        truth_concrete_sigma=0.02,
        truth_rebar_epsr=1.0,
        truth_rebar_sigma=1e7,
    )

    params = material_parameters_from_args(args, "truth")

    assert params == {
        "concrete_epsr": 6.1,
        "concrete_sigma": 0.02,
        "rebar_epsr": 1.0,
        "rebar_sigma": 1e7,
    }


def test_validate_same_length_rejects_mismatched_geometry_lists():
    with pytest.raises(ValueError, match="candidate"):
        validate_same_length("candidate", [250.0], [90.0, 91.0], [6.0])


def test_residual_source_time_reverses_candidate_minus_observed():
    source, residual = residual_source(
        np.array([1.0, 3.0, 2.0]),
        np.array([0.5, 1.0, 2.5]),
    )

    np.testing.assert_allclose(residual, [0.5, 2.0, -0.5])
    np.testing.assert_allclose(source, [-0.5, 2.0, 0.5])
