# BEM Experiment 715: Producer Input Template Acceptance Dry Run Validator

Date: 2026-06-30

## Purpose

Validate the saved run `714` acceptance dry-run.

The validator checks that row identities match the locked contract, blank
templates are rejected, all expected error families are present, live input
files remain absent, and exporter execution remains blocked.

This is CPU-only artifact validation. It does not run FDTD, execute the
exporter, create accepted return files, run a real BEM/FDTD comparison, launch
GPU/HPC work, transfer to field evidence, or promote 3D validation claims.

## Output

```text
outputs/bem_experiments/715_project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              7
checks passed:                       7
checks failed:                       0
template rows:                     558
row-identity matches:                2
accepted files:                      0
validation errors:                2790
live input files present:            0
exporter execution ready:        false
new FDTD executed:               false
GPU/HPC ready:                   false
```

## Interpretation

The dry-run result is valid. The template packet is structurally aligned with
the contract but remains deliberately non-accepted.

## Decision

Keep the exporter and comparison blocked until real matched-FDTD inputs pass
acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_template_acceptance_dry_run_validator.py
3 passed
```

Figure check:

```text
2465x857, dynamic range=255
```
