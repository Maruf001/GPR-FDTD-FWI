# Field Experiment 632: First-Return Operator Packet Validator

Date: 2026-07-01

## Purpose

Validate run `631` from saved artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/632_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_operator_packet_validator
```

## Result

```text
validation checks:                5
passed checks:                    5
failed checks:                    0
operator file instructions:       18
unique pairs:                     9
missing file instructions:        18
parent directories ready:         18
ready for acceptance recheck:     0
```

## Decision

Use run `632` as the consumer-facing guard for citing the operator packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_operator_packet_validator.py
3 passed
```

Figure check:

```text
1997x780, dynamic range=255
```
