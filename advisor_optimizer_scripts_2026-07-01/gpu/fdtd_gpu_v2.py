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

    def run_batch(self, source_waveform, scan_positions):
        """
        Run a B-scan batch on GPU with one field stack per scan position.

        Parameters
        ----------
        source_waveform : ndarray, shape (nt,)
            Source amplitude at each time step. The same waveform is used for
            every source in the batch.
        scan_positions : sequence of tuple
            Tuples ordered as (src_iz, src_ix, rec_iz, rec_ix).

        Returns
        -------
        dict
            ``bscan`` has shape (nt, n_positions), matching the pipeline's
            CPU-side B-scan convention.
        """
        scan_positions = list(scan_positions)
        if not scan_positions:
            return {'bscan': np.zeros((len(source_waveform), 0), dtype=np.float64)}

        source_waveform = np.asarray(source_waveform, dtype=np.float64)
        nt = len(source_waveform)
        batch_size = len(scan_positions)

        position_width = len(scan_positions[0])
        if position_width == 4:
            positions = np.asarray(scan_positions, dtype=np.int64)
            src_iz = cp.asarray(positions[:, 0])
            src_ix = cp.asarray(positions[:, 1])
            rec_iz = cp.asarray(positions[:, 2])
            rec_ix_left = cp.asarray(positions[:, 3])
            rec_ix_right = rec_ix_left
            rec_weight_right = cp.zeros(batch_size, dtype=cp.float64)
        elif position_width == 6:
            positions = np.asarray(scan_positions, dtype=np.float64)
            src_iz = cp.asarray(positions[:, 0].astype(np.int64))
            src_ix = cp.asarray(positions[:, 1].astype(np.int64))
            rec_iz = cp.asarray(positions[:, 2].astype(np.int64))
            rec_ix_left = cp.asarray(positions[:, 3].astype(np.int64))
            rec_ix_right = cp.asarray(positions[:, 4].astype(np.int64))
            rec_weight_right = cp.asarray(positions[:, 5])
        else:
            raise ValueError("scan positions must have 4 or 6 entries")
        batch = cp.arange(batch_size)

        Ez = cp.zeros((batch_size, self.Nz, self.Nx), dtype=cp.float64)
        Hx = cp.zeros_like(Ez)
        Hy = cp.zeros_like(Ez)
        trace = cp.empty((nt, batch_size), dtype=cp.float64)

        n = self.cpml.npml
        psi_Hxz_lo = cp.zeros((batch_size, n, self.Nx), dtype=cp.float64)
        psi_Hxz_hi = cp.zeros((batch_size, n, self.Nx), dtype=cp.float64)
        psi_Hyx_lo = cp.zeros((batch_size, self.Nz, n), dtype=cp.float64)
        psi_Hyx_hi = cp.zeros((batch_size, self.Nz, n), dtype=cp.float64)
        psi_Ezx_lo = cp.zeros((batch_size, self.Nz, n), dtype=cp.float64)
        psi_Ezx_hi = cp.zeros((batch_size, self.Nz, n), dtype=cp.float64)
        psi_Ezz_lo = cp.zeros((batch_size, n, self.Nx), dtype=cp.float64)
        psi_Ezz_hi = cp.zeros((batch_size, n, self.Nx), dtype=cp.float64)

        for it in range(nt):
            Hx[:, :-1, :] -= (self.Dh[None, :-1, :] / self.dz) * (
                Ez[:, 1:, :] - Ez[:, :-1, :]
            )
            Hy[:, :, :-1] += (self.Dh[None, :, :-1] / self.dx) * (
                Ez[:, :, 1:] - Ez[:, :, :-1]
            )

            n_top = min(n, self.Nz - 1)
            dEz_dz = (Ez[:, 1:n_top + 1, :] - Ez[:, :n_top, :]) / self.dz
            psi_Hxz_lo[:, :n_top, :] = (
                self.cpml.bz_h[None, :n_top, None] * psi_Hxz_lo[:, :n_top, :]
                + self.cpml.cz_h[None, :n_top, None] * dEz_dz
            )
            Hx[:, :n_top, :] -= self.Dh[None, :n_top, :] * psi_Hxz_lo[:, :n_top, :]

            iz_start = max(self.Nz - n, 0)
            iz_end = self.Nz - 1
            if iz_start < iz_end:
                n_bot = iz_end - iz_start
                ip_start = iz_start - (self.Nz - n)
                dEz_dz = (Ez[:, iz_start + 1:iz_end + 1, :] - Ez[:, iz_start:iz_end, :]) / self.dz
                b_coeffs = self.cpml.bz_h_rev[None, ip_start:ip_start + n_bot, None]
                c_coeffs = self.cpml.cz_h_rev[None, ip_start:ip_start + n_bot, None]
                psi_Hxz_hi[:, ip_start:ip_start + n_bot, :] = (
                    b_coeffs * psi_Hxz_hi[:, ip_start:ip_start + n_bot, :]
                    + c_coeffs * dEz_dz
                )
                Hx[:, iz_start:iz_end, :] -= (
                    self.Dh[None, iz_start:iz_end, :]
                    * psi_Hxz_hi[:, ip_start:ip_start + n_bot, :]
                )

            n_left = min(n, self.Nx - 1)
            dEz_dx = (Ez[:, :, 1:n_left + 1] - Ez[:, :, :n_left]) / self.dx
            psi_Hyx_lo[:, :, :n_left] = (
                self.cpml.bx_h[None, None, :n_left] * psi_Hyx_lo[:, :, :n_left]
                + self.cpml.cx_h[None, None, :n_left] * dEz_dx
            )
            Hy[:, :, :n_left] += self.Dh[None, :, :n_left] * psi_Hyx_lo[:, :, :n_left]

            ix_start = max(self.Nx - n, 0)
            ix_end = self.Nx - 1
            if ix_start < ix_end:
                n_right = ix_end - ix_start
                ip_start = ix_start - (self.Nx - n)
                dEz_dx = (Ez[:, :, ix_start + 1:ix_end + 1] - Ez[:, :, ix_start:ix_end]) / self.dx
                b_coeffs = self.cpml.bx_h_rev[None, None, ip_start:ip_start + n_right]
                c_coeffs = self.cpml.cx_h_rev[None, None, ip_start:ip_start + n_right]
                psi_Hyx_hi[:, :, ip_start:ip_start + n_right] = (
                    b_coeffs * psi_Hyx_hi[:, :, ip_start:ip_start + n_right]
                    + c_coeffs * dEz_dx
                )
                Hy[:, :, ix_start:ix_end] += (
                    self.Dh[None, :, ix_start:ix_end]
                    * psi_Hyx_hi[:, :, ip_start:ip_start + n_right]
                )

            Ez[:, 1:, 1:] = (
                self.Ca[None, 1:, 1:] * Ez[:, 1:, 1:]
                + self.Cb[None, 1:, 1:] * (
                    (Hy[:, 1:, 1:] - Hy[:, 1:, :-1]) / self.dx
                    - (Hx[:, 1:, 1:] - Hx[:, :-1, 1:]) / self.dz
                )
            )

            if n > 1:
                dHy_dx = (Hy[:, :, 1:n] - Hy[:, :, :n - 1]) / self.dx
                psi_Ezx_lo[:, :, 1:n] = (
                    self.cpml.bx_e[None, None, 1:n] * psi_Ezx_lo[:, :, 1:n]
                    + self.cpml.cx_e[None, None, 1:n] * dHy_dx
                )
                Ez[:, 1:, 1:n] += self.Cb[None, 1:, 1:n] * psi_Ezx_lo[:, 1:, 1:n]

            ix_start = max(self.Nx - n, 1)
            if ix_start < self.Nx:
                n_right = self.Nx - ix_start
                ip_start = ix_start - (self.Nx - n)
                dHy_dx = (Hy[:, :, ix_start:self.Nx] - Hy[:, :, ix_start - 1:self.Nx - 1]) / self.dx
                b_coeffs = self.cpml.bx_e_rev[None, None, ip_start:ip_start + n_right]
                c_coeffs = self.cpml.cx_e_rev[None, None, ip_start:ip_start + n_right]
                psi_Ezx_hi[:, :, ip_start:ip_start + n_right] = (
                    b_coeffs * psi_Ezx_hi[:, :, ip_start:ip_start + n_right]
                    + c_coeffs * dHy_dx
                )
                Ez[:, 1:, ix_start:self.Nx] += (
                    self.Cb[None, 1:, ix_start:self.Nx]
                    * psi_Ezx_hi[:, 1:, ip_start:ip_start + n_right]
                )

            if n > 1:
                dHx_dz = (Hx[:, 1:n, :] - Hx[:, :n - 1, :]) / self.dz
                psi_Ezz_lo[:, 1:n, :] = (
                    self.cpml.bz_e[None, 1:n, None] * psi_Ezz_lo[:, 1:n, :]
                    + self.cpml.cz_e[None, 1:n, None] * dHx_dz
                )
                Ez[:, 1:n, 1:] -= self.Cb[None, 1:n, 1:] * psi_Ezz_lo[:, 1:n, 1:]

            iz_start = max(self.Nz - n, 1)
            if iz_start < self.Nz:
                n_bot = self.Nz - iz_start
                ip_start = iz_start - (self.Nz - n)
                dHx_dz = (Hx[:, iz_start:self.Nz, :] - Hx[:, iz_start - 1:self.Nz - 1, :]) / self.dz
                b_coeffs = self.cpml.bz_e_rev[None, ip_start:ip_start + n_bot, None]
                c_coeffs = self.cpml.cz_e_rev[None, ip_start:ip_start + n_bot, None]
                psi_Ezz_hi[:, ip_start:ip_start + n_bot, :] = (
                    b_coeffs * psi_Ezz_hi[:, ip_start:ip_start + n_bot, :]
                    + c_coeffs * dHx_dz
                )
                Ez[:, iz_start:self.Nz, 1:] -= (
                    self.Cb[None, iz_start:self.Nz, 1:]
                    * psi_Ezz_hi[:, ip_start:ip_start + n_bot, 1:]
                )

            Ez[batch, src_iz, src_ix] += source_waveform[it]
            left_values = Ez[batch, rec_iz, rec_ix_left]
            right_values = Ez[batch, rec_iz, rec_ix_right]
            trace[it, :] = (
                (1.0 - rec_weight_right) * left_values
                + rec_weight_right * right_values
            )

        return {'bscan': cp.asnumpy(trace)}

    def run(self, source_waveform, src_iz, src_ix, rec_iz, rec_ix,
            save_fields_every=0, save_all_fields=False):
        """
        Run forward simulation on GPU with CPML.

        Parameters
        ----------
        source_waveform : ndarray, shape (nt,)
        src_iz, src_ix : int — source grid position
        rec_iz, rec_ix : int — receiver grid position
        save_fields_every : int
            If > 0, store CPU Ez snapshots every N steps for animation.
        save_all_fields : bool
            If True, store Ez at every time step (for adjoint method).

        Returns
        -------
        dict with 'trace' and optionally 'snapshots' and 'fields'.
        """
        nt = len(source_waveform)
        source_waveform = np.asarray(source_waveform, dtype=np.float64)
        trace_gpu = cp.empty(nt, dtype=cp.float64)
        snapshots = []
        fields = [] if save_all_fields else None

        self.reset_fields()

        for n in range(nt):
            self.step(source_waveform[n], src_iz, src_ix)
            if isinstance(rec_ix, (tuple, list)):
                rec_ix_left, rec_ix_right, weight_right = rec_ix
                trace_gpu[n] = (
                    (1.0 - float(weight_right)) * self.Ez[rec_iz, int(rec_ix_left)]
                    + float(weight_right) * self.Ez[rec_iz, int(rec_ix_right)]
                )
            else:
                trace_gpu[n] = self.Ez[rec_iz, rec_ix]
            if save_fields_every and save_fields_every > 0 and n % int(save_fields_every) == 0:
                snapshots.append((n, cp.asnumpy(self.Ez.copy())))
            if save_all_fields:
                fields.append(cp.asnumpy(self.Ez.copy()))

        result = {'trace': cp.asnumpy(trace_gpu), 'snapshots': snapshots}
        if save_all_fields:
            result['fields'] = fields
        return result
