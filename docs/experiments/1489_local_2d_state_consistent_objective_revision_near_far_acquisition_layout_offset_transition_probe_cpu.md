# Experiment 1489: Near/Far Acquisition-Layout Offset Transition Probe

Date: 2026-06-29

## Purpose

Expand the run `1483` acquisition-layout check from two Tx/Rx offsets to five
offsets:

```text
20, 30, 35, 40, 45 mm
```

Run `1483` showed that the 20 mm layout reproduces far-error-driven failures,
while the 45 mm layout suppresses far-error-driven failures in the tested grid.
This run asks where that transition begins.

This is CPU-only. It does not launch GPU work, transfer to field evidence, run
field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1489_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_probe_cpu_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_probe_cpu_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_probe_cpu.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_OFFSET_TRANSITION_PROBE_CPU.md
```

## Result

```text
Tx/Rx offsets mm:                    [20.0, 30.0, 35.0, 40.0, 45.0]
Tx/Rx offset count:                  5
near-radius deltas:                  5
far-radius deltas:                   3
grid models:                         75
objective selection rows:            450
candidate rows:                      1800
all-objectives-truth models:         45
any-failure models:                  30
all-objective failure models:        18
first suppressed far -0.8 offset mm: 45.0
first suppressed far -1.6 offset mm: 45.0
figure size:                         2430x1495
figure dynamic range:                255
```

The transition is not monotonic in claim strength. All-objective far-error
failures disappear by the 35 mm and 40 mm layouts, but any-objective far-error
failures persist through 40 mm. Full suppression of the tested far-error cases
appears only at 45 mm.

## Decision

Run this as the offset-transition map for the 2D near/far acquisition-layout
branch. Keep broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC
claims blocked pending validation.
