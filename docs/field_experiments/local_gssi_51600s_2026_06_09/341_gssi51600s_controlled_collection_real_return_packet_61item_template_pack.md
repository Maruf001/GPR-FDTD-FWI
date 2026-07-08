# Field Experiment 341: 61-Item Return Packet Template Pack

Date: 2026-06-29

## Purpose

Create a corrected non-evidence template pack for the current antenna-aware
controlled field return packet.

This run does not stage measured field files, pass the return-packet
acceptance gate, accept provenance, promote controlled field evidence, launch
field FWI, use GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/341_gssi51600s_controlled_collection_real_return_packet_61item_template_pack
```

Key artifacts:

```text
template_return_inbox/
data/gssi51600s_controlled_collection_real_return_packet_61item_template_pack_packet_requirement_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_template_pack_template_file_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_template_pack_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
packet requirements:                 61
unique return paths:                 49
template files written:              50
template packet files:               49
duplicate-path requirements:         12
real DZT requirements:               9
real DZT template files:             9
metadata requirements:               36
metadata template files:             24
global metadata requirements:        15
file metadata requirements:          21
antenna metadata addendum records:   4
checksum requirements:               9
checksum template files:             9
acceptance-result requirements:      7
acceptance-result template files:    7
real packet files present:           false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

## Interpretation

The antenna-aware field packet has 61 requirements but 49 unique return paths.
The difference is intentional: several per-file metadata requirements share one
metadata JSON path for the same measured DZT item. This run records both
numbers so the handoff is clear.

The templates are not measured evidence. They are placeholders inside this run
folder only and must be replaced by real measured DZT files, measured metadata,
checksum records, and acceptance results in the return inbox.

## Decision

Use this corrected template pack for measured field packet intake. Provenance
acceptance, archive acceptance, controlled field evidence, field FWI, GPU work,
and field 3D/HPC remain blocked until real items replace the templates and pass
the antenna-aware acceptance gate.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_template_pack.py
3 passed
```

Figure validation:

```text
3616x931, dynamic range=255
```
