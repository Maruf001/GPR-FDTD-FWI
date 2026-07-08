# BEM Experiment 833: Stage-1 Live Return Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `832` stage-1 live-return intake gate.

The validator checks source identity, expected absent-file state, six fail-closed
gate rows, zero accepted live rows, blocked downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/bem_experiments/833_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_intake_gate_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
gate count:                         6
passed gates:                       0
failed gates:                       6
live return rows:                   0
accepted stage-1 live rows:         0
stage-1 live partial file present:  false
full external input file present:   false
real BEM/FDTD comparison ready:     false
field transfer ready:               false
3D/HPC ready:                       false
```

## Interpretation

The saved intake gate validates from artifacts and remains fail-closed.

## Decision

Use this validator before accepting a stage-1 live FDTD return into the
BEM/FDTD adapter stream.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_intake_gate_validator.py
3 passed
```

Figure check:

```text
3257x892, dynamic range=255
```
