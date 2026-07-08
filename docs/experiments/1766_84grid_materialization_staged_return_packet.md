# Experiment 1766: 84-Grid Materialization Staged Return Packet

Date: 2026-07-01

## Purpose

Convert the 84-grid materialization critical path from run `1745` and the
approval-token handoff from run `1760` into a staged external return packet.

This run does not create approval, materialize observed-by-case data, run FDTD,
launch GPU work, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1766_local_2d_state_consistent_objective_revision_84grid_materialization_staged_return_packet
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_materialization_staged_return_packet_item_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_materialization_staged_return_packet_stage_rows.csv
data/staged_84grid_return_packet/
docs/OBSERVED_BY_CASE_STAGED_RETURN_PACKET.md
figures/local_2d_state_consistent_objective_revision_84grid_materialization_staged_return_packet.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stages:                              6
external items:                      21
approval-token items:                1
artifact items:                      20
cache arrays:                        10
result JSON files:                   10
artifact jobs:                       10
required approval fields:            4
blank approval fields:               4
external items present:              0
external items missing:              21
stage-only packet files:             6
cumulative packet files:             6
first artifact smoke items:          2
first two artifact-stage items:      4
first two artifact-stage jobs:       2
remaining artifact-stage items:      16
remaining artifact-stage jobs:       8
final cumulative external items:     21
final cumulative artifact jobs:      10
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

Return stages:

| Stage | Stage | External items | Cumulative external items | Artifact jobs |
| ---: | --- | ---: | ---: | ---: |
| 1 | approval token | 1 | 1 | 0 |
| 2 | first nominal job smoke | 2 | 3 | 1 |
| 3 | first time-shift job smoke | 2 | 5 | 1 |
| 4 | middle payload jobs | 8 | 13 | 4 |
| 5 | late payload jobs | 8 | 21 | 4 |
| 6 | final materialization gate | 0 | 21 | 0 |

## Interpretation

The 84-grid branch still does not justify a new simulation run. The current
blocker is the external return path: one approval token and twenty materialized
job artifacts are absent.

The staged packet makes the next return small and testable. First fill the real
approval token. Then return a two-file nominal job smoke pair, followed by the
paired time-shift smoke pair. Only after those returns should the remaining
sixteen artifacts be filled and the materialization gate rerun.

## Decision

Use this packet before considering new 2D simulation execution. Keep
materialization, FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC
blocked until the approval token and all twenty artifacts are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_materialization_staged_return_packet.py
4 passed
```

Figure check:

```text
2486x883, dynamic range=255
```
