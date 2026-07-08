# Field Experiment 600: Paired Metadata Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `599` validator with damaged versions of the run `598`
paired metadata template pack.

Damaged cases include policy-label damage, source-readiness damage,
template-row-count damage, stage-count damage, stage-shape damage,
template-file-count damage, paired-DZT presence promotion, blank-field damage,
payload-field damage, payload-pairing damage, payload-status promotion,
external-root damage, live-metadata promotion, evidence promotion, field-FWI
promotion, field-3D promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/600_gssi51600s_controlled_collection_trace_pairing_collection_day_return_paired_metadata_template_pack_validation_sensitivity
```

## Result

```text
scenarios:                    22
expected pass scenarios:       1
expected fail scenarios:      21
observed pass scenarios:       1
observed fail scenarios:      21
unexpected outcomes:           0
damaged scenarios:            21
damaged scenarios rejected:   21
gpu priority:                 none
```

## Interpretation

The validator fails closed. The exact saved draft-template pack passes, while
all damaged or falsely promoted variants fail.

## Decision

Use runs `598-600` as the guarded paired metadata template-pack block.
Measured DZT files and paired metadata must pass together before controlled
field evidence, field FWI, or field 3D/HPC can be promoted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_paired_metadata_template_pack_validation_sensitivity.py
3 passed
```

Figure check:

```text
3761x885, dynamic range=255
```
