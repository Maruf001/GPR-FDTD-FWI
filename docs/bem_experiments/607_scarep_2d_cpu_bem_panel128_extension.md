# BEM Experiment 607: scarep 2D CPU BEM 128-Panel Extension

Date: 2026-06-30

## Purpose

Extend the colleague-provided `scarep` 2D CPU BEM scan validation from the
64-panel endpoint in run `129` to a 128-panel boundary discretization.

Panels are boundary elements around the circular dielectric target. Increasing
the panel count refines the boundary approximation and tests whether the CPU
Galerkin BEM solve keeps converging against the analytic dielectric-cylinder
reference.

This run compares only against the `scarep` analytic dielectric-cylinder
reference. It does not compare against `outputs/experiments`, run 3D FDTD,
launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/607_scarep_2d_cpu_bem_panel128_extension
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_scan_validation_panel_summary.csv
data/scarep_2d_cpu_bem_scan_validation_best_panel_samples.csv
data/scarep_2d_cpu_bem_scan_validation_arrays.npz
data/scarep_2d_cpu_bem_scan_validation_summary.json
data/scarep_2d_cpu_bem_panel128_extension_summary.json
figures/scarep_2d_cpu_bem_scan_validation.png
figures/scarep_2d_cpu_bem_bscan_vs_analytic.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scan positions:                       11
frequencies:                          25
panel values:                         [8, 16, 32, 64, 128]
best panels:                          128
64-panel complex relative L2:          0.0007053747139208214
128-panel complex relative L2:         0.00017926490798156493
complex error reduction 64 to 128:     3.9348175940455676
complex order 64 to 128:               1.9762967584099294
64-panel time-B-scan relative L2:      0.0005202399688500149
128-panel time-B-scan relative L2:     0.00013202484159666165
time-B-scan reduction 64 to 128:       3.9404703126958314
time-B-scan order 64 to 128:           1.9783678320421263
64-panel wall seconds:                 20.652381618972868
128-panel wall seconds:                79.30079158884473
128/64 wall-time ratio:                3.839789185184963
total wall seconds:                    109.05398436589167
panel128 extension ready:              true
compared to project FDTD archive:      false
```

Panel convergence:

| Panels | Complex relative L2 | Time-B-scan relative L2 | Wall seconds |
| ---: | ---: | ---: | ---: |
| 8 | 0.04415449039471055 | 0.032036432437250406 | 0.7366274879314005 |
| 16 | 0.011871573995031992 | 0.008758046125144577 | 1.8869604070205241 |
| 32 | 0.0028625612719971973 | 0.0021161825095859987 | 5.942273576045409 |
| 64 | 0.0007053747139208214 | 0.0005202399688500149 | 20.652381618972868 |
| 128 | 0.00017926490798156493 | 0.00013202484159666165 | 79.30079158884473 |

## Interpretation

The 128-panel endpoint continues the nearly second-order convergence observed
in run `130`. Doubling from 64 to 128 panels reduces both the complex-spectrum
error and reconstructed time-B-scan error by just under `4x`.

The cost also rises sharply: the 128-panel endpoint takes about `3.84x` the
64-panel wall time for this CPU solve. This is still practical for method
validation, but it supports the original motivation for using BEM carefully as
a fast forward-model path rather than blindly increasing resolution.

The scope is unchanged. This is strong 2D method-validation evidence for the
colleague `scarep` CPU BEM implementation, not a direct comparison to the
project FDTD archive and not a 3D finite-rebar result.

## Decision

Use the 128-panel endpoint as the current high-resolution 2D `scarep` CPU BEM
method-validation result. Keep project FDTD comparison, 3D validation, GPU/HPC,
field transfer, and field FWI blocked until a matched setup is used.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_extension.py

4 passed
```

Figure validation:

```text
scarep_2d_cpu_bem_scan_validation.png    1760x1289, dynamic range=255
scarep_2d_cpu_bem_bscan_vs_analytic.png  2139x740, dynamic range=255
```

Script snapshots:

```text
run_scarep_2d_cpu_bem_panel128_extension.py
run_scarep_2d_cpu_bem_scan_validation.py
tests/test_scarep_2d_cpu_bem_panel128_extension.py
```
