# Experiment 1707: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval-Token Synthetic Completion Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `1706` from saved artifacts.

This run checks that the synthetic completion smoke is internally consistent,
that all schema rules pass, that the synthetic token remains output-local, and
that the real external approval boundary is still closed.

## Output

```text
outputs/experiments/1707_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
schema fields checked:          12
schema rules passed:            12
synthetic completion fields:     4
synthetic token written:         true
synthetic token is output-local: true
synthetic token is external:     false
external approval token present: false
ready for materialization:       false
new FDTD executed:               false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
```

The five checks cover source readiness, schema validation rows, synthetic-token
path and contents, external approval and execution blocking, and figure/script
artifacts.

## Interpretation

Run `1706` is a valid schema smoke test, not an approval event. The synthetic
token proves the JSON shape can be completed, while run `1707` confirms that no
real approval, materialization, FDTD execution, or downstream promotion occurred.

## Decision

Use run `1707` as the artifact guard for run `1706`. The next materialization
step remains blocked until a real external approval token is supplied and the
approval gate is rerun.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_synthetic_completion_smoke_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
