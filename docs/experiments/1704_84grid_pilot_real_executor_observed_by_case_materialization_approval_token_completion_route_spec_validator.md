# Experiment 1704: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Completion Route Spec Validator

Date: 2026-06-30

## Purpose

Validate the approval-token completion route from run `1703`.

Run `1703` identified the four real approval values required before
observed-by-case materialization can proceed. This run verifies the field list,
phase list, current absence state, downstream blocking, and artifacts.

## Output

```text
outputs/experiments/1704_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
completion fields:              4
completed fields:               0
route phases:                   4
ready phases:                   0
external approval token present: false
external approval token accepted: false
ready for materialization:      false
new FDTD executed:              false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

## Interpretation

The approval-token completion route is valid. The branch remains blocked on
explicit approval, not on hidden compute.

## Decision

Use run `1704` as the validator for run `1703`. Keep observed-by-case
materialization and FDTD execution blocked until a completed real approval
token passes the gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_completion_route_spec_validator.py

3 passed
```

Figure validation:

```text
2285x842, dynamic range=255
```
