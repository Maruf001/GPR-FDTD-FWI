# BEM Experiment 408: Post-Synthetic-Fill-Smoke Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `407` BEM claim boundary from artifacts.

This run does not stage real returned FDTD files, run a real BEM/FDTD
comparison, calibrate thresholds, transfer to field evidence, launch GPU work,
or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/408_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
boundary validation ready:           true
claims:                              20
guarded claims:                      17
blocked claims:                      3
frequency rows filled:               558
frequency component cells filled:    3348
metadata fields:                     35
preflight checks:                    25
synthetic packet is evidence:        false
real comparison ready:               false
3D validation claim ready:           false
GPU/HPC ready:                       false
```

The validator confirms source identity, claim counts, the synthetic-smoke
claim row, smoke metrics, blocked downstream states, figure validation, and
script snapshots.

## Decision

Use this validator as the artifact guard for run `407`. Sensitivity hardening
remains required before closing the post-synthetic-fill-smoke boundary block.

## Validation

Focused validator test:

```text
tests/test_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3581x893, dynamic range=255
```
