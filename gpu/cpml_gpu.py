"""
GPU-accelerated CPML (Convolutional Perfectly Matched Layer) for 2D TMz FDTD.

CuPy port of core/cpml.py. All psi arrays and coefficient profiles reside
on the GPU. The per-layer loops are replaced with vectorised 2D array
operations so the entire PML update executes as a few GPU kernel launches.

Version history:
    v1 (cpml_gpu.py) — Initial GPU port from core/cpml.py
"""
import numpy as np

try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    HAS_CUPY = False

import config as cfg


class CPML_GPU:
    """GPU-accelerated CPML absorbing boundary for 2D TMz FDTD."""

    def __init__(self, Nz, Nx, npml, dt, dx, dz, eps0):
        """Initialize CPML on GPU with graded polynomial profiles."""
        if not HAS_CUPY:
            raise RuntimeError("CuPy is not installed. GPU CPML unavailable.")

        self.Nz = Nz
        self.Nx = Nx
        self.npml = npml
        self.dt = dt
        self.dx = dx
        self.dz = dz

        # Compute profiles on CPU, then transfer to GPU
        sigma_max_x = (cfg.PML_SIGMA_OPT_FACTOR * (cfg.PML_ORDER + 1)
                       / (cfg.ETA0 * dx))
        sigma_max_z = (cfg.PML_SIGMA_OPT_FACTOR * (cfg.PML_ORDER + 1)
                       / (cfg.ETA0 * dz))

        bx_e, cx_e = self._profile(npml, sigma_max_x, dt, eps0, half=False)
        bx_h, cx_h = self._profile(npml, sigma_max_x, dt, eps0, half=True)
        bz_e, cz_e = self._profile(npml, sigma_max_z, dt, eps0, half=False)
        bz_h, cz_h = self._profile(npml, sigma_max_z, dt, eps0, half=True)

        # Transfer 1D profiles to GPU
        self.bx_e = cp.asarray(bx_e)
        self.cx_e = cp.asarray(cx_e)
        self.bx_h = cp.asarray(bx_h)
        self.cx_h = cp.asarray(cx_h)
        self.bz_e = cp.asarray(bz_e)
        self.cz_e = cp.asarray(cz_e)
        self.bz_h = cp.asarray(bz_h)
        self.cz_h = cp.asarray(cz_h)

        # Reversed coefficient arrays for the high-side boundaries
        self.bx_e_rev = self.bx_e[::-1].copy()
        self.cx_e_rev = self.cx_e[::-1].copy()
        self.bx_h_rev = self.bx_h[::-1].copy()
        self.cx_h_rev = self.cx_h[::-1].copy()
        self.bz_e_rev = self.bz_e[::-1].copy()
        self.cz_e_rev = self.cz_e[::-1].copy()
        self.bz_h_rev = self.bz_h[::-1].copy()
        self.cz_h_rev = self.cz_h[::-1].copy()

        # Psi arrays on GPU
        self.psi_Hxz_lo = cp.zeros((npml, Nx), dtype=cp.float64)
        self.psi_Hxz_hi = cp.zeros((npml, Nx), dtype=cp.float64)
        self.psi_Hyx_lo = cp.zeros((Nz, npml), dtype=cp.float64)
        self.psi_Hyx_hi = cp.zeros((Nz, npml), dtype=cp.float64)
        self.psi_Ezx_lo = cp.zeros((Nz, npml), dtype=cp.float64)
        self.psi_Ezx_hi = cp.zeros((Nz, npml), dtype=cp.float64)
        self.psi_Ezz_lo = cp.zeros((npml, Nx), dtype=cp.float64)
        self.psi_Ezz_hi = cp.zeros((npml, Nx), dtype=cp.float64)

    @staticmethod
    def _profile(npml, sigma_max, dt, eps0, half=False):
        """Compute b and c coefficient arrays (CPU, then transferred)."""
        d = np.arange(npml, dtype=np.float64)
        if half:
            d = d + 0.5
        d_norm = d / npml
        depth = 1.0 - d_norm

        sigma = sigma_max * depth ** cfg.PML_ORDER
        kappa = 1.0 + (cfg.PML_KAPPA_MAX - 1.0) * depth ** cfg.PML_ORDER
        alpha = cfg.PML_ALPHA_MAX * d_norm

        b = np.exp(-(sigma / kappa + alpha) * dt / eps0)
        denom = sigma * kappa + kappa**2 * alpha
        c = np.where(denom > 1e-30, sigma / denom * (b - 1.0), 0.0)
        return b, c

    def reset(self):
        """Zero all psi arrays on GPU."""
        for arr in [self.psi_Hxz_lo, self.psi_Hxz_hi,
                    self.psi_Hyx_lo, self.psi_Hyx_hi,
                    self.psi_Ezx_lo, self.psi_Ezx_hi,
                    self.psi_Ezz_lo, self.psi_Ezz_hi]:
            arr[:] = 0

    def update_H(self, Ez, Hx, Hy, Dh):
        """Apply CPML corrections to H-fields (all on GPU)."""
        n = self.npml
        Nz, Nx = self.Nz, self.Nx

        # Hx: z-PML (top, iz=0..n-1). Hx valid at iz=0..Nz-2
        n_top = min(n, Nz - 1)
        dEz_dz = (Ez[1:n_top+1, :] - Ez[:n_top, :]) / self.dz
        self.psi_Hxz_lo[:n_top, :] = (
            self.bz_h[:n_top, None] * self.psi_Hxz_lo[:n_top, :]
            + self.cz_h[:n_top, None] * dEz_dz
        )
        Hx[:n_top, :] -= Dh[:n_top, :] * self.psi_Hxz_lo[:n_top, :]

        # Hx: z-PML (bottom, iz=Nz-n..Nz-2)
        iz_start = max(Nz - n, 0)
        iz_end = Nz - 1  # Hx not valid at iz=Nz-1
        if iz_start < iz_end:
            sl = slice(iz_start, iz_end)
            n_bot = iz_end - iz_start
            ip_start = iz_start - (Nz - n)
            dEz_dz = (Ez[iz_start+1:iz_end+1, :] - Ez[iz_start:iz_end, :]) / self.dz
            b_coeffs = self.bz_h_rev[ip_start:ip_start+n_bot, None]
            c_coeffs = self.cz_h_rev[ip_start:ip_start+n_bot, None]
            self.psi_Hxz_hi[ip_start:ip_start+n_bot, :] = (
                b_coeffs * self.psi_Hxz_hi[ip_start:ip_start+n_bot, :]
                + c_coeffs * dEz_dz
            )
            Hx[sl, :] -= Dh[sl, :] * self.psi_Hxz_hi[ip_start:ip_start+n_bot, :]

        # Hy: x-PML (left, ix=0..n-1). Hy valid at ix=0..Nx-2
        n_left = min(n, Nx - 1)
        dEz_dx = (Ez[:, 1:n_left+1] - Ez[:, :n_left]) / self.dx
        self.psi_Hyx_lo[:, :n_left] = (
            self.bx_h[None, :n_left] * self.psi_Hyx_lo[:, :n_left]
            + self.cx_h[None, :n_left] * dEz_dx
        )
        Hy[:, :n_left] += Dh[:, :n_left] * self.psi_Hyx_lo[:, :n_left]

        # Hy: x-PML (right, ix=Nx-n..Nx-2)
        ix_start = max(Nx - n, 0)
        ix_end = Nx - 1
        if ix_start < ix_end:
            n_right = ix_end - ix_start
            ip_start = ix_start - (Nx - n)
            dEz_dx = (Ez[:, ix_start+1:ix_end+1] - Ez[:, ix_start:ix_end]) / self.dx
            b_coeffs = self.bx_h_rev[None, ip_start:ip_start+n_right]
            c_coeffs = self.cx_h_rev[None, ip_start:ip_start+n_right]
            self.psi_Hyx_hi[:, ip_start:ip_start+n_right] = (
                b_coeffs * self.psi_Hyx_hi[:, ip_start:ip_start+n_right]
                + c_coeffs * dEz_dx
            )
            Hy[:, ix_start:ix_end] += Dh[:, ix_start:ix_end] * self.psi_Hyx_hi[:, ip_start:ip_start+n_right]

    def update_E(self, Ez, Hx, Hy, Cb):
        """Apply CPML corrections to Ez (all on GPU)."""
        n = self.npml
        Nz, Nx = self.Nz, self.Nx

        # Ez: x-PML from dHy/dx (left, ix=1..n-1). Ez valid at ix>=1
        if n > 1:
            dHy_dx = (Hy[:, 1:n] - Hy[:, :n-1]) / self.dx
            self.psi_Ezx_lo[:, 1:n] = (
                self.bx_e[None, 1:n] * self.psi_Ezx_lo[:, 1:n]
                + self.cx_e[None, 1:n] * dHy_dx
            )
            Ez[1:, 1:n] += Cb[1:, 1:n] * self.psi_Ezx_lo[1:, 1:n]

        # Ez: x-PML from dHy/dx (right, ix=Nx-n..Nx-1)
        ix_start = max(Nx - n, 1)
        if ix_start < Nx:
            n_right = Nx - ix_start
            ip_start = ix_start - (Nx - n)
            dHy_dx = (Hy[:, ix_start:Nx] - Hy[:, ix_start-1:Nx-1]) / self.dx
            b_coeffs = self.bx_e_rev[None, ip_start:ip_start+n_right]
            c_coeffs = self.cx_e_rev[None, ip_start:ip_start+n_right]
            self.psi_Ezx_hi[:, ip_start:ip_start+n_right] = (
                b_coeffs * self.psi_Ezx_hi[:, ip_start:ip_start+n_right]
                + c_coeffs * dHy_dx
            )
            Ez[1:, ix_start:Nx] += Cb[1:, ix_start:Nx] * self.psi_Ezx_hi[1:, ip_start:ip_start+n_right]

        # Ez: z-PML from -dHx/dz (top, iz=1..n-1). Ez valid at iz>=1
        if n > 1:
            dHx_dz = (Hx[1:n, :] - Hx[:n-1, :]) / self.dz
            self.psi_Ezz_lo[1:n, :] = (
                self.bz_e[1:n, None] * self.psi_Ezz_lo[1:n, :]
                + self.cz_e[1:n, None] * dHx_dz
            )
            Ez[1:n, 1:] -= Cb[1:n, 1:] * self.psi_Ezz_lo[1:n, 1:]

        # Ez: z-PML from -dHx/dz (bottom, iz=Nz-n..Nz-1)
        iz_start = max(Nz - n, 1)
        if iz_start < Nz:
            n_bot = Nz - iz_start
            ip_start = iz_start - (Nz - n)
            dHx_dz = (Hx[iz_start:Nz, :] - Hx[iz_start-1:Nz-1, :]) / self.dz
            b_coeffs = self.bz_e_rev[ip_start:ip_start+n_bot, None]
            c_coeffs = self.cz_e_rev[ip_start:ip_start+n_bot, None]
            self.psi_Ezz_hi[ip_start:ip_start+n_bot, :] = (
                b_coeffs * self.psi_Ezz_hi[ip_start:ip_start+n_bot, :]
                + c_coeffs * dHx_dz
            )
            Ez[iz_start:Nz, 1:] -= Cb[iz_start:Nz, 1:] * self.psi_Ezz_hi[ip_start:ip_start+n_bot, 1:]
