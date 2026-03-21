"""
EM wave propagation animation.

Creates an animation of the Ez field as it propagates through the
domain, showing interactions with the concrete surface and rebars.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import config as cfg


def animate_wavefield(snapshots, save_path=None, show=True, fps=15):
    """
    Create animation of Ez field propagation.

    Parameters
    ----------
    snapshots : list of (step, Ez_array)
        Field snapshots from the FDTD simulation.
    save_path : str, optional
        Path to save animation (e.g., .gif or .mp4).
    show : bool
        Whether to display.
    fps : int
        Frames per second.

    Returns
    -------
    anim : FuncAnimation
    """
    if not snapshots:
        print("No snapshots to animate.")
        return None

    n = cfg.NPML

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Physical coordinates in mm
    first_field = snapshots[0][1][n:-n, n:-n]
    x_mm = np.arange(first_field.shape[1]) * cfg.DX * 1000
    z_mm = np.arange(first_field.shape[0]) * cfg.DZ * 1000

    # Determine color scale from max amplitude across all snapshots
    all_max = max(np.max(np.abs(s[1][n:-n, n:-n])) for s in snapshots)
    vmax = 0.3 * all_max if all_max > 0 else 1.0

    im = ax.pcolormesh(x_mm, z_mm, first_field, cmap='RdBu_r',
                       shading='auto', vmin=-vmax, vmax=vmax)
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('z [mm]')
    ax.invert_yaxis()
    ax.set_aspect('equal')
    fig.colorbar(im, ax=ax, label='Ez [V/m]')
    title = ax.set_title('')

    # Overlay rebar circles
    for z_c, x_c in cfg.REBAR_POSITIONS:
        circle = patches.Circle(
            (x_c * 1000, z_c * 1000),
            cfg.REBAR_RADIUS * 1000,
            linewidth=1, edgecolor='black', facecolor='none',
        )
        ax.add_patch(circle)

    # Concrete surface line
    ax.axhline(y=cfg.CONCRETE_TOP * 1000, color='gray', linestyle='--',
               linewidth=0.5)

    def update(frame):
        step, field = snapshots[frame]
        data = field[n:-n, n:-n]
        im.set_array(data.ravel())
        t_ns = step * cfg.DT * 1e9
        title.set_text(f'Ez field at t = {t_ns:.2f} ns (step {step})')
        return [im, title]

    anim = FuncAnimation(fig, update, frames=len(snapshots),
                         interval=1000 // fps, blit=False)

    plt.tight_layout()
    if save_path:
        print(f"Saving animation to {save_path}...")
        if save_path.endswith('.gif'):
            anim.save(save_path, writer='pillow', fps=fps)
        else:
            anim.save(save_path, writer='ffmpeg', fps=fps)
        print("Done.")
    if show:
        plt.show()
    else:
        plt.close(fig)
    return anim
