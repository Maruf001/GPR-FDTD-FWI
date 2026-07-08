# Experiment 1690: 84-Grid Pilot Real-Executor Observed-By-Case Bounded Input Design Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1689` validator with controlled damage to the run `1688`
bounded input design contract.

This run checks that the validator fails when target identity, case identity,
revised payload identity, solve budget, blocker state, observed-data state,
finite difference time domain state, downstream state, figure paths, or script
snapshots are damaged.

## Output

```text
outputs/experiments/1690_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       13
expected pass cases:                     1
expected fail cases:                     12
actual pass cases:                       1
actual fail cases:                       12
unexpected cases:                        0
damaged cases:                           12
observed_by_case materialized:           false
new FDTD executed:                       false
bounded pilot execution ready:           false
gpu work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

The exact source contract passes. Damaged states fail for:

```text
source readiness removal
true-model target identity damage
case identity damage
revised payload identity damage
solve-budget damage
blocker removal
blocker readiness promotion
observed_by_case promotion
FDTD execution promotion
downstream GPU promotion
missing figure
missing script snapshots
```

## Interpretation

The bounded input contract validator is sensitive to the intended failure
modes. It cannot silently accept stale payload identity, altered solve budgets,
or accidental promotion from design contract to execution evidence.

## Decision

Use runs `1688-1690` as the validated non-executing input-contract block. The
next 2D step must be a separately versioned execution contract before any
observed-data materialization or finite difference time domain solve is run.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_bounded_input_design_contract_validation_sensitivity.py

10 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
