# Experiment 1650: 84-Grid Pilot Real-Result Field Value-Domain Contract

Date: 2026-06-30

## Purpose

Define value-domain checks for the 50 required fields in the future five-row
real pilot JSON outputs.

Runs `1647-1649` lock the file identities. This run adds the field-level value
rules for payload row, grid identifier, objective profile, transition bin,
solver status, runtime, result summary, solver-log hash, input-contract hash,
and new-FDTD-executed flag.

This run does not write real result files, run FDTD, promote a physical claim,
start GPU work, transfer to field evidence, or escalate to 3D/HPC.

## Output

```text
outputs/experiments/1650_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_field_value_domain_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source file-identity ready:                true
source file-identity validation ready:     true
source file-identity sensitivity ready:    true
source acceptance gate ready:              true
required field value contracts:            50
payloads:                                  5
required field names:                      10
integer fields:                            10
SHA-256 hash fields:                       10
positive-float fields:                     5
boolean fields:                            5
structured-object fields:                  5
present fields:                            0
accepted field values:                     0
value actions:                             3
field value-domain contract ready:         true
GPU priority:                              none
```

## Decision

Future real pilot JSON files must pass both file-identity checks and field
value-domain checks before the five-row pilot can be accepted as FDTD evidence
or expanded to the 84-row screen.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_field_value_domain_contract.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
