# Experiment 1638: 84-Grid Pilot Real-Execution Implementation Gap Audit

Date: 2026-06-30

## Purpose

Connect the five-row pilot output schema from runs `1635-1637` to the current
executor implementation.

This run asks whether the current code can now execute the real five-row pilot
and write accepted result files, or whether the project still needs a separate
bounded real-pilot executor.

This is a CPU-only audit. It does not run FDTD, FWI, GPU work, field transfer,
or 3D/HPC work.

## Output

```text
outputs/experiments/1638_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_executor_probe_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_output_acceptance_probe_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_blocker_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source schema ready:                       true
source validation ready:                   true
source sensitivity ready:                  true
pilot rows:                                5
executor probes:                           5
executor real-mode refusals:               5
real FDTD execution enabled:               0
new FDTD executions:                       0
expected real output files:                5
real output files present now:             0
real output schemas accepted now:          0
template or synthetic outputs allowed:     0
implementation blockers:                   4
ready implementation blockers:             0
implementation-gap audit ready:            true
GPU priority:                              none
```

The four remaining blockers are:

| Order | Blocker | Required artifact |
| ---: | --- | --- |
| 1 | duplicated real pilot executor | five bounded real pilot executions with solver logs |
| 2 | real result JSON writer | five nonempty real pilot result JSON files |
| 3 | real result validator | five schema-accepted real pilot result JSON files |
| 4 | pilot-to-84 decision table | bounded pilot decision table with no template or synthetic substitutions |

## Decision

The schema block is ready, but it is still not evidence of a real pilot run.
The current guarded executor refuses real mode for every selected row, and no
real result files are present or accepted.

The next 2D task is a duplicated bounded real-pilot executor and output
validator. Full 84-row execution remains blocked until the five-row pilot
produces accepted real outputs.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit.py
3 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
