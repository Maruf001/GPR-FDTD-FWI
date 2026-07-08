# Field Experiment 306: Real-Return Packet Acceptance Gate Validator

Date: 2026-06-29

## Purpose

Validate the saved run `305` field return-packet acceptance gate from
artifacts.

This run checks acceptance-gate counts, gate order, current packet item rows,
action-group rows, downstream blocked states, figure validation, and script
snapshots.

It does not stage packet files, run provenance acceptance, promote field
evidence, run field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/306_gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validator.png
docs/GSSI51600S_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_ACCEPTANCE_GATE_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
acceptance gates:                   9
ready gates:                        2
blocked gates:                      7
packet items:                       57
present packet items:               0
missing packet items:               57
missing measured DZT files:         9
missing metadata requirements:      32
missing checksum rows:              9
missing acceptance results:         7
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

## Interpretation

The run `305` acceptance gate is internally consistent: two source/inventory
gates pass, seven measured-data or execution gates remain blocked, and no
measured packet items are present.

## Decision

Use run `306` as the validator for the run `305` field return-packet
acceptance gate. Sensitivity hardening remains required before treating the
gate as fully guarded.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_validator.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_real_return_packet_acceptance_gate_validator.py: pass
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_validator.py: pass
```

Figure validation:

```text
3653x927, dynamic range=255
```
