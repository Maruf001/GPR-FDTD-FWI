# BEM Experiment 420: Post 35-Field Synthetic Scattered Anatomy Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `419` from saved artifacts.

## Output

```text
outputs/bem_experiments/420_project_core_bem_post_35field_synthetic_scattered_anatomy_claim_boundary_validator
```

## Result

```text
validation checks:                 6
passed checks:                     6
failed checks:                     0
validation ready:                  true
claims:                            22
guarded claims:                    19
blocked claims:                    3
dominant component:                ez
peak receiver index:               30
peak frequency:                    3.0 GHz
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
```

## Decision

Use this as the artifact validator for run `419`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_scattered_anatomy_claim_boundary_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x840, dynamic range=255
```
