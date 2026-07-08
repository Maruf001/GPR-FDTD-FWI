# Experiment 1679: 84-Grid Pilot Real Executor Solver-Array Binding Design Contract

Date: 2026-06-30

## Purpose

Map the remaining solver-array bindings for the revised five-row 84-grid pilot
executor to concrete producer functions.

Runs `1676`-`1678` created and guarded the input-contract layer. This run
identifies the producer route for the four unresolved solver-array bindings:
`time_values`, `mute`, `scan_positions`, and `observed_by_case`.

This run does not materialize arrays, bind observed data, run FDTD, write real
solver logs or real result JSON, or promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1679_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_producer_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_interface_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source input-contract sensitivity ready: true
source input-contract audit ready:       true
producer bindings:                       4
producer functions available:            4
arrays materialized:                     0
pilot payloads:                          5
payload 68 included:                     true
stale payload 86 included:               false
input contracts written:                 5
run_candidate_family parameters:         8
parameters present:                      8
solver-array parameters:                 4
actions:                                 5
ready actions:                           0
solver-array design ready:               true
solver arrays materialized now:          false
solver binding ready:                    false
new FDTD executed:                       false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
3D/HPC ready:                            false
design contract ready:                   true
```

Producer map:

| Binding | Producer |
| --- | --- |
| time_values | `base.generate_time_array` |
| mute | `base._build_mute_window` |
| scan_positions | `base.build_scan_positions` |
| observed_by_case | `base.build_observed_cases` |

## Interpretation

The route for the solver-array layer is now explicit. The executor has a
validated input-contract block and all four array producer functions are
available, but no arrays have been materialized and no real executor run has
occurred.

## Decision

Use run `1679` as the design contract before any bounded solver-array
materialization. Real FDTD execution remains blocked until array
materialization, solver logging, result JSON writing, and post-write validation
are implemented and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract.py
4 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
