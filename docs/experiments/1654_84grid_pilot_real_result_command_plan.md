# Experiment 1654: 84-Grid Pilot Real-Result Command Plan

Date: 2026-06-30

## Purpose

Convert the run `1653` producer checklist into non-executed validation commands
for the five future real pilot JSON files.

Each command checks that the staged JSON file is nonempty, parses as JSON, and
has a SHA-256 checksum. The commands are intended to run only after real pilot
outputs are produced.

This run does not execute the commands, write real result files, run FDTD,
promote a physical claim, start GPU work, transfer to field evidence, or
escalate to 3D/HPC.

## Output

```text
outputs/experiments/1654_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_command_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_command_plan_command_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_command_plan_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_command_plan_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_command_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source producer checklist ready:           true
commands:                                  5
required fields covered:                   50
commands executed:                         0
JSON-file checks ready:                    0
command actions:                           3
command plan ready:                        true
GPU priority:                              none
```

## Decision

Run these commands only after all five real pilot JSON files are produced.
Then rerun file-identity, field-domain, and acceptance gates. Full 84-row
execution remains blocked until the five-row pilot is accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_command_plan.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
