# BEM Experiment 813: Complex FDTD Adapter Input External Handoff Guard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `812` validator with damaged versions of the run `811`
external handoff guard.

The damaged scenarios include policy-label damage, handoff-shape damage,
template disappearance, template row-count damage, false template placement
under the external return root, fake external input presence, fake external
input acceptance, comparison promotion, downstream promotion, figure damage,
and script-snapshot damage.

## Output

```text
outputs/bem_experiments/813_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_guard_validation_sensitivity
```

## Result

```text
scenarios:                         12
expected pass scenarios:           1
expected fail scenarios:           11
observed pass scenarios:           1
observed fail scenarios:           11
unexpected outcomes:               0
damaged scenarios:                 11
damaged scenarios rejected:        11
gpu priority:                      none
```

The exact saved handoff guard passes. All eleven damaged variants fail.

## Decision

Use this sensitivity run to keep the complex FDTD external handoff guard
fail-closed. Do not promote comparison from the output-local template or from a
damaged external input state.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_guard_validation_sensitivity.py

3 passed
```

Figure check:

```text
2824x875, dynamic range=255
```
