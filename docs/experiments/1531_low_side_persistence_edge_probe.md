# Experiment 1531: Low-Side Persistence Edge Probe

Date: 2026-06-29

## Purpose

Refine the acquisition-layout transition immediately below the sampled 45.0 mm
Tx/Rx offset.

The previous high-side edge block showed that the 45.0 mm point is not a
monotonic larger-offset safety rule: negative far-radius failures reappear at
45.015625 mm. This run asks the complementary low-side question:

```text
How close below 45.0 mm do the negative far-radius failures persist?
```

This is a CPU run. It does not launch GPU work, transfer to field evidence, run
field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1531_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_summary.json
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_candidate_rows.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu.png
scripts/
```

## Result

```text
Tx/Rx offsets tested:                   44.875, 44.9375, 44.96875, 44.984375, 44.9921875, 45.0 mm
grid models:                            90
objective rows:                         540
candidate rows:                         2160
all-objectives truth models:            58
any-failure models:                     32
all-objective failure models:           12
far -0.8 first suppression:             45.0 mm
far -1.6 first suppression:             45.0 mm
far -0.8 last failed point below 45:     44.992188 mm
far -1.6 last failed point below 45:     44.992188 mm
far-error failure persists below 45:     true
physical claim ready:                   false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
elapsed CPU time:                       3335.75 s
```

## Interpretation

The failure transition is extremely sharp on both sides of 45.0 mm. The nearest
tested point below 45.0 mm, labeled `44.992188` mm after label rounding, still
fails for both negative far-radius cases. The 45.0 mm point suppresses both of
those failures.

Together with the high-side edge probe, this makes 45.0 mm a narrow sampled
suppression point rather than a broad safe acquisition rule.

## Decision

Use run `1531` as the low-side persistence-edge probe for the local 2D
acquisition-layout transition. Keep broad physical, GPU, field-transfer,
field-FWI, and 3D/HPC claims blocked pending validation.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu.py
3 passed
```

Figure validation:

```text
2430x1495, dynamic range=255
```
