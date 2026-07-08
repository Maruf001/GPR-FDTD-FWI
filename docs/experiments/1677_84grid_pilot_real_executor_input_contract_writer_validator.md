# Experiment 1677: 84-Grid Pilot Real Executor Input-Contract Writer Validator

Date: 2026-06-30

## Purpose

Validate the run `1676` revised pilot input-contract writer output.

Run `1676` wrote five non-evidence input contracts for revised pilot payloads
`1;23;46;68;72`. This run checks that those contracts exist, preserve the
revised payload set, retain the unresolved solver bindings, and keep FDTD
execution blocked.

This run does not bind observed data, scan positions, time values, or a mute
mask; does not run FDTD; does not write real solver logs or real result JSON;
and does not promote GPU, field, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1677_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source audit ready:                    true
checks:                                8
passed checks:                         8
failed checks:                         0
input contracts written:               5
unresolved solver bindings total:      20
bindings closed:                       1
remaining blocking bindings:           7
new FDTD executed:                     false
execution permitted:                   false
bounded CPU execution ready:           false
bounded pilot execution ready:         false
physical claim ready:                  false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
validation ready:                      true
```

Validation checks:

| Check | Passed |
| --- | --- |
| source audit ready | true |
| five input contracts exist | true |
| revised payload identity | true |
| unresolved solver bindings preserved | true |
| no FDTD execution | true |
| one binding closed and seven remain | true |
| downstream remains blocked | true |
| figure and scripts exist | true |

## Interpretation

The input-contract writer output is structurally valid. It captures the revised
payload set and explicitly keeps `observed_by_case`, `scan_positions`,
`time_values`, and `mute` unresolved in each contract.

This validates only the input-contract layer. Real execution remains blocked by
the remaining solver-array and output-writing bindings.

## Decision

Use runs `1676` and `1677` as the guarded input-contract block for the revised
2D pilot executor. Do not enable real FDTD execution until the seven remaining
bindings are implemented and validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_input_contract_writer_validator.py
3 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
