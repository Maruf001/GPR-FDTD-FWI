# Experiment 1481: Near/Far Source-Model Generalization Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1480` source-model generalization probe from artifacts.

This validator checks source/grid row counts, failure-taxonomy counts,
source/far threshold maps, source-effect interpretation, downstream guardrails,
figure validation, and script snapshots.

This uses saved artifacts only. It does not launch GPU work, transfer to field
evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1481_local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validator_threshold_rows.csv
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validator.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_SOURCE_MODEL_GENERALIZATION_VALIDATOR.md
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
source time-shift count:            2
grid models:                        30
objective selection rows:           180
candidate rows:                     720
all-objectives-truth models:        10
any-failure models:                 20
all-objective failure models:       10
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The source-model generalization probe validates from saved artifacts. The first
any-objective failure threshold is stable between matched `-50 ps` and `+50 ps`
source shifts, while positive time shift only softens the far-error-free
all-objective failure case.

## Decision

Use run `1481` as the validator for the 2D source-model generalization result.
Sensitivity hardening remains required before treating the source-model
validator as guarded.
