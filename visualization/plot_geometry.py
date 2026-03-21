"""
Visualization of the ground-truth model geometry.

Shows the spatial distribution of relative permittivity with
overlaid rebar locations and scan path.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import config as cfg


def plot_ground_truth(model, save_path=None, show=True):
    """
    Plot the ground-truth model showing material distribution.

    Parameters
    ----------
    model : MaterialModel
        The model to visualize.
    save_path : str, optional
        Path to save the figure.
    show : bool
        Whether to display the plot.
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Extract the physical domain (exclude PML)
    n = cfg.NPML
    eps_r = model.epsilon_r[n:-n, n:-n]

    # Physical coordinates in mm
    x_mm = np.arange(eps_r.shape[1]) * cfg.DX * 1000
    z_mm = np.arange(eps_r.shape[0]) * cfg.DZ * 1000

    im = ax.pcolormesh(x_mm, z_mm, eps_r, cmap='gray_r',
                       shading='auto', vmin=1, vmax=8)
    ax.set_xlabel('Lateral position x [mm]')
    ax.set_ylabel('Depth z [mm]')
    ax.set_title('Ground-Truth Model: Relative Permittivity')
    ax.invert_yaxis()
    ax.set_aspect('equal')

    cbar = fig.colorbar(im, ax=ax, label=r'$\varepsilon_r$')

    # Overlay rebar circles
    for z_c, x_c in cfg.REBAR_POSITIONS:
        circle = patches.Circle(
            (x_c * 1000, z_c * 1000),
            cfg.REBAR_RADIUS * 1000,
            linewidth=1.5, edgecolor='red', facecolor='none',
            linestyle='--', label='Rebar'
        )
        ax.add_patch(circle)

    # Mark concrete surface
    ax.axhline(y=cfg.CONCRETE_TOP * 1000, color='blue', linestyle='-',
               linewidth=1, label='Concrete surface')

    # Show scan path
    scan_z = cfg.TX_Z * 1000
    ax.axhline(y=scan_z, color='green', linestyle='--',
               linewidth=1, label='Scan path')

    # Avoid duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='lower right')

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
