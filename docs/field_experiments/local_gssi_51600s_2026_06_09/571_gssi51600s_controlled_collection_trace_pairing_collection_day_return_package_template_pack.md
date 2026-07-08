# Field Experiment 571: Trace-Pairing Collection-Day Return Package Template Pack

Date: 2026-07-01

## Purpose

Create an output-local return package template for the controlled GSSI field
collection.

This run does not create fake DZT files, does not place files in the live-return
area, does not accept any field evidence, does not run a parser, does not run
field FWI, and does not run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/571_gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack
```

Key artifacts:

```text
data/collection_day_return_package_templates/
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_package_manifest_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_stage_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_trace_pairing_capture_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                  true
source trace-pairing schema ready:    true
source trace-pairing intake ready:    true
stages:                               6
package items:                        33
measured DZT files required:          9
metadata templates:                   24
metadata templates written:           24
DZT file templates written:           0
required metadata value fields:       96
template nonblank value count:        0
trace-pairing capture rows:           3
ready trace-pairing rows:             0
accepted as live return:              0
live receipt ready:                   false
field table intake accepted:          false
field FWI ready:                      false
gpu priority:                         none
```

Stage package:

| Stage | Package items | Measured DZT files | Metadata templates | Metadata values |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 7 | 0 | 7 | 28 |
| 2 | 4 | 0 | 4 | 16 |
| 3 | 6 | 3 | 3 | 12 |
| 4 | 6 | 3 | 3 | 12 |
| 5 | 6 | 3 | 3 | 12 |
| 6 | 4 | 0 | 4 | 16 |

## Interpretation

The field return package is now easier to execute on collection day. It lists
all thirty-three required files and provides blank metadata JSON templates for
the twenty-four metadata records. It also provides a three-row trace-pairing
capture sheet that ties each controlled profile repeat to its time-zero and
amplitude references.

The templates are deliberately output-local and blank. They contain zero
nonblank metadata values, create no DZT placeholders, and are not accepted as
live evidence. This prevents a template from being mistaken for a measured field
return.

## Decision

Use run `571` to organize future controlled collection returns. Keep parser,
provenance, controlled field evidence, field FWI, and field 3D/HPC blocked until
real DZT files and filled metadata pass the guarded intake path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py: pass
```

Figure check:

```text
2212x844, dynamic range=255
```
