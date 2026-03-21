"""
Inversion result visualization.

Displays side-by-side comparison of initial, inverted, and true models,
plus convergence history.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import config as cfg


def plot_inversion_comparison(initial_epsr, inverted_epsr, true_epsr,
                              save_path=None, show=True):
    """
    Three-panel comparison: initial | inverted | ground truth.

    Parameters
    ----------
    initial_epsr, inverted_epsr, true_epsr : ndarray, shape (Nz, Nx)
        Relative permittivity arrays (full grid including PML).
    """
    n = cfg.NPML
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    datasets = [
        (initial_epsr[n:-n, n:-n], 'Initial Model'),
        (inverted_epsr[n:-n, n:-n], 'Inverted Model'),
        (true_epsr[n:-n, n:-n], 'Ground Truth'),
    ]

    x_mm = np.arange(datasets[0][0].shape[1]) * cfg.DX * 1000
    z_mm = np.arange(datasets[0][0].shape[0]) * cfg.DZ * 1000

    vmin = 1.0
    vmax = max(np.max(d[0]) for d in datasets)
    vmax = min(vmax, 10.0)

    for ax, (data, title) in zip(axes, datasets):
        im = ax.pcolormesh(x_mm, z_mm, data, cmap='viridis',
                           shading='auto', vmin=vmin, vmax=vmax)
        ax.set_xlabel('x [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_title(title)
        ax.invert_yaxis()
        ax.set_aspect('equal')

        # Overlay true rebar outlines
        for z_c, x_c in cfg.REBAR_POSITIONS:
            circle = patches.Circle(
                (x_c * 1000, z_c * 1000),
                cfg.REBAR_RADIUS * 1000,
                linewidth=1.5, edgecolor='red', facecolor='none',
                linestyle='--',
            )
            ax.add_patch(circle)

    fig.colorbar(im, ax=axes, label=r'$\varepsilon_r$', shrink=0.8)
    fig.suptitle('Full-Waveform Inversion Results', fontsize=14, y=1.02)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
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
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    iters = np.arange(1, len(misfit_history) + 1)
    ax.semilogy(iters, misfit_history, 'b-o', markersize=4)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Misfit J')
    ax.set_title('Inversion Convergence')
    ax.grid(True, alpha=0.3)

    # Annotate initial and final misfit
    ax.annotate(f'Initial: {misfit_history[0]:.4e}',
                xy=(1, misfit_history[0]),
                xytext=(3, misfit_history[0]),
                fontsize=9)
    ax.annotate(f'Final: {misfit_history[-1]:.4e}',
                xy=(len(misfit_history), misfit_history[-1]),
                xytext=(len(misfit_history) - 5, misfit_history[-1] * 2),
                fontsize=9)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
