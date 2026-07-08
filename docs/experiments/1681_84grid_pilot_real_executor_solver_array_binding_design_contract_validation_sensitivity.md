# Experiment 1681: 84-Grid Pilot Real Executor Solver-Array Binding Design Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `1680` solver-array design-contract validator.

Run `1680` validated the producer map for the four unresolved solver-array
bindings. This run checks that the validator rejects damaged source readiness,
producer mapping, producer availability, array materialization promotion,
payload identity damage, interface damage, FDTD execution promotion, downstream
promotion, figure damage, and script-snapshot damage.

This run does not materialize arrays, bind observed data, run FDTD, write real
solver logs or real result JSON, or promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1681_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
sensitivity cases:                     11
expected pass cases:                   1
expected fail cases:                   10
actual pass cases:                     1
actual fail cases:                     10
unexpected cases:                      0
damaged cases:                         10
solver binding ready:                  false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
sensitivity ready:                     true
```

Damaged cases rejected:

| Case | Damage |
| --- | --- |
| source_ready_false | source contract readiness false |
| producer_map_damage | producer function mapping changed |
| producer_unavailable | producer availability false |
| array_materialization_promotion | array materialization count promoted |
| payload_identity_damage | one revised payload removed |
| interface_missing | `run_candidate_family` parameter marked missing |
| fdtd_promotion | new FDTD execution promoted |
| downstream_promotion | GPU work readiness promoted |
| figure_damage | figure path missing |
| script_snapshot_damage | script snapshot count missing |

## Interpretation

The solver-array design-contract validator is now sensitivity-hardened. It
accepts only the exact design state and rejects producer, materialization,
payload, interface, execution, downstream, figure, and script-snapshot damage.

## Decision

Use runs `1679`-`1681` as the guarded solver-array design block. Solver-array
materialization remains blocked until a bounded materialization run is
explicitly defined.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_solver_array_binding_design_contract_validation_sensitivity.py
3 passed
```

Figure check:

```text
1709x847, dynamic range=255
```
