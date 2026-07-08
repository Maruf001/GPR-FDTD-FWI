# Experiment 1747: 84-Grid Materialization Critical-Path Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1746` validator by confirming that it accepts the exact
run `1745` critical-path audit and rejects damaged or prematurely promoted
states.

This is a non-executing validation-sensitivity wrapper around saved artifacts.
It does not materialize observed-by-case data, run FDTD, launch GPU work,
transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1747_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validation_sensitivity_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                         17
expected pass cases:                       1
expected fail cases:                       16
actual pass cases:                         1
actual fail cases:                         16
unexpected cases:                          0
damaged cases:                             16
materialization ready:                     false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
validation sensitivity ready:              true
```

The damaged cases cover source readiness, item/action shape, dependency-level
count, root/parallel blocker counts, false external item presence, false root
approval presence, false materialization/FDTD/GPU/field/3D promotion, figure
damage, and missing script snapshots.

## Interpretation

The validator accepts only the exact critical-path audit and rejects all
damaged states tested here. This keeps the result narrow: run `1745` is a
dependency checkpoint, not a materialization or FDTD execution event.

## Decision

Keep run `1745` as a non-executing 84-grid materialization dependency
checkpoint.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validation_sensitivity.py
9 passed
```

Figure check:

```text
2717x850, dynamic range=255
```

