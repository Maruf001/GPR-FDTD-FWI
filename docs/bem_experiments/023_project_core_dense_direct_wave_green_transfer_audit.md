# BEM Experiment 023: Project-Core Dense Direct-Wave Green Transfer Audit

Date: 2026-06-24

## Purpose

Run a denser no-target direct-wave calibration grid after runs `020` and `021`
showed that one source factor does not transfer across Tx/Rx distance.

This run samples Tx/Rx offsets every 10 mm from `0.02 m` to `0.28 m`, with no
target present. It remains a project-core/BEM bridge diagnostic, not a normal
synthetic experiment.

## Output

```text
outputs/bem_experiments/023_project_core_dense_direct_wave_green_transfer_audit
```

Key artifacts:

```text
data/project_core_direct_wave_green_transfer_summary.json
data/project_core_direct_wave_frequency_metrics.csv
data/project_core_direct_wave_offset_metrics.csv
data/project_core_direct_wave_green_transfer_arrays.npz
figures/project_core_direct_wave_geometry.png
figures/project_core_direct_wave_offset_metrics.png
figures/project_core_direct_wave_frequency_metrics.png
docs/PROJECT_CORE_DIRECT_WAVE_GREEN_TRANSFER_AUDIT.md
```

## Result

```text
source count:                            9
Tx/Rx offsets:                           0.02 to 0.28 m, step 0.01 m
pair count:                              243
selected frequency bins:                 17
all-pair direct symmetric L2:            1.6206668574552758
reference-offset transfer symmetric L2:  1.346364319602316
max offset transfer symmetric L2:        1.7781960212651726
max per-offset symmetric L2:             0.4418908733177504
direct-wave transfer ready:              false
```

## Interpretation

The dense grid confirms the same basic result as runs `020` and `021`: a
single source factor calibrated at 20 mm does not transfer across offsets.
However, the measured per-offset fits remain much better, staying below about
`0.45` symmetric L2 across the sampled range.

## Decision

Use this dense grid as the calibration source for an interpolation validation
probe. Do not apply the table to targets until interpolation is validated.

## Validation

```text
conda run -n gpr-fdtd-fwi python run_project_core_direct_wave_green_transfer_audit.py
```

Figure check:

```text
3 PNG figures, nonblank dynamic range, dimensions from 1187x731 to 1816x701
```
