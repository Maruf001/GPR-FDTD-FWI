# BEM Experiment 402: Post-Template-Pack Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `401` BEM claim boundary from artifacts.

This run does not stage returned FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, transfer to field evidence, launch GPU work, or make a
3D validation claim.

## Output

```text
outputs/bem_experiments/402_project_core_bem_post_35field_template_pack_claim_boundary_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
boundary validation ready:           true
claims:                              19
guarded claims:                      16
blocked claims:                      3
template packet files:               3
rows per frequency file:             279
blank frequency component cells:     3348
metadata fields:                     35
real comparison ready:               false
3D validation claim ready:           false
field FWI ready:                     false
GPU/HPC ready:                       false
```

The validator confirms source identity, claim counts, the template-pack claim
row, template metrics, blocked downstream states, figure validation, and script
snapshots.

## Decision

Use this validator as the artifact guard for run `401`. Sensitivity hardening
remains required before closing the post-template-pack boundary block.

## Validation

Focused validator test:

```text
tests/test_project_core_bem_post_35field_template_pack_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3581x893, dynamic range=255
```
