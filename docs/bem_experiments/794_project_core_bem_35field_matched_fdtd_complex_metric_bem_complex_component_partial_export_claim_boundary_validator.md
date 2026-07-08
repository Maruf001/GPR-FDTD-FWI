# BEM Experiment 794: Complex-Component Partial Export Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `793` claim boundary.

The validator checks that the claim boundary keeps two guarded claims and three
blocked claims, preserves the BEM/FDTD cell counts, and does not promote the
partial BEM export to a real comparison.

## Output

```text
outputs/bem_experiments/794_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_claim_boundary_validator
```

## Result

```text
validation checks:                         7
passed checks:                             7
failed checks:                             0
claims:                                    5
guarded claims:                            2
blocked claims:                            3
partial metric rows:                       279
BEM complex value cells:                   558
FDTD value blank cells:                    558
FDTD provenance/status blank cells:        1395
partial files preflight-passed:            0
real BEM/FDTD comparison ready:            false
field transfer ready:                      false
3D/HPC ready:                              false
gpu priority:                              none
```

## Decision

Use this validator before citing run `793` as the BEM partial-export claim
boundary.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_claim_boundary_validator.py
3 passed
```

Figure check:

```text
3329x929, dynamic range=255
```
