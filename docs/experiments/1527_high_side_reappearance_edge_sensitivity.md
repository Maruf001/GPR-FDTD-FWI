# Experiment 1527: High-Side Reappearance Edge Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1526` high-side reappearance-edge validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `1525` artifact set
and rejects damaged variants covering policy drift, offset drift, label
collision, row-count drift, taxonomy drift, removed 45.0 mm suppression,
removed or shifted 45.015625 mm reappearance, downstream promotion, figure
drift, and script-snapshot drift.

## Output

```text
outputs/experiments/1527_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                         15
expected pass:                     1
observed pass:                     1
expected failures:                 14
observed failures:                 14
unexpected outcomes:               0
sensitivity ready:                 true
accepts exact run 1525:            true
rejects damaged variants:          true
sampled 45.0 mm suppression:       true
first reappeared far -0.8 offset:  45.015625 mm
first reappeared far -1.6 offset:  45.015625 mm
larger-offset safety claim ready:  false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Interpretation

The run `1526` validator accepts the exact run `1525` edge probe and rejects
controlled damaged variants. This guards the conclusion that the 45.0 mm point
is a narrow sampled suppression point, not a monotonic larger-offset rule.

## Decision

Use runs `1525-1527` as the guarded high-side reappearance-edge block. Do not
promote a larger-offset acquisition safety rule. Physical transfer, GPU work,
field transfer, field FWI, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3491x913, dynamic range=255
```
