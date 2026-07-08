# Experiment 1653: 84-Grid Pilot Real-Result Producer Checklist

Date: 2026-06-30

## Purpose

Convert the guarded five-row pilot result requirements into a practical
producer checklist.

Runs `1647-1652` lock file identities and field value domains. This run lists
the five real pilot JSON result files that must be produced before the pilot
can be accepted or expanded to the full 84-row screen.

This run does not write real result files, run FDTD, promote a physical claim,
start GPU work, transfer to field evidence, or escalate to 3D/HPC.

## Output

```text
outputs/experiments/1653_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_producer_checklist
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_producer_checklist_checklist_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_producer_checklist_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_producer_checklist_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_producer_checklist.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source field-domain contract ready:        true
source validation ready:                   true
source sensitivity ready:                  true
checklist files:                           5
required fields:                           50
SHA-256 hash fields:                       10
integer fields:                            10
positive-float fields:                     5
boolean fields:                            5
pending JSON files:                        5
pilot-evidence-ready files:                0
checklist actions:                         3
producer checklist ready:                  true
GPU priority:                              none
```

## Decision

Produce the five real pilot JSON files before rerunning file-identity,
field-domain, and acceptance gates. Full 84-row execution remains blocked
until the five-row pilot is accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_producer_checklist.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
