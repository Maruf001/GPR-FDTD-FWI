"""
Distributed dipole antenna source model for GPR FDTD simulation.

Replaces the idealised point source with a short dipole antenna that
distributes the excitation over several grid cells. This produces a
more realistic radiation pattern — a point source radiates omnidirectionally,
while a finite-length dipole has a directional radiation pattern with
nulls along the dipole axis.

The antenna is modelled as a linear array of soft current sources along
the z-axis (vertical dipole), with a half-cosine amplitude taper for
smooth edges.

Version history:
    v1 (source.py)          — Point source (single cell)
    v2 (source_antenna.py)  — Distributed dipole antenna (this file)
"""
import numpy as np
from core.source import ricker_wavelet, generate_time_array


class DipoleAntenna:
    """
    Short dipole antenna for 2D TMz FDTD.

    The antenna distributes the source excitation over a vertical line
    of cells centred at (iz_center, ix_center), with a half-cosine
    amplitude tapering.

    Parameters
    ----------
    iz_center, ix_center : int
        Centre of the antenna (grid indices).
    length_m : float
        Total dipole length in metres.
    dz : float
        Grid spacing in z [m].
    """

    def __init__(self, iz_center, ix_center, length_m, dz):
        self.ix = ix_center
        self.dz = dz

        # Compute the cells spanned by the dipole
        n_half = int(np.round(length_m / (2.0 * dz)))
        n_half = max(n_half, 1)

        self.iz_cells = list(range(iz_center - n_half, iz_center + n_half + 1))
        n_cells = len(self.iz_cells)

        # Half-cosine amplitude tapering (smooth edges, peak at centre)
        self.weights = np.zeros(n_cells)
        for k, iz in enumerate(self.iz_cells):
            offset = abs(iz - iz_center)
            self.weights[k] = np.cos(0.5 * np.pi * offset / (n_half + 0.5))

        # Normalise so total injected amplitude equals the point-source value
        self.weights /= np.sum(self.weights)

        self.n_cells = n_cells
        self.length_cells = 2 * n_half + 1
        self.length_m = self.length_cells * dz

    def inject(self, Ez, source_val):
        """
        Inject source into Ez field array (soft source, additive).

        Parameters
        ----------
        Ez : ndarray, shape (Nz, Nx)
            Electric field array (modified in place).
        source_val : float
            Source amplitude at this time step.
        """
        for k, iz in enumerate(self.iz_cells):
            Ez[iz, self.ix] += source_val * self.weights[k]


class DipoleReceiver:
    """
    Finite-length receiver antenna that integrates Ez over its aperture.

    Parameters
    ----------
    iz_center, ix_center : int
        Centre of the receiver antenna (grid indices).
    length_m : float
        Receiver aperture length in metres.
    dz : float
        Grid spacing in z [m].
    """

    def __init__(self, iz_center, ix_center, length_m, dz):
        self.ix = ix_center
        n_half = int(np.round(length_m / (2.0 * dz)))
        n_half = max(n_half, 1)

        self.iz_cells = list(range(iz_center - n_half, iz_center + n_half + 1))

        # Same cosine tapering as transmitter
        self.weights = np.zeros(len(self.iz_cells))
        for k, iz in enumerate(self.iz_cells):
            offset = abs(iz - iz_center)
            self.weights[k] = np.cos(0.5 * np.pi * offset / (n_half + 0.5))
        self.weights /= np.sum(self.weights)

    def record(self, Ez):
        """
        Record the weighted-average Ez over the receiver aperture.

        Parameters
        ----------
        Ez : ndarray, shape (Nz, Nx)

        Returns
        -------
        float : weighted average Ez at receiver.
        """
        total = 0.0
        for k, iz in enumerate(self.iz_cells):
            total += Ez[iz, self.ix] * self.weights[k]
        return total


def run_with_antenna(model, wavelet, src_iz, src_ix, rec_iz, rec_ix,
                     antenna_length_m=0.02):
    """
    Run FDTD simulation with dipole antenna source and receiver.

    Drop-in replacement for FDTDSimulator.run() but with distributed
    source and receiver.

    Parameters
    ----------
    model : MaterialModel
    wavelet : ndarray, shape (nt,)
    src_iz, src_ix : int — source centre position
    rec_iz, rec_ix : int — receiver centre position
    antenna_length_m : float — antenna length in metres (default 20 mm)

    Returns
    -------
    dict with 'trace'
    """
    from core.fdtd import FDTDSimulator
    import config as cfg

    sim = FDTDSimulator(model)
    nt = len(wavelet)

    tx = DipoleAntenna(src_iz, src_ix, antenna_length_m, cfg.DZ)
    rx = DipoleReceiver(rec_iz, rec_ix, antenna_length_m, cfg.DZ)

    trace = np.zeros(nt, dtype=np.float64)
    sim.reset_fields()

    for n in range(nt):
        # H update
        sim.Hx[:-1, :] -= (sim.Dh[:-1, :] / sim.dz) * (
            sim.Ez[1:, :] - sim.Ez[:-1, :]
        )
        sim.Hy[:, :-1] += (sim.Dh[:, :-1] / sim.dx) * (
            sim.Ez[:, 1:] - sim.Ez[:, :-1]
        )
        sim.cpml.update_H(sim.Ez, sim.Hx, sim.Hy, sim.Dh)

        # E update
        sim.Ez[1:, 1:] = (
            sim.Ca[1:, 1:] * sim.Ez[1:, 1:]
            + sim.Cb[1:, 1:] * (
                (sim.Hy[1:, 1:] - sim.Hy[1:, :-1]) / sim.dx
                - (sim.Hx[1:, 1:] - sim.Hx[:-1, 1:]) / sim.dz
            )
        )
        sim.cpml.update_E(sim.Ez, sim.Hx, sim.Hy, sim.Cb)

        # Distributed antenna source injection
        tx.inject(sim.Ez, wavelet[n])

        # Distributed receiver recording
        trace[n] = rx.record(sim.Ez)

    return {'trace': trace}
