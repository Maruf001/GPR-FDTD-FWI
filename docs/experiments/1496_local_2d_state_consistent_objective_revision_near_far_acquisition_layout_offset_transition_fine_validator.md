# Experiment 1496: Near/Far Acquisition-Layout Offset Transition Fine Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1495` fine offset-transition probe from artifacts.

This run checks the row counts, threshold maps, suppressed-offset values, figure
validation, script snapshots, and downstream guardrails for the 40-45 mm fine
Tx/Rx offset sweep.

This is CPU-only validation hardening. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1496_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                       8
passed checks:                           8
failed checks:                           0
fine validation ready:                   true
Tx/Rx offsets mm:                        [40, 41, 42, 43, 44, 45]
Tx/Rx offset count:                      6
grid models:                             90
objective selection rows:                540
candidate rows:                          2160
all-objectives-truth models:             58
any-failure models:                      32
all-objective failure models:            12
first suppressed far -0.8 offset mm:     45.0
first suppressed far -1.6 offset mm:     45.0
physical claim ready:                    false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
3D/HPC ready:                            false
figure size:                             3581x931
figure dynamic range:                    255
```

The eight checks all passed:

| Check | Passed |
| --- | --- |
| source policy and counts | yes |
| failure taxonomy counts | yes |
| first any-failure thresholds stable | yes |
| first all-objective failure thresholds stable | yes |
| acquisition-effect interpretation stable | yes |
| downstream states blocked | yes |
| figure validation present | yes |
| script snapshots present | yes |

## Interpretation

The fine offset-transition probe validates from saved artifacts. In this tested
grid, any-objective far-error failures persist through 44 mm and are first fully
suppressed at 45 mm, while all-objective far-error failures are absent across
the 40-45 mm fine sweep.

## Decision

Use run `1496` as the validator for the 2D acquisition-layout fine
offset-transition map. Sensitivity hardening remains required before updating
the local near/far claim boundary.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_offset_transition_fine_validator.py
4 passed
```
