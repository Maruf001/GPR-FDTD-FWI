"""Spectrum diagnostic plots."""
import matplotlib.pyplot as plt
import numpy as np

from visualization.plot_style import save_validated_figure


def plot_average_spectra(spectra, save_path=None, show=True, title="Average spectra"):
    """Plot normalized average amplitude spectra."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5), constrained_layout=True)
    for item in spectra:
        freqs_ghz = np.asarray(item["freqs_hz"], dtype=np.float64) / 1e9
        amplitude = np.asarray(item["amplitude"], dtype=np.float64)
        scale = float(np.max(amplitude)) if amplitude.size else 0.0
        if scale > 0.0:
            amplitude = amplitude / scale
        ax.plot(freqs_ghz, amplitude, lw=1.7, label=item["label"])

    ax.set_xlim(left=0.0)
    ax.set_xlabel("Frequency [GHz]")
    ax.set_ylabel("Normalized mean amplitude")
    ax.set_title(title, fontweight="bold")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", fontsize=9)

    if save_path:
        save_validated_figure(fig, save_path)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig
