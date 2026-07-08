# BEM Experiment 800: Complex-Metric FDTD Complex Adapter Contract Spec Validator

Date: 2026-07-01

## Purpose

Validate the saved run `799` complex FDTD adapter contract.

The validator checks the adapter input columns, completed-stage output columns,
mapping steps, guards, packet fill counts, and blocked execution/comparison
states.

## Output

```text
outputs/bem_experiments/800_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_contract_spec_validator
```

## Result

```text
validation checks:                         7
passed checks:                             7
failed checks:                             0
adapter input required columns:            12
completed stage output fill columns:       11
mapping steps:                             5
guards:                                    8
partial stage files:                       5
partial metric rows:                       279
FDTD complex value cells required:         558
FDTD provenance/status cells required:     1395
complex FDTD adapter contract ready:       true
adapter implementation ready:              false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
3D/HPC ready:                              false
gpu priority:                              none
```

## Decision

Use this validator before implementing the complex FDTD adapter contract.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_contract_spec_validator.py
3 passed
```

Figure check:

```text
3365x929, dynamic range=255
```
