# BEM Experiment 807: Complex FDTD Adapter Writer Dry Run Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `806` validator with damaged versions of the saved run
`805` writer dry run.

The damaged scenarios include fake input presence, fake adapter input rows, fake
accepted FDTD rows, changed missing-row counts, fake completed files, fake full
input validity, comparison promotion, downstream promotion, contract-hash
damage, figure damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/807_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_validation_sensitivity
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

The exact saved writer dry run passes. All fifteen damaged variants fail.

## Decision

Use this sensitivity run to keep the complex FDTD adapter writer dry run
fail-closed. Do not promote completed BEM/FDTD comparison files from absent,
partial, or damaged FDTD complex input.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_validation_sensitivity.py

3 passed
```

Figure check:

```text
3040x871, dynamic range=255
```
