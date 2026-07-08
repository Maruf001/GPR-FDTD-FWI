# Experiment 1714: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Artifact Frontier Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1713` validator.

This run mutates the saved run `1712` frontier state one condition at a time
and checks that the validator accepts only the exact source state. It covers
job-table damage, payload identity damage, artifact-count damage, partial
completion promotion, all-job completion removal, materialization promotion,
FDTD execution promotion, downstream promotion, figure damage, and missing
script snapshots.

## Output

```text
outputs/experiments/1714_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:       true
cases:                        17
expected pass cases:          1
expected fail cases:          16
actual pass cases:            1
actual fail cases:            16
unexpected cases:             0
damaged cases:                16
ready for materialization:    false
new FDTD executed:            false
GPU work ready:               false
field transfer ready:         false
field FWI ready:              false
3D/HPC ready:                 false
```

The exact source state passes. All damaged states fail as expected:

```text
source readiness false
job row removed
payload identity damaged
required artifact count damaged
current artifact promoted
current artifact accepted
frontier row removed
current-state scenario removed
partial scenario promoted complete
all-job completion removed
minimum job count damaged
materialization readiness promoted
FDTD execution promoted
GPU readiness promoted
figure dynamic range removed
script snapshots removed
```

## Interpretation

The run `1713` validator is sensitive to the failure modes that matter for the
materialization artifact frontier. It does not accept partial-completion
promotion, job-table drift, artifact promotion, materialization/FDTD promotion,
downstream promotion, or damaged supporting artifacts.

## Decision

Use run `1714` as the sensitivity audit for the run `1712` materialization
frontier.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_artifact_frontier_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
