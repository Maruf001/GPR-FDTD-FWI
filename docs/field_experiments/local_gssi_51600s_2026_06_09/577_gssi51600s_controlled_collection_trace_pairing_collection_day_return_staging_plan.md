# Field Experiment 577: Collection-Day Return Staging Plan

Date: 2026-07-01

## Purpose

Create a non-executed staging plan for the controlled-collection field returns
identified by runs `574-576`.

This run does not create measured DZT files, does not fill metadata JSON files,
does not stage files into the live return area, does not execute copy commands,
does not accept field evidence, and does not promote parser, provenance, field
FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/577_gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_item_staging_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_action_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source reconciliation ready:          true
source validation ready:              true
source sensitivity ready:             true
staging items:                        33
stages:                               6
metadata JSON files required:         24
measured DZT files required:          9
template copy allowed:                0
filled metadata files present:        0
measured DZT files present:           0
live files present:                   0
ready to stage items:                 0
copy commands:                        33
executed commands:                    0
action groups:                        5
ready action groups:                  0
trace pairing ready:                  false
field table intake accepted:          false
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

Action groups:

| Order | Action | Required items | Ready now |
| ---: | --- | ---: | --- |
| 1 | fill collection metadata JSON files | 24 | false |
| 2 | collect measured DZT files | 9 | false |
| 3 | preflight measured files and metadata together | 33 | false |
| 4 | stage only real collection files into live paths | 33 | false |
| 5 | rerun trace-pairing and field intake gates | 33 | false |

## Interpretation

The controlled-collection handoff is now reduced to twenty-four filled metadata
JSON files, nine measured DZT files, thirty-three exact live-path copy commands,
and five guarded action groups.

The commands are intentionally non-executed. Blank metadata templates are
non-evidence and are not stageable. A measured DZT file must be paired with its
filled metadata before guarded intake can accept it.

## Decision

Use run `577` as the non-executed staging plan for future controlled-collection
returns. Keep parser execution, provenance promotion, controlled field evidence,
field FWI, and field 3D/HPC blocked until real files pass paired preflight and
guarded intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```
