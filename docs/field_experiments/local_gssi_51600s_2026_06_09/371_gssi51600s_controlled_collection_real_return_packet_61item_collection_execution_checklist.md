# Field Experiment 371: 61-Item Collection Execution Checklist

Date: 2026-06-29

## Purpose

Convert the guarded 61-item replacement ledger into an ordered collection
execution checklist.

This run is a workflow artifact. It does not create measured field evidence,
promote provenance acceptance, run field FWI, launch GPU work, or run field
3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/371_gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_checklist_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_dependency_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_collection_execution_checklist.png
```

## Result

```text
checklist ready:                   true
stages:                            4
dependency edges:                  6
direct collection stages:          2
generated verification stages:     2
unique packet files:               49
packet requirements:               61
duplicate-path requirements:       12
direct collection input files:     33
generated verification files:      16
collection-day direct actions:     true
generated outputs ready now:       false
real packet files present:         false
provenance acceptance ready:       false
archive acceptance ready:          false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The checklist has four ordered stages:

| Step | Stage | Files | Requirements |
| ---: | --- | ---: | ---: |
| 1 | collect controlled DZT files | 9 | 9 |
| 2 | record measured metadata files | 24 | 36 |
| 3 | regenerate checksum files | 9 | 9 |
| 4 | rerun structural, provenance, and acceptance gates | 7 | 7 |

## Decision

Use this as the collection execution checklist. Keep provenance acceptance,
archive acceptance, field evidence, field FWI, GPU work, and field 3D/HPC
blocked until real direct inputs are present and generated outputs are
regenerated from them.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_collection_execution_checklist.py
4 passed
```

Figure check:

```text
2897x879, dynamic range=255
```
