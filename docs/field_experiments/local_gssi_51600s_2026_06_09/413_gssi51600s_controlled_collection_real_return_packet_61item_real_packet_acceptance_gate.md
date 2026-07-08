# Field Experiment 413: Real Packet Acceptance Gate

Date: 2026-06-29

## Purpose

Define the acceptance gate for a future real controlled-collection packet after
the release-gate checklist from runs `407-412`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/413_gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_acceptance_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
acceptance gate ready:                       true
acceptance rows:                             49
direct real-input rows:                      33
generated follow-up rows:                    16
real source rows accepted:                   0
parser-accepted real rows:                   0
provenance-accepted real rows:               0
archive-accepted real rows:                  0
measured-evidence rows ready:                0
blocked rows:                                49
real packet files present:                   false
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Interpretation

The field acceptance gate is now explicit. A future real packet must pass real
source acceptance, parser acceptance, provenance acceptance, archive
acceptance, and measured-evidence readiness before field FWI or 3D/HPC work is
considered.

## Decision

Use this gate before promoting any controlled collection packet to measured
field evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate.py
3 passed
```

Figure check:

```text
2861x860, dynamic range=255
```
