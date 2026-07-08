# Experiment 1719: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Post-Work-Split External Guard Validator

Date: 2026-06-30

## Purpose

Validate the run `1718` post-work-split external guard from generated
artifacts.

The validator checks the 21 external-item rows, confirms that all approval and
materialization artifact paths remain absent, and verifies that materialization,
FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC remain blocked.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1719_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_post_work_split_external_guard_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
external items:                21
external approval-token paths:  1
materialization artifacts:     20
present items:                  0
accepted items:                 0
ready for materialization:      false
new FDTD executed:              false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
validation ready:               true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source external guard ready | pass |
| 2 | external item rows match approval and artifacts | pass |
| 3 | all external items remain absent | pass |
| 4 | materialization and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `1718` validates as the current external materialization guard. The
work-split planning block did not create real external approval, cache-array,
or result-JSON files.

## Decision

Use this validator as the artifact guard for run `1718`.

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
2285x839, dynamic range=255
```
