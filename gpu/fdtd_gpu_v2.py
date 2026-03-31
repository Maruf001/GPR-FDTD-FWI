"""
GPU-accelerated 2D TMz FDTD with CPML — Version 2.

Extends gpu/fdtd_gpu.py (v1, field updates only) to include full CPML
absorbing boundary corrections on the GPU. This makes the entire
time-stepping loop GPU-resident, eliminating CPU-GPU synchronisation
that limited v1 performance.

Version history:
    v1 (fdtd_gpu.py)    — GPU field updates, no CPML
    v2 (fdtd_gpu_v2.py) — GPU field updates + GPU CPML (this file)
"""
import numpy as np

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    HAS_CUPY = False

from gpu.cpml_gpu import CPML_GPU
import config as cfg


class FDTDSimulatorGPU_v2:
    """
    GPU-accelerated 2D TMz FDTD simulator with CPML.

    Drop-in replacement for core.fdtd.FDTDSimulator. All field updates
    and CPML corrections execute on the GPU.
    """

    def __init__(self, model, config=None):
        """
        Initialize GPU simulator with CPML.

        Parameters
        ----------
        model : MaterialModel
            CPU-side material model.
        config : module, optional
            Configuration module. Defaults to the global config.
        """
        if not HAS_CUPY:
            raise RuntimeError("CuPy is not installed. GPU acceleration unavailable.")

        if config is None:
            config = cfg

        self.Nz = model.Nz
        self.Nx = model.Nx
        self.dt = config.DT
        self.dx = config.DX
        self.dz = config.DZ

        # Transfer update coefficients to GPU
        Ca, Cb = model.get_update_coefficients(config.DT, config.EPS0)
        Dh = model.get_magnetic_coefficient(config.DT, config.MU0)

        self.Ca = cp.asarray(Ca)
        self.Cb = cp.asarray(Cb)
        self.Dh = cp.asarray(Dh)

        # Field arrays on GPU
        self.Ez = cp.zeros((self.Nz, self.Nx), dtype=cp.float64)
        self.Hx = cp.zeros((self.Nz, self.Nx), dtype=cp.float64)
        self.Hy = cp.zeros((self.Nz, self.Nx), dtype=cp.float64)

        # GPU CPML
        self.cpml = CPML_GPU(
            self.Nz, self.Nx, config.NPML,
            config.DT, config.DX, config.DZ, config.EPS0
        )

    def reset_fields(self):
        """Zero all field and CPML arrays."""
        self.Ez[:] = 0.0
        self.Hx[:] = 0.0
        self.Hy[:] = 0.0
        self.cpml.reset()

    def step(self, source_val, src_iz, src_ix):
        """One complete time step on GPU (H update + CPML + E update + CPML + source)."""
        # H update
        self.Hx[:-1, :] -= (self.Dh[:-1, :] / self.dz) * (
            self.Ez[1:, :] - self.Ez[:-1, :]
        )
        self.Hy[:, :-1] += (self.Dh[:, :-1] / self.dx) * (
            self.Ez[:, 1:] - self.Ez[:, :-1]
        )

        # CPML H corrections
        self.cpml.update_H(self.Ez, self.Hx, self.Hy, self.Dh)

        # E update
        self.Ez[1:, 1:] = (
            self.Ca[1:, 1:] * self.Ez[1:, 1:]
            + self.Cb[1:, 1:] * (
                (self.Hy[1:, 1:] - self.Hy[1:, :-1]) / self.dx
                - (self.Hx[1:, 1:] - self.Hx[:-1, 1:]) / self.dz
            )
        )

        # CPML E corrections
        self.cpml.update_E(self.Ez, self.Hx, self.Hy, self.Cb)

        # Source injection
        self.Ez[src_iz, src_ix] += source_val

    def run(self, source_waveform, src_iz, src_ix, rec_iz, rec_ix,
            save_all_fields=False):
        """
        Run forward simulation on GPU with CPML.

        Parameters
        ----------
        source_waveform : ndarray, shape (nt,)
        src_iz, src_ix : int — source grid position
        rec_iz, rec_ix : int — receiver grid position
        save_all_fields : bool
            If True, store Ez at every time step (for adjoint method).

        Returns
        -------
        dict with 'trace' and optionally 'fields'.
        """
        nt = len(source_waveform)
        source_gpu = cp.asarray(source_waveform)
        trace = np.zeros(nt, dtype=np.float64)
        fields = [] if save_all_fields else None

        self.reset_fields()

        for n in range(nt):
            self.step(float(source_gpu[n]), src_iz, src_ix)
            trace[n] = float(self.Ez[rec_iz, rec_ix])
            if save_all_fields:
                fields.append(cp.asnumpy(self.Ez.copy()))

        result = {'trace': trace}
        if save_all_fields:
            result['fields'] = fields
        return result
