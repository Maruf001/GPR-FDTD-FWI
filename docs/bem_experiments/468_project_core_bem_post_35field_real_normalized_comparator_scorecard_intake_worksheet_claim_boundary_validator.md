# BEM Experiment 468: Post-Scorecard Intake Worksheet Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the run `467` BEM claim boundary from saved artifacts.

## Output

```text
outputs/bem_experiments/468_project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation passes:                           5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      30
guarded claims:                              27
blocked claims:                              3
worksheet rows:                              279
required real-return cells:                  1116
filled real-return cells:                    0
missing real-return cells:                   1116
hash requirements:                           558
norm requirements:                           558
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Decision

Use this validator as the artifact guard for run `467`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
