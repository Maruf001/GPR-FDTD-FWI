# Experiment 1749: 84-Grid Approval-Token Fillability Audit Validator

Date: 2026-06-30

## Purpose

Validate run `1748`, the approval-token fillability audit for the 84-grid
observed-by-case materialization path.

This is a non-executing validation wrapper around saved run `1748` artifacts.
It does not materialize observed-by-case data, run FDTD, launch GPU work,
transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1749_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
approval-token fields:                     12
actions:                                   3
prefilled context fields:                  8
real approval fields required:             4
approval fields missing:                   4
external approval token present:           0
root authorization items:                  1
materialization ready:                     false
new FDTD executed:                         false
validation ready:                          true
```

The checks cover source readiness, field/action shape, missing approval-field
state, absent external approval token, execution boundary preservation, figure
output, and frozen script snapshots.

## Interpretation

Run `1748` validates as a non-executing root-blocker artifact.

## Decision

Use run `1748` to complete the four approval fields before materialization.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_validation_sensitivity.py
9 passed
```

Figure check:

```text
2357x838, dynamic range=255
```

