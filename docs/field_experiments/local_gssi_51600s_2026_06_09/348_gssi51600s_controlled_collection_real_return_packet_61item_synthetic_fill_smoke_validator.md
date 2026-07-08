# Field Experiment 348: 61-Item Synthetic Fill Smoke Validator

Date: 2026-06-29

## Purpose

Validate the saved run `347` synthetic-fill smoke from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/348_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_fill_smoke_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
packet requirements:                 61
unique return paths:                 49
synthetic packet files:              49
synthetic packet items present:      61
synthetic ready gates:               8
synthetic blocked gates:             1
synthetic packet is measured:        false
real packet files present:           false
field evidence ready:                false
```

The validator confirms synthetic-file inventory, packet-item coverage, closed
action groups, non-evidence status, figure validation, and script snapshots.

## Validation

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_fill_smoke_validator.py
2 passed
```

Figure validation:

```text
3509x898, dynamic range=255
```
