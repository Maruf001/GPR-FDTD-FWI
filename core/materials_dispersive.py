"""
Dispersive material model with single-pole Debye relaxation.

Extends core/materials.py to support frequency-dependent permittivity
via the Debye model:

    ε(ω) = ε_∞ + (ε_s - ε_∞) / (1 + jωτ)

where:
    ε_∞ = high-frequency (optical) permittivity
    ε_s  = static (DC) permittivity
    τ    = relaxation time [s]

In the time domain, this introduces an auxiliary polarisation current
that modifies the E-field update equation.

Typical concrete parameters at GPR frequencies (0.5–3 GHz):
    ε_s  ≈ 7.0   (static)
    ε_∞  ≈ 5.5   (high-frequency)
    τ    ≈ 0.1 ns (relaxation time)

Version history:
    v1 (materials.py)            — Non-dispersive ε_r, σ, μ_r
    v2 (materials_dispersive.py) — Adds single-pole Debye relaxation
"""
import numpy as np
from core.materials import MaterialModel


class DispersiveMaterialModel(MaterialModel):
    """
    MaterialModel extended with Debye dispersion parameters.

    Additional Attributes
    ---------------------
    eps_inf : ndarray, shape (Nz, Nx)
        High-frequency permittivity (ε_∞). For non-dispersive cells, equals ε_r.
    eps_static : ndarray, shape (Nz, Nx)
        Static permittivity (ε_s). For non-dispersive cells, equals ε_r.
    tau : ndarray, shape (Nz, Nx)
        Debye relaxation time [s]. For non-dispersive cells, set to infinity.
    """

    def __init__(self, Nz, Nx, eps_r_bg=1.0, sigma_bg=0.0):
        super().__init__(Nz, Nx, eps_r_bg=eps_r_bg, sigma_bg=sigma_bg)
        # Default: non-dispersive (eps_inf = eps_static = eps_r, tau = inf)
        self.eps_inf = self.epsilon_r.copy()
        self.eps_static = self.epsilon_r.copy()
        self.tau = np.full((Nz, Nx), np.inf, dtype=np.float64)

    def set_dispersive_region(self, z_slice, x_slice, eps_inf, eps_static,
                               tau, sigma=0.0):
        """Set Debye dispersive properties in a rectangular region."""
        self.eps_inf[z_slice, x_slice] = eps_inf
        self.eps_static[z_slice, x_slice] = eps_static
        self.tau[z_slice, x_slice] = tau
        self.sigma[z_slice, x_slice] = sigma
        # eps_r stores the static value for geometry/plotting
        self.epsilon_r[z_slice, x_slice] = eps_static

    def get_debye_coefficients(self, dt, eps0):
        """
        Compute ADE (Auxiliary Differential Equation) coefficients for
        the Debye update.

        The polarisation current J_p is updated as:
            J_p^{n+1} = C1 * J_p^n + C2 * E_z^{n+1}

        where:
            C1 = exp(-dt/tau)
            C2 = eps0 * (eps_s - eps_inf) / tau * (1 - exp(-dt/tau))

        The E-field update is modified to include the polarisation:
            E_z^{n+1} = Ca * E_z^n + Cb * (curl_H - J_p^{n+½})

        Returns
        -------
        C1, C2 : ndarray, shape (Nz, Nx)
        is_dispersive : ndarray, shape (Nz, Nx), bool
        """
        is_dispersive = np.isfinite(self.tau) & (self.tau > 0)

        C1 = np.zeros((self.Nz, self.Nx), dtype=np.float64)
        C2 = np.zeros((self.Nz, self.Nx), dtype=np.float64)

        mask = is_dispersive
        tau_safe = np.where(mask, self.tau, 1.0)  # avoid div by zero
        C1[mask] = np.exp(-dt / tau_safe[mask])
        delta_eps = self.eps_static - self.eps_inf
        C2[mask] = (eps0 * delta_eps[mask] / tau_safe[mask]
                    * (1.0 - np.exp(-dt / tau_safe[mask])))

        return C1, C2, is_dispersive

    def get_update_coefficients(self, dt, eps0):
        """
        Compute modified update coefficients for dispersive media.

        In dispersive regions, Ca and Cb use eps_inf (not eps_static)
        because the static contribution is handled by the ADE.
        """
        # Use eps_inf for the instantaneous permittivity
        eps = eps0 * self.eps_inf
        loss = self.sigma * dt / (2.0 * eps)
        Ca = (1.0 - loss) / (1.0 + loss)
        Cb = (dt / eps) / (1.0 + loss)
        return Ca, Cb
