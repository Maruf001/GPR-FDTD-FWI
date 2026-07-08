"""Helpers for loading and validating layered project-domain surface caches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

REQUIRED_CACHE_KEYS = {
    "surface",
    "surface_x_m",
    "source_points_m",
    "receiver_points_m",
    "target_ix",
    "target_iz",
    "target_weights",
    "selected_indices",
    "selected_frequencies_hz",
    "fdtd_band",
}


def load_layered_surface_cache(path: Path) -> dict[str, np.ndarray]:
    with np.load(path) as arrays:
        return {key: arrays[key] for key in arrays.files}


def validate_layered_surface_cache(arrays: dict[str, np.ndarray]) -> list[str]:
    findings: list[str] = []
    missing = sorted(REQUIRED_CACHE_KEYS - set(arrays))
    for key in missing:
        findings.append(f"missing:{key}")
    if missing:
        return findings

    surface = arrays["surface"]
    if surface.ndim != 3:
        findings.append("surface:not_3d")
        return findings
    surface_x = arrays["surface_x_m"]
    target_ix = arrays["target_ix"]
    selected_indices = arrays["selected_indices"]
    if surface.shape[0] != surface_x.size:
        findings.append("surface_x_m:size_mismatch")
    if surface.shape[1] != target_ix.size:
        findings.append("target_ix:size_mismatch")
    if surface.shape[2] != selected_indices.size:
        findings.append("selected_indices:size_mismatch")
    if arrays["target_iz"].size != target_ix.size:
        findings.append("target_iz:size_mismatch")
    if arrays["target_weights"].size != target_ix.size:
        findings.append("target_weights:size_mismatch")
    if arrays["selected_frequencies_hz"].size != selected_indices.size:
        findings.append("selected_frequencies_hz:size_mismatch")
    if arrays["source_points_m"].shape != arrays["receiver_points_m"].shape:
        findings.append("source_receiver_points:shape_mismatch")
    if not np.iscomplexobj(surface):
        findings.append("surface:not_complex")
    return findings


def layered_surface_cache_summary(arrays: dict[str, np.ndarray]) -> dict[str, Any]:
    surface = arrays["surface"]
    return {
        "surface_shape": "x".join(str(value) for value in surface.shape),
        "surface_sample_count": int(surface.shape[0]),
        "target_cell_count": int(surface.shape[1]),
        "selected_frequency_count": int(surface.shape[2]),
        "scan_count": int(arrays["source_points_m"].shape[0]),
    }


def fields_by_surface_x(arrays: dict[str, np.ndarray]) -> dict[float, np.ndarray]:
    surface_x = arrays["surface_x_m"]
    surface = arrays["surface"]
    return {round(float(x), 12): surface[index] for index, x in enumerate(surface_x)}
