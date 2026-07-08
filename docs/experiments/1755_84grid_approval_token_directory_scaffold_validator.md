# Experiment 1755: 84-Grid Approval-Token Directory Scaffold Validator

Date: 2026-06-30

## Purpose

Validate the saved run `1754` directory-scaffold artifact set.

The validator checks that the scaffold state is complete at the directory
level, incomplete at the approval-token level, and not promoted into execution
readiness.

This is CPU-only artifact validation. It does not create an approval token,
materialize the 84-grid packet, run FDTD, launch GPU work, transfer to field
evidence, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1755_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              6
checks passed:                       6
checks failed:                       0
scaffold paths:                      1
parent directory present after:      1
external approval token present:     0
real approval fields missing:        4
complete actions:                    1
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
```

## Interpretation

The directory-scaffold state is valid and intentionally incomplete. It confirms
that the next missing item is not another directory operation; it is the real
approval token and its four real approval fields.

## Decision

Treat the directory scaffold as accepted for the 84-grid branch. Keep all
execution and downstream promotion gates closed.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validator.py
3 passed
```

Figure check:

```text
2357x841, dynamic range=255
```
