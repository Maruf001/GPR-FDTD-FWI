# FDTD Wavefield Amplitude Template For Selected Coordinate Runs

Date: 2026-06-11

## Purpose

Create a reusable summary-driven template for true FDTD wavefield-amplitude
animations, then apply it to six coordinate-optimizer runs:

- `1004_coordinate_optimizer_variable_depth_radius_seed3524578_target0_sources8_txrx60_ringdown050_objectives`
- `1006_coordinate_optimizer_variable_depth_radius_seed3524578_target2_sources5_txrx60_ringdown050_objectives`
- `1007_coordinate_optimizer_variable_depth_radius_seed3524578_target1_sources5_txrx60_ringdown050_objectives`
- `1140_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources9_txrx60_ringdown050_objectives`
- `1158_coordinate_optimizer_variable_depth_radius_seed17167680207565_target2_sources9_txrx60_ringdown050_objectives`
- `1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives`

The new script is `run_experiment_fdtd_wavefield_animation.py`. It reads each
run's `multi_rebar_coordinate_optimizer_summary.json`, builds the true rebar
geometry, selects one representative Tx/Rx pair near the target rebar from the
saved scan positions, reconstructs the configured source wavelet including
ringdown, and runs one forward FDTD simulation with sparse Ez snapshots.

Observed-data Gaussian noise is not injected into the wavefield because that
noise is added after forward simulation to B-scans.

## Commands

Example command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_fdtd_wavefield_animation.py \
  --summary outputs/experiments/1140_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources9_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

All six runs were generated with the same default settings:

- backend: `cpu`
- grid step: from summary, 1.0 mm
- model state: `truth`
- frames requested: 42
- actual snapshots/GIF frames: 43
- output GIF: `figures/fdtd_wavefield_amplitude.gif`
- output summary: `data/fdtd_wavefield_amplitude_summary.json`

## Selected Pairs

| run | target | Tx x mm | Rx x mm |
| --- | ---: | ---: | ---: |
| 1004 | 0 | 106 | 166 |
| 1006 | 2 | 346 | 406 |
| 1007 | 1 | 250 | 310 |
| 1140 | 0 | 98 | 158 |
| 1158 | 2 | 298 | 358 |
| 1160 | 1 | 194 | 254 |

## Validation

Each GIF validated as nonblank:

- frame count: 43 for all six.
- image size: 1000 x 600 px for all six.
- maximum dynamic range: 255 for all six.
- peak absolute Ez: `0.013287600952502754`.

Audit files:

- `outputs/visualization_audits/20260611/fdtd_wavefield_amplitude_targets_1004_1006_1007_1140_1158_1160.json`
- `outputs/visualization_audits/20260611/fdtd_wavefield_amplitude_targets_1004_1006_1007_1140_1158_1160.csv`

Focused tests:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_experiment_fdtd_wavefield_animation.py tests/test_wavefield_animation.py
```

Result: `16 passed`.
