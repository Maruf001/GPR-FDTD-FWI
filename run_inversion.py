"""
Entry point: Adjoint-state full-waveform inversion.

Recovers rebar geometry from simulated GPR data using the
adjoint-state method for gradient computation and L-BFGS-B
optimization with Total Variation regularization.

Usage:
    python run_inversion.py [--iterations N] [--method steepest_descent|lbfgs]
"""
import sys
import os
import argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as cfg
from inversion.inversion_engine import InversionEngine
from inversion.objective import compute_ssim_map
from visualization.plot_inversion import plot_inversion_comparison, plot_convergence
from visualization.plot_signals import plot_signal_comparison, plot_residual_bscan
from visualization.plot_bscan import plot_bscan


def main():
    parser = argparse.ArgumentParser(description='GPR Full-Waveform Inversion')
    parser.add_argument('--iterations', type=int, default=cfg.N_ITERATIONS,
                        help='Number of inversion iterations')
    parser.add_argument('--method', type=str, default='steepest_descent',
                        choices=['steepest_descent', 'lbfgs'],
                        help='Optimization method')
    args = parser.parse_args()

    print("=" * 60)
    print("Adjoint-State Full-Waveform Inversion")
    print("=" * 60)

    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/data", exist_ok=True)

    # --- Run inversion ---
    engine = InversionEngine()
    results = engine.run(max_iter=args.iterations, method=args.method)

    # --- Save results ---
    np.savez("outputs/data/inversion_results.npz",
             initial_epsr=results['initial_epsr'],
             inverted_epsr=results['inverted_epsr'],
             true_epsr=results['true_epsr'],
             misfit_history=results['misfit_history'],
             d_obs=results['d_obs'],
             d_syn_final=results['d_syn_final'])

    # --- Plots ---
    print("\nGenerating plots...")

    # Model comparison
    plot_inversion_comparison(
        results['initial_epsr'],
        results['inverted_epsr'],
        results['true_epsr'],
        save_path="outputs/figures/inversion_comparison.png",
        show=False,
    )

    # Convergence
    plot_convergence(
        results['misfit_history'],
        save_path="outputs/figures/convergence.png",
        show=False,
    )

    # Signal comparison
    plot_signal_comparison(
        results['d_obs'], results['d_syn_final'],
        results['scan_x'], results['time'],
        save_path="outputs/figures/signal_comparison.png",
        show=False,
    )

    # Observed B-scan
    plot_bscan(results['d_obs'], results['scan_x'], results['time'],
               save_path="outputs/figures/bscan_observed.png",
               show=False, title='Observed B-scan (Ground Truth)')

    # Synthetic B-scan from inverted model
    plot_bscan(results['d_syn_final'], results['scan_x'], results['time'],
               save_path="outputs/figures/bscan_inverted.png",
               show=False, title='Synthetic B-scan (Inverted Model)')

    # Residual
    plot_residual_bscan(
        results['d_obs'], results['d_syn_final'],
        results['scan_x'], results['time'],
        save_path="outputs/figures/residual_bscan.png",
        show=False,
    )

    # --- Quantitative metrics ---
    n = cfg.NPML
    ssim = compute_ssim_map(
        results['true_epsr'][n:-n, n:-n],
        results['inverted_epsr'][n:-n, n:-n],
    )

    print("\n" + "=" * 60)
    print("Inversion Results Summary")
    print("=" * 60)
    print(f"  Method: {args.method}")
    print(f"  Iterations: {len(results['misfit_history'])}")
    print(f"  Initial misfit: {results['misfit_history'][0]:.6e}")
    print(f"  Final misfit: {results['misfit_history'][-1]:.6e}")
    print(f"  Misfit reduction: {results['misfit_history'][0]/results['misfit_history'][-1]:.1f}x")
    print(f"  NRMS data error: {results['nrms_data']:.4f}")
    print(f"  NRMS model error: {results['nrms_model']:.4f}")
    print(f"  SSIM (model): {ssim:.4f}")
    print(f"  Elapsed time: {results['elapsed_time']:.1f} s")
    print(f"\nOutputs saved to outputs/figures/")
    print("=" * 60)


if __name__ == "__main__":
    main()
