# Field Experiment 602: Collection-Day Execution Packet Validator

Date: 2026-07-01

## Purpose

Validate the saved run `601` collection-day execution packet.

The validator checks source identity, slot and template counts, six action
groups, zero live-file state, zero accepted action groups, blocked downstream
states, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/602_gssi51600s_controlled_collection_trace_pairing_collection_day_execution_packet_validator
```

## Result

```text
validation checks:                7
passed checks:                    7
failed checks:                    0
total return slots:              33
metadata templates total:        24
measured DZT files required:      9
required live return files:      18
action groups:                    6
live measured DZT files:          0
live paired metadata files:       0
accepted action groups:           0
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
```

## Interpretation

The saved collection-day execution packet validates from artifacts.

## Decision

Use this validator before treating the collection-day packet as the current
field checklist.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_validator.py
3 passed
```

Figure check:

```text
3221x895, dynamic range=255
```
