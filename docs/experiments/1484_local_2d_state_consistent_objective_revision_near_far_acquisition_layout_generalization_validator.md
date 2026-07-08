# Experiment 1484: Near/Far Acquisition-Layout Generalization Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1483` acquisition-layout generalization probe from
artifacts.

This validator checks Tx/Rx offset/grid row counts, failure-taxonomy counts,
acquisition/far threshold maps, acquisition-effect interpretation, downstream
guardrails, figure validation, and script snapshots.

This uses saved artifacts only. It does not launch GPU work, transfer to field
evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1484_local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_acquisition_layout_generalization_validator.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_ACQUISITION_LAYOUT_GENERALIZATION_VALIDATOR.md
```

## Result

```text
validation checks:                       8
passed checks:                           8
failed checks:                           0
validation ready:                        true
Tx/Rx offset count:                      2
grid models:                             30
objective selection rows:                180
candidate rows:                          720
all-objectives-truth models:             18
any-failure models:                      12
all-objective failure models:            8
physical claim ready:                    false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
3D/HPC ready:                            false
```

## Interpretation

The acquisition-layout generalization probe validates from saved artifacts. The
45 mm Tx/Rx layout suppresses the far-error-driven failures seen at 20 mm in
this tested grid, while far-error-free near-radius failures remain.

## Decision

Use run `1484` as the validator for the 2D acquisition-layout generalization
result. Sensitivity hardening remains required before integrating this with the
full near/far claim boundary.
