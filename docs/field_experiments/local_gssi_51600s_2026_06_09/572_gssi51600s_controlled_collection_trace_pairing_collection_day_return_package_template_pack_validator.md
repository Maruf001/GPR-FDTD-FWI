# Field Experiment 572: Trace-Pairing Collection-Day Return Package Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `571` collection-day return package template pack.

This run does not create fake DZT files, does not place files in the live-return
area, does not accept any field evidence, does not run a parser, does not run
field FWI, and does not run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/572_gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator_check_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:           true
validation checks:                    7
passed validation checks:             7
failed validation checks:             0
package items:                        33
metadata templates written:           24
DZT file templates written:           0
template nonblank value count:        0
accepted as live return:              0
field table intake accepted:          false
field FWI ready:                      false
gpu priority:                         none
```

Validation checks:

| Check | Result |
| --- | --- |
| source template pack ready | pass |
| thirty-three package items represented | pass |
| metadata templates written without DZT placeholders | pass |
| stage package shape is preserved | pass |
| templates remain blank and unaccepted | pass |
| capture rows exist but field analysis remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved collection-day package is internally consistent. It covers all
thirty-three expected field-return items, writes twenty-four blank metadata
templates, writes no DZT placeholders, and keeps all field-analysis states
blocked.

## Decision

Use run `572` as the saved-artifact validator for the run `571`
collection-day template pack.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.py
7 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
