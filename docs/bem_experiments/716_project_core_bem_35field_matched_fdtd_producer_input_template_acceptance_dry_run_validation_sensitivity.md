# BEM Experiment 716: Producer Input Template Acceptance Dry Run Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `715` validator.

The sensitivity cases check whether the validator rejects source damage,
file-count damage, error-family damage, row-identity drift, false validation
acceptance, validation-error count drift, live-file promotion, false exporter
readiness, false FDTD/GPU readiness, damaged figures, and missing script
snapshots.

This is CPU-only validation sensitivity. It does not run FDTD, execute the
exporter, create accepted return files, run a real BEM/FDTD comparison, launch
GPU/HPC work, transfer to field evidence, or promote 3D validation claims.

## Output

```text
outputs/bem_experiments/716_project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                              14
expected pass cases:                 1
expected fail cases:                13
actual pass cases:                   1
actual fail cases:                  13
unexpected cases:                    0
damaged cases:                      13
exporter execution ready:        false
new FDTD executed:               false
GPU/HPC ready:                   false
```

## Interpretation

The validator accepts only the exact non-evidence rejection state. It rejects
false evidence, false live-file presence, and false exporter/GPU readiness.

## Decision

Use runs `714-716` as the guarded acceptance dry-run block for the producer
input templates.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validation_sensitivity.py
3 passed
```

Figure check:

```text
2609x855, dynamic range=255
```
