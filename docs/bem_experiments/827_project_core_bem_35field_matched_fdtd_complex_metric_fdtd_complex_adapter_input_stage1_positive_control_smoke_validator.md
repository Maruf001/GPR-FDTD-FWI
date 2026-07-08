# BEM Experiment 827: Complex FDTD Adapter Input Stage-1 Positive Control Smoke Validator

Date: 2026-07-01

## Purpose

Validate the saved run `826` stage-1 positive-control smoke.

The validator checks that the synthetic stage-1 row passes row-level adapter
validation, covers only one of 279 required identities, remains output-local,
does not become accepted external input, and keeps comparison/downstream states
blocked.

## Output

```text
outputs/bem_experiments/827_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
stage-1 positive-control rows:      1
accepted stage-1 rows:              1
full required rows:                 279
synthetic positive control only:    true
full input valid:                   false
accepted as real external input:    false
real BEM/FDTD comparison ready:     false
3D/HPC ready:                       false
```

## Interpretation

The stage-1 positive control is valid as a one-row mechanics smoke only. It does
not satisfy full external input requirements.

## Decision

Do not promote full external input, completed stage files, real comparison,
field transfer, or 3D/HPC from the stage-1 positive control.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_positive_control_smoke_validator.py
```

Figure check:

```text
2717x937, dynamic range=255
```
