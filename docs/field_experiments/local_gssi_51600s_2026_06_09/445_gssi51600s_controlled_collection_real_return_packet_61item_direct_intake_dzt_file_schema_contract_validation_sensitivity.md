# Field Experiment 445: Direct Intake DZT File Schema Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `444` validator.

The exact run `443` DZT contract should pass. Damaged source readiness, file
counts, family counts, check counts, family shape, check names, live-DZT
promotion, checksum promotion, parser promotion, metadata-link promotion,
schema acceptance, template substitution, action readiness, downstream
promotion, figure damage, and script-snapshot damage should fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/445_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     17
expected pass scenarios:                   1
expected failure scenarios:                16
unexpected scenarios:                      0
DZT validation sensitivity ready:          true
exact source artifacts pass:               true
count or shape damage rejected:            true
file or parser promotion rejected:         true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
dzt_file_count_drift
family_count_drift
check_count_drift
family_shape_damage
check_name_damage
live_dzt_file_promotion
sha256_promotion
header_parse_promotion
linked_metadata_promotion
schema_acceptance_promotion
template_allowed_promotion
action_damage
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `443-445` as the guarded DZT file schema block. The next field task is
not field FWI; it is a real-file intake or a combined metadata-plus-DZT
acceptance gate once actual measured files are available.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validation_sensitivity.py
4 passed
```

Figure check:

```text
3221x839, dynamic range=255
```
