# BEM Experiment 426: Post-35-Field Synthetic Scattered Normalization Policy Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `425` from saved artifacts.

The validator checks claim counts, the inserted normalization-policy claim,
normalization metrics, blocked downstream rows, figure validation, and script
snapshots.

## Output

```text
outputs/bem_experiments/426_project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
passed checks:                     5
failed checks:                     0
claim-boundary validation ready:   true
claims:                            23
guarded claims:                    20
blocked claims:                    3
raw norm span ratio:               232.50000000000006
normalized coefficient cv:         2.0884850334665626e-16
normalized coefficient range:      1.0408340855860843e-17
normalization collapses scaling:   true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this validator as the artifact guard for run `425`. Sensitivity testing
remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x840, dynamic range=255
```
