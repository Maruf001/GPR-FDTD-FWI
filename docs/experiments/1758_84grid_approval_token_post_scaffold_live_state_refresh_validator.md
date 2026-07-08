# Experiment 1758: 84-Grid Approval-Token Post-Scaffold Live-State Refresh Validator

Date: 2026-06-30

## Purpose

Validate the saved run `1757` post-scaffold live-state refresh.

The validator checks that the directory is now present, the token is absent,
the four real approval fields are still blank, and materialization remains
blocked.

This is CPU-only artifact validation. It does not create an approval token,
materialize the 84-grid packet, run FDTD, launch GPU work, transfer to field
evidence, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1758_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              7
checks passed:                       7
checks failed:                       0
external parent directory present:   1
external approval token present:     0
real approval fields missing:        4
completed actions:                   2
materialization ready:           false
new FDTD executed:               false
```

## Interpretation

The post-scaffold state is valid and intentionally incomplete. The next
required item is the real approval token and its real approval values.

## Decision

Keep materialization and FDTD execution blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validator.py
3 passed
```

Figure check:

```text
2429x861, dynamic range=255
```
