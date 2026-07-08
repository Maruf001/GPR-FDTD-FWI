# Field Experiment 595: Preparable Metadata Template Pack

Date: 2026-07-01

## Purpose

Create output-local JSON templates for the fifteen controlled-collection
metadata records that can be prepared before the field collection.

Runs `589-594` defined the full 33-slot collection return manifest and guarded
its claim boundary. This run takes the preparable portion of that manifest and
turns it into fillable metadata worksheets. It does not write to the external
field-return path and does not create live metadata evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/595_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack
```

Key artifacts:

```text
data/preparable_metadata_templates/
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_template_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_stage_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source manifest ready:              true
source claim boundary ready:        true
preparable metadata templates:      15
stages with templates:              3
stage shape:                        7;4;4
template files present:             15
required fill fields:               75
blank required fill fields:         75
templates under external root:      0
accepted live metadata:             0
ready for pre-collection fill:      true
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

Template distribution:

| Stage | Template count | Blank required fill fields |
| ---: | ---: | ---: |
| 1 | 7 | 35 |
| 2 | 4 | 20 |
| 6 | 4 | 20 |

## Interpretation

The field-side checklist now has a practical pre-collection worksheet pack.
The templates cover the global/session metadata that can be prepared before the
measured DZT files exist: antenna/system details, survey setup, material/truth
context, operator/date/weather/notes, and related setup records.

The templates intentionally remain blank in the fields that must be filled by a
human or collection record. They are not accepted live metadata and do not make
controlled field evidence ready.

## Decision

Use these templates for pre-collection preparation. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until live metadata and measured
DZT files pass preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preparable_metadata_template_pack.py
2 passed
```

Figure check:

```text
2645x882, dynamic range=255
```
