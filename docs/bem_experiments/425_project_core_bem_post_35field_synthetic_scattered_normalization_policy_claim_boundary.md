# BEM Experiment 425: Post-35-Field Synthetic Scattered Normalization Policy Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `422-424` normalization-policy result into the BEM claim
boundary.

This is a claim-boundary update. It does not create measured evidence, run a
real BEM/FDTD comparison, launch GPU/HPC work, run 3D validation, or run field
FWI.

## Output

```text
outputs/bem_experiments/425_project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_summary.json
figures/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary.png
```

## Result

```text
claim boundary ready:              true
claims:                            23
guarded claims:                    20
blocked claims:                    3
base claims:                       22
base guarded claims:               19
base blocked claims:               3
normalization policy ready:        true
normalization sensitivity ready:   true
raw norm span ratio:               232.50000000000006
normalized coefficient mean:       0.01907878402833891
normalized coefficient cv:         2.0884850334665626e-16
normalized coefficient range:      1.0408340855860843e-17
normalization collapses scaling:   true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The new guarded claim keeps raw synthetic magnitude as a diagnostic-only
quantity and requires normalized metrics before future real comparison claims.

## Decision

Use this as the current BEM claim boundary after the synthetic scattered
normalization-policy block. Keep real comparison, 3D validation, GPU/HPC work,
field transfer, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary.py
4 passed
```

Figure check:

```text
3941x909, dynamic range=255
```
