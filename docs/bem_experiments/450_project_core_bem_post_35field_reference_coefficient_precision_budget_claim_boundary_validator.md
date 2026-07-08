# BEM Experiment 450: Post-Precision-Budget Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved artifacts from run `449`.

## Output

```text
outputs/bem_experiments/450_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validator.png
```

## Result

```text
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
claim-boundary validation ready:    true
claims:                             27
guarded claims:                     24
blocked claims:                     3
minimum passing significant digits: 13
recommended significant digits:     13
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The validator confirms the claim count, the precision-budget claim support
range, the 13-significant-digit requirement, nonblank figure output, script
snapshots, and blocked downstream states.

## Decision

Use this validator as the artifact guard for run `449`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary.py
tests/test_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
