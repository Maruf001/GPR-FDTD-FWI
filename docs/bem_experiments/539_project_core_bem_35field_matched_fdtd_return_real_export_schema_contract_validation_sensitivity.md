# BEM Experiment 539: Matched FDTD Return Real-Export Schema Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `538` validator.

The exact run `537` schema contract should pass. Damaged source readiness,
file counts, row-key counts, column counts, required value fields, real-file
promotion, real-value promotion, schema acceptance, template substitution,
action readiness, downstream promotion, figure damage, and script-snapshot
damage should fail.

## Output

```text
outputs/bem_experiments/539_project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     14
expected pass scenarios:                   1
expected failure scenarios:                13
unexpected scenarios:                      0
schema validation sensitivity ready:       true
exact source artifacts pass:               true
count or field damage rejected:            true
file or value promotion rejected:          true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
file_count_drift
key_count_drift
column_count_drift
value_field_damage
real_return_file_promotion
real_value_promotion
schema_acceptance_promotion
template_allowed_promotion
action_damage
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `537-539` as the guarded matched-FDTD real-export schema block. The
next BEM implementation task is a bounded real FDTD return exporter that writes
to this schema, not accepted comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validation_sensitivity.py
4 passed
```

Figure check:

```text
2897x839, dynamic range=255
```
