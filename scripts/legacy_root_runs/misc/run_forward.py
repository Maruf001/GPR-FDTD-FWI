"""
Entry point: Forward FDTD simulation.

Generates:
    1. Ground-truth geometry plot
    2. B-scan radargram
    3. EM wave propagation animation

Usage:
    python run_forward.py
"""
import sys
import os
import numpy as np

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as cfg
from core.geometry import build_rebar_model
from core.scan import Scanner
from core.utils import check_cfl, points_per_wavelength
from visualization.plot_geometry import plot_ground_truth
from visualization.plot_bscan import plot_bscan
from visualization.plot_wavefield import animate_wavefield


def main():
    print("=" * 60)
    print("2D TMz FDTD Forward Simulation — GPR Concrete Scanning")
    print("=" * 60)

    # --- Parameter verification ---
    stable, courant, dt_max = check_cfl(cfg.DT, cfg.DX, cfg.DZ, cfg.C0)
    ppw_concrete = points_per_wavelength(cfg.F_CENTER, cfg.CONCRETE_EPSR, cfg.DX)
    ppw_air = points_per_wavelength(cfg.F_CENTER, cfg.AIR_EPSR, cfg.DX)

    print(f"\nSimulation parameters:")
    print(f"  Grid: {cfg.NZ} x {cfg.NX} cells ({cfg.NZ_INNER} x {cfg.NX_INNER} + PML)")
    print(f"  Grid spacing: dx = dz = {cfg.DX*1000:.1f} mm")
    print(f"  Time step: dt = {cfg.DT*1e12:.3f} ps")
    print(f"  CFL stable: {stable} (Courant = {courant:.3f}, max dt = {dt_max*1e12:.3f} ps)")
    print(f"  Time steps: {cfg.NT} ({cfg.T_MAX*1e9:.1f} ns)")
    print(f"  Center frequency: {cfg.F_CENTER/1e9:.2f} GHz")
    print(f"  Points/wavelength in concrete: {ppw_concrete:.1f}")
    print(f"  Points/wavelength in air: {ppw_air:.1f}")

    # --- Build model ---
    print("\nBuilding ground-truth model...")
    model = build_rebar_model()
    print(f"  Domain: {cfg.DOMAIN_X*1000:.0f} x {cfg.DOMAIN_Z*1000:.0f} mm")
    print(f"  Rebars: {cfg.NUM_REBARS} x {cfg.REBAR_RADIUS*2000:.1f} mm dia "
          f"at {cfg.REBAR_COVER*1000:.0f} mm cover depth")

    # --- Plot geometry ---
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/animations", exist_ok=True)
    os.makedirs("outputs/data", exist_ok=True)

    print("\nPlotting ground-truth geometry...")
    plot_ground_truth(model, save_path="outputs/figures/ground_truth.png", show=False)

    # --- Run B-scan ---
    print(f"\nRunning B-scan ({len(np.arange(cfg.SCAN_START_X, cfg.SCAN_END_X + 1e-10, cfg.SCAN_STEP))} positions)...")
    scanner = Scanner(model)

    # Save animation for the middle scan position
    mid_scan = len(scanner.scan_x) // 2
    result = scanner.run_scan(save_animation_for=mid_scan)

    bscan = result['bscan']
    print(f"  B-scan shape: {bscan.shape}")
    print(f"  Max amplitude: {np.max(np.abs(bscan)):.4e}")

    # Save B-scan data
    np.savez("outputs/data/forward_data.npz",
             bscan=bscan, scan_x=result['scan_x'], time=result['time'])

    # --- Plot B-scan ---
    print("\nPlotting B-scan radargram...")
    plot_bscan(bscan, result['scan_x'], result['time'],
               save_path="outputs/figures/bscan.png", show=False)

    # --- Create animation ---
    if result['snapshots']:
        print(f"\nCreating wave propagation animation "
              f"({len(result['snapshots'])} frames)...")
        animate_wavefield(result['snapshots'],
                          save_path="outputs/animations/wave_propagation.gif",
                          show=False)
    else:
        print("\nNo snapshots captured for animation.")

    print("\n" + "=" * 60)
    print("Forward simulation complete!")
    print("Outputs saved to outputs/figures/ and outputs/animations/")
    print("=" * 60)


if __name__ == "__main__":
    main()
