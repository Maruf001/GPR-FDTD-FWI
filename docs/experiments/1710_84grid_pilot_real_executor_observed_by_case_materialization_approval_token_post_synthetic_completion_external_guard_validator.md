# Experiment 1710: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Post-Synthetic Completion External Guard Validator

Date: 2026-06-30

## Purpose

Validate run `1709` from saved artifacts.

This run checks that the post-synthetic external guard is internally
consistent: the synthetic token is present but remains outside the approval
path, the real external approval token is absent, and all planned
materialization artifacts remain absent.

## Output

```text
outputs/experiments/1710_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validator.png
scripts/
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
synthetic token present:             true
synthetic token is external token:    false
synthetic token under external root:  false
external approval token present:      false
external approval token accepted:     false
approval token completion ready:      false
materialization artifacts planned:    20
planned cache artifacts:              10
planned result artifacts:             10
present materialization artifacts:    0
accepted materialization artifacts:   0
ready for materialization:            false
new FDTD executed:                    false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

The five checks cover source readiness, upstream chain readiness, synthetic
token placement, absent materialization artifacts with blocked execution, and
valid figure/script artifacts.

## Interpretation

Run `1709` is a valid post-synthetic external guard. The completed synthetic
token remains a local plumbing artifact and does not authorize materialization
or FDTD execution.

## Decision

Use run `1710` as the artifact validator for run `1709`. The next
materialization step remains blocked until a real external approval token is
supplied and the approval gate is rerun.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
