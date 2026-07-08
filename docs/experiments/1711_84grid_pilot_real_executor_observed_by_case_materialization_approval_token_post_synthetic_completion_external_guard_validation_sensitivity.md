# Experiment 1711: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Post-Synthetic Completion External Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1710` validator.

This run mutates the saved run `1709` guard state one condition at a time and
checks that the validator accepts only the exact source state. It covers
synthetic-token placement, external approval promotion, materialization
artifact promotion, FDTD execution promotion, downstream promotion, figure
damage, and missing script snapshots.

## Output

```text
outputs/experiments/1711_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:          true
cases:                           21
expected pass cases:             1
expected fail cases:             20
actual pass cases:               1
actual fail cases:               20
unexpected cases:                0
damaged cases:                   20
new FDTD executed:               false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
```

The exact source state passes. All damaged states fail as expected:

```text
source guard false
source chain false
synthetic token missing
synthetic token hash damaged
synthetic token promoted to external token
synthetic token moved under external root
external token present
external token accepted
completion readiness promoted
artifact row removed
artifact count damaged
cache count damaged
result count damaged
materialization artifact present
materialization artifact accepted
materialization readiness promoted
FDTD execution promoted
GPU readiness promoted
figure dynamic range removed
script snapshots removed
```

## Interpretation

The run `1710` validator is sensitive to the failure modes that matter for this
boundary. It does not silently accept synthetic-token promotion, external-token
promotion, materialization-artifact promotion, execution promotion, or damaged
provenance artifacts.

## Decision

Use run `1711` as the sensitivity audit for the post-synthetic external guard.
Keep observed-by-case materialization, FDTD execution, GPU work, field
transfer, field FWI, and 3D/HPC blocked until a real external approval token
exists and passes the gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_synthetic_completion_external_guard_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
