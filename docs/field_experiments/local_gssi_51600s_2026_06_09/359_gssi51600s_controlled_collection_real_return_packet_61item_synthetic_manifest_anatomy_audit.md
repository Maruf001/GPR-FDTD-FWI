# Field Experiment 359: 61-Item Synthetic Manifest Anatomy Audit

Date: 2026-06-29

## Purpose

Explain why the current 61-item controlled field return packet maps to 49
unique synthetic payload files in the run `353` manifest.

This is a synthetic packet anatomy audit. It does not create measured field
evidence, accept provenance, accept a real archive, run field FWI, launch GPU
work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/359_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_group_summary.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_prefix_summary.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_duplicate_paths.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit.png
```

## Result

```text
manifest anatomy ready:            true
synthetic packet files:            49
packet requirements:               61
duplicate-path requirements:       12
duplicate-path files:              9
metadata files:                    24
metadata requirements:             36
metadata duplicate requirements:   12
measured DZT files:                9
checksum files:                    9
acceptance files:                  7
measured-evidence payloads:        0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

All 12 duplicate-path requirements are metadata requirements. They are
concentrated in nine metadata files: the three controlled profile-repeat
metadata files carry three requirements each, while three time-zero reference
metadata files and three amplitude-reference metadata files carry two
requirements each.

## Decision

Use this audit to explain the 61-requirement/49-file packet anatomy before
real-return intake. Keep provenance, archive acceptance, controlled field
evidence, field FWI, GPU, and field 3D/HPC blocked until measured files replace
the synthetic payloads.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit.py
4 passed
```

Figure check:

```text
3581x902, dynamic range=255
```
