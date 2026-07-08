# Field Experiment 444: Direct Intake DZT File Schema Contract Validator

Date: 2026-06-30

## Purpose

Validate run `443` from its artifacts.

The DZT schema contract should pass only when the nine DZT file rows, three
families, 54 required checks, blocked actions, nonblank figure, and script
snapshots are present while no live DZT files, parser acceptance, provenance
acceptance, archive acceptance, field FWI, or field 3D/HPC are promoted.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/444_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
DZT schema validation ready:               true
DZT files required:                        9
DZT file families:                         3
DZT check requirements:                    54
remaining DZT schema blockers:             4
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The five validation checks confirm:

```text
source_chain_ready                         pass
dzt_file_family_and_check_counts           pass
schema_is_contract_only                    pass
actions_and_downstream_states_blocked      pass
figure_and_script_snapshots_present        pass
```

## Decision

Use this validator as the artifact guard for run `443`. The next field task is
a validation-sensitivity run that proves damaged DZT contracts and premature
field-evidence promotion are rejected.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_dzt_file_schema_contract_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
