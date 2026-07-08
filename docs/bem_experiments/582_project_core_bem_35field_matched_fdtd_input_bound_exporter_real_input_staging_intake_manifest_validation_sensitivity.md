# BEM Experiment 582: Matched FDTD Input-Bound Exporter Real-Input Staging Intake Manifest Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `581` intake-manifest validator with controlled damage to
the run `580` artifacts.

This run checks that the validator fails when manifest identity, file
promotion, action readiness, downstream readiness, figure metadata, or script
snapshots are damaged.

## Output

```text
outputs/bem_experiments/582_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       13
expected pass cases:                     1
expected fail cases:                     12
actual pass cases:                       1
actual fail cases:                       12
unexpected cases:                        0
damaged cases:                           12
exporter execution ready:                false
real BEM/FDTD comparison ready:          false
3D validation claim ready:               false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

The exact source manifest passes. Damaged states fail for:

```text
source readiness removal
manifest row removal
input/return role-count damage
file-key damage
staged-file presence promotion
file-acceptance promotion
exporter-readiness promotion
comparison-readiness promotion
action-readiness promotion
BEM/FDTD comparison promotion
figure damage
missing script snapshots
```

## Interpretation

The intake-manifest validator is sensitive to the intended failure modes. It
cannot silently promote missing staged files, accepted returns, exporter
execution, or BEM/FDTD comparison readiness.

## Decision

Use runs `580-582` as the guarded four-file BEM/FDTD intake-manifest block.
Exporter execution and comparison remain blocked until real input files pass
acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validator.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_intake_manifest_validation_sensitivity.py

9 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
