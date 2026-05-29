"""Helpers for comparing cumulative/weighted frequency objectives."""

from __future__ import annotations

from collections import OrderedDict

import numpy as np


def frequency_key(freq_hz):
    """Return the stable JSON key used for frequency-indexed metrics."""
    return f"{float(freq_hz) / 1e9:.6g}GHz"


def parse_frequency_list_ghz(text):
    """Parse comma-separated GHz values into Hz floats."""
    values = [float(part.strip()) for part in str(text).split(",") if part.strip()]
    if not values:
        raise ValueError("at least one frequency is required")
    if any(value <= 0.0 for value in values):
        raise ValueError("frequencies must be positive")
    return [value * 1e9 for value in values]


def parse_weight_sets(text, frequency_keys):
    """
    Parse labelled objective weights.

    Format:

    ```text
    label:w1,w2|other_label:w1,w2
    ```
    """
    keys = list(frequency_keys)
    if not keys:
        raise ValueError("frequency_keys must be non-empty")

    weight_sets = OrderedDict()
    for item in str(text).split("|"):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError("each weight set must be labelled as label:w1,w2")
        label, weights_text = item.split(":", 1)
        label = label.strip()
        if not label:
            raise ValueError("weight-set label must be non-empty")
        if label in weight_sets:
            raise ValueError(f"duplicate weight-set label: {label}")
        weights = [float(part.strip()) for part in weights_text.split(",") if part.strip()]
        if len(weights) != len(keys):
            raise ValueError(
                f"weight set {label!r} has {len(weights)} weights for {len(keys)} frequencies"
            )
        if any(weight < 0.0 for weight in weights) or not any(weight > 0.0 for weight in weights):
            raise ValueError("weights must be non-negative with at least one positive value")
        weight_sets[label] = {
            key: float(weight)
            for key, weight in zip(keys, weights)
        }

    if not weight_sets:
        raise ValueError("at least one weight set is required")
    return weight_sets


def weighted_misfit(misfit_by_frequency, weights_by_frequency):
    """Compute a normalized weighted average from per-frequency misfits."""
    numerator = 0.0
    denominator = 0.0
    for key, weight in weights_by_frequency.items():
        if key not in misfit_by_frequency:
            raise KeyError(f"missing misfit for frequency {key}")
        numerator += float(weight) * float(misfit_by_frequency[key])
        denominator += float(weight)
    if denominator <= 0.0:
        raise ValueError("weight sum must be positive")
    return numerator / denominator


def rank_weighted_candidates(candidates, weights_by_frequency, top_k=10):
    """Rank candidate records by one weighted objective."""
    ranked = []
    for candidate in candidates:
        value = weighted_misfit(candidate["misfit_by_frequency"], weights_by_frequency)
        ranked.append({
            "misfit": float(value),
            "params": dict(candidate["params"]),
            "misfit_by_frequency": dict(candidate["misfit_by_frequency"]),
        })
    ranked.sort(key=lambda item: item["misfit"])
    return ranked[:max(0, int(top_k))]


def best_curve_by_radius(candidates, weights_by_frequency):
    """Return the best objective at each radius, minimizing over x/z."""
    best_by_radius = {}
    for candidate in candidates:
        radius = float(candidate["params"]["radius_mm"])
        value = weighted_misfit(candidate["misfit_by_frequency"], weights_by_frequency)
        current = best_by_radius.get(radius)
        if current is None or value < current["misfit"]:
            best_by_radius[radius] = {
                "radius_mm": radius,
                "misfit": float(value),
                "params": dict(candidate["params"]),
            }
    return [
        best_by_radius[radius]
        for radius in sorted(best_by_radius)
    ]


def radius_margin_from_ranked(ranked):
    """Compute best-vs-next-distinct-radius margin for pre-ranked candidates."""
    if not ranked:
        return {
            "best_radius_mm": None,
            "best_radius_misfit": None,
            "next_radius_mm": None,
            "next_radius_misfit": None,
            "radius_margin_abs": None,
            "radius_margin_rel": None,
        }

    ordered = sorted(ranked, key=lambda item: item["misfit"])
    best = ordered[0]
    best_radius = float(best["params"]["radius_mm"])
    best_misfit = float(best["misfit"])
    for item in ordered[1:]:
        radius = float(item["params"]["radius_mm"])
        if not np.isclose(radius, best_radius, rtol=0.0, atol=1e-9):
            next_misfit = float(item["misfit"])
            margin = next_misfit - best_misfit
            return {
                "best_radius_mm": best_radius,
                "best_radius_misfit": best_misfit,
                "next_radius_mm": radius,
                "next_radius_misfit": next_misfit,
                "radius_margin_abs": float(margin),
                "radius_margin_rel": float(margin / max(abs(best_misfit), 1e-12)),
            }

    return {
        "best_radius_mm": best_radius,
        "best_radius_misfit": best_misfit,
        "next_radius_mm": None,
        "next_radius_misfit": None,
        "radius_margin_abs": None,
        "radius_margin_rel": None,
    }
