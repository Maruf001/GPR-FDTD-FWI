# Experiment 1646: 84-Grid Pilot Real-Result File Staging-Scaffold Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1645` validator with controlled damaged copies of the
run `1644` artifacts.

The goal is to ensure that the validator does not accept damaged staging
states or premature promotion of the empty scaffold into physical evidence.

## Output

```text
outputs/experiments/1646_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source scaffold validation ready:          true
sensitivity scenarios:                    16
expected pass scenarios:                  1
expected failure scenarios:               15
unexpected scenarios:                     0
directory damage rejected:                true
file damage rejected:                     true
action damage rejected:                   true
downstream promotion rejected:            true
figure damage rejected:                   true
script-snapshot damage rejected:          true
validation sensitivity ready:             true
GPU priority:                             none
```

## Decision

Runs `1644-1646` are the current guarded five-row pilot result staging block.
The scaffold is valid, but every downstream claim remains blocked until real
pilot result JSON files are written and accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_staging_scaffold_validation_sensitivity.py
3 passed
```

Figure check:

```text
3077x841, dynamic range=255
```
