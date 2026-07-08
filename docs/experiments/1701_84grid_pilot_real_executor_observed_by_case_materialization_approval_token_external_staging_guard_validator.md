# Experiment 1701: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token External Staging Guard Validator

Date: 2026-06-30

## Purpose

Validate the external approval-token staging guard from run `1700`.

Run `1700` checked that the local approval-token template remained incomplete
and output-local, that the external approval token was absent, and that no
planned materialization artifacts existed. This run verifies that guard with
explicit checks for source readiness, token absence, artifact absence,
execution blocking, and artifact presence.

## Output

```text
outputs/experiments/1701_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validator.png
scripts/
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
local template present:              true
external approval token present:     false
external approval token accepted:    false
materialization artifacts planned:   20
present materialization artifacts:   0
accepted materialization artifacts:  0
ready for materialization:           false
new FDTD executed:                   false
gpu work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The external approval-token staging guard is valid. The branch remains at an
approval boundary, not an execution boundary.

## Decision

Use run `1701` as the validator for run `1700`. Keep observed-by-case
materialization and FDTD execution blocked until a real external approval token
is supplied and the approval gate is rerun.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_external_staging_guard_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
