# BEM Experiment 444: Post-Scorecard-Template Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the BEM claim boundary from run `443`.

## Output

```text
outputs/bem_experiments/444_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validator.png
```

## Result

```text
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
claim-boundary validation ready:    true
claims:                             26
guarded claims:                     23
blocked claims:                     3
scorecard template ready:           true
template rows:                      279
required real input cells:          1116
real return values present:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The validator confirms the scorecard-template claim is present, supports runs
`440-442`, preserves the non-evidence wording, and leaves the three downstream
claims blocked.

## Decision

Use this validator as the artifact guard for run `443`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary.py
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
