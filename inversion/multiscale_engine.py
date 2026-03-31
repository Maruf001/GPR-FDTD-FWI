"""
Multi-scale frequency continuation for Full-Waveform Inversion.

Standard FWI can get trapped in local minima when high-frequency data
is used from the start. Multi-scale continuation starts the inversion
at low frequencies (smooth, convex misfit landscape) and progressively
increases to higher frequencies (more detail, more local minima).

At each frequency stage:
    1. Generate a new source wavelet at the target frequency
    2. Compute observed data from the true model at this frequency
    3. Run the geometry-based inversion using the previous stage's
       result as the initial guess
    4. Pass the result to the next stage

Version history:
    v1 (multiscale_engine.py) — Multi-scale wrapper for GeometryInversionEngine
"""
import numpy as np
import time as timer
from core.geometry import build_rebar_model
from core.scan import Scanner
from core.source import ricker_wavelet, generate_time_array
from inversion.adjoint import _build_mute_window
from inversion.objective import compute_normalized_rms
import config as cfg

try:
    from gpu.fdtd_gpu import FDTDSimulatorGPU
    HAS_GPU = True
except ImportError:
    HAS_GPU = False


class MultiscaleInversionEngine:
    """
    Multi-scale frequency continuation for geometry-based GPR inversion.

    Runs the inversion at progressively higher frequencies, using the
    result of each stage as the starting point for the next.
    """

    def __init__(self, freq_schedule=None, n_sources=15, use_gpu=True):
        """
        Parameters
        ----------
        freq_schedule : list of float, optional
            Frequencies in Hz, from low to high.
            Default: [0.5 GHz, 1.0 GHz, 1.5 GHz]
        n_sources : int
            Number of scan positions per stage.
        use_gpu : bool
            Use GPU for forward simulations.
        """
        if freq_schedule is None:
            freq_schedule = [0.5e9, 1.0e9, 1.5e9]

        self.freq_schedule = freq_schedule
        self.n_sources = n_sources
        self.use_gpu = use_gpu and HAS_GPU
        self.n_rebars = cfg.NUM_REBARS

        # Build true model (frequency-independent)
        print("Building ground-truth model...")
        self.true_model = build_rebar_model()

        # Get scan positions (same for all frequencies)
        scanner = Scanner(self.true_model)
        full_positions, full_scan_x = scanner.get_scan_positions(
            scan_step=cfg.INVERSION_SCAN_STEP
        )
        n_full = len(full_positions)
        idx = np.linspace(0, n_full - 1, n_sources, dtype=int)
        self.scan_positions = [full_positions[i] for i in idx]
        self.scan_x = full_scan_x[idx]

        # For final evaluation
        self.full_positions = full_positions
        self.full_scan_x = full_scan_x

        print(f"  Frequency schedule: {[f/1e9 for f in freq_schedule]} GHz")
        print(f"  Sources: {n_sources}, GPU={'ON' if self.use_gpu else 'OFF'}")

    def _generate_observed_data(self, freq):
        """Generate observed B-scan from true model at given frequency."""
        t = generate_time_array(cfg.NT, cfg.DT)
        wavelet = ricker_wavelet(t, freq)

        from core.fdtd import FDTDSimulator
        n_scans = len(self.scan_positions)
        d_obs = np.zeros((cfg.NT, n_scans))

        for k, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(self.scan_positions):
            sim = FDTDSimulator(self.true_model)
            result = sim.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)
            d_obs[:, k] = result['trace']

        return d_obs, wavelet

    def _run_forward_gpu(self, model, wavelet, src_iz, src_ix, rec_iz, rec_ix):
        """Run a single forward simulation (GPU or CPU)."""
        if self.use_gpu:
            sim = FDTDSimulatorGPU(model, cfg)
            return sim.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)
        else:
            from core.fdtd import FDTDSimulator
            sim = FDTDSimulator(model)
            return sim.run(wavelet, src_iz, src_ix, rec_iz, rec_ix)

    def _objective_at_freq(self, params, freq, d_obs, wavelet):
        """Compute misfit for given parameters at given frequency."""
        from inversion.geometry_inversion import build_model_from_params

        model = build_model_from_params(params, self.n_rebars)
        total_misfit = 0.0

        for k, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(self.scan_positions):
            result = self._run_forward_gpu(model, wavelet, src_iz, src_ix, rec_iz, rec_ix)
            residual = result['trace'] - d_obs[:, k]
            total_misfit += 0.5 * np.sum(residual ** 2)

        return total_misfit / len(self.scan_positions)

    def run(self, max_iter_per_stage=20):
        """
        Run multi-scale frequency continuation.

        Returns
        -------
        dict with results from the final stage plus stage-by-stage history.
        """
        from scipy.optimize import minimize
        from inversion.geometry_inversion import build_model_from_params

        # Initial guess (same as geometry_inversion.py)
        current_params = np.array([
            0.160, 0.080, 0.007,
            0.240, 0.080, 0.007,
            0.340, 0.080, 0.007,
        ])

        true_params = []
        for z_c, x_c in cfg.REBAR_POSITIONS:
            true_params.extend([x_c, z_c, cfg.REBAR_RADIUS])
        true_params = np.array(true_params)

        # Bounds
        bounds = []
        for _ in range(self.n_rebars):
            bounds.extend([(0.05, 0.45), (0.05, 0.20), (0.003, 0.015)])

        # FD step sizes (same as geometry_inversion)
        fd_eps = np.array([
            3*cfg.DX, 3*cfg.DZ, 0.001,
            3*cfg.DX, 3*cfg.DZ, 0.001,
            3*cfg.DX, 3*cfg.DZ, 0.001,
        ])

        all_misfit_history = []
        stage_results = []
        t_start = timer.time()

        for stage_idx, freq in enumerate(self.freq_schedule):
            print(f"\n{'='*50}")
            print(f"Stage {stage_idx+1}/{len(self.freq_schedule)}: "
                  f"f = {freq/1e9:.1f} GHz")
            print(f"{'='*50}")

            # Generate observed data at this frequency
            print("  Generating observed data...")
            d_obs, wavelet = self._generate_observed_data(freq)

            eval_count = [0]
            stage_history = []

            def objective(p):
                eval_count[0] += 1
                J = self._objective_at_freq(p, freq, d_obs, wavelet)
                stage_history.append(J)
                if eval_count[0] % 10 == 0 or eval_count[0] <= 2:
                    print(f"    Eval {eval_count[0]}: J = {J:.6e}")
                return J

            # Run Nelder-Mead at this frequency
            result = minimize(
                objective, current_params,
                method='Nelder-Mead',
                options={
                    'maxiter': max_iter_per_stage * 20,
                    'maxfev': max_iter_per_stage * 20,
                    'xatol': cfg.DX,
                    'fatol': 1e-6,
                    'adaptive': True,
                },
            )

            current_params = result.x
            all_misfit_history.extend(stage_history)

            # Report stage results
            print(f"\n  Stage {stage_idx+1} complete:")
            print(f"  Evaluations: {eval_count[0]}")
            print(f"  Final misfit: {result.fun:.6e}")
            for k in range(self.n_rebars):
                x_c = current_params[3*k] * 1000
                z_c = current_params[3*k+1] * 1000
                r = current_params[3*k+2] * 1000
                print(f"    Rebar {k+1}: x={x_c:.1f} mm, z={z_c:.1f} mm, r={r:.1f} mm")

            stage_results.append({
                'freq': freq,
                'params': current_params.copy(),
                'misfit': result.fun,
                'n_evals': eval_count[0],
            })

        t_elapsed = timer.time() - t_start

        # Build final models
        init_model_params = np.array([0.160, 0.080, 0.007, 0.240, 0.080, 0.007, 0.340, 0.080, 0.007])
        init_model = build_model_from_params(init_model_params, self.n_rebars)
        inverted_model = build_model_from_params(current_params, self.n_rebars)

        # Final B-scan comparison at target frequency
        t = generate_time_array(cfg.NT, cfg.DT)
        wavelet_final = ricker_wavelet(t, self.freq_schedule[-1])
        scanner_true = Scanner(self.true_model)
        full_result = scanner_true.run_scan(scan_step=cfg.INVERSION_SCAN_STEP, verbose=False)

        inv_bscan = np.zeros_like(full_result['bscan'])
        for k, (siz, six, riz, rix) in enumerate(self.full_positions):
            r = self._run_forward_gpu(inverted_model, wavelet_final, siz, six, riz, rix)
            inv_bscan[:, k] = r['trace']

        n = cfg.NPML
        nrms_model = compute_normalized_rms(
            self.true_model.epsilon_r[n:-n, n:-n],
            inverted_model.epsilon_r[n:-n, n:-n],
        )

        print(f"\n{'='*50}")
        print(f"Multi-scale inversion complete in {t_elapsed:.1f}s")
        print(f"  Total evaluations: {sum(s['n_evals'] for s in stage_results)}")
        print(f"  NRMS model error: {nrms_model:.4f}")

        return {
            'initial_epsr': init_model.epsilon_r,
            'inverted_epsr': inverted_model.epsilon_r,
            'true_epsr': self.true_model.epsilon_r,
            'misfit_history': all_misfit_history,
            'd_obs': full_result['bscan'],
            'd_syn_final': inv_bscan,
            'scan_x': self.full_scan_x,
            'time': full_result['time'],
            'nrms_data': compute_normalized_rms(full_result['bscan'], inv_bscan),
            'nrms_model': nrms_model,
            'elapsed_time': t_elapsed,
            'optimal_params': current_params,
            'true_params': true_params,
            'initial_params': init_model_params,
            'stage_results': stage_results,
        }
