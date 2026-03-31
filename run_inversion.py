"""
Entry point: Full-Waveform Inversion for GPR rebar detection.

Supports two inversion approaches:
    1. 'geometry' (default): Recover rebar positions (x, z, r) — 9 parameters,
       uses finite-difference gradients and L-BFGS-B. Fast and robust.
    2. 'pixel': Pixel-wise eps_r recovery via adjoint-state method — 50K
       parameters, steepest descent or L-BFGS-B. Research-grade.

Usage:
    python run_inversion.py                           # geometry, GPU, 30 iter
    python run_inversion.py --method geometry --iter 30
    python run_inversion.py --method pixel --iter 30 --optimizer lbfgs
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np


def main():
    parser = argparse.ArgumentParser(description='GPR FWI Inversion')
    parser.add_argument('--method', choices=['geometry', 'pixel'],
                        default='geometry',
                        help='Inversion method (default: geometry)')
    parser.add_argument('--iterations', type=int, default=30,
                        help='Max iterations (default: 30)')
    parser.add_argument('--optimizer', choices=['lbfgs', 'steepest_descent'],
                        default='lbfgs',
                        help='Optimizer for pixel method (default: lbfgs)')
    parser.add_argument('--sources', type=int, default=15,
                        help='Number of sources for geometry method (default: 15)')
    parser.add_argument('--no-gpu', action='store_true',
                        help='Disable GPU acceleration')
    args = parser.parse_args()

    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/data", exist_ok=True)

    if args.method == 'geometry':
        from inversion.geometry_inversion import GeometryInversionEngine

        engine = GeometryInversionEngine(
            n_sources=args.sources,
            use_gpu=not args.no_gpu,
        )
        results = engine.run(max_iter=args.iterations)
    else:
        from inversion.inversion_engine import InversionEngine

        engine = InversionEngine()
        results = engine.run(
            max_iter=args.iterations,
            method=args.optimizer,
        )

    # ── Save visualizations ──
    import config as cfg
    from visualization.plot_inversion import (
        plot_inversion_comparison, plot_convergence,
    )
    from visualization.plot_bscan import plot_bscan
    from visualization.plot_signals import plot_signal_comparison

    plot_inversion_comparison(
        results['initial_epsr'],
        results['inverted_epsr'],
        results['true_epsr'],
        save_path='outputs/figures/inversion_comparison.png',
        show=False,
    )
    print("  Saved: outputs/figures/inversion_comparison.png")

    plot_convergence(
        results['misfit_history'],
        save_path='outputs/figures/convergence.png',
        show=False,
    )
    print("  Saved: outputs/figures/convergence.png")

    plot_bscan(results['d_obs'], results['scan_x'], results['time'],
               title='Observed B-scan',
               save_path='outputs/figures/bscan_observed.png', show=False)

    plot_bscan(results['d_syn_final'], results['scan_x'], results['time'],
               title='Inverted B-scan',
               save_path='outputs/figures/bscan_inverted.png', show=False)

    # Residual B-scan
    plot_bscan(results['d_obs'] - results['d_syn_final'],
               results['scan_x'], results['time'],
               title='Residual B-scan',
               save_path='outputs/figures/residual_bscan.png', show=False)

    # Save all data
    save_dict = {
        'initial_epsr': results['initial_epsr'],
        'inverted_epsr': results['inverted_epsr'],
        'true_epsr': results['true_epsr'],
        'misfit_history': results['misfit_history'],
        'nrms_data': results['nrms_data'],
        'nrms_model': results['nrms_model'],
        'elapsed_time': results['elapsed_time'],
    }
    # Include geometry parameters if available (from geometry inversion)
    for key in ('optimal_params', 'true_params', 'initial_params'):
        if key in results:
            save_dict[key] = results[key]
    np.savez('outputs/data/inversion_results.npz', **save_dict)
    print("  Saved: outputs/data/inversion_results.npz")

    print(f"\nResults summary:")
    print(f"  Misfit reduction: {results['misfit_history'][0]/max(results['misfit_history'][-1], 1e-30):.1f}x")
    print(f"  NRMS data error: {results['nrms_data']:.4f}")
    print(f"  NRMS model error: {results['nrms_model']:.4f}")
    print(f"  Runtime: {results['elapsed_time']:.1f}s")


if __name__ == "__main__":
    main()
