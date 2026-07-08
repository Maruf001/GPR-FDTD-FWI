# Experiment 1641: 84-Grid Pilot Real-Result File Acceptance Gate

Date: 2026-06-30

## Purpose

Turn the five-row pilot real-output schema and implementation-gap audit into a
concrete result-file acceptance gate.

This run defines the file and field checks for future real pilot outputs. It
does not run FDTD, does not write real result files, and does not promote any
physical, GPU, field, or 3D/HPC claim.

## Output

```text
outputs/experiments/1641_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_file_gate_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_field_gate_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_acceptance_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source schema ready:                       true
source schema validation ready:            true
source schema sensitivity ready:           true
source implementation-gap ready:           true
source gap validation ready:               true
source gap sensitivity ready:              true
required result files:                     5
present result files:                      0
nonempty result files:                     0
JSON parse ready files:                    0
accepted result files:                     0
new FDTD executions:                       0
template or synthetic outputs allowed:     0
required fields:                           50
accepted fields:                           0
acceptance actions:                        4
ready acceptance actions:                  0
acceptance gate ready:                     true
GPU priority:                              none
```

## Decision

The five-row pilot now has an explicit result-file acceptance gate. The current
state remains non-evidence: no result JSON files, required fields, solver logs,
input-contract hashes, or FDTD executions are accepted.

The next 2D implementation task is still a bounded real five-row pilot executor
that writes these result files. Full 84-row execution remains blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
