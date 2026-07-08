"""
Optimization engine for full-waveform inversion.

Provides steepest descent with Armijo backtracking line search and
L-BFGS-B via scipy. Both methods handle the adjoint gradient's
small magnitude through appropriate scaling strategies.
"""
import numpy as np
from scipy.optimize import minimize
import config as cfg


def run_steepest_descent(objective_and_gradient, x0, bounds,
                          max_iter=30, initial_step=2e-4, callback=None):
    """
    Steepest descent with fixed step size.

    Uses a small, safe step size determined from empirical testing.
    The step size is the max eps_r change per iteration after gradient
    normalization. With ~50K pixels and nonlinear wave physics, usable
    step sizes are O(1e-4) to avoid overshooting.

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
        Step size (max eps_r change per iteration).
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

        grad_max = np.max(np.abs(grad))
        if grad_max < 1e-30:
            print(f"  Iteration {k}: gradient near zero, stopping.")
            break

        # Normalize gradient and step
        direction = grad / grad_max
        x = x - alpha * direction
        x = np.clip(x, bounds[0], bounds[1])

        print(f"  Iteration {k+1}/{max_iter}: J = {J:.6e}, "
              f"max|grad| = {grad_max:.4e}, step = {alpha:.4e}")

    return {'x': x, 'misfit_history': misfit_history,
            'n_iterations': len(misfit_history)}


def run_lbfgs(objective_and_gradient, x0, bounds,
              max_iter=30, callback=None):
    """
    Run L-BFGS-B optimization via scipy.

    The adjoint gradient has small magnitude (~1e-3) relative to the
    parameter scale (eps_r ~ 1-15). We apply a fixed scaling factor computed
    from the first evaluation so L-BFGS-B's initial step is meaningful.
    This fixed factor is applied to ALL evaluations, preserving relative
    gradient changes so L-BFGS-B can build proper curvature estimates.

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
    grad_scale = [None]

    def wrapped_callback(xk):
        iter_count[0] += 1
        if callback:
            callback(iter_count[0], xk)

    n = len(x0)
    scipy_bounds = [(bounds[0], bounds[1])] * n

    def func_and_grad(x):
        J, g = objective_and_gradient(x)

        # On first evaluation, compute a fixed scaling factor.
        grad_max = np.max(np.abs(g))
        if grad_scale[0] is None and grad_max > 0:
            grad_scale[0] = 1.0 / grad_max
            print(f"  Gradient scale factor: {grad_scale[0]:.4e} "
                  f"(raw max|grad| = {grad_max:.4e})")

        if grad_scale[0] is not None:
            g = g * grad_scale[0]

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
            'maxfun': max_iter * 2,
            'ftol': 1e-10,
            'gtol': 1e-6,
            'maxcor': 10,
            'disp': False,
        },
    )

    return {
        'x': result.x,
        'misfit_history': misfit_history,
        'n_iterations': len(misfit_history),
        'scipy_result': result,
    }
