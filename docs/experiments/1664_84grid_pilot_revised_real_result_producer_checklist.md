# Experiment 1664: 84-Grid Pilot Revised Real-Result Producer Checklist

Date: 2026-06-30

## Purpose

Refresh the pilot real-result producer checklist around the revised five-row
pilot candidate.

Run `1663` showed that the old producer checklist, command plan, and fillable
template pack still targeted old payload row `86` and missed revised payload
row `68`. This run refreshes the producer checklist only.

This run does not refresh the command plan or fillable templates, execute FDTD,
accept pilot evidence, launch GPU work, transfer to field evidence, or promote
3D/HPC readiness.

## Output

```text
outputs/experiments/1664_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_producer_checklist
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_producer_checklist_checklist_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_producer_checklist_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_producer_checklist_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_producer_checklist.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source compatibility audit ready:          true
source revised-pilot validation ready:     true
checklist rows:                            5
required payload IDs:                      1;23;46;68;72
contains payload 68:                       true
contains stale payload 86:                 false
contains retained_blend:                   false
required fields:                           50
hash fields:                               10
integer fields:                            10
positive-float fields:                     5
boolean fields:                            5
pilot evidence-ready rows:                 0
real result files present:                 0
new FDTD executions:                       0
command plan refreshed:                    false
fillable templates refreshed:              false
real executor script available:            false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
checklist ready:                           true
```

Revised checklist rows:

| Order | Payload row | Objective profile | Transition bin |
| ---: | ---: | --- | ---: |
| 1 | 1 | highband | 0 |
| 2 | 23 | late | 4 |
| 3 | 46 | late_high | 9 |
| 4 | 68 | veryhigh | 13 |
| 5 | 72 | veryhigh | 17 |

## Interpretation

The producer checklist now matches the revised pilot identity. It no longer
contains `retained_blend` or stale payload `86`, and it includes payload `68`.

The execution path is still not ready. The revised command plan and revised
fillable templates have not been generated yet, and the real executor script is
still absent.

## Decision

Use run `1664` as the revised checklist source. Refresh the command plan and
fillable template pack from this checklist before building or running any real
FDTD pilot executor.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_producer_checklist.py
4 passed
```

Figure check:

```text
2321x847, dynamic range=255
```
