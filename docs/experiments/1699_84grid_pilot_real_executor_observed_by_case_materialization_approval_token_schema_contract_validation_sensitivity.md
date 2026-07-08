# Experiment 1699: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval Token Schema Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1698` validator with controlled damage to the run `1697`
approval-token schema contract.

This run checks that the validator fails when schema shape, placeholder state,
template scope, downstream permission, external-token state, action readiness,
materialization state, FDTD execution, downstream state, figure metadata, or
script snapshots are damaged.

## Output

```text
outputs/experiments/1699_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       15
expected pass cases:                     1
expected fail cases:                     14
actual pass cases:                       1
actual fail cases:                       14
unexpected cases:                        0
damaged cases:                           14
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

Damaged states fail for:

```text
source readiness removal
schema row removal
schema count damage
placeholder count damage
approval-scope damage
downstream-permission damage
external-token presence
external-token acceptance
action-readiness promotion
materialization promotion
FDTD-execution promotion
GPU-readiness promotion
figure damage
missing script snapshots
```

## Interpretation

The schema validator is sensitive to the intended failure modes. It does not
silently accept a token that expands scope, permits downstream work, promotes
execution, or bypasses the external-token boundary.

## Decision

Use runs `1697-1699` as the guarded approval-token schema block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
