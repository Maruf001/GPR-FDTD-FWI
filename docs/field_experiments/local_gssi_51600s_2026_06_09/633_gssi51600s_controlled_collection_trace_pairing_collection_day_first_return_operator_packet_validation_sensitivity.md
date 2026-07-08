# Field Experiment 633: First-Return Operator Packet Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `632` validator.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/633_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_operator_packet_validation_sensitivity
```

## Result

```text
source validator ready:       true
scenarios:                    16
expected pass scenarios:      1
expected fail scenarios:      15
observed pass scenarios:      1
observed fail scenarios:      15
unexpected outcomes:          0
damaged scenarios rejected:   15
```

Damaged states include row/count drift, false file presence, parent-directory
damage, false recheck readiness, command damage, field-evidence/FWI/3D
promotion, GPU-priority promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `631-633` as the guarded first-return operator-packet block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_operator_packet_validation_sensitivity.py
3 passed
```

Figure check:

```text
2789x849, dynamic range=255
```
