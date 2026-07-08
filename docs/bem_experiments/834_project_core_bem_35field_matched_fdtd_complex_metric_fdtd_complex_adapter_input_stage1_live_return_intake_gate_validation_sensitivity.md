# BEM Experiment 834: Stage-1 Live Return Intake Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `833` validator with damaged versions of the run `832`
stage-1 live-return intake gate.

Damaged cases include policy-label damage, gate-readiness damage, source-
readiness damage, expected-row-count damage, required-column-count damage,
partial-file and full-file presence promotion, gate-count damage, passed-gate
promotion, live-row-count promotion, schema promotion, value/provenance
promotion, acceptance promotion, merge promotion, comparison promotion,
field-transfer promotion, 3D promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/bem_experiments/834_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_intake_gate_validation_sensitivity
```

## Result

```text
scenarios:                    20
expected pass scenarios:       1
expected fail scenarios:      19
observed pass scenarios:       1
observed fail scenarios:      19
unexpected outcomes:           0
damaged scenarios:            19
damaged scenarios rejected:   19
gpu priority:                 none
```

## Interpretation

The validator fails closed. The exact saved absent-file intake state passes,
while all damaged or falsely promoted variants fail.

## Decision

Use runs `832-834` as the guarded stage-1 live FDTD return intake block. Do not
merge values into the full 279-row external input or compare BEM and FDTD until
a real stage-1 partial return passes the intake gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_intake_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3653x885, dynamic range=255
```
