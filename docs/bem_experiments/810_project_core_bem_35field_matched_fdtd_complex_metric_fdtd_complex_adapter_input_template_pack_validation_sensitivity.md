# BEM Experiment 810: Complex FDTD Adapter Input Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `809` validator with damaged versions of the run `808`
input template packet.

The damaged scenarios include schema damage, row-count damage, stage-shape
damage, contract-hash damage, filled FDTD value blanks, filled FDTD provenance
blanks, evidence promotion, comparison promotion, downstream promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/810_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_validation_sensitivity
```

## Result

```text
scenarios:                         13
expected pass scenarios:           1
expected fail scenarios:           12
observed pass scenarios:           1
observed fail scenarios:           12
unexpected outcomes:               0
damaged scenarios:                 12
damaged scenarios rejected:        12
gpu priority:                      none
```

The exact saved template packet passes. All twelve damaged variants fail.

## Decision

Use this sensitivity run to keep the FDTD complex-input template fail-closed.
The template remains a fill-in packet only; it is not evidence until real FDTD
complex values and provenance pass validation.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_validation_sensitivity.py

3 passed
```

Figure check:

```text
2896x877, dynamic range=255
```
