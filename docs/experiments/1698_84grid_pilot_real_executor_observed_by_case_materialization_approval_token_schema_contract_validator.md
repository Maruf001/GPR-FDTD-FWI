# Experiment 1698: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval Token Schema Contract Validator

Date: 2026-06-30

## Purpose

Validate run `1697` from its saved artifacts.

This run checks the 12-field token schema, the output-local incomplete template,
the absent external approval token, blocked materialization, blocked FDTD
execution, blocked downstream states, and figure/script artifacts.

## Output

```text
outputs/experiments/1698_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validator.png
scripts/
```

## Result

```text
check count:                             5
passed checks:                           5
failed checks:                           0
schema fields:                           12
placeholder fields:                      4
external approval token present:         false
ready for materialization:               false
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

## Interpretation

The approval-token schema contract validates and still leaves materialization
blocked. The template is not a completed approval token.

## Decision

Use run `1698` as the artifact validator for run `1697`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_schema_contract_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
