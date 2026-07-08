# Experiment 1708: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Synthetic Completion Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `1707`.

This run checks that the validator accepts the exact run `1706` synthetic
completion smoke and rejects damaged states that would hide schema drift,
synthetic-token promotion, external approval promotion, materialization
promotion, FDTD execution, downstream readiness, or artifact damage.

## Output

```text
outputs/experiments/1708_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready: true
cases:                  17
expected pass cases:    1
expected fail cases:    16
actual pass cases:      1
actual fail cases:      16
unexpected outcomes:    0
damaged cases:          16
new FDTD executed:      false
GPU work ready:         false
field transfer ready:   false
field FWI ready:        false
3D/HPC ready:           false
```

The damaged states cover source readiness removal, schema-row removal, schema
count damage, schema-rule failure, synthetic completion-field damage,
synthetic-token write flag removal, synthetic-token identity damage,
synthetic-token external promotion, external token presence or acceptance,
completion readiness promotion, materialization readiness promotion, FDTD
execution, GPU-readiness promotion, figure damage, and script-snapshot damage.

## Interpretation

The synthetic completion smoke validator is sensitive to the failure modes that
matter before observed-by-case materialization. It does not confuse an
output-local synthetic token with a real external approval token.

## Decision

Use runs `1706-1708` as the current closed synthetic approval-token smoke
block. Keep observed-by-case materialization blocked until a real external
approval token passes the approval gate.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
