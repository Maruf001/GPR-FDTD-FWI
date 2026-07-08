# Experiment 1682: 84-Grid Pilot Real Executor Safe Solver-Array Materialization Audit

Date: 2026-06-30

## Purpose

Materialize only the solver arrays that are safe to build without observed-case
solver execution.

Runs `1679`-`1681` mapped and guarded the solver-array design. This run builds
the cheap, non-observed bindings: `time_values`, `mute`, and per-payload
`scan_positions`. It deliberately leaves `observed_by_case` unbuilt because
that is the solver-data-producing step.

This run does not build observed cases, run FDTD, write real solver logs or
real result JSON, or promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1682_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit_time_mute_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit_scan_position_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit_binding_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source design sensitivity ready:        true
source design ready:                    true
pilot payloads:                         5
payload 68 included:                    true
stale payload 86 included:              false
time_values materialized:               true
mute materialized:                      true
scan-position payloads:                 5
scan-position payloads materialized:    5
observed_by_case materialized:          false
safe array bindings materialized:       3
remaining array bindings:               1
solver binding ready:                   false
commands executed:                      false
new FDTD executed:                      false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
audit ready:                            true
```

Binding status:

| Binding | Materialized | Remaining blocker |
| --- | --- | --- |
| time_values | true | false |
| mute | true | false |
| scan_positions | true | false |
| observed_by_case | false | true |

## Interpretation

Three of the four solver-array bindings are now safely materialized without
observed-case construction. This is still not an FDTD run. The remaining array
blocker is `observed_by_case`, which must be bounded separately because it
constructs solver data.

## Decision

Use run `1682` as the safe materialization checkpoint. Do not enable real FDTD
or write real result JSON until `observed_by_case` materialization is separately
bounded, executed, and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_safe_solver_array_materialization_audit.py
4 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
