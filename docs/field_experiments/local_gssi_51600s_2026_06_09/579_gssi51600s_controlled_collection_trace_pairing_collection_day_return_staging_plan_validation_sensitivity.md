# Field Experiment 579: Collection-Day Return Staging Plan Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `578` staging-plan validator against controlled damaged
states.

This run does not create measured DZT files, does not fill metadata JSON files,
does not stage files into the live return area, does not execute copy commands,
does not accept field evidence, and does not promote parser, provenance, field
FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/579_gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:       true
validation scenarios:         19
expected pass scenarios:      1
expected fail scenarios:      18
observed pass scenarios:      1
observed fail scenarios:      18
unexpected outcomes:          0
damaged scenarios:            18
damaged scenarios rejected:   18
gpu priority:                 none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Outcome |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| item count damage | fail | fail | expected |
| stage count damage | fail | fail | expected |
| metadata count damage | fail | fail | expected |
| DZT count damage | fail | fail | expected |
| template copy allowed | fail | fail | expected |
| filled metadata promotion | fail | fail | expected |
| measured DZT promotion | fail | fail | expected |
| live file promotion | fail | fail | expected |
| ready-to-stage promotion | fail | fail | expected |
| executed command | fail | fail | expected |
| copy command damage | fail | fail | expected |
| action count damage | fail | fail | expected |
| ready action promotion | fail | fail | expected |
| field table promotion | fail | fail | expected |
| field FWI promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The staging-plan validator accepts the exact non-executed state and rejects
damaged source, count, template-copy, file-promotion, execution, action,
field-analysis, figure, and script-snapshot states.

This closes the guarded collection-day return staging-plan block. The next
field state change must come from real measured DZT files and filled metadata
JSON files that pass paired preflight and guarded intake.

## Decision

Use runs `577-579` as the guarded field collection-day return staging-plan
block. Keep parser execution, provenance promotion, controlled field evidence,
field FWI, and field 3D/HPC blocked until real files pass paired preflight and
guarded intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_staging_plan_validation_sensitivity.py: pass
```

Figure check:

```text
3076x855, dynamic range=255
```
