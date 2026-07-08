# Field Experiment 631: First-Return Operator Packet

Date: 2026-07-01

## Purpose

Convert the run `628` first-return unblock action matrix into an operator-facing
file placement packet with one row per required live file.

This does not accept field data, run FWI, or promote 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/631_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_operator_packet
```

## Result

```text
operator file instructions:       18
unique pairs:                     9
DZT instructions:                 9
metadata JSON instructions:       9
missing file instructions:        18
parent directories ready:         18
ready for acceptance recheck:     0
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
```

## Decision

Use this as an operator-facing file placement packet only. Rerun the
first-return acceptance gate after all 18 files arrive.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_operator_packet.py
3 passed
```

Figure check:

```text
1672x774, dynamic range=255
```
