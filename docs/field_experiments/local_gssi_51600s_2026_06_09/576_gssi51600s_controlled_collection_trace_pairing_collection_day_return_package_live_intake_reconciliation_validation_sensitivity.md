# Field Experiment 576: Collection-Day Return Package Live Intake Reconciliation Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `575` validator for the collection-day return package
live-intake reconciliation table.

This run does not create fake DZT files, does not move templates into the live
return area, does not accept live evidence, and does not promote parser,
provenance, field FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/576_gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
validation scenarios:                  14
expected pass scenarios:               1
expected fail scenarios:               13
observed pass scenarios:               1
observed fail scenarios:               13
unexpected outcomes:                   0
damaged scenarios:                     13
damaged scenarios rejected:            13
gpu priority:                          none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Result |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| item count damage | fail | fail | expected |
| stage count damage | fail | fail | expected |
| metadata template damage | fail | fail | expected |
| nonblank template damage | fail | fail | expected |
| live file promotion | fail | fail | expected |
| ready for intake promotion | fail | fail | expected |
| false acceptance | fail | fail | expected |
| status split damage | fail | fail | expected |
| parser promotion | fail | fail | expected |
| field FWI promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The reconciliation validator accepts the exact saved pre-return state and
rejects damaged source, count, template, live-file, acceptance, status, parser,
FWI, figure, and snapshot states.

This closes the field collection-day live-intake reconciliation block. The
current physical next step is unchanged: real measured DZT files and filled
metadata JSON files must appear in the live return area before parsing,
provenance, field evidence, or field FWI can proceed.

## Decision

Use runs `574-576` as the guarded field collection-day live-intake
reconciliation block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_live_intake_reconciliation_validation_sensitivity.py: pass
```

Figure check:

```text
2824x860, dynamic range=255
```
