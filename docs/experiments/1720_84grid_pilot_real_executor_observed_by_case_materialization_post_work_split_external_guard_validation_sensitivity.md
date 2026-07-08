# Experiment 1720: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Post-Work-Split External Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1719` validator by mutating the run `1718`
post-work-split external guard artifacts.

The sensitivity audit checks that the validator accepts the exact guard and
rejects damaged row shape, false external approval-token presence, false
artifact presence, false artifact acceptance, materialization promotion, FDTD
execution promotion, downstream promotion, figure damage, and missing script
snapshots.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1720_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                    11
expected pass cases:       1
expected fail cases:      10
actual pass cases:         1
actual fail cases:        10
unexpected cases:          0
exact source passes:       true
damaged cases rejected:    true
ready for materialization: false
new FDTD executed:         false
sensitivity ready:         true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact_source | pass | pass |
| source_ready_false | fail | fail |
| guard_row_removed | fail | fail |
| approval_token_present | fail | fail |
| artifact_present | fail | fail |
| item_accepted | fail | fail |
| materialization_ready | fail | fail |
| fdtd_execution | fail | fail |
| downstream_promotion | fail | fail |
| figure_damage | fail | fail |
| script_snapshot_damage | fail | fail |

## Interpretation

The validator rejects false external-file and execution promotions. This keeps
the current 2D materialization state explicit: no real approval token, no cache
arrays, no result JSON files, and no FDTD execution.

## Decision

Keep run `1718` as the current 2D external materialization guard.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2284x843, dynamic range=255
```
