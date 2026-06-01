"""Radius confidence helpers for source-profiled candidate curves."""

from __future__ import annotations


def radius_interval_from_curve(curve, abs_tolerance=0.0, rel_tolerance=0.0):
    """Return the radius interval whose objective is close to the best value.

    ``curve`` is expected to contain dictionaries with ``misfit`` and
    ``params.radius_mm`` fields, matching source-profiled polish summaries.
    The accepted objective threshold is:

    ``best_misfit + max(abs_tolerance, abs(best_misfit) * rel_tolerance)``.
    """
    if not curve:
        raise ValueError("radius curve must contain at least one candidate")
    if abs_tolerance < 0.0:
        raise ValueError("abs_tolerance must be non-negative")
    if rel_tolerance < 0.0:
        raise ValueError("rel_tolerance must be non-negative")

    best = min(curve, key=lambda item: float(item["misfit"]))
    best_misfit = float(best["misfit"])
    objective_tolerance = max(float(abs_tolerance), abs(best_misfit) * float(rel_tolerance))
    threshold = best_misfit + objective_tolerance
    selected = [
        item for item in curve
        if float(item["misfit"]) <= threshold + 1e-15
    ]
    radii = sorted({
        round(float(item["params"]["radius_mm"]), 10)
        for item in selected
    })
    return {
        "best_radius_mm": float(best["params"]["radius_mm"]),
        "best_misfit": best_misfit,
        "abs_tolerance": float(abs_tolerance),
        "rel_tolerance": float(rel_tolerance),
        "objective_tolerance": float(objective_tolerance),
        "objective_threshold": float(threshold),
        "radius_min_mm": float(radii[0]),
        "radius_max_mm": float(radii[-1]),
        "radius_count": int(len(radii)),
        "radii_mm": radii,
    }
