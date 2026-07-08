# Experiment 1756: 84-Grid Approval-Token Directory Scaffold Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1755` validator.

The sensitivity cases check whether the validator rejects malformed scaffold
state, false token promotion, false materialization readiness, false FDTD/GPU
readiness, and missing figure or script evidence.

This is CPU-only validation sensitivity. It does not create an approval token,
materialize the 84-grid packet, run FDTD, launch GPU work, transfer to field
evidence, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1756_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validation_sensitivity_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                               16
expected pass cases:                 1
expected fail cases:                 15
actual pass cases:                   1
actual fail cases:                   15
unexpected cases:                    0
damaged cases:                       15
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
3D/HPC ready:                        false
```

## Interpretation

The validator accepts only the exact directory-scaffold state. It rejects
claims that the token exists, that the token is accepted, that the missing
approval fields have been closed, or that any execution path is ready.

## Decision

Use runs `1754-1756` as the guarded 84-grid approval-token directory-scaffold
block. The next unresolved blocker is the real approval token, not directory
creation.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_directory_scaffold_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x854, dynamic range=255
```
