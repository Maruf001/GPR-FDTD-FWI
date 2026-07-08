# Field Experiment 299: Real-Return Packet Filesystem Gap Audit

Date: 2026-06-29

## Purpose

Audit whether the current controlled-collection return inbox contains the items
required by the guarded real-return packet contract.

Runs `293-298` define, validate, and harden the field real-return packet
contract and its non-executed staging command plan. This run checks the current
dataset-local return inbox against that contract.

This run does not stage measured files, run DZT preprocessing, run FDTD, run
field FWI, launch GPU/HPC work, or claim field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/299_gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_filesystem_gap_audit_packet_item_rows.csv
data/field_controlled_collection_real_return_packet_filesystem_gap_audit_action_rows.csv
data/field_controlled_collection_real_return_packet_filesystem_gap_audit_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_packet_filesystem_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
expected packet root:              outputs/field_experiments/local_gssi_51600s_2026_06_09/263_gssi51600s_controlled_collection_real_return_empty_intake_layout/return_inbox
packet contract guarded:           true
packet items:                      57
present packet items:              0
missing packet items:              57
measured requirements:             50
missing real DZT files:            9
missing metadata requirements:     32
missing checksum rows:             9
missing acceptance gates:          7
open action groups:                7
real packet files present:         false
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
figure size:                       3130x925
figure dynamic range:              255
```

The seven open action groups are:

| Priority | Action group | Missing items |
| ---: | --- | ---: |
| 1 | stage controlled profile repeats | 3 |
| 2 | stage time-zero references | 3 |
| 3 | stage amplitude references | 3 |
| 4 | record global metadata values | 11 |
| 5 | record per-file metadata values | 21 |
| 6 | record SHA-256 checksums | 9 |
| 7 | rerun acceptance gates | 7 |

## Interpretation

The guarded field packet contract and staging plan are intact, but the current
return inbox contains none of the required packet items. Provenance acceptance,
real archive acceptance, controlled field evidence, field FWI, field 3D/HPC,
and GPU work remain blocked.

## Decision

Use run `299` as the filesystem gap audit for the controlled-collection
real-return packet. The next field-side action is to stage the nine measured
DZT files, 32 measured metadata values, nine checksum records, and then rerun
structural/provenance acceptance gates.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_filesystem_gap_audit.py
3 passed
```
