# Experiment 1753: 84-Grid Approval-Token Live-Path Rescan Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1752` validator.

The validator should accept only the exact run `1751` state and reject false
directory/file presence, false approval-token acceptance, and premature
materialization, FDTD, GPU, field, or 3D/HPC promotion.

## Output

```text
outputs/experiments/1753_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validation_sensitivity_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:       true
sensitivity cases:            18
expected pass cases:          1
expected fail cases:          17
actual pass cases:            1
actual fail cases:            17
unexpected cases:             0
materialization ready:        false
new FDTD executed:            false
GPU work ready:               false
field transfer ready:         false
3D/HPC ready:                 false
```

The exact run `1751` state passes. The seventeen damaged states fail as
expected for source readiness, field/action shape damage, prefilled-field or
approval-missing count damage, false external directory presence, false token
presence, false token nonempty state, false token acceptance, action-completion
promotion, materialization promotion, FDTD execution promotion, GPU promotion,
field-transfer promotion, 3D/HPC promotion, figure damage, and missing script
snapshots.

## Interpretation

The validator is sensitive to the failure modes that would incorrectly unblock
84-grid materialization or FDTD execution.

## Decision

Keep materialization and FDTD execution blocked until the real external
approval token exists and is accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_validation_sensitivity.py
9 passed
```

Figure check:

```text
2753x852, dynamic range=255
```
