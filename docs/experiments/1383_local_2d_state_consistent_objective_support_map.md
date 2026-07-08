# Experiment 1383: Local 2D State-Consistent Objective Support Map

Date: 2026-06-27

## Purpose

Map which objective labels actually support the promoted corrected-state
evidence from run `1382`.

This run does not rerun the optimizer, launch broad batches, run GPU work, use
field data, run field FWI, perform 3D/HPC work, or train neural networks.

## Output

```text
outputs/experiments/1383_local_2d_state_consistent_objective_support_map
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_support_rows.csv
data/local_2d_state_consistent_objective_support_by_run.csv
data/local_2d_state_consistent_objective_support_map_summary.json
figures/local_2d_state_consistent_objective_support_map.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_SUPPORT_MAP.md
scripts/run_local_2d_state_consistent_objective_support_map.py
scripts/test_local_2d_state_consistent_objective_support_map.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source status rows:                  116
promoted rows:                       12
objective support rows:              6
run support rows:                    5
core objective count:                2
core objective labels:               base, highband
expanded-only objective labels:      early_high, late, late_high, veryhigh
minimum promoted margin:             0.00799252117380315
objective support map ready:         true
broad radius tolerance promoted:     false
broad batch ready:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
```

Objective support:

| Objective | Accepted rows | Accepted run count | Min margin | Core regression objective |
| --- | ---: | ---: | ---: | --- |
| base | 4 | 4 | 0.022485563942480497 | true |
| early_high | 1 | 1 | 0.00799252117380315 | false |
| highband | 4 | 4 | 0.01994705692712514 | true |
| late | 1 | 1 | 0.03116866327859709 | false |
| late_high | 1 | 1 | 0.04212689628171617 | false |
| veryhigh | 1 | 1 | 0.01994273760685534 | false |

## Interpretation

Only `base` and `highband` have promoted corrected-state support across every
promoted source run. The other promoted objective labels appear only in the
expanded-window run `1379`, so they should remain supporting observations
rather than general acceptance objectives.

## Decision

Use `base` and `highband` as the core regression objectives for future local 2D
state-consistency checks. Keep `early_high`, `late`, `late_high`, and
`veryhigh` as expanded-window observations until they are tested across more
than one promoted source run.

Do not promote broad radius tolerance, broad batches, GPU work, field transfer,
field FWI, or 3D/HPC work from this evidence.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_objective_support_map.py
sha256: 8c498fb9de63c1e8937cff7de5a67a570af0d1bc6262fc1a1eb3a5dcfd93592b

test_local_2d_state_consistent_objective_support_map.py
sha256: 96b562540980de1bc7e7dc8b73af6b42b1244ab912d8063383f498471cbc1ecd
```

Subsequent related local 2D state-consistency experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_support_map.py
4 passed
```

Figure check:

```text
local_2d_state_consistent_objective_support_map.png
2680x846, dynamic range=255
```
