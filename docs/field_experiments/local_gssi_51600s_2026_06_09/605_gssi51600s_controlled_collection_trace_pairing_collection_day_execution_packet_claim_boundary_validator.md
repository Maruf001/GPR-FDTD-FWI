# Field Experiment 605: Collection-Day Execution Packet Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `604` claim boundary from its written artifacts.

The validator checks that the claim table has the expected guarded and blocked
claims, the controlled collection counts remain stable, no live measured return
files are present, and field evidence or downstream analysis is not promoted.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/605_gssi51600s_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary_validator
```

## Result

```text
validation checks:                 8
passed checks:                     8
failed checks:                     0
claims:                            5
guarded claims:                    2
blocked claims:                    3
field return slots:               33
required live return files:       18
live measured DZT files:           0
live paired metadata files:        0
accepted action groups:            0
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
```

## Interpretation

The saved field claim boundary validates from artifacts and remains
evidence-blocked.

## Decision

Use this validator before citing the run `604` field claim boundary.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_execution_packet_claim_boundary_validator.py
5 passed
```

Figure check:

```text
3221x893, dynamic range=255
```
