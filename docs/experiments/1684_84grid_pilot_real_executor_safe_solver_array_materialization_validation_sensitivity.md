# Experiment 1684: 84-Grid Pilot Real-Executor Safe Solver-Array Materialization Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1683` validator by damaging the saved materialization
state in controlled ways.

This run checks whether the validator fails when the safe-array boundary is
broken, especially when `observed_by_case` or FDTD execution is accidentally
promoted.

## Output

```text
outputs/experiments/1684_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   11
expected pass cases:                 1
expected fail cases:                 10
actual pass cases:                   1
actual fail cases:                   10
unexpected cases:                    0
damaged cases:                       10
new FDTD executed by this run:        false
gpu work ready:                      false
field transfer ready:                false
field FWI ready:                     false
ready for 3D/HPC:                    false
```

The exact source state passes. Damaged cases fail for:

```text
source readiness removal
safe array name damage
safe array length damage
scan-position payload removal
observed_by_case promotion
safe binding-count damage
FDTD execution promotion
GPU/downstream promotion
missing figure
missing script snapshots
```

## Interpretation

The run `1683` validator is sensitive to the intended failure modes. It does not
allow the safe materialization audit to become a real execution claim through
array drift, payload drift, observed-data promotion, FDTD promotion, downstream
promotion, or damaged artifacts.

## Decision

The revised five-row pilot can proceed only to a bounded `observed_by_case`
producer design. It is still not ready for FDTD execution, GPU work, field
transfer, field FWI, or 3D/HPC escalation.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity.py

3 passed
```

Combined safe-array slice:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_validation_sensitivity.py

10 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
