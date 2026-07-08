# Field Experiment 442: Direct-Intake Metadata JSON Schema Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `441` validator.

The exact run `440` schema contract should pass. Source damage, metadata-file
count drift, field-requirement count drift, schema-family damage, live-file
promotion, schema-acceptance promotion, template/synthetic allowance,
downstream promotion, action damage, figure damage, and script-snapshot damage
should fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/442_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
metadata schema sensitivity ready:         true
exact source artifacts pass:               true
count/schema damage rejected:              true
file/acceptance promotion rejected:        true
downstream promotion rejected:             true
action damage rejected:                    true
figure damage rejected:                    true
script-snapshot damage rejected:           true
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Decision

Use runs `440-442` as the guarded metadata JSON schema contract block. Real
metadata files still need to be written before parser, provenance, archive, or
field FWI work can proceed.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validation_sensitivity.py
4 passed
```

Figure check:

```text
2717x839, dynamic range=255
```
