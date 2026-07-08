"""
Material property management for the FDTD simulation.

Stores relative permittivity (eps_r), electrical conductivity (sigma),
and relative permeability (mu_r) as 2D arrays over the Yee grid.
Computes the FDTD update coefficients Ca and Cb for the electric field.
"""
import numpy as np


class MaterialModel:
    """
    Holds material property arrays and computes FDTD update coefficients.

    Array convention: shape (Nz, Nx) with z as first index (depth, rows)
    and x as second index (lateral, columns). z increases downward.

    Attributes
    ----------
    epsilon_r : ndarray, shape (Nz, Nx)
        Relative permittivity.
    sigma : ndarray, shape (Nz, Nx)
        Electrical conductivity [S/m].
    mu_r : ndarray, shape (Nz, Nx)
        Relative permeability.
    """

    def __init__(self, Nz, Nx, eps_r_bg=1.0, sigma_bg=0.0, mu_r_bg=1.0):
        """
        Initialize with uniform background properties.

        Parameters
        ----------
        Nz, Nx : int
            Grid dimensions.
        eps_r_bg : float
            Background relative permittivity.
        sigma_bg : float
            Background conductivity [S/m].
        mu_r_bg : float
            Background relative permeability.
        """
        self.Nz = Nz
        self.Nx = Nx
        self.epsilon_r = np.full((Nz, Nx), eps_r_bg, dtype=np.float64)
        self.sigma = np.full((Nz, Nx), sigma_bg, dtype=np.float64)
        self.mu_r = np.full((Nz, Nx), mu_r_bg, dtype=np.float64)

    def set_region(self, z_slice, x_slice, eps_r, sigma, mu_r=1.0):
        """Set material properties in a rectangular region."""
        self.epsilon_r[z_slice, x_slice] = eps_r
        self.sigma[z_slice, x_slice] = sigma
        self.mu_r[z_slice, x_slice] = mu_r

    def add_circle(self, z_center_m, x_center_m, radius_m, eps_r, sigma,
                   dz, dx, npml, mu_r=1.0):
        """
        Set material properties inside a circular region.

        Parameters
        ----------
        z_center_m, x_center_m : float
            Circle center in physical coordinates [m].
        radius_m : float
            Circle radius [m].
        eps_r, sigma : float
            Material properties to assign inside the circle.
        dz, dx : float
            Grid spacings [m].
        npml : int
            PML offset (added to convert physical to grid coords).
        mu_r : float
            Relative permeability.
        """
        iz_c = int(np.round(z_center_m / dz)) + npml
        ix_c = int(np.round(x_center_m / dx)) + npml
        ir = int(np.ceil(radius_m / dz)) + 1  # search radius in cells

        for iz in range(max(0, iz_c - ir), min(self.Nz, iz_c + ir + 1)):
            for ix in range(max(0, ix_c - ir), min(self.Nx, ix_c + ir + 1)):
                dz_phys = (iz - iz_c) * dz
                dx_phys = (ix - ix_c) * dx
                if dz_phys**2 + dx_phys**2 <= radius_m**2:
                    self.epsilon_r[iz, ix] = eps_r
                    self.sigma[iz, ix] = sigma
                    self.mu_r[iz, ix] = mu_r

    def add_circle_subcell(self, z_center_m, x_center_m, radius_m, eps_r, sigma,
                           dz, dx, npml, samples=5, mu_r=1.0):
        """
        Blend material properties using sub-cell circular area fractions.

        This avoids radius plateaus from hard node rasterization. Each grid
        sample represents the control volume around an Ez node. The material
        epsilon and permeability are linearly blended between the current
        background value and the inclusion value according to the fraction of
        sub-samples inside the circle. Conductivity is blended in log-space so
        a partial steel cell does not immediately behave like a full steel
        cell.
        """
        if samples < 1:
            raise ValueError("samples must be >= 1")
        samples = int(samples)

        iz_c = int(np.round(z_center_m / dz)) + npml
        ix_c = int(np.round(x_center_m / dx)) + npml
        ir_z = int(np.ceil(radius_m / dz)) + 2
        ir_x = int(np.ceil(radius_m / dx)) + 2

        offsets_z = (np.arange(samples, dtype=np.float64) + 0.5) / samples - 0.5
        offsets_x = (np.arange(samples, dtype=np.float64) + 0.5) / samples - 0.5
        zz, xx = np.meshgrid(offsets_z * dz, offsets_x * dx, indexing="ij")
        n_total = float(samples * samples)

        for iz in range(max(0, iz_c - ir_z), min(self.Nz, iz_c + ir_z + 1)):
            z_node = (iz - npml) * dz
            for ix in range(max(0, ix_c - ir_x), min(self.Nx, ix_c + ir_x + 1)):
                x_node = (ix - npml) * dx
                dist2 = (z_node + zz - z_center_m) ** 2 + (x_node + xx - x_center_m) ** 2
                fraction = np.count_nonzero(dist2 <= radius_m**2) / n_total
                if fraction <= 0.0:
                    continue
                self.epsilon_r[iz, ix] = (
                    (1.0 - fraction) * self.epsilon_r[iz, ix] + fraction * eps_r
                )
                sigma_bg = max(float(self.sigma[iz, ix]), 1e-12)
                sigma_inc = max(float(sigma), 1e-12)
                self.sigma[iz, ix] = np.exp(
                    (1.0 - fraction) * np.log(sigma_bg) + fraction * np.log(sigma_inc)
                )
                self.mu_r[iz, ix] = (
                    (1.0 - fraction) * self.mu_r[iz, ix] + fraction * mu_r
                )

    def get_update_coefficients(self, dt, eps0):
        """
        Compute FDTD electric field update coefficients Ca and Cb.

        From the discretized Ez update equation with conductive losses:

            Ca = (1 - sigma*dt/(2*eps)) / (1 + sigma*dt/(2*eps))
            Cb = (dt / eps)             / (1 + sigma*dt/(2*eps))

        where eps = eps0 * eps_r.

        Parameters
        ----------
        dt : float
            Time step [s].
        eps0 : float
            Vacuum permittivity [F/m].

        Returns
        -------
        Ca, Cb : ndarray, shape (Nz, Nx)
            Update coefficients for the Ez field.
        """
        eps = eps0 * self.epsilon_r
        loss = self.sigma * dt / (2.0 * eps)
        Ca = (1.0 - loss) / (1.0 + loss)
        Cb = (dt / eps) / (1.0 + loss)
        return Ca, Cb

    def get_magnetic_coefficient(self, dt, mu0):
        """
        Compute magnetic field update coefficient: dt / (mu0 * mu_r).

        Returns
        -------
        Dh : ndarray, shape (Nz, Nx)
            Coefficient for H-field update.
        """
        return dt / (mu0 * self.mu_r)

    def copy(self):
        """Return a deep copy of this MaterialModel."""
        new = MaterialModel(self.Nz, self.Nx)
        new.epsilon_r = self.epsilon_r.copy()
        new.sigma = self.sigma.copy()
        new.mu_r = self.mu_r.copy()
        return new
