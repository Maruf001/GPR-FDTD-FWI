# BEM Experiment 819: Complex FDTD External Input Preflight Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `818` validator with damaged versions of the run `817`
preflight gate.

The damaged scenarios include source-readiness damage, fake external input
presence, fake schema validity, fake row/value/provenance counts, fake accepted
input, completed-stage promotion, comparison promotion, 3D promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/819_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_gate_validation_sensitivity
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected fail scenarios:           17
observed pass scenarios:           1
observed fail scenarios:           17
unexpected outcomes:               0
damaged scenarios:                 17
damaged scenarios rejected:        17
gpu priority:                      none
```

The exact saved preflight gate passes. All seventeen damaged variants fail.

## Decision

Use runs `817-819` as the guarded BEM complex FDTD external input preflight
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_gate_validation_sensitivity.py

3 passed
```

Figure check:

```text
3401x887, dynamic range=255
```
