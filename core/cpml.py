"""
Convolutional Perfectly Matched Layer (CPML) for 2D TMz FDTD.

Implements the CFS-PML using recursive convolution following
Roden & Gedney (2000).

Array convention: [iz, ix] where iz=z(depth), ix=x(lateral).
Hx[iz,ix] at (iz+1/2, ix) -> staggered in z -> z-PML affects Hx
Hy[iz,ix] at (iz, ix+1/2) -> staggered in x -> x-PML affects Hy

The CPML replaces the standard spatial derivative d/dx with:
    (1/kappa) * d/dx + psi
where psi is updated recursively:
    psi^{n+1} = b * psi^n + c * (d/dx)_standard

Important: PML corrections must only be applied where the standard
FDTD update also applies, to avoid modifying cells at the domain
boundary that serve as implicit PEC conditions.
  - Ez standard update: iz in [1, Nz-1], ix in [1, Nx-1]
  - Hx standard update: iz in [0, Nz-2]
  - Hy standard update: ix in [0, Nx-2]
"""
import numpy as np
import config as cfg


class CPML:
    """CPML absorbing boundary for 2D TMz FDTD."""

    def __init__(self, Nz, Nx, npml, dt, dx, dz, eps0):
        self.Nz = Nz
        self.Nx = Nx
        self.npml = npml
        self.dt = dt
        self.dx = dx
        self.dz = dz

        # sigma_max from Taflove: (m+1) * factor / (eta0 * dh)
        sigma_max_x = (cfg.PML_SIGMA_OPT_FACTOR * (cfg.PML_ORDER + 1)
                       / (cfg.ETA0 * dx))
        sigma_max_z = (cfg.PML_SIGMA_OPT_FACTOR * (cfg.PML_ORDER + 1)
                       / (cfg.ETA0 * dz))

        # Coefficient profiles: b and c arrays indexed [0..npml-1]
        # Index 0 = outermost cell (max absorption), index npml-1 = interface
        self.bx_e, self.cx_e = self._profile(npml, sigma_max_x, dt, eps0, half=False)
        self.bx_h, self.cx_h = self._profile(npml, sigma_max_x, dt, eps0, half=True)
        self.bz_e, self.cz_e = self._profile(npml, sigma_max_z, dt, eps0, half=False)
        self.bz_h, self.cz_h = self._profile(npml, sigma_max_z, dt, eps0, half=True)

        # Psi arrays for H corrections
        self.psi_Hxz_lo = np.zeros((npml, Nx))   # top z-PML for Hx
        self.psi_Hxz_hi = np.zeros((npml, Nx))   # bottom z-PML for Hx
        self.psi_Hyx_lo = np.zeros((Nz, npml))   # left x-PML for Hy
        self.psi_Hyx_hi = np.zeros((Nz, npml))   # right x-PML for Hy

        # Psi arrays for E corrections
        self.psi_Ezx_lo = np.zeros((Nz, npml))   # left x-PML for Ez
        self.psi_Ezx_hi = np.zeros((Nz, npml))   # right x-PML for Ez
        self.psi_Ezz_lo = np.zeros((npml, Nx))   # top z-PML for Ez
        self.psi_Ezz_hi = np.zeros((npml, Nx))   # bottom z-PML for Ez

    def _profile(self, npml, sigma_max, dt, eps0, half=False):
        """
        Compute b and c coefficient arrays.

        Index 0 = outermost PML cell, index npml-1 = interface.
        """
        d = np.arange(npml, dtype=np.float64)
        if half:
            d = d + 0.5
        d_norm = d / npml  # 0 at outer, 1 at interface

        # Depth: 1 at outer boundary, 0 at interface
        depth = 1.0 - d_norm

        sigma = sigma_max * depth ** cfg.PML_ORDER
        kappa = 1.0 + (cfg.PML_KAPPA_MAX - 1.0) * depth ** cfg.PML_ORDER
        alpha = cfg.PML_ALPHA_MAX * d_norm  # 0 at outer, max at interface

        b = np.exp(-(sigma / kappa + alpha) * dt / eps0)

        denom = sigma * kappa + kappa**2 * alpha
        c = np.where(denom > 1e-30, sigma / denom * (b - 1.0), 0.0)

        return b, c

    def reset(self):
        """Zero all psi arrays."""
        for arr in [self.psi_Hxz_lo, self.psi_Hxz_hi,
                    self.psi_Hyx_lo, self.psi_Hyx_hi,
                    self.psi_Ezx_lo, self.psi_Ezx_hi,
                    self.psi_Ezz_lo, self.psi_Ezz_hi]:
            arr[:] = 0

    def update_H(self, Ez, Hx, Hy, Dh):
        """
        Apply CPML corrections to H-fields after standard H update.

        Hx is affected by z-PML (top/bottom boundaries).
        Hy is affected by x-PML (left/right boundaries).

        Standard Hx update covers iz in [0, Nz-2].
        Standard Hy update covers ix in [0, Nx-2].
        """
        n = self.npml
        Nz, Nx = self.Nz, self.Nx

        # --- Hx: z-PML correction (top boundary, iz = 0..n-1) ---
        for ip in range(n):
            iz = ip
            if iz > Nz - 2:
                continue  # Hx not standard-updated at iz=Nz-1
            dEz_dz = (Ez[iz + 1, :] - Ez[iz, :]) / self.dz
            self.psi_Hxz_lo[ip, :] = (self.bz_h[ip] * self.psi_Hxz_lo[ip, :]
                                       + self.cz_h[ip] * dEz_dz)
            Hx[iz, :] -= Dh[iz, :] * self.psi_Hxz_lo[ip, :]

        # --- Hx: z-PML correction (bottom boundary, iz = Nz-n..Nz-1) ---
        for ip in range(n):
            iz = Nz - n + ip
            ic = n - 1 - ip  # outer boundary coefficient at ip=n-1 -> ic=0
            if iz > Nz - 2:
                continue  # Hx not standard-updated at iz=Nz-1
            dEz_dz = (Ez[iz + 1, :] - Ez[iz, :]) / self.dz
            self.psi_Hxz_hi[ip, :] = (self.bz_h[ic] * self.psi_Hxz_hi[ip, :]
                                       + self.cz_h[ic] * dEz_dz)
            Hx[iz, :] -= Dh[iz, :] * self.psi_Hxz_hi[ip, :]

        # --- Hy: x-PML correction (left boundary, ix = 0..n-1) ---
        for ip in range(n):
            ix = ip
            if ix > Nx - 2:
                continue  # Hy not standard-updated at ix=Nx-1
            dEz_dx = (Ez[:, ix + 1] - Ez[:, ix]) / self.dx
            self.psi_Hyx_lo[:, ip] = (self.bx_h[ip] * self.psi_Hyx_lo[:, ip]
                                       + self.cx_h[ip] * dEz_dx)
            Hy[:, ix] += Dh[:, ix] * self.psi_Hyx_lo[:, ip]

        # --- Hy: x-PML correction (right boundary, ix = Nx-n..Nx-1) ---
        for ip in range(n):
            ix = Nx - n + ip
            ic = n - 1 - ip
            if ix > Nx - 2:
                continue  # Hy not standard-updated at ix=Nx-1
            dEz_dx = (Ez[:, ix + 1] - Ez[:, ix]) / self.dx
            self.psi_Hyx_hi[:, ip] = (self.bx_h[ic] * self.psi_Hyx_hi[:, ip]
                                       + self.cx_h[ic] * dEz_dx)
            Hy[:, ix] += Dh[:, ix] * self.psi_Hyx_hi[:, ip]

    def update_E(self, Ez, Hx, Hy, Cb):
        """
        Apply CPML corrections to Ez after standard E update.

        Standard Ez update covers iz in [1, Nz-1], ix in [1, Nx-1].
        PML corrections must skip iz=0 and ix=0 (PEC outer boundary).
        """
        n = self.npml
        Nz, Nx = self.Nz, self.Nx

        # --- Ez: x-PML correction from dHy/dx (left boundary) ---
        for ip in range(n):
            ix = ip
            if ix < 1:
                continue  # Ez not standard-updated at ix=0
            dHy_dx = (Hy[:, ix] - Hy[:, ix - 1]) / self.dx
            self.psi_Ezx_lo[:, ip] = (self.bx_e[ip] * self.psi_Ezx_lo[:, ip]
                                       + self.cx_e[ip] * dHy_dx)
            Ez[1:, ix] += Cb[1:, ix] * self.psi_Ezx_lo[1:, ip]

        # --- Ez: x-PML correction from dHy/dx (right boundary) ---
        for ip in range(n):
            ix = Nx - n + ip
            ic = n - 1 - ip
            if ix < 1:
                continue
            dHy_dx = (Hy[:, ix] - Hy[:, ix - 1]) / self.dx
            self.psi_Ezx_hi[:, ip] = (self.bx_e[ic] * self.psi_Ezx_hi[:, ip]
                                       + self.cx_e[ic] * dHy_dx)
            Ez[1:, ix] += Cb[1:, ix] * self.psi_Ezx_hi[1:, ip]

        # --- Ez: z-PML correction from -dHx/dz (top boundary) ---
        for ip in range(n):
            iz = ip
            if iz < 1:
                continue  # Ez not standard-updated at iz=0
            dHx_dz = (Hx[iz, :] - Hx[iz - 1, :]) / self.dz
            self.psi_Ezz_lo[ip, :] = (self.bz_e[ip] * self.psi_Ezz_lo[ip, :]
                                       + self.cz_e[ip] * dHx_dz)
            Ez[iz, 1:] -= Cb[iz, 1:] * self.psi_Ezz_lo[ip, 1:]

        # --- Ez: z-PML correction from -dHx/dz (bottom boundary) ---
        for ip in range(n):
            iz = Nz - n + ip
            ic = n - 1 - ip
            dHx_dz = (Hx[iz, :] - Hx[iz - 1, :]) / self.dz
            self.psi_Ezz_hi[ip, :] = (self.bz_e[ic] * self.psi_Ezz_hi[ip, :]
                                       + self.cz_e[ic] * dHx_dz)
            Ez[iz, 1:] -= Cb[iz, 1:] * self.psi_Ezz_hi[ip, 1:]
