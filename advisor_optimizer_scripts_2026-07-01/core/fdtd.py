"""
2D TMz FDTD Engine.

Solves Maxwell's equations for the TMz polarization (Ez, Hx, Hy)
on a Yee staggered grid using the leapfrog time-stepping scheme.

Array convention: index [iz, ix] where iz=row=depth(z), ix=col=lateral(x).

Field component locations on the Yee grid (physical coordinates):
    Ez[iz, ix]  at position (iz*dz,     ix*dx)       -- integer grid point
    Hx[iz, ix]  at position ((iz+½)*dz, ix*dx)       -- half-step in z (1st index)
    Hy[iz, ix]  at position (iz*dz,     (ix+½)*dx)   -- half-step in x (2nd index)

Maxwell's equations for TMz in the x-z plane:
    dHx/dt = -(1/mu) * dEz/dz      [Hx staggered in z → uses z-derivative of Ez]
    dHy/dt =  (1/mu) * dEz/dx      [Hy staggered in x → uses x-derivative of Ez]
    dEz/dt =  (1/eps) * (dHy/dx - dHx/dz) - (sigma/eps) * Ez

Discretized leapfrog update:
    Hx[iz,ix] -= Dh/dz * (Ez[iz+1,ix] - Ez[iz,ix])     [z-diff → 1st index]
    Hy[iz,ix] += Dh/dx * (Ez[iz,ix+1] - Ez[iz,ix])      [x-diff → 2nd index]
    Ez[iz,ix]  = Ca*Ez + Cb*((Hy[iz,ix]-Hy[iz,ix-1])/dx - (Hx[iz,ix]-Hx[iz-1,ix])/dz)

where Dh = dt/(mu0*mu_r), Ca and Cb incorporate conductivity losses.
"""
import numpy as np
from core.cpml import CPML
import config as cfg


class FDTDSimulator:
    """
    Complete 2D TMz FDTD simulator with CPML absorbing boundaries.
    """

    def __init__(self, model):
        """
        Initialize simulator from a MaterialModel.

        Parameters
        ----------
        model : MaterialModel
            Defines eps_r, sigma, mu_r over the grid.
        """
        self.Nz = model.Nz
        self.Nx = model.Nx
        self.dt = cfg.DT
        self.dx = cfg.DX
        self.dz = cfg.DZ
        self.nt = cfg.NT

        # Compute update coefficients from material properties
        self.Ca, self.Cb = model.get_update_coefficients(cfg.DT, cfg.EPS0)
        self.Dh = model.get_magnetic_coefficient(cfg.DT, cfg.MU0)

        # Initialize field arrays
        self.Ez = np.zeros((self.Nz, self.Nx), dtype=np.float64)
        self.Hx = np.zeros((self.Nz, self.Nx), dtype=np.float64)
        self.Hy = np.zeros((self.Nz, self.Nx), dtype=np.float64)

        # Initialize CPML
        self.cpml = CPML(self.Nz, self.Nx, cfg.NPML,
                         cfg.DT, cfg.DX, cfg.DZ, cfg.EPS0)

    def reset_fields(self):
        """Zero all field arrays and CPML auxiliary fields."""
        self.Ez[:] = 0.0
        self.Hx[:] = 0.0
        self.Hy[:] = 0.0
        self.cpml.reset()

    def update_H(self):
        """
        Update magnetic fields Hx, Hy from Ez (vectorized NumPy).

        Hx[iz,ix] -= Dh/dz * (Ez[iz+1,ix] - Ez[iz,ix])   z-difference (1st index)
        Hy[iz,ix] += Dh/dx * (Ez[iz,ix+1] - Ez[iz,ix])    x-difference (2nd index)
        """
        # Hx update: dEz/dz → first index difference, valid iz in [0, Nz-2]
        self.Hx[:-1, :] -= (self.Dh[:-1, :] / self.dz) * (
            self.Ez[1:, :] - self.Ez[:-1, :]
        )

        # Hy update: dEz/dx → second index difference, valid ix in [0, Nx-2]
        self.Hy[:, :-1] += (self.Dh[:, :-1] / self.dx) * (
            self.Ez[:, 1:] - self.Ez[:, :-1]
        )

    def update_E(self):
        """
        Update electric field Ez from Hx, Hy (vectorized NumPy).

        Ez[iz,ix] = Ca*Ez + Cb*((Hy[iz,ix]-Hy[iz,ix-1])/dx - (Hx[iz,ix]-Hx[iz-1,ix])/dz)
        dHy/dx → x-difference (2nd index);  dHx/dz → z-difference (1st index)
        """
        # Valid for iz in [1, Nz-1] and ix in [1, Nx-1]
        self.Ez[1:, 1:] = (
            self.Ca[1:, 1:] * self.Ez[1:, 1:]
            + self.Cb[1:, 1:] * (
                (self.Hy[1:, 1:] - self.Hy[1:, :-1]) / self.dx   # dHy/dx: 2nd index
                - (self.Hx[1:, 1:] - self.Hx[:-1, 1:]) / self.dz  # dHx/dz: 1st index
            )
        )

    def inject_source(self, src_iz, src_ix, source_val):
        """
        Inject a soft source (additive current) at the specified grid point.

        A soft source adds to the existing field rather than replacing it,
        avoiding artificial reflections from the source point.

        The source represents a z-directed current density Jz:
            Ez += -(dt/eps) * Jz = -Cb * source_val
        """
        self.Ez[src_iz, src_ix] += source_val

    def step(self, source_val, src_iz, src_ix):
        """
        Advance one complete time step.

        Order of operations (leapfrog staggering):
            1. Update H from E (H at n-1/2 -> n+1/2)
            2. Apply CPML corrections to H
            3. Update E from H (E at n -> n+1)
            4. Apply CPML corrections to E
            5. Inject source into Ez
        """
        # 1. H-field update
        self.update_H()

        # 2. CPML H corrections
        self.cpml.update_H(self.Ez, self.Hx, self.Hy, self.Dh)

        # 3. E-field update
        self.update_E()

        # 4. CPML E corrections
        self.cpml.update_E(self.Ez, self.Hx, self.Hy, self.Cb)

        # 5. Source injection
        self.inject_source(src_iz, src_ix, source_val)

    def run(self, source_waveform, src_iz, src_ix, rec_iz, rec_ix,
            save_fields_every=0, save_all_fields=False):
        """
        Run the complete forward simulation.

        Parameters
        ----------
        source_waveform : ndarray, shape (nt,)
            Source amplitude at each time step.
        src_iz, src_ix : int
            Source grid position.
        rec_iz, rec_ix : int
            Receiver grid position.
        save_fields_every : int
            If > 0, save Ez snapshot every N steps (for animation).
        save_all_fields : bool
            If True, save Ez at every time step (for adjoint computation).
            WARNING: memory-intensive for large grids.

        Returns
        -------
        result : dict
            'trace': ndarray (nt,) -- recorded Ez at receiver
            'snapshots': list of (step, Ez_copy) if save_fields_every > 0
            'fields': list of Ez arrays if save_all_fields
        """
        nt = len(source_waveform)
        trace = np.zeros(nt, dtype=np.float64)
        snapshots = []
        fields = []

        self.reset_fields()

        for n in range(nt):
            self.step(source_waveform[n], src_iz, src_ix)

            # Record at receiver. Tuple rec_ix values are linear x-interpolation
            # samples: (left_ix, right_ix, weight_right).
            if isinstance(rec_ix, (tuple, list)):
                rec_ix_left, rec_ix_right, weight_right = rec_ix
                trace[n] = (
                    (1.0 - float(weight_right)) * self.Ez[rec_iz, int(rec_ix_left)]
                    + float(weight_right) * self.Ez[rec_iz, int(rec_ix_right)]
                )
            else:
                trace[n] = self.Ez[rec_iz, rec_ix]

            # Save snapshots for animation
            if save_fields_every > 0 and n % save_fields_every == 0:
                snapshots.append((n, self.Ez.copy()))

            # Save all fields for adjoint
            if save_all_fields:
                fields.append(self.Ez.copy())

        result = {'trace': trace, 'snapshots': snapshots, 'fields': fields}
        return result
