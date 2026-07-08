# Experiment 1762: 84-Grid Approval-Token Handoff Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1761` handoff-template validator.

The sensitivity audit checks that the validator accepts the exact non-live
template state and rejects damaged or falsely promoted states, including a
filled template placeholder, a false external-token claim, false
materialization readiness, and false FDTD/GPU promotion.

This is CPU-only validator sensitivity auditing. It does not create a live
approval token, materialize the 84-grid packet, run FDTD, launch GPU work,
transfer to field evidence, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1762_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_handoff_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_handoff_template_pack_validation_sensitivity_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_handoff_template_pack_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_handoff_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                  17
expected pass cases:                 1
expected fail cases:                16
actual pass cases:                   1
actual fail cases:                  16
unexpected outcomes:                 0
damaged cases:                      16
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
```

## Interpretation

The validator is strict enough for this handoff boundary. It accepts the exact
template-only state and rejects false approval, false token presence, false
materialization readiness, false FDTD/GPU readiness, figure damage, and missing
script snapshots.

## Decision

Keep materialization and FDTD execution blocked until the external approval
token is completed outside the handoff-template pack.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_token_handoff_template_pack_validation_sensitivity.py
2 passed
```

Figure check:

```text
2753x874, dynamic range=255
```
