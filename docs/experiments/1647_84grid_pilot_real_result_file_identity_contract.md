# Experiment 1647: 84-Grid Pilot Real-Result File Identity Contract

Date: 2026-06-30

## Purpose

Lock the file identities for the five future real pilot result JSON files.

Runs `1641-1646` defined the result-file acceptance gate and created the empty
staging directory. This run records the expected payload row, pilot order,
objective profile, transition bin, result path, and required top-level field
sequence for each future JSON file.

This run does not write real result files, run FDTD, promote a physical claim,
start GPU work, transfer to field evidence, or escalate to 3D/HPC.

## Output

```text
outputs/experiments/1647_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_file_identity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_directory_manifest_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gate ready:                         true
source scaffold ready:                     true
source scaffold validation ready:          true
source scaffold sensitivity ready:         true
required file identities:                  5
unique file identities:                    5
unique field sequences:                    1
required fields:                           50
required directories:                      1
present directories:                       1
unexpected files:                          0
present files:                             0
JSON parse ready files:                    0
accepted files:                            0
new FDTD executions:                       0
identity actions:                          4
identity contract ready:                   true
GPU priority:                              none
```

## Decision

The future five-row pilot JSON outputs now have a locked file-identity
contract. Real files must match this identity contract before FDTD results can
be accepted or the full 84-row screen can be launched.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
