# BEM Experiment 538: Matched FDTD Return Real-Export Schema Contract Validator

Date: 2026-06-30

## Purpose

Validate run `537` from its artifacts.

The schema contract should pass only when the two return files, 558 row keys,
22 required columns, blocked actions, nonblank figure, and script snapshots are
present while no real FDTD values or accepted comparison evidence are promoted.

## Output

```text
outputs/bem_experiments/538_project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validator_checks.csv
data/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
schema-contract validation ready:          true
future FDTD return files:                  2
required FDTD return rows:                 558
required return columns:                   22
remaining schema blockers:                 4
accepted evidence ready:                   false
real BEM/FDTD comparison ready:            false
3D validation claim ready:                 false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

The five validation checks confirm:

```text
source_chain_ready                         pass
file_key_and_column_contract               pass
schema_is_contract_only                    pass
actions_and_downstream_states_blocked      pass
figure_and_script_snapshots_present        pass
```

## Decision

Use this validator as the artifact guard for run `537`. The next BEM step is a
validation-sensitivity run that proves the validator rejects damaged schemas or
premature evidence promotion.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_export_schema_contract_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
