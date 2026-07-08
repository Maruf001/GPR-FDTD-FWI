# Experiment 1526: High-Side Reappearance Edge Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1525` high-side reappearance-edge probe from artifacts.

This run checks the source identity, row counts, threshold maps, 45.0 mm
suppression point, 45.015625 mm reappearance point, downstream guardrails,
figure output, and script snapshots.

## Output

```text
outputs/experiments/1526_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validator_validation_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validator.png
scripts/
```

## Result

```text
validation checks:                     9
passed checks:                         9
failed checks:                         0
edge validation ready:                 true
Tx/Rx offsets tested:                  6
grid models:                           90
objective-selection rows:              540
candidate rows:                        2160
all-objectives truth models:           58
any-failure models:                    32
all-objective failure models:          12
first suppressed far -0.8 mm offset:   45.0 mm
first suppressed far -1.6 mm offset:   45.0 mm
first reappeared far -0.8 mm offset:   45.015625 mm
first reappeared far -1.6 mm offset:   45.015625 mm
monotonic larger-offset safety ready:  false
physical claim ready:                  false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

## Interpretation

The run `1525` edge result is internally consistent. The 45.0 mm point remains
a sampled far-error suppression point, but the suppression disappears at the
first tested offset above it: 45.015625 mm.

## Decision

Use run `1526` as the validator for run `1525`. Do not promote a monotonic
larger-offset safety rule. Physical transfer, GPU work, field transfer, field
FWI, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_high_side_reappearance_edge_probe_cpu_validator.py
4 passed
```

Figure validation:

```text
3617x932, dynamic range=255
```
