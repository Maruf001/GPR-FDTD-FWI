import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from inversion.objective_variants import (  # noqa: E402
    apply_objective_variant,
    objective_variant_window,
    parse_objective_variants,
)


def test_parse_objective_variants_accepts_time_and_bandpass():
    variants = parse_objective_variants(
        "base:1.0,7.0,0.3,none,none,0.0|"
        "late_high:1.5,5.5,0.2,1.1,3.4,0.15"
    )

    assert [variant.label for variant in variants] == ["base", "late_high"]
    assert variants[0].low_hz is None
    assert variants[1].low_hz == pytest.approx(1.1e9)
    assert variants[1].high_hz == pytest.approx(3.4e9)
    assert variants[1].band_taper_hz == pytest.approx(0.15e9)


def test_parse_objective_variants_rejects_duplicate_labels():
    with pytest.raises(ValueError, match="duplicate"):
        parse_objective_variants(
            "base:1.0,7.0,0.3,none,none,0.0|"
            "base:1.5,5.5,0.2,none,none,0.0"
        )


def test_objective_variant_window_zeros_outside_window():
    variant = parse_objective_variants("late:1.5,3.0,0.2,none,none,0.0")[0]
    window = objective_variant_window(variant, nt=80, dt=0.05e-9)

    assert window.shape == (80,)
    assert np.all(window[:30] == 0.0)
    assert np.any(window[34:56] > 0.0)
    assert np.all(window[60:] == 0.0)


def test_apply_objective_variant_preserves_shape_and_changes_bandpassed_data():
    dt = 0.01
    t = np.arange(256) * dt
    low = np.sin(2.0 * np.pi * 2.0 * t)
    high = 0.5 * np.sin(2.0 * np.pi * 30.0 * t)
    traces = np.column_stack([low + high, low - high])
    variant = parse_objective_variants("low:0.0,2.5,0.0,none,1e-8,0.0")[0]

    filtered = apply_objective_variant(traces, variant, dt)

    assert filtered.shape == traces.shape
    assert np.linalg.norm(filtered - traces) > 0.1
