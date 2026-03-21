"""
Regularization for full-waveform inversion.

Total Variation (TV) regularization promotes piecewise-constant models,
which is ideal for the concrete/rebar problem where we have exactly
two materials with sharp interfaces.

Smoothed TV functional:
    TV(m) = sum_{i,j} sqrt( (m[i+1,j]-m[i,j])^2 + (m[i,j+1]-m[i,j])^2 + beta^2 )

where beta is a small parameter for differentiability (modified TV).

The gradient of TV involves the discrete divergence of the normalized gradient:
    dTV/dm[i,j] = -div( grad(m) / |grad(m)|_beta )
"""
import numpy as np
import config as cfg


def tv_penalty(model, beta=None):
    """
    Compute smoothed Total Variation penalty.

    Parameters
    ----------
    model : ndarray, shape (Nz, Nx)
        Model parameter array (e.g., eps_r).
    beta : float
        Smoothing parameter.

    Returns
    -------
    float
        TV penalty value.
    """
    if beta is None:
        beta = cfg.TV_BETA

    # Forward differences
    dz = np.diff(model, axis=0)  # shape (Nz-1, Nx)
    dx = np.diff(model, axis=1)  # shape (Nz, Nx-1)

    # Pad to same size for combined magnitude
    dz_pad = np.zeros_like(model)
    dx_pad = np.zeros_like(model)
    dz_pad[:-1, :] = dz
    dx_pad[:, :-1] = dx

    return np.sum(np.sqrt(dz_pad**2 + dx_pad**2 + beta**2))


def tv_gradient(model, beta=None):
    """
    Compute gradient of smoothed TV penalty.

    Uses the discrete divergence of the normalized gradient:
        grad_TV = -div( [dz, dx] / sqrt(dz^2 + dx^2 + beta^2) )

    Parameters
    ----------
    model : ndarray, shape (Nz, Nx)
        Model parameter array.
    beta : float
        Smoothing parameter.

    Returns
    -------
    ndarray, shape (Nz, Nx)
        TV gradient.
    """
    if beta is None:
        beta = cfg.TV_BETA

    Nz, Nx = model.shape

    # Forward differences
    dz = np.zeros_like(model)
    dx = np.zeros_like(model)
    dz[:-1, :] = model[1:, :] - model[:-1, :]
    dx[:, :-1] = model[:, 1:] - model[:, :-1]

    # Magnitude with smoothing
    mag = np.sqrt(dz**2 + dx**2 + beta**2)

    # Normalized gradient components
    nz = dz / mag
    nx_comp = dx / mag

    # Discrete divergence: -div(n) = -(d(nz)/dz + d(nx)/dx)
    # Using backward differences for the divergence
    div = np.zeros_like(model)

    # d(nz)/dz via backward differences
    div[1:-1, :] += nz[1:-1, :] - nz[:-2, :]
    div[0, :] += nz[0, :]
    div[-1, :] -= nz[-2, :]

    # d(nx)/dx via backward differences
    div[:, 1:-1] += nx_comp[:, 1:-1] - nx_comp[:, :-2]
    div[:, 0] += nx_comp[:, 0]
    div[:, -1] -= nx_comp[:, -2]

    return -div
