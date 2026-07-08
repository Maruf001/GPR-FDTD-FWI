# Experiment 1645: 84-Grid Pilot Real-Result File Staging-Scaffold Validator

Date: 2026-06-30

## Purpose

Validate run `1644` from its saved artifacts.

This run checks that the staging directory exists, the five required result
files remain absent, no unexpected files are present, and all downstream
physical or compute claims remain blocked.

## Output

```text
outputs/experiments/1645_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validator_validation_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                        5
validation passes:                        5
blocking failures:                        0
required directories:                     1
required result files:                    5
missing result files:                     5
staging actions:                          3
validation ready:                         true
GPU priority:                             none
```

## Decision

Run `1644` is a valid empty staging scaffold. It is ready to receive real
five-row pilot result files, but it does not itself provide evidence.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validator.py
3 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
