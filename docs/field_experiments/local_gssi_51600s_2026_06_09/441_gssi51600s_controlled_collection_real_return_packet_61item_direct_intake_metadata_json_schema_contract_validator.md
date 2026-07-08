# Field Experiment 441: Direct-Intake Metadata JSON Schema Contract Validator

Date: 2026-06-30

## Purpose

Validate run `440` from saved artifacts.

The validator checks source readiness, metadata-file and field-requirement
counts, contract-only state, blocked field-evidence states, actions, figure,
and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/441_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
metadata schema validation ready:          true
metadata JSON files:                       24
schema field requirements:                 129
remaining metadata blockers:               3
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Decision

Use run `441` as the artifact validator for the run `440` metadata schema
contract. The schema is validated as contract-only; no live metadata is present
or accepted.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_metadata_json_schema_contract_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
