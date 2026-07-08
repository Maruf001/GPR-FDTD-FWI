# Experiment 1649: 84-Grid Pilot Real-Result File Identity-Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1648` validator with controlled damaged variants of the
run `1647` artifacts.

The sensitivity set tests source damage, missing and duplicate file
identities, field-count damage, staging-directory damage, file promotion,
JSON-parse promotion, FDTD-execution promotion, downstream promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1649_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source contract ready:                     true
source validator ready:                    true
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
source damage rejected:                    true
identity damage rejected:                  true
directory damage rejected:                 true
file promotion rejected:                   true
parse promotion rejected:                  true
FDTD promotion rejected:                   true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
sensitivity ready:                         true
GPU priority:                              none
```

## Decision

Runs `1647-1649` are the guarded five-row pilot result-file identity block.
The next 2D implementation step remains writing real five-row pilot results
into the staging directory and rerunning acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_identity_contract_validation_sensitivity.py
2 passed
```

Figure check:

```text
2897x841, dynamic range=255
```
