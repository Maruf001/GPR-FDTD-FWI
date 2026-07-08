# Experiment 1729: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Result JSON Template-Pack External Result Path Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1728` external-result path guard validator.

The sensitivity run mutates the run `1727` artifacts in memory and checks
whether the validator rejects damaged source readiness, guard-row shape,
template output-local state, external-result promotion, path overlap,
template-under-external-root promotion, external-root damage, FDTD/materialized
state promotion, downstream promotion, figure damage, and missing script
snapshots.

This run does not materialize observed arrays, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1729_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                         25
expected pass cases:            1
expected fail cases:           24
actual pass cases:              1
actual fail cases:             24
unexpected outcomes:            0
exact source passes:          true
damaged cases rejected:       true
observed-by-case materialized:false
new FDTD executed:            false
GPU work ready:               false
field transfer ready:         false
field FWI ready:              false
3D/HPC ready:                 false
sensitivity ready:             true
```

## Interpretation

The validator accepts only the exact external-result path guard and rejects
damaged template, external-result, FDTD, downstream, figure, and script states.

## Decision

Keep run `1728` as the validator guard for run `1727`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2572x927, dynamic range=255
```
