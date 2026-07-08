# Experiment 1532: Low-Side Persistence Edge Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1531` low-side persistence edge probe from artifacts.

This run checks the exact offset list, threshold maps, failure taxonomy counts,
the 44.992188 mm last-failed point below 45.0 mm, the 45.0 mm suppression
point, downstream blocked states, figure validation, and script snapshots. It
does not run new FDTD simulations, launch GPU work, transfer to field evidence,
run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1532_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validator_validation_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validator.png
scripts/
```

## Result

```text
validation checks:                   9
passed checks:                       9
failed checks:                       0
validation ready:                    true
grid models:                         90
objective rows:                      540
candidate rows:                      2160
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 last failed below 45:       44.992188 mm
far -1.6 last failed below 45:       44.992188 mm
far-error failure persists below 45: true
broad acquisition safety ready:      false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved low-side edge probe is internally consistent. Both negative far-radius
cases fail at the closest tested point below 45.0 mm, and both suppress at
45.0 mm.

## Decision

Use run `1532` as the validator for the run `1531` low-side persistence-edge
probe. Sensitivity hardening remains required before integrating this into the
claim boundary.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_low_side_persistence_edge_probe_cpu_validator.py
4 passed
```

Figure validation:

```text
3617x926, dynamic range=255
```
