# Experiment 1745: 84-Grid Materialization Critical-Path Audit

Date: 2026-06-30

## Purpose

Convert the 84-grid observed-by-case materialization return-packet closure
sequence into a dependency/critical-path audit.

Run `1742` established that 21 external items are missing. This run separates
the blocker into stages:

```text
1 root approval token
20 parallel cache/result artifacts
1 final all-items materialization gate
```

This is a non-executing audit. It does not materialize observed-by-case data,
run FDTD, launch GPU work, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1745_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_item_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_critical_path_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
dependency items:                          21
dependency actions:                        4
dependency levels:                         3
root authorization items:                  1
parallel cache/result artifacts:           20
final-gate required items:                 21
external items present:                    0
external items missing:                    21
complete actions:                          0
root authorization present:                false
parallel artifacts present:                0
critical-path stages:                      3
parallel materialization branches:         2
materialization ready:                     false
new FDTD executed:                         false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
critical-path audit ready:                 true
```

Action-level dependency table:

| Action | Dependency level | Required items | Missing items | Dependency |
| --- | ---: | ---: | ---: | --- |
| external approval token | 1 | 1 | 1 | root authorization blocker |
| planned cache arrays | 2 | 10 | 10 | depends on approval token |
| planned result JSON files | 2 | 10 | 10 | depends on approval token |
| final materialization gate | 3 | 21 | 21 | depends on all items |

## Interpretation

The current 84-grid path is not blocked by an ambiguous compute failure. It is
blocked at the return-packet boundary. The first blocker is the external
approval token. After that, the cache arrays and result JSON files form two
parallel materialization artifact branches. Only after all 21 items exist can
the final materialization gate be rerun.

## Decision

Resolve the approval token first, then produce the cache/result artifacts, then
rerun the materialization gate. Keep materialization and FDTD execution blocked
now.

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
2572x852, dynamic range=255
```

