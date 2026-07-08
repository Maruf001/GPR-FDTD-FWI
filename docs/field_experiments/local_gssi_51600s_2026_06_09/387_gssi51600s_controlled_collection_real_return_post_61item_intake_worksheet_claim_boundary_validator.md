# Field Experiment 387: Post-Intake-Worksheet Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the field claim boundary from run `386`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/387_gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validator.png
```

## Result

```text
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
claim-boundary validation ready:    true
claims:                             22
guarded claims:                     18
blocked claims:                     4
worksheet rows:                     49
direct real-input rows:             33
generated follow-up rows:           16
blank completion cells:             294
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The validator confirms that the intake-worksheet claim supports runs `383-385`,
preserves the blank-completion-cell evidence, and keeps the four downstream
claims blocked.

## Decision

Use this validator as the artifact guard for run `386`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
