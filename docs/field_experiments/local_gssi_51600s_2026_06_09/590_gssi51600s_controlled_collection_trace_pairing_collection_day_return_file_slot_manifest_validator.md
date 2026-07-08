# Field Experiment 590: Controlled Collection Return File-Slot Manifest Validator

Date: 2026-07-01

## Purpose

Validate the saved run `589` controlled collection return file-slot manifest.

Run `589` converted the collection-day dependency map into a per-file checklist.
This validator checks the slot shape, metadata/measured-file split, dependency
classes, blocked preflight state, and blocked field-analysis state.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/590_gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_validator
```

## Result

```text
validation checks:                         8
passed checks:                             8
failed checks:                             0
file slots:                                33
stages:                                    6
metadata JSON slots:                       24
measured DZT slots:                        9
metadata preparable before collection:     15
metadata paired with DZT:                  9
measured DZT dependency slots:             9
collection-coupled slots:                  18
preflight-passed slots:                    0
ready slots:                               0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

## Interpretation

The saved file-slot manifest is stable. It preserves the 33 expected return
slots, keeps the 18 collection-coupled slots grouped around measured DZT files
and paired metadata, and does not promote controlled field evidence.

## Decision

Use this validator before accepting any update to the controlled collection
return manifest.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_validator.py

3 passed
```

Figure check:

```text
2861x931, dynamic range=255
```
