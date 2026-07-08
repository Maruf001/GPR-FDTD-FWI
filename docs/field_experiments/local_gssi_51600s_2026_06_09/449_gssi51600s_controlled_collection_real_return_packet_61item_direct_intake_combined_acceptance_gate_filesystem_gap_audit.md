# Field Experiment 449: Combined Acceptance Gate Filesystem Gap Audit

Date: 2026-06-30

## Purpose

Check the live staging filesystem against the combined 33-file direct-intake
acceptance gate from runs `446-448`.

This run does not create measured files and does not run DZT parsing,
provenance validation, archive acceptance, field FWI, GPU work, or field 3D/HPC
work. It records the current filesystem state before any real files are copied.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/449_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_filesystem_file_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_filesystem_directory_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gate ready:                         true
source validation ready:                   true
source sensitivity ready:                  true
required files:                            33
scanned files:                             33
required directories:                      5
present directories:                       5
present files:                             0
nonempty files:                            0
missing files:                             33
missing DZT files:                         9
missing metadata JSON files:               24
accepted files:                            0
unexpected files:                          0
filesystem actions:                        4
ready filesystem actions:                  0
filesystem-gap audit ready:                true
real packet files present:                 false
real packet accepted:                      false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The five required staging directories exist, but none of the 33 required files
has been copied into them.

## Decision

The field side is ready for file receipt, not for parser/provenance/archive
reruns. The next physical action is to copy the nine measured DZT files and
24 metadata JSON files into the staged return tree, then rerun the combined
acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit.py
3 passed
```

Figure check:

```text
2465x844, dynamic range=255
```
