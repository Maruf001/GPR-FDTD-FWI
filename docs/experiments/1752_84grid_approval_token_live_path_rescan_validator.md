# Experiment 1752: 84-Grid Approval-Token Live-Path Rescan Validator

Date: 2026-06-30

## Purpose

Validate run `1751` from written artifacts.

The validator checks that the approval-token field/action shape is correct,
that the four real approval fields remain blank, that the external approval
directory and token file are absent, and that materialization/FDTD/downstream
states remain blocked.

## Output

```text
outputs/experiments/1752_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              6
passed checks:                       6
failed checks:                       0
approval-token fields:              12
actions:                            5
real approval fields missing:       4
external parent directory present:  0
external approval token present:    0
complete actions:                   1
materialization ready:              false
new FDTD executed:                  false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

## Interpretation

Run `1751` validates as a missing external directory, missing token file, and
four blank approval fields.

## Decision

Keep materialization and FDTD execution blocked until the real external
approval token is supplied.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validator.py
3 passed
```

Figure check:

```text
2357x836, dynamic range=255
```
