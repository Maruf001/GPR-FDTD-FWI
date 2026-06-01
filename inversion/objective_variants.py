"""Objective-variant helpers for trace-window and bandpass comparisons."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from inversion.adjoint import _build_mute_window
from inversion.trace_filters import apply_bandpass_traces


@dataclass(frozen=True)
class ObjectiveVariant:
    """One trace objective variant applied before source-profiled LS."""

    label: str
    t_start_s: float = 1.0e-9
    t_end_s: float = 7.0e-9
    taper_s: float = 0.3e-9
    low_hz: float | None = None
    high_hz: float | None = None
    band_taper_hz: float = 0.0

    def as_dict(self):
        return {
            "label": self.label,
            "t_start_ns": float(self.t_start_s * 1e9),
            "t_end_ns": float(self.t_end_s * 1e9),
            "taper_ns": float(self.taper_s * 1e9),
            "low_ghz": None if self.low_hz is None else float(self.low_hz / 1e9),
            "high_ghz": None if self.high_hz is None else float(self.high_hz / 1e9),
            "band_taper_ghz": float(self.band_taper_hz / 1e9),
        }


def _optional_ghz(text):
    value = str(text).strip().lower()
    if value in {"", "none", "null", "-"}:
        return None
    parsed = float(value)
    if parsed < 0.0:
        raise ValueError("bandpass frequency bounds must be non-negative")
    return parsed * 1e9


def parse_objective_variants(text):
    """
    Parse labelled time-window/bandpass objective variants.

    Format:

    ```text
    label:t_start_ns,t_end_ns,taper_ns,low_ghz,high_ghz,band_taper_ghz
    ```

    Use `none` for an open bandpass bound.
    """
    variants = []
    seen = set()
    for item in str(text).split("|"):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError("each objective variant must be labelled")
        label, values_text = item.split(":", 1)
        label = label.strip()
        if not label:
            raise ValueError("objective variant label must be non-empty")
        if label in seen:
            raise ValueError(f"duplicate objective variant label: {label}")
        parts = [part.strip() for part in values_text.split(",")]
        if len(parts) != 6:
            raise ValueError(
                "objective variants require 6 values: "
                "t_start_ns,t_end_ns,taper_ns,low_ghz,high_ghz,band_taper_ghz"
            )
        t_start_ns = float(parts[0])
        t_end_ns = float(parts[1])
        taper_ns = float(parts[2])
        low_hz = _optional_ghz(parts[3])
        high_hz = _optional_ghz(parts[4])
        band_taper_ghz = float(parts[5])
        if t_start_ns < 0.0 or t_end_ns <= t_start_ns:
            raise ValueError("objective time window must satisfy 0 <= start < end")
        if taper_ns < 0.0:
            raise ValueError("objective time taper must be non-negative")
        if low_hz is not None and high_hz is not None and low_hz >= high_hz:
            raise ValueError("objective bandpass low bound must be below high bound")
        if band_taper_ghz < 0.0:
            raise ValueError("objective band taper must be non-negative")
        variants.append(ObjectiveVariant(
            label=label,
            t_start_s=t_start_ns * 1e-9,
            t_end_s=t_end_ns * 1e-9,
            taper_s=taper_ns * 1e-9,
            low_hz=low_hz,
            high_hz=high_hz,
            band_taper_hz=band_taper_ghz * 1e9,
        ))
        seen.add(label)

    if not variants:
        raise ValueError("at least one objective variant is required")
    return variants


def objective_variant_window(variant, nt, dt):
    """Build the time-domain weight for an objective variant."""
    return _build_mute_window(
        int(nt),
        float(dt),
        t_start=float(variant.t_start_s),
        t_end=float(variant.t_end_s),
        taper_ns=float(variant.taper_s),
    )


def apply_objective_variant(traces, variant, dt):
    """Apply the variant's bandpass transform, preserving trace shape."""
    data = np.asarray(traces, dtype=np.float64)
    if variant.low_hz is None and variant.high_hz is None:
        return data.copy()
    return apply_bandpass_traces(
        data,
        float(dt),
        low_hz=variant.low_hz,
        high_hz=variant.high_hz,
        taper_hz=variant.band_taper_hz,
    )
