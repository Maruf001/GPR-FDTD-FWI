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
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    # Extract the physical domain (exclude PML)
    n = cfg.NPML
    eps_r = model.epsilon_r[n:-n, n:-n]

    # Physical coordinates in mm
    x_mm = np.arange(eps_r.shape[1]) * cfg.DX * 1000
    z_mm = np.arange(eps_r.shape[0]) * cfg.DZ * 1000

    im = ax.pcolormesh(x_mm, z_mm, eps_r, cmap='YlOrBr',
                       shading='auto', vmin=1, vmax=8)
    ax.set_xlabel('Lateral position x [mm]', fontsize=12)
    ax.set_ylabel('Depth z [mm]', fontsize=12)
    ax.set_title('Ground-Truth Model: Relative Permittivity', fontsize=14,
                 fontweight='bold')
    ax.invert_yaxis()
    ax.set_aspect('equal')

    cbar = fig.colorbar(im, ax=ax, label=r'$\varepsilon_r$', shrink=0.9)
    cbar.ax.tick_params(labelsize=10)

    # Overlay rebar circles with better visibility
    for z_c, x_c in cfg.REBAR_POSITIONS:
        circle = patches.Circle(
            (x_c * 1000, z_c * 1000),
            cfg.REBAR_RADIUS * 1000,
            linewidth=2.0, edgecolor='red', facecolor='none',
            linestyle='-', label='Rebar', zorder=5
        )
        ax.add_patch(circle)
        # Add cross-hair at center
        ax.plot(x_c * 1000, z_c * 1000, 'r+', markersize=8, markeredgewidth=1.5,
                zorder=6)

    # Mark concrete surface
    ax.axhline(y=cfg.CONCRETE_TOP * 1000, color='#2196F3', linestyle='-',
               linewidth=2, label='Concrete surface')

    # Show scan path
    scan_z = cfg.TX_Z * 1000
    ax.axhline(y=scan_z, color='#4CAF50', linestyle='--',
               linewidth=1.5, label='Scan path')

    # Add dimension annotations
    # Cover depth annotation
    z_rebar = cfg.REBAR_POSITIONS[0][0] * 1000
    x_ann = cfg.REBAR_POSITIONS[-1][1] * 1000 + 40
    ax.annotate('', xy=(x_ann, cfg.CONCRETE_TOP * 1000),
                xytext=(x_ann, z_rebar),
                arrowprops=dict(arrowstyle='<->', color='white', lw=1.5))
    ax.text(x_ann + 5, (cfg.CONCRETE_TOP * 1000 + z_rebar) / 2,
            f'{cfg.REBAR_COVER*1000:.0f} mm\ncover',
            color='white', fontsize=9, va='center')

    # Avoid duplicate legend entries
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='lower right',
              fontsize=10, framealpha=0.9)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
