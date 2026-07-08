# BEM Experiment 366: Real-Pair Post Acceptance Gate Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `365` BEM post-acceptance claim boundary from artifacts.

## Output

```text
outputs/bem_experiments/366_project_core_bem_real_pair_post_acceptance_gate_claim_boundary_validator
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
claims:                         12
guarded claims:                 9
blocked claims:                 3
missing packet items:           34
missing projected traces:       26
missing metadata/control:       8
real comparison ready:          false
threshold calibration ready:    false
GPU work ready:                 false
field transfer ready:           false
3D validation ready:            false
```

## Decision

Use run `366` as the validator for the run `365` BEM post-acceptance claim
boundary.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_post_acceptance_gate_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3581x929, dynamic range=255
```
