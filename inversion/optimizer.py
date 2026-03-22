"""
Optimization engine for full-waveform inversion.

Wraps scipy.optimize.minimize with L-BFGS-B for bounded optimization
of the relative permittivity field. Also provides a simple steepest
descent implementation as a fallback/reference.
"""
import numpy as np
from scipy.optimize import minimize
import config as cfg


def run_steepest_descent(objective_and_gradient, x0, bounds,
                          max_iter=30, initial_step=0.1, callback=None):
    """
    Steepest descent with fixed normalized step size.

    Each iteration:
        1. Compute gradient (expensive: N_sources forward + adjoint sims)
        2. Step: x -= alpha * grad / max(|grad|)  (normalized direction)
        3. Clip to bounds

    No line search — each iteration costs exactly one gradient evaluation.
    The gradient is already normalized to max=1 by the adjoint module,
    so the step size directly controls the max eps_r change per iteration.

    Parameters
    ----------
    objective_and_gradient : callable
        Takes x (1D array) and returns (J, grad).
    x0 : ndarray
        Initial model (flattened).
    bounds : tuple (lower, upper)
        Bounds on all parameters.
    max_iter : int
        Maximum number of iterations.
    initial_step : float
        Step size (max change in eps_r per iteration).
    callback : callable, optional
        Called with (iteration, x, J, grad) after each step.

    Returns
    -------
    dict with 'x', 'misfit_history', 'n_iterations'
    """
    x = x0.copy()
    misfit_history = []
    alpha = initial_step

    for k in range(max_iter):
        J, grad = objective_and_gradient(x)
        misfit_history.append(J)

        if callback:
            callback(k, x, J, grad)

        grad_norm = np.linalg.norm(grad)
        if grad_norm < 1e-30:
            print(f"  Iteration {k}: gradient near zero, stopping.")
            break

        # Step along negative gradient (gradient already normalized to max=1)
        x = x - alpha * grad
        x = np.clip(x, bounds[0], bounds[1])

        # Reduce step size gradually (cooling schedule)
        if k > 0 and k % 15 == 0:
            alpha *= 0.7

        print(f"  Iteration {k+1}/{max_iter}: J = {J:.6e}, "
              f"|grad| = {grad_norm:.4e}, step = {alpha:.4e}")

    return {'x': x, 'misfit_history': misfit_history,
            'n_iterations': len(misfit_history)}


def run_lbfgs(objective_and_gradient, x0, bounds,
              max_iter=30, callback=None):
    """
    Run L-BFGS-B optimization via scipy.

    Parameters
    ----------
    objective_and_gradient : callable
        Takes x (1D) and returns (J, grad).
    x0 : ndarray
        Initial model (flattened).
    bounds : tuple (lower, upper)
        Parameter bounds.
    max_iter : int
        Maximum iterations.
    callback : callable, optional
        Called after each iteration with current x.

    Returns
    -------
    dict with 'x', 'misfit_history', 'n_iterations'
    """
    misfit_history = []
    iter_count = [0]

    def wrapped_callback(xk):
        iter_count[0] += 1
        if callback:
            callback(iter_count[0], xk)

    # scipy L-BFGS-B expects bounds as list of (low, high) per parameter
    n = len(x0)
    scipy_bounds = [(bounds[0], bounds[1])] * n

    def func_and_grad(x):
        J, g = objective_and_gradient(x)
        misfit_history.append(J)
        print(f"  L-BFGS eval {len(misfit_history)}: J = {J:.6e}")
        return J, g

    result = minimize(
        func_and_grad,
        x0,
        method='L-BFGS-B',
        jac=True,
        bounds=scipy_bounds,
        callback=wrapped_callback,
        options={
            'maxiter': max_iter,
            'maxfun': max_iter * 3,
            'ftol': 1e-15,
            'gtol': 1e-8,
            'disp': False,
        },
    )

    return {
        'x': result.x,
        'misfit_history': misfit_history,
        'n_iterations': len(misfit_history),
        'scipy_result': result,
    }
