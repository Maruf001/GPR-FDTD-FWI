# Field Experiment 419: 61-Item Real-Packet Filesystem Gap Audit

Date: 2026-06-29

## Purpose

Scan the field experiment tree for the 33 direct real-input files required by
the run `413` real-packet acceptance gate.

This run separates real returned files from blank templates and synthetic
smoke-test files.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/419_gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_scan_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_candidate_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
direct real inputs required:                 33
generated follow-ups required:               16
open filesystem gaps:                        33
matching candidate files:                    95
real-return candidates:                      0
blank-template candidates:                   62
synthetic-reference candidates:              33
accepted measured-evidence files:            0
real packet files present:                   false
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
GPU priority:                                none
```

All 33 direct real-input slots remain open gaps. The matching files currently
on disk are templates or synthetic smoke-test files, not measured field
evidence.

## Decision

Keep controlled field evidence, provenance acceptance, archive acceptance,
field FWI, and field 3D/HPC blocked until real packet files arrive.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_filesystem_gap_audit.py
4 passed
```

Figure check:

```text
2825x846, dynamic range=255
```
