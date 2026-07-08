# Experiment 1716: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Work-Split Policy Validator

Date: 2026-06-30

## Purpose

Validate the run `1715` materialization work-split policy from generated
artifacts.

The validator checks the four-stage approval/cache/result/acceptance route, the
21 required-item count, and the blocked materialization/FDTD/downstream
boundary.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1716_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validator.png
scripts/
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
work stages:                         4
external approval token required:    1
planned jobs:                       10
cache-array artifacts:              10
result-JSON artifacts:              10
materialization artifacts:          20
total required items:               21
current present artifacts:           0
current accepted artifacts:          0
partial artifacts promote FDTD:      false
ready for materialization:           false
new FDTD executed:                   false
validation ready:                    true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source materialization work split ready | pass |
| 2 | stage rows match approval cache result acceptance route | pass |
| 3 | approval and artifact counts match | pass |
| 4 | partial artifacts keep materialization and FDTD blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The work-split policy validates as a planning artifact. It preserves the
execution boundary: one external approval token and all 20 materialization
artifacts remain required before FDTD execution can proceed.

## Decision

Use this validator as the artifact guard for run `1715`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2285x838, dynamic range=255
```
