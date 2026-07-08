# Experiment 1725: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Result JSON Template-Pack Validator

Date: 2026-06-30

## Purpose

Validate the run `1724` observed-by-case materialization result JSON template
pack from generated artifacts.

The validator checks the ten template rows, five-payload/two-case coverage,
16-field schema shape, blank future solver/hash/runtime values, output-local
placement, absent external result files, blocked FDTD execution, and
figure/script artifacts.

This run does not create cache arrays, execute commands, run FDTD, start GPU
work, transfer to field work, or start 3D/HPC work.

## Output

```text
outputs/experiments/1725_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
templates:                     10
payloads:                       5
cases:                          2
schema fields per template:    16
total schema fields:          160
future-value placeholders:    100
external result files present:  0
observed-by-case materialized: false
result written:                false
new FDTD executed:             false
execution permitted:           false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
validation ready:              true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source result template pack ready | pass |
| 2 | template rows preserve job and schema shape | pass |
| 3 | template payloads keep future values blank | pass |
| 4 | external results and FDTD remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The result JSON templates validate as preparation only. They do not create
external results, materialize observed arrays, execute FDTD, or support
downstream physical claims.

## Decision

Use this validator as the artifact guard for run `1724`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_result_json_template_pack_validator.py

6 passed
```

Figure validation:

```text
2285x832, dynamic range=255
```
