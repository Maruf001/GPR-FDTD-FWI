# BEM Experiment 579: Matched FDTD Input-Bound Exporter Real-Input Staging Scaffold Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `578` staging-scaffold validator with controlled damage to
the run `577` artifacts.

This run checks that the validator fails when source readiness, staging
directory shape, file obligations, action state, downstream state, figure
metadata, or script snapshots are damaged.

## Output

```text
outputs/bem_experiments/579_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validation_sensitivity.png
scripts/
```

## Result

```text
source scaffold validation ready:         true
sensitivity scenarios:                    16
expected pass scenarios:                  1
expected failure scenarios:               15
unexpected scenarios:                     0
exact source artifacts pass:              true
directory damage rejected:                true
file damage rejected:                     true
action damage rejected:                   true
downstream promotion rejected:            true
figure damage rejected:                   true
script snapshot damage rejected:          true
exporter execution ready:                 false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
gpu priority:                             none
```

The exact source scaffold passes. Damaged states fail for:

```text
source-chain readiness removal
directory-count drift
directory absence
unexpected-file promotion
staged-file-count drift
real-input file-count drift
accepted-return file-count drift
staged-file presence promotion
nonempty-file promotion
accepted-file promotion
action readiness promotion
action-count drift
BEM/FDTD comparison promotion
figure damage
missing script snapshots
```

## Interpretation

The staging scaffold validator is sensitive to the intended failure modes. It
cannot silently treat staged files, accepted returns, exporter execution, or
BEM/FDTD comparison as ready from an empty scaffold.

## Decision

Use runs `577-579` as the current guarded input-bound matched-FDTD staging
block. The next BEM handoff step still requires real matched-FDTD input CSV
files; no exporter execution or comparison is justified from the scaffold alone.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_scaffold_validation_sensitivity.py

10 passed
```

Figure validation:

```text
2933x853, dynamic range=255
```
