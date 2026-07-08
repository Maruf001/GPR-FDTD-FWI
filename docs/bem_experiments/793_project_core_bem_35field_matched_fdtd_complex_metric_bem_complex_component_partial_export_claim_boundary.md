# BEM Experiment 793: Complex-Component Partial Export Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the BEM-side complex-component export from run
`790` and its hardening runs `791-792`.

The BEM side now has finite complex `scattered_ey` values for all required
receiver-frequency rows. The packet remains partial because the matched FDTD
complex values and FDTD provenance/status fields are still blank.

## Output

```text
outputs/bem_experiments/793_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_claim_boundary
```

## Result

```text
source export ready:                         true
source validation ready:                     true
source sensitivity ready:                    true
claims:                                     5
guarded claims:                             2
blocked claims:                             3
frequency solves ready:                     9
partial stage files:                        5
partial metric rows:                        279
finite BEM complex rows:                    279
BEM complex value cells:                    558
FDTD value blank cells:                     558
FDTD provenance/status blank cells:         1395
real FDTD exported flags true:              0
partial files preflight-passed:             0
real BEM/FDTD comparison ready:             false
field transfer ready:                       false
3D/HPC ready:                               false
gpu priority:                               none
```

## Decision

Use run `790` as BEM-side complex-component evidence only. Do not cite it as
real BEM/FDTD agreement, detector evidence, inversion evidence, field transfer,
or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_bem_complex_component_partial_export_claim_boundary.py
3 passed
```

Figure check:

```text
3473x956, dynamic range=255
```
