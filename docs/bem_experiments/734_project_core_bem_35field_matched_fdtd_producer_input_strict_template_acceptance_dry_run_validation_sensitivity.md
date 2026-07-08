# BEM Experiment 734: Strict-Template Producer Input Acceptance Dry Run Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `733` validator against damaged and prematurely promoted
strict-template dry-run states.

This run is validation sensitivity only. It does not execute FDTD, run
BEM/FDTD comparison, write live producer input files, run 3D validation, launch
GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/734_project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
cases:                           19
expected passes:                 1
expected failures:               18
actual passes:                   1
actual failures:                 18
unexpected outcomes:             0
damaged cases:                   18
exporter execution ready:        false
GPU/HPC ready:                   false
field transfer ready:            false
sensitivity ready:               true
```

The exact run `732` state passes. The damaged cases fail as expected:

```text
source readiness loss
file row removal
template row count damage
row identity damage
strict hash match damage
strict hash error promotion
blank value count damage
validation-pass promotion
accepted-row promotion
validation error count damage
error family row removal
error family count damage
live file promotion
exporter readiness promotion
GPU/HPC readiness promotion
field-transfer readiness promotion
figure damage
script-snapshot damage
```

## Interpretation

The validator is fail-closed for the strict-template dry-run boundary. It does
not accept contract-hash drift, false file acceptance, live-file promotion,
downstream promotion, or missing evidence artifacts.

## Decision

Use runs `732-734` as the current strict-template acceptance dry-run boundary.
Real matched-FDTD producer input remains required before exporter execution,
BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, or
field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_template_acceptance_dry_run_validation_sensitivity.py
3 passed
```

Figure check:

```text
2861x843, dynamic range=255
```
