# Experiment 1746: 84-Grid Materialization Critical-Path Audit Validator

Date: 2026-06-30

## Purpose

Validate run `1745`, the 84-grid observed-by-case materialization critical-path
audit.

This is a non-executing validation wrapper around saved run `1745` artifacts.
It does not materialize observed-by-case data, run FDTD, launch GPU work,
transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1746_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
dependency items:                          21
dependency actions:                        4
dependency levels:                         3
root authorization items:                  1
parallel artifacts:                        20
external items missing:                    21
critical-path stages:                      3
materialization ready:                     false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
validation ready:                          true
```

The checks cover source readiness, dependency shape, root/parallel blocker
counts, empty external packet state, execution boundary preservation, figure
output, and frozen script snapshots.

## Interpretation

Run `1745` validates as a non-executing materialization dependency result.

## Decision

Use run `1745` as the materialization dependency checkpoint. Keep FDTD
execution blocked.

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
2357x838, dynamic range=255
```

