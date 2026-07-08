# Experiment 1625: 84-Grid Pilot Executor Interface Guard Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1624` validator.

The exact run `1623` executor audit should pass. Source readiness damage, audit
count drift, pilot-scope drift, real-execution promotion, downstream promotion,
figure damage, and script-snapshot damage should fail.

## Output

```text
outputs/experiments/1625_local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     11
expected pass scenarios:                   1
expected failure scenarios:                10
unexpected scenarios:                      0
executor sensitivity ready:                true
exact source artifacts pass:               true
audit scope damage rejected:               true
real execution promotion rejected:         true
downstream promotion rejected:             true
new FDTD executed:                         false
GPU priority:                              none
```

## Decision

Use runs `1623-1625` as the guarded pilot executor-interface block. The next
2D task is a pilot command inventory or a real-execution implementation plan,
not the full 84-row screen.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_executor_interface_guard_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
2825x857, dynamic range=255
```
