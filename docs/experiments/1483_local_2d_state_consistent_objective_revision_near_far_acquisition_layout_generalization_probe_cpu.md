# Experiment 1483: Near/Far Acquisition-Layout Generalization Probe

Date: 2026-06-28

## Purpose

Execute the acquisition-layout axis from the guarded run `1466` near/far
generalization design.

This CPU-only probe repeats the near/far radius-error interaction grid for
matched 20 mm and 45 mm Tx/Rx offsets. It keeps the geometry, candidate grid,
objective windows, source profile, and noise seed fixed while changing only the
transmitter/receiver offset.

This does not launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/experiments/1483_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_probe.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_GENERALIZATION_PROBE.md
```

## Result

```text
Tx/Rx offsets mm:                    [20.0, 45.0]
Tx/Rx offset count:                  2
near-radius deltas:                  5
far-radius deltas:                   3
grid models:                         30
objective selection rows:            180
candidate rows:                      720
all-objectives-truth models:         18
any-failure models:                  12
all-objective failure models:        8
first any-failure by acquisition/far:{'tx_rx_offset_20mm': {'0.0': 1.5, '-0.8': 0.5, '-1.6': 0.5}, 'tx_rx_offset_45mm': {'0.0': 1.5, '-0.8': None, '-1.6': None}}
first all-failure by acquisition/far:{'tx_rx_offset_20mm': {'0.0': 1.5, '-0.8': 1.5, '-1.6': 1.5}, 'tx_rx_offset_45mm': {'0.0': 1.5, '-0.8': None, '-1.6': None}}
acquisition probe ready:             true
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The acquisition layout changes the near/far failure boundary strongly in this
tested grid. The baseline 20 mm Tx/Rx layout reproduces the prior far-error
behavior: far-neighbor radius errors move the first any-objective failure to
near +0.5 mm and all-objective failures start at near +1.5 mm. The 45 mm Tx/Rx
layout suppresses the far-error-driven failures in this grid; failures remain
only for far=0 at near +1.5 mm and +1.9 mm.

## Decision

Use this as the executed acquisition-layout generalization check. Keep
broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked
until the acquisition result is validated and integrated with the position,
depth, spacing, and source-model blocks.
