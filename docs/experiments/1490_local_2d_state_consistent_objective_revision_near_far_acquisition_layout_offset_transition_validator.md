# Experiment 1490: Near/Far Acquisition-Layout Offset-Transition Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1489` acquisition-layout offset-transition result from
artifacts.

Run `1489` expanded the Tx/Rx offset axis to 20, 30, 35, 40, and 45 mm. This
validator checks that the saved result has the expected run identity, row
counts, failure taxonomy, threshold maps, blocked downstream states, figure
validation, and script snapshots.

This is CPU-only artifact validation. It does not launch GPU work, transfer to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1490_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                       8
passed checks:                           8
failed checks:                           0
validation ready:                        true
Tx/Rx offsets mm:                        [20.0, 30.0, 35.0, 40.0, 45.0]
grid models:                             75
objective selection rows:                450
candidate rows:                          1800
all-objectives-truth models:             45
any-failure models:                      30
all-objective failure models:            18
first suppressed far -0.8 offset mm:     45.0
first suppressed far -1.6 offset mm:     45.0
figure size:                             3581x931
figure dynamic range:                    255
```

## Interpretation

The offset-transition result validates from saved artifacts. In the tested
grid, all-objective far-error failures disappear by 35 mm, while any-objective
far-error failures persist through 40 mm and are first fully suppressed at
45 mm.

## Decision

Use run `1490` as the validator for the run `1489` offset-transition map.
Sensitivity hardening is still required before folding this result into the
local near/far claim boundary.
