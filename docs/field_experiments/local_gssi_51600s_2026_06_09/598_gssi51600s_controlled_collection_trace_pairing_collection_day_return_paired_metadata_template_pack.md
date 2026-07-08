# Field Experiment 598: Paired Metadata Template Pack

Date: 2026-07-01

## Purpose

Create output-local JSON templates for the nine metadata records that must be
completed together with measured DZT files during controlled collection.

These records correspond to three controlled profile repeats, three time-zero
references, and three amplitude references.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/598_gssi51600s_controlled_collection_trace_pairing_collection_day_return_paired_metadata_template_pack
```

## Result

```text
paired metadata templates:             9
stage count:                           3
stage shape:                           3;3;3
template files present:                9
paired DZT files present:              0
required fill fields:                  54
blank required fill fields:            54
templates under external return root:  0
accepted live paired metadata:         0
ready for collection-day fill:         true
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
```

## Interpretation

The collection-coupled metadata packet is now explicit. Each measured radar
file has a matching metadata template, but no measured DZT file is present and
no paired metadata is accepted as live evidence.

## Decision

Use these templates during collection-day file pairing only. Controlled field
evidence, field FWI, and field 3D/HPC remain blocked until measured DZT files
and paired metadata pass together.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_paired_metadata_template_pack.py
2 passed
```

Figure check:

```text
2717x882, dynamic range=255
```
