# Experiment 1680: 84-Grid Pilot Real Executor Solver-Array Binding Design Contract Validator

Date: 2026-06-30

## Purpose

Validate the run `1679` solver-array binding design contract.

Run `1679` mapped the four unresolved solver-array bindings to concrete
producer functions. This run checks that the producer map is exact, the revised
payload identities are preserved, no arrays are materialized, no execution is
promoted, and downstream states remain blocked.

This run does not materialize arrays, bind observed data, run FDTD, write real
solver logs or real result JSON, or promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1680_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source contract ready:                 true
checks:                                8
passed checks:                         8
failed checks:                         0
producer bindings:                     4
producer functions available:          4
arrays materialized:                   0
pilot payloads:                        5
run_candidate_family parameters:       8
solver-array parameters:               4
solver binding ready:                  false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
validation ready:                      true
```

Validation checks:

| Check | Passed |
| --- | --- |
| source contract ready | true |
| producer map | true |
| no arrays materialized | true |
| revised payload identity | true |
| `run_candidate_family` interface coverage | true |
| no execution promotion | true |
| downstream remains blocked | true |
| figure and scripts exist | true |

## Interpretation

The solver-array binding route is valid as a design contract. The four
producer functions are available, and the target executor interface expects the
same four unresolved arrays. No arrays have been built yet, so this is still a
pre-execution checkpoint.

## Decision

Use runs `1679` and `1680` as the guarded solver-array binding design block.
Do not materialize arrays or enable FDTD before a bounded materialization run
is defined and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validator.py
3 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
