# BEM Experiment 283: Half-Space Finite-Rebar Threshold Calibration Current Guard Execution Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `282` current-guard execution validator.

This run does not execute commands, ingest real FDTD traces, run a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, run 3D validation, or run field
FWI.

## Output

```text
outputs/bem_experiments/283_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_CURRENT_GUARD_EXECUTION_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         31
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        30
observed failure scenarios:        30
unexpected outcomes:               0
sensitivity ready:                 true
execution validation ready:        true
execution smoke ready:             true
future real-pair commands executed:false
real trace files present:          false
real BEM/FDTD comparison ready:    false
threshold calibration ready:       false
3D validation ready:               false
inversion-scale half-space ready:  false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The current-guard execution validator accepts the exact run `281` smoke and
rejects controlled damage to execution rows, source command-plan matching,
summary counts, execution state, and false real/downstream readiness.

## Decision

Use runs `281-283` as the guarded current-guard execution smoke for the
first-real-pair threshold-calibration checklist.

Real paired BEM/FDTD data remain required before threshold calibration,
agreement claims, 3D validation, inversion-scale claims, field transfer, GPU/HPC
work, or field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_sensitivity.py
6 passed
```

Figure validation:

```text
4301x878, dynamic range=255
```
