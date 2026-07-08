# Experiment 1683: 84-Grid Pilot Real-Executor Safe Solver-Array Materialization Validator

Date: 2026-06-30

## Purpose

Validate the run `1682` safe solver-array materialization audit from saved
artifacts.

The audit materialized only the arrays that do not require a new finite
difference time domain solve:

```text
time_values
mute
scan_positions
```

This validator checks that those arrays are present and stable, while the
`observed_by_case` binding remains blocked.

## Output

```text
outputs/experiments/1683_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator.png
scripts/
```

## Result

```text
source audit ready:                  true
validation checks:                   8
failed checks:                       0
payloads:                            5
safe array bindings materialized:    3
remaining array bindings:            1
observed_by_case materialized:       false
solver binding ready:                false
new FDTD executed:                   false
bounded pilot execution ready:        false
gpu work ready:                      false
field transfer ready:                false
field FWI ready:                     false
ready for 3D/HPC:                    false
```

The eight validation checks confirm source readiness, stable `time_values` and
`mute` arrays, scan positions for revised payloads `1;23;46;68;72`, a blocked
`observed_by_case` binding, the three-safe/one-remaining binding count, no FDTD
execution, blocked downstream states, and valid figure/script artifacts.

## Interpretation

The safe materialization step is valid. The real-executor path has moved past
the purely symbolic array-design stage for `time_values`, `mute`, and
`scan_positions`, but it still has no observed data array and no accepted real
FDTD output.

The next implementation boundary is therefore narrow and explicit:

```text
define a bounded observed_by_case producer without allowing uncontrolled pilot
or full-grid execution
```

## Decision

Do not promote the revised five-row pilot to execution yet. Keep FDTD, GPU work,
field transfer, field FWI, and 3D/HPC blocked until the observed-case binding is
designed and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator.py

7 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
