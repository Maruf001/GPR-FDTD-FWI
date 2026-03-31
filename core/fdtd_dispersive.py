"""
2D TMz FDTD simulator with Debye dispersion — extends core/fdtd.py.

Adds an auxiliary polarisation current J_p that implements the Debye
relaxation model in the time domain via Auxiliary Differential Equations
(ADE). The E-field update is modified to include the polarisation
current at each time step.

Non-dispersive cells (tau = inf) behave identically to the base FDTD.

Version history:
    v1 (fdtd.py)           — Non-dispersive FDTD with CPML
    v2 (fdtd_dispersive.py) — Adds single-pole Debye ADE (this file)
"""
import numpy as np
from core.fdtd import FDTDSimulator
from core.materials_dispersive import DispersiveMaterialModel
import config as cfg


class FDTDSimulatorDispersive(FDTDSimulator):
    """
    2D TMz FDTD with Debye dispersion via ADE.

    Inherits from FDTDSimulator and adds the polarisation current update.
    For non-dispersive materials, behaviour is identical to the base class.
    """

    def __init__(self, model):
        """
        Parameters
        ----------
        model : DispersiveMaterialModel
            Must include Debye parameters (eps_inf, eps_static, tau).
        """
        super().__init__(model)

        if not isinstance(model, DispersiveMaterialModel):
            raise TypeError("FDTDSimulatorDispersive requires a DispersiveMaterialModel")

        # Debye ADE coefficients
        self.C1, self.C2, self.is_dispersive = model.get_debye_coefficients(
            cfg.DT, cfg.EPS0
        )

        # Polarisation current array
        self.Jp = np.zeros((model.Nz, model.Nx), dtype=np.float64)

        # Modified update coefficients (use eps_inf, not eps_static)
        self.Ca, self.Cb = model.get_update_coefficients(cfg.DT, cfg.EPS0)

        self.n_dispersive = int(np.sum(self.is_dispersive))

    def reset_fields(self):
        """Zero all fields including polarisation current."""
        super().reset_fields()
        self.Jp[:] = 0.0

    def step(self, source_val, src_iz, src_ix):
        """
        One time step with Debye ADE.

        Order:
            1. Update H from E (same as base)
            2. CPML H corrections (same as base)
            3. Update E from H (modified: subtract Jp)
            4. Update Jp from new E (ADE step)
            5. CPML E corrections (same as base)
            6. Inject source
        """
        # H update (inherited stencil)
        self.Hx[:-1, :] -= (self.Dh[:-1, :] / self.dz) * (
            self.Ez[1:, :] - self.Ez[:-1, :]
        )
        self.Hy[:, :-1] += (self.Dh[:, :-1] / self.dx) * (
            self.Ez[:, 1:] - self.Ez[:, :-1]
        )

        # CPML H corrections
        self.cpml.update_H(self.Ez, self.Hx, self.Hy, self.Dh)

        # E update with polarisation current subtraction
        curl_H = ((self.Hy[1:, 1:] - self.Hy[1:, :-1]) / self.dx
                  - (self.Hx[1:, 1:] - self.Hx[:-1, 1:]) / self.dz)
        self.Ez[1:, 1:] = (
            self.Ca[1:, 1:] * self.Ez[1:, 1:]
            + self.Cb[1:, 1:] * (curl_H - self.Jp[1:, 1:])
        )

        # ADE: update polarisation current Jp
        # J_p^{n+1} = C1 * J_p^n + C2 * E_z^{n+1}
        if self.n_dispersive > 0:
            self.Jp = self.C1 * self.Jp + self.C2 * self.Ez

        # CPML E corrections
        self.cpml.update_E(self.Ez, self.Hx, self.Hy, self.Cb)

        # Source injection
        self.Ez[src_iz, src_ix] += source_val
