# BEM Experiment 019: Project-Core Homogeneous Dielectric Bridge Adapter

Date: 2026-06-24

## Purpose

Run the first factorized project-core bridge diagnostic after the failed
half-space PEC gate in run `017`.

This run removes both the air/concrete interface and PEC rebar rasterization.
The project-core FDTD solver runs a homogeneous background with one dielectric
cylinder, and the comparison reference is the analytic 2D TMz dielectric
cylinder line-source solution.

This is a BEM-track diagnostic. It is not a normal `outputs/experiments`
synthetic run and not a field result.

## Output

```text
outputs/bem_experiments/019_project_core_homogeneous_dielectric_bridge_adapter
```

Key artifacts:

```text
data/project_core_homogeneous_dielectric_summary.json
data/project_core_homogeneous_dielectric_frequency_metrics.csv
data/project_core_homogeneous_dielectric_scan_summary.csv
data/project_core_homogeneous_dielectric_arrays.npz
figures/project_core_homogeneous_dielectric_geometry.png
figures/project_core_homogeneous_dielectric_frequency_diagnostics.png
figures/project_core_homogeneous_dielectric_bscan_comparison.png
figures/project_core_homogeneous_dielectric_mid_trace.png
docs/PROJECT_CORE_HOMOGENEOUS_DIELECTRIC_BRIDGE_ADAPTER.md
```

## Result

```text
scan positions:                         7
selected frequency bins:                17
frequency range:                        624772413.7942328 to 2998907586.212318 Hz
background epsr:                        1.0
cylinder epsr:                          4.0
cylinder radius:                        0.025 m
direct/background relative L2:          0.2109902555403409
total time symmetric L2:                0.3506392905143433
scattered time symmetric L2:            1.5121594456531522
residual best scale |beta|:             0.34312099521761924
homogeneous dielectric bridge ready:    false
```

## Interpretation

The bridge failure is not caused by PEC rasterization or the air/concrete
interface. The homogeneous dielectric case already fails on the isolated
scattered response after direct-wave calibration.

The total field is closer than the scattered field because it is dominated by
the direct wave. The scattered response exposes the calibration mismatch.

## Decision

Do not proceed to homogeneous PEC as the next bridge gate. First isolate the
source/Green-function assumption with a no-target direct-wave transfer audit.

## Validation

```text
python -m py_compile run_project_core_homogeneous_dielectric_bridge_adapter.py
conda run -n gpr-fdtd-fwi python run_project_core_homogeneous_dielectric_bridge_adapter.py
```

Figure check:

```text
4 PNG figures, nonblank dynamic range, dimensions from 1167x731 to 2176x740
```
