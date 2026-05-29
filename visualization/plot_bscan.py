"""
B-scan (radargram) visualization.

Displays the recorded GPR data as a 2D image with scan position
on the x-axis and two-way travel time on the y-axis.
"""
import numpy as np
import matplotlib.pyplot as plt
import config as cfg
from visualization.plot_style import safe_symmetric_limits, save_validated_figure, scan_extent_mm_ns


def plot_bscan(bscan, scan_x, time, save_path=None, show=True,
               clip_pct=0.1, title='B-scan Radargram'):
    """
    Plot B-scan radargram.

    Parameters
    ----------
    bscan : ndarray, shape (nt, n_scans)
        B-scan data.
    scan_x : ndarray
        Scan positions [m].
    time : ndarray
        Time array [s].
    save_path : str, optional
        Path to save figure.
    show : bool
        Whether to display.
    clip_pct : float
        Clip amplitude to +/- clip_pct * max for contrast.
    title : str
        Plot title.
    """
    bscan = np.asarray(bscan, dtype=np.float64)
    if bscan.ndim != 2:
        raise ValueError("bscan must have shape (nt, n_scans)")

    fig, ax = plt.subplots(1, 1, figsize=(10, 7), constrained_layout=True)

    extent = scan_extent_mm_ns(scan_x, time)
    if clip_pct is None:
        vmin, vmax = safe_symmetric_limits(bscan, percentile=99.0)
    else:
        max_abs = float(np.max(np.abs(bscan))) if bscan.size else 0.0
        if max_abs == 0.0:
            vmin, vmax = safe_symmetric_limits(bscan)
        else:
            vmax = max(float(clip_pct) * max_abs, 1e-12)
            vmin = -vmax

    im = ax.imshow(
        bscan,
        cmap='RdBu_r',
        aspect='auto',
        interpolation='nearest',
        extent=extent,
        vmin=vmin,
        vmax=vmax,
    )

    ax.set_xlabel('Scan position x [mm]', fontsize=12)
    ax.set_ylabel('Two-way travel time [ns]', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_ylim(float(np.asarray(time)[-1] * 1e9), float(np.asarray(time)[0] * 1e9))

    cbar = fig.colorbar(im, ax=ax, label='Amplitude', shrink=0.9)
    cbar.ax.tick_params(labelsize=10)

    if save_path:
        save_validated_figure(fig, save_path)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
