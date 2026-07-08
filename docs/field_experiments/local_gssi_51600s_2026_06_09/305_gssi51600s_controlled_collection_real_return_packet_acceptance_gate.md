# Field Experiment 305: Real-Return Packet Acceptance Gate

Date: 2026-06-29

## Purpose

Convert the guarded field real-return packet gap boundary from runs `302-304`
into a rerunnable acceptance gate for the eventual measured return packet.

This run does not stage packet files, run provenance acceptance, promote field
evidence, run field FWI, launch GPU work, or start field 3D/HPC. It checks the
current return inbox against the guarded packet contract and reports what must
be present before execution can start.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/305_gssi51600s_controlled_collection_real_return_packet_acceptance_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_packet_item_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_acceptance_gate_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_acceptance_gate.png
docs/GSSI51600S_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_ACCEPTANCE_GATE.md
scripts/
```

## Result

```text
acceptance gates:                   9
ready gates:                        2
blocked gates:                      7
packet items:                       57
present packet items:               0
missing packet items:               57
measured requirements:              50
completed measured requirements:    0
missing measured DZT files:         9
missing metadata requirements:      32
missing checksum rows:              9
missing acceptance results:         7
required action groups:             7
open action groups:                 7
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The two ready gates are:

| Gate | Meaning |
| --- | --- |
| `guarded_source_contracts_available` | The upstream field packet contract, staging plan, and gap claim boundary are guarded. |
| `expected_packet_inventory_known` | The expected 57-item packet inventory is known. |

The seven blocked gates are measured-data and execution gates. The return inbox
currently has no required measured packet items present.

## Interpretation

The field branch is ready to accept a returned measured packet, but it is not
ready to promote field evidence. The current blocker is concrete: 57 items are
missing, including nine measured DZT files, 32 metadata requirements, nine
checksum rows, and seven acceptance result files.

## Decision

Use run `305` as the rerunnable acceptance gate for future measured field
return packets. Do not run provenance acceptance, archive acceptance, field
evidence, field FWI, GPU work, or field 3D/HPC until this gate passes.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_real_return_packet_acceptance_gate.py: pass
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate.py: pass
```

Figure validation:

```text
3761x962, dynamic range=255
```
