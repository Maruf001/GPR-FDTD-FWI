# Field Experiment 604: Collection-Day Execution Packet Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the guarded controlled collection-day execution
packet.

This run does not create measured DZT files, create live paired metadata, accept
field evidence, run field FWI, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/604_gssi51600s_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary
```

## Result

```text
claims:                            5
guarded claims:                    2
blocked claims:                    3
supported guarded claims:          2
field return slots:               33
metadata templates:               24
measured DZT files required:       9
required live return files:       18
live measured DZT files:           0
live paired metadata files:        0
accepted action groups:            0
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
```

The guarded claims are:

```text
collection-day execution packet
metadata template split
```

The blocked claims are:

```text
measured collection returns
controlled field evidence
field FWI and field 3D/HPC
```

## Interpretation

The collection-day packet and metadata split are guarded, but measured
collection returns, controlled field evidence, field FWI, and field 3D/HPC
remain blocked.

## Decision

Use this boundary as the current field claim line after the execution-packet
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary.py
2 passed
```

Figure check:

```text
3293x893, dynamic range=255
```
