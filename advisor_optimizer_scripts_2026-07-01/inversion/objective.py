"""
Objective (misfit) function for full-waveform inversion.

The least-squares misfit measures the discrepancy between observed
and synthetic GPR data:

    J(m) = (1/2) * sum_{s,t} (d_obs[s,t] - d_syn[s,t])^2

The residual r = d_syn - d_obs is used as the adjoint source
(injected time-reversed at the receiver locations).
"""
import numpy as np


def compute_misfit(d_obs, d_syn):
    """
    Compute L2 misfit.

    J = 0.5 * ||d_obs - d_syn||^2

    Parameters
    ----------
    d_obs : ndarray
        Observed data (from ground-truth simulation).
    d_syn : ndarray
        Synthetic data (from current model simulation).

    Returns
    -------
    float
        Scalar misfit value.
    """
    residual = d_syn - d_obs
    return 0.5 * np.sum(residual ** 2)


def compute_residual(d_obs, d_syn):
    """
    Compute data residual: r = d_syn - d_obs.

    This residual, when time-reversed, becomes the adjoint source.

    Parameters
    ----------
    d_obs, d_syn : ndarray, shape (nt,) or (nt, n_scans)

    Returns
    -------
    ndarray
        Residual, same shape as inputs.
    """
    return d_syn - d_obs


def compute_normalized_rms(d_obs, d_syn):
    """
    Compute normalized RMS error as a quantitative metric.

    NRMS = ||d_obs - d_syn|| / ||d_obs||

    Returns
    -------
    float
        Value between 0 (perfect fit) and >1 (poor fit).
    """
    return np.linalg.norm(d_obs - d_syn) / (np.linalg.norm(d_obs) + 1e-30)


def compute_ssim_map(img1, img2):
    """
    Compute a simple structural similarity index between two 2D arrays.

    Used to compare inverted vs true permittivity models.

    Returns
    -------
    float
        SSIM value between -1 and 1 (1 = identical).
    """
    c1 = 0.01 ** 2
    c2 = 0.03 ** 2

    mu1 = np.mean(img1)
    mu2 = np.mean(img2)
    sig1 = np.std(img1)
    sig2 = np.std(img2)
    sig12 = np.mean((img1 - mu1) * (img2 - mu2))

    ssim = ((2 * mu1 * mu2 + c1) * (2 * sig12 + c2)) / \
           ((mu1**2 + mu2**2 + c1) * (sig1**2 + sig2**2 + c2))
    return ssim
