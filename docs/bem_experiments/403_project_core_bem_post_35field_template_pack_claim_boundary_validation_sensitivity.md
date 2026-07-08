# BEM Experiment 403: Post-Template-Pack Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `402` validator with controlled damaged variants of the
run `401` claim boundary.

This run does not stage returned FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, transfer to field evidence, launch GPU work, or make a
3D validation claim.

## Output

```text
outputs/bem_experiments/403_project_core_bem_post_35field_template_pack_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                           14
expected pass:                       1
observed pass:                       1
expected failures:                   13
observed failures:                   13
unexpected outcomes:                 0
sensitivity ready:                   true
accepts exact run 401:               true
rejects damaged variants:            true
claims:                              19
template packet files:               3
metadata fields:                     35
real comparison ready:               false
3D validation claim ready:           false
GPU/HPC ready:                       false
```

The exact run `401` boundary passes. Thirteen damaged variants fail as expected
for policy-label drift, claim-count drift, template-claim drift,
template-metric drift, source-readiness drift, blocked-claim drift, downstream
promotion, figure-validation drift, and script-snapshot drift.

## Decision

Use runs `401-403` as the current guarded BEM post-template-pack claim-boundary
block. The BEM side has a validated handoff template and a guarded claim
boundary, but it still has no real returned target/background frequency files.

## Validation

Focused sensitivity test:

```text
tests/test_project_core_bem_post_35field_template_pack_claim_boundary_validation_sensitivity.py
2 passed
```

Combined focused claim-boundary tests:

```text
tests/test_project_core_bem_post_35field_template_pack_claim_boundary.py
tests/test_project_core_bem_post_35field_template_pack_claim_boundary_validator.py
tests/test_project_core_bem_post_35field_template_pack_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3581x886, dynamic range=255
```
