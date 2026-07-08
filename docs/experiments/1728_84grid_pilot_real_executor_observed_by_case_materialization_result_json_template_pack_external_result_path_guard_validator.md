# Experiment 1728: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Result JSON Template-Pack External Result Path Guard Validator

Date: 2026-06-30

## Purpose

Validate run `1727` from saved artifacts.

The validator checks source readiness, the ten-row template guard table, empty
and separated external result paths, blocked materialization/FDTD/downstream
states, and figure/script artifacts.

This run does not materialize observed arrays, execute commands, run FDTD,
start GPU work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1728_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validator.png
scripts/
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
guard rows:                         10
payloads:                            5
cases:                               2
template files exist:               10
output-local templates:             10
external result files exist:         0
computed template/external equals:   0
templates under external root:       0
external paths under external root: 10
templates accepting as result:       0
row FDTD executed count:             0
observed-by-case materialized:   false
result written:                  false
new FDTD executed:               false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
validation ready:                 true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source external-result path guard ready | pass |
| 2 | template guard rows preserve job shape | pass |
| 3 | external result paths remain empty and separated | pass |
| 4 | materialization FDTD and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `1727` validates as an output-local result-template preparation guard. The
external result paths remain empty and separated from generated templates.

## Decision

Use this validator as the artifact guard for run `1727`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_external_result_path_guard_validator.py

6 passed
```

Figure validation:

```text
2285x835, dynamic range=255
```
