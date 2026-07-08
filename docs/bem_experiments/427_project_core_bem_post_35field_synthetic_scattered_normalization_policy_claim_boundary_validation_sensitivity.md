# BEM Experiment 427: Post-35-Field Synthetic Scattered Normalization Policy Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `426` validator with controlled damaged variants of the
run `425` claim boundary.

## Output

```text
outputs/bem_experiments/427_project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         19
expected pass scenarios:           1
expected failure scenarios:        18
observed pass scenarios:           1
observed failure scenarios:        18
unexpected outcomes:               0
claim-boundary sensitivity ready:  true
validator accepts exact run 425:   true
validator rejects damaged variants:true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `425` boundary and rejects controlled
damage to claim counts, normalization readiness, metric spread, evidence text,
blocked rows, downstream state, figure validation, and script snapshots.

## Decision

Use runs `425-427` as the guarded BEM post-normalization-policy claim-boundary
block. Keep real BEM/FDTD comparison, 3D validation, GPU/HPC work, field
transfer, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_scattered_normalization_policy_claim_boundary_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x887, dynamic range=255
```
