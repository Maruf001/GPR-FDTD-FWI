# Field Experiment 599: Paired Metadata Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `598` paired metadata template pack from its saved
artifacts.

The validator checks source identity, nine-template shape, stage shape,
blank required fields, measured-DZT pairing identity, output-local placement,
absent paired DZT files, zero live metadata acceptance, blocked downstream
states, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/599_gssi51600s_controlled_collection_trace_pairing_collection_day_return_paired_metadata_template_pack_validator
```

## Result

```text
validation checks:              8
passed checks:                  8
failed checks:                  0
paired metadata templates:      9
stage count:                    3
stage shape:                    3;3;3
template files present:         9
paired DZT files present:       0
required fill fields:           54
blank required fill fields:     54
accepted live paired metadata:  0
controlled field evidence:      false
field FWI ready:                false
field 3D/HPC ready:             false
```

## Interpretation

The paired metadata templates validate as draft forms tied to absent measured
DZT files.

## Decision

Use this validator before paired metadata is accepted into the controlled field
packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_paired_metadata_template_pack_validator.py
3 passed
```

Figure check:

```text
3401x893, dynamic range=255
```
