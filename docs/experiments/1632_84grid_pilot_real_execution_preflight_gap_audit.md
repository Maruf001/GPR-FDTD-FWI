# Experiment 1632: 84-Grid Pilot Real-Execution Preflight Gap Audit

Date: 2026-06-30

## Purpose

Audit what still blocks real execution of the five-row 84-grid pilot.

This run probes the current pilot executor in real mode for the five selected
rows. The expected result is refusal, not execution. It does not run FDTD,
launch GPU work, transfer to field data, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1632_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_real_mode_probe_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source pilot ready:                        true
source smoke ready:                        true
source validation ready:                   true
source sensitivity ready:                  true
pilot rows:                                5
estimated pilot runtime:                   195.6415 seconds
estimated pilot runtime:                   3.26069 minutes
real-mode probes:                          5
real-mode refusals:                        5
pilot execution allowed by design:         0
real FDTD execution enabled:               0
new FDTD executed:                         0
implementation actions:                    4
ready implementation actions:              0
remaining real-pilot blockers:             4
GPU priority:                              none
```

Probe result:

| Payload row | Objective profile | Real-mode exit code | Refused | Real FDTD enabled | New FDTD executed |
| ---: | --- | ---: | --- | --- | --- |
| 1 | highband | 2 | true | false | false |
| 23 | late | 2 | true | false | false |
| 46 | late_high | 2 | true | false | false |
| 86 | retained_blend | 2 | true | false | false |
| 72 | veryhigh | 2 | true | false | false |

## Decision

The five-row pilot is ready only through contract-check smoke and validation.
It is not ready for real execution. The next implementation step is a separate
real pilot executor plus a real output validator, followed by the five-row
bounded pilot before any full 84-row screen.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_preflight_gap_audit.py
3 passed
```

Figure check:

```text
2465x845, dynamic range=255
```
