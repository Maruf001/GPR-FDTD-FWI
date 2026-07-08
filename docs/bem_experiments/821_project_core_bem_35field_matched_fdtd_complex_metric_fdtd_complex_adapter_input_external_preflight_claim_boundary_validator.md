# BEM Experiment 821: Complex FDTD External Input Preflight Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `820` external input preflight claim boundary.

The validator checks claim counts, guarded preflight claims, absent-input
metrics, blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/821_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_claim_boundary_validator
```

## Result

```text
validation checks:               6
passed checks:                   6
failed checks:                   0
claims:                          5
guarded claims:                  2
blocked claims:                  3
expected rows:                   279
external input file present:     false
external input accepted:         false
finite FDTD value cells:         0
provenance/status cells:         0
completed stage files ready:     false
real BEM/FDTD comparison ready:  false
field transfer ready:            false
3D/HPC ready:                    false
gpu priority:                    none
```

## Interpretation

The saved external input preflight claim boundary validates from artifacts.

## Decision

Use this validator before treating the preflight gate as the current BEM
external-input boundary.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_claim_boundary_validator.py

3 passed
```

Figure check:

```text
2789x898, dynamic range=255
```
