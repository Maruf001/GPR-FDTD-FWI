"""
Utility functions for FDTD simulation.

Provides CFL stability checks, wavelength calculations, and
grid-coordinate conversion helpers.
"""
import numpy as np


def check_cfl(dt, dx, dz, c0):
    """
    Verify the CFL stability condition for 2D FDTD.

    The Courant-Friedrichs-Lewy condition requires:
        dt <= 1 / (c0 * sqrt(1/dx^2 + 1/dz^2))

    Parameters
    ----------
    dt : float
        Time step [s].
    dx, dz : float
        Spatial grid spacings [m].
    c0 : float
        Maximum wave speed in the domain [m/s].

    Returns
    -------
    stable : bool
    courant_number : float
        Actual Courant number (must be <= 1 for stability).
    dt_max : float
        Maximum stable time step.
    """
    dt_max = 1.0 / (c0 * np.sqrt(1.0 / dx**2 + 1.0 / dz**2))
    courant = dt / dt_max
    return courant <= 1.0, courant, dt_max


def wavelength_in_medium(f, eps_r):
    """Compute wavelength in a medium: lambda = c0 / (f * sqrt(eps_r))."""
    from config import C0
    return C0 / (f * np.sqrt(eps_r))


def points_per_wavelength(f, eps_r, dx):
    """Compute the number of grid points per wavelength."""
    lam = wavelength_in_medium(f, eps_r)
    return lam / dx


def pos_to_index(pos, d, npml):
    """
    Convert physical position [m] to grid index including PML offset.

    Parameters
    ----------
    pos : float
        Physical position [m] (0 = start of physical domain).
    d : float
        Grid spacing [m].
    npml : int
        Number of PML cells (offset).

    Returns
    -------
    int
        Grid index.
    """
    return int(np.round(pos / d)) + npml


def index_to_pos(idx, d, npml):
    """Convert grid index to physical position [m]."""
    return (idx - npml) * d
