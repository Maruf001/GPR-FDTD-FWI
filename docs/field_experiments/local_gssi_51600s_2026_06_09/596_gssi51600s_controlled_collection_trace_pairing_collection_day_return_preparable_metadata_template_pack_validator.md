# Field Experiment 596: Preparable Metadata Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `595` preparable metadata template pack from its saved
artifacts.

The validator checks source identity, template counts, stage shape, blank
required fields, output-local placement, absence of live metadata acceptance,
blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/596_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_validator
```

## Result

```text
validation checks:                    8
passed checks:                        8
failed checks:                        0
template count:                       15
stage count:                          3
stage shape:                          7;4;4
template files present:               15
required fill fields:                 75
blank required fill fields:           75
templates under external return root: 0
accepted live metadata count:         0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

## Interpretation

The run `595` template pack validates as a complete set of blank preparation
forms. It is not live metadata and not field evidence.

## Decision

Use this validator before accepting any prefilled metadata templates into the
controlled field packet.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_validator.py
```

Figure check:

```text
3437x894, dynamic range=255
```
