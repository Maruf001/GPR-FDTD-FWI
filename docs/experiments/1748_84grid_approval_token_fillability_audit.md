# Experiment 1748: 84-Grid Approval-Token Fillability Audit

Date: 2026-06-30

## Purpose

Audit the approval token that blocks the 84-grid observed-by-case
materialization path.

Run `1745` identified the approval token as the root blocker. This run expands
the approval-token template into field-level and action-level fillability
tables.

This is a non-executing audit. It does not materialize observed-by-case data,
run FDTD, launch GPU work, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1748_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_field_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_fillability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
approval-token fields:                     12
actions:                                   3
prefilled context fields:                  8
real approval fields required:             4
prefilled context values present:          8
approval values present:                   0
approval values missing:                   4
external approval token present:           0
template accepted as external approval:    0
root authorization items:                  1
root authorization present:                false
materialization ready:                     false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
approval-token audit ready:                true
```

The four missing approval fields are:

```text
approval_id
approval_created_at_utc
approved_by
approval_reason
```

## Interpretation

The approval-token blocker is now concrete. The template already carries eight
context fields, including the planned job count, expected trace solves, scope,
execution mode, and downstream permission flag. The four actual approval fields
are still blank, and the real external approval token is still absent.

## Decision

Complete the four approval fields and copy the real external approval token
before materialization. Keep materialization and FDTD execution blocked now.

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
2536x842, dynamic range=255
```

