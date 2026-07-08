# Experiment 1648: 84-Grid Pilot Real-Result File Identity-Contract Validator

Date: 2026-06-30

## Purpose

Validate run `1647` from its saved artifacts.

This run checks that the five file identities are unique, that each file has
the same ten-field required schema, that the staging directory is present, and
that no real file, parser state, FDTD execution, physical claim, GPU work,
field transfer, or 3D/HPC state has been promoted.

## Output

```text
outputs/experiments/1648_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
required file identities:                  5
unique file identities:                    5
required fields:                           50
identity actions:                          4
identity validation ready:                 true
GPU priority:                              none
```

## Decision

Run `1647` validates as the current five-row pilot result-file identity lock.
It still accepts no staged real results.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validator.py
4 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
