# BEM Experiment 421: Post 35-Field Synthetic Scattered Anatomy Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `420` validator with controlled damaged variants of the
run `419` claim boundary.

## Output

```text
outputs/bem_experiments/421_project_core_bem_post_35field_synthetic_scattered_anatomy_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
expected failure scenarios:        15
observed pass scenarios:           1
observed failure scenarios:        15
unexpected outcomes:               0
sensitivity ready:                 true
claims:                            22
guarded claims:                    19
blocked claims:                    3
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
```

## Decision

Use runs `419-421` as the guarded BEM post-synthetic-scattered-anatomy
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_scattered_anatomy_claim_boundary_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
