# BEM Experiment 286: Half-Space Finite-Rebar Threshold Calibration Post-Execution Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `285` post-execution boundary validator.

This run does not execute future real-pair commands, ingest real FDTD traces,
run a real BEM/FDTD comparison, set thresholds, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/286_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_POST_EXECUTION_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         26
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        25
observed failure scenarios:        25
unexpected outcomes:               0
sensitivity ready:                 true
boundary validation ready:         true
source boundary ready:             true
future real-pair commands executed:false
real BEM/FDTD comparison ready:    false
threshold calibration ready:       false
3D validation ready:               false
inversion-scale half-space ready:  false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The post-execution boundary validator accepts the exact run `284` boundary and
rejects controlled damage to rows, counts, guards, and false real/downstream
readiness.

## Decision

Use runs `284-286` as the guarded BEM post-execution boundary. Real paired
BEM/FDTD data remain required before calibration.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_sensitivity.py
5 passed
```

Figure validation:

```text
4121x888, dynamic range=255
```
