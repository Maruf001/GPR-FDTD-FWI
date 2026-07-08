# BEM Experiment 548: Matched FDTD Return Real-File Staging Scaffold Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `547` validator.

The exact run `546` artifacts should pass. Damaged source readiness, directory
count drift, missing directory, unexpected-file promotion, file count drift,
file presence, nonempty-file promotion, accepted-file promotion, action damage,
downstream promotion, figure damage, and script-snapshot damage should fail.

## Output

```text
outputs/bem_experiments/548_project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     14
expected pass scenarios:                   1
expected failure scenarios:                13
unexpected scenarios:                      0
staging scaffold sensitivity ready:        true
exact source artifacts pass:               true
directory damage rejected:                 true
file damage rejected:                      true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
real return packet accepted:               false
real BEM/FDTD comparison ready:            false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
directory_count_drift
directory_missing
unexpected_file_promotion
file_count_drift
file_present_promotion
file_nonempty_promotion
accepted_file_promotion
action_ready_promotion
action_count_drift
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `546-548` as the current matched-FDTD return-file staging scaffold.
The branch remains blocked on the two real FDTD return CSV files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_file_staging_scaffold_validation_sensitivity.py
4 passed
```

Figure check:

```text
2825x841, dynamic range=255
```
