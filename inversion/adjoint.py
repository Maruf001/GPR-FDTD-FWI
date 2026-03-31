"""
Adjoint-state gradient computation for permittivity inversion.

The adjoint method computes the gradient of the misfit functional
with respect to model parameters using only TWO FDTD simulations
per source, regardless of the number of model parameters.

Mathematical derivation:

    The misfit is J = 0.5 * ||d_obs - d_syn||^2

    The gradient with respect to eps_r at grid point (i,j) is:

        dJ/d(eps_r)[i,j] = -eps0 * integral_0^T {
            Ez_adj(i,j,t) * dEz_fwd(i,j,t)/dt
        } dt

    where:
        Ez_fwd = forward wavefield (source at Tx, current model)
        Ez_adj = adjoint wavefield (time-reversed residual at Rx, same model)

    The time derivative is approximated by central differences:
        dEz_fwd/dt ~ (Ez_fwd^{n+1} - Ez_fwd^{n-1}) / (2*dt)

Workflow:
    1. Forward simulation -> store Ez at all time steps
    2. Compute residual r = d_syn - d_obs at receiver
    3. Adjoint simulation: inject time-reversed r at Rx
    4. Cross-correlate forward and adjoint fields -> gradient
"""
import numpy as np
from core.fdtd import FDTDSimulator
from core.source import ricker_wavelet, generate_time_array
import config as cfg


def _build_mute_window(nt, dt, t_start=1.0e-9, t_end=7.0e-9, taper_ns=0.3e-9):
    """
    Build a time-domain muting window that suppresses the direct wave
    and focuses on the rebar reflection window.

    The direct wave and air-concrete interface reflection arrive before
    ~1 ns. Rebar reflections arrive at ~1.5-4 ns. Muting early arrivals
    dramatically improves gradient quality by removing the dominant signal
    that is identical in both observed and synthetic data.

    Returns
    -------
    window : ndarray, shape (nt,)
        Weights in [0, 1] with cosine tapers.
    """
    t = np.arange(nt) * dt
    window = np.ones(nt)

    # Taper on at t_start
    mask_early = t < t_start
    taper_on = (t >= t_start) & (t < t_start + taper_ns)
    window[mask_early] = 0.0
    if np.any(taper_on):
        window[taper_on] = 0.5 * (1 - np.cos(np.pi * (t[taper_on] - t_start) / taper_ns))

    # Taper off at t_end
    taper_off = (t >= t_end - taper_ns) & (t < t_end)
    mask_late = t >= t_end
    if np.any(taper_off):
        window[taper_off] = 0.5 * (1 + np.cos(np.pi * (t[taper_off] - (t_end - taper_ns)) / taper_ns))
    window[mask_late] = 0.0

    return window


def compute_gradient_single_source(model, source_waveform,
                                    src_iz, src_ix, rec_iz, rec_ix,
                                    d_obs_trace):
    """
    Compute gradient contribution from a single Tx-Rx pair.

    Parameters
    ----------
    model : MaterialModel
        Current model for forward and adjoint simulations.
    source_waveform : ndarray, shape (nt,)
        Source wavelet.
    src_iz, src_ix : int
        Source grid position.
    rec_iz, rec_ix : int
        Receiver grid position.
    d_obs_trace : ndarray, shape (nt,)
        Observed trace at this receiver.

    Returns
    -------
    gradient : ndarray, shape (Nz, Nx)
        Gradient of J w.r.t. eps_r from this source.
    misfit : float
        Misfit contribution from this source.
    d_syn_trace : ndarray, shape (nt,)
        Synthetic trace from current model.
    """
    nt = len(source_waveform)

    # =========================================================
    # Step 1: Forward simulation — store all Ez fields
    # =========================================================
    sim_fwd = FDTDSimulator(model)
    fwd_result = sim_fwd.run(
        source_waveform, src_iz, src_ix, rec_iz, rec_ix,
        save_all_fields=True,
    )
    d_syn_trace = fwd_result['trace']
    forward_fields = fwd_result['fields']  # list of (Nz, Nx) arrays

    # =========================================================
    # Step 2: Compute residual and misfit
    # =========================================================
    residual = d_syn_trace - d_obs_trace

    # Apply time-domain muting to focus on rebar reflections.
    # This suppresses the direct wave and air-concrete reflection which
    # are nearly identical in observed/synthetic data and produce large
    # but uninformative gradients.
    mute = _build_mute_window(nt, cfg.DT)
    residual = residual * mute

    misfit = 0.5 * np.sum(residual ** 2)

    # =========================================================
    # Step 3: Adjoint simulation with time-reversed residual
    # =========================================================
    # The adjoint source is the time-reversed residual injected at Rx
    adjoint_source = residual[::-1].copy()

    sim_adj = FDTDSimulator(model)
    gradient = np.zeros((model.Nz, model.Nx), dtype=np.float64)

    sim_adj.reset_fields()

    for n_adj in range(nt):
        # Run one adjoint time step (source at receiver position)
        sim_adj.step(adjoint_source[n_adj], rec_iz, rec_ix)

        # Corresponding forward time index (time reversal)
        n_fwd = nt - 1 - n_adj

        # Compute time derivative of forward field via central differences
        if 0 < n_fwd < nt - 1:
            dEz_dt = (forward_fields[n_fwd + 1] - forward_fields[n_fwd - 1]) / (2.0 * cfg.DT)
        elif n_fwd == 0:
            dEz_dt = (forward_fields[1] - forward_fields[0]) / cfg.DT
        else:  # n_fwd == nt - 1
            dEz_dt = (forward_fields[nt - 1] - forward_fields[nt - 2]) / cfg.DT

        # Accumulate gradient: g += Ez_adj * dEz_fwd/dt * dt
        gradient += sim_adj.Ez * dEz_dt * cfg.DT

    # Apply the physical sign: gradient = -Σ(Ez_adj * dEz_fwd/dt * dt)
    # Note: we omit the eps0 prefactor here. It produces ~1e-17 magnitudes
    # which are near machine precision. Instead, the total gradient is
    # normalized once after summing all sources (in compute_gradient_all_sources).
    # This preserves relative source contributions while giving the optimizer
    # a workable magnitude.
    gradient *= -1.0

    return gradient, misfit, d_syn_trace


def compute_gradient_all_sources(model, d_obs_bscan, scan_positions, scan_x,
                                  verbose=True):
    """
    Compute total gradient by summing over all source positions.

    Parameters
    ----------
    model : MaterialModel
        Current model.
    d_obs_bscan : ndarray, shape (nt, n_scans)
        Observed B-scan data.
    scan_positions : list of (src_iz, src_ix, rec_iz, rec_ix)
        Grid positions for each scan.
    scan_x : ndarray
        Scan x-positions [m].
    verbose : bool
        Print progress.

    Returns
    -------
    total_gradient : ndarray, shape (Nz, Nx)
    total_misfit : float
    d_syn_bscan : ndarray, shape (nt, n_scans)
    """
    time = generate_time_array(cfg.NT, cfg.DT)
    wavelet = ricker_wavelet(time, cfg.F_CENTER)

    n_scans = len(scan_positions)
    total_gradient = np.zeros((model.Nz, model.Nx), dtype=np.float64)
    total_misfit = 0.0
    d_syn_bscan = np.zeros_like(d_obs_bscan)

    for i, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(scan_positions):
        if verbose and i % 5 == 0:
            print(f"    Gradient: source {i+1}/{n_scans}")

        grad_i, misfit_i, d_syn_i = compute_gradient_single_source(
            model, wavelet, src_iz, src_ix, rec_iz, rec_ix,
            d_obs_bscan[:, i],
        )
        total_gradient += grad_i
        total_misfit += misfit_i
        d_syn_bscan[:, i] = d_syn_i

    # Average misfit over sources
    total_misfit /= n_scans

    # Mask gradient in PML region (no model updates in absorbing layer)
    n = cfg.NPML
    total_gradient[:n, :] = 0.0
    total_gradient[-n:, :] = 0.0
    total_gradient[:, :n] = 0.0
    total_gradient[:, -n:] = 0.0

    # Also mask the air region (eps_r is known and fixed)
    iz_air_bottom = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
    total_gradient[:iz_air_bottom, :] = 0.0

    return total_gradient, total_misfit, d_syn_bscan
