# Experiment 1786: 84-Grid External Return Staging Plan Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1785` 84-grid external-return staging plan from disk.

This run does not create a real approval token, does not create cache arrays,
does not create result JSON files, does not stage files into the live external
return area, does not execute copy commands, does not materialize observed-by-
case data, and does not execute FDTD.

## Output

```text
outputs/experiments/1786_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:       true
validation checks:               7
passed validation checks:        7
failed validation checks:        0
staging items:                   21
approval token required:         1
cache arrays required:           10
result JSON files required:      10
artifact jobs required:          10
copy commands:                   21
executed commands:               0
ready for materialization:       false
new FDTD executed:               false
gpu priority:                    none
```

Validation checks:

| Check | Result |
| --- | --- |
| source staging plan ready | pass |
| twenty-one items and five stages represented | pass |
| approval cache result and job counts preserved | pass |
| templates are non-stageable and real files absent | pass |
| commands are present but non-executed | pass |
| action groups and materialization remain blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved 84-grid external-return staging plan is internally consistent. It
preserves twenty-one non-executed copy commands, one approval-token
requirement, ten cache-array requirements, ten result-JSON requirements,
non-stageable templates, absent real files, and blocked materialization.

## Decision

Use run `1786` as the saved-artifact validator for the run `1785`
non-executed 2D external-return staging plan.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py
7 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py: pass
run_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
