# Experiment 1782: 84-Grid External Return Package Live Intake Reconciliation

Date: 2026-07-01

## Purpose

Reconcile the run `1779` 84-grid external-return package templates against the
run `1776` live intake paths.

This run does not create fake cache arrays, does not place template files in
the live external-return area, does not accept external evidence, does not
execute FDTD, and does not materialize observed-by-case data.

## Output

```text
outputs/experiments/1782_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_reconciliation_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_artifact_job_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_stage_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_status_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:             true
source live intake ready:               true
package items:                          21
stages:                                 5
approval templates present:             1
result JSON templates present:          10
cache arrays required:                  10
cache array templates written:          0
live files present:                     0
ready for guarded live intake:          0
accepted external items:                0
artifact jobs:                          10
artifact jobs ready for guarded intake: 0
artifact jobs accepted:                 0
ready for materialization:              false
new FDTD executed:                      false
gpu priority:                           none
```

Current item status:

| Status | Items |
| --- | ---: |
| awaiting real approval token | 1 |
| awaiting real cache array | 10 |
| awaiting real result JSON | 10 |

## Interpretation

The 84-grid external-return package is now connected to the live intake paths.
The output-local approval template and ten result JSON templates exist, but the
ten cache arrays have no fake templates and must come from real FDTD execution.

The live external-return area currently contains no accepted files. No artifact
job has both cache and result files present, and materialization remains
blocked.

## Decision

Use run `1782` as the current 84-grid external-return pre-return checklist.
Keep materialization and FDTD blocked until the real approval token, ten real
cache arrays, and ten real result JSON files pass live intake.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```
