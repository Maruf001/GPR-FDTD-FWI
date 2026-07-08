# BEM Experiment 025: Project-Core Homogeneous Dielectric Distance-Calibrated Replay

Date: 2026-06-24

## Purpose

Replay the homogeneous dielectric target from run `019` using the dense
distance-aware direct-wave calibration validated in run `024`.

The replay applies:

- direct Tx/Rx offset scaling to the incident/direct component;
- source-cylinder-receiver broken-path scaling to the analytic scattered
  component.

No new FDTD solve is launched.

## Output

```text
outputs/bem_experiments/025_project_core_homogeneous_dielectric_distance_calibrated_replay
```

Key artifacts:

```text
data/homogeneous_dielectric_distance_replay_summary.json
data/homogeneous_dielectric_distance_replay_scan_metrics.csv
data/homogeneous_dielectric_distance_replay_arrays.npz
figures/homogeneous_dielectric_distance_replay_path_lengths.png
figures/homogeneous_dielectric_distance_replay_bscan.png
figures/homogeneous_dielectric_distance_replay_scan_metrics.png
docs/HOMOGENEOUS_DIELECTRIC_DISTANCE_CALIBRATED_REPLAY.md
```

## Result

```text
target run:                         outputs/bem_experiments/019_project_core_homogeneous_dielectric_bridge_adapter
calibration run:                    outputs/bem_experiments/024_project_core_dense_distance_interpolation_validation
broken path range:                  0.22090722034374521 to 0.2613143459487711 m
calibration range:                  0.02 to 0.28 m
direct-offset scattered L2:         1.520128574804845
broken-path scattered L2:           1.4544669770583798
broken-path total L2:               0.43040354025518324
distance-calibrated replay ready:   false
```

## Interpretation

Dense distance-aware direct-wave calibration does not repair the homogeneous
dielectric target-scattered field when applied by a simple
source-target-receiver broken path length. It improves the scattered metric
only slightly and does not make the bridge viable.

The project-core/BEM target mismatch is therefore not explained by direct-wave
path length alone.

## Decision

Do not use broken-path direct-wave scaling as the BEM/project-core correction.
The next useful repair is source formulation work or a true scattered-field
calibration against controlled simple targets, not additional PEC or half-space
complexity.

## Validation

```text
python -m py_compile run_project_core_homogeneous_dielectric_distance_calibrated_replay.py
conda run -n gpr-fdtd-fwi python run_project_core_homogeneous_dielectric_distance_calibrated_replay.py
```

Figure check:

```text
3 PNG figures, nonblank dynamic range, dimensions from 1167x703 to 2590x740
```
