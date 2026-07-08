# BEM Experiment 581: Matched FDTD Input-Bound Exporter Real-Input Staging Intake Manifest Validator

Date: 2026-06-30

## Purpose

Validate the run `580` four-file intake manifest from saved artifacts.

This run checks source readiness, manifest shape, file acceptance state,
action/downstream blocking, and figure/script artifacts.

## Output

```text
outputs/bem_experiments/581_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validator.png
scripts/
```

## Result

```text
validation checks:                        5
passed checks:                            5
failed checks:                            0
manifest rows:                            4
present staged files:                     0
accepted files:                           0
actions:                                  4
exporter execution ready:                 false
real BEM/FDTD comparison ready:           false
3D validation claim ready:                false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
gpu priority:                             none
```

The five validation checks all pass:

```text
source manifest ready
four row manifest shape
no files accepted or promoted
actions and downstream blocked
figure and scripts exist
```

## Interpretation

The four-file intake manifest is valid and empty. It does not yet provide real
matched-FDTD input files, accepted return files, or comparison evidence.

## Decision

Use run `581` as the artifact guard for the run `580` intake manifest. Keep
exporter execution and BEM/FDTD comparison blocked until real input CSV files
exist and pass acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validator.py

6 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
