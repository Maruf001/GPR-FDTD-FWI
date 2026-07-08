# BEM Experiment 795: Complex-Component Partial Export Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `794` validator with damaged versions of the saved run
`793` claim boundary.

The damaged scenarios include claim-count damage, guarded/blocked row damage,
BEM value-count damage, FDTD blank-count damage, fake preflight promotion, fake
BEM/FDTD comparison promotion, downstream promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/bem_experiments/795_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                         15
expected pass scenarios:           1
expected fail scenarios:           14
observed pass scenarios:           1
observed fail scenarios:           14
unexpected outcomes:               0
damaged scenarios:                 14
damaged scenarios rejected:        14
gpu priority:                      none
```

The exact saved claim boundary passes. All fourteen damaged variants fail.

## Decision

Use this sensitivity run to guard against treating the BEM partial export as
real BEM/FDTD comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
2860x855, dynamic range=255
```
