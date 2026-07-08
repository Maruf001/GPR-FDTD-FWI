# Experiment 1475: Near/Far Spacing Generalization Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1474` neighbor-spacing generalization probe from
artifacts.

This run confirms the source counts, failure taxonomy, spacing-dependent
threshold maps, blocked downstream states, figure validation, and script
snapshots.

This is an artifact validator. It does not launch GPU work, transfer to field
evidence, run field FWI, promote a physical claim, or start 3D/HPC work.

## Output

```text
outputs/experiments/1475_local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validator_thresholds.csv
data/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
grid models:                        45
objective rows:                     270
candidate rows:                     1080
all-objectives-truth models:        23
any-failure models:                 22
all-objective failure models:       12
broad radius promoted:              false
physical claim ready:               false
GPU work ready:                     false
field FWI ready:                    false
3D/HPC ready:                       false
```

Validated thresholds:

| Neighbor spacing | Far delta | First any failure | First all-objective failure |
| --- | ---: | ---: | ---: |
| 10 mm narrower | +0.0 mm | +1.5 mm | none |
| 10 mm narrower | -0.8 mm | +0.5 mm | +1.5 mm |
| 10 mm narrower | -1.6 mm | +0.5 mm | +1.5 mm |
| baseline | +0.0 mm | +1.5 mm | +1.5 mm |
| baseline | -0.8 mm | +0.5 mm | +1.5 mm |
| baseline | -1.6 mm | +0.5 mm | +1.5 mm |
| 10 mm wider | +0.0 mm | +1.5 mm | +1.5 mm |
| 10 mm wider | -0.8 mm | none | none |
| 10 mm wider | -1.6 mm | none | none |

## Interpretation

The saved run `1474` spacing-generalization result is internally consistent.
The failure thresholds confirm that wider neighbor spacing suppresses
far-error-driven failures in the tested grid, while narrower and baseline
spacing keep far-error partial failures active.

## Decision

Use runs `1474-1475` as the guarded neighbor-spacing generalization block.
Keep broad radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_spacing_generalization_validator.py
4 passed
```

Figure validation:

```text
3581x931, dynamic range=255
```
