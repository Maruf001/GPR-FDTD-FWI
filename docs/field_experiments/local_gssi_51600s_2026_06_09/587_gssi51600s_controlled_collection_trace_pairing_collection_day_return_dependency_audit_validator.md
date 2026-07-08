# Field Experiment 587: Controlled Collection Return Dependency Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `586` dependency audit for controlled collection return
items.

The validator checks that the audit preserves the split between metadata records
that can be prepared separately and measured DZT files whose paired metadata
must travel with the field data.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/587_gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit_validator
```

## Result

```text
validation checks:                         7
passed checks:                             7
failed checks:                             0
stages:                                    6
required return items:                     33
metadata JSON items:                       24
measured DZT items:                        9
metadata preparable without DZT:           15
metadata paired with DZT:                  9
collection-coupled stages:                 3
collection-coupled items:                  18
preflight-passed items:                    0
ready stages:                              0
ready action groups:                       0
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
gpu priority:                              none
```

## Decision

Use this validator before citing run `586` as the controlled-collection
dependency map.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_dependency_audit_validator.py
3 passed
```

Figure check:

```text
3293x927, dynamic range=255
```
