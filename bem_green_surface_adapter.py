"""Reusable helpers for BEM/project-domain Green-surface adapter probes."""

from __future__ import annotations

import numpy as np

from run_project_core_fdtd_source_normalization_adapter import best_complex_scale, symmetric_relative_l2


def validate_surface_pair(candidate: np.ndarray, reference: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return complex surface arrays after checking shape and rank."""
    candidate_array = np.asarray(candidate, dtype=np.complex128)
    reference_array = np.asarray(reference, dtype=np.complex128)
    if candidate_array.shape != reference_array.shape:
        raise ValueError(f"candidate/reference shape mismatch: {candidate_array.shape} != {reference_array.shape}")
    if candidate_array.ndim != 3:
        raise ValueError("surface arrays must have shape samples x cells x frequencies")
    if 0 in candidate_array.shape:
        raise ValueError("surface arrays must be non-empty")
    return candidate_array, reference_array


def dense_x_grid(
    *,
    start_m: float,
    stop_m: float,
    step_m: float,
    required_x_m: list[float] | tuple[float, ...] = (),
) -> list[float]:
    """Build a sorted dense x grid that includes exact required positions."""
    if step_m <= 0.0:
        raise ValueError("step_m must be positive")
    if stop_m < start_m:
        raise ValueError("stop_m must be >= start_m")
    base = np.arange(float(start_m), float(stop_m) + 0.5 * float(step_m), float(step_m))
    values = {round(float(value), 12) for value in base}
    values.update(round(float(value), 12) for value in required_x_m)
    return sorted(values)


def per_cell_all_source_prediction(candidate: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """Fit one complex scale per cell/frequency using all source positions."""
    candidate_array, reference_array = validate_surface_pair(candidate, reference)
    mapped = np.zeros_like(candidate_array)
    for cell_index in range(candidate_array.shape[1]):
        for freq_index in range(candidate_array.shape[2]):
            scale = best_complex_scale(
                candidate_array[:, cell_index, freq_index],
                reference_array[:, cell_index, freq_index],
            )
            mapped[:, cell_index, freq_index] = scale * candidate_array[:, cell_index, freq_index]
    return mapped


def per_cell_leave_one_source_prediction(candidate: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """Predict each held-out source with per-cell/frequency scales fit on other sources."""
    candidate_array, reference_array = validate_surface_pair(candidate, reference)
    predicted = np.zeros_like(candidate_array)
    all_indices = np.arange(candidate_array.shape[0])
    if all_indices.size < 2:
        raise ValueError("leave-one-source prediction requires at least two source samples")
    for heldout in all_indices:
        train = all_indices[all_indices != heldout]
        for cell_index in range(candidate_array.shape[1]):
            for freq_index in range(candidate_array.shape[2]):
                scale = best_complex_scale(
                    candidate_array[train, cell_index, freq_index],
                    reference_array[train, cell_index, freq_index],
                )
                predicted[heldout, cell_index, freq_index] = scale * candidate_array[heldout, cell_index, freq_index]
    return predicted


def per_cell_all_source_l2(candidate: np.ndarray, reference: np.ndarray) -> float:
    """Symmetric L2 after all-source per-cell/frequency scaling."""
    _, reference_array = validate_surface_pair(candidate, reference)
    return float(symmetric_relative_l2(per_cell_all_source_prediction(candidate, reference), reference_array))


def per_cell_leave_one_source_l2(candidate: np.ndarray, reference: np.ndarray) -> float:
    """Symmetric L2 after leave-one-source per-cell/frequency scaling."""
    _, reference_array = validate_surface_pair(candidate, reference)
    return float(symmetric_relative_l2(per_cell_leave_one_source_prediction(candidate, reference), reference_array))
