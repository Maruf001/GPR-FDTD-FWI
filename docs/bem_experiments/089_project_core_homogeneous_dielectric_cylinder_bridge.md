# BEM Experiment 089: Project-Core Homogeneous Dielectric-Cylinder Bridge

Date: 2026-06-25

## Purpose

Run the first factorized project-core bridge rung after the run `017` source
normalization failure.

Run `017` showed that direct/background calibration works on the air/concrete
PEC-rebar case, but the calibrated scattered field does not transfer. This run
removes the air/concrete interface and PEC rebar, then compares project-core
FDTD against the analytic 2D dielectric-cylinder reference on a homogeneous
background.

This is CPU-only. It does not run GPU kernels, field FWI, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/bem_experiments/089_project_core_homogeneous_dielectric_cylinder_bridge
```

Key artifacts:

```text
data/project_core_homogeneous_dielectric_cylinder_bridge_summary.json
data/project_core_homogeneous_dielectric_frequency_metrics.csv
data/project_core_homogeneous_dielectric_scan_summary.csv
data/project_core_homogeneous_dielectric_arrays.npz
figures/project_core_homogeneous_dielectric_cylinder_geometry.png
figures/project_core_homogeneous_dielectric_frequency_diagnostics.png
figures/project_core_homogeneous_dielectric_bscan_comparison.png
figures/project_core_homogeneous_dielectric_mid_trace.png
docs/PROJECT_CORE_HOMOGENEOUS_DIELECTRIC_CYLINDER_BRIDGE.md
scripts/run_project_core_homogeneous_dielectric_cylinder_bridge.py
scripts/test_project_core_homogeneous_dielectric_cylinder_bridge.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scan positions:                         7
selected frequency bins:                17
frequency range:                        624772413.7942328 to 2998907586.212318 Hz
cylinder radius:                        0.03 m
exterior epsr:                          1.0
interior epsr:                          4.0
direct/background relative L2:          0.21186906609266937
scattered spectral symmetric L2:        1.5075838091082052
scattered time symmetric L2:            1.5075838091082052
residual best scale |beta|:             0.2303344587056435
residual-scaled scattered time L2:      0.9947715954168446
homogeneous dielectric bridge ready:    false
next half-space rung ready:             false
outputs/experiments promotion ready:    false
GPU work ready:                         false
field transfer ready:                   false
```

## Interpretation

The bridge failure is already present before the half-space interface and PEC
rebar are reintroduced. Direct/background calibration is good enough to be
useful, but the calibrated analytic scattered field does not match project-core
FDTD scattering. A residual scale of about `0.230` would still be needed, and
even residual scaling leaves the scattered time-domain relative L2 near `0.995`.

This means the next correction should target source/field convention, finite
domain behavior, and project-grid scattering representation. It should not
advance to a half-space rung or to the older `outputs/experiments` archive.

## Decision

Keep run `089` as rung 1 of the factorized bridge ladder and do not promote the
project-core FDTD/BEM comparison yet. The next useful branch is another narrow
diagnostic of source injection, finite-domain convention, or grid-aware
scattering, not a new GPU/FWI run.

## Script-Freezing Check

The output folder includes frozen copies of the exact generator and test used
for this result:

```text
scripts/run_project_core_homogeneous_dielectric_cylinder_bridge.py
scripts/test_project_core_homogeneous_dielectric_cylinder_bridge.py
```

The snapshot manifest SHA-256 entries match the frozen files.

## Validation

Focused tests:

```text
tests/test_project_core_homogeneous_dielectric_cylinder_bridge.py
3 passed
```

Figure checks:

```text
project_core_homogeneous_dielectric_bscan_comparison.png        2211x740, dynamic range=255
project_core_homogeneous_dielectric_cylinder_geometry.png       1167x731, dynamic range=255
project_core_homogeneous_dielectric_frequency_diagnostics.png   1852x718, dynamic range=255
project_core_homogeneous_dielectric_mid_trace.png               1184x703, dynamic range=255
```
