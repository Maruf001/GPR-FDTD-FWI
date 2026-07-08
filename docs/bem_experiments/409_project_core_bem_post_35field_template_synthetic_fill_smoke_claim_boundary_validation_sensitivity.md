# BEM Experiment 409: Post-Synthetic-Fill-Smoke Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `408` validator with controlled damaged variants of the
run `407` claim boundary.

This run does not stage real returned FDTD files, run a real BEM/FDTD
comparison, calibrate thresholds, transfer to field evidence, launch GPU work,
or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/409_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_validation_sensitivity
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
accepts exact run 407:               true
rejects damaged variants:            true
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

The exact run `407` boundary passes. Thirteen damaged variants fail as expected
for source-label drift, claim-count drift, synthetic-claim drift, smoke-metric
drift, false evidence promotion, blocked-row drift, downstream promotion,
figure-validation drift, and script-snapshot drift.

## Decision

Use runs `407-409` as the current guarded BEM
post-synthetic-fill-smoke claim-boundary block.

## Validation

Focused sensitivity test:

```text
tests/test_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_validation_sensitivity.py
2 passed
```

Combined focused claim-boundary tests:

```text
tests/test_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary.py
tests/test_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_validator.py
tests/test_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_validation_sensitivity.py
6 passed
```

Figure validation:

```text
3581x877, dynamic range=255
```
