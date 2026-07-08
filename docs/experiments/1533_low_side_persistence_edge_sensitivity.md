# Experiment 1533: Low-Side Persistence Edge Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1532` validator for the saved run `1531` low-side
persistence edge probe.

This run checks that the validator accepts the exact run `1531` artifacts and
rejects controlled damaged variants for offset drift, label collision,
row-count drift, failure-taxonomy drift, low-side failure removal, 45.0 mm
suppression removal, downstream promotion, figure drift, and script-snapshot
drift.

## Output

```text
outputs/experiments/1533_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validation_sensitivity.png
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
accepts exact run 1531:            true
rejects damaged variants:          true
last failed far -0.8 below 45:     44.992188 mm
last failed far -1.6 below 45:     44.992188 mm
broad acquisition safety ready:    false
GPU work ready:                    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Interpretation

The run `1532` validator accepts the exact run `1531` low-side edge result and
rejects controlled damaged variants. This protects the conclusion that failure
persists at the nearest tested point below 45.0 mm and suppresses at 45.0 mm.

## Decision

Use runs `1531-1533` as the guarded low-side persistence-edge block. Keep broad
physical, GPU, field-transfer, field-FWI, and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3491x914, dynamic range=255
```
