# BEM Experiment 822: Complex FDTD External Input Preflight Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `821` validator with damaged versions of the run `820`
claim boundary.

The damaged scenarios include claim-count drift, missing guarded claims, fake
external input presence, fake accepted input, fake value/provenance counts,
comparison promotion, 3D promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/822_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
expected fail scenarios:           15
observed pass scenarios:           1
observed fail scenarios:           15
unexpected outcomes:               0
damaged scenarios:                 15
damaged scenarios rejected:        15
gpu priority:                      none
```

The exact saved boundary passes. All fifteen damaged variants fail.

## Decision

Use runs `820-822` as the guarded BEM external input preflight claim-boundary
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_claim_boundary_validation_sensitivity.py

3 passed
```

Figure check:

```text
3131x886, dynamic range=255
```
