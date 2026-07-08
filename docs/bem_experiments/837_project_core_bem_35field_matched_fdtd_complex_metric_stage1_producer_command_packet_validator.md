# BEM Experiment 837: Stage-1 Producer Command Packet Validator

Date: 2026-07-01

## Purpose

Validate the saved run `836` producer command packet from its written artifacts.

This validator checks that the packet still names exactly one stage-1
receiver-frequency pair, uses the 12-column complex adapter schema, targets the
expected partial-return path, remains non-executed, and does not promote real
BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/837_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_validator
```

## Result

```text
validation checks:                 8
passed checks:                     8
failed checks:                     0
producer command rows:             1
packet acceptance checks:          6
receiver index:                   15
frequency:                         1.0 GHz
required columns:                 12
stage-1 partial file present:      false
full external input present:       false
FDTD executed now:                 false
executed command count:            0
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Interpretation

The saved stage-1 producer command packet is stable and remains non-executed.
It is a request packet for one real FDTD row, not evidence that FDTD has run.

## Decision

Use this validator before accepting changes to the first real FDTD producer
packet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_validator.py
5 passed
```

Figure check:

```text
3257x893, dynamic range=255
```
