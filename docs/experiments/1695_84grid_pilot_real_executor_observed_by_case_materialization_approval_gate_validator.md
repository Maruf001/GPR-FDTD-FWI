# Experiment 1695: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval Gate Validator

Date: 2026-06-30

## Purpose

Validate run `1694` from its saved artifacts.

This run checks that the approval token is absent, all twenty planned
materialization artifacts are absent, materialization is blocked, FDTD execution
is blocked, downstream states are blocked, and figure/script artifacts are
valid.

## Output

```text
outputs/experiments/1695_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validator.png
scripts/
```

## Result

```text
check count:                             5
passed checks:                           5
failed checks:                           0
planned jobs:                            10
future FDTD trace solves:                80
planned artifacts:                       20
approval tokens present:                 0
present artifacts:                       0
accepted artifacts:                      0
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

## Interpretation

The approval gate validates as a planning boundary only. It does not authorize
or imply observed-array materialization, command execution, FDTD execution, GPU
work, field transfer, or 3D/HPC escalation.

## Decision

Use run `1695` as the artifact validator for run `1694`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validator.py

3 passed
```

Figure validation:

```text
2285x842, dynamic range=255
```
