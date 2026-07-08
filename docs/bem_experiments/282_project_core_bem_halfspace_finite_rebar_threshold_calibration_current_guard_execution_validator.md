# BEM Experiment 282: Half-Space Finite-Rebar Threshold Calibration Current Guard Execution Validator

Date: 2026-06-28

## Purpose

Validate the run `281` current-guard execution smoke from saved artifacts.

This run does not execute commands, ingest real FDTD traces, run a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, run 3D validation, or run field
FWI.

## Output

```text
outputs/bem_experiments/282_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_CURRENT_GUARD_EXECUTION_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                    6
validation checks passed:             6
blocking failures:                    0
current-guard validation ready:       true
current-guard execution smoke ready:  true
future real-pair commands executed:   false
real trace files present:             false
real BEM/FDTD comparison ready:       false
threshold calibration ready:          false
3D validation ready:                  false
inversion-scale half-space ready:     false
field transfer ready:                 false
GPU work ready:                       false
field FWI ready:                      false
```

The saved current-guard execution smoke is internally consistent and matches
the runnable current-guard subset of the first-real-pair command plan.

## Decision

Use runs `281-282` as the consumer-validated current-guard execution smoke.
Sensitivity remains required before treating the smoke as fully guarded.

Real paired BEM/FDTD data remain required before threshold calibration,
agreement claims, 3D validation, inversion-scale claims, field transfer, GPU/HPC
work, or field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_validator.py
6 passed
```

Figure validation:

```text
2717x814, dynamic range=255
```
