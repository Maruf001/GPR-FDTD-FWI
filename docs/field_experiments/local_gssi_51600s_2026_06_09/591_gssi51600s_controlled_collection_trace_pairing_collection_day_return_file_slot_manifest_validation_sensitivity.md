# Field Experiment 591: Controlled Collection Return File-Slot Manifest Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `590` validator with damaged versions of the run `589`
file-slot manifest.

The damaged scenarios include slot-count damage, stage-count damage,
metadata/measured-file count damage, dependency-class damage, collection-coupled
count damage, fake candidate files, fake preflight passes, fake ready slots,
controlled-field-evidence promotion, field FWI promotion, field 3D/HPC
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/591_gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_validation_sensitivity
```

## Result

```text
scenarios:                         15
expected pass scenarios:           1
expected fail scenarios:           14
observed pass scenarios:           1
observed fail scenarios:           14
unexpected outcomes:               0
damaged scenarios:                 14
damaged scenarios rejected:        14
gpu priority:                      none
```

The exact saved manifest passes. All fourteen damaged variants fail.

## Decision

Use this sensitivity run to keep the controlled collection file-slot manifest
fail-closed. Do not promote controlled field evidence, field FWI, or field
3D/HPC from partial or damaged return files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_validation_sensitivity.py

3 passed
```

Figure check:

```text
2950x873, dynamic range=255
```
