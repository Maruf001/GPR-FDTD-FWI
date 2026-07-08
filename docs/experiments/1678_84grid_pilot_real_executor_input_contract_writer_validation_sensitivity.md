# Experiment 1678: 84-Grid Pilot Real Executor Input-Contract Writer Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `1677` input-contract writer validator.

Run `1677` validated the five input contracts from run `1676`. This run checks
that the validator rejects damaged source readiness, missing contracts, payload
identity drift, FDTD execution promotion, binding-count damage, downstream
promotion, figure damage, and script-snapshot damage.

This run does not bind observed data, scan positions, time values, or a mute
mask; does not run FDTD; does not write real solver logs or real result JSON;
and does not promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1678_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
sensitivity cases:                     9
expected pass cases:                   1
expected fail cases:                   8
actual pass cases:                     1
actual fail cases:                     8
unexpected cases:                      0
damaged cases:                         8
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
| source_ready_false | source audit readiness false |
| missing_contract | one input contract row removed |
| payload_identity_duplicate | payload contract path duplicated, removing one revised payload identity |
| fdtd_promotion | new FDTD execution promoted |
| binding_count_damage | remaining blocking binding count changed |
| downstream_promotion | GPU work readiness promoted |
| figure_damage | figure path missing |
| script_snapshot_damage | script snapshot count missing |

## Interpretation

The input-contract writer validator is sensitive to the failure modes that
would matter before real execution. It rejects missing or duplicated payload
contracts, execution promotion, blocker-count drift, downstream promotion, and
missing figure/script evidence.

## Decision

Use runs `1676`-`1678` as the guarded input-contract block for the revised 2D
pilot executor. The next implementation work remains the seven unresolved
solver-array and output-writing bindings.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validation_sensitivity.py
3 passed
```

Figure check:

```text
1709x847, dynamic range=255
```
