# Field Experiment 597: Preparable Metadata Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `596` validator with damaged versions of the run `595`
preparable metadata template pack.

Damaged cases include policy-label damage, source-readiness damage, template
row-count damage, stage-count damage, stage-shape damage, template-file-count
damage, blank-field-count damage, payload-field damage, external-root damage,
live-metadata promotion, evidence promotion, field-FWI promotion, field-3D
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/597_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_validation_sensitivity
```

## Result

```text
scenarios:                    20
expected pass scenarios:       1
expected fail scenarios:      19
observed pass scenarios:       1
observed fail scenarios:      19
unexpected outcomes:           0
damaged scenarios:            19
damaged scenarios rejected:   19
gpu priority:                 none
```

## Interpretation

The validator fails closed. The exact saved blank-template pack passes, while
all damaged or falsely promoted variants fail.

## Decision

Use runs `595-597` as the guarded preparable metadata template-pack block.
These runs prepare the field packet for real metadata entry, but do not promote
controlled field evidence, field FWI, or field 3D/HPC.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_validation_sensitivity.py
```

Figure check:

```text
3653x879, dynamic range=255
```
