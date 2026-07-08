# Experiment 1759: 84-Grid Approval-Token Post-Scaffold Live-State Refresh Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1758` validator.

The sensitivity cases check whether the validator rejects false directory,
approval, token, materialization, FDTD, GPU, field-transfer, figure, and script
snapshot states.

This is CPU-only validation sensitivity. It does not create an approval token,
materialize the 84-grid packet, run FDTD, launch GPU work, transfer to field
evidence, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1759_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validation_sensitivity_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                              16
expected pass cases:                 1
expected fail cases:                15
actual pass cases:                   1
actual fail cases:                  15
unexpected cases:                    0
damaged cases:                      15
materialization ready:           false
new FDTD executed:               false
GPU work ready:                  false
```

## Interpretation

The validator accepts only the exact post-scaffold state. It rejects false
approval completion, false token acceptance, and false execution readiness.

## Decision

Use runs `1757-1759` as the guarded post-scaffold approval-token state. The
84-grid branch remains blocked until the real approval token is completed and
accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_post_scaffold_live_state_refresh_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x853, dynamic range=255
```
