# Field Experiment 455: Direct-Intake Collection-Day Checklist

Date: 2026-06-30

## Purpose

Convert the guarded field receipt manifest from runs `452-454` into an
ordered collection-day copy checklist.

This run is practical preparation, not measured evidence. It records the 33
files that must be copied into the staged return area and groups them into the
three measured DZT families plus metadata. It does not copy files, accept
parser output, accept provenance, archive the packet, run field FWI, or run
field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/455_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_checklist
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_checklist_checklist_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_checklist_action_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_checklist_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_checklist.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source receipt manifest ready:             true
source receipt validation ready:           true
source receipt sensitivity ready:          true
checklist items:                           33
DZT items:                                 9
metadata JSON items:                       24
amplitude-reference DZT items:             3
controlled-profile-repeat DZT items:       3
time-zero-reference DZT items:             3
global metadata items:                     15
per-file metadata items:                   9
pending copy items:                        33
evidence-ready items:                      0
checklist actions:                         5
checklist ready:                           true
GPU priority:                              none
```

## Decision

Use this checklist to copy measured files into the staged return tree. After
the files are copied, rerun receipt, parser, provenance, and archive gates
before any field FWI or field 3D/HPC work.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_checklist.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
