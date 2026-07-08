# Experiment 1636: 84-Grid Pilot Real-Output Schema Contract Validator

Date: 2026-06-30

## Purpose

Validate run `1635` from its artifacts.

The schema contract should pass only when it is complete, contract-only, and
does not promote real execution, FDTD output, physical claims, GPU work, field
transfer, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1636_local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
schema-contract validation ready:          true
future pilot output files:                 5
required output fields:                    50
remaining output-schema blockers:          3
execution permitted:                       false
new FDTD executed:                         false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
GPU priority:                              none
```

The five validation checks confirm:

```text
source_chain_ready                         pass
output_file_and_field_counts               pass
schema_is_contract_only                    pass
actions_and_downstream_states_blocked      pass
figure_and_script_snapshots_present        pass
```

## Decision

Use this validator as the artifact guard for run `1635`. The next 2D step is a
validation-sensitivity run that proves the validator rejects damaged contracts
before any real pilot executor is implemented.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_output_schema_contract_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
