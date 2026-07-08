# Field Experiment 335: Antenna-Aware Filesystem Gap Audit Refresh

Date: 2026-06-29

## Purpose

Refresh the current return-inbox filesystem gap audit for the 61-item
antenna-aware controlled field return packet.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/335_gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_packet_item_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh.png
scripts/script_snapshot_manifest.json
```

## Result

```text
gap audit ready:                    true
antenna-aware packet guarded:       true
packet items required:              61
present packet items:               0
missing packet items:               61
measured requirements:              54
missing measured DZT files:         9
metadata requirements:              36
missing metadata requirements:      36
global metadata requirements:       15
per-file metadata requirements:     21
antenna metadata addendum items:    4
missing checksum rows:              9
missing acceptance gates:           7
open action groups:                 7
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The previous filesystem gap audit covered a 57-item packet. The current
antenna-aware packet has 61 required items, and none are present in the current
return inbox. The missing set is nine measured DZT files, 36 metadata
requirements, nine checksum rows, and seven acceptance-result files.

## Decision

Use this run as the current field filesystem coverage record. Do not run
provenance acceptance, archive acceptance, field evidence, field FWI, GPU work,
or field 3D/HPC until the missing 61-item packet is closed and passes the
refreshed acceptance gate.

## Validation

Focused source test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh.py
3 passed
```

Figure validation:

```text
3130x931, dynamic range=255
```
