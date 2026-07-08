# Field Experiment 578: Collection-Day Return Staging Plan Validator

Date: 2026-07-01

## Purpose

Validate the saved run `577` controlled-collection field return staging plan
from disk.

This run does not create measured DZT files, does not fill metadata JSON files,
does not stage files into the live return area, does not execute copy commands,
does not accept field evidence, and does not promote parser, provenance, field
FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/578_gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator_check_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:       true
validation checks:               7
passed validation checks:        7
failed validation checks:        0
staging items:                   33
metadata JSON files required:    24
measured DZT files required:     9
copy commands:                   33
executed commands:               0
field table intake accepted:     false
field FWI ready:                 false
gpu priority:                    none
```

Validation checks:

| Check | Result |
| --- | --- |
| source staging plan ready | pass |
| thirty-three items and six stages represented | pass |
| metadata and measured DZT counts preserved | pass |
| blank templates are non-stageable | pass |
| commands are present but non-executed | pass |
| action groups and field analysis remain blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved collection-day return staging plan is internally consistent. It
preserves thirty-three non-executed copy commands, twenty-four metadata JSON
requirements, nine measured DZT requirements, non-stageable blank templates,
and blocked field-analysis states.

## Decision

Use run `578` as the saved-artifact validator for the run `577` non-executed
field return staging plan.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.py
7 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
