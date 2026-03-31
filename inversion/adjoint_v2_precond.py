"""
Adjoint-state gradient with pseudo-Hessian preconditioning — Version 2.

Extends inversion/adjoint.py (v1) by computing the diagonal of the
approximate Hessian (source-illumination term) and using it to
precondition the gradient. This equalises parameter sensitivity
across the domain, enabling larger step sizes and faster convergence.

The pseudo-Hessian diagonal is:

    H_diag[i,j] = sum_t (dEz_fwd/dt)^2 * dt

This approximates how well each grid cell is "illuminated" by the source.
Cells with high illumination have large H_diag and thus smaller
preconditioned gradients — preventing over-correction in well-lit areas
while boosting updates in poorly-lit areas.

Version history:
    v1 (adjoint.py)           — Raw gradient, no preconditioning
    v2 (adjoint_v2_precond.py) — Pseudo-Hessian preconditioned gradient
"""
import numpy as np
from core.fdtd import FDTDSimulator
from core.source import ricker_wavelet, generate_time_array
from inversion.adjoint import _build_mute_window
import config as cfg


def compute_gradient_single_source_precond(model, source_waveform,
                                            src_iz, src_ix, rec_iz, rec_ix,
                                            d_obs_trace):
    """
    Compute preconditioned gradient from a single Tx-Rx pair.

    Same workflow as adjoint.compute_gradient_single_source, but also
    computes the pseudo-Hessian diagonal for preconditioning.

    Returns
    -------
    gradient : ndarray, shape (Nz, Nx)
        Preconditioned gradient.
    hessian_diag : ndarray, shape (Nz, Nx)
        Diagonal of the approximate Hessian (source illumination).
    misfit : float
    d_syn_trace : ndarray, shape (nt,)
    """
    nt = len(source_waveform)

    # Step 1: Forward simulation — store all Ez fields
    sim_fwd = FDTDSimulator(model)
    fwd_result = sim_fwd.run(
        source_waveform, src_iz, src_ix, rec_iz, rec_ix,
        save_all_fields=True,
    )
    d_syn_trace = fwd_result['trace']
    forward_fields = fwd_result['fields']

    # Step 2: Compute residual and misfit (with muting)
    residual = d_syn_trace - d_obs_trace
    mute = _build_mute_window(nt, cfg.DT)
    residual = residual * mute
    misfit = 0.5 * np.sum(residual ** 2)

    # Step 3: Adjoint simulation + gradient + Hessian diagonal
    adjoint_source = residual[::-1].copy()
    sim_adj = FDTDSimulator(model)
    gradient = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    hessian_diag = np.zeros((model.Nz, model.Nx), dtype=np.float64)

    sim_adj.reset_fields()

    for n_adj in range(nt):
        sim_adj.step(adjoint_source[n_adj], rec_iz, rec_ix)

        n_fwd = nt - 1 - n_adj

        # Time derivative of forward field
        if 0 < n_fwd < nt - 1:
            dEz_dt = (forward_fields[n_fwd + 1] - forward_fields[n_fwd - 1]) / (2.0 * cfg.DT)
        elif n_fwd == 0:
            dEz_dt = (forward_fields[1] - forward_fields[0]) / cfg.DT
        else:
            dEz_dt = (forward_fields[nt - 1] - forward_fields[nt - 2]) / cfg.DT

        # Gradient cross-correlation
        gradient += sim_adj.Ez * dEz_dt * cfg.DT

        # Pseudo-Hessian diagonal: source illumination
        hessian_diag += dEz_dt ** 2 * cfg.DT

    gradient *= -1.0

    return gradient, hessian_diag, misfit, d_syn_trace


def compute_gradient_all_sources_precond(model, d_obs_bscan, scan_positions,
                                          scan_x, verbose=True):
    """
    Compute preconditioned total gradient over all sources.

    The gradient at each pixel is divided by the accumulated
    pseudo-Hessian diagonal (source illumination), which normalises
    sensitivity across the domain.

    Returns
    -------
    precond_gradient : ndarray, shape (Nz, Nx)
    total_misfit : float
    d_syn_bscan : ndarray, shape (nt, n_scans)
    """
    time = generate_time_array(cfg.NT, cfg.DT)
    wavelet = ricker_wavelet(time, cfg.F_CENTER)

    n_scans = len(scan_positions)
    total_gradient = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    total_hessian = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    total_misfit = 0.0
    d_syn_bscan = np.zeros_like(d_obs_bscan)

    for i, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(scan_positions):
        if verbose and i % 5 == 0:
            print(f"    Gradient: source {i+1}/{n_scans}")

        grad_i, hess_i, misfit_i, d_syn_i = compute_gradient_single_source_precond(
            model, wavelet, src_iz, src_ix, rec_iz, rec_ix,
            d_obs_bscan[:, i],
        )
        total_gradient += grad_i
        total_hessian += hess_i
        total_misfit += misfit_i
        d_syn_bscan[:, i] = d_syn_i

    total_misfit /= n_scans

    # Mask PML and air regions
    n = cfg.NPML
    total_gradient[:n, :] = 0.0
    total_gradient[-n:, :] = 0.0
    total_gradient[:, :n] = 0.0
    total_gradient[:, -n:] = 0.0
    iz_air = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
    total_gradient[:iz_air, :] = 0.0

    total_hessian[:n, :] = 1.0   # Avoid division by zero in masked regions
    total_hessian[-n:, :] = 1.0
    total_hessian[:, :n] = 1.0
    total_hessian[:, -n:] = 1.0
    total_hessian[:iz_air, :] = 1.0

    # Apply preconditioning: divide gradient by Hessian diagonal
    # Add small epsilon to prevent division by zero
    eps = 1e-10 * np.max(total_hessian)
    precond_gradient = total_gradient / (total_hessian + eps)

    return precond_gradient, total_misfit, d_syn_bscan
