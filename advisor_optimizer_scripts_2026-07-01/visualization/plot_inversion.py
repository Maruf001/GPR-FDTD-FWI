"""
Inversion result visualization.

Displays side-by-side comparison of initial, inverted, and true models,
plus convergence history.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import config as cfg
from visualization.plot_style import save_validated_figure


def plot_inversion_comparison(initial_epsr, inverted_epsr, true_epsr,
                              save_path=None, show=True, rebar_params=None):
    """
    Three-panel comparison: initial | inverted | ground truth.

    Parameters
    ----------
    initial_epsr, inverted_epsr, true_epsr : ndarray, shape (Nz, Nx)
        Relative permittivity arrays (full grid including PML).
    rebar_params : list of (z, x, radius), optional
        Rebar outlines to overlay in physical coordinates [m]. Defaults to the
        configured three-rebar scene.
    """
    n = cfg.NPML
    fig = plt.figure(figsize=(18, 5.5), constrained_layout=True)
    grid = fig.add_gridspec(1, 4, width_ratios=[1.0, 1.0, 1.0, 0.045], wspace=0.16)
    axes = [fig.add_subplot(grid[0, index]) for index in range(3)]
    cax = fig.add_subplot(grid[0, 3])

    datasets = [
        (initial_epsr[n:-n, n:-n], 'Initial Model\n(homogeneous concrete)'),
        (inverted_epsr[n:-n, n:-n], 'Inverted Model\n(FWI result)'),
        (true_epsr[n:-n, n:-n], 'Ground Truth'),
    ]

    x_mm = np.arange(datasets[0][0].shape[1]) * cfg.DX * 1000
    z_mm = np.arange(datasets[0][0].shape[0]) * cfg.DZ * 1000

    vmin = 1.0
    vmax = max(np.max(d[0]) for d in datasets)
    vmax = min(vmax, 10.0)

    for ax, (data, title) in zip(axes, datasets):
        extent = [float(x_mm[0]), float(x_mm[-1]), float(z_mm[-1]), float(z_mm[0])]
        im = ax.imshow(
            data,
            cmap='viridis',
            interpolation='nearest',
            extent=extent,
            aspect='equal',
            vmin=vmin,
            vmax=vmax,
        )
        ax.set_xlabel('x [mm]', fontsize=11)
        ax.set_ylabel('z [mm]', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')

        # Overlay true rebar outlines.
        if rebar_params is None:
            rebar_params = [
                (z_c, x_c, cfg.REBAR_RADIUS)
                for z_c, x_c in cfg.REBAR_POSITIONS
            ]
        for z_c, x_c, radius in rebar_params:
            circle = patches.Circle(
                (x_c * 1000, z_c * 1000),
                radius * 1000,
                linewidth=2.0, edgecolor='red', facecolor='none',
                linestyle='--',
            )
            ax.add_patch(circle)

    fig.colorbar(im, cax=cax, label=r'$\varepsilon_r$')
    fig.suptitle('Full-Waveform Inversion: Permittivity Recovery',
                 fontsize=15, fontweight='bold')

    if save_path:
        save_validated_figure(fig, save_path)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def plot_convergence(misfit_history, save_path=None, show=True):
    """
    Plot misfit vs iteration number.

    Parameters
    ----------
    misfit_history : list of float
        Misfit value at each iteration.
    """
    misfit_history = np.asarray(misfit_history, dtype=np.float64)
    if misfit_history.ndim != 1 or misfit_history.size == 0:
        raise ValueError("misfit_history must be a non-empty 1D array")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

    iters = np.arange(1, len(misfit_history) + 1)
    plot_values = np.maximum(misfit_history, 1e-30)

    # Left: log-scale misfit
    ax1.semilogy(iters, plot_values, 'b-o', markersize=4, linewidth=1.4)
    ax1.set_xlabel('Function evaluation', fontsize=12)
    ax1.set_ylabel('Misfit J', fontsize=12)
    ax1.set_title('Convergence (log scale)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.text(
        0.03,
        0.97,
        f"initial {misfit_history[0]:.3e}\nfinal {misfit_history[-1]:.3e}",
        transform=ax1.transAxes,
        va='top',
        ha='left',
        fontsize=9,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='0.8', alpha=0.9),
    )

    # Right: normalized reduction
    if abs(misfit_history[0]) > 1e-30:
        normalized = misfit_history / misfit_history[0]
        reduction_text = f"{(1.0 - misfit_history[-1] / misfit_history[0]) * 100.0:.1f}% reduction"
    else:
        normalized = np.zeros_like(misfit_history)
        reduction_text = "reduction n/a"
    ax2.plot(iters, normalized * 100, 'r-s', markersize=4, linewidth=1.4)
    ax2.set_xlabel('Function evaluation', fontsize=12)
    ax2.set_ylabel('Misfit (% of initial)', fontsize=12)
    ax2.set_title('Relative Misfit Reduction', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.text(0.97, 0.95, reduction_text,
             transform=ax2.transAxes, fontsize=12, fontweight='bold',
             va='top', ha='right',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    if save_path:
        save_validated_figure(fig, save_path)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
