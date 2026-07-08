# Field Experiment 573: Trace-Pairing Collection-Day Return Package Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `572` validator for the controlled field collection-day
template pack.

This run does not create fake DZT files, does not place files in the live-return
area, does not accept any field evidence, does not run a parser, does not run
field FWI, and does not run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/573_gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
sensitivity scenarios:           12
expected pass scenarios:         1
expected fail scenarios:         11
observed pass scenarios:         1
observed fail scenarios:         11
unexpected outcomes:             0
damaged scenarios:               11
damaged scenarios rejected:      11
gpu priority:                    none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source not ready | fail | fail | source template pack ready |
| item count damage | fail | fail | thirty-three package items represented |
| metadata template damage | fail | fail | metadata templates written without DZT placeholders |
| DZT placeholder damage | fail | fail | metadata templates written without DZT placeholders |
| stage shape damage | fail | fail | stage package shape is preserved |
| template nonblank damage | fail | fail | templates remain blank and unaccepted |
| false live acceptance | fail | fail | templates remain blank and unaccepted |
| capture ready damage | fail | fail | capture rows exist but field analysis remains blocked |
| field FWI promotion | fail | fail | capture rows exist but field analysis remains blocked |
| figure damage | fail | fail | figure and script snapshots are present |
| snapshot damage | fail | fail | figure and script snapshots are present |

## Interpretation

The template-pack validator accepts only the exact saved run `571` state. It
rejects damaged source readiness, item-count drift, missing metadata templates,
fake DZT placeholders, stage-shape drift, nonblank templates, false live-return
acceptance, false capture-row readiness, false field-FWI promotion, damaged
figure validation, and missing script snapshots.

## Decision

Use runs `571-573` as the guarded field collection-day template-pack block.
Real parser and field-FWI work remain blocked until real measured files and
filled metadata pass the guarded intake path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.py: pass
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_package_template_pack_validation_sensitivity.py: pass
```

Figure check:

```text
2572x861, dynamic range=255
```
