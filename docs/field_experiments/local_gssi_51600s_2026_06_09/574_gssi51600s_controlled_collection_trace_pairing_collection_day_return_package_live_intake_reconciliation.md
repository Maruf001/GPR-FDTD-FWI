# Field Experiment 574: Collection-Day Return Package Live Intake Reconciliation

Date: 2026-07-01

## Purpose

Reconcile the run `571` collection-day return package templates against the
live field intake paths.

This run does not create fake DZT files, does not move templates into the live
return area, does not accept live evidence, and does not promote parser,
provenance, field FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/574_gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_reconciliation_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_stage_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_status_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:             true
source trace intake ready:              true
package items:                          33
stages:                                 6
measured DZT files required:            9
metadata items required:                24
metadata templates present:             24
metadata template nonblank values:      0
live files present:                     0
ready for guarded live intake:          0
accepted as live returns:               0
trace-pairing capture rows:             3
trace-pairing capture rows ready:       0
field table intake accepted:            false
field FWI ready:                        false
gpu priority:                           none
```

Current item status:

| Status | Items |
| --- | ---: |
| awaiting filled metadata | 24 |
| awaiting measured DZT | 9 |

## Interpretation

The collection-day package is now connected to the live intake paths. All
twenty-four metadata templates exist and remain blank. The nine measured DZT
files are still absent. No live file is present, no item is ready for guarded
live intake, and no item is accepted as field evidence.

This is the current pre-return checklist for the controlled field collection.
The next state change must come from real measured DZT files and filled
metadata JSON files appearing in the live return area.

## Decision

Use run `574` as the field collection-day pre-return reconciliation table. Keep
parser execution, provenance promotion, controlled field evidence, field FWI,
and field 3D/HPC blocked until real live files pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```
