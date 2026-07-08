# Experiment 1624: 84-Grid Pilot Executor Interface Guard Validator

Date: 2026-06-30

## Purpose

Validate run `1623` from saved artifacts.

The validator checks that the executor script is available, the five pilot rows
pass contract checks, the non-pilot row is rejected, real execution is refused,
and all downstream execution states remain blocked.

## Output

```text
outputs/experiments/1624_local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         4
validation passes:                         4
blocking failures:                         0
pilot executor validation ready:           true
audit cases:                               7
valid pilot contract checks:               5
remaining pilot execution blockers:        2
new FDTD executed:                         false
GPU priority:                              none
```

## Decision

Use this validator as the artifact guard for run `1623`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validator.py
3 passed
```

Figure check:

```text
1925x839, dynamic range=255
```
