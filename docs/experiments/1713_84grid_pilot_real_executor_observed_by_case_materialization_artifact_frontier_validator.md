# Experiment 1713: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Artifact Frontier Validator

Date: 2026-06-30

## Purpose

Validate run `1712` from saved artifacts.

This run checks the planned job table, the 1024-scenario frontier table, the
all-job-only completion rule, the blocked materialization/FDTD state, and the
figure/script artifacts.

## Output

```text
outputs/experiments/1713_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validator.png
scripts/
```

## Result

```text
checks:                                   5
passed checks:                            5
failed checks:                            0
observed-by-case jobs:                    10
payloads:                                 5
variants:                                 2
required artifacts:                       20
current present artifacts:                0
current accepted artifacts:               0
job-subset scenarios:                     1024
partial scenarios:                        1022
artifact-complete scenarios:              1
partial artifact-complete scenarios:      0
minimum jobs for artifact completion:     10
ready for materialization:                false
new FDTD executed:                        false
GPU work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
3D/HPC ready:                             false
```

The five checks cover source readiness, planned job-table shape, frontier-table
shape, blocked materialization/downstream state, and figure/script artifacts.

## Interpretation

Run `1712` is a valid materialization artifact frontier. The saved artifacts
support the rule that only the all-job case closes the conservative artifact
gate.

## Decision

Use run `1713` as the artifact validator for run `1712`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
