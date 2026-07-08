# Experiment 1607: 84-Grid Budget-Feasible Subset Design Validator

Date: 2026-06-29

## Purpose

Validate the run `1606` budget-feasible subset design from saved artifacts.

## Output

```text
outputs/experiments/1607_local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation passes:                           5
blocking failures:                           0
validation ready:                            true
selected payload rows:                       84
removed payload rows:                        6
selected budget headroom:                    5.22038 minutes
remaining execution-contract blockers:       5
execution permitted:                         false
bounded CPU execution ready:                 false
new FDTD executed:                           false
GPU priority:                                none
```

The validator confirms that the six removed rows are midpoint rows, all
objective endpoints are retained, the budget blocker is closed, and execution
remains blocked until the non-budget execution contracts exist.

## Decision

Use run `1607` as the artifact guard for run `1606`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_validator.py
4 passed
```

Figure check:

```text
2141x838, dynamic range=255
```
