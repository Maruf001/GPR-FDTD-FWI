# Experiment 1620: 84-Grid Pilot Execution Design

Date: 2026-06-30

## Purpose

Choose the smallest credible next 2D execution step after the 84-grid
contract-check block.

Runs `1606-1619` established that the 84-row screen is budget-feasible and that
all 84 rows pass contract-check execution, but real FDTD execution is still not
enabled. This run selects a five-row pilot from that guarded 84-row subset
before any full screen is attempted.

## Output

```text
outputs/experiments/1620_local_2d_state_consistent_objective_revision_84grid_pilot_execution_design
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_pilot_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_action_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source 84-grid rows:                       84
pilot rows:                                5
objective profiles covered:                5
transition bins covered:                   5
endpoint pilot rows:                       2
central-band pilot rows:                   1
estimated seconds per grid row:            39.1283
pilot estimated total time:                3.26069 minutes
pilot budget:                              10.0 minutes
pilot budget headroom:                     6.73931 minutes
minimum required pilot headroom:           5.0 minutes
pilot budget headroom passed:              true
pilot fraction of 84-grid screen:          0.05952
remaining pilot execution blockers:        3
pilot execution design ready:              true
execution permitted:                       false
new FDTD executed:                         false
GPU priority:                              none
```

Pilot rows:

| Order | Payload row | Objective profile | Transition bin | Transition fraction |
| ---: | ---: | --- | ---: | ---: |
| 1 | 1 | highband | 0 | 0.000000 |
| 2 | 23 | late | 4 | 0.235294 |
| 3 | 46 | late_high | 9 | 0.529412 |
| 4 | 86 | retained_blend | 13 | 0.764706 |
| 5 | 72 | veryhigh | 17 | 1.000000 |

## Interpretation

The next 2D step is no longer ambiguous. The full 84-row CPU screen should not
be the first real execution attempt. A five-row pilot is enough to exercise all
five objective profiles, both transition endpoints, and the midpoint band while
using only about six percent of the full 84-row screen.

This run still does not execute FDTD. It defines the pilot target and preserves
three blockers: a duplicated pilot executor, a pilot-only real command
inventory, and a pilot output validator.

## Decision

Use this five-row pilot as the next 2D execution target. Do not run the full
84-row screen until the pilot executor, real command inventory, and output
validator exist and pass.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_execution_design.py
3 passed
```

Figure check:

```text
3258x881, dynamic range=255
```
