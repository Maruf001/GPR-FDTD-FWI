# Experiment 1696: 84-Grid Pilot Real-Executor Observed-By-Case Materialization Approval Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1695` validator with controlled damage to the run `1694`
approval-gate artifacts.

This run checks that the validator fails when approval, planned artifact,
materialization, command execution, FDTD execution, downstream state, figure
metadata, or script snapshots are damaged.

## Output

```text
outputs/experiments/1696_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       15
expected pass cases:                     1
expected fail cases:                     14
actual pass cases:                       1
actual fail cases:                       14
unexpected cases:                        0
damaged cases:                           14
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
ready for 3D/HPC:                        false
```

Damaged states fail for:

```text
source readiness removal
approval-token presence
approval-token acceptance
artifact row removal
artifact role damage
artifact presence promotion
artifact acceptance promotion
materialization-readiness promotion
observed-array materialization promotion
command-execution promotion
FDTD-execution promotion
GPU-readiness promotion
figure damage
missing script snapshots
```

## Interpretation

The approval-gate validator is sensitive to the intended failure modes. It
rejects accidental promotion of planning artifacts into executed evidence.

## Decision

Use runs `1694-1696` as the guarded materialization approval block. Keep
observed-by-case materialization blocked until an explicit approval token and a
separate execution run exist.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_approval_gate_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
