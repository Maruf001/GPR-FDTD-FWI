# Experiment 1687: 84-Grid Pilot Real-Executor Observed-By-Case Preflight Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1686` validator with controlled damage to the run `1685`
observed-data preflight audit artifacts.

This run checks that the validator fails when producer identity, solver-safety
state, blocker state, observed-data state, FDTD state, downstream state, figure
paths, or script snapshots are damaged.

## Output

```text
outputs/experiments/1687_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validation_sensitivity.png
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
observed_by_case materialized:       false
solver binding ready:                false
new FDTD executed:                   false
bounded pilot execution ready:       false
gpu work ready:                      false
field transfer ready:                false
field FWI ready:                     false
ready for 3D/HPC:                    false
```

The exact source state passes. Damaged states fail for:

```text
source readiness removal
producer signature damage
unsafe materialization promotion
blocker removal
blocker readiness promotion
observed_by_case promotion
FDTD execution promotion
downstream GPU promotion
missing figure
missing script snapshots
```

## Interpretation

The observed-data boundary validator is sensitive to the intended failure
modes. It cannot silently treat `observed_by_case` as a safe materialized array
or allow FDTD/downstream promotion from damaged artifacts.

## Decision

Keep `observed_by_case`, FDTD execution, bounded pilot execution, GPU work,
field transfer, field FWI, and 3D/HPC blocked until the preflight blockers are
closed by a separately bounded execution design.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validation_sensitivity.py

3 passed
```

Observed-data boundary slice:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_preflight_gap_audit_validation_sensitivity.py

10 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
