# Field Experiment 575: Collection-Day Return Package Live Intake Reconciliation Validator

Date: 2026-07-01

## Purpose

Validate the saved run `574` collection-day return package live-intake
reconciliation table from disk.

This run does not create fake DZT files, does not move templates into the live
return area, does not accept live evidence, and does not promote parser,
provenance, field FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/575_gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator_check_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source reconciliation ready:           true
validation checks:                     7
passed validation checks:              7
failed validation checks:              0
package items:                         33
metadata templates present:            24
live files present:                    0
ready for guarded live intake:         0
accepted as live returns:              0
field table intake accepted:           false
parser ready:                          false
field FWI ready:                       false
gpu priority:                          none
```

Validation checks:

| Check | Result |
| --- | --- |
| source reconciliation ready | pass |
| thirty-three items and six stages represented | pass |
| metadata templates are present and blank | pass |
| live files remain absent and unaccepted | pass |
| current status split is preserved | pass |
| field analysis remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved reconciliation table is internally consistent. It preserves all
thirty-three expected return items, the six-stage collection shape, the
twenty-four blank metadata templates, the nine missing measured DZT files, and
the zero-live-file current state.

The validator also confirms that the field analysis boundary is unchanged:
parser execution, evidence promotion, and field FWI remain blocked.

## Decision

Use run `575` as the saved-artifact validator for the run `574` pre-return
reconciliation table.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.py
7 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
