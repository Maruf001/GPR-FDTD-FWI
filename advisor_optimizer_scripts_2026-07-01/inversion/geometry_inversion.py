"""
Geometry-based inversion for rebar detection.

Instead of inverting for 50K pixel eps_r values, this inverts for the
geometric parameters of the rebars: (x_center, z_center, radius) per rebar.

With only 9 parameters (3 rebars x 3 params), we can use finite-difference
gradients efficiently and converge in ~10-20 L-BFGS-B iterations.

All forward simulations run on GPU for speed.
"""
import numpy as np
import time as timer
from scipy.optimize import minimize
from core.geometry import build_initial_model, model_from_epsilon_r
from core.materials import MaterialModel
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


def build_model_from_params(params, n_rebars=3):
    """
    Build a MaterialModel from geometric rebar parameters.

    Parameters
    ----------
    params : ndarray, shape (n_rebars * 3,)
        [x1, z1, r1, x2, z2, r2, ...] in meters.
    n_rebars : int
        Number of rebars.

    Returns
    -------
    MaterialModel
    """
    model = MaterialModel(cfg.NZ, cfg.NX)
    eps_r = model.epsilon_r
    sigma = model.sigma

    npml = cfg.NPML

    # Air region
    iz_air_bottom = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + npml
    eps_r[:iz_air_bottom, :] = cfg.AIR_EPSR
    sigma[:iz_air_bottom, :] = cfg.AIR_SIGMA

    # Concrete region
    eps_r[iz_air_bottom:, :] = cfg.CONCRETE_EPSR
    sigma[iz_air_bottom:, :] = cfg.CONCRETE_SIGMA

    # Add rebars from parameters
    for k in range(n_rebars):
        x_c = params[3 * k]
        z_c = params[3 * k + 1]
        r = params[3 * k + 2]

        # Convert to grid indices
        ix_c = int(np.round(x_c / cfg.DX)) + npml
        iz_c = int(np.round(z_c / cfg.DZ)) + npml
        r_cells = r / cfg.DX

        # Fill circular rebar
        for iz in range(max(0, int(iz_c - r_cells) - 1),
                        min(cfg.NZ, int(iz_c + r_cells) + 2)):
            for ix in range(max(0, int(ix_c - r_cells) - 1),
                            min(cfg.NX, int(ix_c + r_cells) + 2)):
                dist = np.sqrt((iz - iz_c) ** 2 + (ix - ix_c) ** 2)
                if dist <= r_cells:
                    eps_r[iz, ix] = cfg.REBAR_EPSR
                    sigma[iz, ix] = cfg.REBAR_SIGMA

    model.epsilon_r = eps_r
    model.sigma = sigma
    return model


class GeometryInversionEngine:
    """
    Geometry-based FWI: recover rebar (x, z, r) from GPR data.

    Uses L-BFGS-B with finite-difference gradients. All forward
    simulations run on GPU.
    """

    def __init__(self, n_sources=15, use_gpu=True):
        """
        Parameters
        ----------
        n_sources : int
            Number of scan positions for inversion.
        use_gpu : bool
            Use GPU for forward simulations.
        """
        self.use_gpu = use_gpu and HAS_GPU
        self.n_rebars = cfg.NUM_REBARS

        # Ground truth for reference
        from core.geometry import build_rebar_model
        print("Building ground-truth model...")
        self.true_model = build_rebar_model()

        # Generate observed data from true model
        print("Generating observed data...")
        scanner = Scanner(self.true_model)
        full_positions, full_scan_x = scanner.get_scan_positions(
            scan_step=cfg.INVERSION_SCAN_STEP
        )
        full_result = scanner.run_scan(
            scan_step=cfg.INVERSION_SCAN_STEP, verbose=False
        )
        full_bscan = full_result['bscan']

        # Subsample sources for inversion speed
        n_full = len(full_positions)
        idx = np.linspace(0, n_full - 1, n_sources, dtype=int)
        self.scan_positions = [full_positions[i] for i in idx]
        self.scan_x = full_scan_x[idx]
        self.d_obs = full_bscan[:, idx]
        self.time = full_result['time']
        self.mute = _build_mute_window(cfg.NT, cfg.DT)

        # For final evaluation (all sources)
        self.full_positions = full_positions
        self.full_scan_x = full_scan_x
        self.full_bscan = full_bscan

        self.t_array = generate_time_array(cfg.NT, cfg.DT)
        self.wavelet = ricker_wavelet(self.t_array, cfg.F_CENTER)

        self.eval_count = 0
        print(f"  Using {n_sources} sources, GPU={'ON' if self.use_gpu else 'OFF'}")

    def _run_forward(self, model, src_iz, src_ix, rec_iz, rec_ix):
        """Run a single forward simulation (GPU or CPU)."""
        if self.use_gpu:
            sim = FDTDSimulatorGPU(model, cfg)
            return sim.run(self.wavelet, src_iz, src_ix, rec_iz, rec_ix)
        else:
            from core.fdtd import FDTDSimulator
            sim = FDTDSimulator(model)
            return sim.run(self.wavelet, src_iz, src_ix, rec_iz, rec_ix)

    def objective(self, params):
        """Compute misfit for given rebar parameters."""
        self.eval_count += 1

        model = build_model_from_params(params, self.n_rebars)

        total_misfit = 0.0
        for k, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(
                self.scan_positions):
            result = self._run_forward(model, src_iz, src_ix, rec_iz, rec_ix)
            residual = result['trace'] - self.d_obs[:, k]
            total_misfit += 0.5 * np.sum(residual ** 2)

        total_misfit /= len(self.scan_positions)

        if self.eval_count % 5 == 0 or self.eval_count <= 3:
            print(f"  Eval {self.eval_count}: J = {total_misfit:.6e}")

        return total_misfit

    def run(self, max_iter=30):
        """
        Run geometry-based inversion.

        Returns
        -------
        dict with results for visualization.
        """
        # Initial guess from B-scan analysis (hyperbola apex positions).
        # In practice, an operator reads approximate x-positions from the
        # B-scan hyperbola apexes and estimates depth from arrival times.
        # We offset each parameter ~20% from truth to simulate this.
        x0 = np.array([
            0.160, 0.080, 0.007,   # Rebar 1: x, z, r
            0.240, 0.080, 0.007,   # Rebar 2
            0.340, 0.080, 0.007,   # Rebar 3
        ])

        # True parameters for reference
        true_params = []
        for z_c, x_c in cfg.REBAR_POSITIONS:
            true_params.extend([x_c, z_c, cfg.REBAR_RADIUS])
        true_params = np.array(true_params)

        # Bounds
        x_bounds = (0.05, 0.45)
        z_bounds = (0.05, 0.20)
        r_bounds = (0.003, 0.015)
        bounds = []
        for _ in range(self.n_rebars):
            bounds.extend([x_bounds, z_bounds, r_bounds])

        print(f"\nStarting geometry inversion ({max_iter} iterations)...")
        print(f"  Parameters: {len(x0)} (3 per rebar x {self.n_rebars} rebars)")
        print(f"  Initial guess: {x0}")
        print(f"  True params:   {true_params}")

        t_start = timer.time()
        misfit_history = []

        def callback(xk):
            pass

        def obj_with_history(x):
            J = self.objective(x)
            misfit_history.append(J)
            return J

        result = minimize(
            obj_with_history,
            x0,
            method='Nelder-Mead',
            options={
                'maxiter': max_iter * 20,
                'maxfev': max_iter * 20,
                'xatol': cfg.DX,       # Position tolerance: 1 grid cell
                'fatol': 1e-6,
                'adaptive': True,
                'disp': True,
            },
        )

        t_elapsed = timer.time() - t_start
        optimal_params = result.x

        print(f"\nInversion complete in {t_elapsed:.1f} seconds.")
        print(f"  Function evaluations: {self.eval_count}")
        print(f"  Final misfit: {result.fun:.6e}")
        print(f"\n  Recovered parameters:")
        for k in range(self.n_rebars):
            x_c = optimal_params[3 * k] * 1000
            z_c = optimal_params[3 * k + 1] * 1000
            r = optimal_params[3 * k + 2] * 1000
            x_t = true_params[3 * k] * 1000
            z_t = true_params[3 * k + 1] * 1000
            r_t = true_params[3 * k + 2] * 1000
            print(f"    Rebar {k+1}: x={x_c:.1f}mm (true {x_t:.1f}), "
                  f"z={z_c:.1f}mm (true {z_t:.1f}), "
                  f"r={r:.1f}mm (true {r_t:.1f})")

        # Build final models for visualization
        inverted_model = build_model_from_params(optimal_params, self.n_rebars)
        init_model = build_model_from_params(x0, self.n_rebars)

        # Generate synthetic B-scan from inverted model
        inv_bscan = np.zeros_like(self.full_bscan)
        for k, (src_iz, src_ix, rec_iz, rec_ix) in enumerate(self.full_positions):
            r = self._run_forward(inverted_model, src_iz, src_ix, rec_iz, rec_ix)
            inv_bscan[:, k] = r['trace']

        # Model error
        n = cfg.NPML
        nrms_model = compute_normalized_rms(
            self.true_model.epsilon_r[n:-n, n:-n],
            inverted_model.epsilon_r[n:-n, n:-n],
        )
        nrms_data = compute_normalized_rms(self.full_bscan, inv_bscan)

        print(f"  NRMS model error: {nrms_model:.4f}")
        print(f"  NRMS data error: {nrms_data:.4f}")

        return {
            'initial_epsr': init_model.epsilon_r,
            'inverted_epsr': inverted_model.epsilon_r,
            'true_epsr': self.true_model.epsilon_r,
            'misfit_history': misfit_history,
            'd_obs': self.full_bscan,
            'd_syn_final': inv_bscan,
            'scan_x': self.full_scan_x,
            'time': self.time,
            'nrms_data': nrms_data,
            'nrms_model': nrms_model,
            'elapsed_time': t_elapsed,
            'optimal_params': optimal_params,
            'true_params': true_params,
            'initial_params': x0,
        }
