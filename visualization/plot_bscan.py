"""
B-scan (radargram) visualization.

Displays the recorded GPR data as a 2D image with scan position
on the x-axis and two-way travel time on the y-axis.
"""
import numpy as np
import matplotlib.pyplot as plt
import config as cfg


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
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Convert to mm and ns
    x_mm = scan_x * 1000
    t_ns = time * 1e9

    vmax = clip_pct * np.max(np.abs(bscan))

    im = ax.pcolormesh(x_mm, t_ns, bscan, cmap='seismic',
                       shading='auto', vmin=-vmax, vmax=vmax)

    ax.set_xlabel('Scan position x [mm]')
    ax.set_ylabel('Two-way travel time [ns]')
    ax.set_title(title)
    ax.invert_yaxis()

    fig.colorbar(im, ax=ax, label='Normalized amplitude')

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
