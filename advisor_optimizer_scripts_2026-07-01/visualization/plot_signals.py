"""
Signal comparison plots.

Overlays observed vs synthetic traces at selected scan positions
to show how well the inverted model reproduces the data.
"""
import numpy as np
import matplotlib.pyplot as plt
import config as cfg


def plot_signal_comparison(d_obs, d_syn, scan_x, time,
                           trace_indices=None, save_path=None, show=True):
    """
    Compare observed and synthetic traces.

    Parameters
    ----------
    d_obs, d_syn : ndarray, shape (nt, n_scans)
        Observed and synthetic B-scan data.
    scan_x : ndarray
        Scan positions [m].
    time : ndarray
        Time array [s].
    trace_indices : list of int, optional
        Which scan positions to plot. Defaults to 5 evenly spaced.
    """
    if trace_indices is None:
        n = d_obs.shape[1]
        trace_indices = np.linspace(0, n - 1, 5, dtype=int)

    n_traces = len(trace_indices)
    fig, axes = plt.subplots(1, n_traces, figsize=(3 * n_traces, 6),
                              sharey=True)
    if n_traces == 1:
        axes = [axes]

    t_ns = time * 1e9

    for ax, idx in zip(axes, trace_indices):
        ax.plot(d_obs[:, idx], t_ns, 'b-', linewidth=0.8, label='Observed')
        ax.plot(d_syn[:, idx], t_ns, 'r--', linewidth=0.8, label='Synthetic')
        ax.set_xlabel('Amplitude')
        ax.set_title(f'x={scan_x[idx]*1000:.0f} mm')
        ax.invert_yaxis()
        ax.legend(fontsize=7)

    axes[0].set_ylabel('Time [ns]')
    fig.suptitle('Trace Comparison: Observed vs Synthetic', fontsize=12)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def plot_residual_bscan(d_obs, d_syn, scan_x, time,
                         save_path=None, show=True):
    """Plot the residual (d_syn - d_obs) as a B-scan."""
    from visualization.plot_bscan import plot_bscan
    residual = d_syn - d_obs
    return plot_bscan(residual, scan_x, time,
                      save_path=save_path, show=show,
                      clip_pct=0.5, title='Residual B-scan')
