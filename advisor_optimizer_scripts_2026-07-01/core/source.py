"""
Source wavelet generation for GPR FDTD simulation.

Implements the Ricker wavelet (Mexican hat), which is the standard
source for GPR simulations. It is the second derivative of a Gaussian
and has zero DC component, making it ideal for wave propagation.
"""
import numpy as np


def ricker_wavelet(t, f_center):
    """
    Generate a Ricker (Mexican hat) wavelet.

    Formula:
        tau = t - t_delay
        w(t) = (1 - 2*(pi*fc*tau)^2) * exp(-(pi*fc*tau)^2)

    The delay t_delay = 1/fc ensures the wavelet amplitude is
    negligible at t=0, preventing numerical artifacts from an
    abrupt start.

    Parameters
    ----------
    t : ndarray
        Time array [s].
    f_center : float
        Center frequency [Hz].

    Returns
    -------
    w : ndarray
        Wavelet amplitude, same shape as t.
    """
    t_delay = 1.0 / f_center
    tau = t - t_delay
    arg = (np.pi * f_center * tau) ** 2
    return (1.0 - 2.0 * arg) * np.exp(-arg)


def ricker_spectrum(f, f_center):
    """
    Analytical amplitude spectrum of the Ricker wavelet.

    Parameters
    ----------
    f : ndarray
        Frequency array [Hz].
    f_center : float
        Center frequency [Hz].

    Returns
    -------
    S : ndarray
        Spectral amplitude.
    """
    u = (f / f_center) ** 2
    return (2.0 / np.sqrt(np.pi)) * u * np.exp(-u)


def generate_time_array(nt, dt):
    """Create time array: t = [0, dt, 2*dt, ..., (nt-1)*dt]."""
    return np.arange(nt) * dt
