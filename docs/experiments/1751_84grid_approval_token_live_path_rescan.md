# Experiment 1751: 84-Grid Approval-Token Live-Path Rescan

Date: 2026-06-30

## Purpose

Rescan the locked external approval-token path after run `1748`.

Run `1748` showed that the approval token has eight prefilled context fields
and four real approval fields still blank. This run checks the live external
path itself and separates the root blocker into directory, approval-field, and
token-file requirements.

This is CPU-only filesystem and readiness auditing. It does not create the
external approval token, materialize the 84-grid outputs, run FDTD, launch GPU
work, transfer to field evidence, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1751_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_field_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source fillability ready:              true
approval-token fields:                 12
actions:                               5
prefilled context fields present:      8 / 8
real approval fields present:          0 / 4
real approval fields missing:          4
external approval path count:          1
external parent directory present:     0
external parent directory missing:     1
external approval token present:       0
external approval token nonempty:      0
external approval token accepted:      0
complete actions:                      1
materialization ready:                 false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
3D/HPC ready:                          false
```

## Interpretation

The approval token is blocked at three levels: the external parent directory is
absent, the four real approval fields are blank, and the external token file is
absent.

## Decision

Create the external approval-token directory, complete the four real approval
fields, and copy the real token before any materialization or FDTD execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_live_path_rescan.py
3 passed
```

Figure check:

```text
2608x846, dynamic range=255
```
