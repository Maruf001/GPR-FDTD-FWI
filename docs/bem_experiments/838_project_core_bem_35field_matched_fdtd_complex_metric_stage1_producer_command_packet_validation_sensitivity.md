# BEM Experiment 838: Stage-1 Producer Command Packet Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `837` validator by damaging the saved run `836` producer
packet in controlled ways.

The sensitivity set checks that the validator rejects wrong packet identity,
wrong schema, wrong target path, false file presence, false FDTD execution,
false acceptance, false downstream promotion, figure damage, and script
snapshot damage.

## Output

```text
outputs/bem_experiments/838_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_validation_sensitivity
```

## Result

```text
scenarios:                         22
expected passes:                    1
expected failures:                 21
observed passes:                    1
observed failures:                 21
unexpected outcomes:                0
damaged scenarios:                 21
damaged scenarios rejected:        21
gpu priority:                    none
```

The exact saved packet passes. All damaged states fail:

```text
policy label damage
packet readiness damage
source readiness damage
command row-count damage
receiver identity damage
frequency identity damage
required column-count damage
required columns damage
target path damage
partial-file presence promotion
full-file presence promotion
FDTD execution promotion
command execution promotion
acceptance-check damage
stage-1 acceptance promotion
full acceptance promotion
comparison promotion
field-transfer promotion
3D/HPC promotion
figure damage
script-snapshot damage
```

## Interpretation

The producer-packet validator accepts only the exact saved non-executed packet.
It rejects controlled damage to identity, schema, target paths, file presence,
execution, acceptance, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `836-838` as the guarded stage-1 real FDTD producer command-packet
block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_validation_sensitivity.py
8 passed
```

Figure check:

```text
3941x884, dynamic range=255
```
