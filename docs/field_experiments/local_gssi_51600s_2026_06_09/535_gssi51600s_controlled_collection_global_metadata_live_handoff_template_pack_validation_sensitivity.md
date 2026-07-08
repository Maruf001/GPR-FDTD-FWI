# Field Experiment 535: Global Metadata Live Handoff Template Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `534` validator.

The sensitivity cases check whether the validator rejects damaged packet shape,
filled placeholder values, false live-file promotion, false evidence
promotion, false action completion, false live receipt, false field FWI, false
field 3D/HPC, damaged figures, and missing script snapshots.

This is CPU-only validation sensitivity. It does not ingest DZT files, run a
parser, accept provenance, launch field FWI, launch GPU work, or promote field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/535_gssi51600s_controlled_collection_global_metadata_live_handoff_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_global_metadata_live_handoff_template_pack_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_global_metadata_live_handoff_template_pack_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_global_metadata_live_handoff_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                              15
expected pass cases:                 1
expected fail cases:                14
actual pass cases:                   1
actual fail cases:                  14
unexpected cases:                    0
damaged cases:                      14
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
```

## Interpretation

The validator accepts only the exact non-live global metadata template packet.
It rejects false promotion into live receipt, field FWI, or field 3D/HPC.

## Decision

Use runs `533-535` as the guarded global metadata handoff-template block. The
next field blocker remains real live metadata and measured DZT files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_global_metadata_live_handoff_template_pack_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x857, dynamic range=255
```
