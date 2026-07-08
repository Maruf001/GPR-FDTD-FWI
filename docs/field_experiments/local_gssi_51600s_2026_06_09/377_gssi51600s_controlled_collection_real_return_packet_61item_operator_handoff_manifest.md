# Field Experiment 377: 61-Item Operator Handoff Manifest

Date: 2026-06-29

## Purpose

Turn the guarded collection checklist into a file-level operator handoff
manifest for the controlled 61-item field packet.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/377_gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_handoff_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_stage_summary_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_operator_handoff_manifest.png
```

## Result

```text
operator handoff ready:            true
stages:                            4
handoff rows:                      49
direct operator items:             33
generated follow-up items:         16
measured DZT items:                9
metadata items:                    24
checksum items:                    9
acceptance items:                  7
packet requirements:               61
duplicate-path requirements:       12
current measured-evidence payloads:0
collection-day direct actions ready:true
generated outputs ready now:       false
real packet files present:         false
provenance acceptance ready:       false
archive acceptance ready:          false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The first 33 rows are the direct collection inputs: nine DZT files and 24
metadata files. The remaining 16 rows are generated after the real inputs
exist: nine checksum files and seven acceptance outputs.

## Decision

Use this manifest as the collection-day file handoff. It does not promote
field evidence, provenance acceptance, archive acceptance, field FWI, GPU
work, or field 3D/HPC.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_operator_handoff_manifest.py
3 passed as part of the 10-test focused set
```

Figure check:

```text
3221x879, dynamic range=255
```
