# Field Experiment 601: Collection-Day Execution Packet

Date: 2026-07-01

## Purpose

Assemble the controlled collection-day execution packet from the guarded
manifest, preparable metadata templates, and paired metadata templates.

This run combines the full set of 24 metadata templates with the nine measured
DZT file requirements and turns them into six collection-day action groups.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/601_gssi51600s_controlled_collection_trace_pairing_collection_day_execution_packet
```

## Result

```text
total return slots:                 33
preparable metadata templates:      15
paired metadata templates:           9
measured DZT files required:         9
metadata templates total:           24
live collection-coupled files:      18
live measured DZT files present:     0
live paired metadata files present:  0
action groups:                       6
accepted action groups:              0
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

The six action groups are:

| Order | Action group | Templates | Measured DZT required | Paired metadata required |
| ---: | --- | ---: | ---: | ---: |
| 1 | prepare global/setup/closeout metadata | 15 | 0 | 0 |
| 2 | collect controlled profile repeats | 3 | 3 | 3 |
| 3 | collect time-zero references | 3 | 3 | 3 |
| 4 | collect amplitude references | 3 | 3 | 3 |
| 5 | place real returns under external field root | 0 | 9 | 9 |
| 6 | run live preflight after collection | 0 | 9 | 9 |

## Interpretation

The field-side execution packet is now collection-day ready as a checklist.
It is not field evidence: no live measured DZT files or live paired metadata
files are present yet.

## Decision

Use this packet as the controlled collection-day execution checklist.
Controlled field evidence, field FWI, and field 3D/HPC remain blocked until the
18 live collection-coupled returns pass preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet.py
2 passed
```

Figure check:

```text
3005x904, dynamic range=255
```
