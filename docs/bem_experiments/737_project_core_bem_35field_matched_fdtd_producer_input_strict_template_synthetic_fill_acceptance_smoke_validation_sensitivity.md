# BEM Experiment 737: Strict-Template Synthetic Fill Acceptance Smoke Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `736` validator against damaged and prematurely promoted
synthetic positive-control states.

This run is validation sensitivity only. It does not execute FDTD, create real
BEM/FDTD evidence, write live producer input files, run 3D validation, launch
GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/737_project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
cases:                           15
expected passes:                 1
expected failures:               14
actual passes:                   1
actual failures:                 14
unexpected outcomes:             0
damaged cases:                   14
exporter execution ready:        false
GPU/HPC ready:                   false
field transfer ready:            false
sensitivity ready:               true
```

The exact run `735` state passes. The damaged cases fail as expected:

```text
source readiness loss
file row removal
input row count damage
accepted file count damage
accepted row count damage
validation error promotion
strict hash error promotion
synthetic-boundary damage
real-evidence promotion
exporter readiness promotion
GPU/HPC readiness promotion
field-transfer readiness promotion
figure damage
script-snapshot damage
```

## Interpretation

The positive-control validator is fail-closed for acceptance-count damage,
false real-evidence promotion, downstream promotion, and missing evidence
artifacts.

## Decision

Use runs `735-737` as output-local strict-acceptance positive-control coverage.
Real matched-FDTD producer input remains required before exporter execution or
scientific comparison.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_template_synthetic_fill_acceptance_smoke_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x855, dynamic range=255
```
