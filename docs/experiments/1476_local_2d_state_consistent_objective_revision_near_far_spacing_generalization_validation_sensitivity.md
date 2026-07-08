# Experiment 1476: Near/Far Spacing Generalization Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1475` spacing-generalization validator with controlled
damaged variants.

This run checks that the validator accepts the exact run `1474` artifacts and
rejects damaged versions with source-policy drift, row-count drift,
failure-taxonomy drift, threshold drift, false downstream promotion, invalid
figure metadata, and missing script snapshots.

This is an artifact sensitivity test. It does not launch GPU work, transfer to
field evidence, run field FWI, promote a physical claim, or start 3D/HPC work.

## Output

```text
outputs/experiments/1476_local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validation_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    10
expected pass:                1
observed pass:                1
expected failures:            9
observed failures:            9
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 1474:       true
rejects damaged variants:     true
broad radius promoted:        false
physical claim ready:         false
GPU work ready:               false
field FWI ready:              false
3D/HPC ready:                 false
```

## Interpretation

The spacing-generalization validator accepts the exact run `1474` artifacts
and rejects damaged variants covering source policy drift, row-count drift,
failure-taxonomy drift, threshold drift, downstream promotion, figure
validation, and script snapshots.

## Decision

Use runs `1474-1476` as the guarded neighbor-spacing generalization block.
Broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims remain
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3293x891, dynamic range=255
```
