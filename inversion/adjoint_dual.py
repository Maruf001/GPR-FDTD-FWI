"""
Dual-parameter adjoint gradient: εr and σ simultaneously.

Extends inversion/adjoint.py to compute gradients with respect to both
relative permittivity (εr) and conductivity (σ). The gradient formulas
are derived from the adjoint-state method applied to the lossy wave
equation with both parameters as unknowns.

Gradient formulas:
    g_εr[i,j]  = -ε₀ Σ_t Ez_adj · (∂Ez_fwd/∂t) · Δt      [same as v1]
    g_σ[i,j]   = -Σ_t Ez_adj · Ez_fwd · Δt                  [new]

The σ gradient arises from the loss term σ·Ez in Maxwell's equation.
While εr controls the wave speed, σ controls attenuation. Together they
provide a more complete inversion, but the problem is more ill-posed
(trade-offs between speed and attenuation effects).

Version history:
    v1 (adjoint.py)      — εr gradient only
    v2 (adjoint_dual.py) — εr + σ gradients simultaneously (this file)
"""
import numpy as np
from core.fdtd import FDTDSimulator
from core.source import ricker_wavelet, generate_time_array
from inversion.adjoint import _build_mute_window
import config as cfg


def compute_dual_gradient_single_source(model, source_waveform,
                                         src_iz, src_ix, rec_iz, rec_ix,
                                         d_obs_trace):
    """
    Compute gradients for both εr and σ from a single source.

    Returns
    -------
    grad_epsr : ndarray, shape (Nz, Nx)
    grad_sigma : ndarray, shape (Nz, Nx)
    misfit : float
    d_syn_trace : ndarray, shape (nt,)
    """
    nt = len(source_waveform)

    # Forward simulation — store all Ez fields
    sim_fwd = FDTDSimulator(model)
    fwd_result = sim_fwd.run(
        source_waveform, src_iz, src_ix, rec_iz, rec_ix,
        save_all_fields=True,
    )
    d_syn_trace = fwd_result['trace']
    forward_fields = fwd_result['fields']

    # Residual with muting
    residual = d_syn_trace - d_obs_trace
    mute = _build_mute_window(nt, cfg.DT)
    residual = residual * mute
    misfit = 0.5 * np.sum(residual ** 2)

    # Adjoint simulation
    adjoint_source = residual[::-1].copy()
    sim_adj = FDTDSimulator(model)

    grad_epsr = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    grad_sigma = np.zeros((model.Nz, model.Nx), dtype=np.float64)

    sim_adj.reset_fields()

    for n_adj in range(nt):
        sim_adj.step(adjoint_source[n_adj], rec_iz, rec_ix)
        n_fwd = nt - 1 - n_adj

        # Time derivative of forward Ez (for εr gradient)
        if 0 < n_fwd < nt - 1:
            dEz_dt = (forward_fields[n_fwd + 1] - forward_fields[n_fwd - 1]) / (2.0 * cfg.DT)
        elif n_fwd == 0:
            dEz_dt = (forward_fields[1] - forward_fields[0]) / cfg.DT
        else:
            dEz_dt = (forward_fields[nt - 1] - forward_fields[nt - 2]) / cfg.DT

        Ez_adj = sim_adj.Ez
        Ez_fwd = forward_fields[n_fwd]

        # εr gradient: -Σ Ez_adj · ∂Ez_fwd/∂t · dt
        grad_epsr += Ez_adj * dEz_dt * cfg.DT

        # σ gradient: -Σ Ez_adj · Ez_fwd · dt
        grad_sigma += Ez_adj * Ez_fwd * cfg.DT

    grad_epsr *= -1.0
    grad_sigma *= -1.0

    return grad_epsr, grad_sigma, misfit, d_syn_trace


def compute_dual_gradient_all_sources(model, d_obs_bscan, scan_positions,
                                       scan_x, verbose=True):
    """
    Compute dual gradients (εr and σ) over all sources.

    Returns
    -------
    total_grad_epsr : ndarray, shape (Nz, Nx)
    total_grad_sigma : ndarray, shape (Nz, Nx)
    total_misfit : float
    d_syn_bscan : ndarray, shape (nt, n_scans)
    """
    time = generate_time_array(cfg.NT, cfg.DT)
    wavelet = ricker_wavelet(time, cfg.F_CENTER)

    n_scans = len(scan_positions)
    total_grad_epsr = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    total_grad_sigma = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    total_misfit = 0.0
    d_syn_bscan = np.zeros_like(d_obs_bscan)

    for i, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(scan_positions):
        if verbose and i % 5 == 0:
            print(f"    Dual gradient: source {i+1}/{n_scans}")

        g_eps, g_sig, misfit_i, d_syn_i = compute_dual_gradient_single_source(
            model, wavelet, src_iz, src_ix, rec_iz, rec_ix,
            d_obs_bscan[:, i],
        )
        total_grad_epsr += g_eps
        total_grad_sigma += g_sig
        total_misfit += misfit_i
        d_syn_bscan[:, i] = d_syn_i

    total_misfit /= n_scans

    # Mask PML and air regions
    n = cfg.NPML
    for grad in [total_grad_epsr, total_grad_sigma]:
        grad[:n, :] = 0.0
        grad[-n:, :] = 0.0
        grad[:, :n] = 0.0
        grad[:, -n:] = 0.0
        iz_air = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
        grad[:iz_air, :] = 0.0

    return total_grad_epsr, total_grad_sigma, total_misfit, d_syn_bscan
