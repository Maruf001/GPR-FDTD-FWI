# Experiment 1525: High-Side Reappearance Edge Probe

Date: 2026-06-29

## Purpose

Refine the high-side acquisition-layout transition between the sampled 45.0 mm
suppression point and the previously observed 45.125 mm failure reappearance.

This run uses the same local 2D CPU selection pipeline as run `1519`, but
samples a narrower Tx/Rx offset grid:

```text
45.0, 45.015625, 45.03125, 45.0625, 45.09375, 45.125 mm
```

It does not launch GPU work, field transfer, field FWI, or 3D/HPC work.

## Output

```text
outputs/experiments/1525_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_summary.json
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_candidate_rows.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu.png
scripts/
```

## Result

```text
Tx/Rx offsets tested:                    6
grid models:                             90
objective-selection rows:                540
candidate rows:                          2160
all-objectives truth models:             58
any-failure models:                      32
all-objective failure models:            12
far -0.8 mm suppressed at 45.0 mm:       true
far -1.6 mm suppressed at 45.0 mm:       true
first reappeared far -0.8 mm failure:    45.015625 mm
first reappeared far -1.6 mm failure:    45.015625 mm
failure reappears above 45.0 mm:         true
elapsed time:                            3339.769 s
```

The first any-objective failure near-delta map is:

| Tx/Rx offset | Far +0.0 mm | Far -0.8 mm | Far -1.6 mm |
| --- | ---: | ---: | ---: |
| 45.0 mm | +1.5 | none | none |
| 45.015625 mm | +1.5 | +1.5 | +1.5 |
| 45.03125 mm | +1.5 | +1.5 | +1.5 |
| 45.0625 mm | +1.5 | +1.5 | +1.5 |
| 45.09375 mm | +1.5 | +1.5 | +1.5 |
| 45.125 mm | +1.5 | +1.5 | +1.5 |

## Interpretation

The high-side correction is sharper than run `1519` showed. The sampled 45.0
mm layout remains a far-error suppression point, but the suppression disappears
at the first tested offset above 45.0 mm: 45.015625 mm.

This reinforces the previous decision that 45.0 mm is not a monotonic
larger-offset safety threshold. It is a narrow sampled local point in this
synthetic selection pipeline.

## Decision

Use run `1525` as the high-side reappearance-edge probe. Do not promote a
larger-offset acquisition safety rule. Physical transfer, GPU work, field
transfer, field FWI, and 3D/HPC remain blocked pending validation and broader
evidence.

## Validation

Focused tests before execution:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu.py
3 passed
```

Figure validation:

```text
2430x1495, dynamic range=255
```
