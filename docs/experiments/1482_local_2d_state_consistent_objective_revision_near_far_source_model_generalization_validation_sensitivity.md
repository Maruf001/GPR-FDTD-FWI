# Experiment 1482: Near/Far Source-Model Generalization Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1481` source-model generalization validator with
controlled damaged variants.

This run verifies that the validator accepts the exact run `1480` source-model
result and rejects controlled damage to source counts, grid counts, result row
counts, failure taxonomy, threshold maps, downstream guardrails, figure
validation, and script snapshots.

This uses saved artifacts only. It does not launch GPU work, transfer to field
evidence, run field FWI, promote a physical claim, or start 3D/HPC work.

## Output

```text
outputs/experiments/1482_local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validation_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_source_model_generalization_validation_sensitivity.png
scripts/script_snapshot_manifest.json
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_SOURCE_MODEL_GENERALIZATION_VALIDATION_SENSITIVITY.md
```

## Result

```text
scenarios:                    11
expected pass:                1
observed pass:                1
expected failures:            10
observed failures:            10
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 1480:       true
rejects damaged variants:     true
broad radius promoted:        false
physical claim ready:         false
GPU work ready:               false
field transfer ready:         false
field FWI ready:              false
3D/HPC ready:                 false
```

## Interpretation

The run `1481` validator accepts the exact run `1480` source-model result and
rejects controlled damaged variants for source/count drift, row-count drift,
taxonomy drift, threshold drift, downstream promotion, figure validation drift,
and script-snapshot drift.

## Decision

Use runs `1480-1482` as the guarded 2D source-model generalization block. Keep
broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked until
the remaining acquisition-layout axis is executed and validated.
