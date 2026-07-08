# Experiment 1519: Acquisition-Layout High-Side Stability Probe

Date: 2026-06-29

## Purpose

Directly test whether the run `1513` far-error suppression at `45.0 mm`
Tx/Rx offset remains stable for slightly larger Tx/Rx offsets.

The probe repeats the same CPU objective-selection pipeline at five high-side
offsets:

```text
45.0, 45.125, 45.25, 45.5, 46.0 mm
```

It does not run GPU work, field FWI, field transfer, neural-network training,
or 3D/HPC work.

## Output

```text
outputs/experiments/1519_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_summary.json
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu_candidate_rows.csv
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu.png
scripts/
```

## Result

```text
Tx/Rx offsets tested:                     5
grid models:                              75
objective rows:                           450
candidate rows:                           1800
all-objectives truth models:              49
any-failure models:                       26
all-objective failure models:             10
first sampled suppression, far -0.8 mm:   45.0 mm
first sampled suppression, far -1.6 mm:   45.0 mm
runtime:                                  2809.348 s
high-side probe ready:                    true
physical claim ready:                     false
GPU work ready:                           false
field transfer ready:                     false
field FWI ready:                          false
3D/HPC ready:                             false
```

The first any-objective failure thresholds were:

| Tx/Rx offset | far +0.0 mm | far -0.8 mm | far -1.6 mm |
| ---: | ---: | ---: | ---: |
| 45.0 mm | near +1.5 mm | none | none |
| 45.125 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |
| 45.25 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |
| 45.5 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |
| 46.0 mm | near +1.5 mm | near +1.5 mm | near +1.5 mm |

## Interpretation

The result preserves the directly sampled `45.0 mm` suppression point, but it
does not show high-side stability. The negative far-radius cases that were
fully suppressed at `45.0 mm` reappear as partial failures at `45.125 mm` and
remain present at `45.25`, `45.5`, and `46.0 mm`.

This means the acquisition-layout behavior is non-monotonic in the tested
local synthetic pipeline. The current evidence supports a narrow sampled
`45.0 mm` point, not a rule that larger Tx/Rx offsets are generally safer.

## Decision

Use this run as a high-side correction to the local 2D acquisition-layout
transition block. Keep broad physical, GPU, field-transfer, field-FWI, and
3D/HPC claims blocked. The next required step is an artifact validator that
checks both the `45.0 mm` suppression point and the reappearance of failures
above `45.0 mm`.

## Validation

Focused test before execution:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_stability_probe_cpu.py
3 passed
```

Figure validation:

```text
2430x1495, dynamic range=255
```
