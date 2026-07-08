# Experiment 1783: 84-Grid External Return Package Live Intake Reconciliation Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1782` 84-grid external-return package live-intake
reconciliation table from disk.

This run does not create fake cache arrays, does not place template files in
the live external-return area, does not accept external evidence, does not
execute FDTD, and does not materialize observed-by-case data.

## Output

```text
outputs/experiments/1783_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source reconciliation ready:           true
validation checks:                     7
passed validation checks:              7
failed validation checks:              0
package items:                         21
live files present:                    0
accepted external items:               0
artifact jobs:                         10
artifact jobs accepted:                0
ready for materialization:             false
new FDTD executed:                     false
gpu priority:                          none
```

Validation checks:

| Check | Result |
| --- | --- |
| source reconciliation ready | pass |
| twenty-one items and five stages represented | pass |
| approval and result templates are present without cache templates | pass |
| live files remain absent and unaccepted | pass |
| current status split is preserved | pass |
| artifact jobs and materialization remain blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved 84-grid external-return reconciliation table is internally
consistent. It preserves the twenty-one expected external items, five-stage
shape, one approval template, ten result JSON templates, zero cache-array
templates, zero live files, and zero accepted artifact jobs.

The validator confirms that materialization and FDTD execution remain blocked.

## Decision

Use run `1783` as the saved-artifact validator for the run `1782` 84-grid
pre-return reconciliation table.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.py
7 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_package_live_intake_reconciliation_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
