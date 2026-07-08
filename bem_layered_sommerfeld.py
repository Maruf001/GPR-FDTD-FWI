"""Scalar two-layer Sommerfeld-style Green helpers for layered 2D probes."""

from __future__ import annotations

import numpy as np

import config as cfg
from core.source import generate_time_array, ricker_wavelet

EPS0 = 8.8541878128e-12


def gamma_branch(k: complex, kx: np.ndarray) -> np.ndarray:
    gamma = np.sqrt(k * k - kx * kx + 0.0j)
    gamma = np.where(np.imag(gamma) < 0.0, -gamma, gamma)
    gamma = np.where(np.abs(gamma) < 1.0e-12, 1.0e-12 + 0.0j, gamma)
    return gamma


def lower_wavenumber(frequency_hz: float, epsr: float, sigma: float) -> complex:
    omega = 2.0 * np.pi * float(frequency_hz)
    eps_complex = complex(float(epsr), -float(sigma) / (omega * EPS0))
    return complex(omega / cfg.C0) * np.sqrt(eps_complex)


def transmitted_surface(
    *,
    arrays: dict[str, np.ndarray],
    interface_z_m: float = cfg.CONCRETE_TOP,
    lower_epsr: float = cfg.CONCRETE_EPSR,
    lower_sigma: float = cfg.CONCRETE_SIGMA,
    source_z_m: float = cfg.TX_Z,
    kx_sample_count: int = 768,
    kx_span_factor: float = 6.0,
    chunk_size: int = 96,
) -> np.ndarray:
    x_values = arrays["surface_x_m"].astype(float)
    target_x = (arrays["target_ix"].astype(float) - cfg.NPML) * cfg.DX
    target_z = (arrays["target_iz"].astype(float) - cfg.NPML) * cfg.DZ
    selected_frequencies_hz = arrays["selected_frequencies_hz"].astype(float)
    selected_indices = arrays["selected_indices"].astype(int)
    waveform = ricker_wavelet(generate_time_array(cfg.NT, cfg.DT), cfg.F_CENTER)
    source_spec = np.fft.rfft(waveform)[selected_indices]
    dx = target_x[None, :] - x_values[:, None]
    d1 = max(float(interface_z_m) - float(source_z_m), 0.0)
    d2 = np.maximum(target_z - float(interface_z_m), 0.0)
    surface = np.zeros((x_values.size, target_x.size, selected_frequencies_hz.size), dtype=np.complex128)
    for freq_index, frequency_hz in enumerate(selected_frequencies_hz):
        omega = 2.0 * np.pi * float(frequency_hz)
        k1 = complex(omega / cfg.C0)
        k2 = lower_wavenumber(float(frequency_hz), lower_epsr, lower_sigma)
        kx_max = float(kx_span_factor) * max(abs(k1), abs(k2))
        kx = np.linspace(-kx_max, kx_max, int(kx_sample_count))
        dk = float(kx[1] - kx[0])
        weights = np.ones_like(kx)
        weights[0] = 0.5
        weights[-1] = 0.5
        integral = np.zeros((x_values.size, target_x.size), dtype=np.complex128)
        for start in range(0, kx.size, int(chunk_size)):
            stop = min(start + int(chunk_size), kx.size)
            kx_chunk = kx[start:stop]
            gamma1 = gamma_branch(k1, kx_chunk)
            gamma2 = gamma_branch(k2, kx_chunk)
            transmission = 2.0 * gamma1 / (gamma1 + gamma2)
            z_phase = np.exp(1j * gamma1[:, None] * d1 + 1j * gamma2[:, None] * d2[None, :])
            amplitude = (weights[start:stop, None] * transmission[:, None] / gamma1[:, None]) * z_phase
            x_phase = np.exp(1j * kx_chunk[:, None, None] * dx[None, :, :])
            integral += np.sum(x_phase * amplitude[:, None, :], axis=0) * dk
        surface[:, :, freq_index] = source_spec[freq_index] * (1j / (4.0 * np.pi)) * integral
    return surface
