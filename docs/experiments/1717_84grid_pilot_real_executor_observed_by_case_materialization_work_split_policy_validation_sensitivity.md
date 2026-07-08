# Experiment 1717: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Work-Split Policy Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1716` validator by mutating the run `1715`
materialization work-split policy artifacts.

The sensitivity audit checks that the validator accepts the exact policy and
rejects damaged approval, artifact, dependency, promotion, figure, and
script-snapshot states.

This run does not create materialization artifacts, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1717_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_work_split_policy_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                    19
expected pass cases:       1
expected fail cases:      18
actual pass cases:         1
actual fail cases:        18
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
| stage_removed | fail | fail |
| approval_count_damage | fail | fail |
| cache_count_damage | fail | fail |
| result_count_damage | fail | fail |
| total_item_count_damage | fail | fail |
| approval_dependency_removed | fail | fail |
| execution_dependency_removed | fail | fail |
| materialization_unlock | fail | fail |
| fdtd_unlock | fail | fail |
| all_jobs_gate_removed | fail | fail |
| all_artifacts_gate_removed | fail | fail |
| partial_artifacts_promote_fdtd | fail | fail |
| materialization_ready | fail | fail |
| fdtd_execution | fail | fail |
| downstream_promotion | fail | fail |
| figure_damage | fail | fail |
| script_snapshot_damage | fail | fail |

## Interpretation

The validator is sensitive to the route failures that matter. It rejects
damaged approval-token counts, damaged cache/result artifact counts, missing
approval or execution dependencies, and any attempt to promote materialization,
FDTD execution, GPU work, field transfer, field FWI, or 3D/HPC readiness.

## Decision

Keep observed-by-case materialization and FDTD execution blocked until the real
approval token and all 20 artifacts are accepted.

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
2428x854, dynamic range=255
```
