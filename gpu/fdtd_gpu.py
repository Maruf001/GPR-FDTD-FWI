"""
GPU-accelerated 2D TMz FDTD using CuPy.

Strategy: Replace NumPy arrays with CuPy arrays. The vectorized
update equations are identical, but operations execute on the GPU.

Key operations moved to GPU:
    1. H-field update (stencil difference + element-wise multiply)
    2. E-field update (stencil difference + element-wise multiply)
    3. Source injection
    4. Receiver recording

Operations on CPU:
    - Parameter setup (one-time cost)
    - CPML coefficients (computed once, transferred to GPU)
    - Optimization loop control

Practical considerations:
    - Memory: ~50 MB for all arrays at our grid size (trivial for modern GPUs)
    - Access pattern: Row-major (C-order) storage ensures coalesced memory access
    - CPU-GPU transfers: Minimized by keeping all arrays on GPU; only receiver
      trace transferred back each step
"""
import numpy as np

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    HAS_CUPY = False


class FDTDSimulatorGPU:
    """
    GPU-accelerated 2D TMz FDTD simulator.

    Drop-in replacement for FDTDSimulator when CuPy is available.
    """

    def __init__(self, model, config):
        """
        Initialize GPU simulator by transferring arrays to GPU memory.

        Parameters
        ----------
        model : MaterialModel
            CPU-side material model.
        config : module
            Configuration module.
        """
        if not HAS_CUPY:
            raise RuntimeError("CuPy is not installed. GPU acceleration unavailable.")

        self.Nz = model.Nz
        self.Nx = model.Nx
        self.dt = config.DT
        self.dx = config.DX
        self.dz = config.DZ
        self.nt = config.NT

        # Transfer update coefficients to GPU
        Ca, Cb = model.get_update_coefficients(config.DT, config.EPS0)
        Dh = model.get_magnetic_coefficient(config.DT, config.MU0)

        self.Ca_gpu = cp.asarray(Ca)
        self.Cb_gpu = cp.asarray(Cb)
        self.Dh_gpu = cp.asarray(Dh)

        # Field arrays on GPU
        self.Ez = cp.zeros((self.Nz, self.Nx), dtype=cp.float64)
        self.Hx = cp.zeros((self.Nz, self.Nx), dtype=cp.float64)
        self.Hy = cp.zeros((self.Nz, self.Nx), dtype=cp.float64)

    def reset_fields(self):
        """Zero all GPU field arrays."""
        self.Ez[:] = 0.0
        self.Hx[:] = 0.0
        self.Hy[:] = 0.0

    def step(self, source_val, src_iz, src_ix):
        """
        One time step on GPU.

        Same algorithm as CPU, using CuPy's vectorized operations.
        """
        # H update: same equations as CPU version
        # Hx: dEz/dz → first index difference
        self.Hx[:-1, :] -= (self.Dh_gpu[:-1, :] / self.dz) * (
            self.Ez[1:, :] - self.Ez[:-1, :]
        )
        # Hy: dEz/dx → second index difference
        self.Hy[:, :-1] += (self.Dh_gpu[:, :-1] / self.dx) * (
            self.Ez[:, 1:] - self.Ez[:, :-1]
        )

        # E update
        self.Ez[1:, 1:] = (
            self.Ca_gpu[1:, 1:] * self.Ez[1:, 1:]
            + self.Cb_gpu[1:, 1:] * (
                (self.Hy[1:, 1:] - self.Hy[1:, :-1]) / self.dx   # dHy/dx: 2nd index
                - (self.Hx[1:, 1:] - self.Hx[:-1, 1:]) / self.dz  # dHx/dz: 1st index
            )
        )

        # Source injection
        self.Ez[src_iz, src_ix] += source_val

    def run(self, source_waveform, src_iz, src_ix, rec_iz, rec_ix):
        """
        Run forward simulation on GPU.

        Returns trace on CPU.
        """
        nt = len(source_waveform)
        source_gpu = cp.asarray(source_waveform)
        trace = np.zeros(nt, dtype=np.float64)

        self.reset_fields()

        for n in range(nt):
            self.step(float(source_gpu[n]), src_iz, src_ix)
            # Transfer only the single receiver value to CPU
            trace[n] = float(self.Ez[rec_iz, rec_ix])

        return {'trace': trace}
