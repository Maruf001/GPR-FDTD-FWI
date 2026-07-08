# BEM Experiment 832: Stage-1 Live Return Intake Gate

Date: 2026-07-01

## Purpose

Define the intake gate for the one-row live FDTD return specified by run `829`.

The gate checks file presence, required columns, one-row shape, receiver and
frequency identity, finite real/imaginary FDTD values, solver provenance,
solver completion, real-export status, and input-contract hash identity.

## Output

```text
outputs/bem_experiments/832_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_intake_gate
```

## Result

```text
source contract ready:              true
source sensitivity ready:           true
expected stage-1 rows:              1
required columns:                   12
stage-1 live partial file present:  false
full external input file present:   false
gate count:                         6
passed gates:                       0
failed gates:                       6
live return rows:                   0
accepted stage-1 live rows:         0
can merge into full input:          false
accepted as full external input:    false
real BEM/FDTD comparison ready:     false
field transfer ready:               false
3D/HPC ready:                       false
```

## Interpretation

The stage-1 live-return intake gate is now executable. The expected one-row
live FDTD partial file is absent, so the gate accepts zero rows and does not
promote comparison evidence.

## Decision

Wait for the real stage-1 FDTD partial return before merging any value into the
full 279-row external input or comparing BEM and FDTD.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_intake_gate.py
3 passed
```

Figure check:

```text
3329x890, dynamic range=255
```
