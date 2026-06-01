"""B-scan based rebar seed detection utilities.

The detector is intentionally a seed generator, not a final estimator. It
scores physically plausible TX/RX hyperbolas and returns x/z candidate windows
for the existing FWI refinement machinery.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np

import config as cfg


@dataclass(frozen=True)
class RebarDetectionCandidate:
    """One x/z seed candidate from hyperbola-energy detection."""

    x_m: float
    z_m: float
    score: float
    normalized_score: float
    support_fraction: float
    time_offset_s: float = 0.0

    def as_mm(self):
        return {
            "x_mm": self.x_m * 1000.0,
            "z_mm": self.z_m * 1000.0,
            "score": float(self.score),
            "normalized_score": float(self.normalized_score),
            "support_fraction": float(self.support_fraction),
            "time_offset_ps": float(self.time_offset_s * 1e12),
        }


def background_removed_bscan(bscan, mode="median"):
    """Remove horizontally coherent energy from a B-scan."""
    data = np.asarray(bscan, dtype=np.float64)
    if data.ndim != 2:
        raise ValueError("bscan must have shape (nt, n_scans)")
    if mode == "none":
        return data.copy()
    if mode == "mean":
        background = np.mean(data, axis=1, keepdims=True)
    elif mode == "median":
        background = np.median(data, axis=1, keepdims=True)
    else:
        raise ValueError(f"unsupported background removal mode: {mode}")
    return data - background


def envelope_bscan(bscan):
    """Return a positive B-scan envelope, using Hilbert if available."""
    data = np.asarray(bscan, dtype=np.float64)
    try:
        from scipy.signal import hilbert

        return np.abs(hilbert(data, axis=0))
    except Exception:
        return np.abs(data)


def hyperbola_times(
        scan_x,
        x_m,
        z_m,
        tx_rx_offset=cfg.TX_RX_OFFSET,
        antenna_z=cfg.TX_Z,
        epsr=cfg.CONCRETE_EPSR,
        time_offset_s=0.0):
    """Return TX-to-target-to-RX travel times for one candidate."""
    scan_x = np.asarray(scan_x, dtype=np.float64)
    src_x = scan_x
    rec_x = scan_x + float(tx_rx_offset)
    dz = float(z_m) - float(antenna_z)
    if dz <= 0.0:
        raise ValueError("candidate z must be deeper than antenna_z")
    velocity = cfg.C0 / np.sqrt(float(epsr))
    src_dist = np.sqrt((src_x - float(x_m)) ** 2 + dz ** 2)
    rec_dist = np.sqrt((rec_x - float(x_m)) ** 2 + dz ** 2)
    return (src_dist + rec_dist) / velocity + float(time_offset_s)


def _interpolate_curve_values(image, time, curve_time):
    """Sample an image along a time-varying scan curve."""
    image = np.asarray(image, dtype=np.float64)
    time = np.asarray(time, dtype=np.float64)
    curve_time = np.asarray(curve_time, dtype=np.float64)
    if image.ndim != 2:
        raise ValueError("image must have shape (nt, n_scans)")
    if time.ndim != 1 or time.size != image.shape[0]:
        raise ValueError("time must match image time dimension")
    if curve_time.ndim != 1 or curve_time.size != image.shape[1]:
        raise ValueError("curve_time must match image scan dimension")

    valid = (curve_time >= time[0]) & (curve_time <= time[-1])
    values = np.zeros(image.shape[1], dtype=np.float64)
    if not np.any(valid):
        return values, valid

    dt = float(time[1] - time[0])
    fractional = (curve_time[valid] - time[0]) / dt
    lower = np.floor(fractional).astype(int)
    upper = np.clip(lower + 1, 0, time.size - 1)
    lower = np.clip(lower, 0, time.size - 1)
    weight = fractional - lower
    columns = np.flatnonzero(valid)
    values[valid] = (
        (1.0 - weight) * image[lower, columns]
        + weight * image[upper, columns]
    )
    return values, valid


def score_hyperbola_candidate(
        image,
        scan_x,
        time,
        x_m,
        z_m,
        tx_rx_offset=cfg.TX_RX_OFFSET,
        antenna_z=cfg.TX_Z,
        epsr=cfg.CONCRETE_EPSR,
        time_offset_s=0.0):
    """Score one x/z candidate by envelope energy along its hyperbola."""
    curve_time = hyperbola_times(
        scan_x,
        x_m,
        z_m,
        tx_rx_offset=tx_rx_offset,
        antenna_z=antenna_z,
        epsr=epsr,
        time_offset_s=time_offset_s,
    )
    values, valid = _interpolate_curve_values(image, time, curve_time)
    if not np.any(valid):
        return 0.0, 0.0
    support_fraction = float(np.mean(valid))
    return float(np.mean(values[valid])), support_fraction


def _candidate_grid(values_mm):
    values = np.asarray(values_mm, dtype=np.float64)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("candidate grid must be a non-empty 1D array")
    return values / 1000.0


def _suppress_nearby(candidates, x_min_separation_m, z_min_separation_m):
    kept = []
    for candidate in candidates:
        too_close = False
        for existing in kept:
            if (
                abs(candidate.x_m - existing.x_m) < x_min_separation_m
                and abs(candidate.z_m - existing.z_m) < z_min_separation_m
            ):
                too_close = True
                break
        if not too_close:
            kept.append(candidate)
    return kept


def assign_rebar_candidates(candidates, count, min_x_separation_mm=45.0):
    """
    Choose a physically distinct detector seed set for coordinate FWI.

    The detector can return multiple plausible hyperbola picks at the same x
    but different z. Coordinate FWI should start from one physical seed per
    rebar, so this assignment keeps the highest-scoring combination whose
    x-locations are sufficiently separated.
    """
    candidates = list(candidates)
    count = int(count)
    if count <= 0:
        raise ValueError("count must be positive")
    if len(candidates) < count:
        raise ValueError("not enough candidates for requested assignment")

    min_x_m = float(min_x_separation_mm) / 1000.0
    best_combo = None
    best_score = None
    for combo in itertools.combinations(candidates, count):
        xs = sorted(candidate.x_m for candidate in combo)
        if any((right - left) < min_x_m for left, right in zip(xs[:-1], xs[1:])):
            continue
        score = sum(float(candidate.score) for candidate in combo)
        if best_score is None or score > best_score:
            best_combo = combo
            best_score = score

    if best_combo is None:
        raise ValueError("no candidate assignment satisfies min_x_separation_mm")
    return sorted(best_combo, key=lambda candidate: candidate.x_m)


def detect_rebar_candidates(
        bscan,
        scan_x,
        time,
        x_values_mm=None,
        z_values_mm=None,
        top_k=5,
        background_mode="median",
        min_support_fraction=0.75,
        x_min_separation_mm=20.0,
        z_min_separation_mm=10.0,
        tx_rx_offset=cfg.TX_RX_OFFSET,
        antenna_z=cfg.TX_Z,
        epsr=cfg.CONCRETE_EPSR,
        time_offset_s=0.0,
        time_offsets_s=None):
    """Detect likely rebar x/z seeds from a B-scan."""
    if top_k <= 0:
        raise ValueError("top_k must be positive")
    scan_x = np.asarray(scan_x, dtype=np.float64)
    time = np.asarray(time, dtype=np.float64)
    if scan_x.ndim != 1 or scan_x.size == 0:
        raise ValueError("scan_x must be a non-empty 1D array")
    if time.ndim != 1 or time.size < 2:
        raise ValueError("time must contain at least two samples")
    if time_offsets_s is None:
        offset_values_s = [float(time_offset_s)]
    else:
        offset_values_s = [float(value) for value in time_offsets_s]
        if not offset_values_s:
            raise ValueError("time_offsets_s must not be empty")

    x_grid_m = _candidate_grid(
        x_values_mm
        if x_values_mm is not None
        else np.arange(
            cfg.SCAN_START_X * 1000.0,
            cfg.SCAN_END_X * 1000.0 + 1e-9,
            4.0,
        )
    )
    z_grid_m = _candidate_grid(
        z_values_mm
        if z_values_mm is not None
        else np.arange(
            (cfg.CONCRETE_TOP + 0.020) * 1000.0,
            (cfg.CONCRETE_TOP + 0.160) * 1000.0 + 1e-9,
            4.0,
        )
    )

    processed = background_removed_bscan(bscan, mode=background_mode)
    image = envelope_bscan(processed)
    scale = float(np.percentile(image[np.isfinite(image)], 95.0)) if image.size else 1.0
    scale = max(scale, 1e-30)

    candidates = []
    for offset_s in offset_values_s:
        for x_m in x_grid_m:
            for z_m in z_grid_m:
                score, support_fraction = score_hyperbola_candidate(
                    image,
                    scan_x,
                    time,
                    x_m,
                    z_m,
                    tx_rx_offset=tx_rx_offset,
                    antenna_z=antenna_z,
                    epsr=epsr,
                    time_offset_s=offset_s,
                )
                if support_fraction < min_support_fraction:
                    continue
                candidates.append(
                    RebarDetectionCandidate(
                        x_m=float(x_m),
                        z_m=float(z_m),
                        score=score,
                        normalized_score=score / scale,
                        support_fraction=support_fraction,
                        time_offset_s=float(offset_s),
                    )
                )

    candidates.sort(key=lambda item: item.score, reverse=True)
    candidates = _suppress_nearby(
        candidates,
        x_min_separation_m=float(x_min_separation_mm) / 1000.0,
        z_min_separation_m=float(z_min_separation_mm) / 1000.0,
    )
    return candidates[:int(top_k)]


def candidate_window(candidate, x_half_window_mm=20.0, z_half_window_mm=20.0):
    """Return a local FWI search window around a detection candidate."""
    return {
        "x_min_mm": candidate.x_m * 1000.0 - float(x_half_window_mm),
        "x_max_mm": candidate.x_m * 1000.0 + float(x_half_window_mm),
        "z_min_mm": candidate.z_m * 1000.0 - float(z_half_window_mm),
        "z_max_mm": candidate.z_m * 1000.0 + float(z_half_window_mm),
    }
