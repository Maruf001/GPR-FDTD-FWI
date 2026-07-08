# Experiment 1635: 84-Grid Pilot Real-Output Schema Contract

Date: 2026-06-30

## Purpose

Define the acceptance schema for future real five-row pilot execution results.

Runs `1632-1634` showed that the current pilot executor correctly refuses real
execution. This run turns the next implementation step into a concrete output
contract:

```text
What JSON files and fields must exist before a real five-row pilot result can
be accepted?
```

This is a CPU-only contract run. It does not execute FDTD, FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/experiments/1635_local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_output_file_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_output_field_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gap audit ready:                    true
source validator ready:                    true
source sensitivity ready:                  true
future pilot output files:                 5
required output fields:                    50
real output files present now:             0
real output schemas accepted now:          0
new FDTD executions now:                   0
template/synthetic outputs allowed:        0
remaining output-schema blockers:          3
schema contract ready:                     true
execution permitted:                       false
bounded pilot execution ready:             false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
GPU priority:                              none
```

The five future result files each require 10 top-level fields:

```text
payload_row_id
grid_model_id
objective_profile
transition_bin
solver_status
runtime_seconds
result_summary
solver_log_sha256
input_contract_sha256
new_fdtd_executed
```

## Decision

Use this schema before accepting any real five-row pilot execution result or
expanding to the full 84-row screen. The next 2D implementation task is a
validator for this schema, then a bounded real pilot executor that writes these
files.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
