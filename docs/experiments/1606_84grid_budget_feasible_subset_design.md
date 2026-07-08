# Experiment 1606: 84-Grid Budget-Feasible Subset Design

Date: 2026-06-29

## Purpose

Repair the budget-headroom blocker from the run `1603` 90-grid execution
readiness gate without executing FDTD.

The 90-grid design had only 1.30755 minutes of headroom under a 60-minute
budget, below the required 5.0 minutes. This run removes six interior midpoint
rows and checks whether the remaining subset preserves the objective and
transition coverage needed for a future execution contract.

## Output

```text
outputs/experiments/1606_local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_selected_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_removed_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source payload rows:                         90
selected payload rows:                       84
removed payload rows:                        6
objective profiles retained:                 5
transition bins still covered:               18
endpoint rows retained:                      10
budget:                                      60.0 minutes
estimated seconds per grid:                  39.1283
selected estimated runtime:                  54.77962 minutes
selected budget headroom:                    5.22038 minutes
minimum required headroom:                   5.0 minutes
budget headroom requirement passed:          true
90-grid source headroom requirement passed:  false
budget blocker closed by subset design:      true
remaining execution-contract blockers:       5
execution permitted:                         false
new FDTD executed:                           false
GPU priority:                                none
```

The six removed rows are interior midpoint bins:

| Objective profile | Removed transition bins |
| --- | --- |
| `highband` | 8 |
| `late` | 9 |
| `late_high` | 8 |
| `veryhigh` | 9 |
| `retained_blend` | 8, 9 |

All objective profiles remain represented, and each objective keeps both
transition endpoints.

## Decision

Use this as the budget-feasible subset design for the next execution-contract
step. Do not execute the screen yet: run-specific script, command inventory,
output contract, resume policy, and resource guard are still absent.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_budget_feasible_subset_design.py
3 passed
```

Figure check:

```text
3221x844, dynamic range=255
```
