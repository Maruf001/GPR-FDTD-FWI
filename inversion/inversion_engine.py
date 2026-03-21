"""
Full-waveform inversion engine.

Orchestrates the complete inversion workflow:
    1. Generate observed data from ground-truth model
    2. Initialize model (homogeneous concrete, no rebars)
    3. Iterative optimization loop:
        a. Forward simulation with current model -> d_syn
        b. Compute misfit and residual
        c. Adjoint simulation -> gradient
        d. Add TV regularization gradient
        e. Update model via optimizer
        f. Apply bounds
    4. Return results for visualization
"""
import numpy as np
import time as timer
from core.geometry import build_rebar_model, build_initial_model, model_from_epsilon_r
from core.scan import Scanner
from inversion.adjoint import compute_gradient_all_sources
from inversion.regularization import tv_gradient, tv_penalty
from inversion.objective import compute_misfit, compute_normalized_rms
import config as cfg


class InversionEngine:
    """
    Full-waveform inversion for GPR permittivity recovery.
    """

    def __init__(self):
        """Initialize with ground-truth and initial models."""
        print("Building ground-truth model...")
        self.true_model = build_rebar_model()

        print("Building initial model (homogeneous concrete)...")
        self.init_model = build_initial_model()

        # Generate observed data
        print("Generating observed data (B-scan from true model)...")
        scanner = Scanner(self.true_model)
        self.scan_positions, self.scan_x = scanner.get_scan_positions(
            scan_step=cfg.INVERSION_SCAN_STEP
        )
        scan_result = scanner.run_scan(scan_step=cfg.INVERSION_SCAN_STEP)
        self.d_obs = scan_result['bscan']
        self.time = scan_result['time']
        print(f"  Observed data: {self.d_obs.shape} "
              f"({len(self.scan_positions)} sources)")

    def objective_and_gradient(self, eps_r_flat):
        """
        Compute misfit and gradient for the optimizer.

        Parameters
        ----------
        eps_r_flat : ndarray, shape (Nz*Nx,)
            Flattened relative permittivity.

        Returns
        -------
        J : float
            Total misfit (data + regularization).
        grad_flat : ndarray, shape (Nz*Nx,)
            Total gradient.
        """
        # Reshape into 2D model
        eps_r_2d = eps_r_flat.reshape(cfg.NZ, cfg.NX)
        model = model_from_epsilon_r(eps_r_2d)

        # Compute data misfit gradient (adjoint method)
        data_gradient, data_misfit, d_syn = compute_gradient_all_sources(
            model, self.d_obs, self.scan_positions, self.scan_x,
            verbose=False,
        )

        # TV regularization
        tv_grad = tv_gradient(eps_r_2d)
        tv_val = tv_penalty(eps_r_2d)

        # Total objective and gradient
        J = data_misfit + cfg.TV_WEIGHT * tv_val
        gradient = data_gradient + cfg.TV_WEIGHT * tv_grad

        # Mask PML and air regions
        n = cfg.NPML
        gradient[:n, :] = 0.0
        gradient[-n:, :] = 0.0
        gradient[:, :n] = 0.0
        gradient[:, -n:] = 0.0
        iz_air = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
        gradient[:iz_air, :] = 0.0

        return J, gradient.ravel()

    def run(self, max_iter=None, method='steepest_descent'):
        """
        Execute the full inversion.

        Parameters
        ----------
        max_iter : int, optional
            Override cfg.N_ITERATIONS.
        method : str
            'steepest_descent' or 'lbfgs'.

        Returns
        -------
        dict with results for visualization.
        """
        if max_iter is None:
            max_iter = cfg.N_ITERATIONS

        # Initial model as flat vector
        x0 = self.init_model.epsilon_r.ravel().copy()

        print(f"\nStarting inversion ({method}, {max_iter} iterations)...")
        print(f"  Grid: {cfg.NZ} x {cfg.NX} = {cfg.NZ * cfg.NX} parameters")
        print(f"  Sources: {len(self.scan_positions)}")
        t_start = timer.time()

        # Store intermediate models for visualization
        models_history = [x0.copy()]

        def callback(k, x, J=None, grad=None):
            models_history.append(x.copy())

        if method == 'lbfgs':
            from inversion.optimizer import run_lbfgs
            opt_result = run_lbfgs(
                self.objective_and_gradient, x0,
                bounds=cfg.EPSR_BOUNDS,
                max_iter=max_iter,
                callback=lambda k, x: models_history.append(x.copy()),
            )
        else:
            from inversion.optimizer import run_steepest_descent
            opt_result = run_steepest_descent(
                self.objective_and_gradient, x0,
                bounds=cfg.EPSR_BOUNDS,
                max_iter=max_iter,
                callback=callback,
            )

        t_elapsed = timer.time() - t_start
        print(f"\nInversion complete in {t_elapsed:.1f} seconds.")
        print(f"  Iterations: {opt_result['n_iterations']}")
        print(f"  Final misfit: {opt_result['misfit_history'][-1]:.6e}")

        # Get final inverted model
        inverted_epsr = opt_result['x'].reshape(cfg.NZ, cfg.NX)

        # Generate synthetic data from inverted model
        inverted_model = model_from_epsilon_r(inverted_epsr)
        scanner_inv = Scanner(inverted_model)
        inv_result = scanner_inv.run_scan(
            scan_step=cfg.INVERSION_SCAN_STEP, verbose=False
        )
        d_syn_final = inv_result['bscan']

        # Compute error metrics
        n = cfg.NPML
        nrms_data = compute_normalized_rms(self.d_obs, d_syn_final)
        nrms_model = compute_normalized_rms(
            self.true_model.epsilon_r[n:-n, n:-n],
            inverted_epsr[n:-n, n:-n],
        )

        print(f"  NRMS data error: {nrms_data:.4f}")
        print(f"  NRMS model error: {nrms_model:.4f}")

        return {
            'initial_epsr': self.init_model.epsilon_r,
            'inverted_epsr': inverted_epsr,
            'true_epsr': self.true_model.epsilon_r,
            'misfit_history': opt_result['misfit_history'],
            'd_obs': self.d_obs,
            'd_syn_final': d_syn_final,
            'scan_x': self.scan_x,
            'time': self.time,
            'nrms_data': nrms_data,
            'nrms_model': nrms_model,
            'elapsed_time': t_elapsed,
        }
