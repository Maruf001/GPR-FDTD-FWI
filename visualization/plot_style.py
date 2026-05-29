"""Shared plotting helpers for experiment-grade figures."""
import os

import numpy as np
from PIL import Image


def safe_symmetric_limits(values, percentile=99.0, floor=1e-12):
    """Return symmetric color limits that remain valid for zero-valued data."""
    data = np.asarray(values, dtype=np.float64)
    finite = np.abs(data[np.isfinite(data)])
    if finite.size == 0:
        return -1.0, 1.0

    finite = finite[finite > 0.0]
    if finite.size == 0:
        vmax = float(floor)
    else:
        vmax = float(np.percentile(finite, percentile))
        vmax = max(vmax, float(floor))
    return -vmax, vmax


def scan_extent_mm_ns(scan_x, time, min_width_mm=5.0):
    """Build an imshow extent for B-scans, including one-column scans."""
    x_mm = np.asarray(scan_x, dtype=np.float64) * 1000.0
    t_ns = np.asarray(time, dtype=np.float64) * 1e9
    if x_mm.ndim != 1 or x_mm.size == 0:
        raise ValueError("scan_x must be a non-empty 1D array")
    if t_ns.ndim != 1 or t_ns.size < 2:
        raise ValueError("time must be a 1D array with at least two samples")

    if x_mm.size == 1:
        half_width = 0.5 * float(min_width_mm)
        x0 = float(x_mm[0] - half_width)
        x1 = float(x_mm[0] + half_width)
    else:
        edges = np.empty(x_mm.size + 1, dtype=np.float64)
        edges[1:-1] = 0.5 * (x_mm[:-1] + x_mm[1:])
        edges[0] = x_mm[0] - 0.5 * (x_mm[1] - x_mm[0])
        edges[-1] = x_mm[-1] + 0.5 * (x_mm[-1] - x_mm[-2])
        x0 = float(edges[0])
        x1 = float(edges[-1])

    return [x0, x1, float(t_ns[-1]), float(t_ns[0])]


def save_validated_figure(fig, save_path, min_dynamic_range=2):
    """Save a figure and check that the resulting image is not degenerate."""
    if save_path is None:
        return None

    directory = os.path.dirname(save_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fig.savefig(save_path, dpi=170, bbox_inches="tight", facecolor="white")

    with Image.open(save_path) as image:
        gray = np.asarray(image.convert("L"))
    if gray.size == 0:
        raise ValueError(f"Saved empty figure: {save_path}")
    if int(gray.max()) - int(gray.min()) < int(min_dynamic_range):
        raise ValueError(f"Saved near-blank figure: {save_path}")
    return save_path
