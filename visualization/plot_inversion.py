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
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

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
        im = ax.pcolormesh(x_mm, z_mm, data, cmap='viridis',
                           shading='auto', vmin=vmin, vmax=vmax)
        ax.set_xlabel('x [mm]', fontsize=11)
        ax.set_ylabel('z [mm]', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.invert_yaxis()
        ax.set_aspect('equal')

        # Overlay true rebar outlines
        for z_c, x_c in cfg.REBAR_POSITIONS:
            circle = patches.Circle(
                (x_c * 1000, z_c * 1000),
                cfg.REBAR_RADIUS * 1000,
                linewidth=2.0, edgecolor='red', facecolor='none',
                linestyle='--',
            )
            ax.add_patch(circle)

    fig.colorbar(im, ax=axes, label=r'$\varepsilon_r$', shrink=0.85)
    fig.suptitle('Full-Waveform Inversion: Permittivity Recovery',
                 fontsize=15, fontweight='bold', y=1.02)

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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    iters = np.arange(1, len(misfit_history) + 1)

    # Left: log-scale misfit
    ax1.semilogy(iters, misfit_history, 'b-o', markersize=5, linewidth=1.5)
    ax1.set_xlabel('Function evaluation', fontsize=12)
    ax1.set_ylabel('Misfit J', fontsize=12)
    ax1.set_title('Convergence (log scale)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.annotate(f'Initial: {misfit_history[0]:.3e}',
                 xy=(1, misfit_history[0]),
                 xytext=(max(3, len(misfit_history)*0.15), misfit_history[0]*0.7),
                 fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))
    ax1.annotate(f'Final: {misfit_history[-1]:.3e}',
                 xy=(len(misfit_history), misfit_history[-1]),
                 xytext=(max(1, len(misfit_history)*0.6), misfit_history[-1]*3),
                 fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))

    # Right: normalized reduction
    normalized = np.array(misfit_history) / misfit_history[0]
    ax2.plot(iters, normalized * 100, 'r-s', markersize=4, linewidth=1.5)
    ax2.set_xlabel('Function evaluation', fontsize=12)
    ax2.set_ylabel('Misfit (% of initial)', fontsize=12)
    ax2.set_title('Relative Misfit Reduction', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    reduction = (1 - misfit_history[-1] / misfit_history[0]) * 100
    ax2.text(0.95, 0.95, f'{reduction:.1f}% reduction',
             transform=ax2.transAxes, fontsize=12, fontweight='bold',
             va='top', ha='right',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
